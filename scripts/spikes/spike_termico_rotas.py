"""
Spike 3 — Indicadores térmicos por rota (o diferencial do Feneme).

Reaproveita o spike 2 (spike_regras_rotas.py, na MESMA pasta): usa as mesmas CIDADES_LISTA,
PARES e regras RN-01..RN-06 para escolher as rotas e, para cada rota escolhida:

  1. amostra pontos a cada PASSO_KM ao longo do percurso;
  2. estima o horário de passagem em cada ponto (saída + fração da duração);
  3. consulta a previsão horária da Open-Meteo (temperature_2m) nesses pontos;
  4. calcula: temperatura máxima, média ponderada pelo tempo, minutos acima do limite
     da carga e exposição térmica em grau-hora;
  5. destaca a rota de menor exposição (empate -> menor tempo);
  6. compara HORARIOS_COMPARAR na rota mais rápida (mesma rota, saídas diferentes).

Uso (PowerShell):
    $env:GOOGLE_MAPS_API_KEY="chave-routes"
    $env:GOOGLE_MAPS_JS_KEY="chave-maps"      # opcional, para gerar mapa_termico.html
    python spike_termico_rotas.py
    python -m http.server 8000   ->  http://localhost:8000/mapa_termico.html

O limite usado vem do catálogo inicial de cargas (docs/produto/escopo-r3-r4.md).
Código de spike: descartável. Não versionar mapa_termico.html (contém a chave do mapa).
"""

import datetime as dt
import json
import os
import pathlib
import sys
import urllib.parse
import urllib.request

import spike_regras_rotas as base

# ------------------------------------------------------------------ CONFIGURAÇÃO

# Tipo de carga do catálogo inicial (US-15, FT-114). Troque pelo item desejado.
CARGA = {
    "tipo": "Frangos de corte (5–6 semanas)",
    "limite_c": 23.0,  # Embrapa Suínos e Aves, IT 37 — ver docs/produto/escopo-r3-r4.md
}

AMANHA = (dt.date.today() + dt.timedelta(days=1)).isoformat()
DATA_SAIDA = AMANHA            # "AAAA-MM-DD" (previsão cobre poucos dias à frente)
HORARIO_SAIDA = "11:00"        # horário principal da comparação entre rotas
HORARIOS_COMPARAR = ["05:00", "11:00", "15:00"]  # mesma rota, saídas diferentes

PASSO_KM = 10.0                # 1 ponto de temperatura a cada X km
EMPATE_GRAU_HORA = 0.5         # diferença abaixo disso = empate -> desempata por tempo
DIAS_PREVISAO = 3              # dias consultados na Open-Meteo a partir de hoje
FUSO = "America/Sao_Paulo"

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
LOTE_PONTOS = 40               # pontos por requisição multi-localização

# ------------------------------------------------------------------ PREVISÃO


def pontos_com_fracao(rota):
    """Amostra a polilinha a cada PASSO_KM e devolve [(lat, lon, fração_do_percurso)]."""
    pts = rota["pontos"]
    if len(pts) < 2:
        return [(pts[0][0], pts[0][1], 0.0)] if pts else []
    acumulado = [0.0]
    for a, b in zip(pts, pts[1:]):
        acumulado.append(acumulado[-1] + base.haversine_km(a, b))
    total = acumulado[-1] or 1.0
    saida, proximo = [], 0.0
    for p, d in zip(pts, acumulado):
        if d >= proximo:
            saida.append((p[0], p[1], d / total))
            proximo = d + PASSO_KM
    if saida[-1][2] < 1.0:
        saida.append((pts[-1][0], pts[-1][1], 1.0))
    return saida


def buscar_series(pontos):
    """Previsão horária (temperature_2m) para vários pontos; uma série por ponto."""
    series = []
    for i in range(0, len(pontos), LOTE_PONTOS):
        lote = pontos[i:i + LOTE_PONTOS]
        query = urllib.parse.urlencode({
            "latitude": ",".join(f"{p[0]:.4f}" for p in lote),
            "longitude": ",".join(f"{p[1]:.4f}" for p in lote),
            "hourly": "temperature_2m",
            "timezone": FUSO,
            "forecast_days": DIAS_PREVISAO,
        })
        with urllib.request.urlopen(f"{FORECAST_URL}?{query}", timeout=30) as resp:
            dados = json.load(resp)
        if isinstance(dados, dict):  # resposta de ponto único vem como objeto
            dados = [dados]
        for d in dados:
            horas = [dt.datetime.fromisoformat(t) for t in d["hourly"]["time"]]
            series.append((horas, d["hourly"]["temperature_2m"]))
    return series


def temperatura_em(serie, instante):
    """Interpola linearmente a temperatura no instante; None se fora da previsão."""
    horas, temps = serie
    for i in range(len(horas) - 1):
        if horas[i] <= instante <= horas[i + 1]:
            t0, t1 = temps[i], temps[i + 1]
            if t0 is None or t1 is None:
                return None
            frac = (instante - horas[i]).total_seconds() / 3600
            return t0 + (t1 - t0) * frac
    return None


# ------------------------------------------------------------------ INDICADORES


def indicadores(rota, amostras, series, saida, limite):
    """Calcula os indicadores térmicos para uma saída; None se faltar previsão."""
    duracao_h = rota["min"] / 60
    temps = []
    for (_, _, frac), serie in zip(amostras, series):
        t = temperatura_em(serie, saida + dt.timedelta(hours=duracao_h * frac))
        if t is None:
            return None
        temps.append(t)

    soma_ponderada = minutos_acima = grau_hora = 0.0
    for i in range(len(amostras) - 1):
        dt_h = duracao_h * (amostras[i + 1][2] - amostras[i][2])
        t_meio = (temps[i] + temps[i + 1]) / 2
        soma_ponderada += t_meio * dt_h
        if t_meio > limite:
            minutos_acima += dt_h * 60
            grau_hora += (t_meio - limite) * dt_h
    return {
        "max": max(temps),
        "media": soma_ponderada / duracao_h if duracao_h else temps[0],
        "min_acima": minutos_acima,
        "grau_hora": grau_hora,
        "temps": temps,
    }


def destacar(avaliadas):
    """Índice da rota destacada: menor grau-hora; empate -> menor tempo; tudo zero -> menor média."""
    validas = [(i, r) for i, r in enumerate(avaliadas) if r["ind"]]
    if not validas:
        return None
    if all(r["ind"]["grau_hora"] == 0 for _, r in validas):
        return min(validas, key=lambda x: x[1]["ind"]["media"])[0]
    menor = min(r["ind"]["grau_hora"] for _, r in validas)
    empatadas = [(i, r) for i, r in validas if r["ind"]["grau_hora"] - menor < EMPATE_GRAU_HORA]
    return min(empatadas, key=lambda x: x[1]["rota"]["min"])[0]


def saida_em(horario):
    return dt.datetime.fromisoformat(f"{DATA_SAIDA}T{horario}")


def fmt(ind):
    if not ind:
        return "sem previsão para esse horário/data"
    return (f"máx {ind['max']:4.1f} °C | média {ind['media']:4.1f} °C | "
            f"acima do limite {ind['min_acima']:4.0f} min | {ind['grau_hora']:5.1f} grau-hora")


# ------------------------------------------------------------------ EXECUÇÃO


def analisar_par(chave_api, origem, destino):
    resultado = base.avaliar_par(chave_api, origem, destino)
    if not resultado:
        return None
    limite = CARGA["limite_c"]
    print(f"\n  --- Térmico | carga: {CARGA['tipo']} | limite {limite} °C | saída {DATA_SAIDA} {HORARIO_SAIDA}")

    avaliadas = []
    for rota in resultado["rotas"]:
        amostras = pontos_com_fracao(rota)
        series = buscar_series(amostras)
        avaliadas.append({
            "rota": rota, "amostras": amostras, "series": series,
            "ind": indicadores(rota, amostras, series, saida_em(HORARIO_SAIDA), limite),
        })

    estrela = destacar(avaliadas)
    for i, a in enumerate(avaliadas):
        marca = "  <- MENOR EXPOSIÇÃO" if i == estrela else ""
        print(f"  Rota {i + 1} ({a['rota']['km']:.0f} km, {a['rota']['min']:.0f} min): {fmt(a['ind'])}{marca}")

    validas = [a["ind"]["grau_hora"] for a in avaliadas if a["ind"]]
    if len(validas) > 1:
        print(f"  Diferença de exposição entre a melhor e a pior rota: {max(validas) - min(validas):.1f} grau-hora")

    # Mesma rota (a mais rápida), horários de saída diferentes
    rapida = min(avaliadas, key=lambda a: a["rota"]["min"])
    comparacao_horarios = []
    print("  --- Mesma rota (mais rápida), saídas diferentes:")
    for h in HORARIOS_COMPARAR:
        ind = indicadores(rapida["rota"], rapida["amostras"], rapida["series"], saida_em(h), limite)
        comparacao_horarios.append({"horario": h, "ind": ind})
        print(f"  Saída {h}: {fmt(ind)}")

    resultado["termico"] = {
        "estrela": estrela,
        "rotas": [
            {"ind": a["ind"], "amostras": [[p[0], p[1]] for p in a["amostras"]]} for a in avaliadas
        ],
        "horarios": comparacao_horarios,
    }
    return resultado


HTML = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Feneme — comparação térmica (spike)</title>
<style>
 body{margin:0;font-family:system-ui,sans-serif;display:flex;height:100vh}
 #painel{width:380px;padding:16px;overflow:auto;border-right:1px solid #ddd}
 #mapa{flex:1} select{width:100%;padding:6px;margin:8px 0}
 .rota{border-left:6px solid;padding:8px 10px;margin:8px 0;background:#f6f6f6;cursor:pointer;font-size:14px}
 .selo{background:#0f9d58;color:#fff;border-radius:4px;padding:1px 6px;font-size:12px}
 .aviso{background:#fff4e5;border:1px solid #f0b37e;padding:8px;margin-top:8px;font-size:13px}
 table{border-collapse:collapse;width:100%;font-size:13px;margin-top:6px} td,th{border-bottom:1px solid #ddd;padding:4px;text-align:left}
 small{color:#666}
</style></head><body>
<div id="painel"><h3 style="margin:0">Feneme — rotas e exposição ao calor</h3>
<small>Spike. Temperatura = previsão do ambiente (Open-Meteo), não da carga.</small>
<div style="margin-top:8px;font-size:14px">Carga: <b>__CARGA__</b><br>Limite: <b>__LIMITE__ °C</b> · Saída: <b>__SAIDA__</b></div>
<select id="par"></select><div id="lista"></div><div id="aviso"></div>
<h4 style="margin:16px 0 0">Mesma rota, outros horários de saída</h4><div id="horarios"></div>
<p><small>Pontos vermelhos: trechos acima do limite da carga no horário estimado de passagem.</small></p></div>
<div id="mapa"></div>
<script>
const DADOS = __DADOS__, CORES = ["#1a73e8","#e8710a","#9334e6"], LIMITE = __LIMITE__;
let mapa, objs = [];
const f = (v,d=1)=>v==null?'–':v.toFixed(d);
function mostrar(i){
  objs.forEach(o=>o.setMap(null)); objs=[];
  const par = DADOS[i], lim = new google.maps.LatLngBounds(), lista = document.getElementById('lista');
  lista.innerHTML='';
  par.rotas.forEach((r,k)=>{
    const t = par.termico.rotas[k], ind = t.ind;
    const caminho = r.pontos.map(p=>({lat:p[0],lng:p[1]})); caminho.forEach(p=>lim.extend(p));
    const linha = new google.maps.Polyline({path:caminho,strokeColor:CORES[k],strokeOpacity:.8,strokeWeight:k===0?7:5,zIndex:10-k,map:mapa});
    objs.push(linha);
    if(ind) t.amostras.forEach((p,j)=>{ const quente = ind.temps[j] > LIMITE;
      objs.push(new google.maps.Circle({center:{lat:p[0],lng:p[1]},radius:quente?900:500,
        fillColor:quente?'#d93025':CORES[k],fillOpacity:.9,strokeWeight:0,zIndex:20,map:mapa})); });
    const div = document.createElement('div'); div.className='rota'; div.style.borderColor=CORES[k];
    const selo = par.termico.estrela===k?' <span class="selo">Menor exposição ao calor</span>':'';
    div.innerHTML = `<b>Rota ${k+1}</b>${selo}<br>${r.km.toFixed(1)} km · ${Math.round(r.min)} min · <small>${r.descricao||''}</small><br>`+
      (ind?`Máx <b>${f(ind.max)} °C</b> · Média ${f(ind.media)} °C<br>Acima do limite: <b>${Math.round(ind.min_acima)} min</b> · ${f(ind.grau_hora)} grau-hora`
          :'<i>Sem previsão para essa data/horário</i>');
    lista.appendChild(div);
  });
  [['A',par.origem],['B',par.destino]].forEach(([t,c])=>objs.push(new google.maps.Marker({position:{lat:c[0],lng:c[1]},label:t,map:mapa})));
  document.getElementById('aviso').innerHTML = par.aviso?`<div class="aviso">${par.aviso}</div>`:'';
  document.getElementById('horarios').innerHTML = '<table><tr><th>Saída</th><th>Máx</th><th>Acima</th><th>Grau-h</th></tr>'+
    par.termico.horarios.map(h=>`<tr><td>${h.horario}</td><td>${h.ind?f(h.ind.max)+' °C':'–'}</td><td>${h.ind?Math.round(h.ind.min_acima)+' min':'–'}</td><td>${h.ind?f(h.ind.grau_hora):'–'}</td></tr>`).join('')+'</table>';
  mapa.fitBounds(lim, 40);
}
function iniciar(){
  mapa = new google.maps.Map(document.getElementById('mapa'),{center:{lat:-7.2,lng:-35.9},zoom:8});
  const sel = document.getElementById('par'); DADOS.forEach((p,i)=>sel.add(new Option(p.rotulo,i)));
  sel.onchange=()=>mostrar(sel.value); mostrar(0);
}
</script>
<script async src="https://maps.googleapis.com/maps/api/js?key=__CHAVE__&callback=iniciar"></script>
</body></html>"""


def gerar_mapa(resultados):
    chave_mapa = os.environ.get("GOOGLE_MAPS_JS_KEY")
    if not chave_mapa:
        print("\nMapa não gerado: defina GOOGLE_MAPS_JS_KEY (chave restrita à Maps JavaScript API).")
        return
    html = (HTML.replace("__DADOS__", json.dumps(resultados, ensure_ascii=False))
            .replace("__CARGA__", CARGA["tipo"])
            .replace("__LIMITE__", str(CARGA["limite_c"]))
            .replace("__SAIDA__", f"{DATA_SAIDA} {HORARIO_SAIDA}")
            .replace("__CHAVE__", urllib.parse.quote(chave_mapa)))
    pathlib.Path("mapa_termico.html").write_text(html, encoding="utf-8")
    print("\nMapa gerado: mapa_termico.html — rode  python -m http.server 8000  e acesse "
          "http://localhost:8000/mapa_termico.html  (NÃO versionar: contém a chave do mapa)")


def main():
    chave_api = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not chave_api:
        sys.exit("Defina a variável de ambiente GOOGLE_MAPS_API_KEY.")
    base.SAIDA.mkdir(exist_ok=True)
    print(f"Carga: {CARGA['tipo']} | limite {CARGA['limite_c']} °C | saída {DATA_SAIDA} {HORARIO_SAIDA}")
    resultados = []
    for origem, destino in base.PARES:
        try:
            r = analisar_par(chave_api, origem, destino)
            if r:
                resultados.append(r)
        except Exception as erro:
            print(f"  ERRO: {erro}")
    if resultados:
        gerar_mapa(resultados)


if __name__ == "__main__":
    main()

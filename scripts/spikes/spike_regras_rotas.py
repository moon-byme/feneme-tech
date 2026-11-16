"""
Spike 2 — Valida as regras de negócio de seleção de rotas do Feneme (RN-01 a RN-06)
usando a Google Routes API e a geocodificação gratuita da Open-Meteo.

Uso:
    PowerShell: $env:GOOGLE_MAPS_API_KEY="sua-chave"
    bash:       export GOOGLE_MAPS_API_KEY="sua-chave"
    python spike_regras_rotas.py

Preencha CIDADES_LISTA com a MESMA lista de cidades usada na previsão do clima
e PARES com os trajetos a testar. Os parâmetros das regras ficam em PARAMS,
para o PO calibrar sem mexer na lógica.

Código de spike: descartável, não vai para a main como funcionalidade.
Respostas brutas são salvas em ./spike2_respostas/ (sem a chave).
"""

import json
import math
import os
import pathlib
import sys
import urllib.parse
import urllib.request

# ------------------------------------------------------------------ CONFIGURAÇÃO

# Lista fixa de cidades do Feneme (nome, UF) — mesma lista da US-14 (FT-113)
CIDADES_LISTA = [
    ("João Pessoa", "PB"), ("Campina Grande", "PB"), ("Patos", "PB"),
    ("Recife", "PE"), ("Caruaru", "PE"), ("Serra Talhada", "PE"), ("Petrolina", "PE"),
    ("Natal", "RN"), ("Mossoró", "RN"),
    ("Fortaleza", "CE"), ("Juazeiro do Norte", "CE"),
    ("Maceió", "AL"), ("Arapiraca", "AL"),
    ("Aracaju", "SE"),
    ("Salvador", "BA"), ("Feira de Santana", "BA"), ("Juazeiro", "BA"), ("Vitória da Conquista", "BA"),
    ("Teresina", "PI"),
    ("São Luís", "MA"),
    ("Montes Claros", "MG"), ("Belo Horizonte", "MG"),
    ("São Paulo", "SP"),
    ("Rio de Janeiro", "RJ"),
    ("Brasília", "DF"),
    ("Goiânia", "GO"),
]

# Pares (origem, destino) a testar — devem pertencer à lista acima
PARES = [
    (("Campina Grande", "PB"), ("Caruaru", "PE")),
    (("Campina Grande", "PB"), ("João Pessoa", "PB")),
    (("Campina Grande", "PB"), ("Recife", "PE")),
]

PARAMS = {
    "distancia_minima_km": 50,        # RN-01
    "fator_duracao_max": 1.5,         # RN-02 (x duração da rota mais rápida)
    "sobreposicao_max": 0.60,         # RN-03 (fração do percurso compartilhado)
    "raio_sobreposicao_km": 1.0,      # RN-03 (tolerância para considerar "mesmo trecho")
    "passo_amostragem_km": 1.0,       # RN-03 (amostra 1 ponto a cada X km)
    "fator_desvio_linha_reta": 1.4,   # RN-04 (pré-filtro de cidade intermediária)
    "max_chamadas_waypoint": 3,       # RN-04
    "rotas_exibidas": 3,              # RN-05 / RN-06
}

ROUTES_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FIELD_MASK = (
    "routes.distanceMeters,routes.duration,routes.routeLabels,"
    "routes.description,routes.polyline.encodedPolyline"
)
SAIDA = pathlib.Path("spike2_respostas")

UFS = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas", "BA": "Bahia",
    "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo", "GO": "Goiás",
    "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul", "MG": "Minas Gerais",
    "PA": "Pará", "PB": "Paraíba", "PR": "Paraná", "PE": "Pernambuco", "PI": "Piauí",
    "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte", "RS": "Rio Grande do Sul",
    "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina", "SP": "São Paulo",
    "SE": "Sergipe", "TO": "Tocantins",
}

contador_chamadas = 0

# ------------------------------------------------------------------ GEOMETRIA


def haversine_km(a, b):
    lat1, lon1, lat2, lon2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(h))


def decodificar_polilinha(texto):
    """Decodifica o formato Encoded Polyline do Google em [(lat, lon), ...]."""
    pontos, i, lat, lon = [], 0, 0, 0
    while i < len(texto):
        valores = []
        for _ in range(2):
            resultado, deslocamento = 0, 0
            while True:
                b = ord(texto[i]) - 63
                i += 1
                resultado |= (b & 0x1F) << deslocamento
                deslocamento += 5
                if b < 0x20:
                    break
            valores.append(~(resultado >> 1) if resultado & 1 else resultado >> 1)
        lat += valores[0]
        lon += valores[1]
        pontos.append((lat / 1e5, lon / 1e5))
    return pontos


def amostrar(pontos, passo_km):
    """Mantém um ponto a cada `passo_km` ao longo da polilinha (aproximação)."""
    if not pontos:
        return []
    amostra, acumulado = [pontos[0]], 0.0
    for anterior, atual in zip(pontos, pontos[1:]):
        acumulado += haversine_km(anterior, atual)
        if acumulado >= passo_km:
            amostra.append(atual)
            acumulado = 0.0
    if amostra[-1] != pontos[-1]:
        amostra.append(pontos[-1])
    return amostra


def distancia_ponto_segmento_km(p, a, b):
    """Distância de p ao segmento ab, em projeção equiretangular local."""
    lat0 = math.radians(p[0])

    def xy(q):
        return (math.radians(q[1]) * math.cos(lat0) * 6371.0, math.radians(q[0]) * 6371.0)

    px, py = xy(p)
    ax, ay = xy(a)
    bx, by = xy(b)
    dx, dy = bx - ax, by - ay
    comprimento2 = dx * dx + dy * dy
    t = 0.0 if comprimento2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / comprimento2))
    cx, cy = ax + t * dx, ay + t * dy
    return math.hypot(px - cx, py - cy)


def sobreposicao(rota_b, rota_a):
    """RN-03: fração dos pontos amostrados de B que estão a <= raio de A."""
    amostra_b = amostrar(rota_b["pontos"], PARAMS["passo_amostragem_km"])
    segmentos_a = list(zip(rota_a["pontos"], rota_a["pontos"][1:]))
    if not amostra_b or not segmentos_a:
        return 0.0
    raio = PARAMS["raio_sobreposicao_km"]
    proximos = sum(
        1 for p in amostra_b
        if any(distancia_ponto_segmento_km(p, a, b) <= raio for a, b in segmentos_a)
    )
    return proximos / len(amostra_b)


def lado_da_reta(origem, destino, ponto):
    """+1 / -1 conforme o lado da linha origem→destino em que o ponto está."""
    cruz = (destino[1] - origem[1]) * (ponto[0] - origem[0]) - (destino[0] - origem[0]) * (ponto[1] - origem[1])
    return 1 if cruz > 0 else -1


# ------------------------------------------------------------------ APIs


def geocodificar(cidade, uf, cache={}):
    chave = (cidade, uf)
    if chave in cache:
        return cache[chave]
    query = urllib.parse.urlencode(
        {"name": cidade, "count": 10, "language": "pt", "countryCode": "BR", "format": "json"}
    )
    with urllib.request.urlopen(f"{GEOCODE_URL}?{query}", timeout=15) as resp:
        resultados = json.load(resp).get("results", [])
    estado = UFS.get(uf.upper())
    for r in resultados:
        if estado is None or r.get("admin1") == estado:
            cache[chave] = (r["latitude"], r["longitude"])
            return cache[chave]
    raise ValueError(f"Cidade não encontrada: {cidade}/{uf}")


def ponto_api(coord, via=False):
    p = {"location": {"latLng": {"latitude": coord[0], "longitude": coord[1]}}}
    if via:
        p["via"] = True
    return p


def chamar_routes(chave_api, origem, destino, waypoint=None):
    global contador_chamadas
    corpo = {
        "origin": ponto_api(origem),
        "destination": ponto_api(destino),
        "travelMode": "DRIVE",
        "computeAlternativeRoutes": waypoint is None,
        "languageCode": "pt-BR",
        "units": "METRIC",
    }
    if waypoint is not None:
        corpo["intermediates"] = [ponto_api(waypoint, via=True)]
    req = urllib.request.Request(
        ROUTES_URL,
        data=json.dumps(corpo).encode(),
        headers={"Content-Type": "application/json", "X-Goog-Api-Key": chave_api, "X-Goog-FieldMask": FIELD_MASK},
        method="POST",
    )
    contador_chamadas += 1
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.load(resp)


def normalizar(rota_api, origem_rota):
    return {
        "origem_rota": origem_rota,
        "km": rota_api.get("distanceMeters", 0) / 1000,
        "min": int(rota_api.get("duration", "0s").rstrip("s")) / 60,
        "descricao": rota_api.get("description", ""),
        "pontos": decodificar_polilinha(rota_api.get("polyline", {}).get("encodedPolyline", "")),
    }


# ------------------------------------------------------------------ REGRAS


def filtrar(candidatas, mais_rapida, aceitas, descartes):
    """Aplica RN-02 (viabilidade) e RN-03 (distinção) às candidatas."""
    for c in candidatas:
        limite = mais_rapida["min"] * PARAMS["fator_duracao_max"]
        if c["min"] > limite:
            descartes.append((c, f"RN-02: {c['min']:.0f} min > {limite:.0f} min"))
            continue
        maior = max((sobreposicao(c, a) for a in aceitas), default=0.0)
        if maior > PARAMS["sobreposicao_max"]:
            descartes.append((c, f"RN-03: sobreposição {maior:.0%} > {PARAMS['sobreposicao_max']:.0%}"))
            continue
        aceitas.append(c)


def selecionar(aceitas):
    """RN-05: mais rápida primeiro; depois a de menor sobreposição com as já escolhidas."""
    escolhidas = [min(aceitas, key=lambda r: r["min"])]
    restantes = [r for r in aceitas if r is not escolhidas[0]]
    while restantes and len(escolhidas) < PARAMS["rotas_exibidas"]:
        proxima = min(restantes, key=lambda r: max(sobreposicao(r, e) for e in escolhidas))
        escolhidas.append(proxima)
        restantes.remove(proxima)
    return escolhidas


def candidatas_intermediarias(origem_nome, destino_nome, origem, destino):
    """RN-04: pré-filtro por linha reta e alternância de lados da reta origem→destino."""
    reta = haversine_km(origem, destino)
    lados = {1: [], -1: []}
    for nome in CIDADES_LISTA:
        if nome in (origem_nome, destino_nome):
            continue
        c = geocodificar(*nome)
        fator = (haversine_km(origem, c) + haversine_km(c, destino)) / reta
        if fator <= PARAMS["fator_desvio_linha_reta"]:
            lados[lado_da_reta(origem, destino, c)].append((fator, nome, c))
    for lista in lados.values():
        lista.sort()
    intercaladas = []
    while (lados[1] or lados[-1]) and len(intercaladas) < PARAMS["max_chamadas_waypoint"]:
        for lado in (1, -1):
            if lados[lado] and len(intercaladas) < PARAMS["max_chamadas_waypoint"]:
                intercaladas.append(lados[lado].pop(0))
    return intercaladas


def avaliar_par(chave_api, origem_nome, destino_nome):
    global contador_chamadas
    contador_chamadas = 0
    rotulo = f"{origem_nome[0]}/{origem_nome[1]} -> {destino_nome[0]}/{destino_nome[1]}"
    print("\n" + "=" * 90 + f"\n{rotulo}")

    origem, destino = geocodificar(*origem_nome), geocodificar(*destino_nome)
    resposta = chamar_routes(chave_api, origem, destino)
    salvar(rotulo, "base", resposta)
    rotas = [normalizar(r, "Google") for r in resposta.get("routes", [])]
    if not rotas:
        print("  Nenhuma rota retornada pela API.")
        return
    mais_rapida = min(rotas, key=lambda r: r["min"])

    # RN-01
    if mais_rapida["km"] < PARAMS["distancia_minima_km"]:
        print(f"  RN-01: trajeto de {mais_rapida['km']:.1f} km < {PARAMS['distancia_minima_km']} km "
              "→ exibir 1 rota + aviso de condições térmicas equivalentes.")
        imprimir([mais_rapida])
        print(f"  Chamadas à Routes API: {contador_chamadas}")
        return {"rotulo": rotulo, "origem": origem, "destino": destino, "rotas": [mais_rapida],
                "aviso": "Trajeto curto: as rotas possíveis têm condições térmicas equivalentes (RN-01)."}

    aceitas, descartes = [mais_rapida], []
    filtrar([r for r in rotas if r is not mais_rapida], mais_rapida, aceitas, descartes)

    # RN-04
    if len(aceitas) < PARAMS["rotas_exibidas"]:
        candidatas = candidatas_intermediarias(origem_nome, destino_nome, origem, destino)
        if not candidatas:
            print("  RN-04: nenhuma cidade da lista passou no pré-filtro de desvio.")
        for fator, nome, coord in candidatas:
            try:
                resp = chamar_routes(chave_api, origem, destino, waypoint=coord)
            except Exception as erro:
                print(f"  RN-04: via {nome[0]} falhou: {erro}")
                continue
            salvar(rotulo, f"via_{nome[0]}", resp)
            novas = [normalizar(r, f"via {nome[0]} (linha reta {fator:.2f}x)") for r in resp.get("routes", [])]
            filtrar(novas, mais_rapida, aceitas, descartes)

    escolhidas = selecionar(aceitas)
    imprimir(escolhidas)
    for rota, motivo in descartes:
        print(f"  descartada: {rota['km']:6.1f} km | {rota['min']:4.0f} min | {rota['origem_rota']} | {motivo}")
    # RN-06
    aviso = ""
    if len(escolhidas) < PARAMS["rotas_exibidas"]:
        print(f"  RN-06: apenas {len(escolhidas)} rota(s) significativamente diferente(s) → exibir com aviso.")
        aviso = f"Foram encontradas apenas {len(escolhidas)} rota(s) significativamente diferente(s) (RN-06)."
    print(f"  Chamadas à Routes API: {contador_chamadas}")
    return {"rotulo": rotulo, "origem": origem, "destino": destino, "rotas": escolhidas, "aviso": aviso}


def imprimir(rotas):
    for i, r in enumerate(rotas, 1):
        print(f"  {i}. {r['km']:6.1f} km | {r['min']:4.0f} min | {r['origem_rota']:<35} | {r['descricao']}")
    if len(rotas) > 1:
        print("  Sobreposição entre as escolhidas:")
        for i, a in enumerate(rotas):
            for j, b in enumerate(rotas):
                if i < j:
                    print(f"     {i + 1}x{j + 1}: {sobreposicao(b, a):.0%}")


def salvar(rotulo, sufixo, dados):
    nome = f"{rotulo}_{sufixo}".replace(" ", "_").replace("/", "-").replace(">", "")
    (SAIDA / f"{nome}.json").write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    chave_api = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not chave_api:
        sys.exit("Defina a variável de ambiente GOOGLE_MAPS_API_KEY.")
    SAIDA.mkdir(exist_ok=True)
    print("Parâmetros:", json.dumps(PARAMS, ensure_ascii=False))
    resultados = []
    for origem, destino in PARES:
        try:
            r = avaliar_par(chave_api, origem, destino)
            if r:
                resultados.append(r)
        except Exception as erro:
            print(f"  ERRO: {erro}")
    if resultados:
        gerar_mapa(resultados)


CORES = ["#1a73e8", "#e8710a", "#0f9d58"]

HTML_MAPA = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Feneme — prévia de rotas (spike)</title>
<style>
 body{margin:0;font-family:system-ui,sans-serif;display:flex;height:100vh}
 #painel{width:340px;padding:16px;overflow:auto;border-right:1px solid #ddd}
 #mapa{flex:1} select{width:100%;padding:6px;margin:8px 0 12px}
 .rota{border-left:6px solid;padding:8px 10px;margin:8px 0;background:#f6f6f6;cursor:pointer}
 .aviso{background:#fff4e5;border:1px solid #f0b37e;padding:8px;margin-top:8px;font-size:14px}
 small{color:#666}
</style></head><body>
<div id="painel"><h3 style="margin:0">Feneme — comparação de rotas</h3>
<small>Prévia do spike. Temperatura ainda não calculada.</small>
<select id="par"></select><div id="lista"></div><div id="aviso"></div></div>
<div id="mapa"></div>
<script>
const DADOS = __DADOS__;
const CORES = __CORES__;
let mapa, linhas = [], marcadores = [];
function mostrar(i){
  linhas.forEach(l=>l.setMap(null)); marcadores.forEach(m=>m.setMap(null)); linhas=[]; marcadores=[];
  const par = DADOS[i], limites = new google.maps.LatLngBounds(), lista = document.getElementById('lista');
  lista.innerHTML='';
  par.rotas.forEach((r,k)=>{
    const caminho = r.pontos.map(p=>({lat:p[0],lng:p[1]}));
    caminho.forEach(p=>limites.extend(p));
    const linha = new google.maps.Polyline({path:caminho,strokeColor:CORES[k],strokeOpacity:.85,
      strokeWeight:k===0?7:5,zIndex:10-k,map:mapa});
    linhas.push(linha);
    const div = document.createElement('div'); div.className='rota'; div.style.borderColor=CORES[k];
    div.innerHTML=`<b>Rota ${k+1}</b> — ${r.km.toFixed(1)} km · ${Math.round(r.min)} min<br><small>${r.descricao||''} · ${r.origem_rota}</small>`;
    div.onmouseenter=()=>linhas.forEach((l,j)=>l.setOptions({strokeOpacity:j===k?1:.25}));
    div.onmouseleave=()=>linhas.forEach(l=>l.setOptions({strokeOpacity:.85}));
    lista.appendChild(div);
  });
  [['A',par.origem],['B',par.destino]].forEach(([t,c])=>marcadores.push(
    new google.maps.Marker({position:{lat:c[0],lng:c[1]},label:t,map:mapa})));
  document.getElementById('aviso').innerHTML = par.aviso?`<div class="aviso">${par.aviso}</div>`:'';
  mapa.fitBounds(limites, 40);
}
function iniciar(){
  mapa = new google.maps.Map(document.getElementById('mapa'),{center:{lat:-7.2,lng:-35.9},zoom:8});
  const sel = document.getElementById('par');
  DADOS.forEach((p,i)=>sel.add(new Option(p.rotulo,i)));
  sel.onchange=()=>mostrar(sel.value); mostrar(0);
}
</script>
<script async src="https://maps.googleapis.com/maps/api/js?key=__CHAVE__&callback=iniciar"></script>
</body></html>"""


def gerar_mapa(resultados):
    """Gera mapa_rotas.html com as rotas escolhidas (Maps JavaScript API)."""
    chave_mapa = os.environ.get("GOOGLE_MAPS_JS_KEY")
    if not chave_mapa:
        print("\nMapa não gerado: defina GOOGLE_MAPS_JS_KEY (chave restrita à Maps JavaScript API).")
        return
    dados = [
        {
            "rotulo": r["rotulo"], "origem": r["origem"], "destino": r["destino"], "aviso": r["aviso"],
            "rotas": [{k: v for k, v in rota.items()} for rota in r["rotas"]],
        }
        for r in resultados
    ]
    html = (HTML_MAPA.replace("__DADOS__", json.dumps(dados, ensure_ascii=False))
            .replace("__CORES__", json.dumps(CORES))
            .replace("__CHAVE__", urllib.parse.quote(chave_mapa)))
    pathlib.Path("mapa_rotas.html").write_text(html, encoding="utf-8")
    print("\nMapa gerado: mapa_rotas.html — abra com: python -m http.server 8000  e acesse "
          "http://localhost:8000/mapa_rotas.html  (NÃO versionar: contém a chave do mapa)")


if __name__ == "__main__":
    main()

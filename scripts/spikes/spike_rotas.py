"""
Spike — Google Routes API: quantas rotas alternativas voltam entre cidades da lista do Feneme?

Uso:
    export GOOGLE_MAPS_API_KEY="sua-chave"        (Windows PowerShell: $env:GOOGLE_MAPS_API_KEY="sua-chave")
    python spike_rotas.py

Edite PARES abaixo com cidades da MESMA lista usada na previsão do clima.
Sugestão: 1 par curto (< 50 km), 1 médio (~100-150 km) e 1 longo (> 300 km).

Saídas:
    - tabela no terminal (rotas retornadas, distância, duração, descrição)
    - respostas brutas em ./spike_respostas/*.json (reaproveitáveis como fixtures de teste)

Não versionar a chave. Este script é descartável (código de spike).
"""

import json
import os
import pathlib
import sys
import urllib.parse
import urllib.request

# Pares usados no spike de 13/11/2026 (resultados em docs/produto/spikes-rotas-google.md)
PARES = [
    (("Campina Grande", "PB"), ("Lagoa Seca", "PB")),
    (("Campina Grande", "PB"), ("João Pessoa", "PB")),
    (("Campina Grande", "PB"), ("Recife", "PE")),
]

ROUTES_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FIELD_MASK = "routes.distanceMeters,routes.duration,routes.routeLabels,routes.description"
SAIDA = pathlib.Path("spike_respostas")

# Siglas -> nome do estado, para desambiguar cidades homônimas na geocodificação
UFS = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas", "BA": "Bahia",
    "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo", "GO": "Goiás",
    "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul", "MG": "Minas Gerais",
    "PA": "Pará", "PB": "Paraíba", "PR": "Paraná", "PE": "Pernambuco", "PI": "Piauí",
    "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte", "RS": "Rio Grande do Sul",
    "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina", "SP": "São Paulo",
    "SE": "Sergipe", "TO": "Tocantins",
}


def geocodificar(cidade: str, uf: str) -> tuple[float, float]:
    query = urllib.parse.urlencode(
        {"name": cidade, "count": 10, "language": "pt", "countryCode": "BR", "format": "json"}
    )
    with urllib.request.urlopen(f"{GEOCODE_URL}?{query}", timeout=15) as resp:
        resultados = json.load(resp).get("results", [])
    estado = UFS.get(uf.upper())
    for r in resultados:
        if estado is None or r.get("admin1") == estado:
            return r["latitude"], r["longitude"]
    raise ValueError(f"Cidade não encontrada: {cidade}/{uf}")


def ponto(lat: float, lon: float) -> dict:
    return {"location": {"latLng": {"latitude": lat, "longitude": lon}}}


def buscar_rotas(chave: str, origem: tuple, destino: tuple) -> dict:
    corpo = {
        "origin": ponto(*origem),
        "destination": ponto(*destino),
        "travelMode": "DRIVE",
        "computeAlternativeRoutes": True,
        "languageCode": "pt-BR",
        "units": "METRIC",
    }
    req = urllib.request.Request(
        ROUTES_URL,
        data=json.dumps(corpo).encode(),
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": chave,
            "X-Goog-FieldMask": FIELD_MASK,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def main() -> None:
    chave = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not chave:
        sys.exit("Defina a variável de ambiente GOOGLE_MAPS_API_KEY.")
    SAIDA.mkdir(exist_ok=True)

    for (cid_o, uf_o), (cid_d, uf_d) in PARES:
        rotulo = f"{cid_o}/{uf_o} -> {cid_d}/{uf_d}"
        try:
            origem = geocodificar(cid_o, uf_o)
            destino = geocodificar(cid_d, uf_d)
            dados = buscar_rotas(chave, origem, destino)
        except Exception as erro:  # spike: registrar e seguir para o próximo par
            print(f"\n{rotulo}\n  ERRO: {erro}")
            continue

        arquivo = SAIDA / f"{cid_o}_{cid_d}.json".replace(" ", "_")
        arquivo.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")

        rotas = dados.get("routes", [])
        print(f"\n{rotulo}  ->  {len(rotas)} rota(s)  [{arquivo}]")
        for i, r in enumerate(rotas, 1):
            km = r.get("distanceMeters", 0) / 1000
            minutos = int(r.get("duration", "0s").rstrip("s")) / 60
            labels = ",".join(r.get("routeLabels", []))
            print(f"  {i}. {km:7.1f} km | {minutos:6.0f} min | {labels} | {r.get('description', '')}")


if __name__ == "__main__":
    main()

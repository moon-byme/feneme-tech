# Spikes — rotas da Google Routes API e comparação térmica

> Investigações de 13 e 14/11/2026 que embasaram a mudança de escopo registrada em [FT-112](https://feneme.atlassian.net/browse/FT-112). Os scripts ficam em [`scripts/spikes/`](../../scripts/spikes/) e são **código de spike**: servem como evidência e referência, não como implementação do produto.

## Spike 1 — A API devolve 3 rotas?

**Pergunta:** a Google Routes API, com `computeAlternativeRoutes: true`, devolve 3 rotas entre cidades da região?
**Script:** [`spike_rotas.py`](../../scripts/spikes/spike_rotas.py)

| Par | Distância | Rotas retornadas | Observação |
| --- | --- | --- | --- |
| Campina Grande → Lagoa Seca | 9,2–12,0 km | 3 | Alternativas reais, mas curtas demais para diferença térmica |
| Campina Grande → João Pessoa | 127,1 km | 1 | Só a BR-230; sem alternativa natural |
| Campina Grande → Recife | 193,7–211,0 km | 3 | BR-230, BR-230/BR-408 e Rod. Terezinha Lins Pessoa |

**Conclusão:** a API não garante 3 alternativas. Isso gerou as regras RN-04 (cidades intermediárias da lista) e RN-06 (aviso de rotas insuficientes).

## Spike 2 — Regras de seleção de rotas

**Pergunta:** as regras RN-01 a RN-06 produzem rotas realmente diferentes?
**Script:** [`spike_regras_rotas.py`](../../scripts/spikes/spike_regras_rotas.py) (gera também `mapa_rotas.html`)

| Par | Resultado |
| --- | --- |
| Campina Grande → Lagoa Seca | RN-01: 9,3 km < 50 km → 1 rota e aviso |
| Campina Grande → João Pessoa | 1 rota; alternativas descartadas por sobreposição de 77% a 88% (RN-03) → RN-06 |
| Campina Grande → Recife | 3 rotas distintas; sobreposição entre elas de 2%, 32% e 42% |

Observação: no spike a lista de cidades tinha só 4 itens, o que limitou a RN-04. A versão no repositório já usa as 26 cidades da lista oficial.

## Spike 3 — Indicadores térmicos

**Pergunta:** dá para calcular a exposição ao calor de cada rota com a Open-Meteo e mostrar isso no mapa?
**Script:** [`spike_termico_rotas.py`](../../scripts/spikes/spike_termico_rotas.py) (gera `mapa_termico.html`)

O protótipo amostra pontos a cada 10 km, estima o horário de passagem, consulta a previsão horária e calcula máxima, média, minutos acima do limite e grau-hora. O mapa mostra pontos vermelhos onde a previsão passa do limite da carga e uma tabela comparando horários de saída. A visualização foi aprovada pela equipe como referência para as US-18 e US-09.

## Como executar

Requisitos: Python 3.10+ (só biblioteca padrão) e as chaves descritas em [`docs/devops/google-maps-platform.md`](../devops/google-maps-platform.md).

```powershell
cd scripts/spikes
$env:GOOGLE_MAPS_API_KEY="chave-routes"
$env:GOOGLE_MAPS_JS_KEY="chave-maps"      # só para gerar os mapas
python spike_termico_rotas.py             # usa spike_regras_rotas.py da mesma pasta
python -m http.server 8000                # abrir http://localhost:8000/mapa_termico.html
```

**Não versionar** os arquivos gerados (`mapa_*.html` contém a chave do mapa; `spike*_respostas/` contém respostas brutas). Eles estão no `.gitignore`.

## Uso futuro

As respostas JSON gravadas pelos spikes devem virar *fixtures* dos testes das US-17 e US-09, para que o CI nunca chame as APIs reais.

# Nova linha do produto — rotas reais e comparação térmica (R2 a R4)

> **Situação:** escopo aprovado pela equipe em 14/11/2026 e detalhado em 16/11/2026. Este documento descreve o que **será construído**; nada aqui está implementado ainda.
> **Registro oficial no Jira:** [FT-112](https://feneme.atlassian.net/browse/FT-112).

## Em uma frase

O Feneme passa a comparar até 3 rotas reais entre cidades de uma lista fechada e a indicar qual delas expõe menos a carga ao calor do ambiente, conforme o tipo de carga e o horário de saída. **O Gestor decide.**

Esse é o diferencial em relação a Waze e Google Maps: eles escolhem a rota mais rápida; o Feneme mostra qual rota e qual horário protegem melhor a carga.

## Origem da mudança

Na Sprint Review da Sprint 2 (12/11/2026), a professora pediu:

1. cidades pré-definidas no cadastro de entrega, iguais às da previsão do clima;
2. que o sistema indique distância, caminho e temperatura das rotas (por exemplo, com a API do Google Maps), cabendo ao Gestor comparar e decidir;
3. 3 rotas comparadas em vez de 2, visíveis em um mapa;
4. um diferencial frente a outros sistemas de rotas: a temperatura conforme o tipo de carga.

## Premissas

| Premissa | Decisão |
| --- | --- |
| Rotas | Não existe mais cadastro manual de trajetos. As rotas vêm da Google Routes API a partir das cidades escolhidas. |
| Refrigeração | Abstraída: o Feneme considera a carga transportada sem refrigeração e compara a temperatura **prevista do ambiente** (Open-Meteo) com o limite da carga. |
| Decisão | O sistema indica a rota de menor exposição; quem escolhe é o Gestor, e a escolha fica registrada. |
| Temperatura | É previsão do ambiente, nunca temperatura medida da carga. A tela deve dizer isso. |

## Novas funcionalidades

| Funcionalidade | O que o usuário faz | Jira | Sprint |
| --- | --- | --- | --- |
| Lista única de cidades | Gestor escolhe origem e destino em uma lista; o clima usa a mesma lista | [FT-113](https://feneme.atlassian.net/browse/FT-113) (US-14) | S3 |
| Catálogo de tipos de carga | Gestor escolhe o tipo de carga e vê o limite e a fonte | [FT-114](https://feneme.atlassian.net/browse/FT-114) (US-15) | S3 |
| Tipo de carga e saída na entrega | Gestor informa tipo de carga, data e hora de saída | [FT-117](https://feneme.atlassian.net/browse/FT-117) (US-16) | S4 |
| Rotas automáticas | Sistema gera até 3 rotas distintas (km, minutos, rodovias) | [FT-118](https://feneme.atlassian.net/browse/FT-118) (US-17) | S4 |
| Mapa das rotas | Gestor vê as rotas desenhadas no mapa | [FT-120](https://feneme.atlassian.net/browse/FT-120) (US-18) | S4 |
| Comparação térmica | Sistema calcula indicadores por rota e destaca a de menor exposição | [FT-57](https://feneme.atlassian.net/browse/FT-57) (US-09, reescrita) | S5 |
| Registro da escolha | Gestor escolhe a rota; o sistema guarda os indicadores daquele momento | [FT-122](https://feneme.atlassian.net/browse/FT-122) (US-19) | S5 |
| Comparar horários de saída | Sistema simula 8 saídas e destaca o melhor horário | [FT-123](https://feneme.atlassian.net/browse/FT-123) (US-20) | S6 |

Itens de apoio: remoção do cadastro manual de trajetos ([FT-119](https://feneme.atlassian.net/browse/FT-119)), configuração do projeto Google ([FT-115](https://feneme.atlassian.net/browse/FT-115)), driver DA-CON-JP-02 ([FT-121](https://feneme.atlassian.net/browse/FT-121)) e risco R10 ([FT-116](https://feneme.atlassian.net/browse/FT-116)).

## Fluxo do Gestor (visão final, após a R4)

1. Cadastra a entrega escolhendo origem, destino e tipo de carga nas listas, e informa data e hora de saída.
2. Abre a comparação: o sistema busca até 3 rotas e as mostra no mapa.
3. Para cada rota, vê distância, tempo, temperatura máxima e média previstas, tempo acima do limite da carga e exposição em grau-hora.
4. A rota de menor exposição recebe o selo **"Menor exposição ao calor"**.
5. Se quiser, compara horários de saída e adota o melhor.
6. Escolhe a rota (pode informar o motivo); a escolha vai para o histórico e o resumo da entrega.

## Catálogo inicial de cargas

Critério de entrada: limite de referência **≥ 20 °C**. Como o Feneme não considera refrigeração, cargas com limite menor ficariam acima do limite em qualquer rota do Brasil e a comparação não diferenciaria nada.

| # | Categoria | Carga | Limite (°C) | Referência na fonte | Fonte | Tipo de fonte |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Hortifrúti | Tomate (maduro-verde) | 27 | Acima de 27 °C reduz a intensidade da cor vermelha | [USDA HB-66 — tomate](https://webarchive.library.unt.edu/eot2008/20090305020046/http:/www.ba.ars.usda.gov/hb66/138tomato.pdf) | Literatura técnica |
| 2 | Animais vivos | Frangos de corte (5–6 semanas) | 23 | Faixa de conforto térmico de 20–23 °C | [Embrapa Suínos e Aves, IT 37](https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1105008/1/ITAV37PAbreu.pdf) | Órgão técnico |
| 3 | Animais vivos | Suínos (crescimento e terminação) | 24 | Zona de conforto térmico de 18–24 °C | [Embrapa Suínos e Aves](https://ainfo.cnptia.embrapa.br/digital/bitstream/doc/1169212/1/final10419-O-uso-da-climatizacao-melhora-a-conversao-alimentar-e-o-ganho-de-peso-dos-suinos.pdf) | Órgão técnico |
| 4 | Animais vivos | Bovinos zebuínos | 27 | Faixa ótima de 10–27 °C para zebuínos adultos | [Semina: Ciências Agrárias (UEL)](https://ojs.uel.br/revistas/uel/index.php/semagrarias/article/download/33889/25462/175800) | Artigo revisado por pares |
| 5 | Medicamentos | Medicamentos de temperatura ambiente | 30 | "Temperatura ambiente" = 15–30 °C | [Farmacopeia Brasileira, via CRF-SP](https://crfsp.org.br/images/2023/OrientacaoFarmaceutica/Parte_2/Armazenamento_inadequado_de_produtos__almoxarifado.pdf); [Anvisa, RDC 430/2020](https://www.gov.br/anvisa/pt-br/assuntos/educacaoepesquisa/webinar/medicamentos/arquivos/apresentacao-boas-praticas-de-distribuicao-armazenagem-e-transporte-de-medicamentos.pdf) | Norma oficial |
| 6 | Biológicos | Amostras biológicas para diagnóstico | 25 | Transporte aceitável até 25 °C | [POP HC-UFTM/Ebserh, base RDC 504/2021](https://www.gov.br/hubrasil/pt-br/hospitais-universitarios/regiao-sudeste/hc-uftm/documentos/procedimentos-e-rotinas-operacionais-padrao/pops/POP.UACAP.017PadroesSanitariosparaAcondicionamentoeTransportedeMaterialBiologicoversao4.pdf) | Órgão público |
| 7 | Cosméticos e higiene | Cosméticos e produtos de higiene | 30 | Deduzido: o guia avalia a validade em temperatura ambiente; 37–50 °C são condições de estresse | [Anvisa, Guia de Estabilidade de Produtos Cosméticos](https://bibliotecadigital.anvisa.gov.br/jspui/bitstream/anvisa/189/1/Guia%20de%20estabilidade%20de%20produtos%20cosm%c3%a9ticos.pdf) + faixa ambiente da Farmacopeia | Derivado (exibir como "limite derivado") |

Fora do catálogo inicial por terem limite muito baixo para transporte sem refrigeração: uva de mesa, banana, carne resfriada, leite cru, medicamentos termolábeis e vacinas. Defensivos agrícolas também ficaram de fora: a norma citada (ABNT NBR 9843) é paga e as bulas consultadas trazem limites diferentes, então não há uma fonte verificável para um limite único (decisão do PO em 16/11/2026). O catálogo pode ser ampliado depois, sempre com fonte e com o mesmo critério.

**Fontes conferidas em 16/11/2026:** itens 1 a 6 confirmados; item 7 é um limite derivado e deve aparecer assim na interface.

## Lista de cidades (26 cidades, 13 estados + DF)

| Região | UF | Cidades |
| --- | --- | --- |
| Nordeste | PB | João Pessoa, Campina Grande, Patos |
| Nordeste | PE | Recife, Caruaru, Serra Talhada, Petrolina |
| Nordeste | RN | Natal, Mossoró |
| Nordeste | CE | Fortaleza, Juazeiro do Norte |
| Nordeste | AL | Maceió, Arapiraca |
| Nordeste | SE | Aracaju |
| Nordeste | BA | Salvador, Feira de Santana, Juazeiro, Vitória da Conquista |
| Nordeste | PI | Teresina |
| Nordeste | MA | São Luís |
| Sudeste | MG | Montes Claros, Belo Horizonte |
| Sudeste | SP | São Paulo |
| Sudeste | RJ | Rio de Janeiro |
| Centro-Oeste | DF | Brasília |
| Centro-Oeste | GO | Goiânia |

A concentração no Nordeste dá cidades intermediárias para a regra RN-04; os polos de fruticultura (Petrolina, Juazeiro, Mossoró) e os centros consumidores do Sudeste dão cenários coerentes para a demo. As coordenadas ficam gravadas no seed, sem geocodificação em tempo de execução.

**Transição a partir do código atual:** a previsão do clima (FT-47) usa hoje `backend/weather/locations.py`, com 5 localidades (João Pessoa, Campina Grande, Patos, Sousa e Recife). A US-14 substitui essa lista pela lista acima, reaproveitando as coordenadas já conferidas. **Sousa-PB sai da lista**; se a equipe quiser mantê-la, basta incluí-la no seed (a lista passaria a ter 27 cidades). O campo de origem/destino da entrega (`Delivery.origin`/`destination`) deixa de ser texto livre e exige migração dos registros existentes.

## Regras de negócio

Todos os parâmetros ficam em `settings`, para o PO calibrar sem mudar a lógica.

| Regra | O que faz | Valor inicial |
| --- | --- | --- |
| RN-01 Distância mínima | Rota padrão abaixo do limite: exibe 1 rota e o aviso "trajeto curto: condições térmicas equivalentes" | 50 km |
| RN-02 Viabilidade | Descarta rota muito mais lenta que a mais rápida | 1,5× até 300 km; 1,3× acima |
| RN-03 Distinção | Descarta rota que repete o percurso de outra (amostra a cada 1 km, raio de 1 km) | sobreposição ≤ 60% |
| RN-04 Candidatas | Com menos de 3 rotas, testa cidades da lista como ponto de passagem, alternando lados da reta origem–destino | desvio ≤ 1,4× em linha reta; até 3 chamadas extras |
| RN-05 Seleção | A mais rápida entra; as demais por menor sobreposição. A temperatura não influi na escolha das rotas | 3 rotas |
| RN-06 Rotas insuficientes | Mostra as rotas existentes com o aviso "foram encontradas apenas N rotas significativamente diferentes" | — |
| RN-07 Cache | Reaproveita as rotas do par origem–destino; a temperatura é sempre recalculada | 24 h |
| RN-08 Amostragem térmica | Pontos ao longo da rota; horário de passagem proporcional à distância percorrida | a cada 10 km, no máximo 60 pontos |
| RN-09 Horizonte | Saída entre agora + 1 h e hoje + 5 dias; chegada dentro dos 7 dias de previsão horária | — |
| RN-10 Indicadores e destaque | Máxima, média ponderada, minutos acima do limite e grau-hora; selo na menor exposição | empate (< 0,5 grau-hora) → menor tempo; nenhuma rota acima do limite → menor média |

**Grau-hora** = soma de (temperatura − limite) × tempo, só nos trechos acima do limite. Um trecho a 31 °C durante 30 minutos, com limite de 28 °C, soma (31 − 28) × 0,5 = 1,5 grau-hora.

## Fora do escopo

- GPS e rastreamento em tempo real.
- Sensores e temperatura medida da carga.
- Modelagem de veículo refrigerado.
- Trânsito em tempo real e pausas obrigatórias do motorista no cálculo do horário de passagem.
- Confirmação por destinatário e aplicativo nativo.

## Limitações conhecidas

- A temperatura é a prevista do ambiente (Open-Meteo), não a da carga.
- O horário de passagem supõe velocidade constante; em viagens de mais de um dia a chegada real tende a ser mais tarde.
- A Google Routes API nem sempre devolve alternativas (ex.: Campina Grande → João Pessoa teve 1 rota no spike); por isso existem RN-04 e RN-06.

## Itens retirados para "desejável"

FT-93 (editar entrega), FT-94 (filtros), FT-95 (trocar senha), FT-97 (limitar tentativas de login), FT-106 (painel de indicadores), FT-107 (exportar CSV), FT-108 (observações do Motorista). Continuam no backlog do Jira com o rótulo `desejavel`.

## Documentos relacionados

- [Spikes das rotas e da comparação térmica](spikes-rotas-google.md)
- [Gestão do projeto Google Cloud e das chaves](../devops/google-maps-platform.md)
- Jira: [FT-112](https://feneme.atlassian.net/browse/FT-112) (registro da mudança), [FT-50](https://feneme.atlassian.net/browse/FT-50) (plano de releases)

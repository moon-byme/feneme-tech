#set page(paper: "a4", margin: (x: 20mm, y: 17mm), footer: align(right, text(size: 9pt, fill: rgb("53636d"))[Feneme · R2 · FT-110 / FT-92]))
#set text(font: "Libertinus Serif", size: 11pt, lang: "pt")
#set par(justify: false, leading: 0.65em)
#show heading: set text(fill: rgb("173b4a"))
#text(size: 10pt, weight: "bold", fill: rgb("28756f"))[FENEME / RELEASE 2 / SPRINT 3]
= Validação do deploy automatizado
#text(fill: rgb("53636d"))[Registro complementar ao relatório do pipeline — 25/11/2026]

#block(fill: rgb("eaf4f2"), inset: 9pt, radius: 4pt)[
  *Resultado:* implantação automática em homologação validada com sucesso. Aplicação e banco responderam corretamente; o commit implantado correspondeu ao push na main.
]

== 1. Evidências da implantação
#table(columns: (1fr, 2fr), inset: 6pt, stroke: 0.4pt + rgb("c8d5da"),
  [Ambiente], [#link("https://feneme-homologacao.onrender.com")[Render — feneme-homologacao]],
  [Execução], [#link("https://github.com/moon-byme/feneme-tech/actions/runs/45738722270")[CI nº 351] — sucesso, 6 min 49 s],
  [Integração], [#link("https://github.com/moon-byme/feneme-tech/pull/53")[PR nº 53] — correção do parâmetro do Deploy Hook],
  [Deploy Hook], [HTTP 200; iniciado às 22h57, Live às 22h59 (BRT)],
  [Health check], [#link("https://feneme-homologacao.onrender.com/api/health/")[/api/health/] — status: ok; database: ok],
  [Commit], [#text(size: 9pt)[`b017151287a6b9325c690037651c92412aff8a1f`]],
)

== 2. Condições de execução e segurança
O workflow exige push na main e sucesso de backend, frontend, E2E e varredura de segredos (`needs`). O Blueprint desativa o deploy automático do próprio Render. No CI nº 351, os jobs obrigatórios e as duas etapas de deploy passaram. O job de segurança passou; a verificação não constitui auditoria integral de todos os logs e segredos.

== 3. Cenário de falha e correção
- #link("https://github.com/moon-byme/feneme-tech/actions/runs/45730929872")[CI nº 331]: E2E falhou e deploy ficou ignorado em branch de QA. Evidência complementar, pois a branch também não era main. O bloqueio na main foi conferido pela configuração do workflow, não por uma execução deliberadamente falha na main.
- #link("https://github.com/moon-byme/feneme-tech/actions/runs/45734971703")[CI nº 345] e #link("https://github.com/moon-byme/feneme-tech/actions/runs/45735867289")[CI nº 348]: testes passaram, mas o deploy falhou. O nº 348 registrou HTTP 404; a PR nº 53 corrigiu a montagem da URL. O CI nº 351 confirmou a recuperação.

== 4. Rastreabilidade e limites
#link("https://feneme.atlassian.net/browse/FT-110")[FT-110] · #link("https://feneme.atlassian.net/browse/FT-92")[FT-92] · #link("https://github.com/moon-byme/feneme-tech/blob/main/docs/devops/homologacao.md")[Guia de homologação] · #link("https://github.com/moon-byme/feneme-tech/blob/main/.github/workflows/ci.yml")[Workflow]. Este registro complementa o recorte anterior do relatório do pipeline (execuções 52–310); não recalcula suas métricas nem certifica a publicação da tag v2.0.0.

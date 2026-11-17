// Feneme — Registro de Sprint Planning 3
// Documento em Typst; síntese de registros de 16/11 e das confirmações presenciais informadas pela Scrum Master.
#set page(
  paper: "a4",
  margin: (top: 22mm, bottom: 20mm, left: 22mm, right: 22mm),
  numbering: "1",
)
#set text(font: "Liberation Sans", size: 10pt, lang: "pt")
#set par(justify: true, leading: 0.55em)
#set heading(numbering: "1.")
#show heading.where(level: 1): set text(size: 12.5pt, weight: "bold", fill: rgb("#173E60"))
#show link: set text(fill: rgb("#166392"))

#align(center)[
  #text(size: 18pt, weight: "bold", fill: rgb("#173E60"))[Feneme — Registro da Sprint Planning 3]
  #v(4pt)
  #text(size: 10.5pt, fill: rgb("#566A7D"))[Release 2 · Sprint 3 · Consolidação e confirmação das decisões]
]
#v(11pt)

*Release:* R2 (término previsto em 26/11/2026) \
*Sprint:* FT Sprint 3 (17 a 26/11/2026) \
*Referência principal:* #link("https://feneme.atlassian.net/browse/FT-90")[FT-90] \
*Registros de mensagens:* 16/11/2026, das 18h32 às 21h04 \
*Modalidade:* alinhamentos por WhatsApp, decisões no Jira e confirmação presencial pela equipe \
*Natureza:* ata consolidada de planejamento, com os encaminhamentos ratificados presencialmente, conforme informação da Scrum Master \
*Situação:* planejamento confirmado e encerrado

= Participantes e papéis

- *Lethycia Zenaide Queiroz Melo* — Scrum Master (SM).
- *João Paulo de Araujo* — Product Owner (PO) e DevOps.
- *José Araújo Agra Neto* — QA.

Os papéis estão registrados na #link("https://feneme.atlassian.net/browse/FT-50")[FT-50]. As conversas de 16/11 serviram à preparação da Planning; os alinhamentos e encaminhamentos finais foram confirmados presencialmente pelos integrantes, conforme registro da Scrum Master.

= Alinhamentos e confirmações

- *16/11, 18h32–18h35:* a SM solicitou que as tarefas estivessem com a Definition of Ready (DoR) assinalada antes do início da Sprint 3 e esclareceu o significado desse critério de prontidão.
- *16/11, 20h38–20h41:* a SM compartilhou as planilhas de Análise de Riscos, Definition of Done (DoD) e Plano de Qualidade e solicitou a conferência do QA.
- *16/11, 21h04:* foi recebido retorno favorável à conferência inicial dos materiais. Posteriormente, os documentos e os encaminhamentos foram revisados e confirmados presencialmente pela equipe.
- *Decisões de produto:* o PO registrou na #link("https://feneme.atlassian.net/browse/FT-112")[FT-112] o escopo com lista fechada de 26 cidades, catálogo de 7 tipos de carga, configuração do Google Cloud e transferência da FT-57 para a Sprint 5/R3. Essas decisões foram mantidas na confirmação presencial.

= Backlog, estimativas e capacidade aprovados

Na conferência do Jira de 17/11, a Sprint 3 reunia *19 issues e 58 SP*, vinculadas à Sprint 3 e à R2, com responsáveis atribuídos e status *Pronto para a sprint*. A DoR estava assinalada nas histórias FT-48, FT-49, FT-59, FT-90, FT-91, FT-92, FT-110, FT-113 e FT-114. A equipe confirmou presencialmente a prontidão dos itens selecionados e o compromisso com o escopo planejado.

#table(
  columns: (2.2fr, 1fr),
  inset: 7pt,
  stroke: .5pt + rgb("#D5DFE7"),
  table.header([*Responsável no Jira*], [*SP atribuídos*]),
  [João Paulo], [31],
  [Lethycia], [15],
  [José], [12],
  [*Total*], [*58*],
)

A velocidade operacional de referência da Sprint 2 foi de *36 SP em status Concluído* (11 issues), conforme `docs/sprints/sprint-2/fontes/metricas-e-impedimentos.typ`, que também documenta as ressalvas históricas relativas à DoD e ao aceite. O volume de 58 SP da Sprint 3 é *22 SP superior*, aproximadamente *61%* acima dessa referência. A diferença e a distribuição de esforço (31/15/12 SP) foram consideradas na avaliação presencial de capacidade, e a equipe confirmou a manutenção integral do escopo de 58 SP.

*Estimativas ratificadas presencialmente:*

- #link("https://feneme.atlassian.net/browse/FT-113")[FT-113] — *5 SP*: estimativa confirmada pela equipe para a Sprint 3.
- #link("https://feneme.atlassian.net/browse/FT-114")[FT-114] — *3 SP*: estimativa confirmada pela equipe para a Sprint 3.

A validação ocorreu por confirmação presencial dos integrantes, sem atribuição de votação numérica ou de procedimento não registrado.

= Sequência técnica de dependências aprovada

*FT-48 → FT-49 → FT-59* foi ratificada presencialmente como a ordem de integração de referência da Sprint 3, em conformidade com as dependências das histórias no Jira e a priorização do PO.

+ *FT-48 — US-11 (5 SP; Lethycia):* atualização de status pelo Motorista, autorização, transições permitidas, persistência e eventos de histórico.
+ *FT-49 — US-12 (3 SP; João Paulo):* consulta do status atual pelo Gestor; preparação de interface e testes isolados pode ocorrer em paralelo, com integração e aceite apoiados na persistência da FT-48.
+ *FT-59 — US-13 (3 SP; Lethycia):* consulta de histórico cronológico e persistente; preparação isolada pode ocorrer em paralelo, com integração e aceite apoiados nas FT-48 e FT-49.

A equipe confirmou o encadeamento e suas dependências como diretriz de execução da sprint.

= Sprint Goal aprovado

#block(
  fill: rgb("#F3F7FA"),
  stroke: (left: 2.5pt + rgb("#42789A")),
  inset: (x: 12pt, y: 10pt),
  radius: 3pt,
)[
  Concluir a Release 2 com a atualização manual de status das entregas pelo Motorista, a consulta de andamento pelo Gestor e o histórico persistente, integrados na sequência *FT-48 → FT-49 → FT-59*. Preparar a evolução do Feneme com uma lista única de *26 cidades*, catálogo de *7 tipos de carga* com fontes, configuração segura do *Google Cloud* e registro do *risco R10*, além de executar testes, regressão, validação da DoD e procedimentos de homologação e publicação da R2.
]

O objetivo segue a meta da FT Sprint 3 no Jira, atualizada pelas decisões do PO na #link("https://feneme.atlassian.net/browse/FT-112")[FT-112], de 16/11. A *FT-57 foi transferida para a Sprint 5/R3* e não integra o compromisso desta sprint. A redação final e o compromisso correspondente foram *ratificados presencialmente* pela equipe.

= DoD, qualidade e riscos confirmados

A *Definition of Done (DoD)* foi disponibilizada por link em 16/11 e, na confirmação presencial da Planning, foi apresentada, revisada e validada pela equipe como referência para o aceite das entregas da Sprint 3.

O *Plano de Qualidade* e a *Análise de Riscos* foram compartilhados e conferidos, com validação presencial dos encaminhamentos pela equipe. A evolução de escopo contempla o *risco R10*, rastreado na *FT-116*, cuja inclusão foi confirmada no planejamento e considerada na atualização da matriz de riscos da release.

= Quadro de decisões concluídas — FT-90

#table(
  columns: (1.4fr, 1.45fr, 1.8fr),
  inset: 6pt,
  stroke: .5pt + rgb("#D5DFE7"),
  table.header([*Item*], [*Deliberação final*], [*Rastreabilidade*]),
  [Estimativas FT-113/FT-114], [*Confirmadas presencialmente:* 5 SP e 3 SP.], [FT-113 e FT-114; alinhamento da Planning.],
  [Capacidade e escopo], [*Aprovados:* 19 issues, 58 SP, distribuição 31/15/12 e manutenção integral do escopo.], [Jira da Sprint 3; referência de 36 SP da Sprint 2.],
  [Ordem FT-48 → FT-49 → FT-59], [*Aprovada* como sequência de integração.], [Dependências das três histórias e priorização do PO.],
  [Sprint Goal], [*Ratificado presencialmente* com o escopo atualizado.], [FT Sprint 3; FT-112.],
  [DoD e documentos de qualidade], [*Apresentados, revisados e confirmados* pela equipe.], [Materiais compartilhados em 16/11 e confirmação presencial.],
  [Riscos e R10], [*Encaminhamento aprovado*, com R10 rastreado na FT-116.], [Análise de Riscos; FT-116.],
  [Registro da Planning], [*Concluído* por esta ata consolidada.], [Este documento; referência FT-90.],
)

= Encerramento da Sprint Planning 3

Com a confirmação presencial informada pela Scrum Master, PO, SM e QA ratificaram o backlog da Sprint 3, as estimativas de 5 SP e 3 SP para FT-113 e FT-114, a capacidade comprometida de 58 SP, a ordem técnica FT-48 → FT-49 → FT-59, o Sprint Goal e os critérios da DoD, bem como os encaminhamentos de qualidade e riscos.

*Conclusão:* os itens de preparação e deliberação tratados na #link("https://feneme.atlassian.net/browse/FT-90")[FT-90] ficam registrados nesta ata como *confirmados e encerrados*. A execução das histórias, os testes, a homologação e a publicação da R2 permanecem atividades próprias da Sprint 3, e não deliberações em aberto da Planning.

= Rastreabilidade

#link("https://feneme.atlassian.net/browse/FT-90")[FT-90] ·
#link("https://feneme.atlassian.net/browse/FT-50")[FT-50] ·
#link("https://feneme.atlassian.net/browse/FT-112")[FT-112] ·
#link("https://feneme.atlassian.net/browse/FT-113")[FT-113] ·
#link("https://feneme.atlassian.net/browse/FT-114")[FT-114] ·
#link("https://feneme.atlassian.net/browse/FT-116")[FT-116]

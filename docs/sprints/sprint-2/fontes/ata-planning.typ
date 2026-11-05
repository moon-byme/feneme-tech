// FENEME | ATA DA SPRINT PLANNING 2
// Documento-fonte editavel para Typst / Tinymist no VS Code.
// Para alterar os dados, edite os textos das secoes abaixo.
// Depois exporte para PDF usando: Typst: Export PDF (paleta de comandos do VS Code).
// Registro elaborado posteriormente a reuniao. Validar com os participantes.

#let ink = rgb("#1b3041")
#let muted = rgb("#425a6f")
#let navy = rgb("#2c4c62")
#let teal = rgb("#087b8f")
#let border_color = rgb("#cfdae3")
#let shade = rgb("#f4f7f9")
#let soft_blue = rgb("#ebf2f6")

#set page(
  paper: "a4",
  margin: (top: 18mm, bottom: 20mm, left: 20mm, right: 20mm),
  footer: context [
    #line(length: 100%, stroke: 0.5pt + border_color)
    #v(4pt)
    #grid(
      columns: (1fr, auto),
      text(fill: muted, size: 8pt)[FENEME | ATA DE SPRINT PLANNING | 03/11/2026],
      text(fill: muted, size: 8pt)[Página #counter(page).display("1 de 1", both: true)],
    )
  ],
)
#set text(font: ("Arial", "Liberation Sans", "Noto Sans"), size: 9.6pt, fill: ink, lang: "pt")
#set par(leading: 0.52em)

#let sec(label) = block(above: 10pt, below: 5pt)[
  #text(fill: ink, weight: "bold", size: 12pt)[#label]
]
#let note(body) = text(fill: muted, size: 9pt, style: "italic")[#body]
#let whitehead(body) = table.cell(fill: navy, inset: 7pt)[
  #text(fill: white, weight: "bold", size: 9.2pt)[#body]
]

// ===== PAGINA 1: DADOS DA REUNIAO =====
#text(fill: teal, weight: "bold", size: 9.5pt)[FENEME / GESTÃO DE PROJETO]
#v(5pt)
#text(size: 21pt, weight: "bold", fill: ink)[Ata da Sprint Planning 2]
#v(4pt)
#text(size: 11.5pt, fill: muted)[Release 2 | Planejamento e distribuição de responsabilidades]
#v(10pt)
#line(length: 100%, stroke: 1.2pt + teal)
#v(10pt)

#table(
  columns: (27%, 73%),
  inset: (x: 7pt, y: 5pt),
  stroke: 0.45pt + border_color,
  table.cell(fill: shade)[*Data da reunião*], [03 de novembro de 2026],
  table.cell(fill: shade)[*Horário*], [19h às 22h (horário de Brasília)],
  table.cell(fill: shade)[*Modalidade*], [Reunião remota, realizada por mensagens no WhatsApp],
  table.cell(fill: shade)[*Projeto e período*], [Feneme | Release 2 (03/11 a 26/11/2026) | Sprint 2 (03/11 a 12/11/2026)],
  table.cell(fill: shade)[*Registro*], [Consolidação posterior ao encontro, a partir das informações relatadas e do planejamento do Jira.],
)

#sec[1. Participantes e papéis da Release 2]
#table(
  columns: (52%, 48%),
  inset: (x: 7pt, y: 6pt),
  stroke: 0.45pt + border_color,
  table.header(
    whitehead[Integrante], whitehead[Responsabilidade na R2],
  ),
  [Lethycia Zenaide Queiroz Melo], [Scrum Master (SM)],
  [João Paulo de Araujo], [Product Owner (PO) / DevOps],
  [José Araújo Agra Neto], [Quality Assurance (QA)],
)

#sec[2. Pauta da reunião]
- Distribuição dos deveres e responsabilidades entre os três integrantes da Release 2.
- Análise das pendências identificadas pela professora na Release 1.
- Organização do trabalho e das entregas entre as Sprints 2 e 3.

#sec[3. Síntese dos assuntos discutidos]
*3.1. Responsabilidades.* A equipe discutiu a divisão das atividades de desenvolvimento, gestão do produto, qualidade, integração e acompanhamento Scrum, considerando a rotação de papéis definida para a Release 2.

*3.2. Feedback da Release 1.* Foram abordadas as pendências de documentação das cerimônias, atualização contínua do quadro, revisão de riscos, aprovação de Pull Requests, aplicação da Definition of Done, testes e evidências de qualidade, integração contínua e formalização de releases.

*3.3. Organização das sprints.* A equipe discutiu a separação dos trabalhos entre a Sprint 2 e a Sprint 3. A discriminação de histórias e tarefas apresentada a seguir corresponde ao *planejamento atualmente registrado no Jira* e serve como referência posterior; não representa uma transcrição literal das mensagens de 03/11.

#sec[4. Planejamento de referência no Jira]
*Sprint Goal registrado para a Sprint 2:* Desenvolver as funcionalidades iniciais de planejamento e acompanhamento de entregas do Feneme, permitindo o cadastro de alternativas de trajeto, a consulta de previsão de temperatura e a atualização do status das entregas, com atenção à confiabilidade, segurança e usabilidade.

// ===== PAGINA 2: ENCAMINHAMENTOS =====
#pagebreak()

#sec[4.1. Distribuição de referência das atividades]
#table(
  columns: (23%, 77%),
  inset: (x: 7pt, y: 8pt),
  stroke: 0.45pt + border_color,
  table.header(
    whitehead[Período], whitehead[Histórias e organização atual],
  ),
  [*Sprint 2*\
   03 a 12/11/2026],
  [FT-46: cadastrar alternativas de trajeto; FT-47: consultar previsão de temperatura; FT-48: atualizar status de entrega.

   Melhorias de processo: FT-87 (SM), FT-88 (QA) e FT-89 (PO/DevOps), além de drivers, riscos e indicadores vinculados.],
  [*Sprint 3*\
   Período da R2],
  [FT-56: comparar trajetos; FT-57: receber recomendação; FT-58: consultar entregas atribuídas; FT-49: acompanhar entregas; FT-59: consultar histórico.

   Continuidade das melhorias de processo: FT-90 (SM), FT-91 (QA) e FT-92 (PO/DevOps), além de verificações e riscos associados.],
)

#v(7pt)
#note[Observação: As referências FT-87 a FT-92 e a distribuição detalhada acima documentam o acompanhamento do projeto no Jira e podem incluir formalizações realizadas depois de 03/11. O aceite de estimativas, a capacidade e decisões adicionais devem ser conferidos com a equipe.]

#sec[5. Encaminhamentos e acompanhamento]
#table(
  columns: (18%, 68%, 14%),
  inset: (x: 6pt, y: 7pt),
  stroke: 0.45pt + border_color,
  table.header(
    whitehead[Frente], whitehead[Encaminhamento a acompanhar], whitehead[Resp.],
  ),
  [Scrum], [Registrar atas, calendário e acordos de trabalho; acompanhar quadro, impedimentos e riscos.], [SM],
  [Produto / DevOps], [Conferir prioridades e aceites; acompanhar revisão de PRs, CI e proteção da main.], [PO / DevOps],
  [Qualidade], [Executar e evidenciar testes; acompanhar métricas, defeitos e DoD das histórias.], [QA],
)

#sec[6. Registro e validação]
Esta ata consolida a reunião informada como realizada em 03/11/2026, das 19h às 22h, pelo WhatsApp, com participação dos três integrantes. Foi elaborada posteriormente, com base no relato da reunião, nas atas de referência da Sprint 1 e nos registros atuais do Jira. *Não constitui transcrição das mensagens* e deve ser conferida pelos participantes antes de ser considerada versão definitiva.

#v(5pt)
#text(size: 9pt)[*Rastreabilidade:* Jira FT-87 (Scrum Master), FT-50 (Plano de Releases) e versão Release 2. Documentos utilizados como referência de estrutura: _Ata da Sprint Review — Sprint 1_ e _Ata da Retrospectiva — Sprint 1_, disponíveis no diretório docs/ do repositório.]

#v(9pt)
#block(fill: soft_blue, inset: 10pt, radius: 3pt, width: 100%)[
  *Conferência dos participantes*  —  Pendente de validação dos registros e de eventuais ajustes factuais.
]

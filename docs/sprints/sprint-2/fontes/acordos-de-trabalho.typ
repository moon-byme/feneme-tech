// FENEME | ACORDOS DE TRABALHO DA EQUIPE — RELEASE 2 / SPRINT 2
// Fonte editável para VS Code + Tinymist. Exportar com Typst: Export PDF.
// Aprovação da reunião informada pela Scrum Master (03/11/2026).
// A redação pormenorizada foi consolidada posteriormente com base no Jira e no GitHub;
// conferir com os outros participantes antes de publicar como versão definitiva.

#let ink = rgb("#1b3041")
#let muted = rgb("#425a6f")
#let navy = rgb("#2c4c62")
#let teal = rgb("#087b8f")
#let border-color = rgb("#cfdae3")
#let shade = rgb("#f4f7f9")
#let soft-blue = rgb("#ebf2f6")

#set page(
  paper: "a4",
  margin: (top: 19mm, bottom: 19mm, left: 20mm, right: 20mm),
  footer: context [
    #line(length: 100%, stroke: 0.5pt + border-color)
    #v(4pt)
    #grid(
      columns: (1fr, auto),
      text(fill: muted, size: 8pt)[Feneme | Acordos de trabalho — Release 2],
      text(fill: muted, size: 8pt)[Página #counter(page).display()],
    )
  ],
)
#set text(font: ("Arial", "Liberation Sans", "Noto Sans"), size: 9.5pt, fill: ink, lang: "pt")
#set par(leading: 0.52em)

#let sec(label) = block(above: 12pt, below: 6pt)[
  #text(fill: ink, weight: "bold", size: 12pt)[#label]
]
#let whitehead(body) = table.cell(fill: navy, inset: 7pt)[
  #text(fill: white, weight: "bold", size: 9.1pt)[#body]
]
#let note(body) = text(fill: muted, size: 8.9pt, style: "italic")[#body]

#text(fill: teal, weight: "bold", size: 9.5pt)[FENEME / ORGANIZAÇÃO DA EQUIPE]
#v(5pt)
#text(fill: ink, weight: "bold", size: 20pt)[Acordos de trabalho]
#v(4pt)
#text(fill: muted, size: 10.5pt)[Release 2 — Sprints 2 e 3]
#v(10pt)
#line(length: 100%, stroke: 1.2pt + teal)
#v(10pt)

#table(
  columns: (28%, 72%),
  inset: (x: 7pt, y: 5pt),
  stroke: 0.45pt + border-color,
  table.cell(fill: shade)[*Reunião de origem*], [Sprint Planning 2, em 03/11/2026],
  table.cell(fill: shade)[*Horário e modalidade*], [19h às 22h — reunião remota por mensagens no WhatsApp],
  table.cell(fill: shade)[*Situação*], [Aprovação dos acordos na reunião informada pela Scrum Master; redação detalhada consolidada posteriormente.],
  table.cell(fill: shade)[*Aplicação*], [Release 2; revisão dos acordos quando necessária nas Sprints 2 e 3.],
)

#sec[1. Participantes e responsabilidades]
#table(
  columns: (51%, 49%),
  inset: (x: 7pt, y: 6pt),
  stroke: 0.45pt + border-color,
  table.header(whitehead[Integrante], whitehead[Papel na Release 2]),
  [Lethycia Zenaide Queiroz Melo], [Scrum Master (SM)],
  [João Paulo de Araujo], [Product Owner (PO) / DevOps],
  [José Araújo Agra Neto], [Quality Assurance (QA)],
)

#sec[2. Finalidade]
Padronizar o acompanhamento do projeto, a comunicação, o uso do Jira e o fluxo de alterações no GitHub durante a Release 2. Os acordos buscam evitar a concentração de atualizações no encerramento da sprint, a integração de código sem revisão e a conclusão de histórias sem evidências suficientes de qualidade.

#sec[3. Comunicação e acompanhamento]
#table(
  columns: (27%, 73%),
  inset: (x: 7pt, y: 7pt),
  stroke: 0.45pt + border-color,
  table.header(whitehead[Assunto], whitehead[Procedimento consolidado]),
  [*Comunicação*], [O WhatsApp pode ser utilizado para alinhamentos rápidos; decisões que afetem escopo, tarefas, aceite ou impedimentos devem ficar registradas no Jira.],
  [*Quadro de tarefas*], [Cada responsável atualiza a sua issue conforme o trabalho evolui, com status coerente e evidências disponíveis. Evitar atualizações concentradas apenas no último dia.],
  [*Bloqueios*], [Sinalizar impedimentos assim que forem identificados, informando motivo, impacto, pessoa responsável pelo encaminhamento e situação atual. O SM acompanha a resolução.],
  [*Cerimônias*], [Seguir o calendário publicado, registrar data, horário, participantes, pauta e decisões reais nas atas e indicar mudanças de agendamento.],
)

#pagebreak()

#sec[4. Desenvolvimento, revisão e integração]
#table(
  columns: (28%, 72%),
  inset: (x: 7pt, y: 7pt),
  stroke: 0.45pt + border-color,
  table.header(whitehead[Assunto], whitehead[Procedimento consolidado]),
  [*Branches e PRs*], [Realizar mudanças em branch própria, vinculadas à issue correspondente (FT-XX), e integrar à `main` por Pull Request. Preencher o modelo de PR com descrição, riscos e testes executados.],
  [*Revisão obrigatória*], [Obter ao menos uma aprovação de outro integrante *antes* do merge. Se novos commits invalidarem a aprovação, realizar nova revisão. Resolver conversas pendentes no PR.],
  [*Checagens do CI*], [Integrar somente após aprovação das verificações obrigatórias configuradas: `Backend - Django checks and tests`, `Frontend - build and tests` e `E2E - Cucumber/Cypress (@smoke)`.],
  [*Proteção da main*], [Respeitar a proteção aplicada à `main`, inclusive para administradores, sem push direto, force push, exclusão da branch ou contorno das exigências de revisão.],
)

#sec[5. Qualidade, conclusão e aceite]
#table(
  columns: (28%, 72%),
  inset: (x: 7pt, y: 7pt),
  stroke: 0.45pt + border-color,
  table.header(whitehead[Assunto], whitehead[Procedimento consolidado]),
  [*Critérios de aceite*], [O PO esclarece dúvidas e registra decisões de produto nas issues durante a sprint, além do aceite ou rejeição fundamentados na Review.],
  [*Testes e defeitos*], [O QA registra cenários, resultados e evidências, identifica casos críticos `@smoke` e abre bug específico para defeito confirmado, com severidade e rastreabilidade.],
  [*Definition of Done*], [Uma história não deve ser movida para Concluído apenas por ter código implementado: verificar critérios aplicáveis, testes, evidências, PR integrado, revisão e aceite do PO. Pendências devem permanecer visíveis.],
  [*Métricas e riscos*], [O SM acompanha burndown e impedimentos durante a sprint e coordena, no encerramento, a revisão dos riscos R01–R09. A velocity deve distinguir status no Jira de trabalho efetivamente comprovado pela DoD.],
)

#sec[6. Registro, acompanhamento e revisão dos acordos]
- *Scrum Master:* facilitar o acompanhamento, registrar cerimônias, calendário, impedimentos e revisão de riscos (FT-87 e FT-90).
- *PO/DevOps:* acompanhar prioridades, aceites, proteção da `main`, revisão dos PRs e pipeline (FT-89 e FT-92).
- *QA:* executar e registrar verificações, defeitos, métricas e checagem da DoD (FT-88 e FT-91).
- *Todos:* cumprir os acordos e registrar divergências ou necessidade de atualização durante a sprint.

#v(7pt)
#block(fill: soft-blue, inset: 10pt, radius: 3pt, width: 100%)[
  *Registro de origem e conferência:* a aprovação dos acordos em 03/11/2026 foi informada pela Scrum Master. Este documento foi redigido posteriormente a partir das práticas descritas no Jira, no guia `docs/devops/protecao-main.md` e em `CONTRIBUTING.md`. Como não é uma transcrição do WhatsApp, a formulação de cada regra deve ser conferida pelos três participantes antes da publicação definitiva.
]

#v(6pt)
#note[Rastreabilidade: Jira FT-87, FT-88, FT-89, FT-90, FT-91 e FT-92; documento de proteção da main; instruções de contribuição do repositório Feneme.]

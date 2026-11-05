// FENEME | CALENDARIO DE CERIMONIAS - SPRINT 2
// Edite os dados abaixo no VS Code e exporte com Tinymist: Typst: Export PDF.
// Datas e horarios futuros sao PROPOSTAS; atualizar apos confirmacao da equipe.

#let ink = rgb("#1b3041")
#let muted = rgb("#425a6f")
#let navy = rgb("#2c4c62")
#let teal = rgb("#087b8f")
#let border_color = rgb("#cfdae3")
#let shade = rgb("#f4f7f9")

#set page(
  paper: "a4",
  margin: (top: 20mm, bottom: 20mm, left: 20mm, right: 20mm),
  footer: context [
    #line(length: 100%, stroke: 0.5pt + border_color)
    #v(4pt)
    #grid(
      columns: (1fr, auto),
      text(fill: muted, size: 8pt)[Feneme | Planejamento e acompanhamento da Sprint 2],
      text(fill: muted, size: 8pt)[Página #counter(page).display()],
    )
  ],
)
#set text(font: ("Arial", "Liberation Sans", "Noto Sans"), size: 9.8pt, fill: ink, lang: "pt")
#set par(leading: 0.55em)

#let sec(label) = block(above: 14pt, below: 8pt)[
  #text(fill: ink, weight: "bold", size: 12pt)[#label]
]
#let whitehead(body) = table.cell(fill: navy, inset: 7pt)[
  #text(fill: white, weight: "bold", size: 9.2pt)[#body]
]

#text(fill: muted, size: 9.5pt)[FENEME / RELEASE 2]
#v(6pt)
#text(fill: ink, weight: "bold", size: 19.8pt)[Calendário de cerimônias e alinhamentos]
#v(7pt)
#text(fill: muted, size: 10.2pt)[Sprint 2: 03 a 12 de novembro de 2026 | Scrum Master: Lethycia Zenaide Queiroz Melo]
#v(12pt)

#sec[Agenda da Sprint 2]
#table(
  columns: (18%, 17%, 43%, 22%),
  inset: (x: 5.3pt, y: 8pt),
  stroke: 0.45pt + border_color,
  table.header(
    whitehead[Data], whitehead[Horário], whitehead[Evento], whitehead[Situação / modalidade],
  ),
  [03/11/2026\
   Terça-feira],
  [19h–22h],
  [*Sprint Planning 2*\
   Distribuição de responsabilidades, análise do feedback da R1 e planejamento das Sprints 2 e 3.],
  [#text(fill: teal, weight: "bold")[Realizada]\
   WhatsApp],
  [06/11/2026\
   Sexta-feira],
  [20h\
   #text(fill: muted, size: 8.8pt)[Término a definir]],
  [*Alinhamento complementar*\
   Validar pendências da Planning, acordos de trabalho, impedimentos e próximos passos.],
  [Prevista\
   Plataforma a confirmar],
  [12/11/2026\
   Quinta-feira],
  [A confirmar],
  [*Sprint Review 2*\
   Demonstrar o incremento e registrar feedback e aceite do PO.],
  [Prevista\
   Modalidade a confirmar],
  [12/11/2026\
   Quinta-feira],
  [A confirmar],
  [*Sprint Retrospective 2*\
   Avaliar o processo, revisar impedimentos e definir melhorias para a Sprint 3.],
  [Prevista\
   Modalidade a confirmar],
)

#sec[Acompanhamento durante a sprint]
#text(fill: muted)[Acompanhamento das tarefas pelo Jira durante a Sprint 2, com identificação de bloqueios e atualização das issues ao longo da execução. Caso a equipe combine reuniões rápidas ou horários fixos adicionais, registrá-los após confirmação. Atualizações por mensagens não devem ser descritas como reuniões realizadas.]

#sec[Observações e validação]
#text(fill: muted)[A reunião de 03/11 foi informada como realizada pelos três integrantes via WhatsApp. As reuniões futuras são previsões, não evidências de realização. Horários, plataforma e participantes dos encontros de 06 e 12/11 deverão ser confirmados pela equipe.]

#v(4pt)
#text(fill: muted)[Responsáveis da Release 2: Scrum Master — Lethycia Zenaide Queiroz Melo; PO/DevOps — João Paulo de Araujo; QA — José Araújo Agra Neto.]

#v(8pt)
#text(fill: muted, size: 8.8pt)[Referência: Jira FT-87 (organização e acompanhamento da Sprint 2). Este calendário é complementar às atas e às evidências registradas no Jira/GitHub.]

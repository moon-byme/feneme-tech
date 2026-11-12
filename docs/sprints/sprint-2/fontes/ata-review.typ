// FENEME | REGISTRO DA SPRINT REVIEW — SPRINT 2
// Fonte editável para VS Code + Tinymist. Confirmar a data com o histórico da reunião.

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
      text(fill: muted, size: 8pt)[Feneme | Sprint Review — Sprint 2],
      text(fill: muted, size: 8pt)[Página #counter(page).display()],
    )
  ],
)
#set text(font: ("Arial", "Liberation Sans", "Noto Sans"), size: 9.5pt, fill: ink, lang: "pt")
#set par(leading: 0.52em)

#let sec(label) = block(above: 12pt, below: 6pt)[
  #text(fill: ink, weight: "bold", size: 12pt)[#label]
]

#text(fill: teal, weight: "bold", size: 9.5pt)[FENEME / CERIMÔNIAS DA SPRINT]
#v(5pt)
#text(fill: ink, weight: "bold", size: 20pt)[Registro da reunião de revisão]
#v(4pt)
#text(fill: muted, size: 10.5pt)[Sprint 2 — Release 2]
#v(10pt)
#line(length: 100%, stroke: 1.2pt + teal)
#v(10pt)

#table(
  columns: (29%, 71%),
  inset: (x: 7pt, y: 5pt),
  stroke: 0.45pt + border-color,
  table.cell(fill: shade)[*Data*], [11/11/2026 — confirmar conforme o histórico do chat],
  table.cell(fill: shade)[*Horário*], [20h às 22h],
  table.cell(fill: shade)[*Modalidade*], [Reunião remota por mensagens],
  table.cell(fill: shade)[*Participantes*], [Lethycia Zenaide Queiroz Melo (Scrum Master); João Paulo de Araujo (Product Owner/DevOps); José Araújo Agra Neto (QA).],
)

#sec[1. Demonstração e validação do incremento]

Durante a reunião remota por mensagens, realizada das 20h às 22h, a equipe apresentou e conferiu as funcionalidades desenvolvidas na Sprint 2, com participação do Scrum Master, Product Owner e QA.

O QA solicitou a verificação das funcionalidades disponíveis. Após a apresentação e discussão das evidências, os integrantes confirmaram as alterações realizadas, conforme os registros da conversa.

#sec[2. Aceites do Product Owner]

Foram consideradas as histórias FT-46, FT-47, FT-56 e FT-58, cujos aceites já estavam registrados pelo Product Owner no Jira. A FT-58 permaneceu aceita com ressalva referente à ausência de revisão formal do PR original.

#sec[3. Repriorização do backlog e releases]

Também foi discutida a repriorização do backlog, registrada na FT-89, e sugestões para as próximas releases. Permanece pendente a definição do escopo das Releases 3 e 4.

#sec[4. Sugestões futuras de usabilidade]

Foram discutidas sugestões futuras de melhorias de usabilidade, incluindo uma área de perguntas e respostas frequentes, sem necessariamente implementar um assistente virtual. A aplicabilidade das sugestões às versões web e mobile deverá ser refinada conforme a decisão da equipe.

#sec[5. Evidências]

Histórico das mensagens da reunião, comentários das histórias no Jira e resultados das verificações de QA.

#v(8pt)
#block(fill: soft-blue, inset: 10pt, radius: 3pt, width: 100%)[
  *Ponto a confirmar:* validar a data da reunião no histórico do chat antes da publicação definitiva deste registro.
]

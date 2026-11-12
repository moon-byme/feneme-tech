// FENEME | ATA DE RETROSPECTIVA — SPRINT 2
// Fonte editável para VS Code + Tinymist.

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
      text(fill: muted, size: 8pt)[Feneme | Retrospectiva — Sprint 2],
      text(fill: muted, size: 8pt)[Página #counter(page).display()],
    )
  ],
)
#set text(font: ("Arial", "Liberation Sans", "Noto Sans"), size: 9.5pt, fill: ink, lang: "pt")
#set par(leading: 0.52em)

#let sec(label) = block(above: 12pt, below: 6pt)[
  #text(fill: ink, weight: "bold", size: 12pt)[#label]
]
#let table-head(body) = table.cell(fill: navy, inset: 6pt)[
  #text(fill: white, weight: "bold", size: 8.7pt)[#body]
]

#text(fill: teal, weight: "bold", size: 9.5pt)[FENEME / DOCUMENTAÇÃO DE CERIMÔNIAS]
#v(5pt)
#text(fill: ink, weight: "bold", size: 20pt)[Ata de retrospectiva]
#v(4pt)
#text(fill: muted, size: 10.5pt)[Sprint 2 · Release 2 · Feneme]
#v(10pt)
#line(length: 100%, stroke: 1.2pt + teal)
#v(10pt)

#table(
  columns: (29%, 71%),
  inset: (x: 7pt, y: 5pt),
  stroke: 0.45pt + border-color,
  table.cell(fill: shade)[*Período da sprint*], [03/11/2026 a 12/11/2026],
  table.cell(fill: shade)[*Reunião*], [Presencial | 12/11/2026, das 19h às 19h30],
  table.cell(fill: shade)[*Participantes informados*], [João Paulo de Araujo (Product Owner); José Neto (DevOps); QA; Lethycia Zenaide (Scrum Master).],
  table.cell(fill: shade)[*Facilitação*], [Scrum Master],
)

#block(fill: soft-blue, inset: 9pt, radius: 3pt, width: 100%)[
  *Natureza do registro:* síntese do que foi informado sobre a reunião presencial. O nome da pessoa participante de QA e os responsáveis pelas ações devem ser confirmados antes da publicação definitiva.
]

#sec[1. Objetivo da retrospectiva]

Avaliar a condução da Sprint 2, o trabalho concluído, o processo de revisão e integração e as melhorias a adotar nas próximas sprints, especialmente a análise prévia de dependências entre tarefas e histórias de diferentes sprints.

#sec[2. Balanço da Sprint 2]

Os integrantes revisaram presencialmente as atividades e funcionalidades concluídas durante a sprint, discutindo os resultados e o trabalho realizado.

Foi realizada a conferência e o preenchimento da Definition of Done (DoD) da sprint. As ressalvas e eventuais critérios sem comprovação devem permanecer rastreáveis no Jira e na planilha oficial.

Foram revisadas e aprovadas Pull Requests de outros integrantes, reforçando a prática de revisão por pares antes da integração.

Foram consideradas novas funcionalidades e melhorias para versões futuras, sem transformar sugestões em compromissos de desenvolvimento antes do refinamento e da priorização pelo Product Owner.

#sec[3. Aspectos positivos]

- Colaboração entre os integrantes na conferência das entregas e na revisão de código.
- Maior atenção ao registro de evidências, critérios da DoD e aprovação de Pull Requests.
- Discussão conjunta das melhorias possíveis para o produto e para a organização das próximas sprints.

#sec[4. Pontos de atenção identificados]

- Dependências entre tarefas e histórias de usuário previstas para sprints diferentes podem impedir a conclusão de itens selecionados prematuramente.
- A distribuição de tarefas precisa considerar a ordem real de implementação dos pré-requisitos, não apenas a prioridade isolada da issue.
- Os registros de conclusão, DoD, aprovações e alterações de escopo devem permanecer coerentes entre Jira, GitHub e os documentos da equipe.

#sec[5. Decisão de melhoria para as próximas sprints]

A equipe decidiu que, antes de selecionar ou iniciar uma Task ou US, deve verificar suas dependências e confirmar se os pré-requisitos estão concluídos ou previstos em tempo hábil. Quando uma tarefa depender de outra planejada para uma sprint posterior, a equipe deve discutir o ajuste de sequência e/ou escopo com o Product Owner, atualizar os vínculos no Jira e registrar o encaminhamento, evitando assumir como entregável um item ainda bloqueado.

#sec[6. Plano de ações de melhoria]

#table(
  columns: (4.8fr, 2fr, 1.8fr),
  inset: (x: 6pt, y: 5pt),
  stroke: 0.45pt + border-color,
  table.header(table-head[Ação acordada / encaminhamento], table-head[Responsável sugerido\*], table-head[Quando]),
  [Revisar dependências entre Stories, Tasks, drivers e riscos antes de selecionar os itens da sprint; conferir bloqueios entre sprints.], [PO + SM + equipe], [Antes de cada Planning],
  [Atualizar no Jira os vínculos de dependência e registrar justificativas ao mover itens entre sprints.], [Responsável pela issue + PO], [Durante refinamento e Planning],
  [Conferir DoR, testes e DoD com evidências; preservar ressalvas e itens que não puderem ser validados.], [QA + PO + equipe], [Antes de marcar Concluído],
  [Manter aprovação por outro integrante e verificações de CI antes do merge, acompanhando possíveis exceções.], [DevOps + revisores], [Em cada PR],
  [Refinar ideias de funcionalidades futuras e decidir inclusão ou postergação no backlog, conforme valor e capacidade.], [PO + equipe], [Próximo refinamento],
)

#text(fill: muted, size: 8.9pt, style: "italic")[Os responsáveis acima são sugestões de encaminhamento por papel. Confirmar a atribuição com a equipe.]

#sec[7. Encaminhamentos e evidências]

Registrar esta ata em `docs/sprints/sprint-2/` no GitHub e vincular seu link à FT-87 no Jira. Manter os registros da DoD na FT-38 e na planilha oficial, as decisões do PO na FT-89 e os exemplos de PRs revisados no repositório.

*Referências:* FT-87 (Scrum Master); FT-88 (QA); FT-89 (PO/DevOps); FT-38 (DoD); GitHub moon-byme/feneme-tech.

#v(8pt)
#block(fill: soft-blue, inset: 10pt, radius: 3pt, width: 100%)[
  *Validação desta ata:* a data e o horário da reunião foram informados como 12/11/2026, das 19h às 19h30, presencial. Confirmar o nome da pessoa participante de QA e as atribuições das ações antes da aprovação e publicação definitiva.
]

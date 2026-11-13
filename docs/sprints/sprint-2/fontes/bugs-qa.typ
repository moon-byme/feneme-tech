// FENEME | RELATÓRIO DE ACHADOS DE QA — SPRINT 2
// Fonte editável em Typst.

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
      text(fill: muted, size: 8pt)[Feneme | Achados de QA — Sprint 2],
      text(fill: muted, size: 8pt)[Página #counter(page).display()],
    )
  ],
)
#set text(font: ("Arial", "Liberation Sans", "Noto Sans"), size: 9.5pt, fill: ink, lang: "pt")
#set par(leading: 0.52em)
#set heading(numbering: none)

#let sec(label) = block(above: 12pt, below: 6pt)[
  #text(fill: ink, weight: "bold", size: 12pt)[#label]
]
#let table-head(body) = table.cell(fill: navy, inset: 6pt)[
  #text(fill: white, weight: "bold", size: 8.7pt)[#body]
]
#let field(label, body) = [
  *#label:* #body \
]

#text(fill: teal, weight: "bold", size: 9.5pt)[FENEME / DOCUMENTAÇÃO DE QA]
#v(5pt)
#text(fill: ink, weight: "bold", size: 20pt)[Relatório de achados]
#v(4pt)
#text(fill: muted, size: 10.5pt)[Sprint 2 · Release 2 · Feneme]
#v(10pt)
#line(length: 100%, stroke: 1.2pt + teal)
#v(10pt)

#table(
  columns: (29%, 71%),
  inset: (x: 7pt, y: 5pt),
  stroke: 0.45pt + border-color,
  table.cell(fill: shade)[*Escopo*], [Análise de três defeitos candidatos relacionados às histórias FT-55, FT-44 e FT-47.],
  table.cell(fill: shade)[*Classificação informada*], [Prioridades sugeridas: duas médias e uma baixa. A severidade formal não foi especificada para cada achado.],
)

#block(fill: soft-blue, inset: 9pt, radius: 3pt, width: 100%)[
  *Resumo de severidade:* não foi identificado nenhum achado com severidade superior à média. Os casos abaixo são candidatos a defeito; a classificação formal de severidade deve ser confirmada no Jira.
]

#sec[1. Problemas encontrados]

#text(fill: ink, weight: "bold", size: 11pt)[1.1 Lista vazia exibida quando a consulta falha]

#field[Prioridade sugerida][Média]
#field[História relacionada][#link("https://feneme.atlassian.net/browse/FT-55")[FT-55 — Consultar entregas cadastradas]]

No painel do Gestor, quando a primeira consulta à API de entregas falha, o sistema pode exibir ao mesmo tempo uma mensagem de erro e a mensagem *“Nenhuma entrega cadastrada”*. Uma falha na consulta não comprova que não existam registros.

*Passos para reproduzir:*

+ Entrar como Gestor e simular uma falha de servidor (HTTP 500) na consulta `GET /api/deliveries/`.
+ Observar a lista de entregas.
+ Verificar se aparece a mensagem de lista vazia, apesar de a consulta não ter sido concluída com sucesso.

*Resultado esperado:* exibir somente a mensagem de falha e oferecer uma opção para tentar novamente.

*Causa identificada:* o componente #link("https://github.com/moon-byme/feneme-tech/blob/main/frontend/src/App.tsx")[`frontend/src/App.tsx`] usa o tamanho do array `deliveries` para decidir quando mostrar o estado vazio, sem distinguir a ausência de registros de uma falha de carregamento.

#sec[1.2 Cadastro apresenta apenas um dos campos inválidos]

#field[Prioridade sugerida][Baixa]
#field[História relacionada][#link("https://feneme.atlassian.net/browse/FT-44")[FT-44 — Cadastrar entrega e dados da carga]]

A história exige que os dados que precisam de correção sejam indicados ao usuário. Quando o backend devolve erros para vários campos simultaneamente, a função `errorMessage()` do frontend seleciona somente a primeira mensagem.

*Passos para reproduzir:*

+ Entrar como Gestor.
+ Preencher origem, destino e descrição da carga somente com espaços.
+ Tentar cadastrar.
+ Observar se todos os campos inválidos são identificados ou se aparece apenas o primeiro erro.

*Resultado esperado:* informar todos os campos obrigatórios inválidos ou destacar cada campo correspondente.

*Causa identificada:* a função `errorMessage()` em #link("https://github.com/moon-byme/feneme-tech/blob/main/frontend/src/api.ts")[`frontend/src/api.ts`], linhas 21–30, seleciona apenas uma mensagem.

#sec[1.3 Previsão de temperatura de localidade diferente da selecionada]

#field[Prioridade sugerida][Média]
#field[História relacionada][#link("https://feneme.atlassian.net/browse/FT-47")[FT-47 — Consultar previsão de temperatura]]

Há uma possível condição de concorrência no componente de previsão: a localidade pode ser alterada enquanto uma consulta está em andamento. Nesse caso, o campo pode indicar Campina Grande enquanto o resultado exibido pertence à consulta anterior para João Pessoa.

*Passos para reproduzir:*

+ Selecionar João Pessoa e clicar em *Consultar previsão*.
+ Antes de a API responder, mudar a seleção para Campina Grande.
+ Aguardar o término da primeira consulta.

*Resultado esperado:* descartar a resposta anterior, cancelar a consulta ou impedir a troca de localidade durante o carregamento.

*Causa identificada:* em #link("https://github.com/moon-byme/feneme-tech/blob/main/frontend/src/components/TemperatureForecast.tsx")[`frontend/src/components/TemperatureForecast.tsx`], a seleção pode mudar durante a consulta, mas a resposta assíncrona é apresentada sem verificar se ainda corresponde à localidade selecionada.

Esse defeito afeta uma funcionalidade concluída na Sprint 2 e não depende de funcionalidade futura.

#sec[2. Síntese]

#table(
  columns: (3.3fr, 1.7fr, 2fr),
  inset: (x: 6pt, y: 5pt),
  stroke: 0.45pt + border-color,
  table.header(table-head[Achado], table-head[Prioridade sugerida], table-head[História]),
  [Lista vazia após falha na consulta], [Média], [FT-55],
  [Exibição de apenas um campo inválido], [Baixa], [FT-44],
  [Resultado de outra localidade], [Média], [FT-47],
)

Os três casos são problemas de tratamento de erro ou apresentação de informações, não solicitações de novas funcionalidades. As prioridades acima são as sugeridas no levantamento; elas não substituem a classificação formal de severidade no Jira.

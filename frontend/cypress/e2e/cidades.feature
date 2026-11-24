# language: pt
# US-14 (FT-113); R08 (FT-67).

@R2
Funcionalidade: Lista única de cidades
  Como Gestor
  Quero escolher origem e destino em uma lista fechada de cidades
  Para evitar erros de digitação e usar coordenadas conhecidas

  @US-14 @smoke
  Cenário: Cadastro com cidades da lista
    Dado que estou autenticado como Gestor
    Quando abro o cadastro de entrega
    Então origem e destino são campos de seleção com as 26 cidades da lista
    E a previsão do clima oferece exatamente as mesmas cidades

  @US-14 @excecao @smoke
  Cenário: Origem igual ao destino
    Dado que estou autenticado como Gestor
    Quando seleciono a mesma cidade como origem e destino
    E tento salvar a entrega
    Então o sistema rejeita o cadastro e indica o campo com erro

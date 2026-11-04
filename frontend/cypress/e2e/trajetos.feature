# language: pt
# US-06 (FT-46), US-07 (FT-56); CT-06, CT-07, CT-18, CT-19.

@R2
Funcionalidade: Cadastro e comparação de alternativas de trajeto
  Como Gestor
  Quero registrar e comparar alternativas de trajeto
  Para avaliar distância e duração antes de decidir

  Contexto:
    Dado que estou autenticado como Gestor
    E existe uma entrega cadastrada

  @US-06 @CT-18 @regressao
  Cenário: Cadastrar até duas alternativas válidas
    Dado que ainda há espaço para cadastrar alternativas nessa entrega
    Quando informo até duas alternativas com distância e duração válidas
    E confirmo o cadastro
    Então o sistema salva as alternativas
    E associa os dados à entrega

  @US-06 @CT-07 @excecao @regressao
  Cenário: Impedir cadastro de uma terceira alternativa
    Dado que a entrega já possui duas alternativas cadastradas
    Quando tento registrar uma terceira alternativa
    Então o sistema impede o registro
    E informa que o limite é de duas alternativas

  @US-06 @CT-07 @excecao @regressao
  Cenário: Rejeitar distância ou duração inválida
    Dado que estou preenchendo os dados de uma alternativa de trajeto
    Quando informo uma distância ou duração inválida
    Então o sistema rejeita o registro
    E identifica o valor que deve ser corrigido

  @US-07 @CT-06 @regressao
  Cenário: Comparar duas alternativas cadastradas
    Dado que a entrega possui duas alternativas cadastradas
    Quando solicito a comparação
    Então o sistema exibe as duas alternativas lado a lado
    E apresenta a distância e o tempo informados para cada uma

  @US-07 @CT-19 @excecao @regressao
  Cenário: Não comparar quando há menos de duas alternativas
    Dado que a entrega possui menos de duas alternativas cadastradas
    Quando solicito a comparação de dois trajetos
    Então o sistema informa que faltam alternativas
    E não apresenta uma comparação fictícia

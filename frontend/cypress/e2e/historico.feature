# language: pt
# US-13 (FT-59); CT-12, CT-26.

@R2
Funcionalidade: Consulta do histórico de uma entrega
  Como Gestor
  Quero consultar o histórico das mudanças de status
  Para verificar o progresso registrado durante o transporte

  Contexto:
    Dado que estou autenticado como Gestor
    E existe uma entrega cadastrada

  @US-13 @CT-12 @regressao
  Cenário: Consultar histórico com mudanças registradas
    Dado que a entrega possui mudanças de status registradas
    Quando consulto o histórico da entrega
    Então o sistema exibe as alterações persistidas
    E organiza os registros em ordem cronológica

  @US-13 @CT-26 @excecao @regressao
  Cenário: Consultar histórico sem alterações registradas
    Dado que a entrega não possui alterações de status registradas
    Quando consulto seu histórico
    Então o sistema informa que ainda não há mudanças registradas
    E exibe o status atual quando disponível

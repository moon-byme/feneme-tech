# language: pt
# US-13 (FT-59); CT-12, CT-26.

@R2
Funcionalidade: Consulta do histórico de uma entrega
  Como Gestor
  Quero consultar o histórico das mudanças de status
  Para verificar o progresso registrado durante o transporte

  @US-13 @CT-12 @regressao
  Cenário: Consultar histórico com mudanças registradas
    Dado que criei uma entrega com duas alterações reais para consulta do histórico
    Quando abro o histórico dessa entrega como Gestor
    Então vejo as duas transições persistidas na ordem correta

  @US-13 @CT-26 @excecao @regressao
  Cenário: Consultar histórico sem alterações registradas
    Dado que criei uma entrega sem alterações para consulta do histórico
    Quando abro o histórico dessa entrega como Gestor
    Então vejo mensagem de histórico vazio e o status Pendente

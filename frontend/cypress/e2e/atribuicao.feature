# language: pt
# US-05 (FT-45); CT-05, CT-17.

@R1
Funcionalidade: Atribuição de motorista a uma entrega
  Como Gestor
  Quero atribuir um Motorista a uma entrega
  Para identificar o responsável pelo transporte

  @US-05 @CT-05 @regressao
  Cenário: Atribuir Motorista válido a uma entrega
    Dado que estou autenticado como Gestor
    E existe uma entrega cadastrada
    E existe um usuário válido com perfil Motorista
    Quando associo o Motorista à entrega
    Então o sistema salva a atribuição
    E disponibiliza a entrega ao Motorista responsável

  @US-05 @CT-17 @excecao @regressao
  Cenário: Rejeitar atribuição a usuário que não é Motorista
    Dado que estou autenticado como Gestor
    E existe uma entrega cadastrada
    E existe um usuário que não possui perfil Motorista
    Quando tento atribuir a entrega a esse usuário
    Então o sistema rejeita a atribuição
    E informa o motivo da rejeição
    E mantém o responsável anteriormente registrado

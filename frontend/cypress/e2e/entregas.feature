# language: pt
# US-03 (FT-44), US-04 (FT-55); CT-03, CT-04, CT-15, CT-16.

@R1
Funcionalidade: Cadastro e consulta de entregas
  Como Gestor
  Quero cadastrar e consultar entregas
  Para organizar as operações logísticas

  @US-03 @CT-03 @regressao
  Cenário: Cadastrar entrega com dados válidos
    Dado que estou autenticado como Gestor
    E preenchi os campos obrigatórios aprovados para uma entrega
    Quando confirmo o cadastro da entrega
    Então o sistema registra a entrega
    E gera uma identificação para ela
    E permite recuperar as informações salvas

  @US-03 @CT-04 @excecao @regressao
  Cenário: Impedir cadastro com campos obrigatórios ausentes
    Dado que estou autenticado como Gestor
    E estou preenchendo o formulário de cadastro de entrega
    Quando tento salvar sem preencher um campo obrigatório
    Então o sistema impede o cadastro
    E indica os dados que precisam de correção

  @US-04 @CT-15 @regressao
  Cenário: Consultar entregas cadastradas
    Dado que estou autenticado como Gestor
    E existem entregas cadastradas
    Quando acesso a consulta de entregas
    Então o sistema lista as entregas registradas
    E permite consultar os dados essenciais de cada uma

  @US-04 @CT-16 @excecao @regressao
  Cenário: Consultar lista sem entregas cadastradas
    Dado que estou autenticado como Gestor
    E não existem entregas cadastradas
    Quando acesso a lista de entregas
    Então o sistema informa que não há entregas para exibir
    E não apresenta registros fictícios

# language: pt
# US-10 (FT-58), US-11 (FT-48), US-12 (FT-49); CT-10, CT-11, CT-22 a CT-25.

@R2
Funcionalidade: Consulta e atualização do status das entregas
  Como Motorista ou Gestor
  Quero consultar e atualizar o status das entregas conforme minhas permissões
  Para acompanhar o andamento do transporte

  @US-10 @CT-22 @regressao @smoke
  Cenário: Motorista consulta suas próprias entregas
    Dado que estou autenticado como Motorista
    E possuo entregas atribuídas
    Quando acesso a lista de minhas entregas
    Então o sistema exibe somente as entregas sob minha responsabilidade
    E apresenta as informações essenciais de cada uma

  @US-10 @CT-22 @interface @smoke
  Cenário: Motorista visualiza suas entregas pela interface
    Dado que estou autenticado como Motorista
    E possuo entregas atribuídas
    Quando acesso a área do Motorista pela interface
    Então a interface mostra a entrega atribuída a mim
    E não mostra a entrega atribuída a outro Motorista

  @US-10 @CT-23 @excecao @regressao @smoke
  Cenário: Motorista tenta consultar entrega atribuída a outra pessoa
    Dado que estou autenticado como Motorista
    E existe uma entrega atribuída a outro Motorista
    Quando tento acessar diretamente essa entrega
    Então a API nega o acesso
    E não expõe os dados dessa entrega

  @US-11 @CT-10 @regressao
  Cenário: Motorista atualiza o status de uma entrega atribuída
    Dado que estou autenticado como Motorista
    E possuo uma entrega atribuída
    E a transição solicitada é permitida
    Quando atualizo o status da entrega
    Então o sistema salva o novo status
    E disponibiliza a atualização para consulta
    E registra a alteração no histórico

  @US-11 @CT-11 @excecao @regressao
  Cenário: Motorista tenta atualizar entrega de outra pessoa
    Dado que estou autenticado como Motorista
    E existe uma entrega atribuída a outro Motorista
    Quando tento alterar o status dessa entrega
    Então o sistema nega a operação
    E preserva o status e o histórico originais

  @US-12 @CT-24 @regressao
  Cenário: Gestor consulta o andamento atualizado das entregas
    Dado que estou autenticado como Gestor
    E existem entregas com status atualizados pelos Motoristas
    Quando acesso o acompanhamento das entregas
    Então o sistema exibe o status atual de cada entrega
    E apresenta as atualizações persistidas pelos Motoristas

  @US-12 @CT-25 @excecao @regressao
  Cenário: Gestor consulta andamento de entrega inexistente
    Dado que estou autenticado como Gestor
    Quando tento consultar o andamento de uma entrega inexistente
    Então o sistema informa que o registro não foi encontrado
    E não apresenta dados de outra entrega

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

  @US-10 @interface @excecao @smoke
  Cenário: Motorista visualiza a mensagem de lista vazia
    Dado que estou autenticado como Motorista
    E a consulta de minhas entregas retorna uma lista vazia
    Quando acesso a área do Motorista pela interface
    Então a interface informa que não há entregas atribuídas

  @US-10 @interface @regressao @smoke
  Cenário: Motorista atualiza a lista após reatribuição de sua entrega
    Dado que estou autenticado como Motorista
    E possuo entregas atribuídas
    Quando acesso a área do Motorista pela interface
    Então a interface mostra a entrega atribuída a mim
    Quando o Gestor reatribui minha entrega a outro Motorista
    E atualizo a lista pela interface
    Então a interface deixa de mostrar a entrega reatribuída

  @US-10 @CT-23 @excecao @regressao @smoke
  Cenário: Motorista tenta consultar entrega atribuída a outra pessoa
    Dado que estou autenticado como Motorista
    E existe uma entrega atribuída a outro Motorista
    Quando tento acessar diretamente essa entrega
    Então a API nega o acesso
    E não expõe os dados dessa entrega

  # O histórico é verificado no PostgreSQL por deliveries.test_delivery_status.
  # A consulta pública de eventos pertence à FT-59.
  @US-11 @CT-10 @regressao @smoke
  Cenário: Motorista atualiza o status de uma entrega atribuída
    Dado que estou autenticado como Motorista
    E possuo entregas atribuídas
    Quando acesso a área do Motorista pela interface
    E inicio o transporte da minha entrega
    Então minha entrega mostra o status "Em transporte"
    Quando confirmo a conclusão da minha entrega
    Então minha entrega mostra o status "Entregue"
    E o controle da minha entrega está finalizado
    E o status Entregue permanece após nova autenticação
    E o Gestor visualiza a entrega finalizada sem controles de alteração

  @US-11 @CT-11 @excecao @regressao @smoke
  Cenário: Motorista tenta atualizar entrega de outra pessoa
    Dado que estou autenticado como Motorista
    E existe uma entrega atribuída a outro Motorista
    Quando tento alterar o status dessa entrega
    Então o sistema nega a operação
    E preserva o status original consultado pelo Gestor

  @US-11 @interface @excecao @smoke
  Cenário: Falha de atualização preserva o status e permite nova tentativa
    Dado que estou autenticado como Motorista
    E possuo entregas atribuídas
    Quando acesso a área do Motorista pela interface
    E a API rejeita temporariamente a alteração da minha entrega
    Então vejo o carregamento sem antecipar o novo status
    E vejo a mensagem de erro da atualização
    E minha entrega mostra o status "Pendente"
    Quando inicio o transporte da minha entrega
    Então minha entrega mostra o status "Em transporte"

  @US-11 @interface @excecao @smoke
  Cenário: Sessão expirada durante atualização de status
    Dado que estou autenticado como Motorista
    E possuo entregas atribuídas
    Quando acesso a área do Motorista pela interface
    E a sessão expira ao iniciar o transporte
    Então volto ao login com mensagem de sessão expirada

  @US-11 @interface @excecao @smoke
  Cenário: Outra sessão já iniciou o transporte
    Dado que estou autenticado como Motorista
    E possuo entregas atribuídas
    Quando acesso a área do Motorista pela interface
    E outra sessão inicia o transporte pela API
    E tento iniciar novamente pela interface
    Então vejo a mensagem de transição não permitida
    Quando atualizo a lista pela interface
    Então minha entrega mostra o status "Em transporte"

  @US-12 @CT-24 @regressao
  Cenário: Gestor consulta o andamento atualizado das entregas
    Dado que o Gestor está autenticado para consultar entregas
    E existem entregas com status atualizados pelos Motoristas
    Quando acesso o acompanhamento das entregas
    Então o sistema exibe o status atual de cada entrega
    E apresenta as atualizações persistidas pelos Motoristas

  @US-12 @CT-25 @excecao @regressao
  Cenário: Gestor consulta andamento de entrega inexistente
    Dado que o Gestor está autenticado para consultar entregas
    E existe outra entrega cadastrada
    Quando tento consultar o andamento de uma entrega inexistente
    Então o sistema informa que o registro não foi encontrado
    E não apresenta dados de outra entrega

  @US-12 @interface @excecao
  Cenário: Falha ao consultar o acompanhamento não é apresentada como lista vazia
    Dado que o Gestor está autenticado para consultar entregas
    Quando a consulta do acompanhamento falha
    Então a interface informa a falha sem indicar lista vazia

# language: pt
# US-09 (FT-57); CT-08, CT-21.

@R2
Funcionalidade: Recomendação indicativa de trajeto
  Como Gestor
  Quero receber uma recomendação de trajeto com justificativa
  Para apoiar minha decisão logística

  Contexto:
    Dado que estou autenticado como Gestor
    E existem duas alternativas válidas para a entrega

  @US-09 @CT-08 @regressao
  Cenário: Apresentar recomendação válida e justificada
    Dado que existe previsão disponível
    E o PO aprovou a regra de recomendação
    Quando solicito a análise dos trajetos
    Então o sistema aplica a regra aprovada
    E informa uma alternativa indicativa
    E apresenta os critérios e valores que justificam o resultado

  @US-09 @CT-21 @excecao @regressao
  Cenário: Não confirmar recomendação climática sem previsão válida
    Dado que os dados meteorológicos necessários estão indisponíveis
    Quando solicito a análise climática
    Então o sistema avisa que não pôde concluir a recomendação climática
    E não apresenta uma recomendação climática como confirmada
    E mantém disponível a comparação manual

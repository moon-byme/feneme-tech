# language: pt
# US-08 (FT-47); CT-09, CT-20.

@R2
Funcionalidade: Consulta de previsão de temperatura
  Como Gestor
  Quero consultar a previsão de temperatura da localidade de referência
  Para considerar a condição climática no planejamento do transporte

  Contexto:
    Dado que estou autenticado como Gestor
    E existe uma localidade de referência válida para a entrega

  @US-08 @CT-20 @regressao
  Cenário: Consultar previsão para localidade válida
    Dado que a Open-Meteo responde com a temperatura necessária
    Quando solicito a previsão
    Então o sistema exibe a temperatura ambiente prevista
    E identifica a localidade e o período de referência

  @US-08 @CT-09 @excecao @regressao
  Cenário: Tratar falha na consulta à Open-Meteo
    Dado que solicito uma previsão meteorológica
    E a Open-Meteo não responde ou retorna erro
    Quando o sistema tenta consultar os dados
    Então informa que a previsão está indisponível
    E mantém disponíveis os fluxos de cadastro e comparação manual

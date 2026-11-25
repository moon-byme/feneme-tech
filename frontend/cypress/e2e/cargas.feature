# language: pt
# US-15 (FT-114); CT-31.

@R2
Funcionalidade: Catálogo de tipos de carga
  Como Gestor
  Quero consultar os tipos de carga com o limite de temperatura e a fonte
  Para entender contra qual temperatura as rotas serão comparadas

  @US-15 @CT-31 @smoke
  Cenário: Gestor consulta o catálogo de tipos de carga
    Dado que estou autenticado como Gestor
    Quando consulto o catálogo de tipos de carga
    Então vejo os 7 tipos de carga com categoria, limite e fonte
    E o limite derivado aparece identificado

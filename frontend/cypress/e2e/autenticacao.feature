# language: pt
# Cenários piloto para validar a integração Cucumber + Cypress no CI.
# Rastreabilidade: US-01 (FT-43), US-02 (FT-54); CT-01, CT-02, CT-13, CT-14.
# A QA amplia este arquivo e cria os demais .feature previstos no Plano de Testes.

@R1
Funcionalidade: Autenticação por perfil
  Como usuário do Feneme
  Quero entrar com meu usuário e senha
  Para acessar apenas as funções do meu perfil

  Contexto:
    Dado que estou na página de login

  @US-01 @CT-01 @smoke @regressao
  Cenário: Login válido do Gestor
    Quando eu entro com o usuário "gestor_e2e" e a senha válida
    Então vejo a área do Gestor

  @US-01 @CT-02 @excecao @regressao
  Cenário: Senha inválida do Gestor
    Quando eu entro com o usuário "gestor_e2e" e a senha "senha-errada"
    Então vejo a mensagem de login inválido
    E continuo na página de login

  @US-02 @CT-13 @smoke @regressao
  Cenário: Login válido do Motorista
    Quando eu entro com o usuário "motorista_e2e" e a senha válida
    Então vejo a área do Motorista

  @US-02 @CT-14 @excecao @regressao
  Cenário: Senha inválida do Motorista
    Quando eu entro com o usuário "motorista_e2e" e a senha "senha-errada"
    Então vejo a mensagem de login inválido
    E continuo na página de login

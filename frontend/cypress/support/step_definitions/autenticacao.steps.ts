import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";

// Senha das contas fictícias criadas por `manage.py seed_e2e_users`.
// Vem da variável CYPRESS_E2E_PASSWORD (CI ou máquina local); nunca use credenciais reais.
const senhaValida = (): string => {
  const senha = Cypress.env("E2E_PASSWORD") as string | undefined;
  if (!senha) throw new Error("Defina CYPRESS_E2E_PASSWORD com a senha das contas de teste.");
  return senha;
};

function entrar(usuario: string, senha: string) {
  cy.get("[data-cy=login-username]").clear().type(usuario);
  cy.get("[data-cy=login-password]").clear().type(senha, { log: false });
  cy.get("[data-cy=login-submit]").click();
}

Given("que estou na página de login", () => {
  cy.clearAllSessionStorage();
  cy.visit("/");
  cy.get("[data-cy=login-page]").should("be.visible");
});

When("eu entro com o usuário {string} e a senha válida", (usuario: string) => {
  entrar(usuario, senhaValida());
});

When("eu entro com o usuário {string} e a senha {string}", (usuario: string, senha: string) => {
  entrar(usuario, senha);
});

Then("vejo a área do Gestor", () => {
  cy.get("[data-cy=role-chip]").should("have.text", "Gestor");
  cy.contains("h1", "Gerencie suas entregas").should("be.visible");
});

Then("vejo a área do Motorista", () => {
  cy.get("[data-cy=role-chip]").should("have.text", "Motorista");
  cy.contains("h2", "Entregas atribuídas").should("be.visible");
});

Then("vejo a mensagem de login inválido", () => {
  cy.get("[data-cy=login-error]")
    .should("be.visible")
    .and("contain.text", "Não foi possível realizar o login");
});

Then("continuo na página de login", () => {
  cy.get("[data-cy=login-page]").should("be.visible");
  cy.get("[data-cy=role-chip]").should("not.exist");
});

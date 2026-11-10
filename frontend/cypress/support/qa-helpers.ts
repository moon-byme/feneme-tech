// Funções compartilhadas pelos cenários de regressão da Sprint 1.

export function senhaE2E(): string {
  const senha = Cypress.env("E2E_PASSWORD") as string | undefined;
  if (!senha) {
    throw new Error("Defina CYPRESS_E2E_PASSWORD com a senha das contas fictícias de teste.");
  }
  return senha;
}

export function autenticarComoGestor(): void {
  cy.clearAllSessionStorage();
  cy.visit("/");
  cy.get("[data-cy=login-page]").should("be.visible");
  cy.get("[data-cy=login-username]").clear().type("gestor_e2e");
  cy.get("[data-cy=login-password]").clear().type(senhaE2E(), { log: false });
  cy.get("[data-cy=login-submit]").click();
  cy.get("[data-cy=role-chip]").should("have.text", "Gestor");
}

export function autenticarComoMotorista(): void {
  cy.clearAllSessionStorage();
  cy.visit("/");
  cy.get("[data-cy=login-page]").should("be.visible");
  cy.get("[data-cy=login-username]").clear().type("motorista_e2e");
  cy.get("[data-cy=login-password]").clear().type(senhaE2E(), { log: false });
  cy.get("[data-cy=login-submit]").click();
  cy.get("[data-cy=role-chip]").should("have.text", "Motorista");
}

export function preencherEntregaUnica(): void {
  const origem = `Origem QA ${Date.now()}`;
  cy.wrap(origem).as("qaOrigin");
  cy.contains("label", "Origem").find("input").clear().type(origem);
  cy.contains("label", "Destino").find("input").clear().type("Destino QA - João Pessoa");
  cy.contains("label", "Descrição da carga")
    .find("textarea")
    .clear()
    .type("Carga de teste automatizado da Sprint 1");
}

export function salvarEntregaPelaInterface(): void {
  cy.intercept("POST", "**/api/deliveries/").as("createDelivery");
  cy.contains("button", "Cadastrar entrega").click();
  cy.wait("@createDelivery").then(({ response }) => {
    expect(response?.statusCode).to.eq(201);
    expect(response?.body?.id).to.be.a("number");
    cy.wrap(response?.body).as("qaDelivery");
  });
}

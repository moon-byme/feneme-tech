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

// US-14 (FT-113): origem e destino vêm da lista fechada de cidades, então não
// identificam uma entrega. A descrição da carga, única por execução, identifica
// o cartão; o alias "qaOrigin" foi mantido para os passos existentes.
export const ORIGEM_TESTE = "Campina Grande - PB";
export const DESTINO_TESTE = "João Pessoa - PB";

export function preencherEntregaUnica(): void {
  const carga = `Carga QA ${Date.now()}`;
  cy.wrap(carga).as("qaOrigin");
  cy.contains("label", "Origem").find("select").select(ORIGEM_TESTE);
  cy.contains("label", "Destino").find("select").select(DESTINO_TESTE);
  cy.contains("label", "Descrição da carga").find("textarea").clear().type(carga);
}

/** IDs das cidades usadas nos cadastros feitos pela API nos testes E2E. */
export function cidadesDeTeste(token: string) {
  return cy.request({
    method: "GET",
    url: "/api/cidades/",
    headers: { Authorization: `Bearer ${token}` },
  }).then(({ body }: { body: Array<{ id: number; slug: string }> }) => {
    const origem = body.find((city) => city.slug === "campina-grande");
    const destino = body.find((city) => city.slug === "joao-pessoa");
    expect(origem, "Campina Grande na lista de cidades").to.exist;
    expect(destino, "João Pessoa na lista de cidades").to.exist;
    return { origin_city: origem!.id, destination_city: destino!.id };
  });
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

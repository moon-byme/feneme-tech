import { When, Then } from "@badeball/cypress-cucumber-preprocessor";
import { ORIGEM_TESTE, preencherEntregaUnica, salvarEntregaPelaInterface } from "../qa-helpers";

function opcoes(selector: string) {
  // As listas chegam da API depois da renderização: espera além do "Selecione...".
  return cy.get(`${selector} option`).should("have.length.greaterThan", 1).then(($options) =>
    [...$options].map((option) => option.textContent?.trim() ?? "").filter((text) => !text.startsWith("Selecione")),
  );
}

When("abro o cadastro de entrega", () => {
  cy.get("[data-cy=delivery-origin]").should("be.visible");
});

Then("origem e destino são campos de seleção com as 26 cidades da lista", () => {
  cy.get("[data-cy=delivery-origin]").should("match", "select");
  cy.get("[data-cy=delivery-destination]").should("match", "select");
  opcoes("[data-cy=delivery-origin]").then((origens) => {
    expect(origens).to.have.length(26);
    expect(origens).to.include("Campina Grande - PB");
    expect(origens).not.to.include("Sousa - PB");
    opcoes("[data-cy=delivery-destination]").should("deep.equal", origens);
  });
});

Then("a previsão do clima oferece exatamente as mesmas cidades", () => {
  // A previsão fica no cartão de cada entrega; cadastra uma para abrir o seletor.
  preencherEntregaUnica();
  salvarEntregaPelaInterface();
  opcoes("[data-cy=delivery-origin]").then((origens) => {
    cy.get("@qaDelivery").then((delivery: any) => {
      opcoes(`[data-cy=forecast-${delivery.id}] [data-cy=forecast-location]`).then((clima) => {
        expect([...clima].sort()).to.deep.equal([...origens].sort());
      });
    });
  });
});

When("seleciono a mesma cidade como origem e destino", () => {
  cy.get("[data-cy=delivery-origin]").select(ORIGEM_TESTE);
  cy.get("[data-cy=delivery-destination]").select(ORIGEM_TESTE);
  cy.contains("label", "Descrição da carga").find("textarea").clear().type(`Carga QA mesma cidade ${Date.now()}`);
});

When("tento salvar a entrega", () => {
  cy.intercept("POST", "**/api/deliveries/").as("qaSameCityDelivery");
  cy.contains("button", "Cadastrar entrega").click();
});

Then("o sistema rejeita o cadastro e indica o campo com erro", () => {
  cy.get("[data-cy=delivery-destination]").should("have.attr", "aria-invalid", "true");
  cy.contains("O destino deve ser diferente da origem.").should("be.visible");
  cy.get("@qaSameCityDelivery.all").should("have.length", 0);
  cy.contains("Entrega cadastrada com sucesso").should("not.exist");
});

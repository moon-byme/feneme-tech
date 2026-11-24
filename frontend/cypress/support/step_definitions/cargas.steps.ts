import { When, Then } from "@badeball/cypress-cucumber-preprocessor";

When("consulto o catálogo de tipos de carga", () => {
  cy.get("[data-cy=cargo-catalog-panel]").scrollIntoView().should("be.visible");
});

Then("vejo os 7 tipos de carga com categoria, limite e fonte", () => {
  cy.get("[data-cy=cargo-type-row]").should("have.length", 7);
  cy.contains("[data-cy=cargo-type-row]", "Tomate (maduro-verde)")
    .should("contain.text", "Hortifrúti")
    .and("contain.text", "27,0 °C")
    .find("a[href^='https://']")
    .should("have.attr", "target", "_blank");
});

Then("o limite derivado aparece identificado", () => {
  cy.get("[data-cy=derived-limit]").should("have.length", 1);
  cy.contains("[data-cy=cargo-type-row]", "Cosméticos e produtos de higiene")
    .find("[data-cy=derived-limit]")
    .should("contain.text", "limite derivado");
});

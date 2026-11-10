// US-08 (FT-47) — Consulta de previsão de temperatura (CT-20 e CT-09).
// A resposta do endpoint de previsão é simulada com cy.intercept para não
// depender da Open-Meteo real no CI. O tratamento das falhas da Open-Meteo no
// back-end é coberto por backend/weather/tests.py (18 cenários simulados).
import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";
import { preencherEntregaUnica, salvarEntregaPelaInterface } from "../qa-helpers";

const LOCALIDADE = { slug: "joao-pessoa", name: "João Pessoa - PB" };

function cartaoDePrevisao(): Cypress.Chainable<JQuery<HTMLElement>> {
  return cy.get("@qaDelivery").then((delivery: any) => cy.get(`[data-cy=forecast-${delivery.id}]`));
}

function selecionarLocalidade(): void {
  cartaoDePrevisao().find("[data-cy=forecast-location]").select(LOCALIDADE.slug);
}

Given("existe uma localidade de referência válida para a entrega", () => {
  preencherEntregaUnica();
  salvarEntregaPelaInterface();
  cartaoDePrevisao()
    .find("[data-cy=forecast-location] option")
    .should(($options) => {
      expect([...$options].map((option) => option.textContent)).to.include(LOCALIDADE.name);
    });
});

// Cenário: previsão disponível (CT-20)
Given("que a Open-Meteo responde com a temperatura necessária", () => {
  cy.intercept("GET", "**/api/weather/forecast/**", {
    statusCode: 200,
    body: {
      location: LOCALIDADE,
      date: "2026-11-10",
      temperature_max: 31.2,
      temperature_min: 23.5,
      unit: "°C",
      source: "Open-Meteo",
      notice: "Previsão de temperatura ambiente; não é a temperatura medida da carga.",
    },
  }).as("forecast");
});

When("solicito a previsão", () => {
  selecionarLocalidade();
  cartaoDePrevisao().find("[data-cy=forecast-submit]").click();
  cy.wait("@forecast").its("request.url").should("contain", `location=${LOCALIDADE.slug}`);
});

Then("o sistema exibe a temperatura ambiente prevista", () => {
  cartaoDePrevisao()
    .find("[data-cy=forecast-result]")
    .should("contain.text", "Máx. 31,2 °C")
    .and("contain.text", "Mín. 23,5 °C")
    .and("contain.text", "não é a temperatura medida da carga");
});

Then("identifica a localidade e o período de referência", () => {
  cartaoDePrevisao()
    .find("[data-cy=forecast-result]")
    .should("contain.text", LOCALIDADE.name)
    .and("contain.text", "hoje, 10/11/2026");
});

// Cenário: falha na consulta à Open-Meteo (CT-09)
Given("que solicito uma previsão meteorológica", () => {
  selecionarLocalidade();
});

Given("a Open-Meteo não responde ou retorna erro", () => {
  cy.intercept("GET", "**/api/weather/forecast/**", {
    statusCode: 503,
    body: {
      detail: "Previsão indisponível no momento. O cadastro e a comparação manual continuam disponíveis.",
    },
  }).as("forecastFailure");
});

When("o sistema tenta consultar os dados", () => {
  cartaoDePrevisao().find("[data-cy=forecast-submit]").click();
  cy.wait("@forecastFailure").its("response.statusCode").should("eq", 503);
});

Then("informa que a previsão está indisponível", () => {
  cartaoDePrevisao()
    .find("[data-cy=forecast-error]")
    .should("contain.text", "Previsão indisponível no momento");
  cartaoDePrevisao().find("[data-cy=forecast-result]").should("not.exist");
});

Then("mantém disponíveis os fluxos de cadastro e comparação manual", () => {
  cy.contains("button", "Cadastrar entrega").should("be.enabled");
  cy.get("@qaDelivery").then((delivery: any) => {
    cy.get(`[data-cy=route-alternatives-${delivery.id}]`)
      .find("[data-cy=route-submit]")
      .should("be.enabled");
  });
});

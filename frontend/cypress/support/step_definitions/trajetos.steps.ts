// US-06 (FT-46) — Cadastro de alternativas de trajeto (CT-18 e CT-07).
// US-07 (FT-56) — Comparação de duas alternativas (CT-06 e CT-19).
import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";

function cartaoDaEntrega(): Cypress.Chainable<JQuery<HTMLElement>> {
  return cy.get("@qaDelivery").then((delivery: any) =>
    cy.get(`[data-cy=route-alternatives-${delivery.id}]`),
  );
}

function preencherAlternativa(distancia: string, duracao: string): void {
  cartaoDaEntrega().within(() => {
    cy.get("[data-cy=route-distance]").clear();
    if (distancia) cy.get("[data-cy=route-distance]").type(distancia);
    cy.get("[data-cy=route-duration]").clear();
    if (duracao) cy.get("[data-cy=route-duration]").type(duracao);
  });
}

function enviarAlternativa(alias: string): void {
  cy.intercept("POST", "**/route-alternatives/").as(alias);
  cartaoDaEntrega().within(() => {
    cy.get("[data-cy=route-submit]").click();
  });
}

function cadastrarAlternativaPelaInterface(distancia: string, duracao: string): void {
  preencherAlternativa(distancia, duracao);
  enviarAlternativa("createRouteAlternative");
  cy.wait("@createRouteAlternative").its("response.statusCode").should("eq", 201);
}

function tokenDaSessao(): Cypress.Chainable<string> {
  return cy.window().then((win) => {
    const raw = win.sessionStorage.getItem("feneme-session");
    expect(raw, "sessão do Gestor").to.be.a("string");
    return JSON.parse(raw as string).access as string;
  });
}

// Cenário: Cadastrar até duas alternativas válidas
Given("que ainda há espaço para cadastrar alternativas nessa entrega", () => {
  cartaoDaEntrega().find("[data-cy=route-alternatives-count]").should("have.text", "0/2");
});

When("informo até duas alternativas com distância e duração válidas", () => {
  cadastrarAlternativaPelaInterface("125,5", "110");
  preencherAlternativa("140", "95");
});

When("confirmo o cadastro", () => {
  enviarAlternativa("confirmRouteAlternative");
});

Then("o sistema salva as alternativas", () => {
  cy.wait("@confirmRouteAlternative").its("response.statusCode").should("eq", 201);
  cartaoDaEntrega().within(() => {
    cy.get("[data-cy=route-alternatives-count]").should("have.text", "2/2");
    cy.get("[data-cy=route-alternative-item]").should("have.length", 2);
    cy.contains("[data-cy=route-alternative-item]", "125,5 km").should("contain.text", "1 h 50 min");
    cy.contains("[data-cy=route-alternative-item]", "140 km").should("contain.text", "1 h 35 min");
  });
});

Then("associa os dados à entrega", () => {
  cy.get("@qaDelivery").then((delivery: any) => {
    tokenDaSessao().then((token) => {
      cy.request({
        url: `/api/deliveries/${delivery.id}/route-alternatives/`,
        headers: { Authorization: `Bearer ${token}` },
      }).then(({ body }) => {
        expect(body).to.have.length(2);
        expect(body.every((item: { delivery: number }) => item.delivery === delivery.id)).to.eq(true);
      });
    });
  });
});

// Cenário: Impedir cadastro de uma terceira alternativa
Given("que a entrega já possui duas alternativas cadastradas", () => {
  cadastrarAlternativaPelaInterface("100", "90");
  cadastrarAlternativaPelaInterface("120", "80");
});

When("tento registrar uma terceira alternativa", () => {
  // A interface oculta o formulário no limite; a tentativa é feita direto na API.
  cy.get("@qaDelivery").then((delivery: any) => {
    tokenDaSessao().then((token) => {
      cy.request({
        method: "POST",
        url: `/api/deliveries/${delivery.id}/route-alternatives/`,
        headers: { Authorization: `Bearer ${token}` },
        body: { distance_km: 130, duration_minutes: 70 },
        failOnStatusCode: false,
      }).as("thirdAlternative");
    });
  });
});

Then("o sistema impede o registro", () => {
  cy.get("@thirdAlternative").its("status").should("eq", 400);
  cartaoDaEntrega().within(() => {
    cy.get("[data-cy=route-submit]").should("not.exist");
    cy.get("[data-cy=route-alternative-item]").should("have.length", 2);
  });
});

Then("informa que o limite é de duas alternativas", () => {
  cy.get("@thirdAlternative").its("body.detail").should("contain", "limite é de 2 alternativas");
  cartaoDaEntrega().find("[data-cy=route-alternatives-limit]").should("contain.text", "Limite de 2 alternativas");
});

// Cenário: Rejeitar distância ou duração inválida
Given("que estou preenchendo os dados de uma alternativa de trajeto", () => {
  cartaoDaEntrega().find("[data-cy=route-distance]").should("be.visible");
});

When("informo uma distância ou duração inválida", () => {
  preencherAlternativa("0", "90");
  enviarAlternativa("invalidRouteAlternative");
});

Then("o sistema rejeita o registro", () => {
  cy.wait("@invalidRouteAlternative").its("response.statusCode").should("eq", 400);
  cartaoDaEntrega().find("[data-cy=route-alternatives-count]").should("have.text", "0/2");
});

Then("identifica o valor que deve ser corrigido", () => {
  cartaoDaEntrega().find("[data-cy=route-error]").should("contain.text", "distância");
});


// Cenário US-07: comparar duas alternativas cadastradas
Given("que a entrega possui duas alternativas cadastradas", () => {
  cadastrarAlternativaPelaInterface("125,5", "110");
  cadastrarAlternativaPelaInterface("140", "95");
  cartaoDaEntrega().find("[data-cy=route-alternatives-count]").should("have.text", "2/2");
});

When("solicito a comparação", () => {
  cartaoDaEntrega().find("[data-cy=route-compare-button]").click();
});

Then("o sistema exibe as duas alternativas lado a lado", () => {
  cartaoDaEntrega().find("[data-cy=route-comparison-panel]").should("be.visible");
  cartaoDaEntrega().find("[data-cy=route-comparison-item]").should("have.length", 2);
});

Then("apresenta a distância e o tempo informados para cada uma", () => {
  cartaoDaEntrega().find("[data-cy=route-comparison-item]").eq(0)
    .should("contain.text", "125,5 km")
    .and("contain.text", "1 h 50 min");
  cartaoDaEntrega().find("[data-cy=route-comparison-item]").eq(1)
    .should("contain.text", "140 km")
    .and("contain.text", "1 h 35 min");
});

// Cenário US-07: não comparar quando há menos de duas alternativas
Given("que a entrega possui menos de duas alternativas cadastradas", () => {
  cadastrarAlternativaPelaInterface("125,5", "110");
  cartaoDaEntrega().find("[data-cy=route-alternatives-count]").should("have.text", "1/2");
});

When("solicito a comparação de dois trajetos", () => {
  cartaoDaEntrega().find("[data-cy=route-compare-button]").click();
});

Then("o sistema informa que faltam alternativas", () => {
  cartaoDaEntrega().find("[data-cy=route-comparison-message]")
    .should("be.visible")
    .and("contain.text", "Cadastre duas alternativas para comparar");
});

Then("não apresenta uma comparação fictícia", () => {
  cartaoDaEntrega().find("[data-cy=route-comparison-panel]").should("not.exist");
});

Given("que a entrega não possui alternativas cadastradas", () => {
  cartaoDaEntrega().find("[data-cy=route-alternatives-count]").should("have.text", "0/2");
});

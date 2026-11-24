import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";
import { autenticarComoGestor, senhaE2E } from "../qa-helpers";

// Os testes criam entregas reais na base descartável E2E. Nenhum evento é simulado.
function prepararEntrega() {
  const identificador = "FT59-" + Date.now() + "-" + Cypress._.random(1000, 9999);
  return cy.request("POST", "/api/auth/login/", {
    username: "gestor_e2e", password: senhaE2E(),
  }).then(({ body: authGestor }) => {
    const managerToken = authGestor.access as string;
    return cy.request({
      method: "POST",
      url: "/api/deliveries/",
      headers: { Authorization: "Bearer " + managerToken },
      body: {
        origin: "Origem " + identificador,
        destination: "Destino " + identificador,
        cargo_description: "Carga de teste do histórico FT-59",
      },
    }).then(({ body: delivery }) => {
      const deliveryId = delivery.id as number;
      return cy.request({
        method: "GET",
        url: "/api/drivers/",
        headers: { Authorization: "Bearer " + managerToken },
      }).then(({ body: drivers }) => {
        const motorista = (drivers as Array<{ id: number; username: string }>)
          .find((item) => item.username === "motorista_e2e");
        expect(motorista, "Motorista fictício da base E2E").to.exist;
        return cy.request({
          method: "POST",
          url: "/api/deliveries/" + deliveryId + "/assign-driver/",
          headers: { Authorization: "Bearer " + managerToken },
          body: { driver_id: motorista!.id },
        }).then(() => {
          return cy.request("POST", "/api/auth/login/", {
            username: "motorista_e2e", password: senhaE2E(),
          }).then(({ body: authMotorista }) => {
            return { deliveryId, driverToken: authMotorista.access as string };
          });
        });
      });
    });
  });
}

function registrarTransicao(deliveryId: number, token: string, status: string) {
  return cy.request({
    method: "POST",
    url: "/api/deliveries/" + deliveryId + "/update-status/",
    headers: { Authorization: "Bearer " + token },
    body: { status },
  }).its("status").should("eq", 200);
}

function cardDaEntrega() {
  return cy.get<number>("@ft59DeliveryId").then((id) =>
    cy.contains(".delivery-id", new RegExp("^ENTREGA #" + id + "$"))
      .closest("article.delivery-card")
  );
}

function abrirHistorico() {
  cy.intercept("GET", "**/api/deliveries/*/status-history/").as("ft59History");
  return cardDaEntrega()
    .find("[data-cy=history-toggle]")
    .click()
    .then(() => cy.wait("@ft59History").its("response.statusCode").should("eq", 200));
}

Given("que criei uma entrega com duas alterações reais para consulta do histórico", () => {
  return prepararEntrega().then(({ deliveryId, driverToken }) => {
    cy.wrap(deliveryId).as("ft59DeliveryId");
    return registrarTransicao(deliveryId, driverToken, "EM_TRANSPORTE").then(() =>
      registrarTransicao(deliveryId, driverToken, "ENTREGUE")
    );
  });
});

Given("que criei uma entrega sem alterações para consulta do histórico", () => {
  return prepararEntrega().then(({ deliveryId }) => {
    cy.wrap(deliveryId).as("ft59DeliveryId");
  });
});

When("abro o histórico dessa entrega como Gestor", () => {
  autenticarComoGestor();
  return abrirHistorico();
});

Then("vejo as duas transições persistidas na ordem correta", () => {
  cardDaEntrega().find("[data-cy=history-entry]").should("have.length", 2)
    .first().should("contain.text", "Pendente → Em transporte")
    .and("contain.text", "motorista_e2e");
  cardDaEntrega().find("[data-cy=history-entry]").last()
    .should("contain.text", "Em transporte → Entregue")
    .and("contain.text", "motorista_e2e");
  cardDaEntrega().find("[data-cy=history-current-status]").should("contain.text", "Entregue");
  cardDaEntrega().find("[data-cy=history-entry]").each(($item) => {
    expect($item.text()).to.match(/\d{2}\/\d{2}\/\d{4}/);
  });
});

Then("vejo mensagem de histórico vazio e o status Pendente", () => {
  cardDaEntrega().find("[data-cy=history-empty]")
    .should("contain.text", "Ainda não há mudanças de status registradas");
  cardDaEntrega().find("[data-cy=history-current-status]")
    .should("contain.text", "Pendente");
  cardDaEntrega().find("[data-cy=history-entry]").should("not.exist");
});

When("consulto o histórico após sair e entrar novamente", () => {
  autenticarComoGestor();
  return abrirHistorico().then(() => {
    cardDaEntrega().find("[data-cy=history-entry]").should("have.length", 2);
    cy.contains("button", "Sair").click();
    cy.get("[data-cy=login-page]").should("be.visible");
    autenticarComoGestor();
    return abrirHistorico();
  });
});

Then("continuo vendo os eventos persistidos", () => {
  cardDaEntrega().find("[data-cy=history-entry]").should("have.length", 2);
  cardDaEntrega().find("[data-cy=history-entry]").first()
    .should("contain.text", "Pendente → Em transporte");
  cardDaEntrega().find("[data-cy=history-entry]").last()
    .should("contain.text", "Em transporte → Entregue");
  cardDaEntrega().find("[data-cy=history-current-status]").should("contain.text", "Entregue");
});

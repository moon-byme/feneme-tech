import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";
import {
  preencherEntregaUnica,
  salvarEntregaPelaInterface,
  senhaE2E,
} from "../qa-helpers";

Given("existe uma entrega cadastrada", () => {
  preencherEntregaUnica();
  salvarEntregaPelaInterface();
});

Given("existe um usuário válido com perfil Motorista", () => {
  cy.get("select").should("have.length.greaterThan", 0);
  cy.get("select").first().find("option").should(($options) => {
    expect([...$options].some((option) => option.textContent?.includes("motorista_e2e"))).to.eq(true);
  });
});

When("associo o Motorista à entrega", () => {
  cy.intercept("POST", "**/assign-driver/").as("assignDriver");
  cy.get("@qaOrigin").then((origin) => {
    cy.contains("article.delivery-card", String(origin)).within(() => {
      cy.get("select").find("option").then(($options) => {
        const option = [...$options].find((item) => item.textContent?.includes("motorista_e2e"));
        expect(option, "opção do Motorista de teste").to.exist;
        cy.get("select").select((option as HTMLOptionElement).value);
      });
      cy.contains("button", "Atribuir").click();
    });
  });
});

Then("o sistema salva a atribuição", () => {
  cy.wait("@assignDriver").then(({ response }) => {
    expect(response?.statusCode).to.eq(200);
    expect(response?.body?.assigned_driver_username).to.eq("motorista_e2e");
  });
  cy.get("@qaOrigin").then((origin) => {
    cy.contains("article.delivery-card", String(origin))
      .should("contain.text", "Motorista: motorista_e2e");
  });
});

Then("disponibiliza a entrega ao Motorista responsável", () => {
  cy.contains("button", "Sair").click();
  cy.clearAllSessionStorage();
  cy.visit("/");
  cy.get("[data-cy=login-username]").type("motorista_e2e");
  cy.get("[data-cy=login-password]").type(senhaE2E(), { log: false });
  cy.get("[data-cy=login-submit]").click();
  cy.get("[data-cy=role-chip]").should("have.text", "Motorista");
  cy.get("@qaOrigin").then((origin) => {
    cy.contains("article.delivery-card", String(origin)).should("be.visible");
  });
});

Given("existe um usuário que não possui perfil Motorista", () => {
  cy.request("POST", "/api/auth/login/", {
    username: "gestor_e2e",
    password: senhaE2E(),
  }).then(({ body }) => {
    cy.wrap(body.access).as("qaManagerToken");
    cy.wrap(body.user.id).as("qaNonDriverId");

    cy.request({
      method: "GET",
      url: "/api/drivers/",
      headers: { Authorization: `Bearer ${body.access}` },
    }).then((driversResponse) => {
      const driver = (driversResponse.body as Array<{ id: number; username: string }>)
        .find((item) => item.username === "motorista_e2e");
      expect(driver, "Motorista de teste").to.exist;
      cy.wrap((driver as { id: number }).id).as("qaPreviousDriverId");

      cy.get("@qaDelivery").then((delivery: any) => {
        cy.request({
          method: "POST",
          url: `/api/deliveries/${delivery.id}/assign-driver/`,
          headers: { Authorization: `Bearer ${body.access}` },
          body: { driver_id: (driver as { id: number }).id },
        }).its("status").should("eq", 200);
      });
    });
  });
});

When("tento atribuir a entrega a esse usuário", () => {
  cy.get("@qaDelivery").then((delivery: any) => {
    cy.get("@qaManagerToken").then((token) => {
      cy.get("@qaNonDriverId").then((nonDriverId) => {
        cy.request({
          method: "POST",
          url: `/api/deliveries/${delivery.id}/assign-driver/`,
          headers: { Authorization: `Bearer ${token}` },
          body: { driver_id: nonDriverId },
          failOnStatusCode: false,
        }).then((response) => {
          cy.wrap(response).as("qaRejectedAssignment");
        });
      });
    });
  });
});

Then("o sistema rejeita a atribuição", () => {
  cy.get("@qaRejectedAssignment").its("status").should("eq", 400);
});

Then("informa o motivo da rejeição", () => {
  cy.get("@qaRejectedAssignment").its("body.driver_id.0")
    .should("contain", "não possui perfil Motorista");
});

Then("mantém o responsável anteriormente registrado", () => {
  cy.get("@qaDelivery").then((delivery: any) => {
    cy.get("@qaManagerToken").then((token) => {
      cy.get("@qaPreviousDriverId").then((previousDriverId) => {
        cy.request({
          method: "GET",
          url: `/api/deliveries/${delivery.id}/`,
          headers: { Authorization: `Bearer ${token}` },
        }).its("body.assigned_driver").should("eq", previousDriverId);
      });
    });
  });
});

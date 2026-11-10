import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";
import { autenticarComoMotorista } from "../qa-helpers";

const senhaE2E = (): string => {
  const password = Cypress.env("E2E_PASSWORD") as string | undefined;
  if (!password) {
    throw new Error("Defina CYPRESS_E2E_PASSWORD com a senha das contas fictícias de teste.");
  }
  return password;
};

type Delivery = {
  id: number;
  origin: string;
  destination: string;
  cargo_description: string;
};

type Driver = {
  id: number;
  username: string;
};

function autenticarApi(username: string) {
  return cy.request("POST", "/api/auth/login/", {
    username,
    password: senhaE2E(),
  });
}

function criarEntregaParaMotorista(
  managerToken: string,
  driverUsername: string,
  marker: string,
) {
  return cy.request({
    method: "POST",
    url: "/api/deliveries/",
    headers: { Authorization: `Bearer ${managerToken}` },
    body: {
      origin: `Origem ${marker}`,
      destination: `Destino ${marker}`,
      cargo_description: `Carga privada ${marker}`,
    },
  }).then(({ body: delivery }: { body: Delivery }) => {
    return cy.request({
      method: "GET",
      url: "/api/drivers/",
      headers: { Authorization: `Bearer ${managerToken}` },
    }).then(({ body: drivers }: { body: Driver[] }) => {
      const driver = drivers.find((item) => item.username === driverUsername);
      expect(driver, `conta de teste ${driverUsername}`).to.exist;

      return cy.request({
        method: "POST",
        url: `/api/deliveries/${delivery.id}/assign-driver/`,
        headers: { Authorization: `Bearer ${managerToken}` },
        body: { driver_id: (driver as Driver).id },
      }).then(() => delivery);
    });
  });
}

Given("que estou autenticado como Motorista", () => {
  autenticarApi("gestor_e2e").then(({ body }) => {
    cy.wrap(body.access).as("qaManagerToken");
  });
  autenticarApi("motorista_e2e").then(({ body }) => {
    cy.wrap(body.access).as("qaDriverToken");
  });
});

Given("possuo entregas atribuídas", () => {
  cy.get("@qaManagerToken").then((managerToken) => {
    criarEntregaParaMotorista(
      managerToken as string,
      "motorista_e2e",
      `PROPRIA-${Date.now()}`,
    ).then((delivery) => cy.wrap(delivery).as("qaOwnDelivery"));

    criarEntregaParaMotorista(
      managerToken as string,
      "motorista_outro_e2e",
      `OUTRA-${Date.now()}`,
    ).then((delivery) => cy.wrap(delivery).as("qaOtherDelivery"));
  });
});

When("acesso a lista de minhas entregas", () => {
  cy.get("@qaDriverToken").then((token) => {
    cy.request({
      method: "GET",
      url: "/api/deliveries/",
      headers: { Authorization: `Bearer ${token}` },
    }).then(({ body }) => cy.wrap(body).as("qaDriverDeliveries"));
  });
});

When("acesso a área do Motorista pela interface", () => {
  autenticarComoMotorista();
});

Then("a interface mostra a entrega atribuída a mim", () => {
  cy.get("@qaOwnDelivery").then((own: Delivery) => {
    cy.contains("article.delivery-card", `ENTREGA #${own.id}`)
      .should("be.visible")
      .and("contain.text", own.origin)
      .and("contain.text", own.destination)
      .and("contain.text", own.cargo_description);
  });
});

Then("não mostra a entrega atribuída a outro Motorista", () => {
  cy.get("@qaOtherDelivery").then((other: Delivery) => {
    cy.get("article.delivery-card").should("not.contain.text", other.origin);
  });
});

Then("o sistema exibe somente as entregas sob minha responsabilidade", () => {
  cy.get("@qaOwnDelivery").then((own: Delivery) => {
    cy.get("@qaOtherDelivery").then((other: Delivery) => {
      cy.get("@qaDriverDeliveries").then((deliveries: Delivery[]) => {
        expect(deliveries.map((item) => item.id)).to.include(own.id);
        expect(deliveries.some((item) => item.id === other.id)).to.eq(false);
      });
    });
  });
});

Then("apresenta as informações essenciais de cada uma", () => {
  cy.get("@qaOwnDelivery").then((own: Delivery) => {
    cy.get("@qaDriverDeliveries").then((deliveries: Delivery[]) => {
      const delivery = deliveries.find((item) => item.id === own.id);
      expect(delivery).to.exist;
      expect(delivery?.origin).to.eq(own.origin);
      expect(delivery?.destination).to.eq(own.destination);
      expect(delivery?.cargo_description).to.eq(own.cargo_description);
    });
  });
});

Given("existe uma entrega atribuída a outro Motorista", () => {
  cy.get("@qaManagerToken").then((managerToken) => {
    criarEntregaParaMotorista(
      managerToken as string,
      "motorista_outro_e2e",
      `PRIVADA-${Date.now()}`,
    ).then((delivery) => cy.wrap(delivery).as("qaPrivateDelivery"));
  });
});

When("tento acessar diretamente essa entrega", () => {
  cy.get("@qaDriverToken").then((token) => {
    cy.get("@qaPrivateDelivery").then((delivery: Delivery) => {
      cy.request({
        method: "GET",
        url: `/api/deliveries/${delivery.id}/`,
        headers: { Authorization: `Bearer ${token}` },
        failOnStatusCode: false,
      }).then((response) => cy.wrap(response).as("qaPrivateDeliveryResponse"));
    });
  });
});

Then("a API nega o acesso", () => {
  cy.get("@qaPrivateDeliveryResponse").its("status").should("eq", 404);
});

Then("não expõe os dados dessa entrega", () => {
  cy.get("@qaPrivateDelivery").then((delivery: Delivery) => {
    cy.get("@qaPrivateDeliveryResponse").then((response: any) => {
      const body = JSON.stringify(response.body);
      expect(body).not.to.include(delivery.origin);
      expect(body).not.to.include(delivery.destination);
      expect(body).not.to.include(delivery.cargo_description);
    });
  });
});

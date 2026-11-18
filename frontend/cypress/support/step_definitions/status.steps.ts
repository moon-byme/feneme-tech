import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";
import { autenticarComoGestor, autenticarComoMotorista } from "../qa-helpers";

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
  status: string;
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
  cy.get<string>("@qaManagerToken").then((managerToken) => {
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
  cy.get<string>("@qaDriverToken").then((token) => {
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
  cy.get<Delivery>("@qaOwnDelivery").then((own: Delivery) => {
    cy.contains(".delivery-id", new RegExp(`^ENTREGA #${own.id}$`))
      .closest("article.delivery-card")
      .should("be.visible")
      .and("contain.text", own.origin)
      .and("contain.text", own.destination)
      .and("contain.text", own.cargo_description)
      .find(".status-chip")
      .should("have.text", own.status === "PENDENTE" ? "Pendente" : own.status);
  });
});

Given("a consulta de minhas entregas retorna uma lista vazia", () => {
  // Verificação do estado visual; a resposta real [] já é coberta no Django.
  cy.intercept("GET", "**/api/deliveries/", { statusCode: 200, body: [] })
    .as("qaEmptyDeliveries");
});

Then("a interface informa que não há entregas atribuídas", () => {
  cy.wait("@qaEmptyDeliveries").its("response.body").should("deep.eq", []);
  cy.contains("strong", "Nenhuma entrega atribuída").should("be.visible");
  cy.get("article.delivery-card").should("not.exist");
  cy.get(".count-badge").should("have.text", "0");
});

When("o Gestor reatribui minha entrega a outro Motorista", () => {
  cy.get<string>("@qaManagerToken").then((managerToken) => {
    cy.request({
      method: "GET",
      url: "/api/drivers/",
      headers: { Authorization: `Bearer ${managerToken}` },
    }).then(({ body: drivers }: { body: Driver[] }) => {
      const other = drivers.find((driver) => driver.username === "motorista_outro_e2e");
      expect(other, "segundo Motorista fictício").to.exist;
      cy.get<Delivery>("@qaOwnDelivery").then((own: Delivery) => {
        cy.request({
          method: "POST",
          url: `/api/deliveries/${own.id}/assign-driver/`,
          headers: { Authorization: `Bearer ${managerToken}` },
          body: { driver_id: (other as Driver).id },
        }).its("body.assigned_driver").should("eq", (other as Driver).id);
      });
    });
  });
});

When("atualizo a lista pela interface", () => {
  cy.intercept("GET", "**/api/deliveries/").as("qaRefreshedDeliveries");
  cy.contains("button", "Atualizar").should("be.enabled").click();
  cy.wait("@qaRefreshedDeliveries").its("response.statusCode").should("eq", 200);
});

Then("a interface deixa de mostrar a entrega reatribuída", () => {
  cy.get<Delivery>("@qaOwnDelivery").then((own: Delivery) => {
    cy.contains(".delivery-id", new RegExp(`^ENTREGA #${own.id}$`)).should("not.exist");
    cy.get("main").should("not.contain.text", own.origin);
  });
});

Then("não mostra a entrega atribuída a outro Motorista", () => {
  cy.get<Delivery>("@qaOtherDelivery").then((other: Delivery) => {
    cy.get("article.delivery-card").should("not.contain.text", other.origin);
  });
});

Then("o sistema exibe somente as entregas sob minha responsabilidade", () => {
  cy.get<Delivery>("@qaOwnDelivery").then((own: Delivery) => {
    cy.get<Delivery>("@qaOtherDelivery").then((other: Delivery) => {
      cy.get<Delivery[]>("@qaDriverDeliveries").then((deliveries: Delivery[]) => {
        expect(deliveries.map((item) => item.id)).to.include(own.id);
        expect(deliveries.some((item) => item.id === other.id)).to.eq(false);
      });
    });
  });
});

Then("apresenta as informações essenciais de cada uma", () => {
  cy.get<Delivery>("@qaOwnDelivery").then((own: Delivery) => {
    cy.get<Delivery[]>("@qaDriverDeliveries").then((deliveries: Delivery[]) => {
      const delivery = deliveries.find((item) => item.id === own.id);
      expect(delivery).to.exist;
      expect(delivery?.origin).to.eq(own.origin);
      expect(delivery?.destination).to.eq(own.destination);
      expect(delivery?.cargo_description).to.eq(own.cargo_description);
      expect(delivery?.status).to.eq(own.status);
    });
  });
});

Given("existe uma entrega atribuída a outro Motorista", () => {
  cy.get<string>("@qaManagerToken").then((managerToken) => {
    criarEntregaParaMotorista(
      managerToken as string,
      "motorista_outro_e2e",
      `PRIVADA-${Date.now()}`,
    ).then((delivery) => cy.wrap(delivery).as("qaPrivateDelivery"));
  });
});

When("tento acessar diretamente essa entrega", () => {
  cy.get<string>("@qaDriverToken").then((token) => {
    cy.get<Delivery>("@qaPrivateDelivery").then((delivery: Delivery) => {
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
  cy.get<Delivery>("@qaPrivateDelivery").then((delivery: Delivery) => {
    cy.get("@qaPrivateDeliveryResponse").then((response: any) => {
      const body = JSON.stringify(response.body);
      expect(body).not.to.include(delivery.origin);
      expect(body).not.to.include(delivery.destination);
      expect(body).not.to.include(delivery.cargo_description);
    });
  });
});

function ownCard() {
  return cy.get<Delivery>("@qaOwnDelivery").then((own) =>
    cy.contains(".delivery-id", new RegExp(`^ENTREGA #${own.id}$`)).closest("article.delivery-card"),
  );
}

When("inicio o transporte da minha entrega", () => {
  cy.get<Delivery>("@qaOwnDelivery").then((own) => {
    cy.intercept("POST", `**/api/deliveries/${own.id}/update-status/`).as("qaUpdateStatus");
    ownCard().find("[data-cy=update-status]").should("have.text", "Iniciar transporte").click();
    cy.wait("@qaUpdateStatus").then(({ request, response }) => {
      expect(request.body).to.deep.eq({ status: "EM_TRANSPORTE" });
      expect(response?.statusCode).to.eq(200);
    });
    ownCard().find("[role=status]").should("contain.text", "Status atualizado para Em transporte.");
  });
});

When("confirmo a conclusão da minha entrega", () => {
  ownCard().contains("button", "Confirmar entrega").click();
  cy.wait("@qaUpdateStatus").then(({ request, response }) => {
    expect(request.body).to.deep.eq({ status: "ENTREGUE" });
    expect(response?.statusCode).to.eq(200);
  });
  ownCard().find("[role=status]").should("contain.text", "Status atualizado para Entregue.");
});

Then("minha entrega mostra o status {string}", (label: string) => {
  ownCard().find(".status-chip").should("have.text", label);
});

Then("o controle da minha entrega está finalizado", () => {
  ownCard().find("[data-cy=update-status]").should("be.disabled").and("have.text", "Entrega finalizada");
});

Then("o status Entregue permanece após nova autenticação", () => {
  cy.contains("button", "Sair").click();
  autenticarComoMotorista();
  cy.reload();
  ownCard().find(".status-chip").should("have.text", "Entregue");
  ownCard().find("[data-cy=update-status]").should("be.disabled");
});

Then("o Gestor visualiza a entrega finalizada sem controles de alteração", () => {
  autenticarComoGestor();
  cy.reload();
  ownCard().find(".status-chip").should("have.text", "Entregue");
  cy.get("[data-cy=update-status]").should("not.exist");
});

When("tento alterar o status dessa entrega", () => {
  cy.get<string>("@qaDriverToken").then((token) => {
    cy.get<Delivery>("@qaPrivateDelivery").then((delivery) => {
      cy.request({
        method: "POST", url: `/api/deliveries/${delivery.id}/update-status/`,
        headers: { Authorization: `Bearer ${token}` }, body: { status: "EM_TRANSPORTE" },
        failOnStatusCode: false,
      }).as("qaDeniedUpdate");
    });
  });
});

Then("o sistema nega a operação", () => {
  cy.get<Cypress.Response<unknown>>("@qaDeniedUpdate").its("status").should("eq", 404);
});

Then("preserva o status original consultado pelo Gestor", () => {
  cy.get<string>("@qaManagerToken").then((token) => {
    cy.get<Delivery>("@qaPrivateDelivery").then((delivery) => {
      cy.request({ url: `/api/deliveries/${delivery.id}/`, headers: { Authorization: `Bearer ${token}` } })
        .its("body.status").should("eq", "PENDENTE");
    });
  });
});

When("a API rejeita temporariamente a alteração da minha entrega", () => {
  cy.get<Delivery>("@qaOwnDelivery").then((delivery) => {
    cy.intercept({ method: "POST", url: `**/api/deliveries/${delivery.id}/update-status/`, times: 1 }, {
      statusCode: 400, body: { status: ["Falha temporária no teste. Tente novamente."] },
      delay: 1200,
    }).as("qaFailedStatus");
    ownCard().find("[data-cy=update-status]").click();
  });
});

Then("vejo o carregamento sem antecipar o novo status", () => {
  ownCard().find("[data-cy=update-status]").should("be.disabled").and("have.text", "Salvando status...");
  ownCard().find(".status-chip").should("have.text", "Pendente");
  cy.contains("button", "Atualizar").should("be.disabled");
});

Then("vejo a mensagem de erro da atualização", () => {
  cy.wait("@qaFailedStatus");
  ownCard().find("[role=alert]").should("contain.text", "Falha temporária no teste. Tente novamente.");
  ownCard().find("[data-cy=update-status]").should("be.enabled");
});

When("a sessão expira ao iniciar o transporte", () => {
  cy.get<Delivery>("@qaOwnDelivery").then((delivery) => {
    cy.intercept("POST", `**/api/deliveries/${delivery.id}/update-status/`, {
      statusCode: 401, body: { detail: "Token expirado." },
    });
    ownCard().find("[data-cy=update-status]").click();
  });
});

Then("volto ao login com mensagem de sessão expirada", () => {
  cy.get("[data-cy=login-page]").should("be.visible");
  cy.get("[data-cy=login-error]").should("contain.text", "Sua sessão expirou. Entre novamente.");
});

When("outra sessão inicia o transporte pela API", () => {
  cy.get<string>("@qaDriverToken").then((token) => {
    cy.get<Delivery>("@qaOwnDelivery").then((delivery) => {
      cy.request({
        method: "POST", url: `/api/deliveries/${delivery.id}/update-status/`,
        headers: { Authorization: `Bearer ${token}` }, body: { status: "EM_TRANSPORTE" },
      }).its("status").should("eq", 200);
    });
  });
});

When("tento iniciar novamente pela interface", () => {
  ownCard().find("[data-cy=update-status]").click();
});

Then("vejo a mensagem de transição não permitida", () => {
  ownCard().find("[role=alert]").should("contain.text", "Transição não permitida");
});

import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";
import { autenticarComoGestor, autenticarComoMotorista, cidadesDeTeste, senhaE2E } from "../qa-helpers";

type Delivery = {
  id: number;
  origin: string;
  destination: string;
  cargo_description: string;
  status: "PENDENTE" | "EM_TRANSPORTE" | "ENTREGUE";
  assigned_driver_username?: string | null;
};

type Driver = {
  id: number;
  username: string;
};

function autenticarApi(username: string) {
  return cy.request({
    method: "POST",
    url: "/api/auth/login/",
    body: { username, password: senhaE2E() },
    log: false,
  });
}

function criarEntregaParaMotorista(
  managerToken: string,
  driverUsername: string,
  marker: string,
) {
  return cidadesDeTeste(managerToken).then((cidades) => cy.request({
    method: "POST",
    url: "/api/deliveries/",
    headers: { Authorization: `Bearer ${managerToken}` },
    body: {
      ...cidades,
      cargo_description: `Carga privada ${marker}`,
    },
  })).then(({ body: delivery }: { body: Delivery }) => {
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

function atualizarStatusComoMotorista(
  token: string,
  delivery: Delivery,
  status: Delivery["status"],
) {
  return cy.request({
    method: "POST",
    url: `/api/deliveries/${delivery.id}/update-status/`,
    headers: { Authorization: `Bearer ${token}` },
    body: { status },
  }).then((response) => {
    expect(response.status).to.eq(200);
    expect(response.body.status).to.eq(status);
  });
}

function cardDoGestor(delivery: Delivery) {
  return cy.contains(".delivery-id", new RegExp(`^ENTREGA #${delivery.id}$`))
    .closest("article.delivery-card");
}

Given("que o Gestor está autenticado para consultar entregas", () => {
  autenticarApi("gestor_e2e").then(({ body }) => {
    cy.wrap(body.access).as("qaManagerToken");
  });
  autenticarApi("motorista_e2e").then(({ body }) => {
    cy.wrap(body.access).as("qaDriverToken");
  });
});

Given("que estou autenticado como Motorista", () => {
  autenticarApi("gestor_e2e").then(({ body }) => {
    cy.wrap(body.access).as("qaManagerToken");
  });
  autenticarApi("motorista_e2e").then(({ body }) => {
    cy.wrap(body.access).as("qaDriverToken");
  });
});

Given("existem entregas com status atualizados pelos Motoristas", () => {
  const marker = `US12-${Date.now()}`;
  cy.get<string>("@qaManagerToken").then((managerToken) => {
    return criarEntregaParaMotorista(managerToken, "motorista_e2e", `${marker}-PENDENTE`)
      .then((delivery) => {
        cy.wrap(delivery).as("qaPendingDelivery");
        return criarEntregaParaMotorista(managerToken, "motorista_e2e", `${marker}-TRANSPORTE`);
      })
      .then((delivery) => {
        cy.wrap(delivery).as("qaTransitDelivery");
        return criarEntregaParaMotorista(managerToken, "motorista_e2e", `${marker}-ENTREGUE`);
      })
      .then((delivery) => cy.wrap(delivery).as("qaDeliveredDelivery"));
  }).then(() => {
    return cy.get<string>("@qaDriverToken").then((driverToken) => {
      return cy.get<Delivery>("@qaTransitDelivery").then((delivery) => {
        return atualizarStatusComoMotorista(driverToken, delivery, "EM_TRANSPORTE");
      }).then(() => {
        return cy.get<Delivery>("@qaDeliveredDelivery").then((delivery) => {
          return atualizarStatusComoMotorista(driverToken, delivery, "EM_TRANSPORTE")
            .then(() => atualizarStatusComoMotorista(driverToken, delivery, "ENTREGUE"));
        });
      });
    });
  });
});

Given("existe outra entrega cadastrada", () => {
  cy.get<string>("@qaManagerToken").then((managerToken) => {
    return criarEntregaParaMotorista(
      managerToken,
      "motorista_e2e",
      `NAO-VAZAR-${Date.now()}`,
    ).then((delivery) => cy.wrap(delivery).as("qaExistingDelivery"));
  });
});

When("acesso o acompanhamento das entregas", () => {
  cy.intercept("GET", "**/api/deliveries/").as("qaManagerTracking");
  autenticarComoGestor();
  cy.wait("@qaManagerTracking").its("response.statusCode").should("eq", 200);
});

Then("o sistema exibe o status atual de cada entrega", () => {
  cy.get<Delivery>("@qaPendingDelivery").then((delivery) => {
    cardDoGestor(delivery)
      .should("be.visible")
      .and("contain.text", delivery.origin)
      .and("contain.text", delivery.destination)
      .and("contain.text", "Motorista responsável: motorista_e2e")
      .find(".status-chip")
      .should("have.text", "Pendente");
  });
  cy.get<Delivery>("@qaTransitDelivery").then((delivery) => {
    cardDoGestor(delivery).find(".status-chip").should("have.text", "Em transporte");
  });
  cy.get<Delivery>("@qaDeliveredDelivery").then((delivery) => {
    cardDoGestor(delivery).find(".status-chip").should("have.text", "Entregue");
  });
  cy.get("[data-cy=update-status]").should("not.exist");
});

Then("apresenta as atualizações persistidas pelos Motoristas", () => {
  cy.get<string>("@qaDriverToken").then((driverToken) => {
    return cy.get<Delivery>("@qaPendingDelivery").then((delivery) => {
      return atualizarStatusComoMotorista(driverToken, delivery, "EM_TRANSPORTE");
    });
  }).then(() => {
    cy.intercept("GET", "**/api/deliveries/").as("qaManagerRefresh");
    cy.contains("button", "Atualizar").should("be.enabled").click();
    return cy.wait("@qaManagerRefresh").then(({ response }) => {
      expect(response?.statusCode).to.eq(200);
      cy.get<Delivery>("@qaPendingDelivery").then((delivery) => {
        const refreshed = (response?.body as Delivery[]).find((item) => item.id === delivery.id);
        expect(refreshed?.status).to.eq("EM_TRANSPORTE");
        cardDoGestor(delivery).find(".status-chip").should("have.text", "Em transporte");
      });
    });
  }).then(() => {
    cy.contains("button", "Sair").click();
    cy.intercept("GET", "**/api/deliveries/").as("qaManagerNewSession");
    autenticarComoGestor();
    return cy.wait("@qaManagerNewSession").its("response.statusCode").should("eq", 200);
  }).then(() => {
    cy.get<Delivery>("@qaPendingDelivery").then((delivery) => {
      cardDoGestor(delivery).find(".status-chip").should("have.text", "Em transporte");
    });
  });
});

When("tento consultar o andamento de uma entrega inexistente", () => {
  cy.get<string>("@qaManagerToken").then((token) => {
    cy.request({
      method: "GET",
      url: "/api/deliveries/9000000000000000/",
      headers: { Authorization: `Bearer ${token}` },
      failOnStatusCode: false,
    }).as("qaMissingDeliveryResponse");
  });
});

Then("o sistema informa que o registro não foi encontrado", () => {
  cy.get<Cypress.Response<unknown>>("@qaMissingDeliveryResponse")
    .its("status").should("eq", 404);
});

Then("não apresenta dados de outra entrega", () => {
  cy.get<Delivery>("@qaExistingDelivery").then((delivery) => {
    cy.get<Cypress.Response<unknown>>("@qaMissingDeliveryResponse").then((response) => {
      const body = JSON.stringify(response.body);
      expect(body).not.to.include(delivery.origin);
      expect(body).not.to.include(delivery.destination);
      expect(body).not.to.include(delivery.cargo_description);
    });
  });
});

When("a consulta do acompanhamento falha", () => {
  cy.intercept("GET", "**/api/deliveries/", {
    statusCode: 503,
    body: { detail: "Consulta indisponível no teste." },
  }).as("qaManagerTrackingFailure");
  autenticarComoGestor();
  cy.wait("@qaManagerTrackingFailure").its("response.statusCode").should("eq", 503);
});

Then("a interface informa a falha sem indicar lista vazia", () => {
  cy.get("[role=alert]").should("contain.text", "Consulta indisponível no teste.");
  cy.contains("strong", "Nenhuma entrega cadastrada").should("not.exist");
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
    cy.get("main").should("not.contain.text", own.cargo_description);
  });
});

Then("não mostra a entrega atribuída a outro Motorista", () => {
  cy.get<Delivery>("@qaOtherDelivery").then((other: Delivery) => {
    cy.get("article.delivery-card").should("not.contain.text", other.cargo_description);
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

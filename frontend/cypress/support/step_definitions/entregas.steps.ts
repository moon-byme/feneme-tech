import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";
import {
  autenticarComoGestor,
  preencherEntregaUnica,
  salvarEntregaPelaInterface,
} from "../qa-helpers";

Given("que estou autenticado como Gestor", () => {
  autenticarComoGestor();
});

Given("preenchi os campos obrigatórios aprovados para uma entrega", () => {
  preencherEntregaUnica();
});

When("confirmo o cadastro da entrega", () => {
  salvarEntregaPelaInterface();
});

Then("o sistema registra a entrega", () => {
  cy.get("@qaDelivery").its("id").should("be.a", "number");
});

Then("gera uma identificação para ela", () => {
  cy.get("@qaDelivery").then((delivery: any) => {
    cy.contains("article.delivery-card", `ENTREGA #${delivery.id}`).should("be.visible");
  });
});

Then("permite recuperar as informações salvas", () => {
  cy.get("@qaDelivery").then((delivery: any) => {
    cy.contains("article.delivery-card", delivery.origin).within(() => {
      cy.contains("strong", delivery.destination).should("be.visible");
      cy.contains("p", delivery.cargo_description).should("be.visible");
    });
  });
});

Given("estou preenchendo o formulário de cadastro de entrega", () => {
  preencherEntregaUnica();
});

When("tento salvar sem preencher um campo obrigatório", () => {
  cy.intercept("POST", "**/api/deliveries/").as("invalidCreateDelivery");
  cy.contains("label", "Origem").find("input").clear();
  cy.contains("button", "Cadastrar entrega").click();
});

Then("o sistema impede o cadastro", () => {
  cy.contains("label", "Origem").find("input").should(($input) => {
    const input = $input[0] as HTMLInputElement;
    expect(input.validity.valueMissing).to.eq(true);
    expect(input.validity.valid).to.eq(false);
  });
  cy.get("@invalidCreateDelivery.all").should("have.length", 0);
});

Then("indica os dados que precisam de correção", () => {
  cy.contains("label", "Origem").find("input").should(($input) => {
    const input = $input[0] as HTMLInputElement;
    expect(input.validationMessage).not.to.be.empty;
  });
  cy.contains("Entrega cadastrada com sucesso").should("not.exist");
});

Given("existem entregas cadastradas", () => {
  preencherEntregaUnica();
  salvarEntregaPelaInterface();
});

When("acesso a consulta de entregas", () => {
  cy.intercept("GET", "**/api/deliveries/").as("listDeliveries");
  cy.contains("button", "Atualizar").click();
  cy.wait("@listDeliveries").its("response.statusCode").should("eq", 200);
});

Then("o sistema lista as entregas registradas", () => {
  cy.get("@qaOrigin").then((origin) => {
    cy.contains("article.delivery-card", String(origin)).should("be.visible");
  });
});

Then("permite consultar os dados essenciais de cada uma", () => {
  cy.get("@qaDelivery").then((delivery: any) => {
    cy.contains("article.delivery-card", delivery.origin).within(() => {
      cy.contains("strong", delivery.destination).should("be.visible");
      cy.contains("p", delivery.cargo_description).should("be.visible");
    });
  });
});

Given("não existem entregas cadastradas", () => {
  // Isola o estado vazio da interface. O comportamento real da API sem registros
  // também é coberto pelo teste backend CT-16.
  cy.intercept("GET", "**/api/deliveries/", {
    statusCode: 200,
    body: [],
  }).as("emptyDeliveryList");
});

When("acesso a lista de entregas", () => {
  cy.contains("button", "Atualizar").click();
  cy.wait("@emptyDeliveryList").its("response.body").should("deep.equal", []);
});

Then("o sistema informa que não há entregas para exibir", () => {
  cy.contains("strong", "Nenhuma entrega cadastrada").should("be.visible");
});

Then("não apresenta registros fictícios", () => {
  cy.get("article.delivery-card").should("not.exist");
  cy.get(".count-badge").should("have.text", "0");
});

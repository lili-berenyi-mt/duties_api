describe("Index page should exist", () => {
  it("Loads the index page", () => {
    cy.visit("/");
    cy.contains("Duties");
    cy.contains("Add Duty");
  });
});

describe("Should be able to add a duty", () => {
  it("Adds the duty", () => {
    cy.visit("/");
    cy.get("input[name='number']").type("1");
    cy.get("textarea[name='description']").type("Test duty");
    cy.get("button[type='submit']").click();

    cy.url().should("eq", Cypress.config().baseUrl + "/");
    cy.contains("D1: Test duty");
  });
});

describe("Should be able to add multiple duties", () => {
  it("Displays error message when adding duplicate duty", () => {
    cy.visit("/");
    cy.get("input[name='number']").type("2");
    cy.get("textarea[name='description']").type("Test duty 2");
    cy.get("button[type='submit']").click();

    cy.get("input[name='number']").type("3");
    cy.get("textarea[name='description']").type("Test duty 3");
    cy.get("button[type='submit']").click();

    cy.url().should("eq", Cypress.config().baseUrl + "/");
    cy.contains("D2: Test duty 2");
    cy.contains("D3: Test duty 3");
  });
});

describe("Shouldn't be able to add duplicate duty", () => {
  it("Displays error message when adding duplicate duty", () => {
    cy.visit("/");
    cy.get("input[name='number']").type("4");
    cy.get("textarea[name='description']").type("Test duty 4");
    cy.get("button[type='submit']").click();

    cy.get("input[name='number']").type("4");
    cy.get("textarea[name='description']").type("Test duty 5");
    cy.get("button[type='submit']").click();

    cy.url().should("eq", Cypress.config().baseUrl + "/");
    cy.contains("Duty already exists");
  });
});

describe("Shouldn't be able to add duty with empty description", () => {
  it("Displays error message when adding duty with empty description", () => {
    cy.visit("/");
    cy.get("input[name='number']").type("5");
    cy.get("button[type='submit']").click();

    cy.url().should("eq", Cypress.config().baseUrl + "/");
    cy.contains("Error: Description cannot be empty");
  });
});

describe("Shouldn't be able to add a duplicate duty with empty description", () => {
  it("Displays correct error message when addingduplicate duty with empty description", () => {
    cy.visit("/");
    cy.get("input[name='number']").type("6");
    cy.get("textarea[name='description']").type("Test duty 6");
    cy.get("button[type='submit']").click();

    cy.get("input[name='number']").type("6");
    cy.get("button[type='submit']").click();

    cy.url().should("eq", Cypress.config().baseUrl + "/");
    cy.contains("Error: Description cannot be empty");
  });
});

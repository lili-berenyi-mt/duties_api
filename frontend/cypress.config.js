const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    baseUrl: "http://localhost:5001",
    allowCypressEnv: false,
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});

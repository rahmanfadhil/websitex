import { initializePlugins } from "./plugins";

/**
 * Handle when a page loaded.
 */
document.addEventListener("turbo:load", function (event) {
  initializePlugins();
});

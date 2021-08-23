import dialogPolyfill from "https://cdn.jsdelivr.net/npm/dialog-polyfill@0.5.6/dist/dialog-polyfill.esm.js";
import { Notyf } from "https://cdn.jsdelivr.net/npm/notyf@3.10.0/notyf.es.js";
import getPageData from "./utils/pageData.js";

// Currently, we are using the dialog polyfill to show the dialogs if the
// browser does not support the dialog API.
if (navigator.userAgent.indexOf("Chrome") == -1) {
  const stylesheet = document.createElement("link");
  stylesheet.setAttribute("rel", "stylesheet");
  stylesheet.setAttribute(
    "href",
    "https://cdn.jsdelivr.net/npm/dialog-polyfill@0.5.6/dist/dialog-polyfill.css"
  );
  stylesheet.setAttribute(
    "integrity",
    "sha256-hT0ET4tfm+7MyjeBepBgV2N5tOmsAVKcTWhH82jvoaA="
  );
  stylesheet.setAttribute("crossorigin", "anonymous");
  document.head.appendChild(stylesheet);

  for (const dialog of document.querySelectorAll("dialog")) {
    dialogPolyfill.registerDialog(dialog);
  }
}

for (const dialog of document.querySelectorAll("dialog")) {
  dialog
    .querySelector("[data-close-dialog]")
    .addEventListener("click", () => dialog.close());
}

for (const button of document.querySelectorAll("[data-open-dialog]")) {
  button.addEventListener("click", () => {
    document.querySelector(button.getAttribute("data-open-dialog")).showModal();
  });
}

// Load messages

const { messages } = getPageData();
if (messages.length) {
  const notyf = new Notyf({
    duration: 5000,
    dismissible: true,
    position: { y: "top", x: "right" },
    types: [
      { type: "warning", background: "#FFFF00" },
      { type: "info", background: "#0000FF" },
    ],
  });
  for (const message of messages) {
    notyf.open(message);
  }
}

// Mobile responsive navigation menu

const toggle = document.querySelector("#toggle");
const menu = document.querySelector("#menu");

toggle.addEventListener("click", function () {
  if (menu.classList.contains("open")) {
    this.setAttribute("aria-expanded", "false");
    menu.classList.remove("open");
  } else {
    menu.classList.add("open");
    this.setAttribute("aria-expanded", "true");
  }
});

// Toggle password visibility
// https://web.dev/sign-in-form-best-practices/#password-display

for (const button of document.querySelectorAll("[data-toggle-password]")) {
  const inputId = button.getAttribute("data-toggle-password");
  const passwordInput = document.getElementById(inputId);

  button.addEventListener("click", function () {
    if (passwordInput.type === "password") {
      passwordInput.type = "text";
      button.textContent = "Hide password";
      button.setAttribute("aria-label", "Hide password.");
    } else {
      passwordInput.type = "password";
      button.textContent = "Show password";
      button.setAttribute(
        "aria-label",
        "Show password as plain text. Warning: this will display your password on the screen."
      );
    }
  });
}

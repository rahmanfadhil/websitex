import getPageData from "./utils/pageData.js";
import "./plugins/sweetalert2.js";

const { messages } = getPageData();

// Load messages

if (messages.length) {
  const { Notyf } = await import("notyf");
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

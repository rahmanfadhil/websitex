import "./dialog";

import "@fontsource/commissioner/variable.css";
import "tailwindcss/dist/base.css";
import "../css/main.css";

// Toast messages

const toast = document.querySelector(".toast");

// Hide toast message if the close button is clicked
toast.querySelectorAll("button").forEach((element) => {
  element.addEventListener("click", () => {
    element.parentElement.remove();
  });
});

// Hide all toast messages after 5 seconds
setTimeout(() => {
  for (const element of toast.children) {
    element.classList.add("hidden");
  }
}, 5000);

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

// PWA
// https://developers.google.com/web/fundamentals/primers/service-workers

if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("/service-worker.js", { scope: "/" }).then(
      function (registration) {
        // Registration was successful
        console.log(
          "ServiceWorker registration successful with scope: ",
          registration.scope
        );
      },
      function (err) {
        // registration failed :(
        console.log("ServiceWorker registration failed: ", err);
      }
    );
  });
}

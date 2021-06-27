import "@fontsource/lexend";
import "@fontsource/lexend/500.css";
import "@fontsource/lexend/700.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import "../scss/main.scss";

import "bootstrap/js/dist/collapse"; // for responsive navbar menu
import "bootstrap/js/dist/dropdown"; // for dropdowns

import { showMessages } from "./plugins/notyf";

window.addEventListener("DOMContentLoaded", function () {
  // notyf
  showMessages();

  // trix
  if (document.querySelector("trix-editor")) {
    import("./plugins/trix").then(({ initialize }) => initialize());
  }

  // @yaireo/tagify
  if (document.querySelector("input.tagsinput")) {
    import("./plugins/tagify").then(({ initialize }) => initialize());
  }

  // imask
  if (document.querySelector("input.moneyinput")) {
    import("./plugins/imask").then(({ initialize }) => initialize());
  }

  // flatpickr
  if (document.querySelector("input.dateinput, input.datetimeinput")) {
    import("./plugins/flatpickr").then(({ initialize }) => initialize());
  }

  // sweetalert2
  if (document.querySelector("form[data-confirm]")) {
    import("./plugins/sweetalert2").then(({ initialize }) => initialize());
  }

  enableSubmitOn();
  enableChangeAvatarButton();
});

/**
 * Enable change/upload avatar button in the update user profile page.
 *
 * Path:       /account/update/
 * Template:   users/user_form.html
 * View class: UserUpdateView
 */
export function enableChangeAvatarButton() {
  if (location.pathname === "/account/update/") {
    const changeAvatarButton = document.getElementById("change_avatar_button");
    const changeAvatarInput = document.getElementById("change_avatar_input");

    // When the user clicked the change avatar button, open the file browser.
    changeAvatarButton.addEventListener("click", function () {
      changeAvatarInput.click();
    });

    // When the user has selected the file to upload, submit the form.
    changeAvatarInput.addEventListener("change", async function (event) {
      if (changeAvatarInput.files.length >= 1) {
        changeAvatarButton.form.submit();
      }
    });
  }
}

/**
 * Submit the parent form when an event is triggered.
 */
function enableSubmitOn() {
  document.querySelectorAll("[data-submit-on]").forEach((element) => {
    const eventName = element.getAttribute("data-submit-on");
    element.addEventListener(eventName, function (event) {
      element.form.submit();
    });
  });
}

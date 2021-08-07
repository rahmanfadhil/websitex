import "../scss/main.scss";

import "bootstrap/js/dist/dropdown"; // for dropdowns
import "bootstrap/js/dist/collapse"; // for mobile navigation

import getPageData from "./utils/pageData";
import * as notyf from "./plugins/notyf";
import * as imask from "./plugins/imask";
import * as sweetalert2 from "./plugins/sweetalert2";
import * as flatpickr from "./plugins/flatpickr";
import * as tagify from "./plugins/tagify";

window.addEventListener("DOMContentLoaded", function () {
  // notyf
  notyf.initialize();

  // trix
  if (document.querySelector("trix-editor")) {
    import("./plugins/trix").then(({ initialize }) => initialize());
  }

  // @yaireo/tagify
  if (document.querySelector("input.tagsinput")) {
    tagify.initialize();
  }

  // imask
  if (document.querySelector("input.moneyinput")) {
    imask.initialize();
  }

  // flatpickr
  if (document.querySelector("input.dateinput, input.datetimeinput")) {
    flatpickr.initialize();
  }

  // sweetalert2
  if (document.querySelector("form[data-confirm]")) {
    sweetalert2.initialize();
  }

  enableSubmitOn();
  enableChangeAvatarButton();
});

/**
 * Enable change/upload avatar button in the update user profile page.
 *
 * Path:       /account/update/
 * View name:  users:user_update
 * Template:   users/user_form.html
 * View class: UserUpdateView
 */
export function enableChangeAvatarButton() {
  const { view_name } = getPageData();
  if (view_name === "users:user_update") {
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

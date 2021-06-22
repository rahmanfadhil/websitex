import "@fontsource/lexend";
import "@fontsource/lexend/500.css";
import "@fontsource/lexend/700.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import "../scss/main.scss";

import "bootstrap/js/dist/collapse"; // for responsive navbar menu
import "bootstrap/js/dist/dropdown"; // for dropdowns

import { showMessages } from "./plugins/notyf";

window.addEventListener("DOMContentLoaded", async function () {
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

  if (location.pathname === "/account/update/") {
    enableChangeAvatarButton();
  }

  enableDataTable();
});

/**
 * Enable change/upload avatar button in the update user profile page.
 *
 * Path:       /account/update/
 * Template:   users/user_form.html
 * View class: UserUpdateView
 */
export function enableChangeAvatarButton() {
  const changeAvatarButton = document.getElementById("change_avatar_button"),
    changeAvatarInput = document.getElementById("change_avatar_input");

  // When the user clicked the change avatar button, open the file browser.
  changeAvatarButton.addEventListener("click", () => changeAvatarInput.click());

  // When the user has selected the file to upload, submit the form.
  changeAvatarInput.addEventListener("change", async function (event) {
    if (changeAvatarInput.files.length >= 1) {
      changeAvatarButton.form.submit();
    }
  });
}

/**
 * Initialize the data table element from the DataTableView.
 *
 * Make sure when the user select or deselect all item checkbox in the table
 * heading, all checkboxes in table changed accordingly.
 */
export function enableDataTable() {
  for (const element of document.querySelectorAll("form[data-table]")) {
    // When the user select or deselect all item checkbox in the table heading,
    // all checkboxes in table changed accordingly.
    element
      .querySelector("input[data-table-select-all]")
      .addEventListener("change", function (event) {
        element
          .querySelectorAll("input[data-table-select-item]")
          .forEach((item) => (item.checked = event.target.checked));
      });

    // When the user change how much entries to display per page, change the URL
    // search params, which will refetch the page.
    element
      .querySelector('select[name="per_page"]')
      .addEventListener("change", function (event) {
        const url = new URL(window.location.href);
        url.searchParams.set("per_page", event.target.value);
        location.href = url.href;
      });
  }
}

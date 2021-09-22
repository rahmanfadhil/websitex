import "bootstrap";
import Cookies from "js-cookie";
import { Notyf } from "notyf";
import getPageData from "./utils/pageData";
import reverse from "./utils/reverse";

import "../scss/main.scss";

// Enable mobile navigation menu
// https://getbootstrap.com/docs/5.1/examples/offcanvas-navbar/

document
  .querySelector("#navbarSideCollapse")
  .addEventListener("click", function () {
    document.querySelector(".offcanvas-collapse").classList.toggle("open");
  });

// Display notifications from the Django messages framework using Notyf.
// https://github.com/caroso1222/notyf

const notyf = new Notyf({
  duration: 5000,
  dismissible: true,
  position: { y: "top", x: "right" },
  types: [
    { type: "warning", className: "bg-warning" },
    { type: "info", className: "bg-info" },
  ],
});

const { messages } = getPageData();
for (const message of messages) {
  notyf.open(message);
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

// Modal forms

class ModalFormElement extends HTMLElement {
  connectedCallback() {
    // Show loading spinner
    this.form = this.querySelector("form");
    this.form.innerHTML = `
      <div class="my-5 text-center">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    `;
    this.form.addEventListener("submit", this.onFormSubmit.bind(this));

    this.addEventListener("shown.bs.modal", async function (event) {
      const response = await fetch(this.form.action + "?modal=true");
      this.form.innerHTML = await response.text();
    });
  }

  async onFormSubmit(event) {
    event.preventDefault();
    const data = new FormData(this.form);

    try {
      // Show loading spinner
      this.form.innerHTML = `
        <div class="my-5 text-center">
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
      `;

      const response = await fetch(this.form.action + "?modal=true", {
        method: this.form.method,
        body: data,
      });

      // If the response is not successful, show the error message. If the
      // response is a redirect, redirect the browser to the new URL. If the
      // form is invalid, replace the content with the response from server.
      if (!response.ok) {
        throw new Error(response.statusText);
      } else if (response.redirected) {
        window.location.href = response.url;
      } else {
        this.form.innerHTML = await response.text();
      }
    } catch (err) {
      console.error(err);
      const { default: Swal } = await import("sweetalert2");
      await Swal.fire({
        title: "Oops, something went wrong!",
        text: "We are trying to solve this issue, please try again next time...",
        icon: "error",
      });
      window.location.reload();
    }
  }
}

customElements.define("modal-form", ModalFormElement);

// Trix editor
// https://trix-editor.org/

if (document.querySelector("trix-editor")) {
  import("trix").then(() => {
    document.addEventListener("trix-attachment-add", async ({ attachment }) => {
      async function showErrorMessage() {
        const { default: Swal } = await import("sweetalert2");
        await Swal.fire({
          title: "Failed to upload attachment!",
          text: "Please try again next time...",
          icon: "error",
        });
      }

      if (attachment.file) {
        try {
          // Store the image to a form data.
          const formData = new FormData();
          formData.append("file", attachment.file);

          // Initialize
          const xhr = new XMLHttpRequest();
          const url = await reverse("core:media_create");
          xhr.open("POST", url, true);

          // Send the CSRF token to prevent the 403 forbidden error.
          xhr.setRequestHeader("X-CSRFToken", Cookies.get("csrftoken"));

          // Update the upload progress bar.
          xhr.upload.addEventListener("progress", function (event) {
            const progress = (event.loaded / event.total) * 100;
            attachment.setUploadProgress(progress);
          });

          // Handle when the server responded.
          xhr.addEventListener("load", function (event) {
            if (xhr.status === 200) {
              // Set the image url based on the server response.
              const { url } = JSON.parse(xhr.responseText);
              attachment.setAttributes({ url, href: url });
            } else {
              // Display an error alert to the user when the upload failed.
              showErrorMessage();
            }
          });

          // Perform the request.
          xhr.send(formData);
        } catch (err) {
          showErrorMessage();
        }
      }
    });
  });
}

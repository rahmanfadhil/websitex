import "@hotwired/turbo";
import Tagify from "@yaireo/tagify";
import { Toast } from "bootstrap";
import feather from "feather-icons";
import flatpickr from "flatpickr";
import IMask from "imask";
import Cookies from "js-cookie";
import Swal from "sweetalert2";
import "trix";

document.addEventListener("turbo:load", function () {
  // Bootstrap
  // -----------------------------------------------------------------------------

  for (const el of document.querySelectorAll(".toast")) {
    new Toast(el).show();
  }

  // Feather Icons
  // -----------------------------------------------------------------------------

  feather.replace({ width: "1em", height: "1em", "stroke-width": 2 });

  // Flatpickr
  // -----------------------------------------------------------------------------

  flatpickr("input.datetimepickerinput", {
    enableTime: true,
    altInput: true,
    altFormat: "F j, Y H:i",
    dateFormat: "Y-m-d H:i",
  });

  // IMask
  // -----------------------------------------------------------------------------

  for (const element of document.querySelectorAll("input.moneyinput")) {
    // Create the mask for currency inputs.
    const mask = IMask(element, {
      mask: Number,
      thousandsSeparator: ",",
      scale: 2,
      radix: ".",
    });

    // When the user submits the form, replace the value to the original value,
    // without the comma separator.
    element.form.addEventListener("submit", function (event) {
      element.value = mask.unmaskedValue;
    });
  }

  // SweetAlert2
  // -----------------------------------------------------------------------------

  for (const el of document.querySelectorAll("[data-confirm-submit]")) {
    el.addEventListener("click", async function (event) {
      const url = event.target.getAttribute("data-confirm-submit");
      const title = event.target.getAttribute("data-title");
      const description = event.target.getAttribute("data-description");
      const confirmTitle = event.target.getAttribute("data-confirm-title");
      const confirmColor = event.target.getAttribute("data-confirm-color");
      const rejectTitle = event.target.getAttribute("data-reject-title");
      const rejectColor = event.target.getAttribute("data-reject-color");

      const result = await Swal.fire({
        icon: "warning",
        title: title ?? "Are you sure?",
        html: description ?? "You won't be able to revert this!",
        showCancelButton: true,
        buttonsStyling: false,
        confirmButtonText: confirmTitle ?? "Delete",
        cancelButtonText: rejectTitle ?? "Cancel",
        customClass: {
          confirmButton: `btn btn-${confirmColor ?? "danger"}`,
          cancelButton: `btn btn-${rejectColor ?? "secondary"} ms-3`,
        },
      });

      // Handle when the user clicked "Confirm" button.
      if (result.isConfirmed) {
        // Create a form element.
        const formElement = document.createElement("form");
        formElement.setAttribute("method", "POST");
        formElement.setAttribute("action", url);

        // Attach the CSRF token value to the form that we get from the cookies
        // to prevent 403 forbidden error.
        const csrfElement = document.createElement("input");
        csrfElement.setAttribute("type", "hidden");
        csrfElement.setAttribute("name", "csrfmiddlewaretoken");
        csrfElement.setAttribute("value", Cookies.get("csrftoken"));

        // Attach the form element to the HTML body so that we can call `submit`
        // programatically. Otherwise, it will throw an error.
        formElement.appendChild(csrfElement);
        document.body.appendChild(formElement);

        // Submit the form.
        formElement.submit();
      }
    });
  }

  // Tagify
  // -----------------------------------------------------------------------------

  for (const element of document.querySelectorAll("input.tagsinput")) {
    new Tagify(element, {
      originalInputValueFormat: (values) =>
        values.map((item) => item.value).join(","),
    });
  }

  // Trix
  // -----------------------------------------------------------------------------

  document.addEventListener("trix-attachment-add", function (event) {
    const { attachment } = event;

    if (attachment.file) {
      // Store the image to a form data.
      const formData = new FormData();
      formData.append("file", event.attachment.file);

      // Initialize
      const xhr = new XMLHttpRequest();
      xhr.open("POST", "/upload-media/", true);

      // Set the CSRF token to prevent the 403 forbidden error.
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
          Swal.fire({
            title: "Failed to upload attachment!",
            text: "Please try again next time...",
            icon: "error",
          });
        }
      });

      // Perform the request.
      xhr.send(formData);
    }
  });
});

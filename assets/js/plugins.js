import { Toast } from "bootstrap";
import feather from "feather-icons";
import flatpickr from "flatpickr";
import IMask from "imask";
import "trix";

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

for (const element of document.querySelectorAll(".moneyinput")) {
  const mask = IMask(element, {
    mask: Number,
    thousandsSeparator: ",",
    scale: 2,
    radix: ".",
  });
  element.form.addEventListener("submit", function (event) {
    element.value = mask.unmaskedValue;
  });
}

// Trix
// -----------------------------------------------------------------------------

document.addEventListener("trix-attachment-add", function (event) {
  console.log(event);
});

// SweetAlert2
// -----------------------------------------------------------------------------

for (const el of document.querySelectorAll("[data-confirm-submit]")) {
  el.addEventListener("click", async function (event) {
    event.preventDefault();

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

    if (result.isConfirmed) {
      const formElement = document.createElement("form");
      formElement.setAttribute("method", "POST");
      formElement.setAttribute("action", url);
      const csrfElement = document.createElement("input");
      csrfElement.setAttribute("type", "hidden");
      csrfElement.setAttribute("name", "csrfmiddlewaretoken");
      csrfElement.setAttribute("value", getCookie("csrftoken"));
      formElement.appendChild(csrfElement);
      document.body.appendChild(formElement);
      formElement.submit();
    }
  });
}

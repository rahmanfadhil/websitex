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
  const mask = IMask(element, { mask: Number, thousandsSeparator: "," });
  element.form.addEventListener("submit", function (event) {
    element.value = mask.unmaskedValue;
  });
}

// Trix
// -----------------------------------------------------------------------------

document.addEventListener("trix-attachment-add", function (event) {
  console.log(event);
});

import { Toast } from "bootstrap";
import feather from "feather-icons";
import flatpickr from "flatpickr";
import Cleave from "cleave.js";
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

flatpickr("input.datetimepickerinput");

// Cleave.js
// -----------------------------------------------------------------------------

for (const element of document.querySelectorAll(".moneyinput")) {
  new Cleave(element, {
    numeral: true,
    numeralThousandsGroupStyle: "thousand",
  });
}

// Trix
// -----------------------------------------------------------------------------

document.addEventListener("trix-attachment-add", function (event) {
  console.log(event);
});

import { Toast } from "bootstrap";
import feather from "feather-icons";
import flatpickr from "flatpickr";
import Cleave from "cleave.js";
import "trix";

feather.replace({ width: "1em", height: "1em", "stroke-width": 2 });

for (const el of document.querySelectorAll(".toast")) {
  new Toast(el).show();
}

flatpickr("input.datetimepickerinput");

new Cleave(".moneyinput", {
  numeral: true,
  numeralThousandsGroupStyle: "thousand",
});

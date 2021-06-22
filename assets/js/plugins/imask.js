import IMask from "imask";

/**
 * Initialize the IMask plugin for currency/price form inputs.
 */
export function initialize() {
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
}

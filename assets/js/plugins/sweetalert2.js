import Swal from "sweetalert2";

/**
 * Show confirmation popup before submitting a form.
 */
export function initialize() {
  for (const element of document.querySelectorAll("form[data-confirm]")) {
    // Determine if the user has confirmed the form submission.
    let isConfirmed = false;

    element.addEventListener("submit", async function (event) {
      // If the user clicked the confirm button, don't show the popup again.
      if (isConfirmed) return;

      // Prevent the default browser behavior of submitting this form.
      event.preventDefault();

      // Collect the information to show in the confirmation popup from the
      // elements `data-*` attributes.
      const title = element.getAttribute("data-confirm-title");
      const subtitle = element.getAttribute("data-confirm-subtitle");
      const confirmTitle = element.getAttribute("data-confirm-button-title");
      const confirmClass = element.getAttribute("data-confirm-button-class");

      // Display the confirmation popup.
      const result = await Swal.fire({
        icon: "warning",
        title: title ?? "Are you sure?",
        html: subtitle ?? "You won't be able to revert this!",
        buttonsStyling: false,
        confirmButtonText: confirmTitle ?? "Confirm",
        customClass: {
          confirmButton: `btn ${confirmClass ?? "btn-danger"}`,
        },
      });

      // When the user confirmed, submit this form.
      if (result.isConfirmed) {
        isConfirmed = true;
        element.submit();
      }
    });
  }
}

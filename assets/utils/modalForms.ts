const LOADING_SPINNER = `
  <div class="my-5 text-center">
    <div class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
`;

// Get modal form elements from the document
const forms = document.querySelectorAll("form[data-modal-form]");

for (const form of forms as NodeListOf<HTMLFormElement>) {
  // Show loading indicator because the form isn't fetched yet.
  form.innerHTML = LOADING_SPINNER;

  // Get the bootstrap modal element from `data-modal-form` attribute or find
  // the closest parent element with `modal` class.
  const modal = form.dataset.modalForm
    ? document.querySelector(form.dataset.modalForm)
    : form.closest(".modal");

  // Fetch and display the form from the server.
  modal.addEventListener("shown.bs.modal", async function () {
    const response = await fetch(form.action + "?modal=true");
    form.innerHTML = await response.text();
  });

  form.addEventListener("submit", async function (event) {
    // Prevent the browser from submitting the form.
    event.preventDefault();

    try {
      // Show the loading indicator
      form.innerHTML = LOADING_SPINNER;

      // Send the form data to the server
      const response = await fetch(form.action + "?modal=true", {
        method: form.method,
        body: new FormData(form),
      });

      // If the response is not successful, show the error message. If the
      // response is a redirect, redirect the browser to the new URL. If the
      // form is invalid, replace the content with the response from server.
      if (!response.ok) {
        throw new Error(response.statusText);
      } else if (response.redirected) {
        window.location.href = response.url;
      } else {
        form.innerHTML = await response.text();
      }
    } catch (err) {
      // Log the error to the console.
      console.error(err);

      // Show the error message to the user.
      const { default: Swal } = await import("sweetalert2");
      await Swal.fire({
        title: "Oops, something went wrong!",
        text: "We are trying to solve this issue, please try again next time...",
        icon: "error",
      });

      // Reload the page.
      window.location.reload();
    }
  });
}

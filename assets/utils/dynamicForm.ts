// Get dynamic form elements from the document
const forms = document.querySelectorAll("form[data-dynamic-form]");

for (const form of forms as NodeListOf<HTMLFormElement>) {
  // Grab the form `id` in case there are multiple forms in the page
  const formId = form.dataset.dynamicForm;

  form.addEventListener("submit", async function (event) {
    // Prevent the browser from submitting the form.
    event.preventDefault();

    try {
      // Send the form data to the server
      const response = await fetch(form.action, {
        method: form.method,
        body: new FormData(form),
      });

      // If the response is not successful, show the error message.
      if (!response.ok) {
        throw new Error(response.statusText);
      }

      // If the response is a redirect, redirect the browser to the new URL.
      if (response.redirected) {
        window.location.href = response.url;
        return;
      }

      // Parse respose content into a DOM
      const parser = new DOMParser();
      const content = parser.parseFromString(
        await response.text(),
        "text/html"
      );

      // Get same form from the response
      const newForm = content.querySelector(
        `form[data-dynamic-form="${formId}"]`
      );

      // Replace the old form content with the new form which contains the
      // error messages
      if (newForm) {
        form.replaceChildren(...newForm.childNodes);
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

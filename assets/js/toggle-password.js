// Toggle password visibility
// https://web.dev/sign-in-form-best-practices/#password-display

for (const button of document.querySelectorAll("[data-toggle-password]")) {
  const passwordInput = document.getElementById(button.dataset.togglePassword);

  button.addEventListener("click", function () {
    if (passwordInput.type === "password") {
      passwordInput.type = "text";
      button.textContent = gettext("Hide password");
      button.setAttribute("aria-label", gettext("Hide password"));
    } else {
      passwordInput.type = "password";
      button.textContent = gettext("Show password");
      button.setAttribute("aria-label", gettext("Show password"));
    }
  });
}

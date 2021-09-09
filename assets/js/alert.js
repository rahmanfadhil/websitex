for (const element of document.querySelectorAll(".alert")) {
  const closeButton = element.querySelector(".alert__close");
  if (closeButton) {
    closeButton.addEventListener("click", () => element.remove());
  }
}

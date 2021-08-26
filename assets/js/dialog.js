// https://www.smashingmagazine.com/2014/09/making-modal-windows-better-for-everyone/

for (const button of document.querySelectorAll("[data-open-dialog]")) {
  const dialog = document.querySelector(
    button.getAttribute("data-open-dialog")
  );
  const dialogWindow = dialog.querySelector("[role=document]");

  let previousActiveElement;

  button.addEventListener("click", () => {
    previousActiveElement = document.activeElement;

    dialog.classList.add("open");

    document.addEventListener("keydown", closeDialogOnEscape);
    dialog
      .querySelectorAll("button, a")
      .forEach((el) => el.addEventListener("click", closeDialog));
    dialogWindow.addEventListener("click", stopPropagation);
    dialog.addEventListener("click", closeDialog);

    dialog.setAttribute("aria-hidden", "false");
    dialogWindow.setAttribute("tabindex", "0");
    dialogWindow.focus();
  });

  const stopPropagation = (e) => e.stopPropagation();
  const closeDialogOnEscape = (e) => e.key === "Escape" && closeDialog();

  function closeDialog() {
    dialog.classList.remove("open");

    document.removeEventListener("keydown", closeDialogOnEscape);
    dialog
      .querySelectorAll("button, a")
      .forEach((el) => el.removeEventListener("click", closeDialog));
    dialogWindow.removeEventListener("click", stopPropagation);
    dialog.removeEventListener("click", closeDialog);

    dialog.setAttribute("aria-hidden", "true");
    dialogWindow.setAttribute("tabindex", "-1");
    previousActiveElement.focus();
  }
}

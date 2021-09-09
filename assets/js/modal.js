// https://www.smashingmagazine.com/2014/09/making-modal-windows-better-for-everyone/
// https://codepen.io/scottohara/pen/lIdfv

/**
 * Returns back a NodeList of focusable elements
 * that exist within the passed parent HTMLElement, or
 * an empty array if no parent passed.
 *
 * @param {HTMLElement} parent HTML element
 * @returns {(NodeList|Array)} The focusable elements that we can find
 */
function getAllFocusableElements(parent = document.body) {
  return parent.querySelectorAll(
    'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"]):not([disabled]), details:not([disabled]), summary:not(:disabled)'
  );
}

function createKeydownHandler(firstFocusableElement, lastFocusableElement) {
  return function (e) {
    if (!e.key === "Tab") return;

    if (e.shiftKey) {
      // if shift key pressed for shift + tab combination
      if (document.activeElement === firstFocusableElement) {
        lastFocusableElement.focus(); // add focus for the last focusable element
        e.preventDefault();
      }
    } else {
      // if tab key is pressed
      if (document.activeElement === lastFocusableElement) {
        // if focused has reached to last focusable element then focus first focusable element after pressing tab
        firstFocusableElement.focus(); // add focus for the first focusable element
        e.preventDefault();
      }
    }
  };
}

let previousActiveElement = null;
let keydownHandler = null;

export function openModal(element) {
  previousActiveElement = document.activeElement;
  element.classList.add("open");
  element.setAttribute("aria-hidden", "false");
  element.setAttribute("aria-modal", "true");
  element.setAttribute("tabindex", "0");

  const focusableElements = getAllFocusableElements(element);
  const firstFocusableElement = focusableElements[0];
  const lastFocusableElement = focusableElements[focusableElements.length - 1];

  firstFocusableElement.focus();

  keydownHandler = createKeydownHandler(
    firstFocusableElement,
    lastFocusableElement
  );
  document.addEventListener("keydown", keydownHandler);
}

export function closeModal(element) {
  element.classList.remove("open");
  element.setAttribute("aria-hidden", "true");
  element.removeAttribute("aria-modal");
  element.setAttribute("tabindex", "-1");
  previousActiveElement.focus();
  document.removeEventListener("keydown", keydownHandler);
}

for (const button of document.querySelectorAll("[data-toggle-modal]")) {
  const modal = document.querySelector(button.dataset.toggleModal);
  button.addEventListener("click", () => {
    modal.classList.contains("open") ? closeModal(modal) : openModal(modal);
  });
}

for (const modal of document.querySelectorAll(".modal")) {
  const content = modal.querySelector(".modal__content");
  content.addEventListener("click", (e) => e.stopPropagation());
  modal.addEventListener("click", () => closeModal(modal));
}

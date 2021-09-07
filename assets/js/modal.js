// https://www.smashingmagazine.com/2014/09/making-modal-windows-better-for-everyone/
// https://codepen.io/scottohara/pen/lIdfv

class ModalDialog extends HTMLElement {
  /**
   * Set the visibility of the modal.
   */
  get visible() {
    return this.hasAttribute("visible");
  }

  /**
   * Set the visibility of the modal.
   */
  set visible(value) {
    if (value) {
      this.setAttribute("visible", "");
    } else {
      this.removeAttribute("visible");
    }
  }

  static get observedAttributes() {
    return ["visible"];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (oldValue === newValue) return;
    if (name === "visible") {
      newValue === null ? this.hide() : this.show();
    }
  }

  /**
   * Show the modal.
   */
  show = () => {
    // Remember the previous active element, so that when we close the modal,
    // we can set the focus back to it.
    this.previousActiveElement = document.activeElement;

    // Add event listeners to close the modal
    this.addEventListener("click", this.hide);
    this.content.addEventListener("click", this.stopPropagation);
    document.addEventListener("keydown", this.closeDialogOnEscape);

    // Make the modal visible with css
    this.classList.add("open");

    // Set accessibility attributes
    this.setAttribute("aria-hidden", "false");
    this.content.setAttribute("tabindex", "0");

    // Focus on the modal
    this.content.focus();

    // Make sure the visible attribute is updated
    this.visible = true;
  };

  /**
   * Hide the modal.
   */
  hide = () => {
    // Make the modal invisible with css
    this.classList.remove("open");

    // Set accessibility attributes
    this.setAttribute("aria-hidden", "true");
    this.content.setAttribute("tabindex", "-1");

    // Remove the event listeners to close the modal
    this.removeEventListener("click", this.hide);
    this.content.removeEventListener("click", this.stopPropagation);
    document.removeEventListener("keydown", this.closeDialogOnEscape);

    // Set focus back to the element that had it before the modal was opened.
    this.previousActiveElement.focus();

    // Make sure the visible attribute is updated
    this.visible = false;
  };

  /**
   * Stop event propagation so that the modal can't be closed by clicking on the
   * modal content.
   *
   * @param {Event} event
   * @returns {void}
   * @private
   * @memberof ModalDialog
   * @see https://developer.mozilla.org/en-US/docs/Web/API/Event/stopPropagation
   */
  stopPropagation = (e) => {
    e.stopPropagation();
  };

  /**
   * Close the modal when the escape key is pressed.
   *
   * @param {Event} event
   * @returns {void}
   * @private
   * @memberof ModalDialog
   * @see https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/key
   */
  closeDialogOnEscape = (e) => {
    if (e.key === "Escape") this.hide();
  };

  connectedCallback() {
    // Modify  the modal custom element
    this.classList.add("modal");
    this.setAttribute("aria-hidden", "true");
    this.setAttribute("tabindex", "-1");

    // If the visible property is already defined, open the modal immediately.
    if (this.visible) this.classList.add("open");

    // Create the modal content element. This is the element that will be
    // focused when the modal is opened. We set the ARIA role to "document" so
    // that it can be recognized by screen readers and prevent users from
    // exiting the modal by tabbing out of it.
    this.content = document.createElement("div");
    this.content.classList.add("modal__content");
    this.content.setAttribute("role", "document");

    // Move the children of the <x-modal> element into the modal content.
    this.content.append(...this.children);

    // If there is a heading element inside the x-modal, set it as the
    // modal label.
    const title = this.content.querySelector("h1, h2, h3, h4, h5, h6");
    if (title) {
      // If the heading element doesn't have an id, generate a unique one.
      if (!title.id) {
        title.id =
          title.textContent
            .toLowerCase()
            .replace(/ /g, "-")
            .replace(/[^\w-]+/g, "") +
          "-modal-label-" +
          (Math.random() + 1).toString(36).substring(7);
      }
      this.setAttribute("aria-labelledby", title.id);
    }

    const closeButton = document.createElement("button");
    closeButton.classList.add("modal__close");
    closeButton.setAttribute("aria-label", "Close");
    closeButton.addEventListener("click", this.hide);
    this.content.appendChild(closeButton);

    this.appendChild(this.content);
  }
}

customElements.define("x-modal", ModalDialog);

for (const button of document.querySelectorAll("[data-toggle-modal]")) {
  const modal = document.querySelector(
    button.getAttribute("data-toggle-modal")
  );
  button.addEventListener("click", () => (modal.visible = !modal.visible));
}

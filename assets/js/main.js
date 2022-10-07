import focus from "@alpinejs/focus";
import Alpine from "alpinejs";
import { createFocusTrap } from "focus-trap";
import { animate } from "popmotion";

import "@fontsource/nunito/variable.css";
import "../css/main.css";

// Initialize Alpine.js
// https://alpinejs.dev/essentials/installation

Alpine.plugin(focus);
Alpine.start();

class Modal {
  /**
   * @param {HTMLElement} element
   */
  constructor(element) {
    if (!element) {
      throw new Error("No element provided");
    }

    this.root = element;
    this.root.classList.add(
      "fixed",
      "z-10",
      "inset-0",
      "overflow-y-auto",
      "hidden"
    );
    this.root.setAttribute("tabindex", "-1");
    this.root.setAttribute("role", "dialog");
    this.root.setAttribute("aria-modal", "true");
    this.root.setAttribute("aria-hidden", "true");

    this.container = document.createElement("div");
    this.container.classList.add(
      "modal-container",
      "flex",
      "items-center",
      "justify-center",
      "min-h-screen"
    );

    this.overlay = document.createElement("div");
    this.overlay.classList.add(
      "modal-overlay",
      "fixed",
      "inset-0",
      "bg-black",
      "opacity-30"
    );
    this.overlay.addEventListener("click", () => this.close());
    this.container.append(this.overlay);

    this.content = document.createElement("div");
    this.content.classList.add(
      "modal-content",
      "relative",
      "bg-white",
      "rounded",
      "max-w-md",
      "mx-auto",
      "w-full",
      "p-8"
    );
    this.content.append(...this.root.childNodes);
    this.container.append(this.content);
    this.root.append(this.container);

    this.focusTrap = createFocusTrap(this.container, {
      onDeactivate: () => this.close(),
    });
  }

  open() {
    animate({
      from: { opacity: 0 },
      to: { opacity: 0.3 },
      duration: 300,
      onUpdate: (v) => {
        this.overlay.style.opacity = v.opacity;
      },
    });
    animate({
      from: { opacity: 0, scale: 0 },
      to: { opacity: 1, scale: 1 },
      duration: 200,
      onPlay: () => {
        this.root.classList.remove("hidden");
      },
      onUpdate: (v) => {
        this.content.style.opacity = v.opacity;
        this.content.style.transform = `scale(${v.scale})`;
      },
      onComplete: () => {
        this.root.setAttribute("aria-hidden", "false");
        this.focusTrap.activate();
      },
    });
  }

  close() {
    animate({
      from: { opacity: 0.3 },
      to: { opacity: 0 },
      duration: 300,
      onUpdate: (v) => {
        this.overlay.style.opacity = v.opacity;
      },
    });
    animate({
      from: { opacity: 1, scale: 1 },
      to: { opacity: 0, scale: 0 },
      duration: 200,
      onPlay: () => {
        this.focusTrap.deactivate();
      },
      onUpdate: (v) => {
        this.content.style.opacity = v.opacity;
        this.content.style.transform = `scale(${v.scale})`;
      },
      onComplete: () => {
        this.root.classList.add("hidden");
        this.root.setAttribute("aria-hidden", "true");
      },
    });
  }
}

const modals = new WeakMap();

function createModal(element) {
  if (modals.has(element)) {
    return modals.get(element);
  } else {
    const modal = new Modal(element);
    modals.set(element, modal);
    return modal;
  }
}

for (const button of document.querySelectorAll("[data-modal]")) {
  const element = document.querySelector(button.dataset.modal);
  const modal = createModal(element);
  button.addEventListener("click", () => {
    modal.open();
  });
}

// const result = animate({
//   from: {
//     opacity: 0,
//     scale: 0,
//   },
//   to: {
//     opacity: 1,
//     scale: 1,
//   },
//   onUpdate: (v) => {
//     console.log(v);
//   },
// });
// console.log(result);

customElements.define(
  "x-modal",
  class extends HTMLElement {
    constructor() {
      super();

      let templateElement = document.getElementById("x-modal-template");
      let template = templateElement.content.cloneNode(true);
      this.appendChild(template);
    }

    get open() {
      return this.hasAttribute("open");
    }

    set open(value) {
      console.log(value);
      if (value) {
        this.setAttribute("open", "");
      } else {
        this.removeAttribute("open");
      }
    }

    attributeChangedCallback(name, oldValue, newValue) {
      console.log(name, oldValue, newValue);
      this.update();
      // if (name === "open" && this.shadowRoot) {
      //   if (newValue === null) {
      //     this.querySelector(".modal-wrapper").classList.add("hidden");
      //   } else {
      //     this.querySelector(".modal-wrapper").classList.remove("hidden");
      //   }
      // }
    }

    update() {
      if (this.open) {
        this.querySelector(".modal-wrapper").classList.remove("hidden");
      } else {
        this.querySelector(".modal-wrapper").classList.add("hidden");
      }
    }

    connectedCallback() {
      this.update();

      this.querySelector(".modal-overlay").addEventListener("click", () => {
        this.open = false;
      });
    }

    // connectedCallback() {
    //   this.shadowRoot.querySelector("button").addEventListener("click", () => {
    //     const modal = createModal(this);
    //     modal.open();
    //   });
    // }
  }
);

import Alpine from "https://unpkg.com/alpinejs@3.4.2/dist/module.esm.js";
import { Notyf } from "https://unpkg.com/notyf@3.10.0/notyf.es.js";

// Initialize Alpine.js
// https://alpinejs.dev/essentials/installation

Alpine.start();

// Display notifications from the Django messages framework using Notyf.
// https://github.com/caroso1222/notyf

const notyf = new Notyf({
  duration: 5000,
  dismissible: true,
  position: { y: "top", x: "center" },
  types: [
    { type: "warning", className: "bg-warning" },
    { type: "info", className: "bg-info" },
  ],
});

const { messages } = getPageData();
for (const message of messages) {
  notyf.open(message);
}

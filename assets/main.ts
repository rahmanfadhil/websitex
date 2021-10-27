import { Notyf } from "notyf";
import Alpine from "alpinejs";
import trap from "@alpinejs/trap";
import Sortable from "sortablejs";
import getPageData from "./utils/getPageData";
import "./utils/modalForms";
import "./utils/trix";

import "@fontsource/nunito-sans/200.css";
import "@fontsource/nunito-sans/300.css";
import "@fontsource/nunito-sans/400.css";
import "@fontsource/nunito-sans/600.css";
import "@fontsource/nunito-sans/700.css";
import "@fontsource/nunito-sans/800.css";
import "@fontsource/nunito-sans/900.css";

import "./main.css";
import "notyf/notyf.min.css";

const stages = document.getElementById("stages");
if (stages) {
  new Sortable(stages, {
    animation: 150,
    filter: ".js-immovable",
    preventOnFilter: true,
    onMove: (event) => !event.related.classList.contains("js-immovable"),
  });

  for (const stage of stages.children) {
    new Sortable(stage.querySelector(".js-stage-content"), {
      group: "shared",
      animation: 150,
      filter: ".js-immovable",
      preventOnFilter: true,
    });
  }
}

// Initialize Alpine.js
// https://alpinejs.dev/essentials/installation

Alpine.plugin(trap);
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

// PWA
// https://developers.google.com/web/fundamentals/primers/service-workers

if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("/service-worker.js", { scope: "/" }).then(
      function (registration) {
        // Registration was successful
        console.log(
          "ServiceWorker registration successful with scope: ",
          registration.scope
        );
      },
      function (err) {
        // registration failed :(
        console.log("ServiceWorker registration failed: ", err);
      }
    );
  });
}

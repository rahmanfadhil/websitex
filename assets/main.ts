import "bootstrap";
import { Notyf } from "notyf";
import getPageData from "./utils/getPageData";
import "./utils/modalForms";
import "./utils/trix";

import "./scss/main.scss";

// Enable mobile navigation menu
// https://getbootstrap.com/docs/5.1/examples/offcanvas-navbar/

const navbarSideCollapse = document.querySelector("#navbarSideCollapse");
navbarSideCollapse?.addEventListener("click", function () {
  document.querySelector(".offcanvas-collapse")?.classList.toggle("open");
});

// Display notifications from the Django messages framework using Notyf.
// https://github.com/caroso1222/notyf

const notyf = new Notyf({
  duration: 5000,
  dismissible: true,
  position: { y: "top", x: "right" },
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

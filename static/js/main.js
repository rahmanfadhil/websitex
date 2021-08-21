import getPageData from "./utils/pageData.js";
import "./plugins/sweetalert2.js";

const { messages } = getPageData();

// Load messages
if (messages.length) {
  const { Notyf } = await import("notyf");
  const notyf = new Notyf({
    duration: 5000,
    dismissible: true,
    position: { y: "top", x: "right" },
    types: [
      { type: "warning", background: "#FFFF00" },
      { type: "info", background: "#0000FF" },
    ],
  });
  for (const message of messages) {
    notyf.open(message);
  }
}

const toggle = document.querySelector("#toggle");
const menu = document.querySelector("#menu");

toggle.addEventListener("click", function () {
  if (menu.classList.contains("open")) {
    this.setAttribute("aria-expanded", "false");
    menu.classList.remove("open");
  } else {
    menu.classList.add("open");
    this.setAttribute("aria-expanded", "true");
  }
});

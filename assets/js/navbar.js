// Mobile responsive navigation menu

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

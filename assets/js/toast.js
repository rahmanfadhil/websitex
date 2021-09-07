// Toast messages

const toast = document.querySelector(".toast");
if (toast) {
  // Hide toast message if the close button is clicked
  toast.querySelectorAll("button").forEach((el) => {
    el.addEventListener("click", () => el.parentElement.remove());
  });

  // Hide all toast messages after 5 seconds
  setTimeout(() => {
    Array.from(toast.children).forEach((el) => el.classList.add("hidden"));
  }, 5000);
}

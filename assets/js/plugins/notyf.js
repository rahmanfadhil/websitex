import { Notyf } from "notyf";
import "notyf/notyf.min.css";

/**
 * Display notifications from the Django messages framework using Notyf.
 */
export function showMessages() {
  const notyf = new Notyf({
    duration: 5000,
    dismissible: true,
    position: { y: "top", x: "right" },
    types: [
      { type: "warning", className: "bg-warning" },
      { type: "info", className: "bg-info" },
    ],
  });

  const messagesElement = document.getElementById("json_messages");
  if (messagesElement) {
    const messages = JSON.parse(messagesElement.textContent);
    for (const message of messages) {
      notyf.open(message);
    }
  }
}

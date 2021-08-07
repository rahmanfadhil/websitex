import { Notyf } from "notyf";
import getPageData from "../utils/pageData";

/**
 * Display notifications from the Django messages framework using Notyf.
 */
export function initialize() {
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
}

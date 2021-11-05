import "htmx.org";
import trap from "@alpinejs/trap";
import Alpine from "alpinejs";
import { create } from "filepond";

import "./main.css";
import { trixAttachmentAdd } from "./utils/trix";

// Initialize Alpine.js
// https://alpinejs.dev/essentials/installation

Alpine.plugin(trap);
Alpine.start();

// Replace file inputs with FilePond
// https://pqina.nl/filepond/docs/getting-started/examples/replace-file-input/
for (const element of document.querySelectorAll('input[type="file"]')) {
  create(element, { storeAsFile: true } as any);
}

// If the document contains a <trix-editor />, load the Trix library and
// register an event listener that handles file attachments.
if (document.querySelector("trix-editor")) {
  import("trix");
  document.addEventListener("trix-attachment-add", trixAttachmentAdd);
}

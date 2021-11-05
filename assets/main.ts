import trap from "@alpinejs/trap";
import Alpine from "alpinejs";
import { create } from "filepond";
import "htmx.org";

import "./main.css";
import "./utils/trix";

// Initialize Alpine.js
// https://alpinejs.dev/essentials/installation

Alpine.plugin(trap);
Alpine.start();

for (const element of document.querySelectorAll('input[type="file"]')) {
  create(element, { storeAsFile: true } as any);
}

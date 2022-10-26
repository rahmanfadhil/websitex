// add the beginning of your app entry
import "vite/modulepreload-polyfill";

import focus from "@alpinejs/focus";
import Alpine from "alpinejs";

import "@fontsource/nunito/variable.css";
import "./css/main.css";

// Initialize Alpine.js
// https://alpinejs.dev/essentials/installation

Alpine.plugin(focus);
Alpine.start();

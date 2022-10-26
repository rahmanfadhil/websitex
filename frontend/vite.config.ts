import { defineConfig } from "vite";

export default defineConfig({
  server: {
    origin: "http://localhost:5173",
    host: true,
  },
  base: "/static/dist/",
  build: {
    // generate manifest.json in outDir
    manifest: true,
    outDir: "../backend/static/dist",
    rollupOptions: {
      // overwrite default .html entry
      input: "src/main.ts",
    },
  },
});

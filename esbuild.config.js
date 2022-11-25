const isDevelopment = process.env.NODE_ENV !== "production";

require("esbuild")
  .build({
    entryPoints: ["assets/main.ts"],
    bundle: true,
    outdir: "static/dist",
    minify: !isDevelopment,
    watch: isDevelopment,
    sourcemap: isDevelopment,
  })
  .catch(() => process.exit(1));

const fs = require("fs").promises;

const processor = require("postcss")([
  require("tailwindcss"),
  require("autoprefixer"),
]);

const plugin = {
  name: "app-plugin",
  setup(build) {
    build.onLoad({ filter: /\.css$/ }, async (args) => {
      const css = await fs.readFile(args.path, "utf8");
      const result = await processor.process(css, { from: args.path });
      return { contents: result.css, loader: "css" };
    });
  },
};

const isDevelopment = process.env.NODE_ENV !== "production";

require("esbuild")
  .build({
    entryPoints: ["frontend/main.ts"],
    bundle: true,
    outdir: "static/dist",
    loader: {
      ".woff2": "file",
    },
    plugins: [plugin],
    minify: !isDevelopment,
    watch: isDevelopment,
  })
  .catch(() => process.exit(1));

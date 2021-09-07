import resolve from "@rollup/plugin-node-resolve";
import replace from "@rollup/plugin-replace";
import autoprefixer from "autoprefixer";
import fs from "fs/promises";
import path from "path";
import postcss from "postcss";
import postcssImport from "postcss-import";
import postcssUrl from "postcss-url";

function css({ from, to }) {
  const buildDir = path.dirname(to);

  const processor = postcss([autoprefixer, postcssImport]).use(
    postcssUrl({
      url({ absolutePath }) {
        const fileName = path.basename(absolutePath);
        fs.copyFile(absolutePath, path.resolve(buildDir, fileName));
        return fileName;
      },
    })
  );

  return {
    name: "css",
    async buildStart() {
      this.addWatchFile(from);
      await fs.mkdir(buildDir, { recursive: true });
      const data = await fs.readFile(from);
      const result = await processor.process(data, {
        from,
        map: { inline: false },
      });
      await fs.writeFile(to, result.css);
      if (result.map) await fs.writeFile(`${to}.map`, result.map.toString());
    },
  };
}

const sharedPlugins = [
  resolve(),
  replace({
    values: {
      "process.env.NODE_ENV": JSON.stringify(
        process.env.NODE_ENV || "production"
      ),
    },
    preventAssignment: true,
  }),
];

export default [
  {
    input: "assets/js/main.js",
    output: {
      file: "static/dist/main.js",
      format: "es",
      sourcemap: true,
    },
    plugins: [
      css({ from: "assets/css/main.css", to: "static/dist/main.css" }),
      ...sharedPlugins,
    ],
  },
  {
    input: "assets/js/sw.js",
    output: {
      file: "static/dist/sw.js",
      format: "iife",
      sourcemap: true,
    },
    plugins: sharedPlugins,
  },
];

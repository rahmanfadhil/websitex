// Sources:
// https://webpack.js.org/plugins/mini-css-extract-plugin/#recommended
// https://webpack.js.org/loaders/postcss-loader/#extract-css
// https://webpack.js.org/guides/asset-management/#loading-fonts

const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = (env, argv) => {
  const devMode = argv.mode === "development";

  return {
    entry: {
      main: "./assets/js/main.js",
    },
    output: {
      filename: "[name].js",
      path: path.resolve(__dirname, "project/static/dist"),
    },
    devtool: devMode ? "eval" : false,
    module: {
      rules: [
        {
          test: /\.css$/i,
          use: [MiniCssExtractPlugin.loader, "css-loader", "postcss-loader"],
        },
        {
          test: /\.(png|svg|jpg|jpeg|gif)$/i,
          type: "asset/resource",
        },
        {
          test: /\.(woff|woff2|eot|ttf|otf)$/i,
          type: "asset/resource",
        },
      ],
    },
    resolve: {
      extensions: [".js", ".jsx", ".mjs"],
    },
    plugins: [new MiniCssExtractPlugin()],
  };
};

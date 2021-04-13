const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const { SourceMapDevToolPlugin } = require("webpack");

module.exports = {
  entry: ["./assets/js/main.js", "./assets/scss/main.scss"],
  output: {
    filename: "[name].js",
    path: path.resolve(__dirname, "static/dist"),
  },
  plugins: [
    new MiniCssExtractPlugin({ filename: "[name].css" }),
    new SourceMapDevToolPlugin({ filename: "[file].map" }),
  ],
  module: {
    rules: [
      {
        test: /\.s[ac]ss$/i,
        use: [
          MiniCssExtractPlugin.loader,
          { loader: "css-loader", options: { url: false } },
          "sass-loader",
        ],
      },
    ],
  },
  optimization: {
    minimizer: ["...", new CssMinimizerPlugin({ parallel: true })],
  },
};

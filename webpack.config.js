const path = require("path");
const { SourceMapDevToolPlugin } = require("webpack");

module.exports = {
  entry: "./assets/js/main.js",
  output: {
    filename: "main.js",
    path: path.resolve(__dirname, "static/dist"),
  },
  devtool: false,
  plugins: [new SourceMapDevToolPlugin()],
  module: {
    rules: [
      {
        test: /\.s?[ac]ss$/i, // include .css, .scss, .sass
        use: ["style-loader", "css-loader", "postcss-loader", "sass-loader"],
      },
      {
        test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
        use: [
          {
            loader: "file-loader",
            options: {
              name: "[name].[ext]",
              outputPath: "fonts/",
            },
          },
        ],
      },
    ],
  },
};

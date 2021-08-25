const path = require("path");
const { SourceMapDevToolPlugin } = require("webpack");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
  entry: {
    main: "./assets/js/main.js",
    sw: "./assets/js/sw.js",
  },
  output: {
    filename: "[name].js",
    path: path.resolve(__dirname, "static/dist"),
    publicPath: "auto",
  },
  devtool: false,
  plugins: [
    new SourceMapDevToolPlugin({ filename: "sourcemaps/[file].map" }),
    new MiniCssExtractPlugin(),
  ],
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader",
          {
            loader: "postcss-loader",
            options: {
              postcssOptions: {
                plugins: [["autoprefixer", {}]],
              },
            },
          },
        ],
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
};

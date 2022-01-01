module.exports = {
  content: [
    "./templates/**/*.html",
    "./assets/**/*.{js,jsx,ts,tsx,css}",
    "./apps/**/*.py",
    "./config/**/*.py",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          "RubikVariable",
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "Roboto",
          "Oxygen",
          "Ubuntu",
          "Cantarell",
          "Open Sans",
          "Helvetica Neue",
          "sans-serif",
        ],
      },
    },
  },
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/typography")],
};

const colors = require("tailwindcss/colors");

module.exports = {
  content: [
    "./frontend/**/*.{js,jsx,ts,tsx,css}",
    "./templates/**/*.html",
    "./apps/**/*.py",
    "./config/**/*.py",
  ],
  theme: {
    extend: {
      colors: {
        primary: colors.emerald,
        secondary: colors.slate,
      },
      fontFamily: {
        sans: [
          "InterVariable",
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

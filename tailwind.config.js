module.exports = {
  content: ["./backend/**/*.{html,py}", "./assets/**/*.{js,jsx,ts,tsx,css}"],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          "NunitoVariable",
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

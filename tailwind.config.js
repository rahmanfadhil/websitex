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
        sans: ["LexendVariable", "sans-serif"],
      },
    },
  },
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/typography")],
};

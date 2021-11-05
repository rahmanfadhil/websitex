module.exports = {
  mode: "jit",
  purge: [
    "./templates/**/*.html",
    "./assets/**/*.{js,jsx,ts,tsx,css}",
    "./apps/**/*.py",
    "./config/**/*.py",
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      fontFamily: {
        sans: ["LexendVariable", "sans-serif"],
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/typography")],
};

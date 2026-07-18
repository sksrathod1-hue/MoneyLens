/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        // Override all keys to Space Mono as requested
        sans: ['"Space Mono"', "monospace"],
        serif: ['"Space Mono"', "monospace"],
        mono: ['"Space Mono"', "monospace"],
        anton: ['"Anton SC"', "sans-serif"],
      },
    },
  },
  plugins: [],
}

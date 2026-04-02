/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#2a2a4a',
          DEFAULT: '#1a1a2e',
          dark: '#0f0f1c'
        },
        accent: {
          light: '#e8c96b',
          DEFAULT: '#d4af37',
          dark: '#b3901b'
        },
        surface: {
          light: '#ffffff',
          DEFAULT: '#f8fafc',
          dark: '#e2e8f0'
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}

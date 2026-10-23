/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#FAF8F5',
        charcoal: {
          DEFAULT: '#232824',
          light: '#3C443E',
          muted: '#636D65'
        },
        sage: {
          50: '#F4F7F4',
          100: '#E8EFE9',
          200: '#D2DFD4',
          300: '#AFC5B3',
          400: '#87A58E',
          500: '#5E7363',
          600: '#4D5E51',
          700: '#3D4A40',
        },
        warm: {
          card: '#FFFFFF',
          cream: '#F5F2EB',
          border: '#E8E3D8'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      }
    },
  },
  plugins: [],
}

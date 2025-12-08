/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'deftone': ['Deftone', 'Rubik', 'sans-serif'],
        'rubik': ['Rubik', 'sans-serif'],
      },
      colors: {
        gray: '#6a6a7a',
        grayLight: '#cfcde9',
        red: '#f24841',
        redHover: '#fd5c55',
        green: '#44c276',
        greenHover: '#4db175',
        violet: '#7c75d9',
        violetHover: '#8c84ec',
      },
      screens: {
        'xs': { 'max': '350px' },
        'xa': { 'max': '400px' },
        'sm': { 'max': '499px' },
        'md': { 'max': '768px' },
        'lg': { 'max': '1075px' },
        'xl': { 'max': '1225px' },
        '2xl': { 'max': '1475px' },
      },
      animation: {
        'ping': 'ping 1s cubic-bezier(0, 0, 0.2, 1) infinite',
      },
      keyframes: {
        ping: {
          '75%, 100%': {
            transform: 'scale(2)',
            opacity: '0',
          },
        },
      },
    },
  },
  plugins: [],
}

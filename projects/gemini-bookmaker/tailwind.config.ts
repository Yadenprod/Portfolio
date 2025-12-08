
import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: 'class', // Enabling dark mode
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          background: '#1a202c',
          card: '#2d3748',
          text: '#e2e8f0',
          'text-secondary': '#a0aec0',
        }
      }
    },
  },
  plugins: [],
}
export default config

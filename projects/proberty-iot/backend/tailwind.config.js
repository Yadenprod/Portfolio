/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './resources/**/*.blade.php',
    './resources/**/*.js',
    './resources/**/*.vue',
    './resources/**/*.css'
  ],
  theme: {
    colors: {
      transparent: 'transparent',
      current: 'currentColor',
      black: '#000000',
      white: '#ffffff',
      gray: {
        50: '#f9fafb',
        100: '#f3f4f6',
        200: '#e5e7eb',
        300: '#d1d5db',
        400: '#9ca3af',
        500: '#6b7280',
        600: '#4b5563',
        700: '#374151',
        800: '#1f2937',
        900: '#111827',
        950: '#030712'
      },
      azot: {
        50: '#e6f2ff',
        100: '#b3e0ff',
        200: '#80cdff',
        300: '#4db8ff',
        400: '#1aa3ff',
        500: '#0070e0',
        600: '#0057b3',
        700: '#003d80',
        800: '#00244d',
        900: '#000b1a'
      },
      industrial: {
        50: '#f0f4f8',
        100: '#d9e2ec',
        200: '#bcccdc',
        300: '#9fb3c8',
        400: '#829ab1',
        500: '#627d98',
        600: '#486581',
        700: '#334e68',
        800: '#243b53',
        900: '#102a43'
      },
      chemical: {
        50: '#f4f0f8',
        100: '#e2d6f0',
        200: '#c7b3e6',
        300: '#ad8fdc',
        400: '#936bd2',
        500: '#7a4ebf',
        600: '#633ba6',
        700: '#4c2d8c',
        800: '#351f5c',
        900: '#1e1133'
      }
    },
    extend: {
      fontFamily: {
        'industrial': ['Inter', 'system-ui', 'sans-serif'],
        'technical': ['Roboto Mono', 'monospace']
      },
      boxShadow: {
        'industrial-soft': '0 4px 6px -1px rgba(0, 112, 224, 0.1), 0 2px 4px -1px rgba(0, 112, 224, 0.06)',
        'industrial-medium': '0 10px 15px -3px rgba(0, 112, 224, 0.1), 0 4px 6px -2px rgba(0, 112, 224, 0.05)',
        'industrial-hard': '0 20px 25px -5px rgba(0, 112, 224, 0.1), 0 10px 10px -5px rgba(0, 112, 224, 0.04)',
        'glow-azot': '0 0 16px 4px #0070e0',
        'glow-chemical': '0 0 16px 4px #7a4ebf',
        'glow-industrial': '0 0 16px 4px #627d98',
      },
      borderRadius: {
        'industrial-sm': '0.375rem',
        'industrial-md': '0.75rem',
        'industrial-lg': '1rem',
        'industrial-xl': '1.5rem',
        'wow': '2.5rem',
      },
      backgroundImage: theme => ({
        'azot-gradient': 'linear-gradient(120deg, #0070e0 0%, #7a4ebf 100%)',
        'industrial-gradient': 'linear-gradient(90deg, #f0f4f8 0%, #627d98 100%)',
        'chemical-gradient': 'linear-gradient(135deg, #7a4ebf 0%, #e6f2ff 100%)',
        'azot-pattern': "url('/images/lazot.png')",
        'dots': 'radial-gradient(circle, #0070e0 1px, transparent 1px)',
      }),
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
        'slide-up': 'slideInUp 0.5s ease-out',
        'slide-right': 'slideInRight 0.5s ease-out',
        'scale-in': 'scaleIn 0.4s ease-out',
        'wow-bounce': 'bounce 1.2s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideInUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideInRight: {
          '0%': { opacity: '0', transform: 'translateX(20px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.9)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        bounce: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10%)' },
        },
      },
    }
  },
  plugins: []
};

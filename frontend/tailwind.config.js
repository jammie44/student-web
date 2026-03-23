/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./app/**/*.{js,jsx}', './components/**/*.{js,jsx}', './lib/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-syne)', 'var(--font-dm)', 'sans-serif'],
        display: ['var(--font-syne)', 'sans-serif'],
      },
      colors: {
        ink: { 50:'#f4f3f0',100:'#e8e6e1',200:'#d1cec5',300:'#b5b0a4',400:'#96907f',500:'#7c7566',600:'#655e52',700:'#524d43',800:'#433f37',900:'#39352f',950:'#1e1c18' },
        gold: { 300:'#fcd34d',400:'#fbbf24',500:'#f59e0b',600:'#d97706' },
        jade: { 400:'#4ade80',500:'#22c55e',600:'#16a34a' },
        coral: { 400:'#f87171',500:'#ef4444' },
      },
      keyframes: {
        fadeUp:  { from:{ opacity:'0', transform:'translateY(16px)' }, to:{ opacity:'1', transform:'translateY(0)' } },
        fadeIn:  { from:{ opacity:'0' }, to:{ opacity:'1' } },
        shimmer: { from:{ backgroundPosition:'-200% 0' }, to:{ backgroundPosition:'200% 0' } },
        pulseSoft: { '0%,100%':{ opacity:'1' }, '50%':{ opacity:'0.5' } },
      },
      animation: {
        'fade-up':    'fadeUp 0.45s ease forwards',
        'fade-in':    'fadeIn 0.3s ease forwards',
        'shimmer':    'shimmer 1.5s linear infinite',
        'pulse-soft': 'pulseSoft 1.4s ease-in-out infinite',
      },
    },
  },
  plugins: [],
};

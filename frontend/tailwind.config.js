/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./app/**/*.{js,jsx}', './components/**/*.{js,jsx}', './lib/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-dm)', 'DM Sans', 'sans-serif'],
        display: ['var(--font-syne)', 'Syne', 'sans-serif'],
      },
      colors: {
        space: { DEFAULT: '#020408', 2: '#060d18', 3: '#0a1628', 4: '#0f1e38' },
        accent: { DEFAULT: '#4f8ef7', 2: '#7c3aed', dim: '#1e3a5f' },
        gold:  { DEFAULT: '#f59e0b', light: '#fbbf24', dim: '#78350f' },
        jade:  { DEFAULT: '#10b981', light: '#34d399', dim: '#064e3b' },
        coral: { DEFAULT: '#ef4444', light: '#f87171', dim: '#7f1d1d' },
        ink:   { 100: '#e2e8f0', 200: '#cbd5e1', 300: '#94a3b8', 400: '#64748b', 500: '#475569', 600: '#334155', 700: '#1e293b', 800: '#0f172a' },
      },
      keyframes: {
        fadeUp:  { from: { opacity: '0', transform: 'translateY(20px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
        fadeIn:  { from: { opacity: '0' }, to: { opacity: '1' } },
        slideIn: { from: { opacity: '0', transform: 'translateX(-16px)' }, to: { opacity: '1', transform: 'translateX(0)' } },
        pulse:   { '0%,100%': { opacity: '1' }, '50%': { opacity: '0.4' } },
        shimmer: { from: { backgroundPosition: '-200% 0' }, to: { backgroundPosition: '200% 0' } },
        float:   { '0%,100%': { transform: 'translateY(0)' }, '50%': { transform: 'translateY(-8px)' } },
      },
      animation: {
        'fade-up':  'fadeUp 0.5s ease forwards',
        'fade-in':  'fadeIn 0.3s ease forwards',
        'slide-in': 'slideIn 0.3s ease forwards',
        'float':    'float 4s ease-in-out infinite',
        'pulse-soft': 'pulse 1.4s ease-in-out infinite',
        'shimmer':  'shimmer 1.8s linear infinite',
      },
    },
  },
  plugins: [],
};

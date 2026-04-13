/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./app/**/*.{js,jsx}','./components/**/*.{js,jsx}','./lib/**/*.{js,jsx}'],
  theme: { extend: {
    fontFamily: { sans: ['DM Sans','sans-serif'], display: ['Syne','sans-serif'] },
    animation: {
      'fade-up':'fadeUp 0.5s ease forwards',
      'fade-in':'fadeIn 0.3s ease forwards',
      'float':'float 4s ease-in-out infinite',
    },
    keyframes: {
      fadeUp:{ from:{opacity:'0',transform:'translateY(20px)'}, to:{opacity:'1',transform:'translateY(0)'} },
      fadeIn:{ from:{opacity:'0'}, to:{opacity:'1'} },
      float:{ '0%,100%':{transform:'translateY(0)'},'50%':{transform:'translateY(-8px)'} },
    },
  }},
  plugins: [],
};

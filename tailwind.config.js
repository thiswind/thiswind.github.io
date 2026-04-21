/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './_layouts/**/*.html',
    './_includes/**/*.html',
    './_posts/**/*.markdown',
    './_posts/**/*.md',
    './*.html',
    './*.markdown',
    './*.md'
  ],
  theme: {
    extend: {
      colors: {
        // 主色调：伊斯兰绿 - 中东地区最受欢迎的颜色，象征和平、生命
        primary: {
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#86efac',
          400: '#4ade80', // 主色 - 翠绿
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d',
          800: '#166534',
          900: '#14532d',
        },
        // 中性色：沙漠沙色 - 中东地域感，温暖不刺眼
        sand: {
          50: '#fefcf3',
          100: '#fdf8e1',  // 浅色背景
          200: '#f9efb6',
          300: '#f3e387',
          400: '#e9d057',
          500: '#dcb82e',
          600: '#c29a22',
          700: '#a1781e',
          800: '#85611f',
          900: '#70511e',
          950: '#1f1704', // 深色背景 - 深褐色，比纯黑更温暖
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        ar: ['"Noto Naskh Arabic"', '"Tajawal"', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
  future: {
    hoverOnlyWhenSupported: true,
  },
}

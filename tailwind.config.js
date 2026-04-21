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
        // 主色调：温暖的沙漠金（符合中阿文化的感觉）
        primary: {
          50: '#fefce8',
          100: '#fdf9c3',
          200: '#fcf289',
          300: '#f9e547',
          400: '#f2d00f', // 主色
          500: '#dbb707',
          600: '#bb9206',
          700: '#986b0a',
          800: '#7d5510',
          900: '#6b4513',
        },
        // 中性色：柔和的深灰（比纯黑更有温度）
        sand: {
          50: '#fbf8f4',
          100: '#f5efe6',
          200: '#e8ddd0',
          300: '#d7c7b3',
          400: '#c4ab91',
          500: '#b09072',
          600: '#9a755d',
          700: '#7f5e4d',
          800: '#684e42',
          900: '#574238',
          950: '#2f241f', // 深色背景
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        ar: ['"Noto Naskh Arabic"', '"Tajawal"', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
  // 移动端优先：默认 sm 就是手机尺寸
  future: {
    hoverOnlyWhenSupported: true,
  },
}

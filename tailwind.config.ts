import type { Config } from 'tailwindcss';

export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],

  theme: {
    extend: {
      colors: {
        win: '#4B7AD8',
        loss: '#DC5F61'
      }
    }
  },

  plugins: []
} satisfies Config;

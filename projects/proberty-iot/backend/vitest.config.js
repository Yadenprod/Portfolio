import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'happy-dom',
    globals: true,
    include: ['resources/js/**/*.spec.js', 'resources/js/**/*.test.js'],
    coverage: {
      reporter: ['text', 'html'],
    },
  },
});

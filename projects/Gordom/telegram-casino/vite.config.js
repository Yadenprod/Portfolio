import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.svg', 'images/icon-192.svg', 'images/icon-512.svg'],
      manifest: {
        name: 'TREASURE Casino',
        short_name: 'TREASURE',
        description: 'Современное казино в Telegram с играми Dice, Wheel, Mines, Slots',
        start_url: '/',
        display: 'standalone',
        background_color: '#202024',
        theme_color: '#7c75d9',
        orientation: 'portrait-primary',
        scope: '/',
        lang: 'ru',
        dir: 'ltr',
        categories: ['games', 'entertainment'],
        icons: [
          {
            src: '/images/icon-192.svg',
            sizes: '192x192',
            type: 'image/svg+xml',
            purpose: 'maskable any'
          },
          {
            src: '/images/icon-512.svg',
            sizes: '512x512',
            type: 'image/svg+xml',
            purpose: 'maskable any'
          }
        ]
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/api\./,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              cacheableResponse: {
                statuses: [0, 200]
              }
            }
          },
          {
            urlPattern: /\.(png|jpg|jpeg|gif|svg)$/,
            handler: 'CacheFirst',
            options: {
              cacheName: 'images-cache',
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 30 * 24 * 60 * 60 // 30 days
              }
            }
          }
        ]
      }
    })
  ],
  server: {
    port: 3000,
    host: '0.0.0.0'
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia'],
          telegram: ['@twa-dev/sdk'],
          ui: ['tailwindcss']
        }
      }
    }
  },
  resolve: {
    alias: {
      '@': '/src'
    }
  }
})
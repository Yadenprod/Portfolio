import { defineConfig, optimizeDeps } from 'vite';
import laravel from 'laravel-vite-plugin';
import vue from '@vitejs/plugin-vue2'
import svgLoader from "vite-svg-loader";

export default defineConfig({
    optimizeDeps: {
        include: ["resources/frontend/main.js"]
    },
    plugins: [
        laravel({
            input: ['resources/css/app.css', 'resources/frontend/main.js'],
            refresh: true,
        }),
        vue(),
        svgLoader(),
    ],
    build: {
        outDir: 'public/',
        assetsDir: 'assets/',
        cssCodeSplit: false,
        rollupOptions: {
            external: [
                /^symbols\.svg*/,
                /\/images\/[a-zA-Z]*.(png|jpg|svg)*/
            ],
        }
    }
});

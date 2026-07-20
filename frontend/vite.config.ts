import { resolve } from 'node:path'
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        leaflet: resolve(__dirname, 'leaflet.html'),
        maplibre: resolve(__dirname, 'maplibre.html'),
        cesium: resolve(__dirname, 'cesium.html'),
      },
    },
  },
})

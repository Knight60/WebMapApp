import { resolve } from 'node:path'
import { cp, rm } from 'node:fs/promises'
import { defineConfig, type Plugin } from 'vite'

// Where the built frontend is published for FastAPI to serve as its web root.
const BACKEND_WEB_ROOT = resolve(__dirname, '../backend/static')

/**
 * After every `vite build`, mirror dist/ into the backend so FastAPI serves
 * the current build. The target is wiped first so removed/renamed hashed
 * assets don't linger.
 */
function publishToBackend(): Plugin {
  return {
    name: 'publish-to-backend',
    apply: 'build',
    async closeBundle() {
      const dist = resolve(__dirname, 'dist')
      await rm(BACKEND_WEB_ROOT, { recursive: true, force: true })
      await cp(dist, BACKEND_WEB_ROOT, { recursive: true })
      console.log(`\n[publish-to-backend] dist/ -> ${BACKEND_WEB_ROOT}`)
    },
  }
}

export default defineConfig({
  plugins: [publishToBackend()],
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        leaflet: resolve(__dirname, 'leaflet.html'),
        maplibre: resolve(__dirname, 'maplibre.html'),
        cesium: resolve(__dirname, 'cesium.html'),
        capstone: resolve(__dirname, 'capstone.html'),
      },
    },
  },
})

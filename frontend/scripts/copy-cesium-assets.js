import { cpSync, existsSync, rmSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const src = resolve(root, 'node_modules/cesium/Build/CesiumUnminified')
const dest = resolve(root, 'public/cesium')

if (!existsSync(src)) {
  console.error('[copy-cesium-assets] Cesium build not found; run npm install first.')
  process.exit(0)
}

rmSync(dest, { recursive: true, force: true })
for (const dir of ['Assets', 'ThirdParty', 'Workers', 'Widgets']) {
  cpSync(resolve(src, dir), resolve(dest, dir), { recursive: true })
}
console.log('[copy-cesium-assets] Copied Cesium runtime assets to public/cesium')

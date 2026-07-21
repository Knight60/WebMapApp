import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

interface ProvinceProps {
  PROV_CODE: string
  PROV_NAMT: string // Thai name
  PROV_NAME: string // English name
}

const map = L.map('app').setView([13.7563, 100.5018], 6)

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors',
  maxZoom: 19,
}).addTo(map)

const baseStyle: L.PathOptions = {
  color: '#2563eb',
  weight: 1,
  fillColor: '#3b82f6',
  fillOpacity: 0.08,
}

const highlightStyle: L.PathOptions = {
  color: '#dc2626',
  weight: 2.5,
  fillColor: '#ef4444',
  fillOpacity: 0.25,
}

// Keep a reference to each province's rendered layer, keyed by province code.
const layersByCode = new Map<string, L.Path>()
let selectedCode: string | null = null

function selectProvince(code: string) {
  const layer = layersByCode.get(code)
  if (!layer) return

  if (selectedCode && layersByCode.has(selectedCode)) {
    layersByCode.get(selectedCode)!.setStyle(baseStyle)
  }
  selectedCode = code

  layer.setStyle(highlightStyle)
  layer.bringToFront()
  map.fitBounds((layer as unknown as L.Polygon).getBounds(), { padding: [20, 20] })
}

// Dropdown control (top-right) to pick a province.
const ProvincePicker = L.Control.extend({
  options: { position: 'topright' as L.ControlPosition },
  onAdd() {
    const container = L.DomUtil.create('div', 'province-picker leaflet-bar')
    container.innerHTML = `
      <label for="province-select">จังหวัด / Province</label>
      <select id="province-select">
        <option value="">— เลือกจังหวัด —</option>
      </select>
    `
    // Prevent map drag/scroll when interacting with the control.
    L.DomEvent.disableClickPropagation(container)
    L.DomEvent.disableScrollPropagation(container)
    return container
  },
})
map.addControl(new ProvincePicker())

const select = document.getElementById('province-select') as HTMLSelectElement
select.addEventListener('change', () => {
  if (select.value) selectProvince(select.value)
})

async function loadProvinces() {
  // BASE_URL resolves to the deploy base ('/WebMapApp/' on GitHub Pages,
  // '/' when served from the backend) so the asset is found in both cases.
  const res = await fetch(`${import.meta.env.BASE_URL}data/provinces.geojson`)
  if (!res.ok) throw new Error(`Failed to load provinces: ${res.status}`)
  const geojson = (await res.json()) as GeoJSON.FeatureCollection

  L.geoJSON(geojson, {
    style: () => baseStyle,
    onEachFeature: (feature, layer) => {
      const props = feature.properties as ProvinceProps
      layersByCode.set(props.PROV_CODE, layer as L.Path)
      layer.bindTooltip(`${props.PROV_NAMT} (${props.PROV_NAME})`, { sticky: true })
      layer.on('click', () => {
        select.value = props.PROV_CODE
        selectProvince(props.PROV_CODE)
      })
    },
  }).addTo(map)

  // Populate the dropdown, sorted by Thai name.
  const provinces = geojson.features
    .map((f) => f.properties as ProvinceProps)
    .sort((a, b) => a.PROV_NAMT.localeCompare(b.PROV_NAMT, 'th'))

  const fragment = document.createDocumentFragment()
  for (const p of provinces) {
    const option = document.createElement('option')
    option.value = p.PROV_CODE
    option.textContent = `${p.PROV_NAMT} (${p.PROV_NAME})`
    fragment.appendChild(option)
  }
  select.appendChild(fragment)
}

loadProvinces().catch((err) => {
  console.error(err)
  alert('ไม่สามารถโหลดข้อมูลจังหวัดได้')
})

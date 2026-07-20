import 'maplibre-gl/dist/maplibre-gl.css'
import maplibregl from 'maplibre-gl'

const map = new maplibregl.Map({
  container: 'app',
  style: 'https://demotiles.maplibre.org/style.json',
  center: [100.5018, 13.7563],
  zoom: 6,
})

map.addControl(new maplibregl.NavigationControl())

new maplibregl.Marker()
  .setLngLat([100.5018, 13.7563])
  .setPopup(new maplibregl.Popup().setText('Bangkok, Thailand'))
  .addTo(map)

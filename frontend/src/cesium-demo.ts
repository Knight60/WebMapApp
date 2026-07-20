import 'cesium/Build/Cesium/Widgets/widgets.css'
import * as Cesium from 'cesium'

const viewer = new Cesium.Viewer('app', {
  baseLayer: new Cesium.ImageryLayer(
    new Cesium.OpenStreetMapImageryProvider({
      url: 'https://tile.openstreetmap.org/',
    }),
  ),
  baseLayerPicker: false,
  geocoder: false,
  timeline: false,
  animation: false,
})

viewer.camera.flyTo({
  destination: Cesium.Cartesian3.fromDegrees(100.5018, 13.7563, 1_000_000),
})

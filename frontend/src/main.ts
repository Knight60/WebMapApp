import './style.css'

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
<section id="center">
  <div>
    <h1>Web Map API Demos</h1>
    <p>Pick a library to see a basic example map centered on Bangkok.</p>
  </div>
  <ul class="demo-links">
    <li><a href="/leaflet.html">Leaflet</a></li>
    <li><a href="/maplibre.html">MapLibre GL JS</a></li>
    <li><a href="/cesium.html">CesiumJS</a></li>
  </ul>
</section>
`

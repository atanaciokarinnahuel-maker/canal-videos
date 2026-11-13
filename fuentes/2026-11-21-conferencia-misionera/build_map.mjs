// Genera mapdata.js: paises del mundo proyectados (Natural Earth) a un espacio de 2000x1040.
// Uso: npm i d3-geo topojson-client world-atlas && node build_map.mjs <salida>
import {geoNaturalEarth1, geoPath} from 'd3-geo';
import {feature} from 'topojson-client';
import fs from 'fs';
import {createRequire} from 'module';
const require = createRequire(import.meta.url);
const topo = require('world-atlas/countries-50m.json');
const proj = geoNaturalEarth1().scale(365.6).translate([1000, 520]).precision(0.05);
const path = geoPath(proj).digits(1);
const out = [];
for (const f of feature(topo, topo.objects.countries).features) {
  if (f.id === '010') continue;            // sin Antartida
  const d = path(f); if (!d) continue;
  const b = path.bounds(f).flat().map(v => +v.toFixed(1));
  out.push({id: f.id, n: f.properties.name, b, d});
}
fs.writeFileSync(process.argv[2], 'const MAP=' + JSON.stringify(out) + ';\n');
console.log(out.length, 'paises', (fs.statSync(process.argv[2]).size / 1e6).toFixed(2), 'MB');
for (const id of ['862', '608', '356', '643', '800', '032']) { const c = out.find(o => o.id === id); console.log(id, c.n, c.b.join(' ')); }
for (const [n, lon, lat] of [['Maimara', -65.41, -23.62], ['Caracas', -66.9, 10.49]]) console.log(n, proj([lon, lat]).map(v => v.toFixed(1)).join(' '));

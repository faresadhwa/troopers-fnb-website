#!/usr/bin/env node
/* Step 1 of 2 for the Singapore map: joins Singapore's 55 planning areas into the six areas Troopers uses.

   Troopers counts six areas (Central, East, North, North East, South, West). The government map has only five
   regions, with no South, so South is built here from the southern planning areas, taken out of Central.
   >>> The South list below is OUR choice, not an official one. Change SOUTH if Troopers means something else. <<<

   Source: URA Master Plan 2014 planning areas (Singapore Open Data Licence, data.gov.sg), as published at
   https://raw.githubusercontent.com/yinshanyang/singapore/master/maps/2-planning-area.geojson

   Needs topojson-server and topojson-client (npm i topojson-server topojson-client somewhere, then point NODE_PATH at it):
     NODE_PATH=/path/to/node_modules node tools/dissolve-sg-areas.cjs 2-planning-area.geojson /tmp/sg-six-areas.geojson
   Step 2:  python3 tools/make-sg-regions.py /tmp/sg-six-areas.geojson
*/
const fs = require('fs');
const { topology } = require('topojson-server');
const { merge } = require('topojson-client');

const SOUTH = ['BUKIT MERAH', 'QUEENSTOWN', 'SOUTHERN ISLANDS', 'MARINA SOUTH', 'STRAITS VIEW'];
const GROUPS = {
  'South': SOUTH,
  'Central': ['BISHAN', 'BUKIT TIMAH', 'DOWNTOWN CORE', 'GEYLANG', 'KALLANG', 'MARINA EAST', 'MARINE PARADE', 'MUSEUM',
              'NEWTON', 'NOVENA', 'ORCHARD', 'OUTRAM', 'RIVER VALLEY', 'ROCHOR', 'SINGAPORE RIVER', 'TANGLIN', 'TOA PAYOH'],
  'East': ['BEDOK', 'CHANGI', 'CHANGI BAY', 'PAYA LEBAR', 'PASIR RIS', 'TAMPINES'],
  'North': ['CENTRAL WATER CATCHMENT', 'LIM CHU KANG', 'MANDAI', 'SEMBAWANG', 'SIMPANG', 'SUNGEI KADUT', 'WOODLANDS', 'YISHUN'],
  'North East': ['ANG MO KIO', 'HOUGANG', 'NORTH-EASTERN ISLANDS', 'PUNGGOL', 'SELETAR', 'SENGKANG', 'SERANGOON'],
  'West': ['BOON LAY', 'BUKIT BATOK', 'BUKIT PANJANG', 'CHOA CHU KANG', 'CLEMENTI', 'JURONG EAST', 'JURONG WEST', 'PIONEER',
           'TENGAH', 'TUAS', 'WESTERN ISLANDS', 'WESTERN WATER CATCHMENT'],
};

const [, , src, out] = process.argv;
const gj = JSON.parse(fs.readFileSync(src, 'utf8'));
const which = {};
Object.keys(GROUPS).forEach((g) => GROUPS[g].forEach((n) => { which[n] = g; }));
const missing = gj.features.map((f) => f.properties.name).filter((n) => !which[n]);
if (missing.length) throw new Error('planning areas without a group: ' + missing.join(', '));

const topo = topology({ pa: gj });
const geoms = topo.objects.pa.geometries;
const features = Object.keys(GROUPS).map((g) => ({
  type: 'Feature',
  properties: { name: g },
  geometry: merge(topo, geoms.filter((o) => which[o.properties.name] === g)),
}));
fs.writeFileSync(out, JSON.stringify({ type: 'FeatureCollection', features }));
features.forEach((f) => console.log(f.properties.name, 'polygons:', f.geometry.coordinates.length));
console.log('wrote', out);

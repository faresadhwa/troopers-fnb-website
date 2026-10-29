# TROOPERS — F&B Staffing page

Static HTML. No build step. Content follows the MyBurgerLab business site; the look follows the TROOPERS Branding Guideline 2026, B2B "Clean White Gradient" (white page, navy headlines with an orange key phrase and a short orange bar, pill-shaped orange buttons, rounded-lines motif).

## Files

```
index.html                    the whole page: one <style> block, the HTML, then small scripts
assets/                       photos, client logos and map data referenced by index.html
assets/world-dots.json        dotted land for the coverage globe (generated, see below)
assets/malaysia-states.geojson  state outlines for the coverage map
assets/singapore-regions.geojson  the six Singapore area outlines (generated, see below)
tools/make-world-dots.py      rebuilds world-dots.json (needs numpy)
tools/dissolve-sg-areas.cjs   step 1: joins Singapore's 55 planning areas into the six Troopers areas
tools/make-sg-regions.py      step 2: thins them into assets/singapore-regions.geojson
assets/favicon-*.png, apple-touch-icon.png  browser-tab icon: the official TROOPERS "T" mark (from troopers.com.my) on a white tile
states-map.html               the old stand-alone map page. No longer linked; the map now lives in index.html
```

## Open it

Open `index.html` in a browser, or serve the folder (for example `python3 -m http.server 8820`). The coverage map loads JSON files, so it needs a server, not a double-click on the file.

## Editing notes

- **Rates are hidden on purpose.** The rate table and the cost calculator sit inside one closed block (`details.rates`, button "Show rates") because the rates can change. No rate numbers appear anywhere else on the page. When rates change, edit the rows in `#cost` and the defaults in the calculator script at the bottom of `index.html` (service fee `rp_sf`, SST 8%).
- **Product screens** (`assets/screen-*.webp`) are sample screens with dummy people and data, made for the web. The ten feature buttons in `#platform` switch between them.
- **Topic blocks** are full-width white-to-grey gradients; every second block runs the other way (ids listed in the CSS next to `.sec::before`) so the joins match. New topic = add a `<section class="wrap sec">` and, if it is an even block, add its id to that list.

- Colours are CSS variables at the top of the `<style>` block (`--navy`, `--orange`, `--cream`, and so on). Font is Poppins from Google Fonts.
- The page is English only (the Malay version and language switch were removed on purpose). Keep the wording plain: short sentences, no industry jargon, and never promise same-day staffing (job posts are checked within 3 working days).
- **Coverage numbers** live in one place: the `window.COVERAGE` block near the bottom of `index.html`. Registered and approved talents, pulled 23 Oct 2026 from the Troopers MY and SG connectors. Update the numbers and the "as of" date in the note under the cards. State and area figures are "talents who chose this place as somewhere they will work", so they overlap and add up to more than the totals. Kuala Lumpur, Putrajaya and Labuan are shown as one Federal Territories figure on purpose, because the three are almost always chosen together.
- **Coverage globe**: intro spin, then three views: South-East Asia close-up ("Malaysia"), a zoomed Singapore map ("Singapore", also reached by clicking the little Singapore inset) and the whole earth ("World"). Zoom with the + / − buttons, Ctrl or ⌘ + scroll, or a pinch. Land is dots from `assets/world-dots.json`. If you change `world-land.geojson` or `malaysia-states.geojson`, run `python3 tools/make-world-dots.py` from this folder.
- **Singapore outlines**: URA Master Plan 2014 planning areas via data.gov.sg (Singapore Open Data Licence, credited in the note under the cards), joined into Troopers' six areas. The government map has only five regions, so **South is our own cut**: Bukit Merah, Queenstown, Marina South, Straits View and the Southern Islands (Sentosa and friends) are taken out of Central. To change what counts as South, edit the `SOUTH` list in `tools/dissolve-sg-areas.cjs`, then rebuild in two steps (commands are at the top of each tool: `dissolve-sg-areas.cjs` needs `npm i topojson-server topojson-client`, then `make-sg-regions.py`). Label positions are `SG_AT` in the page script.
- Marquees (client logos, photo band) have two identical sets. If you add or remove an item, do it in **both** sets or the loop will jump.
- Logos: `logo-troopers.png` and `logo-chagee.png` are the full-colour versions for a light background. The `*-dark.png` and `logo-troopers-white.png` files are left over from the old dark page and are not used now.
- d3 is pinned to 7.9.0 with an integrity hash. If you change the version, update the hash too.
- Every call to action links to `https://troopersapp.com/employer-signup`.

## Still to confirm before publishing

- `role-*.png` and `case-*.png` photos are AI-generated placeholders, not real shoots.
- Pricing copy (RM 25 per completed shift) follows troopers.com.my/partner/pricing-plans as of the export date. Re-check before going live.
- Coverage numbers count all talents on the platform, not F&B only.

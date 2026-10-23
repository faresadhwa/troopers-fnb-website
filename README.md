# TROOPERS — F&B Staffing page

Static HTML. No build step. Look follows the MyBurgerLab business deck (cream page, navy text, orange for emphasis).

## Files

```
index.html                    the whole page: one <style> block, the HTML, then small scripts
assets/                       photos, client logos and map data referenced by index.html
assets/world-dots.json        dotted land for the coverage globe (generated, see below)
assets/malaysia-states.geojson  state outlines for the coverage map
tools/make-world-dots.py      rebuilds world-dots.json (needs numpy)
states-map.html               the old stand-alone map page. No longer linked; the map now lives in index.html
```

## Open it

Open `index.html` in a browser, or serve the folder (for example `python3 -m http.server 8820`). The coverage map loads JSON files, so it needs a server, not a double-click on the file.

## Editing notes

- Colours are CSS variables at the top of the `<style>` block (`--navy`, `--orange`, `--cream`, and so on). Font is Poppins from Google Fonts.
- Every English string that has a Malay version carries a `data-ms="..."` attribute. Add the Malay text there when you add or change copy.
- **Coverage numbers** live in one place: the `window.COVERAGE` block near the bottom of `index.html`. Registered and approved talents, pulled 23 Oct 2026 from the Troopers MY and SG connectors. Update the numbers and the "as of" date in the note under the cards (English and `data-ms`). State and area figures are "talents who chose this place as somewhere they will work", so they overlap and add up to more than the totals. Kuala Lumpur, Putrajaya and Labuan are shown as one Federal Territories figure on purpose, because the three are almost always chosen together.
- **Coverage globe**: intro spin, then a South-East Asia close-up ("Region") and a whole-earth view ("Globe"). Land is dots from `assets/world-dots.json`. If you change `world-land.geojson` or `malaysia-states.geojson`, run `python3 tools/make-world-dots.py` from this folder.
- Marquees (client logos, photo band) have two identical sets. If you add or remove an item, do it in **both** sets or the loop will jump.
- Logos: `logo-troopers.png` and `logo-chagee.png` are the full-colour versions for a light background. The `*-dark.png` and `logo-troopers-white.png` files are left over from the old dark page and are not used now.
- d3 is pinned to 7.9.0 with an integrity hash. If you change the version, update the hash too.
- Every call to action links to `https://troopersapp.com/employer-signup`.

## Still to confirm before publishing

- `role-*.png` and `case-*.png` photos are AI-generated placeholders, not real shoots.
- Pricing copy (RM 25 per completed shift) follows troopers.com.my/partner/pricing-plans as of the export date. Re-check before going live.
- Coverage numbers count all talents on the platform, not F&B only.

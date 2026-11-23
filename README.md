# TROOPERS — F&B Staffing page

Static HTML. No build step. A short landing page for F&B owners in Malaysia, headline "Part-timers who actually turn up." The look follows the TROOPERS Branding Guideline 2026, B2B "Clean White Gradient" (white page, navy headlines with an orange key phrase and a short orange bar, pill-shaped orange buttons, rounded-lines motif). Motion uses GSAP.

## Files

```
index.html                    the owner page: one <style> block, the HTML, then small scripts
for-chains.html               the older, longer page for chains and bigger teams (Gig Workers Act, workforce models,
                              product features, welfare, case studies). Linked only from the footer of index.html
assets/                       photos, client logos, product screens and map data
assets/world-dots.json        dotted land for the coverage globe (generated, see below)
assets/malaysia-states.geojson  state outlines for the coverage map
assets/singapore-regions.geojson  the six Singapore area outlines (generated, see below)
tools/make-world-dots.py      rebuilds world-dots.json (needs numpy)
tools/dissolve-sg-areas.cjs   step 1: joins Singapore's 55 planning areas into the six Troopers areas
tools/make-sg-regions.py      step 2: thins them into assets/singapore-regions.geojson
assets/favicon-*.png, apple-touch-icon.png  browser-tab icon: the official TROOPERS "T" mark on a white tile
states-map.html               the old stand-alone map page. No longer linked; the map now lives in index.html
```

## Open it

Open the folder with a small server (for example `python3 -I -m http.server 8820 --bind 127.0.0.1`), then go to http://localhost:8820. The coverage map loads JSON files, so it needs a server, not a double-click on the file.

## What is on the page (in order)

1. **Hero**: headline, one short paragraph, "Post your first shift", and a CSS phone that loops: post a shift, "checked by our team", part-timers apply, you hire.
2. **Logo strip**: food, drink and hotel brands only.
3. **Three staffing headaches** (`#why`): no-shows and ratings, contracts / pay slips / payments, food handler rules.
4. **How it works** (`#how`): three steps. On wide screens a second phone stays in view and changes as you scroll past each step; on phones it loops through the three scenes.
5. **Part-timers near you** (`#coverage`): pick a crew, how many people and where, and see how many approved part-timers are there. Then the coverage map, and a closed box with the numbers for every state.
6. **Costs** (`#cost`): the rates, hidden behind a button.
7. **Questions** (`#faq`), a final call to action, and the footer.

## Editing notes

- **Plain words.** Short sentences, no industry jargon ("part-timers", not "talents"). Never promise same-day staffing: a shift is checked by our team within 3 working days.
- **Rates are hidden on purpose.** The rate table and the cost calculator sit inside one closed block (`details.rates`, button "Show rates") because the rates can change. No rate numbers appear anywhere else on the page. When rates change, edit the rows in `#cost` and the defaults in the calculator script near the bottom of `index.html` (service fee `rp_sf`, SST 8%).
- **Phones show examples.** The people, names, ratings and shift details in both phones are made up, and the page says so ("Example screen. The names are made up."). The faces are the AI placeholder photos.
- **Motion (GSAP 3.13.0 + ScrollTrigger + SplitText)** is loaded from jsDelivr with integrity hashes at the end of `index.html`; if you change the version, update the hashes too. The motion code is the last `<script>` block, and its CSS is the last block in `<style>` ("GSAP motion layer"). It covers the hero intro, the card and icon reveals, the scroll-controlled phone in How it works, and the rolling number in the finder. Everything is switched off for people whose device asks for reduced motion, and the page still works if GSAP fails to load. The gap between steps in How it works is `--gap` on `.how-steps`.
- **Topic blocks** are full-width white-to-grey gradients; every second block runs the other way (`#how` and `#cost` are listed in the CSS block "GSAP motion layer" and next to `.sec::before`) so the joins match.
- **Coverage numbers** live in one place: the `window.COVERAGE` block near the bottom of `index.html`. They feed the finder, the map and the numbers box. Registered and approved talents, pulled 23 Oct 2026 from the Troopers MY and SG connectors. Update the numbers and the "as of" date (in the finder's small print and in the note inside the numbers box). State and area figures are "part-timers who chose this place as somewhere they will work", so they overlap and add up to more than the totals. Kuala Lumpur, Putrajaya and Labuan are shown as one Federal Territories figure on purpose.
- **Coverage globe**: intro spin, then three views: South-East Asia close-up ("Malaysia"), a zoomed Singapore map ("Singapore") and the whole earth ("World"). Zoom with the + / − buttons, Ctrl or ⌘ + scroll, or a pinch. It starts when the map itself scrolls into view. Land is dots from `assets/world-dots.json`. If you change `world-land.geojson` or `malaysia-states.geojson`, run `python3 tools/make-world-dots.py` from this folder.
- **Singapore outlines**: URA Master Plan 2014 planning areas via data.gov.sg (Singapore Open Data Licence, credited in the numbers box), joined into Troopers' six areas. The government map has only five regions, so **South is our own cut**: Bukit Merah, Queenstown, Marina South, Straits View and the Southern Islands are taken out of Central. To change what counts as South, edit the `SOUTH` list in `tools/dissolve-sg-areas.cjs`, then rebuild in two steps (commands are at the top of each tool; `dissolve-sg-areas.cjs` needs `npm i topojson-server topojson-client`, then `make-sg-regions.py`). Label positions are `SG_AT` in the page script.
- **Logo strip** has two identical sets. If you add or remove a logo, do it in **both** sets or the loop will jump.
- Colours are CSS variables at the top of the `<style>` block (`--navy`, `--orange`, and so on). Font is Poppins from Google Fonts.
- d3 is pinned to 7.9.0 with an integrity hash. If you change the version, update the hash too.
- Every sign-up button links to `https://troopersapp.com/employer-signup`.
- `for-chains.html` is the previous full page and still carries its own copy of the old wording (including "you set the pay rate" and managed-service claims). Check it before sending anyone there.

## Still to confirm before publishing

- **No-show answer.** The headline promises part-timers turn up, but the Questions section has no answer to "what if someone does not?". Get the real policy from Product before adding one.
- **Claims for self-serve owners**: "we handle the contracts, pay slips and payments" and "ratings from past shifts".
- **Pay rate wording**: the page says you set the pay rate, while the rate table is fixed.
- **GSAP licence**: confirm at https://gsap.com/standard-license that this use is covered.
- `role-*.png` and `case-*.png` photos are AI-generated placeholders, not real shoots.
- Coverage numbers count all talents on the platform, not F&B only, and are as of 23 Oct 2026.
- Not tested on a real phone, Safari or Firefox.

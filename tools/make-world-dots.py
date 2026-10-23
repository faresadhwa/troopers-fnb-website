#!/usr/bin/env python3
"""Builds assets/world-dots.json, the dotted land used by the coverage globe.

Two dot grids are tested against assets/world-land.geojson:
  coarse  1.0 deg, whole world        (full-globe view)
  fine    0.17 deg, South-East Asia   (zoomed region view)
Each grid is stored as a bitmap (1 = land, plus a second bitmap marking dots that fall
inside a Malaysian state). Odd rows are shifted half a step so dots sit in a staggered grid;
the page decodes them with the same rule.

Run from the repo root:  python3 -I tools/make-world-dots.py
Needs numpy. Re-run only if world-land.geojson or malaysia-states.geojson changes.
"""
import base64
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

GRIDS = {
    "coarse": dict(x0=-180.0, x1=180.0, y0=-58.0, y1=84.0, step=1.0),
    "fine": dict(x0=80.0, x1=145.0, y0=-20.0, y1=35.0, step=0.17),
}


def polygons(path):
    data = json.load(open(path))
    out = []
    for f in data["features"]:
        g = f["geometry"]
        polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        for rings in polys:
            out.append([np.array(r, dtype=float) for r in rings])
    return out


def inside(px, py, polys):
    """Even-odd ray cast of every point against every polygon (outer ring + holes)."""
    hit = np.zeros(px.shape, dtype=bool)
    for rings in polys:
        outer = rings[0]
        x0, y0 = outer.min(axis=0)
        x1, y1 = outer.max(axis=0)
        idx = np.where((px >= x0) & (px <= x1) & (py >= y0) & (py <= y1))[0]
        if idx.size == 0:
            continue
        sx, sy = px[idx], py[idx]
        inpoly = np.zeros(idx.size, dtype=bool)
        for ring in rings:
            xs, ys = ring[:, 0], ring[:, 1]
            n = len(ring)
            j = n - 1
            for i in range(n):
                xi, yi, xj, yj = xs[i], ys[i], xs[j], ys[j]
                if yi != yj:
                    cross = ((yi > sy) != (yj > sy)) & (sx < (xj - xi) * (sy - yi) / (yj - yi) + xi)
                    inpoly ^= cross
                j = i
        hit[idx] |= inpoly
    return hit


def grid(spec):
    step = spec["step"]
    cols = int(round((spec["x1"] - spec["x0"]) / step))
    rows = int(round((spec["y1"] - spec["y0"]) / step)) + 1
    r, c = np.mgrid[0:rows, 0:cols]
    lng = spec["x0"] + (c + 0.5 * (r % 2)) * step
    lat = spec["y0"] + r * step
    return rows, cols, lng.ravel(), lat.ravel()


def pack(mask):
    return base64.b64encode(np.packbits(mask.astype(np.uint8)).tobytes()).decode("ascii")


land = polygons(os.path.join(ASSETS, "world-land.geojson"))
my = polygons(os.path.join(ASSETS, "malaysia-states.geojson"))

out = {}
for name, spec in GRIDS.items():
    rows, cols, lng, lat = grid(spec)
    is_land = inside(lng, lat, land)
    is_my = np.zeros(lng.shape, dtype=bool)
    sel = np.where(is_land & (lng >= 99) & (lng <= 120) & (lat >= 0.5) & (lat <= 8))[0]
    if sel.size:
        is_my[sel] = inside(lng[sel], lat[sel], my)
    out[name] = dict(spec, rows=rows, cols=cols, land=pack(is_land), my=pack(is_my))
    print(name, rows, "x", cols, "land dots:", int(is_land.sum()), "in Malaysia:", int(is_my.sum()))

path = os.path.join(ASSETS, "world-dots.json")
with open(path, "w") as fh:
    json.dump(out, fh, separators=(",", ":"))
print("wrote", path, os.path.getsize(path), "bytes")

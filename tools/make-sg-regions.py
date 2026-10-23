#!/usr/bin/env python3
"""Builds assets/singapore-regions.geojson (the six Singapore areas drawn on the coverage map).

Step 2 of 2. Step 1 is tools/dissolve-sg-areas.cjs, which joins URA Master Plan 2014 planning areas
(Singapore Open Data Licence, data.gov.sg) into Troopers' six areas: Central, East, North, North East, South, West.
South is not an official region; it is made from the southern planning areas (see the SOUTH list in that script).

Run from the repo root, with the file step 1 wrote:

    python3 tools/make-sg-regions.py /tmp/sg-six-areas.geojson

The outlines are thinned (Douglas-Peucker, about 30 m) and tiny islets are dropped so the file stays small.
"""
import json
import os
import sys

TOL = 0.0003          # degrees, about 33 m
MIN_AREA = 4e-6       # square degrees, about 0.05 sq km; smaller islets are dropped
ORDER = ["Central", "East", "North", "North East", "West", "South"]


def area(ring):
    s = 0.0
    for i in range(len(ring) - 1):
        s += ring[i][0] * ring[i + 1][1] - ring[i + 1][0] * ring[i][1]
    return abs(s) / 2


def dp(points, tol):
    """Iterative Douglas-Peucker on an open polyline."""
    n = len(points)
    if n < 3:
        return points
    keep = [False] * n
    keep[0] = keep[-1] = True
    stack = [(0, n - 1)]
    while stack:
        a, b = stack.pop()
        ax, ay = points[a]
        bx, by = points[b]
        dx, dy = bx - ax, by - ay
        norm = dx * dx + dy * dy
        best, idx = -1.0, -1
        for i in range(a + 1, b):
            px, py = points[i]
            if norm == 0:
                d = (px - ax) ** 2 + (py - ay) ** 2
            else:
                t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / norm))
                d = (px - (ax + t * dx)) ** 2 + (py - (ay + t * dy)) ** 2
            if d > best:
                best, idx = d, i
        if best > tol * tol:
            keep[idx] = True
            stack.append((a, idx))
            stack.append((idx, b))
    return [p for p, k in zip(points, keep) if k]


def thin_ring(ring):
    pts = [(round(x, 5), round(y, 5)) for x, y in ring[:-1]]
    out = dp(pts + [pts[0]], TOL)[:-1]
    if len(out) < 4:
        return None
    return [list(p) for p in out] + [list(out[0])]


src = json.load(open(sys.argv[1]))
feats = []
for f in sorted(src["features"], key=lambda f: ORDER.index(f["properties"]["name"])):
    name = f["properties"]["name"]
    g = f["geometry"]
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    kept = []
    for rings in polys:
        if area(rings[0]) < MIN_AREA:
            continue
        thin = [thin_ring(r) for r in rings]
        thin = [r for r in thin if r]
        if thin:
            kept.append(thin)
    feats.append({"type": "Feature", "properties": {"name": name},
                  "geometry": {"type": "MultiPolygon", "coordinates": kept}})
    print(name, "polygons kept:", len(kept), "points:", sum(len(r) for p in kept for r in p))

out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "singapore-regions.geojson")
with open(out, "w") as fh:
    json.dump({"type": "FeatureCollection", "features": feats}, fh, separators=(",", ":"))
print("wrote", out, os.path.getsize(out), "bytes")

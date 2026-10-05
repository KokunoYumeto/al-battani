"""Geometry and reading strips for the circular diagrams of Part III pp. 243-244 (PDF 909-908).
Usage: python polar_kit.py PDF geo [dpi]                -> centre, ring radii and radial-line angles (pt, degrees)
       python polar_kit.py PDF strips [dpi] [ANGLES]    -> p3_kit/PS{PDF}_{angle}.png: for each radial line, the page rotated
                                                            about the centre so that the line runs to the right; a band of
                                                            the rings around the line, upright, with a pt ruler of radii.
Angles are degrees counterclockwise from the right-hand horizontal (east on the page), as on a clock face drawn in maths
convention. Lines on the left half are turned so that their text reads upright (the strip is rotated by 180 degrees)."""
import io, json, sys
import numpy as np
import fitz
from PIL import Image, ImageDraw
from scipy import ndimage
import wide_kit as wk

n = int(sys.argv[1]); mode = sys.argv[2]
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 400
page = wk.doc[n - 1]
s = 72.0 / dpi
img = wk.gray(page, dpi)
a = np.array(img) < 128
H, W = a.shape


def geometry():
    # the horizontal and vertical diameters are the longest straight ink runs through the diagram
    rows = np.array([ndimage.label(a[y])[0].max() for y in range(H)])                  # not used, kept cheap below
    run_h = [max((len(g) for g in np.split(np.arange(W), np.where(np.diff(a[y].astype(int)) != 0)[0] + 1) if a[y][g[0]]), default=0)
             for y in range(H)]
    cy = int(np.argmax(run_h))
    col = a[:, :].T
    run_v = [max((len(g) for g in np.split(np.arange(H), np.where(np.diff(col[x].astype(int)) != 0)[0] + 1) if col[x][g[0]]), default=0)
             for x in range(W)]
    cx = int(np.argmax(run_v))
    # ring crossings along the right half of the horizontal diameter, just above it
    prof = a[cy - int(4 / s):cy - int(2 / s), cx:].any(axis=0)
    xs = np.where(prof)[0]
    rings = []
    for x in xs:
        if not rings or x - rings[-1][-1] > 2:
            rings.append([x])
        else:
            rings[-1].append(x)
    radii = [round(np.mean(g) * s, 1) for g in rings if len(g) < int(2.5 / s)]
    # radial lines: ink on a circle between the 4th and 5th ring from inside
    return cx, cy, radii


def angles(cx, cy, r_pt):
    r = r_pt / s
    th = np.arange(0, 360, 0.25)
    xs = (cx + r * np.cos(np.radians(th))).astype(int); ys = (cy - r * np.sin(np.radians(th))).astype(int)
    ok = (xs >= 0) & (xs < W) & (ys >= 0) & (ys < H)
    hit = np.zeros_like(th, dtype=bool); hit[ok] = a[ys[ok], xs[ok]]
    out, cur = [], []
    for t, h in zip(th, hit):
        if h:
            cur.append(t)
        elif cur:
            out.append(round(float(np.mean(cur)), 1)); cur = []
    return out


if mode == "geo":
    cx, cy, radii = geometry()
    print("centre (pt)", round(cx * s, 1), round(cy * s, 1))
    print("ring radii (pt)", radii)
    for k in range(len(radii) - 1):
        rm = (radii[k] + radii[k + 1]) / 2
        print(f"ink angles at r={rm:.0f}:", angles(cx, cy, rm))
    json.dump({"pdf": n, "cx": cx * s, "cy": cy * s, "radii": radii}, open(wk.OUT + f"PG{n}.json", "w"))
elif mode == "strips":
    g = json.load(open(wk.OUT + f"PG{n}.json"))
    cx, cy = g["cx"] / s, g["cy"] / s
    r0, r1 = g["radii"][0] / s - 4 / s, g["radii"][-1] / s + 4 / s
    angs = [float(v) for v in sys.argv[4].split(",")] if len(sys.argv) > 4 else []
    for t in angs:
        rot = img.rotate(-t, resample=Image.BICUBIC, center=(cx, cy), fillcolor=255)      # line at angle t -> pointing right
        half = int(13 / s)
        strip = rot.crop((int(cx + r0), int(cy - half), int(cx + r1), int(cy + half)))
        d = ImageDraw.Draw(strip)
        for r in g["radii"]:
            x = int(r / s - r0); d.line([(x, 0), (x, 6)], fill=0)
        if 90 < t % 360 < 270:
            strip = strip.rotate(180)
        strip.save(wk.OUT + f"PS{n}_{int(round(t * 10)):04d}.png"); print("strip", t, strip.size)

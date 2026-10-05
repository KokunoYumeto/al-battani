"""Unwrap the rings of a circular diagram (Part III pp. 243-244) into straight bands, so that text written along the
circles with its top pointing outward reads upright, right to left as on the page.
Usage: python polar_unwrap.py PDF QUADRANT [dpi] [rings]
  QUADRANT: 1 = 90..0 degrees (upper right), 2 = 180..90 (upper left), 3 = 270..180 (lower left), 4 = 360..270 (lower
  right); angles counterclockwise from east. Within a band the angle decreases from left to right (clockwise), which keeps
  the page's reading direction for text whose top points outward.
  rings: comma list of ring numbers (1 = innermost), default all; the radii come from p3_kit/PG{PDF}.json.
Each band is resampled so that one pixel along the band equals one pixel radially at the ring's middle radius; radial
lines appear as vertical lines, with a degree ruler every 22.5 degrees. Output: p3_kit/PU{PDF}_q{Q}.png"""
import json, sys
import numpy as np
import fitz
from PIL import Image, ImageDraw
from scipy.ndimage import map_coordinates
import wide_kit as wk

n = int(sys.argv[1]); q = int(sys.argv[2])
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 300
g = json.load(open(wk.OUT + f"PG{n}.json"))
radii = g["radii"]
rings = [int(v) for v in sys.argv[4].split(",")] if len(sys.argv) > 4 else list(range(1, len(radii)))
s = 72.0 / dpi
page = wk.doc[n - 1]
R = radii[-1] + 30
clip = fitz.Rect(g["cx"] - R, g["cy"] - R, g["cx"] + R, g["cy"] + R)
img = np.asarray(wk.gray(page, dpi, clip), dtype=np.float32)
cx, cy = R / s, R / s                                        # centre in the clipped image (px)
t_hi, t_lo = 90.0 * q, 90.0 * (q - 1)
bands = []
for k in rings:
    r_in, r_out = radii[k - 1] - 3, radii[k] + 3                # pt, a little beyond the circles
    rm = (radii[k - 1] + radii[k]) / 2
    n_t = int(np.radians(t_hi - t_lo) * rm / s); n_r = int((r_out - r_in) / s)
    th = np.radians(np.linspace(t_hi + 1.5, t_lo - 1.5, n_t))   # a margin of 1.5 degrees beyond the quadrant
    rr = np.linspace(r_out, r_in, n_r) / s
    T, RR = np.meshgrid(th, rr)
    X = cx + RR * np.cos(T); Y = cy - RR * np.sin(T)
    band = map_coordinates(img, [Y, X], order=1, cval=255).astype(np.uint8)
    im = Image.fromarray(band).convert("L"); d = ImageDraw.Draw(im)
    for deg in np.arange(t_lo, t_hi + 0.01, 22.5):
        x = int((t_hi + 1.5 - deg) / (t_hi - t_lo + 3) * n_t)
        d.line([(x, 0), (x, 5)], fill=0); d.text((x + 2, 0), f"{deg:g}", fill=0)
    bands.append((k, im))
W = max(b.width for _, b in bands) + 40; H = sum(b.height + 10 for _, b in bands)
out = Image.new("L", (W, H), 255); d = ImageDraw.Draw(out); y = 0
for k, b in bands:
    d.text((2, y + b.height // 2), f"r{k}", fill=0); out.paste(b, (40, y)); y += b.height + 10
out.save(wk.OUT + f"PU{n}_q{q}.png"); print(out.size)

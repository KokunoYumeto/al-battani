"""Reading cells of a circular diagram: for each radial line and each ring, the unwrapped band around the line (the
values written on both sides of it), upright. Columns = lines, rows = rings (outermost at the top), one sheet.
Usage: python polar_cells.py PDF ANGLES [dpi] [flip] [tag]
  ANGLES: comma list of line angles (degrees counterclockwise from east), drawn left to right in that order.
  flip: 1 rotates every cell by 180 degrees (for text whose top points to the centre, as in the lower half of Part II p. 92).
The cell spans the ring (plus 2 pt) radially and min(24 pt, 0.47 of the 22.5-degree sector) on each side of the line along
the arc. Output: p3_kit/PC{PDF}_{tag}.png"""
import sys
import numpy as np
import json
import fitz
from PIL import Image, ImageDraw
from scipy.ndimage import map_coordinates
import wide_kit as wk

n = int(sys.argv[1]); angles = [float(v) for v in sys.argv[2].split(",")]
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 450
flip = len(sys.argv) > 4 and sys.argv[4] == "1"
tag = sys.argv[5] if len(sys.argv) > 5 else "x"
g = json.load(open(wk.OUT + f"PG{n}.json")); radii = g["radii"]
s = 72.0 / dpi
R = radii[-1] + 30
clip = fitz.Rect(g["cx"] - R, g["cy"] - R, g["cx"] + R, g["cy"] + R)
img = np.asarray(wk.gray(wk.doc[n - 1], dpi, clip), dtype=np.float32)
cx = cy = R / s
cells = []                                            # [ring][line]
for k in range(len(radii) - 1, 0, -1):
    row = []
    r_in, r_out = radii[k - 1] - 2, radii[k] + 2
    rm = (radii[k - 1] + radii[k]) / 2
    half_pt = min(24.0, 0.47 * np.radians(22.5) * rm)
    for t in angles:
        dt = np.degrees(half_pt / rm)
        n_t = int(2 * half_pt / s); n_r = int((r_out - r_in) / s)
        th = np.radians(np.linspace(t + dt, t - dt, n_t))
        rr = np.linspace(r_out, r_in, n_r) / s
        T, RR = np.meshgrid(th, rr)
        band = map_coordinates(img, [cy - RR * np.sin(T), cx + RR * np.cos(T)], order=1, cval=255).astype(np.uint8)
        im = Image.fromarray(band)
        if flip:
            im = im.rotate(180)
        row.append(im)
    cells.append((k, row))
cw = max(im.width for _, row in cells for im in row) + 12
chh = max(im.height for _, row in cells for im in row) + 8
out = Image.new("L", (40 + cw * len(angles), 18 + chh * len(cells)), 255)
d = ImageDraw.Draw(out)
for j, t in enumerate(angles):
    d.text((40 + j * cw + cw // 2 - 12, 2), f"{t:g}", fill=0)
for i, (k, row) in enumerate(cells):
    d.text((4, 18 + i * chh + chh // 2), f"r{k}", fill=0)
    for j, im in enumerate(row):
        x = 40 + j * cw + (cw - im.width) // 2
        out.paste(im, (x, 18 + i * chh))
out.save(wk.OUT + f"PC{n}_{tag}.png"); print(out.size)

"""List the connected ink components of a small region (a word) with their positions, to place dots objectively.
Usage: python inkparts.py PDF x0 y0 x1 y1 [dpi]   (pt; master copy)
Prints one line per component, right to left: x-range and y-range in pt, height, pixel area, and a class:
  dot (small), stroke (tall and thin), body (everything else). Also writes p3_kit/IP{PDF}.png with each component
  boxed and numbered in reading order, for a visual cross-check."""
import io, sys
import fitz
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
import wide_kit as wk

n = int(sys.argv[1]); x0, y0, x1, y1 = [float(v) for v in sys.argv[2:6]]
dpi = int(sys.argv[6]) if len(sys.argv) > 6 else 1600
page = wk.doc[n - 1]
im = Image.open(io.BytesIO(page.get_pixmap(dpi=dpi, clip=fitz.Rect(x0, y0, x1, y1)).tobytes("png"))).convert("L")
a = np.array(im) < 128
lab, k = ndimage.label(a)
objs = ndimage.find_objects(lab)
s = 72.0 / dpi
rows = []
for i, sl in enumerate(objs):
    ys, xs = sl
    area = int((lab[sl] == i + 1).sum())
    if area < 6:
        continue
    h = (ys.stop - ys.start) * s; w = (xs.stop - xs.start) * s
    kind = "dot" if max(h, w) < 1.6 else ("stroke" if h > 2.5 * w else "body")
    rows.append((xs.stop, xs.start, ys.start, ys.stop, h, w, area, kind))
rows.sort(key=lambda r: -r[0])
out = im.convert("RGB"); d = ImageDraw.Draw(out)
for j, (xe, xs_, ys_, ye, h, w, area, kind) in enumerate(rows, 1):
    print(f"{j:2d} {kind:6s} x {x0 + xs_ * s:6.1f}-{x0 + xe * s:6.1f}  y {y0 + ys_ * s:6.1f}-{y0 + ye * s:6.1f}  h {h:4.1f}  area {area}")
    col = (255, 0, 0) if kind == "dot" else (0, 120, 255)
    d.rectangle([xs_, ys_, xe, ye], outline=col, width=2); d.text((xs_, max(0, ys_ - 12)), str(j), fill=col)
out.save(wk.OUT + f"IP{n:04}.png")

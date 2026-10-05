"""Count the dots of small Arabic words objectively (master copy).
Usage: python dots.py SPECFILE [dpi] [size_factor]   (SPEC rows as for pairs.py: (pdf, label, "x:X0-X1", y_center[, half_height]))
For each region: the baseline (densest ink row) and every small ink component (max side < 3.2 pt, height < 2.2 pt),
right to left, as  x-centre ^|v width x height  in pt  (^ above the baseline, v below). A single footnote dot is
about 1.2-1.6 pt wide; two touching dots about 2.5-3 pt; a merged three-dot cluster about 2.5 pt wide and tall."""
import runpy, sys
import numpy as np
import fitz
from scipy import ndimage
import wide_kit as wk

SPEC = runpy.run_path(sys.argv[1])["SPEC"]
dpi = int(sys.argv[2]) if len(sys.argv) > 2 else 2400
f = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0   # size factor for the thresholds (main table font: about 1.6)
s = 72.0 / dpi
for row in SPEC:
    n, lab, xs, yc = row[:4]
    hh = row[4] if len(row) > 4 else 9
    x0, x1 = [float(v) for v in xs[2:].split("-")]
    r = fitz.Rect(x0, yc - hh, x1, yc + hh)
    a = np.array(wk.gray(wk.doc[n - 1], dpi, r)) < 128
    base = r.y0 + (np.argmax(a.sum(1)) + 0.5) * s
    lab_a, _ = ndimage.label(a)
    small = []
    for i, sl in enumerate(ndimage.find_objects(lab_a)):
        if (lab_a[sl] == i + 1).sum() < 6:
            continue
        ys, xx = sl
        h = (ys.stop - ys.start) * s; w = (xx.stop - xx.start) * s
        if max(h, w) < 3.2 * f and h < 2.2 * f:
            cx = x0 + (xx.start + xx.stop) / 2 * s; cy = r.y0 + (ys.start + ys.stop) / 2 * s
            small.append((cx, "^" if cy < base else "v", w, h, cy))
    small.sort(key=lambda t: -t[0])
    print(f"{lab:12s} base {base:.1f}: " + "  ".join(f"{cx:.1f}{p}{w:.1f}x{h:.1f}" for cx, p, w, h, cy in small))

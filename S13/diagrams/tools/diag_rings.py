"""Rings of a circular diagram by coverage: for a grid of candidate centres, the fraction of 720 directions with ink at
each radius (0.5 pt steps); prints the best centre and the radii whose coverage peaks above a threshold.
Usage: python diag_rings.py PDF cx cy [search_pt] [dpi]   (honours P3_SRC for the IA copy)"""
import sys
import numpy as np
from scipy.signal import find_peaks
import wide_kit as wk

n = int(sys.argv[1]); cx0, cy0 = float(sys.argv[2]), float(sys.argv[3])
span = float(sys.argv[4]) if len(sys.argv) > 4 else 12.0
dpi = int(sys.argv[5]) if len(sys.argv) > 5 else 150
s = 72.0 / dpi
thr = int(sys.argv[6]) if len(sys.argv) > 6 else 150
a = np.array(wk.gray(wk.doc[n - 1], dpi)) < thr
H, W = a.shape
th = np.radians(np.arange(0, 360, 0.5)); rs = np.arange(10, 360, 0.5)
C, S = np.cos(th)[None, :], np.sin(th)[None, :]


def coverage(cx, cy):
    xs = ((cx + rs[:, None] * C) / s).astype(int); ys = ((cy - rs[:, None] * S) / s).astype(int)
    ok = (xs >= 0) & (xs < W) & (ys >= 0) & (ys < H)
    hit = np.zeros(xs.shape, bool); hit[ok] = a[ys[ok], xs[ok]]
    return hit.mean(axis=1)


best = None
for dx in np.arange(-span, span + 0.1, 2.0):
    for dy in np.arange(-span, span + 0.1, 2.0):
        cov = coverage(cx0 + dx, cy0 + dy)
        score = np.sort(cov)[-6:].sum()
        if best is None or score > best[0]:
            best = (score, cx0 + dx, cy0 + dy)
_, bx, by = best
for dx in np.arange(-2, 2.01, 0.5):                      # refine
    for dy in np.arange(-2, 2.01, 0.5):
        cov = coverage(bx + dx, by + dy)
        score = np.sort(cov)[-6:].sum()
        if score > best[0]:
            best = (score, bx + dx, by + dy)
_, bx, by = best
cov = coverage(bx, by)
pk, pr = find_peaks(cov, height=0.5, distance=6)
print(f"centre {bx:.2f} {by:.2f}")
print("rings (r pt, coverage):", [(float(rs[p]), round(float(cov[p]), 2)) for p in pk])

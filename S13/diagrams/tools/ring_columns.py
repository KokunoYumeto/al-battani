"""Angular positions of the text columns in one ring of a circular diagram: the ink of the ring band (lines excluded:
a margin around each sector line and inside the ring borders) projected on the angle, smoothed, peaks per sector.
Usage: python ring_columns.py PDF r0 r1 line0 nsect [dpi] [min_sep_deg]
  line0: the angle of one sector line; nsect: number of sectors (lines every 360/nsect degrees). Prints per sector
  the peak angles (degrees counterclockwise from east)."""
import sys, json
import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks
import wide_kit as wk

n = int(sys.argv[1]); r0, r1, line0 = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
nsect = int(sys.argv[5]); dpi = int(sys.argv[6]) if len(sys.argv) > 6 else 200
sep = float(sys.argv[7]) if len(sys.argv) > 7 else 3.0
g = json.load(open(wk.OUT + f"PG{n}.json")); cx, cy = g["cx"], g["cy"]
s = 72.0 / dpi
a = np.array(wk.gray(wk.doc[n - 1], dpi)) < 140
step = 0.1
th = np.arange(0, 360, step)
rs = np.arange(r0 + 2.5, r1 - 2.5, s)
xs = ((cx + rs[:, None] * np.cos(np.radians(th))[None, :]) / s).astype(int)
ys = ((cy - rs[:, None] * np.sin(np.radians(th))[None, :]) / s).astype(int)
prof = a[ys, xs].sum(axis=0).astype(float)
width = 360 / nsect
lines = [(line0 + i * width) % 360 for i in range(nsect)]
for L in lines:                                            # blank a margin of 0.8 degree around each line
    d = np.abs(((th - L) + 180) % 360 - 180); prof[d < 0.8] = 0
sm = gaussian_filter1d(np.r_[prof, prof], 6)[:len(th)]
for L in sorted(lines):
    lo = L; hi = L + width
    idx = [i for i, t in enumerate(th) if lo < t < hi or lo < t + 360 < hi]
    seg = sm[idx]
    pk, _ = find_peaks(seg, distance=int(sep / step), prominence=seg.max() * 0.15)
    print(f"sector {lo:6.1f}-{hi:6.1f}:", [round(float(th[idx[p]]), 1) for p in pk])

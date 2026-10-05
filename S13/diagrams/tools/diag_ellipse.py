"""For each ring of a circular diagram (approximate radii given), find in 360 directions the radius of the ring line
near the approximate radius (the ink run closest to it within +-tol), fit a circle and an axis-aligned ellipse.
Usage: python diag_ellipse.py PDF cx cy r1,r2,... [tol] [dpi]   (pt; honours P3_SRC)"""
import sys
import numpy as np
import wide_kit as wk

n = int(sys.argv[1]); cx, cy = float(sys.argv[2]), float(sys.argv[3])
radii = [float(v) for v in sys.argv[4].split(",")]
tol = float(sys.argv[5]) if len(sys.argv) > 5 else 8.0
dpi = int(sys.argv[6]) if len(sys.argv) > 6 else 200
s = 72.0 / dpi
thr = int(sys.argv[7]) if len(sys.argv) > 7 else 150
a = np.array(wk.gray(wk.doc[n - 1], dpi)) < thr
H, W = a.shape
for R in radii:
    P = []
    for th in np.radians(np.arange(0, 360, 1.0)):
        rs = np.arange(R - tol, R + tol, s / 2)
        xs = ((cx + rs * np.cos(th)) / s).astype(int); ys = ((cy - rs * np.sin(th)) / s).astype(int)
        ok = (xs >= 0) & (xs < W) & (ys >= 0) & (ys < H)
        hit = np.zeros(len(rs), bool); hit[ok] = a[ys[ok], xs[ok]]
        if hit.any():
            idx = np.where(hit)[0]
            r = rs[idx[np.argmin(abs(rs[idx] - R))]]
            P.append((cx + r * np.cos(th), cy - r * np.sin(th)))
    P = np.array(P)
    Ac = np.c_[P[:, 0], P[:, 1], np.ones(len(P))]
    D, E, F = np.linalg.lstsq(Ac, -(P[:, 0] ** 2 + P[:, 1] ** 2), rcond=None)[0]
    ccx, ccy = -D / 2, -E / 2; rr = np.sqrt(ccx ** 2 + ccy ** 2 - F)
    res = np.hypot(P[:, 0] - ccx, P[:, 1] - ccy) - rr
    M = np.c_[P[:, 0] ** 2, P[:, 1] ** 2, P[:, 0], P[:, 1]]
    Ae, Ce, De, Ee = np.linalg.lstsq(M, np.ones(len(P)), rcond=None)[0]
    ex, ey = -De / (2 * Ae), -Ee / (2 * Ce); G = 1 + Ae * ex ** 2 + Ce * ey ** 2
    print(f"r~{R:g}: circle ({ccx:.1f},{ccy:.1f}) r {rr:.1f} sd {res.std():.2f} | ellipse ({ex:.1f},{ey:.1f}) ax {np.sqrt(G/Ae):.1f} ay {np.sqrt(G/Ce):.1f}  n={len(P)}")

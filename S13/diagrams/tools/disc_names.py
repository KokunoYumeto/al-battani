"""Names written radially in the inner disc of a circular diagram: find the angular clusters of ink inside the innermost
circle and save one upright strip per cluster (the page rotated about the centre so that the cluster's radius runs
horizontally). Both orientations are written: _o (outer end on the right) and _i (outer end on the left).
Usage: python disc_names.py PDF [dpi] [r_max_pt] [tag]   (the geometry comes from p3_kit/PG{PDF}.json, or pass the IA
       file with P3_SRC as for wide_kit)  -> p3_kit/DN{PDF}_{tag}.png (one sheet: angle label, _o strip, _i strip)"""
import sys, json
import numpy as np
import fitz
from PIL import Image, ImageDraw
from scipy import ndimage
import wide_kit as wk

n = int(sys.argv[1]); dpi = int(sys.argv[2]) if len(sys.argv) > 2 else 500
g = json.load(open(wk.OUT + f"PG{n}.json"))
rmax = float(sys.argv[3]) if len(sys.argv) > 3 else g["radii"][0] - 2.5
tag = sys.argv[4] if len(sys.argv) > 4 else "x"
s = 72.0 / dpi
R = g["radii"][0] + 6
clip = fitz.Rect(g["cx"] - R, g["cy"] - R, g["cx"] + R, g["cy"] + R)
img = wk.gray(wk.doc[n - 1], dpi, clip)
a = np.array(img) < 128
c = R / s
yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
rr = np.hypot(xx - c, yy - c) * s
ink = a & (rr < rmax) & (rr > 6)
lab, k = ndimage.label(ndimage.binary_dilation(ink, iterations=int(1.2 / s)))
# angle of each component's centroid; merge components into clusters by angular gaps
comps = []
for i in range(1, k + 1):
    m = (lab == i) & ink
    if m.sum() * s * s < 0.5:
        continue
    y, x = np.nonzero(m)
    th = np.degrees(np.arctan2(c - y, x - c)) % 360
    # circular mean
    mu = np.degrees(np.arctan2(np.sin(np.radians(th)).mean(), np.cos(np.radians(th)).mean())) % 360
    comps.append((mu, th.min(), th.max(), m.sum()))
comps.sort()
angs = [cm[0] for cm in comps]
print("components", len(comps))
clusters = []
for mu, lo, hi, sz in comps:
    if clusters and (mu - clusters[-1][-1][0]) < 6:
        clusters[-1].append((mu, sz))
    else:
        clusters.append([(mu, sz)])
if len(clusters) > 1 and (clusters[0][0][0] + 360 - clusters[-1][-1][0]) < 6:
    clusters[0] = clusters.pop() + clusters[0]
centres = []
for cl in clusters:
    w = np.array([sz for _, sz in cl], float); t = np.radians([mu for mu, _ in cl])
    centres.append(np.degrees(np.arctan2((np.sin(t) * w).sum(), (np.cos(t) * w).sum())) % 360)
centres.sort()
print("clusters", len(centres), [round(t, 1) for t in centres])
strips = []
half = int(9 / s)
for t in centres:
    rot = img.rotate(-t, resample=Image.BICUBIC, center=(c, c), fillcolor=255)
    st = rot.crop((int(c + 4 / s), int(c - half), int(c + rmax / s + 2 / s), int(c + half)))
    strips.append((t, st, st.rotate(180)))
W = 2 * max(st.width for _, st, _ in strips) + 120; H = sum(st.height + 8 for _, st, _ in strips)
out = Image.new("L", (W, H), 255); d = ImageDraw.Draw(out); y = 0
for t, so, si in strips:
    d.text((2, y + so.height // 2), f"{t:.1f}", fill=0); out.paste(so, (60, y)); out.paste(si, (80 + so.width, y))
    y += so.height + 8
out.save(wk.OUT + f"DN{n}_{tag}.png"); print(out.size)

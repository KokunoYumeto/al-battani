"""Radially written names in the inner disc of a circular diagram, both copies: for each angle, the page rotated about
the centre so that the radius at that angle runs to the right (outer end on the right), master strip above the IA strip.
Usage: python disc_pick.py PDF IAPAGE ANGLES [dpi] [half_pt] [tag] [r0_pt] [r1_pt|-] [flip]   ANGLES: comma list (degrees counterclockwise from east)
Geometries: p3_kit/PG{PDF}.json and p3_kit/PG{IAPAGE}.json. Output: p3_kit/DP{PDF}_{tag}.png"""
import sys, json
import numpy as np
import fitz
from PIL import Image, ImageDraw
from scipy.ndimage import map_coordinates
import wide_kit as wk

IA = r"F:/user/Documents/Chat Interl Src/cleanup multilingual/albattani_work_CLAUDE/source_scan/nallino_1899_albattanisivealb00batt.pdf"
n, ian = int(sys.argv[1]), int(sys.argv[2])
angles = [float(v) for v in sys.argv[3].split(",")]
dpi = int(sys.argv[4]) if len(sys.argv) > 4 else 900
half_pt = float(sys.argv[5]) if len(sys.argv) > 5 else 8.0
tag = sys.argv[6] if len(sys.argv) > 6 else "x"
R0 = float(sys.argv[7]) if len(sys.argv) > 7 else 3.0
R1 = float(sys.argv[8]) if len(sys.argv) > 8 and sys.argv[8] != "-" else None   # outer radius (pt); default: just inside the innermost circle
FLIP = len(sys.argv) > 9 and sys.argv[9] == "1"   # rotate every strip by 180 degrees (labels that start at the inner end)
gm = json.load(open(wk.OUT + f"PG{n}.json")); gi = json.load(open(wk.OUT + f"PG{ian}.json"))
copies = [(wk.doc[n - 1], gm, 1.0), (fitz.open(IA)[ian - 1], gi, gi["radii"][-1] / gm["radii"][-1])]


def strip(page, g, scale, t):
    """Sample the band r0..r_end along the radius at angle t (outer end on the right, higher angles at the top)."""
    d = dpi / scale; s = 72.0 / d
    r_end = (R1 * scale) if R1 else (g["radii"][0] - 0.8 * scale)
    r_beg = R0 * scale; h = half_pt * scale
    tr = np.radians(t); e = np.array([np.cos(tr), -np.sin(tr)]); q = np.array([-np.sin(tr), -np.cos(tr)])
    corners = [np.array([g["cx"], g["cy"]]) + u * e + v * q for u in (r_beg, r_end) for v in (-h, h)]
    xs = [c[0] for c in corners]; ys = [c[1] for c in corners]
    clip = fitz.Rect(min(xs) - 2, min(ys) - 2, max(xs) + 2, max(ys) + 2) & page.rect
    pix = page.get_pixmap(matrix=fitz.Matrix(d / 72.0, d / 72.0), clip=clip)
    img = np.asarray(Image.frombytes("RGB" if pix.n >= 3 else "L", (pix.width, pix.height), pix.samples).convert("L"), dtype=np.float32)
    n_u = int((r_end - r_beg) / s); n_v = int(2 * h / s)
    U, V = np.meshgrid(np.linspace(r_beg, r_end, n_u), np.linspace(h, -h, n_v))
    X = g["cx"] + U * e[0] + V * q[0]; Y = g["cy"] + U * e[1] + V * q[1]
    b = map_coordinates(img, [(Y - clip.y0) / s, (X - clip.x0) / s], order=1, cval=255)
    im = Image.fromarray(np.clip(b, 0, 255).astype(np.uint8))
    return im.rotate(180) if FLIP else im


rows = []
for t in angles:
    rows.append((t, [strip(p, g, sc, t) for p, g, sc in copies]))
W = max(max(a.width, b.width) for _, (a, b) in rows) + 60
H = sum(a.height + b.height + 14 for _, (a, b) in rows)
out = Image.new("L", (W, H), 255); dr = ImageDraw.Draw(out); y = 0
for t, (a, b) in rows:
    dr.text((2, y + 4), f"{t:g}", fill=0); out.paste(a, (60, y)); out.paste(b, (60, y + a.height + 4))
    dr.line([(60, y + a.height + 2), (W, y + a.height + 2)], fill=128)
    y += a.height + b.height + 14
if out.width > 2000:
    out = out.resize((2000, int(out.height * 2000 / out.width)))
out.save(wk.OUT + f"DP{n}_{tag}.png"); print(out.size)

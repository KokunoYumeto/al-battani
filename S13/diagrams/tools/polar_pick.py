"""Chosen cells of a circular diagram in both copies, unwrapped and upright: master | IA copy.
Usage: python polar_pick.py PDF IAPAGE SPEC [dpi] [tag]
  SPEC: semicolon list of angle:ring[:label[:half-width in degrees]], e.g. "67.5:6;45:3:check ke/me;104:5::15"; the geometries come from p3_kit/PG{PDF}.json
  (master) and p3_kit/PG{IAPAGE}.json (IA copy, page number in the IA file, 1-based).
Output: p3_kit/PP{PDF}_{tag}.png, one row per cell."""
import sys, json
import numpy as np
import fitz
from PIL import Image, ImageDraw
from scipy.ndimage import map_coordinates
import wide_kit as wk

IA = r"F:/user/Documents/Chat Interl Src/cleanup multilingual/albattani_work_CLAUDE/source_scan/nallino_1899_albattanisivealb00batt.pdf"
n, ian = int(sys.argv[1]), int(sys.argv[2])
spec = [x.split(":") for x in sys.argv[3].split(";") if x]
dpi = int(sys.argv[4]) if len(sys.argv) > 4 else 600
tag = sys.argv[5] if len(sys.argv) > 5 else "x"
docs = {"m": (wk.doc[n - 1], json.load(open(wk.OUT + f"PG{n}.json"))),
        "i": (fitz.open(IA)[ian - 1], json.load(open(wk.OUT + f"PG{ian}.json")))}


def cell(which, t, k, half_deg=None):
    page, g = docs[which]; radii = g["radii"]
    scale = radii[-1] / docs["m"][1]["radii"][-1]                # IA pt per master pt
    d = dpi / scale                                              # same pixel size for both copies
    s = 72.0 / d
    r_in, r_out = radii[k - 1] - 2 * scale, radii[k] + 2 * scale
    rm = (radii[k - 1] + radii[k]) / 2
    half = min(26.0 * scale, 0.47 * np.radians(22.5) * rm) if half_deg is None else np.radians(half_deg) * rm
    R = r_out + 4
    clip = fitz.Rect(g["cx"] - R, g["cy"] - R, g["cx"] + R, g["cy"] + R)
    pix = page.get_pixmap(matrix=fitz.Matrix(d / 72.0, d / 72.0), clip=clip)
    img = np.asarray(Image.frombytes("RGB" if pix.n >= 3 else "L", (pix.width, pix.height), pix.samples).convert("L"), dtype=np.float32)
    c = R / s
    dt = np.degrees(half / rm)
    n_t = int(2 * half / s); n_r = int((r_out - r_in) / s)
    th = np.radians(np.linspace(t + dt, t - dt, n_t)); rr = np.linspace(r_out, r_in, n_r) / s
    T, RR = np.meshgrid(th, rr)
    band = map_coordinates(img, [c - RR * np.sin(T), c + RR * np.cos(T)], order=1, cval=255)
    return Image.fromarray(np.clip(band, 0, 255).astype(np.uint8))


rows = []
for item in spec:
    t, k = float(item[0]), int(item[1]); lab = f"{t:g} r{k}" + (f" {item[2]}" if len(item) > 2 and item[2] else "")
    hd = float(item[3]) if len(item) > 3 else None          # optional half-width in degrees (whole sectors)
    rows.append((lab, cell("m", t, k, hd), cell("i", t, k, hd)))
W = max(a.width + b.width for _, a, b in rows) + 40
H = sum(max(a.height, b.height) + 22 for _, a, b in rows)
out = Image.new("L", (W, H), 255); dr = ImageDraw.Draw(out); y = 0
for lab, a, b in rows:
    dr.text((4, y + 2), lab, fill=0); out.paste(a, (0, y + 18)); out.paste(b, (a.width + 20, y + 18))
    dr.line([(a.width + 10, y + 18), (a.width + 10, y + 18 + a.height)], fill=0, width=2)
    y += max(a.height, b.height) + 22
if out.width > 2000:
    out = out.resize((2000, int(out.height * 2000 / out.width)))
out.save(wk.OUT + f"PP{n}_{tag}.png"); print(out.size)

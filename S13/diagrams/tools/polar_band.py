"""An annulus of a circular diagram unwrapped into a straight band (text whose top points outward reads upright), both
copies stacked: master above, IA copy below.
Usage: python polar_band.py PDF IAPAGE R0 R1 T_HI T_LO [dpi] [tag]   radii in master pt, angles in degrees counterclockwise
from east; the band runs from T_HI (left) to T_LO (right). Output: p3_kit/PB{PDF}_{tag}.png (at most 2000 px wide)"""
import sys, json
import numpy as np
import fitz
from PIL import Image, ImageDraw
from scipy.ndimage import map_coordinates
import wide_kit as wk

IA = r"F:/user/Documents/Chat Interl Src/cleanup multilingual/albattani_work_CLAUDE/source_scan/nallino_1899_albattanisivealb00batt.pdf"
n, ian = int(sys.argv[1]), int(sys.argv[2])
r0, r1, thi, tlo = [float(v) for v in sys.argv[3:7]]
dpi = int(sys.argv[7]) if len(sys.argv) > 7 else 400
tag = sys.argv[8] if len(sys.argv) > 8 else "x"
gm = json.load(open(wk.OUT + f"PG{n}.json")); gi = json.load(open(wk.OUT + f"PG{ian}.json"))


def band(page, g, scale):
    d = dpi / scale; s = 72.0 / d
    R = r1 * scale + 4
    clip = fitz.Rect(g["cx"] - R, g["cy"] - R, g["cx"] + R, g["cy"] + R) & page.rect
    pix = page.get_pixmap(matrix=fitz.Matrix(d / 72.0, d / 72.0), clip=clip)
    img = np.asarray(Image.frombytes("RGB" if pix.n >= 3 else "L", (pix.width, pix.height), pix.samples).convert("L"), dtype=np.float32)
    ox, oy = (g["cx"] - clip.x0) / s, (g["cy"] - clip.y0) / s
    rm = (r0 + r1) / 2 * scale
    n_t = int(np.radians(thi - tlo) * rm / s); n_r = int((r1 - r0) * scale / s)
    th = np.radians(np.linspace(thi, tlo, n_t)); rr = np.linspace(r1 * scale, r0 * scale, n_r) / s
    T, RR = np.meshgrid(th, rr)
    b = map_coordinates(img, [oy - RR * np.sin(T), ox + RR * np.cos(T)], order=1, cval=255)
    im = Image.fromarray(np.clip(b, 0, 255).astype(np.uint8))
    return im


a = band(wk.doc[n - 1], gm, 1.0)
b = band(fitz.open(IA)[ian - 1], gi, gi["radii"][-1] / gm["radii"][-1]).resize(a.size)
out = Image.new("L", (a.width, a.height * 2 + 6), 255); out.paste(a, (0, 0)); out.paste(b, (0, a.height + 6))
d = ImageDraw.Draw(out)
for deg in np.arange(np.ceil(tlo / 22.5) * 22.5, thi + 0.01, 22.5):
    x = int((thi - deg) / (thi - tlo) * a.width); d.line([(x, 0), (x, 8)], fill=0); d.text((x + 2, 0), f"{deg:g}", fill=0)
if out.width > 2000:
    out = out.resize((2000, int(out.height * 2000 / out.width)))
out.save(wk.OUT + f"PB{n}_{tag}.png"); print(out.size)

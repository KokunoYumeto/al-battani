"""One-copy annulus unroll (Part II figures): text with its top outward reads upright, angle decreasing to the right.
Usage: python polar_band1.py PDF R0 R1 T_HI T_LO [dpi] [tag] [flip]  -> p3_kit/PB{PDF}_{tag}.png; flip=1 turns the band
by 180 degrees (text with its top toward the centre)."""
import sys, json
import numpy as np
import fitz
from PIL import Image, ImageDraw
from scipy.ndimage import map_coordinates
import wide_kit as wk

n = int(sys.argv[1]); r0, r1, thi, tlo = [float(v) for v in sys.argv[2:6]]
dpi = int(sys.argv[6]) if len(sys.argv) > 6 else 400
tag = sys.argv[7] if len(sys.argv) > 7 else "x"
flip = len(sys.argv) > 8 and sys.argv[8] == "1"
g = json.load(open(wk.OUT + f"PG{n}.json"))
page = wk.doc[n - 1]; s = 72.0 / dpi
R = r1 + 4
clip = fitz.Rect(g["cx"] - R, g["cy"] - R, g["cx"] + R, g["cy"] + R) & page.rect
pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72.0, dpi / 72.0), clip=clip)
img = np.asarray(Image.frombytes("RGB" if pix.n >= 3 else "L", (pix.width, pix.height), pix.samples).convert("L"), dtype=np.float32)
ox, oy = (g["cx"] - clip.x0) / s, (g["cy"] - clip.y0) / s
rm = (r0 + r1) / 2
n_t = int(np.radians(thi - tlo) * rm / s); n_r = int((r1 - r0) / s)
th = np.radians(np.linspace(thi, tlo, n_t)); rr = np.linspace(r1, r0, n_r) / s
T, RR = np.meshgrid(th, rr)
b = map_coordinates(img, [oy - RR * np.sin(T), ox + RR * np.cos(T)], order=1, cval=255)
im = Image.fromarray(np.clip(b, 0, 255).astype(np.uint8))
if flip:
    im = im.rotate(180)
d = ImageDraw.Draw(im)
for deg in np.arange(np.ceil(tlo / 30) * 30, thi + 0.01, 30):
    x = int((thi - deg) / (thi - tlo) * im.width)
    if flip:
        x = im.width - x
    d.line([(x, 0), (x, 8)], fill=0); d.text((x + 2, 0), f"{deg:g}", fill=0)
if im.width > 2000:
    im = im.resize((2000, int(im.height * 2000 / im.width)))
im.save(wk.OUT + f"PB{n}_{tag}.png"); print(im.size)

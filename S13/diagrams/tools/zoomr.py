"""Master crop at high dpi with a pt ruler along the top (every pt, labelled every 5).
Usage: python zoomr.py PDF x0 x1 y0 y1 [dpi] [tag]  -> p3_kit/ZR{PDF}_{tag}.png"""
import sys
import fitz
from PIL import ImageDraw
import wide_kit as wk

n = int(sys.argv[1]); x0, x1, y0, y1 = [float(v) for v in sys.argv[2:6]]
d = int(sys.argv[6]) if len(sys.argv) > 6 else 1800
tag = sys.argv[7] if len(sys.argv) > 7 else "x"
im = wk.gray(wk.doc[n - 1], d, fitz.Rect(x0, y0, x1, y1)).convert("RGB"); dr = ImageDraw.Draw(im)
k = d / 72
for x in range(int(x0) + 1, int(x1) + 1):
    X = int((x - x0) * k); dr.line([(X, 0), (X, 10 if x % 5 else 24)], fill=(255, 0, 0), width=2)
    if x % 5 == 0:
        dr.text((X + 3, 10), str(x), fill=(255, 0, 0))
for y in range(int(y0) + 1, int(y1) + 1):
    Y = int((y - y0) * k); dr.line([(0, Y), (10 if y % 5 else 24, Y)], fill=(0, 0, 255), width=2)
    if y % 5 == 0:
        dr.text((12, Y + 2), str(y), fill=(0, 0, 255))
if im.width > 2000:
    im = im.resize((2000, int(im.height * 2000 / im.width)))
im.save(wk.OUT + f"ZR{n}_{tag}.png"); print(im.size)

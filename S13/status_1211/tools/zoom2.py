"""Zoom one region of a Part III page in both copies, side by side (master | Internet Archive copy).
Usage: python zoom2.py PDF x0-x1 y0-y1[,y0-y1...] [dpi]   (pt in master coordinates; default 900 dpi)
The IA copy (page = PDF - 865) is aligned by the two table frames (wide_kit.geometry).
Output: p3_kit/Z{PDF}.png"""
import io, os, sys
import fitz
from PIL import Image, ImageDraw
import wide_kit as wk

IA = r"F:/user/Documents/Chat Interl Src/cleanup multilingual/albattani_work_CLAUDE/source_scan/nallino_1899_albattanisivealb00batt.pdf"
n = int(sys.argv[1]); xr = [float(v) for v in sys.argv[2].split("-")]
yrs = [[float(v) for v in s.split("-")] for s in sys.argv[3].split(",")]
dpi = int(sys.argv[4]) if len(sys.argv) > 4 else 900
pa = wk.doc[n - 1]; pb = fitz.open(IA)[n - 866]
A = wk.geometry(pa)["table_pt"]; B = wk.geometry(pb)["table_pt"]
sx = (B[2] - B[0]) / (A[2] - A[0]); sy = (B[3] - B[1]) / (A[3] - A[1])
rows = []
for y0, y1 in yrs:
    a = wk.gray(pa, dpi, fitz.Rect(xr[0], y0, xr[1], y1))
    r = fitz.Rect(B[0] + (xr[0] - A[0]) * sx, B[1] + (y0 - A[1]) * sy, B[0] + (xr[1] - A[0]) * sx, B[1] + (y1 - A[1]) * sy)
    b = wk.gray(pb, int(dpi / sx), r)
    rows.append((f"{y0:.0f}", a, b))
W = max(a.width for _, a, _ in rows) + max(b.width for _, _, b in rows) + 90
H = sum(max(a.height, b.height) + 8 for _, a, b in rows)
s = Image.new("L", (W, H), 255); d = ImageDraw.Draw(s); y = 0
wa = max(a.width for _, a, _ in rows)
for lab, a, b in rows:
    d.text((2, y + 6), lab, fill=0); s.paste(a, (50, y)); s.paste(b, (50 + wa + 30, y)); y += max(a.height, b.height) + 8
if s.width > 1990:
    s = s.resize((1990, int(s.height * 1990 / s.width)), Image.LANCZOS)
s.save(os.path.join(wk.OUT, f"Z{n:04}.png")); print(s.size)

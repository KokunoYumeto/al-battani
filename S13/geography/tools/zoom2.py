"""Zoom one region of a Part III page in both copies, side by side (master | Internet Archive copy).
Usage: python zoom2.py PDF x0-x1 y0-y1[,y0-y1...] [dpi]   (pt in master coordinates; default 900 dpi)
The IA copy (page = PDF - 865) is aligned to the master by image matching: the scale comes from the widths of the
table frames, the offset from a normalized cross-correlation of the master region around the requested rows
(within a +/-80 pt search window). This works for pages with more than one table.
Output: p3_kit/Z{PDF}.png"""
import io, os, sys
import fitz
import numpy as np
from PIL import Image, ImageDraw
from scipy.signal import fftconvolve
import wide_kit as wk

IA = r"F:/user/Documents/Chat Interl Src/cleanup multilingual/albattani_work_CLAUDE/source_scan/nallino_1899_albattanisivealb00batt.pdf"
argv = [a for a in sys.argv if not a.startswith("y=")]
band = [tuple(float(v) for v in a[2:].split("-")) for a in sys.argv if a.startswith("y=")]   # y=Y0-Y1: the master's table band,
n = int(argv[1]); xr = [float(v) for v in argv[2].split("-")]                               # as for wide_kit (scan edges)
yrs = [[float(v) for v in s.split("-")] for s in argv[3].split(",")]
dpi = int(argv[4]) if len(argv) > 4 else 900
pa = wk.doc[n - 1]; pb = fitz.open(IA)[n - 866]

A = wk.geometry(pa, band[0] if band else None)["table_pt"]; B = wk.geometry(pb)["table_pt"]
s = (B[2] - B[0]) / (A[2] - A[0])                                # IA pt per master pt (table width; robust)


def arr(page, rect, d):
    """Grayscale render at d pixels per inch (float allowed) as a float array."""
    z = d / 72.0
    pix = page.get_pixmap(matrix=fitz.Matrix(z, z), clip=rect)
    return np.asarray(Image.open(io.BytesIO(pix.tobytes("png"))).convert("L"), dtype=np.float32)


def locate(x0, y0, x1, y1):
    """IA position (pt) of the master rectangle, by matching a padded master patch inside a search window.
    The patch spans the full table width: numeral cells repeat from row to row, the names column does not."""
    D = 60                                                       # matching resolution (master dpi)
    pad = 30
    rx0, rx1 = x0, x1
    x0, x1 = min(x0, A[0]), max(x1, A[2])
    tm = arr(pa, fitz.Rect(max(0, x0 - pad), max(0, y0 - pad), min(pa.rect.width, x1 + pad), min(pa.rect.height, y1 + pad)), D)
    gx0, gy0 = max(0, x0 - pad), max(0, y0 - pad)
    # predicted IA location from the frames, then search +/- 80 pt around it
    px = B[0] + (gx0 - A[0]) * s; py = B[1] + (gy0 - A[1]) * s
    sw = fitz.Rect(max(0, px - 80 * s), max(0, py - 80 * s), min(pb.rect.width, px + (tm.shape[1] * 72 / D + 80) * s),
                   min(pb.rect.height, py + (tm.shape[0] * 72 / D + 80) * s))
    im = arr(pb, sw, D / s)                                      # same physical scale as the template
    t = tm - tm.mean()
    if im.shape[0] < t.shape[0] or im.shape[1] < t.shape[1]:
        return px + (rx0 - gx0) * s, py + (y0 - gy0) * s
    num = fftconvolve(im - im.mean(), t[::-1, ::-1], mode="valid")
    ones = np.ones_like(t)
    loc_sum = fftconvolve(im, ones, mode="valid"); loc_sq = fftconvolve(im * im, ones, mode="valid")
    var = np.maximum(loc_sq - loc_sum ** 2 / t.size, 1e-6)
    score = num / np.sqrt(var * (t * t).sum())
    iy, ix = np.unravel_index(np.argmax(score), score.shape)
    bx = sw.x0 + ix * 72 / (D / s); by = sw.y0 + iy * 72 / (D / s)  # IA pt of the padded patch's corner
    return bx + (rx0 - gx0) * s, by + (y0 - gy0) * s


rows = []
for y0, y1 in yrs:
    a = wk.gray(pa, dpi, fitz.Rect(xr[0], y0, xr[1], y1))
    bx, by = locate(xr[0], y0, xr[1], y1)
    r = fitz.Rect(bx, by, bx + (xr[1] - xr[0]) * s, by + (y1 - y0) * s)
    b = Image.fromarray(arr(pb, r, dpi / s).astype(np.uint8))
    rows.append((f"{y0:.0f}", a, b))
W = max(a.width for _, a, _ in rows) + max(b.width for _, _, b in rows) + 90
H = sum(max(a.height, b.height) + 8 for _, a, b in rows)
img = Image.new("L", (W, H), 255); d = ImageDraw.Draw(img); y = 0
wa = max(a.width for _, a, _ in rows)
for lab, a, b in rows:
    d.text((2, y + 6), lab, fill=0); img.paste(a, (50, y)); img.paste(b, (50 + wa + 30, y)); y += max(a.height, b.height) + 8
if img.width > 1990:
    img = img.resize((1990, int(img.height * 1990 / img.width)), Image.LANCZOS)
img.save(os.path.join(wk.OUT, f"Z{n:04}.png")); print(img.size)

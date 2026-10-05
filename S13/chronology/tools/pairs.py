"""Master | Internet Archive copy side by side for a list of small regions of Part III pages (footnote words, cells).
Usage: python pairs.py SPECFILE [dpi] [y=Y0-Y1] [yb=Y0-Y1]
  SPECFILE defines SPEC = [(pdf, label, "x:X0-X1", y_center[, half_height]), ...] in master pt; half_height default 9.
  y=Y0-Y1: the master's table band for the frame detection (scan edges, a second table), as for zoom2.py;
  yb=Y0-Y1: the same band on the IA page (its own pt), needed when the page has two tables.
The IA copy (page = PDF - 865) is aligned as in zoom2.py: scale from the table frame widths, offset per region from a
normalized cross-correlation of a full-width master patch around the region (search window +/-80 pt).
Output: p3_kit/PR_nn.png sheets (label above, master left, IA copy right), each at most ~2000 x 2000 px."""
import io, os, runpy, sys
import fitz
import numpy as np
from PIL import Image, ImageDraw
from scipy.signal import fftconvolve
import wide_kit as wk

IA = r"F:/user/Documents/Chat Interl Src/cleanup multilingual/albattani_work_CLAUDE/source_scan/nallino_1899_albattanisivealb00batt.pdf"
argv = [a for a in sys.argv if not a.startswith(("y=", "yb="))]
band = [tuple(float(v) for v in a[2:].split("-")) for a in sys.argv if a.startswith("y=")]
bandb = [tuple(float(v) for v in a[3:].split("-")) for a in sys.argv if a.startswith("yb=")]
SPEC = runpy.run_path(argv[1])["SPEC"]
DPI = int(argv[2]) if len(argv) > 2 else 1400
ia = fitz.open(IA)
geo = {}


def arr(page, rect, d):
    z = d / 72.0
    pix = page.get_pixmap(matrix=fitz.Matrix(z, z), clip=rect)
    return np.asarray(Image.open(io.BytesIO(pix.tobytes("png"))).convert("L"), dtype=np.float32)


def frames(n):
    if n not in geo:
        pa, pb = wk.doc[n - 1], ia[n - 866]
        A = wk.geometry(pa, band[0] if band else None)["table_pt"]; B = wk.geometry(pb, bandb[0] if bandb else None)["table_pt"]
        geo[n] = (pa, pb, A, B, (B[2] - B[0]) / (A[2] - A[0]))
    return geo[n]


def locate(n, x0, y0, x1, y1):
    pa, pb, A, B, s = frames(n)
    D, pad = 60, 30
    rx0 = x0
    x0, x1 = min(x0, A[0]), max(x1, A[2])
    gx0, gy0 = max(0, x0 - pad), max(0, y0 - pad)
    tm = arr(pa, fitz.Rect(gx0, gy0, min(pa.rect.width, x1 + pad), min(pa.rect.height, y1 + pad)), D)
    px = B[0] + (gx0 - A[0]) * s; py = B[1] + (gy0 - A[1]) * s
    sw = fitz.Rect(max(0, px - 80 * s), max(0, py - 80 * s), min(pb.rect.width, px + (tm.shape[1] * 72 / D + 80) * s),
                   min(pb.rect.height, py + (tm.shape[0] * 72 / D + 80) * s))
    im = arr(pb, sw, D / s)
    t = tm - tm.mean()
    if im.shape[0] < t.shape[0] or im.shape[1] < t.shape[1]:
        return px + (rx0 - gx0) * s, py + (y0 - gy0) * s
    num = fftconvolve(im - im.mean(), t[::-1, ::-1], mode="valid")
    ones = np.ones_like(t)
    ls = fftconvolve(im, ones, mode="valid"); lq = fftconvolve(im * im, ones, mode="valid")
    score = num / np.sqrt(np.maximum(lq - ls ** 2 / t.size, 1e-6) * (t * t).sum())
    iy, ix = np.unravel_index(np.argmax(score), score.shape)
    bx = sw.x0 + ix * 72 / (D / s); by = sw.y0 + iy * 72 / (D / s)
    return bx + (rx0 - gx0) * s, by + (y0 - gy0) * s


items = []
for row in SPEC:
    n, lab, xs, yc = row[:4]
    hh = row[4] if len(row) > 4 else 9
    x0, x1 = [float(v) for v in xs[2:].split("-")]
    y0, y1 = yc - hh, yc + hh
    pa, pb, A, B, s = frames(n)
    a = Image.fromarray(arr(pa, fitz.Rect(x0, y0, x1, y1), DPI).astype(np.uint8))
    bx, by = locate(n, x0, y0, x1, y1)
    b = Image.fromarray(arr(pb, fitz.Rect(bx, by, bx + (x1 - x0) * s, by + (y1 - y0) * s), DPI / s).astype(np.uint8))
    items.append((f"{n} {lab}", a, b))

sheets, cur, h = [], [], 0
for it in items:
    hh = max(it[1].height, it[2].height) + 24
    if cur and h + hh > 1990:
        sheets.append(cur); cur, h = [], 0
    cur.append(it); h += hh
if cur:
    sheets.append(cur)
for k, sh in enumerate(sheets):
    W = max(a.width + b.width for _, a, b in sh) + 40
    H = sum(max(a.height, b.height) + 24 for _, a, b in sh)
    img = Image.new("L", (W, H), 255); d = ImageDraw.Draw(img); y = 0
    for lab, a, b in sh:
        d.text((4, y + 2), lab, fill=0); img.paste(a, (0, y + 20)); img.paste(b, (a.width + 30, y + 20))
        d.line([(a.width + 15, y + 20), (a.width + 15, y + 20 + a.height)], fill=0, width=2)
        y += max(a.height, b.height) + 24
    if img.width > 2000:
        img = img.resize((2000, int(img.height * 2000 / img.width)), Image.LANCZOS)
    img.save(os.path.join(wk.OUT, f"PR_{k:02}.png")); print(f"PR_{k:02}.png", img.size)

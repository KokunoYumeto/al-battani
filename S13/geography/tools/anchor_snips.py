"""Crop the Arabic words in Nallino's Part II notes next to a named Latin word (text-layer anchor).
Spec rows: (pdf, label, anchor, y_approx, side, width_pt[, k]) - the anchor is the k-th word (x order, default 0) whose
text starts with `anchor` on the text line nearest y_approx; side 'a' crops width_pt after it, 'b' before it, 'x' crops
the absolute x-range given as anchor 'x:X0-X1'. Output: p3_kit/AS_{nn}.png sheets (up to ~1900 px tall, 2 columns).
Usage: python anchor_snips.py SPECFILE [dpi]   (SPECFILE: a .py file defining SPEC = [...])"""
import io, runpy, sys
import fitz
from PIL import Image, ImageDraw
import wide_kit as wk

SPEC = runpy.run_path(sys.argv[1])["SPEC"]
DPI = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
words = {}
crops = []
for row in SPEC:
    pdf, lab, anchor, yap, side, w = row[:6]
    k = row[6] if len(row) > 6 else 0
    page = wk.doc[pdf - 1]
    if pdf not in words:
        words[pdf] = page.get_text("words")
    if side == "x":
        x0, x1 = [float(v) for v in anchor[2:].split("-")]
        r = fitz.Rect(x0, yap - 9, x1, yap + 9)
    else:
        line = [q for q in words[pdf] if abs((q[1] + q[3]) / 2 - yap) < 7]
        cand = sorted([q for q in line if q[4].startswith(anchor)], key=lambda q: q[0])
        if len(cand) <= k:
            print("anchor not found:", pdf, lab, anchor, yap); continue
        q = cand[k]; yc = (q[1] + q[3]) / 2
        r = fitz.Rect(q[2] - 1, yc - 9, q[2] + w, yc + 9) if side == "a" else fitz.Rect(q[0] - w, yc - 9, q[0] + 1, yc + 9)
    pix = page.get_pixmap(dpi=DPI, clip=r)
    crops.append((f"{pdf} {lab}", Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")))
sheets = []; cur = []; h = 0
for it in crops:
    if h + it[1].height + 30 > 1900:
        sheets.append(cur); cur = []; h = 0
    cur.append(it); h += it[1].height + 30
if cur:
    sheets.append(cur)
for n in range(0, len(sheets), 2):
    pair = sheets[n:n + 2]
    ws = [max(im.width for _, im in s) + 10 for s in pair]
    H = max(sum(im.height + 30 for _, im in s) for s in pair)
    out = Image.new("L", (sum(ws) + 30, H), 255); d = ImageDraw.Draw(out); x = 0
    for s, wcol in zip(pair, ws):
        y = 0
        for lab, im in s:
            d.text((x + 4, y + 2), lab, fill=0); out.paste(im, (x + 5, y + 22)); y += im.height + 30
        x += wcol + 30
    out.save(wk.OUT + f"AS_{n // 2:02}.png"); print(f"AS_{n // 2:02}.png", out.size)

"""Part III star-table page kit: find the table's vertical rules on the 600-ppi master page and write
(1) the numeric block (magnitude .. longitude columns) at 400 dpi with row guides,
(2) the description block at 260 dpi, split into halves if tall,
(3) the rule positions as JSON. Usage: python p3_page_kit.py PDF [PDF ...]"""
import io, json, sys
import fitz
import numpy as np
from PIL import Image, ImageDraw

import os
MASTER = os.environ.get("P3_SRC", r"F:/user/Documents/CLAUDE PLEASE DONT DELETE WINDOWS 32/grind/nallino_pars123.pdf")
TAG = os.environ.get("P3_TAG", "")   # output prefix for a second copy, e.g. IA
OUT = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani/_intake/tables/p3_kit/"
doc = fitz.open(MASTER)


def gray(page, dpi, clip=None):
    pix = page.get_pixmap(dpi=dpi, clip=clip)
    return Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")


for n in map(int, sys.argv[1:]):
    page = doc[n - 1]
    a8 = np.array(gray(page, 200))                  # 200 dpi working image
    hist = np.bincount(a8.ravel(), minlength=256).astype(float); p_ = hist / hist.sum()
    om = np.cumsum(p_); mu = np.cumsum(p_ * np.arange(256)); mt = mu[-1]
    sb = (mt * om - mu) ** 2 / np.maximum(om * (1 - om), 1e-9)
    thr = min(175, int(np.argmax(sb)))              # Otsu, capped at the old fixed threshold
    g = a8 < thr
    h, w = g.shape
    # vertical rules: columns whose dark run covers most of the table height
    def runs(idx):
        out = []
        for x in idx:
            if not out or x - out[-1][-1] > 2:
                out.append([x])
            else:
                out[-1].append(x)
        return [int(np.mean(r)) for r in out]
    from scipy import ndimage
    lab, nl = ndimage.label(g)
    objs = ndimage.find_objects(lab)
    inside = [i for i in range(nl) if objs[i][0].start > 2 and objs[i][1].start > 2 and objs[i][0].stop < h - 2 and objs[i][1].stop < w - 2]
    # the table frame: union of all long rule-like components (the frame can be broken in some copies)
    longc = [i for i in inside if (objs[i][0].stop - objs[i][0].start) > 0.3 * h or (objs[i][1].stop - objs[i][1].start) > 0.3 * w]
    if not longc:
        longc = [max(inside, key=lambda i: (objs[i][0].stop - objs[i][0].start) * (objs[i][1].stop - objs[i][1].start))]
    y0s = min(objs[i][0].start for i in longc); y1s = max(objs[i][0].stop for i in longc)
    x0s = min(objs[i][1].start for i in longc); x1s = max(objs[i][1].stop for i in longc)
    sl = (slice(y0s, y1s), slice(x0s, x1s))
    top, bot, left, right = sl[0].start, sl[0].stop - 1, sl[1].start, sl[1].stop - 1
    box = g[top:bot + 1, left:right + 1]
    longv = np.zeros_like(box)                         # pixels in vertical runs longer than any glyph
    for x in range(box.shape[1]):
        c = box[:, x]; y = 0
        while y < len(c):
            if c[y]:
                y1 = y
                while y1 < len(c) and c[y1]:
                    y1 += 1
                if y1 - y > 30:
                    longv[y:y1, x] = True
                y = y1
            else:
                y += 1
    spread = ndimage.binary_dilation(longv, structure=np.ones((1, 7), bool))   # tolerate skew
    vx = [x + left for x in runs(np.where(spread.sum(axis=0) > 0.3 * (bot - top))[0])]
    for edge in (left, right):                          # the table edges are always rules
        if all(abs(edge - x) > 10 for x in vx):
            vx.append(edge)
    vx.sort()
    # horizontal rules inside the table: rows dark across most of the width
    rowsum = g[:, left:right].sum(axis=1)
    hrules = [int(y) for y in np.where(rowsum > 0.8 * (right - left))[0]]
    hr = []
    for y in hrules:
        if not hr or y - hr[-1][-1] > 2:
            hr.append([y])
        else:
            hr[-1].append(y)
    hy = [int(np.mean(r)) for r in hr]
    k = 72 / 200
    info = {"pdf": n, "vrules_pt": [round(x * k, 1) for x in vx], "hrules_pt": [round(y * k, 1) for y in hy],
            "table_pt": [round(left * k, 1), round(top * k, 1), round(right * k, 1), round(bot * k, 1)]}
    # the description column is the widest gap between vertical rules (rightmost wide column)
    gaps = [(vx[i + 1] - vx[i], i) for i in range(len(vx) - 1)]
    widest = max(gaps)[1]
    num_r, desc_l, desc_r = vx[widest], vx[widest], vx[widest + 1]
    body_top = top * k + 1                                  # always include the header rows
    body_bot = bot * k
    num_rect = fitz.Rect(left * k - 2, body_top, num_r * k + 2, body_bot + 2)
    desc_rect = fitz.Rect(desc_l * k - 2, body_top, desc_r * k + 2, body_bot + 2)
    info["num_rect"] = [round(v, 1) for v in num_rect]; info["desc_rect"] = [round(v, 1) for v in desc_rect]
    from PIL import ImageDraw
    def ruled(rect, dpi, y0, y1):
        im = gray(page, dpi, fitz.Rect(rect.x0, y0, rect.x1, y1))
        out = Image.new("L", (im.width + 70, im.height), 255); out.paste(im, (70, 0))
        d = ImageDraw.Draw(out); s = dpi / 72
        t = int(y0 // 10 + 1) * 10
        while t < y1:
            yy = int((t - y0) * s); d.line([(52, yy), (68, yy)], fill=0); d.text((2, yy - 6), str(t), fill=0); t += 10
        return out
    band = 1850 / 500 * 72                                  # pt per sheet at 500 dpi
    kn = 0; y = body_top
    while y < body_bot + 2:
        y0 = max(body_top, y - 6); y1 = min(body_bot + 2, y + band)
        ruled(num_rect, 500, y0, y1).save(OUT + f"{TAG}PDF{n:04}_num_{kn}.png")
        ruled(desc_rect, 500, y0, y1).save(OUT + f"{TAG}PDF{n:04}_desc_{kn}.png")
        kn += 1; y += band
    kd = kn
    im = d = gray(page, 72, num_rect)                       # sizes only, for the log line
    W, Hh = page.rect.width, page.rect.height
    gray(page, 150, fitz.Rect(30, 30, W - 30, top * k + 4)).save(OUT + f"{TAG}PDF{n:04}_above.png")    # running head, folio note, title
    gray(page, 300, fitz.Rect(30, bot * k - 2, W - 30, Hh - 25)).save(OUT + f"{TAG}PDF{n:04}_below.png")  # footnotes
    json.dump(info, open(OUT + f"{TAG}PDF{n:04}.json", "w"), indent=1)
    print(n, "table_pt", info["table_pt"], "num", im.size, kn, "chunks; desc", d.size, kd, "chunks")

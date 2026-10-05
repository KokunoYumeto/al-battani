"""Contact sheet of the rows of a calendar page (p2cal.py output) that have mismatches: each line shows the printed
half-row at 500 dpi with the expected values above it. Usage: python calsheet.py PDF [PDF ...] -> p3_kit/CS{PDF}.png"""
import sys, json
import fitz
from PIL import Image, ImageDraw
import wide_kit as wk

for pdf in map(int, sys.argv[1:]):
    d = json.load(open(wk.OUT + f"CAL{pdf}.json", encoding="utf-8"))
    rows = {(r["half"], r["row"]): r for r in d["rows"]}
    keys = sorted({(b[0], b[1]) for b in d["bad"] if b[1] is not None})
    page = wk.doc[pdf - 1]
    items = []
    for half, row in keys:
        r = rows[(half, row)]
        a, b = (d["x0"], d["xmid"] - 1) if half == "L" else (d["xmid"] + 1, d["x1"])
        im = wk.gray(page, 500, fitz.Rect(a, r["y"] - 7, b, r["y"] + 7))
        e = r["expected"]
        lab = f"{pdf} {half}{row}: expected {e['ah']} | {e['wd']} | {e['sy']} | {e['day']} {e['month'] if r['show_name'] else '»'}"
        items.append((lab, im))
    if not items:
        print(pdf, "no mismatches"); continue
    W = max(im.width for _, im in items); H = sum(im.height + 22 for _, im in items)
    out = Image.new("L", (W, H), 255); dr = ImageDraw.Draw(out); y = 0
    for lab, im in items:
        dr.text((4, y + 2), lab, fill=0); out.paste(im, (0, y + 18)); y += im.height + 22
    if out.height > 1990:
        out = out.resize((int(out.width * 1990 / out.height), 1990))
    out.save(wk.OUT + f"CS{pdf}.png"); print(pdf, len(items), out.size)

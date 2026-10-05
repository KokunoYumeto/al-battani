"""Resolve the equation columns of Part II pp. 61-64 by agreement of the two readers (the model of ra_eq_pages.py
departs from the table by up to 7' in smooth runs, so it only chooses among candidates near it): a cell is A when the
glyph reader (confidence >= 0.85) and the text layer give the same number; otherwise its value is the model-resolved
one if any (B), else unknown (C). Writes p3_kit/EQ{pdf}.json {row: {sign index: [values, classes]}} and a contact
sheet p3_kit/EQS_{n}.png of every cell that is not A, with the model value, for reading by eye."""
import json
import fitz
from PIL import Image, ImageDraw
import wide_kit as wk
import ra_eq_pages as M

items = []
for pdf, signs in M.PAGES.items():
    d = json.load(open(wk.OUT + f"MP{pdf}.json", encoding="utf-8"))
    page = wk.doc[pdf - 1]; R = d["rules"]
    res = {}
    for i, r in enumerate(d["rows"]):
        for k, s in enumerate(signs):
            g = r["groups"][2 * k + 1]
            vals, cls = [], ""
            for c in g:
                if c and c["read"] and c["read"] == c.get("tl") and c["conf"] >= 0.85:
                    vals.append(c["read"]); cls += "A"
                elif c and c["value"] is not None:
                    vals.append(c["value"]); cls += "B"
                else:
                    vals.append(None); cls += "C"
            res.setdefault(i + 1, {})[k] = [vals, cls]
            if cls != "AA":
                lam = s + i + 1
                e = M.equation(lam) * 60 - (-1.0)          # the fitted zero point of the model
                im = wk.gray(page, 400, fitz.Rect(R[2 * k + 2] + 1, r["y"] - 6, R[2 * k + 3] - 1, r["y"] + 6))
                lab = f"{pdf} r{i + 1} s{k} {cls} {vals} model {int(e // 60)};{e % 60:04.1f}"
                items.append((lab, im))
    json.dump(res, open(wk.OUT + f"EQ{pdf}.json", "w", encoding="utf-8"))
print(len(items), "cells to read")
per = 60
for s in range(0, len(items), per):
    part = items[s:s + per]
    cw = max(im.width for _, im in part); ch = max(im.height for _, im in part) + 4; LW = 300
    cols = 3; rows = (len(part) + cols - 1) // cols
    out = Image.new("L", (cols * (cw + LW), rows * ch), 255); dr = ImageDraw.Draw(out)
    for j, (lab, im) in enumerate(part):
        x = (j % cols) * (cw + LW); y = (j // cols) * ch
        dr.text((x + 3, y + ch // 2 - 6), lab, fill=0); out.paste(im, (x + LW, y + 2))
    out.save(wk.OUT + f"EQS_{s // per}.png"); print(f"EQS_{s // per}.png", out.size)

"""Find the B cells (one reader gives the resolved value) where the two readers give different numbers that both lie
near the resolved value (within 3 units): the resolution chose the closer of two plausible readings, and the choice
must be confirmed by eye. Writes p3_kit/AMB_{k}.png with a large crop of each such cell and both readings."""
import glob, json, os, re
import fitz
from PIL import Image, ImageDraw
import wide_kit as wk

FILES = ["MP468", "MP469", "MP470", "MP471", "MP472", "MP473", "MP474", "MP475", "MP476", "MP477", "MP478", "MP479",
         "MP480a", "MP480b", "MP480c", "MP481", "MP504s0", "MP504s1", "MP504s2", "MP505s0", "MP505s1", "MP505s2",
         "MP506L", "MP506R", "MP507L", "MP507RA", "MP508s0", "MP508s1", "MP508s2", "MP509s0", "MP509s1", "MP509s2",
         "MP510", "MP511", "MP512", "MP513", "MP514", "MP515", "MP516", "MP517", "MP518", "MP519", "MP520",
         "MP521", "MP522", "MP523", "MP524", "MP525", "MP526", "MP527c", "MP528c", "MP529c", "MP530c", "MP531c", "MP532c"]
items = []
for name in FILES:
    d = json.load(open(wk.OUT + name + ".json", encoding="utf-8"))
    pdf = d["pdf"]; page = wk.doc[pdf - 1]
    for i, r in enumerate(d["rows"]):
        for gi, g in enumerate(r["groups"]):
            for j, c in enumerate(g):
                if c["cls"] != "B" or not c["box"]:
                    continue
                rd, tl, v = c["read"], c["tl"], c["value"]
                if not (rd and tl and rd.isdigit() and tl.isdigit() and rd != tl):
                    continue
                if abs(int(rd) - int(v)) <= 3 and abs(int(tl) - int(v)) <= 3:
                    x0, x1 = c["box"]
                    im = wk.gray(page, 1000, fitz.Rect(x0 - 3, r["y"] - 7, x1 + 3, r["y"] + 7))
                    items.append((f"{name} r{i + 1} g{gi} p{j}: chosen {v} | glyph {rd} | text {tl}", im))
print(len(items), "ambiguous cells")
per = 40
for s in range(0, len(items), per):
    part = items[s:s + per]
    part = [(lab, im.resize((max(1, im.width // 2), max(1, im.height // 2)))) for lab, im in part]
    cw = max(im.width for _, im in part); ch = max(im.height for _, im in part) + 6; LW = 330
    cols = 4; rows = (len(part) + cols - 1) // cols
    out = Image.new("L", (cols * (cw + LW), rows * ch), 255); dr = ImageDraw.Draw(out)
    for k, (lab, im) in enumerate(part):
        x = (k % cols) * (cw + LW); y = (k // cols) * ch
        dr.text((x + 3, y + ch // 2 - 6), lab, fill=0); out.paste(im, (x + LW, y + 3))
    out.save(wk.OUT + f"AMB_{s // per}.png"); print(f"AMB_{s // per}.png", out.size)

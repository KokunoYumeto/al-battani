"""Second pass over the calendar pages read by p2cal.py: classify every cell.
  A: the glyph reader equals the computed value with confidence >= 0.85, and the text layer is empty or agrees;
  B: only one reader agrees, or the agreement has low confidence -> shown on a contact sheet for a visual check;
  C: neither agrees -> anomaly candidates (also on the sheet).
Usage: python calverify.py PDF [PDF ...]  -> counts, and p3_kit/CV{PDF}_{k}.png sheets of the B and C cells
(each cell crop with its computed value)."""
import sys, json
import fitz
from PIL import Image, ImageDraw
import wide_kit as wk

KEYS = (("ah", "ah"), ("wd", "wd"), ("sy", "sy"), ("dm", "day"))
tot = {"A": 0, "B": 0, "C": 0}
for pdf in map(int, sys.argv[1:]):
    d = json.load(open(wk.OUT + f"CAL{pdf}.json", encoding="utf-8"))
    page = wk.doc[pdf - 1]
    items, cnt = [], {"A": 0, "B": 0, "C": 0}
    for r in d["rows"]:
        for k, ek in KEYS:
            exp = str(r["expected"][ek]); rd = r["read"][k]; tl = r["alt"][k]; cf = r["conf"][k] or 0
            if rd == exp and cf >= 0.85 and (not tl or tl == exp):
                cls = "A"
            elif rd == exp or tl == exp:
                cls = "B"
            else:
                cls = "C"
            cnt[cls] += 1
            if cls != "A" and r["cells"][k]:
                x0, x1 = r["cells"][k]
                im = wk.gray(page, 500, fitz.Rect(x0 - 3, r["y"] - 7, x1 + 3, r["y"] + 7))
                items.append((f"{cls} {r['half']}{r['row']} {k}: {exp}", im))
            elif cls != "A":
                items.append((f"{cls} {r['half']}{r['row']} {k}: {exp} (no token)", None))
    for c in cnt:
        tot[c] += cnt[c]
    print(pdf, cnt)
    cells = [it for it in items if it[1] is not None]
    for it in items:
        if it[1] is None:
            print("   no token:", it[0])
    per = 60
    for s in range(0, len(cells), per):
        part = cells[s:s + per]
        part = [(lab, im.resize((int(im.width * 0.6), int(im.height * 0.6)))) for lab, im in part]
        cw = max(im.width for _, im in part) + 10; chh = max(im.height for _, im in part) + 8
        ncol = 5; nrow = (len(part) + ncol - 1) // ncol
        LW = 130
        out = Image.new("L", (ncol * (cw + LW), nrow * chh), 255); dr = ImageDraw.Draw(out)
        for i, (lab, im) in enumerate(part):
            x = (i % ncol) * (cw + LW); y = (i // ncol) * chh
            dr.text((x + 2, y + chh // 2 - 6), lab.split(": ")[0][2:] + " = " + lab.split(": ")[1], fill=0)
            out.paste(im, (x + LW, y + 4))
        out.save(wk.OUT + f"CV{pdf}_{s // per}.png")
print("total", tot)

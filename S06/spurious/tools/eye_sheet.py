"""Contact sheet of the cells of a reading (MP{name}.json) that are not in class A, with the computed value and the
readings of both readers, for reading by eye: three columns of large labels and 450 dpi crops.
Usage: python eye_sheet.py NAME [--all] -> p3_kit/EYE_{NAME}_k.png
sheet(name, expected=None, labels=None): expected(i, gi) gives the computed value of a group as text; labels(i, gi)
names the cell (default row and group)."""
import json, sys
import fitz
from PIL import Image, ImageDraw, ImageFont
import wide_kit as wk


def sheet(name, show_all=False, per=45, labels=None, expected=None, dpi=450, skip=()):
    d = json.load(open(wk.OUT + f"MP{name}.json", encoding="utf-8"))
    R = d["rules"]; page = wk.doc[d["pdf"] - 1]
    items = []
    for i, r in enumerate(d["rows"]):
        for gi, g in enumerate(r["groups"]):
            if gi in skip or (not show_all and all(c["cls"] == "A" for c in g)):
                continue
            exp = expected(i, gi) if expected else " ".join(c["value"] or "?" for c in g)
            cls = "".join(c["cls"] for c in g)
            rd = " ".join((c["read"] or "-") for c in g); tl = " ".join((c["tl"] or "-") for c in g)
            im = wk.gray(page, dpi, fitz.Rect(R[gi + 1] - 1, r["y"] - 9, R[gi + 2] + 1, r["y"] + 10))
            lab = labels(i, gi) if labels else f"r{i + 1} g{gi}"
            items.append((lab, f"{cls}  computed {exp}", f"glyph {rd} | text {tl}", im))
    big = ImageFont.truetype("arial.ttf", 30); small = ImageFont.truetype("arial.ttf", 20)
    files = []
    for k in range(0, len(items), per):
        part = items[k:k + per]
        cw = max(im.width for *_, im in part); ch = max(max(im.height for *_, im in part), 90) + 12; LW = 330
        cols = 3; rows = (len(part) + cols - 1) // cols
        img = Image.new("L", (cols * (cw + LW + 20), rows * ch), 255); dr = ImageDraw.Draw(img)
        for j, (lab, l2, l3, im) in enumerate(part):
            x = (j % cols) * (cw + LW + 20); y = (j // cols) * ch
            dr.text((x + 4, y + 4), lab, fill=0, font=big)
            dr.text((x + 4, y + 40), l2, fill=0, font=small)
            dr.text((x + 4, y + 64), l3, fill=0, font=small)
            img.paste(im, (x + LW, y + 4))
        f = wk.OUT + f"EYE_{name}_{k // per}.png"; img.save(f); files.append(f)
    return len(items), files


if __name__ == "__main__":
    print(sheet(sys.argv[1], "--all" in sys.argv))

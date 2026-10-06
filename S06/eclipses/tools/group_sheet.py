"""Contact sheet of whole flagged groups (all places of a column in one crop) for reading by eye, with the glyph
reading, the text-layer reading and the expected value. group_sheet(pdfs, tag, name, expected) where
expected(pdf, row_index, group_index) -> str (or ""). Writes p3_kit/{name}_{k}.png."""
import json
import fitz
from PIL import Image, ImageDraw
import wide_kit as wk


def group_sheet(pdfs, tag, name, expected=None, per=45, dpi=400):
    items = []
    for pdf in pdfs:
        d = json.load(open(wk.OUT + f"MP{pdf}{tag}.json", encoding="utf-8"))
        R = d["rules"]; page = wk.doc[pdf - 1]
        flagged = sorted({(int(f[0]), int(f[1])) for f in d["flags"] if f[0] != "fit"})
        for i, gi in flagged:
            r = d["rows"][i]
            cells = r["groups"][gi]
            rd = " ".join(c["read"] if c["read"] else "-" for c in cells)
            tl = " ".join(c["tl"] if c["tl"] else "-" for c in cells)
            im = wk.gray(page, dpi, fitz.Rect(R[gi + 1] + 1, r["y"] - 7, R[gi + 2] - 1, r["y"] + 7))
            exp = expected(pdf, i, gi) if expected else ""
            items.append((f"{pdf} r{i + 1} g{gi} | {rd} | tl {tl} | exp {exp}", im))
    files = []
    for s in range(0, len(items), per):
        part = items[s:s + per]
        cw = max(im.width for _, im in part); ch = max(im.height for _, im in part) + 6; LW = 330
        cols = 3; rows = (len(part) + cols - 1) // cols
        out = Image.new("L", (cols * (cw + LW), rows * ch), 255); dr = ImageDraw.Draw(out)
        for j, (lab, im) in enumerate(part):
            x = (j % cols) * (cw + LW); y = (j // cols) * ch
            dr.text((x + 3, y + ch // 2 - 6), lab, fill=0); out.paste(im, (x + LW, y + 3))
        f = wk.OUT + f"{name}_{s // per}.png"; out.save(f); files.append(f)
    return len(items), files

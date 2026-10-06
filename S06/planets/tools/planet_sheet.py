"""Contact sheets of the flagged groups of the planetary equation pages (MP{pdf}b.json), with the readings of both
readers and the value the empirical curve predicts (degrees and minutes), for reading by eye. Output p3_kit/PLS_{k}.png"""
import json, re
import fitz
from PIL import Image, ImageDraw, ImageFont
import wide_kit as wk

COLS = ["II", "III", "IV", "V", "VI", "VII"]
NSUB = [1, 2, 1, 2, 2, 2]


def fmt(units, nsub):
    units = round(units)
    return f"{units // 60}° {units % 60}′" if nsub == 2 else str(units)


def items(tag="b"):
    out = []
    for pdf in range(557, 587):
        d = json.load(open(wk.OUT + f"MP{pdf}{tag}.json", encoding="utf-8"))
        R = d["rules"]; page = wk.doc[pdf - 1]
        for f in d["flags"]:
            if f[0] == "fit":
                continue
            i, gi = int(f[0]), int(f[1])
            m = re.search(r"predicted ([\d.]+)", f[2])
            pred = fmt(float(m.group(1)), NSUB[gi]) if m else "?"
            r = d["rows"][i]
            cells = r["groups"][gi]
            rd = " ".join(c["read"] or "-" for c in cells); tl = " ".join(c["tl"] or "-" for c in cells)
            im = wk.gray(page, 400, fitz.Rect(R[gi + 1] + 1, r["y"] - 8, R[gi + 2] - 1, r["y"] + 7))
            n = 30 * ((pdf - 557) % 6) + i + 1
            out.append((pdf, i, gi, f"{pdf} r{i + 1} n={n} {COLS[gi]}  glyph {rd}  tl {tl}  curve {pred}", im))
    return out


if __name__ == "__main__":
    font = ImageFont.truetype("arial.ttf", 22)
    its = items()
    per = 36
    for k in range(0, len(its), per):
        part = its[k:k + per]
        W = 1300; H = sum(max(im.height, 40) + 8 for *_, im in part)
        img = Image.new("RGB", (W, H), "white"); dr = ImageDraw.Draw(img); y = 0
        for pdf, i, gi, lab, im in part:
            dr.text((5, y + 10), lab, fill="black", font=font)
            img.paste(im, (820, y)); y += max(im.height, 40) + 8
        img.save(wk.OUT + f"PLS_{k // per}.png")
    print(len(its), "items")

"""Audit of the class-A cells that only the glyph reader saw. motion_page.run classes a cell A when the glyph reader is
confident and gives the value and the OCR text layer gives the same value OR has no token there; in the second case
only one reader saw the number. This script finds those cells in the reading files the build scripts use
(build_inputs.json, from a traced run of the builds), re-reads each with Tesseract (600 dpi crop, digits only, as
third_reader.py), and writes contact sheets of the cells where Tesseract does not give the value (p3_kit/GO_{k}.png),
for reading by eye. Usage: python audit_glyph_only.py build_inputs.json [--sheets]"""
import json, os, subprocess, sys, tempfile
from collections import Counter, defaultdict
import fitz
from PIL import Image, ImageDraw, ImageFont
import wide_kit as wk

TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TMP = tempfile.mkdtemp(dir=wk.OUT)


def tess(im, psm=7):
    p = os.path.join(TMP, "c.png")
    w, h = im.size
    canvas = Image.new("L", (w + 40, h + 40), 255); canvas.paste(im, (20, 20)); canvas.save(p)
    r = subprocess.run([TESS, p, "stdout", "--psm", str(psm), "-c", "tessedit_char_whitelist=0123456789"],
                       capture_output=True, text=True)
    return "".join(ch for ch in r.stdout if ch.isdigit())


def glyph_only(name):
    d = json.load(open(wk.OUT + name, encoding="utf-8"))
    out = []
    if "rows" not in d:
        return d, out
    for i, r in enumerate(d["rows"]):
        for gi, g in enumerate(r.get("groups", [])):
            for j, c in enumerate(g):
                if c and c.get("cls") == "A" and not c.get("tl") and c.get("box"):
                    out.append((i, gi, j, c, r["y"]))
    return d, out


if __name__ == "__main__":
    inputs = json.load(open(sys.argv[1], encoding="utf-8"))
    per_script, items, totals = defaultdict(Counter), [], Counter()
    for script, info in inputs.items():
        for name in info["inputs"]:
            if not name.startswith("MP"):
                continue
            d, cells = glyph_only(name)
            nA = sum(1 for r in d.get("rows", []) for g in r.get("groups", []) for c in g if c and c.get("cls") == "A")
            per_script[script]["A"] += nA
            per_script[script]["glyph only"] += len(cells)
            page = wk.doc[d["pdf"] - 1]
            for i, gi, j, c, y in cells:
                x0, x1 = c["box"]
                clip = fitz.Rect(x0 - 2, y - 6.5, x1 + 2, y + 6.5) & page.rect
                if clip.is_empty or clip.width < 1:
                    t = ""
                else:
                    t = tess(wk.gray(page, 600, clip))
                totals["checked"] += 1
                if t == c["value"]:
                    totals["agree"] += 1
                    continue
                if t == "" or len(c["value"]) == 1:          # single digits: Tesseract often fails on a lone digit
                    t2 = tess(wk.gray(page, 600, clip), psm=10) if not clip.is_empty else ""
                    if t2 == c["value"]:
                        totals["agree"] += 1
                        continue
                    t = t or t2
                items.append((script, name, i, gi, j, c["value"], t,
                              wk.gray(page, 500, fitz.Rect(x0 - 4, y - 8, x1 + 4, y + 8))))
    for script, cnt in per_script.items():
        print(f"{script}: A {cnt['A']}, glyph only {cnt['glyph only']}")
    print("glyph-only cells", totals["checked"], "Tesseract agrees", totals["agree"], "differs", len(items))
    json.dump([(s, n, i, gi, j, v, t) for s, n, i, gi, j, v, t, _ in items],
              open(wk.OUT + "GO_items.json", "w", encoding="utf-8"))
    if "--sheets" in sys.argv:
        font = ImageFont.truetype("arial.ttf", 22)
        per = 60
        for k in range(0, len(items), per):
            part = items[k:k + per]
            cw = max(im.width for *_, im in part); ch = max(max(im.height for *_, im in part), 50) + 10
            cols = 3; rows = (len(part) + cols - 1) // cols; LW = 330
            img = Image.new("L", (cols * (cw + LW + 20), rows * ch), 255); dr = ImageDraw.Draw(img)
            for q, (s, n, i, gi, j, v, t, im) in enumerate(part):
                x = (q % cols) * (cw + LW + 20); y = (q // cols) * ch
                dr.text((x + 4, y + 2), f"{n[:-5]} r{i + 1} g{gi} p{j}", fill=0, font=font)
                dr.text((x + 4, y + 26), f"value {v}  tess {t or '-'}", fill=0, font=font)
                img.paste(im, (x + LW, y + 4))
            img.save(wk.OUT + f"GO_{k // per}.png")
            print(f"GO_{k // per}.png", img.size)

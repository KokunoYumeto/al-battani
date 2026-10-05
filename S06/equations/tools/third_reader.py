"""A third, independent reading of every B cell (one reader gives the resolved value): Tesseract on a 600 dpi crop of
the single cell (psm 7, digits only). Cells where Tesseract does not give the resolved value are written to contact
sheets with large labels (p3_kit/TR_{k}.png) for reading by eye. Usage: python third_reader.py [json names...]"""
import json, os, subprocess, sys, tempfile
import fitz
from PIL import Image, ImageDraw, ImageFont
import wide_kit as wk
from ambiguous_b import FILES

TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TMP = tempfile.mkdtemp(dir=wk.OUT)


def tess(im):
    p = os.path.join(TMP, "c.png")
    w, h = im.size
    canvas = Image.new("L", (w + 40, h + 40), 255); canvas.paste(im, (20, 20)); canvas.save(p)
    r = subprocess.run([TESS, p, "stdout", "--psm", "7", "-c", "tessedit_char_whitelist=0123456789"],
                       capture_output=True, text=True)
    return "".join(ch for ch in r.stdout if ch.isdigit())


names = sys.argv[1:] or FILES
items, n_b, n_ok = [], 0, 0
for name in names:
    d = json.load(open(wk.OUT + name + ".json", encoding="utf-8"))
    pdf = d["pdf"]; page = wk.doc[pdf - 1]
    for i, r in enumerate(d["rows"]):
        for gi, g in enumerate(r["groups"]):
            for j, c in enumerate(g):
                if c["cls"] != "B" or not c["box"]:
                    continue
                n_b += 1
                x0, x1 = c["box"]
                im = wk.gray(page, 600, fitz.Rect(x0 - 2, r["y"] - 6.5, x1 + 2, r["y"] + 6.5))
                t = tess(im)
                if t == c["value"]:
                    n_ok += 1
                    continue
                big = wk.gray(page, 900, fitz.Rect(x0 - 3, r["y"] - 7, x1 + 3, r["y"] + 7))
                items.append((f"{name} r{i + 1} g{gi} p{j}", c["value"], f"glyph {c['read']} text {c['tl']} tess {t}", big))
print(f"B cells {n_b}: Tesseract agrees {n_ok}, differs {len(items)}")
try:
    font = ImageFont.truetype("arial.ttf", 30); small = ImageFont.truetype("arial.ttf", 14)
except OSError:
    font = small = ImageFont.load_default()
per = 30
for s in range(0, len(items), per):
    part = items[s:s + per]
    cw = max(im.width for *_, im in part); ch = max(max(im.height for *_, im in part), 60) + 8; LW = 300
    cols = 3; rows = (len(part) + cols - 1) // cols
    out = Image.new("L", (cols * (cw + LW), rows * ch), 255); dr = ImageDraw.Draw(out)
    for k, (lab, val, extra, im) in enumerate(part):
        x = (k % cols) * (cw + LW); y = (k // cols) * ch
        dr.text((x + 4, y + 2), lab, fill=0, font=small)
        dr.text((x + 4, y + 18), extra, fill=0, font=small)
        dr.text((x + 180, y + 16), val, fill=0, font=font)
        out.paste(im, (x + LW, y + 4))
    out.save(wk.OUT + f"TR_{s // per}.png"); print(f"TR_{s // per}.png", out.size)

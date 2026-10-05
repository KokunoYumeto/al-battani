"""Extra crops for one page pair, after p3_page_kit.py N and p2_page_kit.py P:
  p3_kit/x{N}_fn_K.png   Part III footnotes below the table, 800 dpi, in halves (Arabic words are small)
  p3_kit/x{P}_notes_K.png Part II notes, 520 dpi, left and right halves, at most ~1000 px high each
  p3_kit/x{P}_head.png   Part II running head and anything above the table, 300 dpi
Usage: python pair_extra.py N P"""
import io, json, sys
import fitz
from PIL import Image

MASTER = r"F:/user/Documents/CLAUDE PLEASE DONT DELETE WINDOWS 32/grind/nallino_pars123.pdf"
KIT = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani/_intake/tables/p3_kit/"
n, P = int(sys.argv[1]), int(sys.argv[2])
doc = fitz.open(MASTER)


def g(page, r, dpi):
    return Image.open(io.BytesIO(page.get_pixmap(dpi=dpi, clip=r).tobytes("png"))).convert("L")


# Part III footnotes
p3 = doc[n - 1]; info = json.load(open(KIT + f"PDF{n:04}.json"))
ty1 = info["table_pt"][3]
ws = [w for w in p3.get_text("words") if w[1] > ty1 + 4 and w[3] < p3.rect.height - 40]
if ws:
    y0 = min(w[1] for w in ws) - 4; y1 = max(w[3] for w in ws) + 4
    x0 = min(w[0] for w in ws) - 4; x1 = max(w[2] for w in ws) + 4
    mid = (x0 + x1) / 2
    for k, (a, b) in enumerate(((x0, mid + 6), (mid - 6, x1))):
        g(p3, fitz.Rect(a, y0, b, y1), 800).save(KIT + f"x{n}_fn_{k}.png")
    print("Part III footnote area", round(y0), round(y1))
# Part II notes and head
p2 = doc[P - 1]
words = p2.get_text("words")
tab = [w for w in words if w[4].startswith("Stellarum")]
top = tab[0][1] - 8 if tab else 100
g(p2, fitz.Rect(30, 40, p2.rect.width - 30, top), 300).save(KIT + f"x{P}_head.png")
nums = [w for w in words if w[1] > 300 and w[4].rstrip(".").isdigit() and w[4].endswith(".") and w[0] < 140]
info2 = json.load(open(KIT + f"P2_{P:04}.json")) if False else None
ys = sorted(w[1] for w in words)
# notes start below the table: the first line whose y is beyond the last table row (largest gap search)
body = [w for w in words if 100 < w[1] < p2.rect.height - 50]
body.sort(key=lambda w: w[1])
gaps = [(body[i + 1][1] - body[i][3], i) for i in range(len(body) - 1)]
# the notes block: from the line after the largest vertical gap below y=300 to the end of the text
import re
marks = [w[1] for w in body if w[0] < 260 and w[1] > 200 and (re.fullmatch(r"\d+\.", w[4]) or w[4].endswith(":"))]
if len(sys.argv) > 3:
    ny0 = float(sys.argv[3])                  # explicit notes top in pt
elif marks:
    ny0 = min(marks) - 8                      # note numbers carry a period, table row numbers do not
else:
    ny0 = 500
ny1 = max(w[3] for w in body) + 6
xs0 = min(w[0] for w in body if w[1] >= ny0) - 4; xs1 = max(w[2] for w in body if w[1] >= ny0) + 4
mid = (xs0 + xs1) / 2
step = 1000 / 520 * 72
k = 0
y = ny0
while y < ny1 and k < 6:                      # chunks overlap by 4 pt; the last one ends at ny1
    yb = min(ny1, y + step)
    for half, (a, b) in enumerate(((xs0, mid + 10), (mid - 10, xs1))):
        g(p2, fitz.Rect(a, y, b, yb), 520).save(KIT + f"x{P}_notes_{k}{'ab'[half]}.png")
    k += 1
    if yb >= ny1:
        break
    y = yb - 4
print("Part II notes", round(ny0), round(ny1), "chunks", k)

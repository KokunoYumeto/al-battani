"""Part II geography page kit: full-width crops of the table (300 dpi) and of the notes (280 dpi), in chunks of at most
1800 px height, with a pt ruler. The notes start at the first line beginning with "Nr." at the left margin.
Usage: python p2_geo_kit.py P [P ...]   ->  p3_kit/G{P}_tab_k.png, p3_kit/G{P}_notes_k.png"""
import io, os, sys
import fitz
from PIL import Image, ImageDraw

MASTER = r"F:/user/Documents/CLAUDE PLEASE DONT DELETE WINDOWS 32/grind/nallino_pars123.pdf"
KIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "p3_kit") + os.sep
doc = fitz.open(MASTER)


def ruled(page, x0, x1, y0, y1, dpi):
    im = Image.open(io.BytesIO(page.get_pixmap(dpi=dpi, clip=fitz.Rect(x0, y0, x1, y1)).tobytes("png"))).convert("L")
    out = Image.new("L", (im.width + 60, im.height), 255); out.paste(im, (60, 0))
    d = ImageDraw.Draw(out); s = dpi / 72
    t = int(y0 // 10 + 1) * 10
    while t < y1:
        yy = int((t - y0) * s); d.line([(44, yy), (58, yy)], fill=0); d.text((2, yy - 6), str(t), fill=0); t += 10
    return out


def chunks(page, x0, x1, y0, y1, dpi, tag):
    band = 1800 / dpi * 72
    k = 0; y = y0
    while y < y1:
        b = min(y1, y + band)
        ruled(page, x0, x1, y - 2 if k else y, b, dpi).save(KIT + f"{tag}_{k}.png")
        k += 1; y = b - 4 if b < y1 else b
    return k


for P in map(int, sys.argv[1:]):
    page = doc[P - 1]
    words = page.get_text("words")
    W, H = page.rect.width, page.rect.height
    body = [w for w in words if 60 < w[1] < H - 45]
    nr = [w[1] for w in body if w[4].startswith("Nr") and w[0] < 120 and w[1] > 150]
    notes_y = min(nr) - 5 if nr else H - 45
    top = min(w[1] for w in body) - 6
    x0 = max(20, min(w[0] for w in body) - 8); x1 = min(W - 10, max(w[2] for w in body) + 8)
    for f in os.listdir(KIT):
        if f.startswith(f"G{P}_"):
            os.remove(KIT + f)
    kt = chunks(page, x0, x1, top, notes_y, 300, f"G{P}_tab")
    last = max((w[3] for w in body if w[1] >= notes_y), default=notes_y) + 5
    kn = chunks(page, x0, x1, notes_y, last, 280, f"G{P}_notes") if last > notes_y + 5 else 0
    print(P, "table", round(top), "-", round(notes_y), "chunks", kt, "| notes to", round(last), "chunks", kn)

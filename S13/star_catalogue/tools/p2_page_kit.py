"""Part II star-table page kit: find the table (largest ruling network), then write
  P2_####_table_K.png : the whole table incl. star numbers and identifications at 230 dpi (chunks <= 1850 px)
  P2_####_notes_K.png : everything below the table (Nallino's notes) at 300 dpi
Usage: python p2_page_kit.py PDF [PDF ...]"""
import io, sys
import fitz
import numpy as np
from PIL import Image
from scipy import ndimage

MASTER = r"F:/user/Documents/CLAUDE PLEASE DONT DELETE WINDOWS 32/grind/nallino_pars123.pdf"
OUT = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani/_intake/tables/p3_kit/"
doc = fitz.open(MASTER)


def gray(page, dpi, clip):
    pix = page.get_pixmap(dpi=dpi, clip=clip)
    return Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")


def chunks(im, name, maxh=1850, overlap=40):
    k, y = 0, 0
    while y < im.height:
        im.crop((0, max(0, y - (overlap if y else 0)), im.width, min(im.height, y + maxh))).save(OUT + f"{name}_{k}.png")
        k += 1; y += maxh
    return k


for n in map(int, sys.argv[1:]):
    page = doc[n - 1]
    W, H = page.rect.width, page.rect.height
    g = np.array(gray(page, 200, page.rect)) < 175
    h, w = g.shape
    lab, nl = ndimage.label(g)
    objs = ndimage.find_objects(lab)
    inside = [i for i in range(nl) if objs[i][0].start > 2 and objs[i][1].start > 2 and objs[i][0].stop < h - 2 and objs[i][1].stop < w - 2]
    big = max(inside, key=lambda i: (objs[i][0].stop - objs[i][0].start) * (objs[i][1].stop - objs[i][1].start))
    sl = objs[big]; k = 72 / 200
    top, bot, left, right = sl[0].start * k, sl[0].stop * k, sl[1].start * k, sl[1].stop * k
    kt = chunks(gray(page, 230, fitz.Rect(max(20, left - 40), top - 4, min(W - 10, right + 40), bot + 3)), f"P2_{n:04}_table")
    kn = chunks(gray(page, 300, fitz.Rect(30, bot + 2, W - 30, H - 20)), f"P2_{n:04}_notes")
    print(n, "table pt", [round(v) for v in (left, top, right, bot)], "chunks table/notes:", kt, kn)

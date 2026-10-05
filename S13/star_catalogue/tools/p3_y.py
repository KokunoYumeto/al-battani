"""Crop a Part III table page by pt ranges, stacked: python p3_y.py PDF part:y0-y1[:dpi] [part:y0-y1[:dpi] ...]
part = full | desc | num | x0-x1 (explicit pt columns). Default dpi 600 (full: 300). Output p3_kit/PDF####_y.png"""
import io, json, os, sys
import fitz
from PIL import Image, ImageDraw

MASTER = os.environ.get("P3_SRC", r"F:/user/Documents/CLAUDE PLEASE DONT DELETE WINDOWS 32/grind/nallino_pars123.pdf")
TAG = os.environ.get("P3_TAG", "")
KIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "p3_kit") + os.sep
n = int(sys.argv[1]); info = json.load(open(KIT + f"{TAG}PDF{n:04}.json")); page = fitz.open(MASTER)[n - 1]
items = []
for spec in sys.argv[2:]:
    parts = spec.split(":")
    part, yr = parts[0], parts[1]
    y0, y1 = (float(v) for v in yr.split("-"))
    if part == "full":
        x0, x1, dpi = info["table_pt"][0] - 2, info["table_pt"][2] + 2, 300
    elif part == "desc":
        x0, x1, dpi = info["desc_rect"][0], info["desc_rect"][2], 600
    elif part == "num":
        x0, x1, dpi = info["num_rect"][0], info["num_rect"][2], 600
    else:
        x0, x1 = (float(v) for v in part.split("-")); dpi = 600
    if len(parts) > 2:
        dpi = int(parts[2])
    im = Image.open(io.BytesIO(page.get_pixmap(dpi=dpi, clip=fitz.Rect(x0, y0, x1, y1)).tobytes("png"))).convert("L")
    if im.width > 1960:
        im = im.crop((im.width - 1960, 0, im.width, im.height))
    items.append((spec, im))
W = max(i.width for _, i in items) + 10; H = sum(i.height + 8 for _, i in items) + 12 * len(items)
s = Image.new("L", (W, H), 255); d = ImageDraw.Draw(s); y = 0
for lab, im in items:
    d.text((2, y), lab, fill=0); y += 12; s.paste(im, (W - im.width, y)); y += im.height + 8
s.save(KIT + f"{TAG}PDF{n:04}_y.png"); print(s.size)

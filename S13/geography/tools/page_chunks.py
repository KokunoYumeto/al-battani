"""Render a page region in ruled horizontal chunks (pt ticks on the left), for reading at a fixed resolution.
Usage: python page_chunks.py PDF [y0-y1] [x0-x1] [dpi] [tag]
Output: p3_kit/{tag}{PDF}_{k}.png. The loop advances by the band height minus a 4 pt overlap and stops at y1;
at most 40 chunks are written in any case."""
import io, sys
import fitz
from PIL import Image, ImageDraw
import wide_kit as wk

n = int(sys.argv[1]); page = wk.doc[n - 1]; W, H = page.rect.width, page.rect.height
y0, y1 = [float(v) for v in sys.argv[2].split("-")] if len(sys.argv) > 2 else (60, H - 30)
x0, x1 = [float(v) for v in sys.argv[3].split("-")] if len(sys.argv) > 3 else (40, W - 30)
dpi = int(sys.argv[4]) if len(sys.argv) > 4 else 300
tag = sys.argv[5] if len(sys.argv) > 5 else "C"


def ruled(a, b):
    im = Image.open(io.BytesIO(page.get_pixmap(dpi=dpi, clip=fitz.Rect(x0, a, x1, b)).tobytes("png"))).convert("L")
    out = Image.new("L", (im.width + 60, im.height), 255); out.paste(im, (60, 0))
    d = ImageDraw.Draw(out); s = dpi / 72
    t = int(a // 10 + 1) * 10
    while t < b:
        yy = int((t - a) * s); d.line([(44, yy), (58, yy)], fill=0); d.text((2, yy - 6), str(t), fill=0); t += 10
    return out


band = 1800 / dpi * 72
y = y0; k = 0
while y < y1 and k < 40:
    b = min(y1, y + band)
    ruled(y, b).save(wk.OUT + f"{tag}{n}_{k}.png")
    k += 1
    if b >= y1:
        break
    y = b - 4
print(f"{tag}{n}: {k} chunks")

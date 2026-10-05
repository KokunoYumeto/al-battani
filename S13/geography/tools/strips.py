"""Read one printed line at high resolution: cut it into segments and stack them, right to left or left to right.
Usage: python strips.py PDF x0-x1 y0-y1[,y0-y1...] [seg_pt] [dpi] [rtl]
  PDF: master page number (1-based); x/y in pt; seg_pt: segment width (default 95); dpi (default 1600);
  rtl: stack the segments from the right edge leftwards (for Arabic reading order).
Output: p3_kit/S{PDF}_{k}.png, one image per y-range, each segment labelled with its x range (pt)."""
import io, sys
import fitz
from PIL import Image, ImageDraw
import wide_kit as wk

n = int(sys.argv[1]); x0, x1 = [float(v) for v in sys.argv[2].split("-")]
yrs = [[float(v) for v in s.split("-")] for s in sys.argv[3].split(",")]
seg = float(sys.argv[4]) if len(sys.argv) > 4 else 95.0
dpi = int(sys.argv[5]) if len(sys.argv) > 5 else 1600
rtl = len(sys.argv) > 6 and sys.argv[6] == "rtl"
page = wk.doc[n - 1]
for k, (y0, y1) in enumerate(yrs):
    cuts = []
    a = x0
    while a < x1 - 1:
        b = min(x1, a + seg)
        cuts.append((a - 3, b + 3))                                  # 3 pt overlap so no glyph is split unseen
        a = b
    if rtl:
        cuts.reverse()
    ims = []
    for a, b in cuts:
        pix = page.get_pixmap(dpi=dpi, clip=fitz.Rect(a, y0, b, y1))
        ims.append((f"{a:.0f}-{b:.0f}", Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")))
    W = max(im.width for _, im in ims) + 80
    H = sum(im.height + 10 for _, im in ims)
    out = Image.new("L", (W, H), 255); d = ImageDraw.Draw(out); y = 0
    for lab, im in ims:
        d.text((2, y + 4), lab, fill=0); out.paste(im, (80, y)); y += im.height + 10
    out.save(wk.OUT + f"S{n:04}_{k}.png"); print(f"S{n:04}_{k}.png", out.size)

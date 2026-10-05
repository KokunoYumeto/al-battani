"""Trace the abjad zero sign (ring with a bar above) from the 600-ppi master scan and build a one-glyph
OpenType font, NallinoSigns.otf, with the glyph at U+E000 (Private Use Area).

Source: master PDF 885 (Part III, printed p. 267), Cetus row 3, longitude-degree cell."""
import io
import fitz
import numpy as np
import potrace
from PIL import Image
from scipy import ndimage
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen

MASTER = r"F:/user/Documents/CLAUDE PLEASE DONT DELETE WINDOWS 32/grind/nallino_pars123.pdf"
OUT = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani/_intake/s02_audit/pilot_hard/fonts/NallinoSigns.otf"

page = fitz.open(MASTER)[884]
pix = page.get_pixmap(dpi=600, clip=fitz.Rect(280, 265, 302, 283))
a = np.array(Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")) < 128
lab, n = ndimage.label(a)
keep = np.zeros_like(a)
for i, sl in enumerate(ndimage.find_objects(lab), 1):
    h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
    if h > 0.8 * a.shape[0] and w < 12:      # a column rule, not part of the sign
        continue
    if (lab[sl] == i).sum() < 30:            # specks
        continue
    keep |= lab == i
ys, xs = np.nonzero(keep)
y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
glyph = keep[y0:y1 + 1, x0:x1 + 1]
print("ink box px (w x h):", glyph.shape[1], "x", glyph.shape[0])
Image.fromarray(((~glyph) * 255).astype("uint8")).save(OUT.replace("fonts/NallinoSigns.otf", "zero_bitmap.png"))

# trace; units: ink height = 420 font units, bottom of the ring on the baseline
paths = potrace.Bitmap(~glyph).trace(turdsize=10, alphamax=1.0, opticurve=True, opttolerance=0.2)
s = 420.0 / glyph.shape[0]
lsb = 60
H = glyph.shape[0]


def P(pt):
    return (round(lsb + pt.x * s), round((H - pt.y) * s))


adv = round(2 * lsb + glyph.shape[1] * s)
pen = T2CharStringPen(width=adv, glyphSet=None)
for curve in paths:
    pen.moveTo(P(curve.start_point))
    for seg in curve.segments:
        if seg.is_corner:
            pen.lineTo(P(seg.c)); pen.lineTo(P(seg.end_point))
        else:
            pen.curveTo(P(seg.c1), P(seg.c2), P(seg.end_point))
    pen.closePath()
cs = pen.getCharString()

fb = FontBuilder(1000, isTTF=False)
ZW = [0x200B, 0x200C, 0x200D, 0x200E, 0x200F, 0x2060, 0xFEFF]
fb.setupGlyphOrder([".notdef", "space", "zw", "abjadzero"])
fb.setupCharacterMap({0xE000: "abjadzero", 0x20: "space", **{c: "zw" for c in ZW}})
empty = T2CharStringPen(width=500, glyphSet=None); empty.moveTo((0, 0)); empty.lineTo((0, 1)); empty.closePath()
fb.setupCFF("NallinoSigns", {"FullName": "Nallino Signs"}, {".notdef": empty.getCharString(), "space": T2CharStringPen(250, None).getCharString(), "zw": T2CharStringPen(0, None).getCharString(), "abjadzero": cs}, {})
fb.setupHorizontalMetrics({".notdef": (500, 0), "space": (250, 0), "zw": (0, 0), "abjadzero": (adv, lsb)})
fb.setupHorizontalHeader(ascent=900, descent=-300)
fb.setupNameTable({"familyName": "Nallino Signs", "styleName": "Regular"})
fb.setupOS2(sTypoAscender=900, sTypoDescender=-300, usWinAscent=900, usWinDescent=300)
fb.setupPost()
fb.save(OUT)
print("wrote", OUT, "curves:", len(paths), "advance:", adv)

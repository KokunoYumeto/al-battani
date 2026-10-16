"""S16 - the scan evidence for the readings corrected on Part II p. 299 (master PDF 748), the astrological figure
(repairs.tsv R01-R03). The page is a 600 dpi bilevel image (4972 x 7396 pixels). The labels of the terms are written
along the radius from the outer end; each is cut out of the page image, turned so that it reads from left to right
(the centre of the figure at 266.5, 457.15 pt; angles counterclockwise from the right-hand horizontal) and enlarged
with whole pixels, so no new grey is made. Writes, beside this script:
  p299_term_labels.png    the three corrected labels and reference labels of the same ring, whole
  p299_second_letters.png the first two letters of the Gemini and Cancer labels beside three Iupiter labels
  p299_word_endings.png   the last three letters of the twelve Jupiter labels of the terms
Needs the master scan (not in the repository). python make_p299_evidence.py"""
import math
from pathlib import Path

import fitz
from PIL import Image, ImageDraw

MASTER = Path(r"F:\user\Documents\CLAUDE PLEASE DONT DELETE WINDOWS 32\grind\nallino_pars123.pdf")
HERE = Path(__file__).resolve().parent
K = 600 / 72
CX, CY = 266.5, 457.15
JUPITER = [("Aries 1", 94.5), ("Taurus 3", 134.2), ("Gemini 2", 160.0), ("Cancer 2", 189.3), ("Leo 3", 224.8),
           ("Virgo 3", 254.8), ("Libra 3", 284.9), ("Scorpio 2", 309.0), ("Sagittarius 1", 333.7),
           ("Capricorn 3", 14.5), ("Aquarius 4", 49.5), ("Pisces 2", 69.4)]


def page_image():
    doc = fitz.open(MASTER)
    page = doc[747]
    (info,) = page.get_image_info(xrefs=True)
    pix = fitz.Pixmap(doc, info["xref"])
    return Image.frombytes("L", (pix.width, pix.height), pix.samples)


def strip(im, a, r0, r1, half_width, zoom, label):
    """the band of the page from radius r1 (left) to r0 (right) at angle a, half_width pt across, enlarged"""
    rm = (r0 + r1) / 2
    x, y = CX + rm * math.cos(math.radians(a)), CY - rm * math.sin(math.radians(a))
    half = (r1 - r0) / 2 + 4
    sq = im.crop((round((x - half) * K), round((y - half) * K), round((x + half) * K), round((y + half) * K)))
    sq = sq.rotate(-(a + 180), resample=Image.NEAREST, expand=False, fillcolor=255)
    w, h = sq.size
    band = sq.crop((int(w / 2 - (r1 - r0) / 2 * K), int(h / 2 - half_width * K), int(w / 2 + (r1 - r0) / 2 * K),
                    int(h / 2 + half_width * K)))
    band = band.resize((band.width * zoom, band.height * zoom), Image.NEAREST)
    head = Image.new("L", (band.width, 22), 255)
    ImageDraw.Draw(head).text((4, 5), label, fill=0)
    out = Image.new("L", (band.width, band.height + 22), 255)
    out.paste(head, (0, 0))
    out.paste(band, (0, 22))
    return out


def sheet(tiles, cols, name):
    tw = max(t.width for t in tiles)
    th = max(t.height for t in tiles)
    rows = (len(tiles) + cols - 1) // cols
    out = Image.new("L", (cols * (tw + 6) - 6, rows * (th + 6) - 6), 128)
    for i, t in enumerate(tiles):
        out.paste(t, ((i % cols) * (tw + 6), (i // cols) * (th + 6)))
    out.save(HERE / name, optimize=True)
    print("wrote", name, out.size)


def main():
    im = page_image()
    whole = [("Gemini, term 2: printed Inpiter", 160.0), ("Cancer, term 2: printed Iupitor", 189.3),
             ("Virgo, term 2: printed Verus", 249.7), ("Aries, term 1: Iupiter", 94.5),
             ("Gemini, term 3: Venus", 164.4), ("Pisces, term 1: printed Venns", 63.9)]
    sheet([strip(im, a, 150.0, 200.0, 6.0, 2, f"{lab} (angle {a:g})") for lab, a in whole], 2, "p299_term_labels.png")
    firsts = [("Gemini 2", 160.0), ("Cancer 2", 189.3), ("Aries 1", 94.5), ("Taurus 3", 134.2), ("Pisces 2", 69.4)]
    sheet([strip(im, a, 184.0, 194.0, 4.0, 6, lab) for lab, a in firsts], 5, "p299_second_letters.png")
    sheet([strip(im, a, 160.0, 179.0, 4.5, 3, lab) for lab, a in JUPITER], 4, "p299_word_endings.png")


if __name__ == "__main__":
    main()

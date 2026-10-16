"""S16 - render the seams of the assembled volumes for inspection: for every boundary between two bound sections,
the last page of the one and the first page of the next, side by side, with the volume's page numbers; plus the
cover, the contents and the last page. Writes inspection/seams_<volume>_<n>.png (contact sheets).
python inspect_seams.py"""
import csv
import sys
from pathlib import Path

import fitz
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
OUT = HERE / "inspection"
DPI = 40


def thumb(doc, pno):
    pix = doc[pno - 1].get_pixmap(dpi=DPI)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 64, 16], fill="white")
    d.text((3, 2), f"p. {pno}", fill="red")
    return im


def main():
    OUT.mkdir(exist_ok=True)
    rows = list(csv.DictReader(open(HERE / "assembly_receipt.tsv", encoding="utf-8"), delimiter="\t"))
    for vol in sorted({r["volume"] for r in rows}):
        doc = fitz.open(HERE / vol)
        secs = [r for r in rows if r["volume"] == vol]
        pairs = [(1, 2)]
        for a, b in zip(secs, secs[1:]):
            last = int(a["first_page"]) + int(a["pages"]) - 1
            pairs.append((last, int(b["first_page"])))
        pairs.append((len(doc) - 1, len(doc)))
        per_sheet = 9
        for k in range(0, len(pairs), per_sheet):
            group = pairs[k:k + per_sheet]
            ims = [(thumb(doc, a), thumb(doc, b)) for a, b in group]
            w = max(x.width + y.width for x, y in ims) + 12
            h = max(max(x.height, y.height) for x, y in ims) + 8
            cols = 3
            rows_n = (len(ims) + cols - 1) // cols
            sheet = Image.new("RGB", (cols * w, rows_n * h), "gray")
            for i, (x, y) in enumerate(ims):
                cx, cy = (i % cols) * w, (i // cols) * h
                sheet.paste(x, (cx + 2, cy + 2))
                sheet.paste(y, (cx + 4 + x.width, cy + 2))
            name = OUT / f"seams_{Path(vol).stem}_{k // per_sheet + 1}.png"
            sheet.save(name)
            print(name.name, sheet.size, [g for g in group])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()

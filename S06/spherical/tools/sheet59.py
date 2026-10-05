"""Contact sheets of every value cell of Part II p. 59 (half the increase of the longest day), with the computed
value and the two readings, for reading by eye: p3_kit/S59_{k}.png (one per section, 40 rows)."""
import json
import fitz
from PIL import Image, ImageDraw
import wide_kit as wk
from day_shadow_pages import half_increment

page = wk.doc[507]
for k in range(3):
    d = json.load(open(wk.OUT + f"MP508s{k}.json", encoding="utf-8"))
    R = d["rules"]
    tiles = []
    for i, r in enumerate(d["rows"]):
        phi = 20 * k + 0.5 * (i + 1)
        c = half_increment(phi) * 60
        im = wk.gray(page, 400, fitz.Rect(R[0] + 1, r["y"] - 6, R[2] - 1, r["y"] + 6))
        g = r["groups"][0]
        rd = "/".join(f"{x['read']}|{x['tl']}" if x else "-" for x in g)
        tiles.append((f"{phi:4.1f}  calc {int(c // 60)};{c % 60:04.1f}  read {rd}", im))
    cw = max(t[1].width for t in tiles); ch = max(t[1].height for t in tiles) + 4
    cols = 2; rows = (len(tiles) + cols - 1) // cols; LW = 260
    out = Image.new("L", (cols * (cw + LW), rows * ch), 255); dr = ImageDraw.Draw(out)
    for j, (lab, im) in enumerate(tiles):
        x = (j // rows) * (cw + LW); y = (j % rows) * ch
        dr.text((x + 4, y + ch // 2 - 6), lab, fill=0); out.paste(im, (x + LW, y + 2))
    out.save(wk.OUT + f"S59_{k}.png"); print(k, out.size)

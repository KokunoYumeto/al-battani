"""Page kit for wide Part III tables (e.g. the 1211 status tables): find the table frame and its vertical rules,
then cut the table into a right half and a left half at 500 dpi, in the same pt bands with a pt ruler, so rows
line up across the two halves. Also writes the area above and below the table and the rule geometry (JSON).
Usage: python wide_kit.py PDF [split_pt]
  split_pt: x (pt) where to split; default: the vertical rule nearest the table's middle.
Output (p3_kit/): W{PDF}_R_k.png, W{PDF}_L_k.png, W{PDF}_above.png, W{PDF}_below.png, W{PDF}.json"""
import io, json, os, sys
import fitz
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

MASTER = os.environ.get("P3_SRC", r"F:/user/Documents/CLAUDE PLEASE DONT DELETE WINDOWS 32/grind/nallino_pars123.pdf")
TAG = os.environ.get("P3_TAG", "")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "p3_kit") + os.sep
doc = fitz.open(MASTER)


def gray(page, dpi, clip=None):
    return Image.open(io.BytesIO(page.get_pixmap(dpi=dpi, clip=clip).tobytes("png"))).convert("L")


def geometry(page, clip=None):
    """Table frame and vertical rules; clip=(y0, y1) in pt restricts the search to a band of the page."""
    oy = 0.0
    if clip:
        oy = clip[0]
        a8 = np.array(gray(page, 200, fitz.Rect(0, clip[0], page.rect.width, clip[1])))
    else:
        a8 = np.array(gray(page, 200))
    hist = np.bincount(a8.ravel(), minlength=256).astype(float); p_ = hist / hist.sum()
    om = np.cumsum(p_); mu = np.cumsum(p_ * np.arange(256)); mt = mu[-1]
    sb = (mt * om - mu) ** 2 / np.maximum(om * (1 - om), 1e-9)
    g = a8 < min(175, int(np.argmax(sb)))
    h, w = g.shape
    lab, nl = ndimage.label(g)
    objs = ndimage.find_objects(lab)
    inside = [i for i in range(nl) if objs[i][0].start > 2 and objs[i][1].start > 2 and objs[i][0].stop < h - 2 and objs[i][1].stop < w - 2]
    longc = [i for i in inside if (objs[i][0].stop - objs[i][0].start) > 0.3 * h or (objs[i][1].stop - objs[i][1].start) > 0.3 * w]
    top = min(objs[i][0].start for i in longc); bot = max(objs[i][0].stop for i in longc) - 1
    left = min(objs[i][1].start for i in longc); right = max(objs[i][1].stop for i in longc) - 1
    box = g[top:bot + 1, left:right + 1]
    longv = np.zeros_like(box)
    for x in range(box.shape[1]):
        c = box[:, x]; y = 0
        while y < len(c):
            if c[y]:
                y1 = y
                while y1 < len(c) and c[y1]:
                    y1 += 1
                if y1 - y > 30:
                    longv[y:y1, x] = True
                y = y1
            else:
                y += 1
    spread = ndimage.binary_dilation(longv, structure=np.ones((1, 7), bool))
    idx = np.where(spread.sum(axis=0) > 0.25 * (bot - top))[0]
    vx = []
    for x in idx:
        if vx and x - vx[-1][-1] <= 2:
            vx[-1].append(x)
        else:
            vx.append([x])
    vx = sorted({int(np.mean(r)) + left for r in vx} | {left, right})
    k = 72 / 200
    return {"table_pt": [round(left * k, 1), round(top * k + oy, 1), round(right * k, 1), round(bot * k + oy, 1)],
            "vrules_pt": [round(x * k, 1) for x in vx]}


def ruled(page, x0, x1, y0, y1, dpi):
    im = gray(page, dpi, fitz.Rect(x0, y0, x1, y1))
    out = Image.new("L", (im.width + 70, im.height), 255); out.paste(im, (70, 0))
    d = ImageDraw.Draw(out); s = dpi / 72
    t = int(y0 // 10 + 1) * 10
    while t < y1:
        yy = int((t - y0) * s); d.line([(52, yy), (68, yy)], fill=0); d.text((2, yy - 6), str(t), fill=0); t += 10
    return out


if __name__ == "__main__":
    n = int(sys.argv[1]); page = doc[n - 1]
    yclip = next((tuple(float(v) for v in a[2:].split("-")) for a in sys.argv[2:] if a.startswith("y=")), None)
    args = [a for a in sys.argv[2:] if not a.startswith("y=")]
    info = geometry(page, yclip)
    x0, y0, x1, y1 = info["table_pt"]
    if args:
        split = float(args[0])
    else:
        mid = (x0 + x1) / 2
        split = min(info["vrules_pt"], key=lambda v: abs(v - mid))
    info["split_pt"] = split
    for f in os.listdir(OUT):
        if f.startswith(f"{TAG}W{n:04}_") and f.endswith(".png"):
            os.remove(OUT + f)
    band = 1850 / 500 * 72
    k = 0; y = y0
    while y < y1 + 2:
        a, b = max(y0 - 1, y - 6), min(y1 + 2, y + band)
        ruled(page, split - 2, x1 + 2, a, b, 500).save(OUT + f"{TAG}W{n:04}_R_{k}.png")
        ruled(page, x0 - 2, split + 2, a, b, 500).save(OUT + f"{TAG}W{n:04}_L_{k}.png")
        k += 1; y += band
    W, H = page.rect.width, page.rect.height
    gray(page, 200, fitz.Rect(30, 30, W - 30, y0 + 4)).save(OUT + f"{TAG}W{n:04}_above.png")
    gray(page, 300, fitz.Rect(30, y1 - 2, W - 30, H - 25)).save(OUT + f"{TAG}W{n:04}_below.png")
    json.dump(info, open(OUT + f"{TAG}W{n:04}.json", "w"), indent=1)
    print(n, "table", info["table_pt"], "split", split, "rules", info["vrules_pt"], "bands", k)

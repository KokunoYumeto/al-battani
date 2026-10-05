"""Zoom table cells by pt coordinates in both copies of Part III, side by side (master | IA copy).
Usage: python p3_cell.py PDF y_pt[,y_pt...] col [col ...]
  col: lond lonm latd latm dir mag num (whole numeric block) desc
  The IA copy is located by matching the table frame (IA page (1-based) = PDF - 865; its own page kit JSON is built on demand).
Output: p3_kit/PDF####_cells.png (each row: label | master crop | IA crop)"""
import io, json, os, subprocess, sys
import fitz
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
MASTER = r"F:/user/Documents/CLAUDE PLEASE DONT DELETE WINDOWS 32/grind/nallino_pars123.pdf"
IA = r"F:/user/Documents/Chat Interl Src/cleanup multilingual/albattani_work_CLAUDE/source_scan/nallino_1899_albattanisivealb00batt.pdf"
KIT = os.path.join(HERE, "p3_kit") + os.sep
n = int(sys.argv[1]); ys = [float(v) for v in sys.argv[2].split(",")]; cols = sys.argv[3:]


def kit(tag, src, num):
    path = KIT + f"{tag}PDF{num:04}.json"
    if not os.path.exists(path):
        env = dict(os.environ, P3_SRC=src, P3_TAG=tag, PYTHONIOENCODING="utf-8")
        subprocess.run([sys.executable, os.path.join(HERE, "p3_page_kit.py"), str(num)], env=env, check=True, capture_output=True)
        for f in os.listdir(KIT):                       # keep only the JSON of the helper copy
            if f.startswith(f"{tag}PDF{num:04}_"):
                os.remove(KIT + f)
    return json.load(open(path))


A = kit("", MASTER, n); B = kit("IA", IA, n - 865)
pa = fitz.open(MASTER)[n - 1]; pb = fitz.open(IA)[n - 866]


def colx(info, col):
    n0, n1 = info["num_rect"][0], info["num_rect"][2]
    if col == "num":
        return n0, n1
    if col == "desc":
        return info["desc_rect"][0], info["desc_rect"][2]
    v = []
    for x in sorted(info["vrules_pt"]):                 # merge double rules
        if v and x - v[-1] < 7:
            v[-1] = (v[-1] + x) / 2
        else:
            v.append(x)
    e = [x for x in v if n0 - 6 <= x <= n1 + 6]
    if len(e) == 5:                                     # left frame, mag|dir, dir|lat, lat|lon, lon|desc
        mag, dirc, lat, lon = (e[0], e[1]), (e[1], e[2]), (e[2], e[3]), (e[3], e[4])
    else:                                               # typical proportions of the numeric block
        w = n1 - n0
        mag, dirc, lat, lon = (n0, n0 + .26 * w), (n0 + .26 * w, n0 + .51 * w), (n0 + .51 * w, n0 + .755 * w), (n0 + .755 * w, n1)
    half = lambda a: ((a[0], (a[0] + a[1]) / 2), ((a[0] + a[1]) / 2, a[1]))
    cols = {"mag": mag, "dir": dirc, "latm": half(lat)[0], "latd": half(lat)[1], "lonm": half(lon)[0], "lond": half(lon)[1],
            "lat": lat, "lon": lon}
    a, b = cols[col]
    return a - 2, b + 2


def crop(page, rect, dpi):
    pix = page.get_pixmap(dpi=dpi, clip=rect)
    return Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")


# map master coordinates to the IA copy through the two table frames (the IA copy's thin rules are unreliable)
ta, tb = A["table_pt"], B["table_pt"]
sx = (tb[2] - tb[0]) / (ta[2] - ta[0]); sy = (tb[3] - tb[1]) / (ta[3] - ta[1])
rows = []
for y in ys:
    for col in cols:
        x0, x1 = colx(A, col)
        dpi = 900 if col not in ("num", "desc") else 600
        a = crop(pa, fitz.Rect(x0, y - 11, x1, y + 11), dpi)
        rb = fitz.Rect(tb[0] + (x0 - ta[0]) * sx, tb[1] + (y - 11 - ta[1]) * sy, tb[0] + (x1 - ta[0]) * sx, tb[1] + (y + 11 - ta[1]) * sy)
        b = crop(pb, rb, int(dpi / sx))
        rows.append((f"{y:.0f} {col}", a, b))
W = max(a.width for _, a, _ in rows) + max(b.width for _, _, b in rows) + 120
H = sum(max(a.height, b.height) + 8 for _, a, b in rows)
s = Image.new("L", (W, H), 255); d = ImageDraw.Draw(s); y0 = 0
wa = max(a.width for _, a, _ in rows)
for lab, a, b in rows:
    d.text((2, y0 + 6), lab, fill=0); s.paste(a, (80, y0)); s.paste(b, (80 + wa + 30, y0))
    y0 += max(a.height, b.height) + 8
if W > 1990:
    s = s.resize((1990, int(H * 1990 / W)), Image.LANCZOS)
s.save(KIT + f"PDF{n:04}_cells.png"); print(s.size)

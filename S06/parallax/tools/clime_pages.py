"""Read Part II pp. 95-101: the parallaxes of the Moon in longitude and latitude in the seven climes (one page each;
the upper half: Cancer ... Sagittarius, the lower half: Capricorn ... Gemini). Each sign has a column of hours from
culmination and a column of parallaxes in longitude and latitude (minutes); northern latitudes are printed with «+»
(and «bor.» / «austr.» over the first value of a run).
read_half(pdf, half) -> list of signs: {"sign", "rules", "rows": [{"y", "hour_glyph", "long": cell, "lat": cell,
"plus_tl", "plus_img"}]}; cells as p2motion (text, tl, conf, x0, x1). The glyph reader takes «+» for «1»: the digits of
a latitude are its glyph text without the first character when a «+» is found by the text layer or by the image test
(a component whose middle row is inked across its width)."""
import json, os
import numpy as np
import fitz
from scipy import ndimage
import p2motion, p2cols, wide_kit as wk

SIGNS = {"top": ["Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius"],
         "bot": ["Capricorn", "Aquarius", "Pisces", "Aries", "Taurus", "Gemini"]}
CLIME = {544: 1, 545: 2, 546: 3, 547: 4, 548: 5, 549: 6, 550: 7}
W_HOURS, W_PAR = 29.1, 40.9


def complete_rules(det):
    """the 13 rules of a half: from the left frame, alternately an hours column and a parallax column, each rule
    snapped to a detected one within 3.5 pt"""
    det = sorted(det)
    out = [det[0]]
    for k in range(12):
        target = out[-1] + (W_HOURS if k % 2 == 0 else W_PAR)
        near = [d for d in det if abs(d - target) < 3.5]
        out.append(min(near, key=lambda d: abs(d - target)) if near else round(target, 1))
    return out


def geometry(pdf):
    page = wk.doc[pdf - 1]
    ws = page.get_text("words")
    culm = sorted({round(w[1]) for w in ws if w[4].startswith("culm")})
    longs = sorted({round(w[1]) for w in ws if w[4].startswith("Long")})
    out = {}
    for half, c, lg in (("top", culm[0], longs[0]), ("bot", culm[-1], longs[-1])):
        y0 = lg + 18                                         # below the heads «Long. Lat.»
        y1 = c + (c - y0) + 16
        det = p2cols.rules_banded(pdf, c - 70, c + 70)
        out[half] = {"y0": y0, "y1": y1, "culm": c, "rules": complete_rules(det)}
    return out


def tl_words(page):
    return [(w[0], w[1], w[2], w[3], w[4]) for w in page.get_text("words")]


def plus_tl(words, cell):
    """«+» in the text-layer word under the cell"""
    if cell is None:
        return False
    xc = (cell["x0"] + cell["x1"]) / 2
    for (a0, b0, a1, b1, t) in words:
        if a0 - 2 <= xc <= a1 + 2 and b0 - 3 <= cell["y"] <= b1 + 3 and any(ch.isdigit() for ch in t):
            return "+" in t
    return False


def plus_img(page, cell, dpi=600):
    """the leftmost component of the cell is a «+»: its middle row is inked across most of its width"""
    if cell is None:
        return False
    rect = fitz.Rect(cell["x0"] - 1.5, cell["y"] - 6, cell["x1"] + 0.5, cell["y"] + 6)
    a = np.array(wk.gray(page, dpi, rect)) < 150
    lab, n = ndimage.label(a)
    if n == 0:
        return False
    objs = ndimage.find_objects(lab)
    comps = [(sl[1].start, k + 1, sl) for k, sl in enumerate(objs) if (sl[0].stop - sl[0].start) > 0.25 * a.shape[0]]
    if len(comps) < 2:                                       # a «+» is followed by the digits of the latitude
        return False
    _, k, sl = min(comps)
    m = lab[sl] == k
    h, w = m.shape
    mid = m[max(0, h // 2 - max(1, h // 10)): h // 2 + max(1, h // 10) + 1]
    row_cover = mid.any(axis=0).mean()
    colmid = m[:, max(0, w // 2 - max(1, w // 10)): w // 2 + max(1, w // 10) + 1]
    col_cover = colmid.any(axis=1).mean()
    return bool(row_cover > 0.8 and col_cover > 0.8 and 0.6 < w / max(h, 1) < 1.6)


def read_half(pdf, half):
    g = geometry(pdf)[half]
    R = g["rules"]
    page = wk.doc[pdf - 1]
    words = tl_words(page)
    out = []
    for s, sign in enumerate(SIGNS[half]):
        rules = [R[2 * s], R[2 * s + 1], R[2 * s + 2]]
        rows = p2motion.read(pdf, g["y0"], g["y1"], rules, nsub=2)
        rows = [r for r in rows if None not in r["groups"][0]]              # label rows («bor.», «austr.») and head debris
        recs = []
        for r in rows:
            lo, la = r["groups"][0]
            recs.append({"y": r["y"], "hour_glyph": r["arg"]["text"] if r["arg"] else "",
                         "hour_tl": r["arg"].get("tl", "") if r["arg"] else "",
                         "long": lo, "lat": la, "plus_tl": plus_tl(words, la), "plus_img": plus_img(page, la)})
        out.append({"sign": sign, "rules": rules, "rows": recs})
    return {"pdf": pdf, "half": half, "geometry": g, "signs": out}


def save(pdf, half):
    d = read_half(pdf, half)
    json.dump(d, open(wk.OUT + f"CL{pdf}{half}.json", "w", encoding="utf-8"), ensure_ascii=False, default=str)
    return d


if __name__ == "__main__":
    import sys
    pdf, half = int(sys.argv[1]), sys.argv[2]
    d = save(pdf, half)
    print(pdf, half, d["geometry"])
    for s in d["signs"]:
        print(s["sign"], len(s["rows"]))
        for r in s["rows"]:
            lo, la = r["long"], r["lat"]
            print("   ", round(r["y"], 1), r["hour_glyph"], "|", lo["text"], lo.get("tl"), round(lo["conf"], 2), "|",
                  la["text"] if la else None, la.get("tl") if la else None, round(la["conf"], 2) if la else None,
                  "+tl" if r["plus_tl"] else "", "+img" if r["plus_img"] else "")

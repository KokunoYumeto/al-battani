"""Read Part II pp. 187-188. p. 187 (PDF 636): the increments of the mean motions for the revolutions of the years,
1-12 tropical years, eight columns (degrees, minutes): the Moon's mean longitude, the Moon's anomaly, the northern node,
Saturn, Jupiter, Mars (increment of the mean longitude and diminution of the anomaly), the anomalies of Venus and
Mercury. p. 188 (PDF 637): the table of the revolutions of the years (collected 20-200, single 1-20, «tempora
ascensionum»), the altitudes of the Sun at the twelve temporal hours of the solstices, and the directions of the hours
(to the seconds, with Nallino's bracketed quarters).
The eye reading (EYE) gives the expected values. p. 187 is read with the glyph reader and the OCR text layer
(motion_page.run, classes A, B, C); p. 188 is compared with the numbers of the OCR text layer, row by row."""
import re
import numpy as np
import motion_page as mp
import p2cols, wide_kit as wk

P187 = ["moon", "moon_anom", "node", "sat", "jup", "mars", "ven_anom", "mer_anom"]
EYE187 = {
    "moon": "132 33,265 7,37 40,170 13,302 47,75 20,207 53,340 27,113 1,245 34,18 7,150 40",
    "moon_anom": "91 52,183 43,275 35,7 27,99 19,191 10,283 2,14 54,106 45,198 37,290 29,22 20",
    "node": "19 20,38 41,58 1,77 22,96 42,116 3,135 23,154 44,174 4,193 25,212 45,232 6",
    "sat": "12 14,24 28,36 42,48 57,61 11,73 25,85 39,97 53,110 7,122 21,134 35,146 50",
    "jup": "30 22,60 44,91 6,121 27,151 49,182 11,212 33,242 55,273 17,303 38,334 0,4 22",
    "mars": "191 25,22 50,214 15,45 40,237 5,68 30,259 55,91 20,282 45,114 9,305 33,136 57",
    "ven_anom": "225 11,90 22,315 33,180 43,45 54,271 5,136 16,1 27,226 38,91 48,316 59,182 10",
    "mer_anom": "54 42,109 23,164 4,218 45,273 27,327 8,22 50,77 32,132 13,186 54,241 35,296 16"}
EYE187 = {k: [int(a) * 60 + int(b) for a, b in (x.split() for x in v.split(","))] for k, v in EYE187.items()}
# p. 188
COLLECTED = {20: (292, 0), 40: (224, 0), 60: (156, 0), 80: (88, 0), 100: (20, 0), 120: (312, 0), 140: (244, 0),
             160: (176, 0), 180: (108, 0), 200: (40, 0)}
SINGLE = {1: (86, 36), 2: (173, 12), 3: (259, 48), 4: (346, 24), 5: (73, 0), 6: (159, 36), 7: (246, 12), 8: (332, 48),
          9: (59, 24), 10: (146, 0), 11: (232, 36), 12: (319, 12), 13: (45, 48), 14: (132, 24), 15: (219, 0),
          16: (305, 36), 17: (32, 12), 18: (118, 48), 19: (205, 24), 20: (292, 0)}
ALTITUDE = {"cap": [(8, 3), (15, 18), (21, 28), (26, 18), (29, 23), (30, 25), (29, 23), (26, 18), (21, 28), (15, 18),
                    (8, 3), (0, 0)],
            "can": [(13, 17), (27, 1), (41, 56), (56, 29), (70, 3), (77, 35), (70, 3), (56, 29), (41, 56), (27, 1),
                    (13, 17), (0, 0)]}
DIRECTION = {"can": [((19, 40, 0), "ad bor."), ((10, 23, 40), "id."), ((0, 41, 13), "id."), ((11, 40, 44), "ad austr."),
                     ((33, 29, 30), "id."), ((90, 0, 0), "id.")],
             "cap": [((37, 2, 30), "ad austr."), ((45, 22, 20), "id."), ((54, 56, 30), "id."), ((65, 37, 30), "id."),
                     ((77, 27, 30), "id."), ((90, 0, 0), "id.")]}


def geometry187():
    page = wk.doc[636 - 1]
    ys = {w[4].strip(): w[1] for w in page.get_text("words") if w[0] < 80 and 300 < w[1] < 800}
    y0, y1 = ys["1"] - 10, ys["12"] + 16
    rules = [x for x in p2cols.rules_banded(636, y0, y1) if 40 < x < 560]
    return y0, y1, rules


def run187(tag="e"):
    y0, y1, rules = geometry187()
    tv = [EYE187[c] for c in P187]
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 8
    return mp.run(636, y0, y1, rules, tv, args=list(range(1, 13)), nsub=[2] * 8, mods=[360] * 8,
                  fixed=[(0, 1)] * 8, keep=keep, tag=tag)


def tl_numbers(pdf, x0, x1, y0, y1):
    """the numbers of the text layer in a box, grouped in rows by their y (within 4 pt), read left to right"""
    ws = [w for w in wk.doc[pdf - 1].get_text("words") if x0 < (w[0] + w[2]) / 2 < x1 and y0 < w[1] < y1
          and re.search(r"\d", w[4])]
    ws.sort(key=lambda w: w[1])
    rows = []
    for w in ws:
        if rows and abs(w[1] - rows[-1][0][1]) < 4:
            rows[-1].append(w)
        else:
            rows.append([w])
    return [(round(r[0][1], 1), [d for w in sorted(r, key=lambda w: w[0]) for d in re.findall(r"\d+", w[4])]) for r in rows]


if __name__ == "__main__":
    import sys
    from collections import Counter
    if "188" in sys.argv:
        for name, box in (("collected+single", (215, 515, 520, 1340)),):
            pass
        page = wk.doc[637 - 1]
        for w in page.get_text("words"):
            pass
        for y, nums in tl_numbers(637, 0, 600, 300, 800):
            print(y, nums)
    else:
        y0, y1, rules = geometry187()
        print("band", round(y0, 1), round(y1, 1), "rules", rules)
        out = run187()
        bad = [(i + 1, r["arg"]) for i, r in enumerate(out["rows"]) if r.get("arg_ok") is False]
        print(len(out["rows"]), out["classes"], "flags", len(out["flags"]),
              Counter(int(f[1]) for f in out["flags"] if f[0] != "fit"), "args off", bad)

"""Read Part II pp. 142-143: the elongations of the planets from the true Sun for their apparitions and occultations at
latitude 36° 0′. p. 142 (PDF 591): Saturn, Jupiter, Mars, each with Apparitio (ortus matutinus) and Occultatio (occasus
vespertinus); p. 143 (PDF 592): Venus and Mercury, each with Apparitio (ortus vespertinus, occasus matutinus) and
Occultatio (ortus matutinus, occasus vespertinus). 12 rows, the beginnings of the signs; every value in degrees and
minutes. The eye reading (EYE, from 200 dpi renders) gives the expected values; the glyph reader and the OCR text layer
classify each cell: A both give the eye value, B one, C none (read again by eye at higher resolution).
Output: MP{pdf}e.json via motion_page.run."""
import numpy as np
import motion_page as mp
import p2cols, wide_kit as wk

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpius", "Sagittarius", "Capricornus",
         "Aquarius", "Pisces"]
COLUMNS = {591: ["sat_app", "sat_occ", "jup_app", "jup_occ", "mars_app", "mars_occ"],
           592: ["ven_ov", "ven_om", "ven_orm", "ven_ocv", "mer_ov", "mer_om", "mer_orm", "mer_ocv"]}
EYE = {
    "sat_app": "29 28,27 26,22 10,17 18,14 8,13 8,12 55,13 1,13 47,16 36,21 16,26 46",
    "sat_occ": "13 46,14 3,15 5,17 9,19 48,22 0,22 32,21 20,18 35,16 6,14 40,14 0",
    "jup_app": "19 13,18 21,14 55,11 41,9 44,9 7,9 0,9 7,9 44,11 44,14 54,18 11",
    "jup_occ": "9 28,9 38,10 16,11 44,13 32,15 23,16 7,15 23,13 32,11 44,10 16,9 38",
    "mars_app": "29 0,27 51,22 54,18 55,16 7,15 8,14 52,15 8,16 4,18 35,22 34,27 10",
    "mars_occ": "14 37,15 8,16 7,18 15,22 54,27 51,29 0,27 51,22 54,18 15,16 7,15 8",
    "ven_ov": "15 0,13 48,10 59,8 28,7 5,6 13,6 7,6 31,7 26,9 38,12 47,14 28",
    "ven_om": "7 25,7 25,7 38,8 38,9 39,10 46,11 19,11 26,10 47,9 38,8 29,7 43",
    "ven_orm": "3 36,4 9,5 34,10 42,17 25,23 17,22 27,15 14,8 1,5 18,3 59,3 43",
    "ven_ocv": "7 27,8 3,8 47,10 44,9 30,7 43,6 40,6 17,6 12,6 18,6 25,6 51",
    "mer_ov": "24 10,21 15,17 10,14 9,12 33,12 8,12 10,12 41,14 3,16 59,21 35,24 38",
    "mer_om": "12 20,12 8,12 36,14 9,16 39,20 23,23 7,23 49,20 44,16 59,14 7,12 54",
    "mer_orm": "22 43,25 23,22 28,18 48,15 8,13 15,12 0,11 35,11 56,12 36,14 25,18 22",
    "mer_ocv": "11 19,12 12,14 44,19 48,23 29,26 36,25 38,20 35,16 41,12 30,11 32,11 7"}
EYE = {k: [int(a) * 60 + int(b) for a, b in (x.split() for x in v.split(","))] for k, v in EYE.items()}


def geometry(pdf):
    """the band from the sign names of the first column (text layer), and the vertical rules of the table"""
    page = wk.doc[pdf - 1]
    ys = {w[4].strip("."): w for w in page.get_text("words") if w[4].strip(".") in SIGNS and w[0] < 200}
    y0, y1 = ys["Aries"][1] - 10, ys["Pisces"][3] + 10
    rules = [x for x in p2cols.rules_banded(pdf, y0, y1) if 40 < x < 560]
    return y0, y1, rules


def run_eye(pdf, tag="e"):
    y0, y1, rules = geometry(pdf)
    cols = COLUMNS[pdf]
    tv = [EYE[c] for c in cols]
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 6
    return mp.run(pdf, y0, y1, rules, tv, nsub=[2] * len(cols), mods=[360] * len(cols), fixed=[(0, 1)] * len(cols),
                  keep=keep, tag=tag)


if __name__ == "__main__":
    import sys
    from collections import Counter
    args = sys.argv[1:]
    for pdf in [int(a) for a in args if a.isdigit()] or [591, 592]:
        y0, y1, rules = geometry(pdf)
        print(pdf, "band", round(y0, 1), round(y1, 1), "rules", rules)
        if "--rules" in args:
            continue
        out = run_eye(pdf)
        print(pdf, len(out["rows"]), out["classes"], "flags", len(out["flags"]),
              Counter(int(f[1]) for f in out["flags"] if f[0] != "fit"))

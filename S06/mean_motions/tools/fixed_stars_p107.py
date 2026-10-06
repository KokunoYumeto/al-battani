"""Part II p. 107: the motion of the fixed stars (precession) in Roman years, months and days. Transcribed by eye from
200-400 dpi renders (EYE below) and compared, sub-table by sub-table, with the numbers of the OCR text layer (the second
reader): every printed number of a sub-table must appear, in order, among the text-layer tokens of its band."""
import re
import wide_kit as wk

COLLECTED = {20: (0, 18, 11), 40: (0, 36, 22), 60: (0, 54, 33), 80: (1, 12, 44), 100: (1, 30, 55), 120: (1, 49, 5),
             140: (2, 7, 16), 160: (2, 25, 27), 180: (2, 43, 38), 200: (3, 1, 49), 220: (3, 20, 0), 240: (3, 38, 11),
             260: (3, 56, 22), 280: (4, 14, 33), 300: (4, 32, 44), 320: (4, 50, 55), 340: (5, 9, 6), 360: (5, 27, 16),
             380: (5, 45, 27), 400: (6, 3, 38), 420: (6, 21, 49), 440: (6, 40, 0)}
SINGLE = {1: (0, 54, 33), 2: (1, 49), 3: (2, 44), 4: (3, 38), 5: (4, 33), 6: (5, 27), 7: (6, 22), 8: (7, 16), 9: (8, 11),
          10: (9, 5), 11: (10, 0), 12: (10, 55), 13: (11, 49), 14: (12, 44), 15: (13, 38), 16: (14, 33), 17: (15, 27),
          18: (16, 22), 19: (17, 16), 20: (18, 11, 24)}
MONTHS = [("ādhār [Martius]", 31, (0, 5)), ("nīsān [Aprilis]", 61, (0, 9)), ("ayyār [Maius]", 92, (0, 14)),
          ("ḥazīrān [Iunius]", 122, (0, 18)), ("tammūz [Iulius]", 153, (0, 23)), ("āb [Augustus]", 184, (0, 28)),
          ("aylūl [September]", 214, (0, 32)), ("tishrīn I [October]", 245, (0, 37)),
          ("tishrīn II [November]", 275, (0, 41)), ("kānūn I [December]", 306, (0, 46)),
          ("kānūn II [Ianuarius]", 337, (0, 50)), ("subāṭ [Februarius]", 365, (0, 54))]
DAYS = {d: (0, s) for d, s in zip(range(1, 31), [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4,
                                                  4, 4, 4, 4])}
DAYS[30] = (0, 4, 30)
BANDS = {"collected": (102.4, 170.1), "single": (206.3, 274.2), "months": (348.0, 400.3), "days": (434.8, 488.4)}


def tokens(x0, x1, y0=290, y1=745):
    out = []
    for w in sorted(wk.doc[556 - 1].get_text("words"), key=lambda w: (round(w[1] / 3), w[0])):
        if x0 < (w[0] + w[2]) / 2 < x1 and y0 < w[1] < y1:
            out += re.findall(r"\d+", w[4])
    return out


def tl_rows(x0, x1, y0=290, y1=745):
    """the text-layer numbers of a band, grouped in rows by their y (within 4 pt), each row read left to right"""
    ws = [w for w in wk.doc[556 - 1].get_text("words") if x0 < (w[0] + w[2]) / 2 < x1 and y0 < w[1] < y1
          and re.search(r"\d", w[4])]
    ws.sort(key=lambda w: w[1])
    rows = []
    for w in ws:
        if rows and abs(w[1] - rows[-1][0][1]) < 4:
            rows[-1].append(w)
        else:
            rows.append([w])
    return [[d for w in sorted(r, key=lambda w: w[0]) for d in re.findall(r"\d+", w[4])] for r in rows]


def compare():
    seqs = {"collected": [COLLECTED[k] for k in sorted(COLLECTED)], "single": [SINGLE[k] for k in sorted(SINGLE)],
            "months": [val for _, _, val in MONTHS], "days": [DAYS[k] for k in sorted(DAYS)]}
    report = {}
    for name, (x0, x1) in BANDS.items():
        rows = tl_rows(x0, x1)
        mine = [[str(v) for v in val] for val in seqs[name]]
        agree, differ = 0, []
        for k, val in enumerate(mine):
            tl = rows[k] if k < len(rows) else []
            if tl == val:
                agree += 1
            else:
                differ.append((k + 1, " ".join(val), " ".join(tl)))
        report[name] = (len(mine), len(rows), agree, differ)
    return report


def write(path):
    """S06/mean_motions/fs_p2.tsv: one row per printed row; the places as printed (d m s for the collected years, m s for
    the rest, with thirds where printed); check A where a text-layer row of the band gives the same numbers, else E"""
    import csv
    rows = []
    blocks = [("collected", [(str(k), "", COLLECTED[k]) for k in sorted(COLLECTED)]),
              ("single", [(str(k), "", SINGLE[k]) for k in sorted(SINGLE)]),
              ("months", [(name, str(days), val) for name, days, val in MONTHS]),
              ("days", [(str(k), "", DAYS[k]) for k in sorted(DAYS)])]
    for table, items in blocks:
        tl = [" ".join(r) for r in tl_rows(*BANDS[table])]
        for i, (arg, days, val) in enumerate(items, 1):
            if table == "collected":
                d, m, s, t = val[0], val[1], val[2], ""
            else:
                d, m, s, t = "", val[0], val[1], (val[2] if len(val) > 2 else "")
            mine = " ".join(str(v) for v in val)
            rows.append({"pdf": 556, "ppage": "107", "table": table, "row": i, "arg": arg, "days": days, "d": d, "m": m,
                         "s": s, "t": t, "check": "A" if mine in tl else "E"})
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(rows)
    from collections import Counter
    return len(rows), Counter(r["check"] for r in rows)


if __name__ == "__main__":
    import sys
    for name, (n, ntl, agree, differ) in compare().items():
        print(name, "rows", n, "text-layer rows", ntl, "agree", agree)
        for d in differ:
            print("    row", d[0], "eye", d[1], "| text layer", d[2])
    if "--write" in sys.argv:
        print(write(r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani/S06/mean_motions/fs_p2.tsv"))

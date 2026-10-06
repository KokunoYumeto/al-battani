"""Read Part II pp. 140-141: the latitudes of the planets. p. 140 (PDF 589): Saturn, Jupiter and Mars, the latitude at
the northern and at the southern limit (Septentrio, Auster); p. 141 (PDF 590): Venus and Mercury, Inclinatio and
Obliquitas, and the column of the portions common to all planets. 30 rows a page, n = 6, 12 ... 180 and 360 - n;
every value in degrees and minutes.
The eye reading (EYE, from 200 dpi renders) gives the expected values; the glyph reader and the OCR text layer classify
each cell: A both give the eye value, B one, C none (to be read again by eye at higher resolution).
Output: MP{pdf}e.json via motion_page.run."""
import motion_page as mp
import station_pages as sp

NS = list(range(6, 181, 6))
COLUMNS = {589: ["sat_n", "sat_s", "jup_n", "jup_s", "mars_n", "mars_s"],
           590: ["ven_inc", "ven_obl", "mer_inc", "mer_obl", "portio"]}
EYE = {
    "sat_n": "2 4,2 5,2 6,2 7,2 8,2 10,2 11,2 12,2 14,2 16,2 18,2 21,2 24,2 27,2 30,2 33,2 36,2 39,2 42,2 45,2 47,2 50,"
             "2 53,2 55,2 57,2 59,3 0,3 1,3 2,3 2",
    "sat_s": "2 2,2 3,2 3,2 4,2 5,2 7,2 8,2 10,2 12,2 15,2 18,2 21,2 24,2 27,2 30,2 33,2 36,2 39,2 42,2 45,2 48,2 51,"
             "2 54,2 56,2 58,3 0,3 2,3 3,3 4,3 5",
    "jup_n": "1 7,1 8,1 8,1 9,1 10,1 11,1 12,1 13,1 14,1 16,1 18,1 21,1 24,1 27,1 30,1 33,1 36,1 39,1 42,1 45,1 47,1 50,"
             "1 52,1 55,1 58,2 0,2 2,2 3,2 4,2 4",
    "jup_s": "1 5,1 6,1 6,1 7,1 8,1 9,1 10,1 11,1 13,1 16,1 18,1 21,1 24,1 27,1 30,1 33,1 36,1 39,1 42,1 45,1 48,1 51,"
             "1 54,1 57,2 0,2 3,2 5,2 6,2 7,2 8",
    "mars_n": "0 8,0 9,0 11,0 13,0 14,0 15,0 18,0 21,0 24,0 28,0 32,0 36,0 41,0 46,0 52,0 59,1 6,1 14,1 23,1 34,1 48,"
              "2 1,2 16,2 34,2 55,3 16,3 38,4 0,4 14,4 21",
    "mars_s": "0 4,0 4,0 5,0 6,0 7,0 9,0 12,0 15,0 18,0 22,0 26,0 30,0 36,0 42,0 49,0 56,1 4,1 13,1 24,1 37,1 51,"
              "2 10,2 32,2 56,3 29,4 9,4 55,5 52,6 36,7 7",
    "ven_inc": "1 2,1 1,1 0,0 59,0 57,0 55,0 51,0 46,0 41,0 35,0 29,0 23,0 16,0 8,0 0,0 10,0 20,0 32,0 44,0 59,1 18,"
               "1 38,1 59,2 23,3 3,3 44,4 26,5 13,5 52,6 22",
    "ven_obl": "0 8,0 16,0 25,0 33,0 41,0 49,0 57,1 5,1 13,1 20,1 28,1 35,1 42,1 50,1 57,2 3,2 9,2 15,2 20,2 24,2 27,"
               "2 30,2 30,2 28,2 22,2 12,1 55,1 27,0 48,0 0",
    "mer_inc": "1 45,1 44,1 43,1 40,1 36,1 30,1 23,1 16,1 8,0 59,0 49,0 38,0 26,0 16,0 0,0 15,0 31,0 48,1 6,1 25,1 45,"
               "2 6,2 27,2 47,3 7,3 26,3 42,3 54,4 2,4 5",
    "mer_obl": "0 11,0 22,0 33,0 44,0 55,1 6,1 16,1 26,1 35,1 44,1 52,2 0,2 7,2 14,2 20,2 25,2 28,2 29,2 30,2 29,2 26,"
               "2 20,2 11,2 0,1 46,1 29,1 10,0 48,0 24,0 0",
    "portio": "59 36,58 36,57 0,54 36,52 0,48 24,44 24,40 0,35 12,30 0,24 24,18 24,12 24,6 24,0 0,6 24,12 24,18 24,"
              "24 24,30 0,35 12,40 0,44 24,48 24,52 0,54 36,57 0,58 36,59 36,60 0"}
EYE = {k: [int(a) * 60 + int(b) for a, b in (x.split() for x in v.split(","))] for k, v in EYE.items()}


def run_eye(pdf, tag="e"):
    y0, y1, rules = sp.geometry(pdf)
    rules = [x for x in rules if x < 545]            # p. 140: the dark edge of the scan beyond the right frame
    tv = [[360 - n for n in NS]] + [EYE[c] for c in COLUMNS[pdf]]
    ng = len(tv)
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 5
    return mp.run(pdf, y0, y1, rules, tv, args=NS, nsub=[1] + [2] * (ng - 1), mods=[1000] + [360] * (ng - 1),
                  fixed=[(0, 1)] * ng, keep=keep, tag=tag)


if __name__ == "__main__":
    import sys
    from collections import Counter
    args = sys.argv[1:]
    for pdf in [int(a) for a in args if a.isdigit()] or [589, 590]:
        y0, y1, det = sp.geometry(pdf)
        print(pdf, "band", round(y0, 1), round(y1, 1), "rules", det)
        if "--rules" in args:
            continue
        out = run_eye(pdf)
        bad = [(i + 1, r["arg"], r.get("arg_exp")) for i, r in enumerate(out["rows"]) if r.get("arg_ok") is False]
        print(pdf, len(out["rows"]), out["classes"], "flags", len(out["flags"]),
              Counter(int(f[1]) for f in out["flags"] if f[0] != "fit"), "args off", bad[:4])

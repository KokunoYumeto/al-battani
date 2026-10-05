"""Read Part II pp. 57-58: the declination of the Sun for every degree of longitude (obliquity 23 35'), with the
four arcs of equal declination, and the right ascensions of every tenth degree with their sines (p. 58).
Each half table is read with a dummy first column (no argument column): groups = declination (d m s) and the four
arcs (one number each); every cell is matched against its computed value (the reader's candidate within 2 units).
Output: p3_kit/MP{pdf}{tag}.json and contact sheets."""
import math
import motion_page as mp

EPS = 23 + 35 / 60


def decl(lam):
    return round(math.degrees(math.asin(math.sin(math.radians(lam)) * math.sin(math.radians(EPS)))) * 3600)


def ra(lam):
    """right ascension from the beginning of Aries, degrees"""
    if lam == 90:
        return 90.0
    return math.degrees(math.atan(math.cos(math.radians(EPS)) * math.tan(math.radians(lam))))


HALVES = [(506, "L", [68.0, 72.0, 137.6, 171.8, 206.3, 240.4, 274.8], range(1, 31)),
          (506, "R", [273.3, 277.3, 348.0, 382.1, 416.4, 450.6, 485.8], range(31, 61)),
          (507, "L", [112.5, 116.5, 188.2, 222.5, 257.2, 291.4, 326.5], range(61, 91))]

if __name__ == "__main__":
    for pdf, tag, rules, lams in HALVES:
        lams = list(lams)
        tv = [[decl(l) for l in lams], lams, [180 - l for l in lams], [180 + l for l in lams], [360 - l for l in lams]]
        out = mp.run(pdf, 288, 742, rules, tv, nsub=[3, 1, 1, 1, 1], tag=tag, mods=[90, 360, 360, 360, 360],
                     fixed=[(0, 1)] * 5)
        print(pdf, tag, len(out["rows"]), out["classes"], "flags", len(out["flags"]))
        for f in out["flags"]:
            print("    ", f)
        n, files = mp.sheet(pdf, tag)
        print("    sheet", n, [f.split("\\")[-1] for f in files])
    # p. 58, right: right ascensions of the decades and their sines
    lams = list(range(10, 100, 10))
    tv = [[round(ra(l) * 3600) for l in lams], [round(60 * math.sin(math.radians(ra(l))) * 3600) for l in lams]]
    out = mp.run(507, 600, 726, [371.9, 418.8, 499.4, 576.0], tv, args=lams, nsub=[3, 3], tag="RA", mods=[360, 61],
                 fixed=[(0, 1)] * 2)
    print(507, "RA", len(out["rows"]), out["classes"], "flags", len(out["flags"]))
    for f in out["flags"]:
        print("    ", f)
    print("    args off", [(i + 1, r["arg"], r["arg_exp"]) for i, r in enumerate(out["rows"]) if r.get("arg_ok") is False])
    n, files = mp.sheet(507, "RA")
    print("    sheet", n, [f.split("\\")[-1] for f in files])

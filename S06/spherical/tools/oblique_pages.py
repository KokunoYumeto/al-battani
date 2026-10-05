"""Read Part II pp. 65-67: the oblique ascensions of every tenth degree of the ecliptic (counted from Aries) for the
latitudes of the climes (pp. 65-66), and for Mekkah, Baghdad and Harran with the seasonal hours (p. 67).
  oblique ascension  OA = RA - arcsin(tan phi tan delta)      seasonal hour  (180 + 2 arcsin(tan phi tan delta)) / 12
with sin delta = sin lambda sin 23 35'. Output: p3_kit/MP{pdf}.json and contact sheets."""
import math
import motion_page as mp

EPS = math.radians(23 + 35 / 60)


def dms(d, m):
    return d + m / 60


def decl(lam):
    return math.asin(math.sin(math.radians(lam)) * math.sin(EPS))


def ra(lam):
    l = math.radians(lam)
    return math.degrees(math.atan2(math.cos(EPS) * math.sin(l), math.cos(l))) % 360


def asc_diff(lam, phi):
    return math.degrees(math.asin(math.tan(math.radians(phi)) * math.tan(decl(lam))))


def oblique(lam, phi):
    if lam == 360:
        return 360.0
    return (ra(lam) - asc_diff(lam, phi)) % 360


def hour(lam, phi):
    return (180 + 2 * asc_diff(lam, phi)) / 12


LATS = {514: [dms(16, 39), dms(20, 28), dms(24, 5), dms(27, 28), dms(30, 40), dms(33, 37)],
        515: [dms(36, 22), dms(38, 54), dms(41, 15), dms(43, 25), dms(45, 22), dms(47, 12), dms(48, 53)],
        516: [dms(21, 40), dms(33, 9), dms(36, 40)]}
RULES = {514: [104.4, 139.2, 197.2, 254.5, 314.5, 372.5, 432.2, 489.4],
         515: [148.2, 176.2, 226.9, 277.1, 329.0, 379.0, 430.8, 481.1, 534.4],
         516: [103.3, 137.8, 195.6, 253.3, 313.2, 370.8, 430.9, 488.0]}


def expected(pdf):
    lams = list(range(10, 370, 10))
    tv = []
    if pdf in (514, 515):
        for phi in LATS[pdf]:
            tv.append([round(oblique(l, phi) * 60) for l in lams])
    else:
        for phi in LATS[pdf]:
            tv.append([round(oblique(l, phi) * 60) for l in lams])
            tv.append([round(hour(l, phi) * 60) for l in lams])
    return lams, tv


def run_page(pdf, y0=282, y1=775):
    lams, tv = expected(pdf)
    n = len(tv)
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= n      # drop fragments of the rules
    return mp.run(pdf, y0, y1, RULES[pdf], tv, args=lams, nsub=[2] * n, mods=[361] * n, fixed=[(0, 1)] * n, keep=keep)


if __name__ == "__main__":
    for pdf in (514, 515, 516):
        out = run_page(pdf)
        bad = [(i + 1, r["arg"], r["arg_exp"]) for i, r in enumerate(out["rows"]) if r.get("arg_ok") is False]
        print(pdf, len(out["rows"]), out["classes"], "flags", len(out["flags"]), "args off", bad[:6])
        for f in out["flags"]:
            print("    ", f)
        k, files = mp.sheet(pdf)
        print("    sheet", k, [f.split("\\")[-1] for f in files])


def fitted_lats(pdf):
    """for each column: the latitude that best fits the cells both readers agree on (golden-section search)"""
    import json
    import wide_kit as wk
    d = json.load(open(wk.OUT + f"MP{pdf}.json", encoding="utf-8"))
    lams = list(range(10, 370, 10))
    out = []
    for k, phi0 in enumerate(LATS[pdf]):
        gi = k if pdf != 516 else 2 * k
        pts = []
        for i, r in enumerate(d["rows"]):
            g = r["groups"][gi]
            if all(c and c["read"] and c["read"] == c.get("tl") and c["conf"] >= 0.85 for c in g):
                pts.append((lams[i], int(g[0]["read"]) * 60 + int(g[1]["read"])))
        pts = [(l, v) for l, v in pts if l % 180]           # 180 and 360 do not depend on the latitude

        phi = phi0
        for _ in range(3):                                   # refit without the points more than 5' off
            use = [(l, v) for l, v in pts if abs(v - oblique(l, phi) * 60) <= 5]

            def cost(x):
                return sum((v - oblique(l, x) * 60) ** 2 for l, v in use)
            a, b = phi0 - 0.5, phi0 + 0.5
            for _ in range(60):
                c1, c2 = a + (b - a) * 0.382, a + (b - a) * 0.618
                if cost(c1) < cost(c2):
                    b = c2
                else:
                    a = c1
            phi = (a + b) / 2
        out.append((phi, len(use)))
    return out


def rerun_fitted():
    """resolve every column against its fitted latitude (the heads stay the reference of the check)"""
    for pdf in (514, 515, 516):
        lats = [phi for phi, _ in fitted_lats(pdf)]
        lams = list(range(10, 370, 10))
        tv = []
        for phi in lats:
            tv.append([round(oblique(l, phi) * 60) for l in lams])
            if pdf == 516:
                tv.append([round(hour(l, phi) * 60) for l in lams])
        n = len(tv)
        keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= n
        out = mp.run(pdf, 282, 775, RULES[pdf], tv, args=lams, nsub=[2] * n, mods=[361] * n, fixed=[(0, 1)] * n, keep=keep)
        print(pdf, out["classes"], "flags", len(out["flags"]))
        for f in out["flags"]:
            print("    ", f)
        k, files = mp.sheet(pdf)
        print("    sheet", k, [f.split("\\")[-1] for f in files])

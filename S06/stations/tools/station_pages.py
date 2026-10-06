"""Read Part II pp. 138-139: the stations of the planets (Saturn, Jupiter, Mars on p. 138, PDF 587; Venus, Mercury on
p. 139, PDF 588), 30 rows a page, n = 6, 12 ... 180 and 360 - n, each planet with Statio I and Statio II (degrees,
minutes). Statio I + Statio II = 360 in every row (Nallino, Part II p. 245).
Model for the expected values (Nallino, Part II pp. 245-247): the argument is the true centre (the elongation of the
centre of the epicycle from the apogee of the deferent, seen from the Earth); the station is interpolated between the
stations computed for the greatest, the mean and the least distance of the centre of the epicycle, in proportion to
the distance d at the true centre (Saturn, Venus, Mercury) or to the change of the greatest equation of the epicycle,
asin(r / d) (Jupiter, Mars). The three stations of each planet are fitted to the cells both readers agree on.
Elements (Ptolemy's): eccentricity of the deferent e and radius of the epicycle r, in parts of which the deferent
has 60: Saturn 3;25 and 6;30, Jupiter 2;45 and 11;30, Mars 6 and 39;30, Venus 1;15 and 43;10, Mercury 3 and 22;30.
Output: MP{pdf}{tag}.json via motion_page.run."""
import json, math, os, statistics
import numpy as np
import motion_page as mp
import p2cols, wide_kit as wk

ELEM = {"sat": (3 + 25 / 60, 6.5), "jup": (2.75, 11.5), "mars": (6.0, 39.5), "ven": (1.25, 43 + 10 / 60), "mer": (3.0, 22.5)}
WEIGHT = {"sat": "dist", "jup": "pmax", "mars": "pmax", "ven": "dist", "mer": "dist"}
PAGES = {587: ["sat", "jup", "mars"], 588: ["ven", "mer"]}
NS = list(range(6, 181, 6))
# Statio I as read by eye from 200 dpi renders of the pages (degrees and minutes, n = 6 ... 180): the third reader, and
# the expected values of the reading (Statio II expected as 360 minus Statio I)
EYE = {
    "sat": "112 45,112 46,112 49,112 52,112 56,113 1,113 7,113 14,113 21,113 28,113 36,113 44,113 53,114 2,114 11,"
           "114 19,114 27,114 35,114 43,114 50,114 57,115 3,115 9,115 14,115 19,115 23,115 26,115 28,115 29,115 29",
    "jup": "124 5,124 5,124 8,124 12,124 17,124 22,124 28,124 34,124 43,124 52,125 2,125 12,125 22,125 32,125 42,"
           "125 50,125 58,126 6,126 14,126 24,126 34,126 42,126 48,126 54,127 0,127 4,127 8,127 11,127 11,127 11",
    "mars": "157 33,157 37,157 47,157 57,158 15,158 33,158 57,159 21,159 51,160 21,160 56,161 31,162 9,162 47,163 22,"
            "163 57,164 31,165 5,165 39,166 11,166 41,167 11,167 37,168 1,168 21,168 41,168 53,169 5,169 10,169 14",
    "ven": "165 53,165 54,165 56,165 58,166 2,166 6,166 11,166 17,166 23,166 30,166 38,166 46,166 54,167 2,167 10,"
           "167 17,167 24,167 32,167 40,167 46,167 51,167 56,168 2,168 6,168 10,168 14,168 17,168 19,168 20,168 21",
    "mer": "147 13,147 8,147 0,146 49,146 36,146 21,146 6,145 50,145 34,145 18,145 5,144 55,144 49,144 43,144 38,"
           "144 34,144 32,144 30,144 30,144 29,144 29,144 30,144 32,144 34,144 36,144 37,144 38,144 39,144 40,144 40"}
EYE = {k: [int(a) * 60 + int(b) for a, b in (x.split() for x in v.split(","))] for k, v in EYE.items()}


class Station:
    def __init__(self, key):
        self.key = key
        self.e, self.r = ELEM[key]
        ds = [self.dist(m / 10) for m in range(1801)]
        self.dmax, self.dmin = max(ds), min(ds)

    def dist(self, m):
        """distance of the centre of the epicycle from the Earth for the mean centre m"""
        e, mr = self.e, math.radians(m)
        if self.key == "mer":
            ie = 2 * e * math.cos(mr / 2)
            a = 1.5 * mr
            eh = ie * math.cos(a) + math.sqrt(3600 - (ie * math.sin(a)) ** 2)
            return math.hypot(eh + e * math.cos(mr), e * math.sin(mr))
        hs = math.sqrt(3600 - (e * math.sin(mr)) ** 2)
        return math.hypot(hs + e * math.cos(mr), 2 * e * math.sin(mr))

    def centre(self, m):
        ne = (self.e if self.key == "mer" else 2 * self.e) * math.sin(math.radians(m))
        return math.degrees(math.asin(ne / self.dist(m)))

    def mean_of_true(self, k):
        m = k
        for _ in range(60):
            m = k + self.centre(m)
        return m

    def weights(self, k):
        """(w+, w-): the share of the step to the greatest distance (d > 60) or to the least (d < 60)"""
        d = self.dist(self.mean_of_true(k))
        if WEIGHT[self.key] == "dist":
            f = lambda x: x
        else:
            f = lambda x: -math.asin(self.r / x)
        if d >= 60:
            return (f(d) - f(60)) / (f(self.dmax) - f(60)), 0.0
        return 0.0, (f(d) - f(60)) / (f(self.dmin) - f(60))

    def fit(self, pts):
        """pts {n: minutes of Statio I}: least squares for the stations at the mean, greatest and least distance"""
        A = np.array([[1, *self.weights(n)] for n in pts])
        c, *_ = np.linalg.lstsq(A, np.array(list(pts.values()), float), rcond=None)
        self.anchors = (c[0], c[0] + c[1], c[0] + c[2])
        return self.anchors

    def first(self, n):
        a0, ap, am = self.anchors
        wp, wm = self.weights(n)
        return a0 + wp * (ap - a0) + wm * (am - a0)


def agreed(pdf, tag=""):
    """{(group, n): minutes} where both readers agree with confidence"""
    f = wk.OUT + f"MP{pdf}{tag}.json"
    if not os.path.exists(f):
        return {}
    ag = mp.agreed_units(f"{pdf}{tag}")
    return {(gi, NS[i]): u for (i, gi), u in ag.items() if i < len(NS)}


def geometry(pdf):
    page = wk.doc[pdf - 1]
    pts = sorted((w[1], int(w[4].strip("°.o�"))) for w in page.get_text("words")
                 if 250 < w[1] < 790 and w[0] < 160 and w[4].strip("°.o�").isdigit() and int(w[4].strip("°.o�")) in NS)
    best = None
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            (ya, na), (yb, nb) = pts[i], pts[j]
            if nb == na:
                continue
            b = (yb - ya) / (nb - na)
            if not 13.0 / 6 < b < 16.5 / 6:
                continue
            inl = [(y, n) for y, n in pts if abs(y - (ya + b * (n - na))) < 6]
            if best is None or len(inl) > len(best):
                best = inl
    b, a = np.polyfit([n for y, n in best], [y for y, n in best], 1)
    y0, y1 = a + b * 6 - 8, a + b * 180 + 14
    return y0, y1, p2cols.rules_banded(pdf, y0, y1)


def run_eye(pdf, tag="e"):
    """the reading with the eye values as the expected values: A both machine readers give the eye value, B one, C none"""
    keys = PAGES[pdf]
    y0, y1, rules = geometry(pdf)
    tv = [[360 - n for n in NS]]
    for key in keys:
        tv.append(EYE[key]); tv.append([21600 - u for u in EYE[key]])
    ng = len(tv)
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 5
    return mp.run(pdf, y0, y1, rules, tv, args=NS, nsub=[1] + [2] * (ng - 1), mods=[1000] + [360] * (ng - 1),
                  fixed=[(0, 1)] * ng, keep=keep, tag=tag)


def run(pdf, tag="", rules=None, model_tag=None, empirical=False):
    keys = PAGES[pdf]
    y0, y1, det = geometry(pdf)
    rules = rules or det
    # the model: three stations per planet fitted to the agreed cells of an earlier reading (model_tag), else Ptolemy's
    # rough values
    rough = {"sat": (6850, 6765, 6930), "jup": (7540, 7444, 7632), "mars": (9790, 9450, 10153),
             "ven": (10030, 9952, 10100), "mer": (8705, 8834, 8669)}
    ag = agreed(pdf, model_tag) if model_tag is not None else {}
    tv = [[360 - n for n in NS]]
    for p, key in enumerate(keys):
        st = Station(key)
        pts = {n: u for (gi, n), u in ag.items() if gi == 1 + 2 * p}
        pts.update({n: 21600 - u for (gi, n), u in ag.items() if gi == 2 + 2 * p and n not in pts})
        if len(pts) >= 6:
            st.fit(pts)
        else:
            st.anchors = rough[key]
        first = [st.first(n) for n in NS]
        if empirical and pts:
            res = {n: pts[n] - st.first(n) for n in pts}
            first = [f + (statistics.median([res[j] for j in NS if abs(j - n) <= 18 and j in res])
                          if any(abs(j - n) <= 18 and j in res for j in NS) else 0) for f, n in zip(first, NS)]
        tv.append([round(f) for f in first])
        tv.append([round(21600 - f) for f in first])
    ng = len(tv)
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 5
    return mp.run(pdf, y0, y1, rules, tv, args=NS, nsub=[1] + [2] * (ng - 1), mods=[1000] + [360] * (ng - 1),
                  fixed=[(0, 1)] * ng, keep=keep, tag=tag)


if __name__ == "__main__":
    import sys
    from collections import Counter
    args = sys.argv[1:]
    for pdf in [int(a) for a in args if a.isdigit()] or [587, 588]:
        y0, y1, det = geometry(pdf)
        print(pdf, "band", round(y0, 1), round(y1, 1), "rules", det)
        if "--rules" in args:
            continue
        if "--model" in args:
            out = run(pdf, tag="a")
            out = run(pdf, tag="b", model_tag="a", empirical=True)
        else:
            out = run_eye(pdf)
        bad = [(i + 1, r["arg"], r.get("arg_exp")) for i, r in enumerate(out["rows"]) if r.get("arg_ok") is False]
        print(pdf, len(out["rows"]), out["classes"], "flags", len(out["flags"]),
              Counter(int(f[1]) for f in out["flags"] if f[0] != "fit"), "args off", bad[:4])

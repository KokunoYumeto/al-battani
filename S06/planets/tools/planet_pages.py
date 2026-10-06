"""Read Part II pp. 108-137: the equations of the five planets (Saturn pp. 108-113, Jupiter 114-119, Mars 120-125,
Venus 126-131, Mercury 132-137), 30 rows a page, n = 1 ... 180 and 360 - n. Columns: III the equation of the centre
(degrees, minutes), IV the sixtieths for the two distances (minutes), V the difference at the greatest distance, VI the
equation of the anomaly at the mean distance, VII the difference at the least distance (degrees, minutes).
Models (Nallino, Part II pp. 239-245; equant eccentricity 2e and epicycle radius r in parts of which the deferent has 60):
  superior planets and Venus: the distance of the centre of the epicycle from the Earth for the mean centrum m is
  d = sqrt((sqrt(60^2 - (e sin m)^2) + e cos m)^2 + (2e sin m)^2), and sin(equation of the centre) = 2e sin m / d.
  Mercury (e = 3): IE' = 2e cos(m/2), E'H = IE' cos(3m/2) + sqrt(60^2 - (IE' sin(3m/2))^2),
  d = sqrt((E'H + e cos m)^2 + (e sin m)^2), sin(equation of the centre) = e sin m / d.
  equation of the anomaly at distance D: tan p = r sin n / (D + r cos n); VI at D = 60; V = p(60) - p(greatest d);
  VII = p(least d) - p(60); IV: 60 (pmax(60) - pmax(d)) / (pmax(60) - pmax(greatest d)) while d > 60, and
  60 (pmax(d) - pmax(60)) / (pmax(least d) - pmax(60)) while d < 60, with pmax(D) = asin(r / D).
Output: MP{pdf}{tag}.json via motion_page.run."""
import math, statistics
import motion_page as mp
import p2cols, wide_kit as wk

# first PDF page, equant eccentricity (2e; Mercury: 2 x 3), epicycle radius. Venus: the equation of the centre of the
# table reaches 1 59, the Sun's greatest equation, so its eccentricity is the Sun's 2;4,45 (Ptolemy 2;30)
PLANETS = {"sat": (557, 6 + 50 / 60, 6.5), "jup": (563, 5.5, 11.5), "mars": (569, 12.0, 39.5),
           "ven": (575, 2 + 4 / 60 + 45 / 3600, 43 + 10 / 60), "mer": (581, 6.0, 22.5)}


class Model:
    def __init__(self, key):
        self.key = key
        self.pdf0, e2, self.r = PLANETS[key]
        self.e = e2 / 2
        ds = [self.dist(m / 10) for m in range(0, 1801)]
        self.dmax, self.dmin = max(ds), min(ds)

    def dist(self, m):
        e, mr = self.e, math.radians(m)
        if self.key == "mer":
            ie = 2 * e * math.cos(mr / 2)
            a = mr + mr / 2
            eh = ie * math.cos(a) + math.sqrt(3600 - (ie * math.sin(a)) ** 2)
            return math.hypot(eh + e * math.cos(mr), e * math.sin(mr))
        hs = math.sqrt(3600 - (e * math.sin(mr)) ** 2)
        return math.hypot(hs + e * math.cos(mr), 2 * e * math.sin(mr))

    def centre(self, m):
        ne = (self.e if self.key == "mer" else 2 * self.e) * math.sin(math.radians(m))
        return math.degrees(math.asin(ne / self.dist(m)))

    def anom(self, n, D):
        nr = math.radians(n)
        return math.degrees(math.atan2(self.r * math.sin(nr), D + self.r * math.cos(nr)))

    def pmax(self, D):
        return math.asin(self.r / D)

    def sixtieths(self, m):
        if self.key != "mer":                  # Ptolemy's coefficients for the outer planets and Venus: about 60 |cos m|
            return 60 * abs(math.cos(math.radians(m)))
        d = self.dist(m)
        if d >= 60:
            return 60 * (self.pmax(60) - self.pmax(d)) / (self.pmax(60) - self.pmax(self.dmax))
        return 60 * (self.pmax(d) - self.pmax(60)) / (self.pmax(self.dmin) - self.pmax(60))

    def columns(self, n):
        """III, IV, V, VI, VII in minutes (IV in sixtieths)"""
        return [self.centre(n) * 60, self.sixtieths(n), (self.anom(n, 60) - self.anom(n, self.dmax)) * 60,
                self.anom(n, 60) * 60, (self.anom(n, self.dmin) - self.anom(n, 60)) * 60]


def planet_of(pdf):
    for key, (p0, _, _) in PLANETS.items():
        if p0 <= pdf < p0 + 6:
            return key, pdf - p0
    raise KeyError(pdf)


def geometry(pdf):
    """the band of the 30 rows, from the arguments of column I found in the text layer (the first and the last of
    them), and the vertical rules of the table"""
    page = wk.doc[pdf - 1]
    key, k = planet_of(pdf)
    first, last = 30 * k + 1, 30 * k + 30
    pts = sorted((w[1], int(w[4].strip("°.o"))) for w in page.get_text("words")
                 if 250 < w[1] < 770 and w[0] < 200 and w[4].strip("°.o").isdigit()
                 and first <= int(w[4].strip("°.o")) <= last)
    # the points on one line y = a + pitch n (the rows are evenly spaced, with small gaps every five): the pair of
    # points with a plausible pitch that has the most points within 6 pt of its line, then least squares on those
    import numpy as np
    best = None
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            (ya, na), (yb, nb) = pts[i], pts[j]
            if nb == na:
                continue
            b = (yb - ya) / (nb - na)
            if not 13.0 < b < 16.0:
                continue
            inl = [(y, n) for y, n in pts if abs(y - (ya + b * (n - na))) < 6]
            if best is None or len(inl) > len(best):
                best = inl
    if best and len(best) >= 6:
        b, a = np.polyfit([n for y, n in best], [y for y, n in best], 1)
        y0, y1 = a + b * first - 7, a + b * last + 13
    else:
        y0, y1 = 285, 745
    det = [x for x in p2cols.rules_banded(pdf, max(y0, 300), min(y1, 730)) if x < 560]
    return y0, y1, complete_rules(det)


WIDTHS = [35.5, 37.3, 69.5, 69.5, 69.5, 69.8, 71.0]


def complete_rules(det):
    """the eight rules of the table: the template of column widths placed so that most of its rules fall within 4 pt
    of detected ones, each rule snapped to the detected one"""
    best = None
    for x0 in det:
        for k in range(8):                      # the detected rule taken as the k-th rule of the template
            start = x0 - sum(WIDTHS[:k])
            tmpl = [start + sum(WIDTHS[:j]) for j in range(8)]
            snapped = []
            score = 0
            for t in tmpl:
                near = [d for d in det if abs(d - t) < 4]
                if near:
                    snapped.append(min(near, key=lambda d: abs(d - t))); score += 1
                else:
                    snapped.append(round(t, 1))
            if best is None or score > best[0]:
                best = (score, snapped)
    return best[1] if best else []


def agreed_values(key, tag=""):
    """(column, n) -> units for the cells of the planet's pages where both readers agree with confidence"""
    import json, os
    p0 = PLANETS[key][0]
    out = {}
    for k in range(6):
        f = wk.OUT + f"MP{p0 + k}{tag}.json"
        if not os.path.exists(f):
            continue
        d = json.load(open(f, encoding="utf-8"))
        for i, r in enumerate(d["rows"]):
            n = 30 * k + i + 1
            for gi, g in enumerate(r["groups"]):
                if all(c and c["read"] and c["read"] == c.get("tl") and c["conf"] >= 0.85 for c in g):
                    u = 0
                    for c in g:
                        u = u * 60 + int(c["read"])
                    out[(gi, n)] = u
    return out


def run(pdf, tag="", empirical=False):
    key, k = planet_of(pdf)
    M = Model(key)
    ns = list(range(30 * k + 1, 30 * k + 31))
    model = {col: {n: M.columns(n)[col - 1] for n in range(1, 181)} for col in range(1, 6)}
    if empirical:                      # the computation plus the running median of the residuals of the agreed values
        ag = agreed_values(key)
        for col in range(1, 6):
            res = {n: ag[(col, n)] - model[col][n] for n in range(1, 181) if (col, n) in ag}
            model[col] = {n: model[col][n] + (statistics.median([res[j] for j in range(n - 3, n + 4) if j in res])
                                                if any(j in res for j in range(n - 3, n + 4)) else 0) for n in range(1, 181)}
    tv = [[360 - n for n in ns]] + [[round(model[col][n]) for n in ns] for col in range(1, 6)]
    y0, y1, rules = geometry(pdf)
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 7
    return mp.run(pdf, y0, y1, rules, tv, args=ns, nsub=[1, 2, 1, 2, 2, 2], mods=[1000, 360, 1000, 360, 360, 360],
                  fixed=[(0, 1)] * 6, keep=keep, tag=tag)


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    emp = "--emp" in args
    pdfs = [int(a) for a in args if a.isdigit()] or list(range(557, 587))
    for pdf in pdfs:
        out = run(pdf, tag="b" if emp else "", empirical=emp)
        bad = [(i + 1, r["arg"], r.get("arg_exp")) for i, r in enumerate(out["rows"]) if r.get("arg_ok") is False]
        from collections import Counter
        print(pdf, len(out["rows"]), out["classes"], "flags", len(out["flags"]), Counter(int(f[1]) for f in out["flags"]
                                                                                         if f[0] != "fit"), "args off", bad[:4])

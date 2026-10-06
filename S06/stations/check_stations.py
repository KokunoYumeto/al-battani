"""Check of Nallino's Part II pp. 138-139 (the stations of the planets), from stations_p2.tsv.
1. Every row: 360 - n in the second column, and Statio I + Statio II = 360° (Nallino, Part II p. 245: if the first
   station falls at the corrected anomaly 180° - psi, the second falls at 180° + psi).
2. Statio I against the construction Nallino describes (Part II pp. 245-247): the stations are computed for the
   greatest, the mean and the least distance of the centre of the epicycle from the Earth, and a station at another
   place of the epicycle is the station at the mean distance changed in proportion to the change of the distance
   (statio = statio media +- II x III / I). The argument is the true centre (Nallino p. 247 n. 1), so the distance is
   taken at the true centre. Elements (Ptolemy's): eccentricity of the deferent e and radius of the epicycle r, in parts
   of which the deferent has 60: Saturn 3;25 and 6;30, Jupiter 2;45 and 11;30, Mars 6 and 39;30, Venus 1;15 and 43;10,
   Mercury 3 (with the circlet that carries the centre of its deferent) and 22;30. For Jupiter and Mars the proportion
   follows the greatest equation of the epicycle, asin(r / d), rather than the distance d itself: for Mars, whose
   epicycle is large, the two rules differ by up to 8′ and the table follows the second (0.9′ against 3.8′ r.m.s.).
   The three stations of each planet are fitted to its 30 values by least squares. Mars is computed every 12°: its
   values at 18°, 30° ... 174° are the means of their neighbours (the steps of the column come in equal pairs, 10′, 10′,
   18′, 18′, 24′, 24′ ...), and the computation is halved in the same way.
A value more than TOL off its computation is listed when it, or a value of its run (consecutive values off in the same
direction), is more than LIST off; a single value is also listed when it departs from the mean of its two neighbours
by SPIKE more than the computation does. Nallino's note on the stations of Mars at 90° needs a ledger entry of kind
«noted». Every listed difference must be in stations_discrepancies.tsv. --list shows the ledgered entries too, --stats
the fit of each planet."""
import csv, math, sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TOL, LIST, SPIKE = 3, 4, 2
ELEM = {"sat": (3 + 25 / 60, 6.5), "jup": (2.75, 11.5), "mars": (6.0, 39.5), "ven": (1.25, 43 + 10 / 60), "mer": (3.0, 22.5)}
WEIGHT = {"sat": "dist", "jup": "pmax", "mars": "pmax", "ven": "dist", "mer": "dist"}
STEP = {"mars": 12}
NAMES = {"sat": "Saturn", "jup": "Jupiter", "mars": "Mars", "ven": "Venus", "mer": "Mercury"}
NOTED = ["p. 138 mars 90"]


def read(name):
    return list(csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t"))


class Planet:
    def __init__(self, key):
        self.key = key
        self.e, self.r = ELEM[key]
        ds = [self.dist(m / 10) for m in range(1801)]
        self.dmax, self.dmin = max(ds), min(ds)

    def dist(self, m):
        """the distance of the centre of the epicycle from the Earth at the mean centre m"""
        e, mr = self.e, math.radians(m)
        if self.key == "mer":
            ie = 2 * e * math.cos(mr / 2)
            a = 1.5 * mr
            eh = ie * math.cos(a) + math.sqrt(3600 - (ie * math.sin(a)) ** 2)
            return math.hypot(eh + e * math.cos(mr), e * math.sin(mr))
        hs = math.sqrt(3600 - (e * math.sin(mr)) ** 2)
        return math.hypot(hs + e * math.cos(mr), 2 * e * math.sin(mr))

    def centre(self, m):
        """the equation of the centre at the mean centre m"""
        ne = (self.e if self.key == "mer" else 2 * self.e) * math.sin(math.radians(m))
        return math.degrees(math.asin(ne / self.dist(m)))

    def dist_true(self, k):
        """the distance at the true centre k (the mean centre m solves m - q(m) = k)"""
        m = k
        for _ in range(60):
            m = k + self.centre(m)
        return self.dist(m)

    def weights(self, k, rule):
        d = self.dist_true(k)
        f = (lambda x: x) if rule == "dist" else (lambda x: -math.asin(self.r / x))
        if d >= 60:
            return (f(d) - f(60)) / (f(self.dmax) - f(60)), 0.0
        return 0.0, (f(d) - f(60)) / (f(self.dmin) - f(60))

    def fit(self, ns, vals, rule, step=6):
        row = lambda n: np.array([1, *self.weights(n, rule)])
        A = np.array([row(n) if n % step == 0 else (row(n - step // 2) + row(n + step // 2)) / 2 for n in ns])
        c, *_ = np.linalg.lstsq(A, np.array(vals, float), rcond=None)
        return A @ c, (c[0], c[0] + c[1], c[0] + c[2])


def dm(u):
    return f"{int(u // 60)}° {u % 60:.1f}′" if isinstance(u, float) else f"{u // 60}° {u % 60}′"


R = read("stations_p2.tsv")
found, printed, model, agree, stats = [], {}, {}, [0], {}
identities = [0, 0]
for r in R:
    n = int(r["n"])
    s1 = int(r["s1_d"]) * 60 + int(r["s1_m"]); s2 = int(r["s2_d"]) * 60 + int(r["s2_m"])
    if int(r["n2"]) == 360 - n:
        identities[0] += 1
    else:
        found.append((f"p. {r['ppage']} {r['planet']} {n} 360-n", r["n2"], str(360 - n)))
    if s1 + s2 == 21600:
        identities[1] += 1
    else:
        found.append((f"p. {r['ppage']} {r['planet']} {n} sum", f"{dm(s1)} + {dm(s2)}", "360° 0′"))
runs = []
for key in ELEM:
    T = [r for r in R if r["planet"] == key]
    pl = Planet(key)
    ns = [int(r["n"]) for r in T]
    vals = [int(r["s1_d"]) * 60 + int(r["s1_m"]) for r in T]
    comp, anchors = pl.fit(ns, vals, WEIGHT[key], STEP.get(key, 6))
    other, _ = pl.fit(ns, vals, "pmax" if WEIGHT[key] == "dist" else "dist", STEP.get(key, 6))
    dev = [v - c for v, c in zip(vals, comp)]
    rms = lambda d: math.sqrt(sum(x * x for x in d) / len(d))
    stats[key] = (anchors, max(abs(x) for x in dev), sum(abs(x) <= 1 for x in dev), rms(dev),
                  rms([v - c for v, c in zip(vals, other)]))
    pg = T[0]["ppage"]
    for r, c in zip(T, comp):
        w = f"p. {pg} {key} {r['n']}"
        printed[w], model[w] = f"{r['s1_d']}° {r['s1_m']}′", c
    i = 0
    while i < len(T):
        w = f"p. {pg} {key} {T[i]['n']}"
        if abs(dev[i]) > TOL and w not in NOTED:
            j = i
            while j + 1 < len(T) and abs(dev[j + 1]) > TOL and (dev[j + 1] > 0) == (dev[i] > 0) \
                    and f"p. {pg} {key} {T[j + 1]['n']}" not in NOTED:
                j += 1
            worst = max(range(i, j + 1), key=lambda k: abs(dev[k]))
            if abs(dev[worst]) > LIST:
                a, b = T[i]["n"], T[j]["n"]
                runs.append((key, int(a), int(b)))
                found.append((f"p. {pg} {key} {a}" + (f"-{b}" if b != a else ""),
                              ", ".join(dm(vals[k]) for k in range(i, j + 1)),
                              f"computed {', '.join(dm(comp[k]) for k in range(i, j + 1))}"))
            else:
                agree[0] += j - i + 1
            i = j + 1
        else:
            agree[0] += 1
            i += 1
    for k in range(1, len(T) - 1):
        p = vals[k] - (vals[k - 1] + vals[k + 1]) / 2
        q = comp[k] - (comp[k - 1] + comp[k + 1]) / 2
        n = ns[k]
        w = f"p. {pg} {key} {n}"
        if abs(p - q) >= SPIKE and w not in NOTED and not any(rk == key and a - 6 <= n <= b + 6 for rk, a, b in runs):
            found.append((w + " (neighbours)", dm(vals[k]),
                          f"the neighbours {dm(vals[k - 1])} and {dm(vals[k + 1])}; computed {dm(comp[k - 1])}, "
                          f"{dm(comp[k])}, {dm(comp[k + 1])}"))


def main():
    rows = read("stations_discrepancies.tsv")
    ledger = {r["where"] for r in rows if r["kind"] != "noted"}
    noted = {r["where"]: r for r in rows if r["kind"] == "noted"}
    problems = [f"no ledger entry for Nallino's note: {w} (printed {printed.get(w)})" for w in NOTED if w not in noted]
    problems += [f"{w}: the ledger says printed {noted[w]['printed']}, the table has {printed.get(w)}"
                 for w in NOTED if w in noted and not noted[w]["printed"].startswith(printed.get(w, "?"))]
    open_ = [f for f in found if f[0] not in ledger]
    print(f"identities: 360 - n {identities[0]} of {len(R)}, Statio I + Statio II = 360° {identities[1]} of {len(R)}; "
          f"Statio I within tolerance {agree[0]}, differ {len(found)} (ledgered {len(found) - len(open_)}, open "
          f"{len(open_)}); Nallino's notes {len(NOTED)}, problems {len(problems)}")
    if "--stats" in sys.argv:
        for key, (anc, mx, w1, rms, rms_other) in stats.items():
            print(f"  {NAMES[key]} ({WEIGHT[key]}): stations at the mean, greatest and least distance "
                  f"{dm(anc[0])}, {dm(anc[1])}, {dm(anc[2])}; largest departure {mx:.1f}′, within 1′: {w1} of 30, "
                  f"r.m.s. {rms:.2f}′ (with the other rule {rms_other:.2f}′)")
    for where, p, e in (found if "--list" in sys.argv else open_):
        print(f"  {where}: {p}; {e}" + ("" if where in ledger else "   << not in the ledger"))
    for p in problems:
        print("  " + p)
    stale = [w for w in ledger if w not in {f[0] for f in found}]
    for w in stale:
        print("  ledger entry without a difference:", w)
    sys.exit(1 if open_ or stale or problems else 0)


if __name__ == "__main__":
    main()

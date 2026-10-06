"""Check of Nallino's Part II pp. 108-137 (the equations of the five planets), from planets_p2.tsv and planets_pages.tsv.
Elements (Nallino, Part II p. 244): the eccentricity of the equant (twice that of the deferent) and the radius of the
epicycle at the mean distance, in parts of which the deferent has 60: Saturn 6;50 and 6;30, Jupiter 5;30 and 11;30,
Mars 12 and 39;30, Venus 2;30 and 43;10, Mercury 3 (the distance of the equant from the Earth) and 22;30.
  III  the equation of the centre for the centrum n: sin q = 2e sin n / d (Mercury: e sin n / d), d the distance of the
       centre of the epicycle from the Earth (Nallino pp. 240 and 244). For Venus the column follows al-Battani's solar
       eccentricity, 2;4,45 for the equant: its greatest value is the Sun's greatest equation, 1° 59′.
  V, VI, VII  the equation of the anomaly n at the mean distance 60 (VI), and its difference from the equation at the
       greatest distance of the centre of the epicycle (V) and at the least (VII): tan p = r sin n / (D + r cos n). For
       Venus the distances are Ptolemy's, 61;15 and 58;45 (eccentricity 1;15).
  IV   the sixtieths: for the outer planets and Venus they follow 60 |cos n|; for Mercury, 60 times the excess of the
       distance of the centre of the epicycle over the mean distance in its greatest excess (69 - 60), or its defect in
       the greatest defect (60 - 55;34).
A value more than TOL off its computation is listed when it, or a value of its run (consecutive values off in the same
direction), is more than LIST off (for Mercury's sixtieths, whose computation is only approximate, 6 and 6); a single value is also listed when it departs from the mean of its two neighbours by
SPIKE more than the computation does. The cells Nallino emends (p. 238) need ledger entries of kind «noted». The
numbers of the lines above the first table of each planet (Arabic, Maghribi abjad) are compared with the Latin.
Every listed difference must be in planets_discrepancies.tsv. --list shows the ledgered entries too."""
import csv, math, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOL, LIST, SPIKE = 3, 4, 2
COLS = ["c3", "c4", "c5", "c6", "c7"]
NAMES = {"c3": "III", "c4": "IV", "c5": "V", "c6": "VI", "c7": "VII"}
ELEM = {"sat": (6 + 50 / 60, 6.5), "jup": (5.5, 11.5), "mars": (12.0, 39.5), "ven": (2.5, 43 + 10 / 60), "mer": (6.0, 22.5)}
SUN_E2 = 2 + 4 / 60 + 45 / 3600
NOTED = ["p. 116 jup 90 III", "p. 117 jup 91 III"]
ABJAD = dict(zip("ابجدهوزحطيكلمنصعفضقرستثخذظغش",
                 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800,
                  900, 1000]))


def read(name):
    return list(csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t"))


class Planet:
    def __init__(self, key):
        self.key = key
        e2, self.r = ELEM[key]
        self.e = e2 / 2
        self.e_centre = SUN_E2 / 2 if key == "ven" else self.e
        ds = [self.dist(m / 10, self.e) for m in range(1801)]
        self.dmax, self.dmin = max(ds), min(ds)

    def dist(self, m, e):
        mr = math.radians(m)
        if self.key == "mer":
            e = 3.0
            ie = 2 * e * math.cos(mr / 2)
            a = 1.5 * mr
            eh = ie * math.cos(a) + math.sqrt(3600 - (ie * math.sin(a)) ** 2)
            return math.hypot(eh + e * math.cos(mr), e * math.sin(mr))
        hs = math.sqrt(3600 - (e * math.sin(mr)) ** 2)
        return math.hypot(hs + e * math.cos(mr), 2 * e * math.sin(mr))

    def anom(self, n, D):
        nr = math.radians(n)
        return math.degrees(math.atan2(self.r * math.sin(nr), D + self.r * math.cos(nr)))

    def col(self, c, n):
        """the computed value in minutes (IV in sixtieths)"""
        if c == "c3":
            e = self.e_centre
            ne = (3.0 if self.key == "mer" else 2 * e) * math.sin(math.radians(n))
            return math.degrees(math.asin(ne / self.dist(n, e))) * 60
        if c == "c4":
            if self.key != "mer":
                return 60 * abs(math.cos(math.radians(n)))
            d = self.dist(n, 3.0)
            return 60 * (d - 60) / (self.dmax - 60) if d >= 60 else 60 * (60 - d) / (60 - self.dmin)
        if c == "c5":
            return (self.anom(n, 60) - self.anom(n, self.dmax)) * 60
        if c == "c6":
            return self.anom(n, 60) * 60
        return (self.anom(n, self.dmin) - self.anom(n, 60)) * 60


def units(r, c):
    return int(r["c4"]) if c == "c4" else int(r[c + "_d"]) * 60 + int(r[c + "_m"])


def show(r, c):
    return f"{r['c4']}" if c == "c4" else f"{r[c + '_d']}° {r[c + '_m']}′"


def fmt(x, c):
    if c == "c4":
        return f"{x:.1f}"
    s = round(x, 1)
    return f"{int(s // 60)}° {s % 60:.1f}′"


R = read("planets_p2.tsv")
P = {k: Planet(k) for k in ELEM}
found, printed, model, agree = [], {}, {}, [0]
stats, runs = {}, []


def key(r, c):
    return f"p. {r['ppage']} {r['planet']} {r['n']} {NAMES[c]}"


for pk, pl in P.items():
    T = [r for r in R if r["planet"] == pk]
    for c in COLS:
        dev = []
        for r in T:
            m = pl.col(c, int(r["n"]))
            printed[key(r, c)], model[key(r, c)] = show(r, c), m
            dev.append(units(r, c) - m)
        stats[(pk, c)] = (max(abs(x) for x in dev), sum(abs(x) <= 2 for x in dev))
        # runs beyond TOL, listed when one value is beyond LIST
        tol, lst = (6, 6) if (pk, c) == ("mer", "c4") else (TOL, LIST)
        i = 0
        while i < len(T):
            if abs(dev[i]) > tol and key(T[i], c) not in NOTED:
                j = i
                while j + 1 < len(T) and abs(dev[j + 1]) > tol and (dev[j + 1] > 0) == (dev[i] > 0) \
                        and key(T[j + 1], c) not in NOTED:
                    j += 1
                worst = max(range(i, j + 1), key=lambda k: abs(dev[k]))
                if abs(dev[worst]) > lst:
                    a, b = T[i]["n"], T[j]["n"]
                    runs.append((pk, c, int(a), int(b)))
                    found.append((f"p. {T[i]['ppage']} {pk} {a}" + (f"-{b}" if b != a else "") + f" {NAMES[c]}",
                                  ", ".join(show(T[k], c) for k in range(i, j + 1)),
                                  f"computed {', '.join(fmt(model[key(T[k], c)], c) for k in range(i, j + 1))}"))
                else:
                    agree[0] += j - i + 1
                i = j + 1
            else:
                agree[0] += 1
                i += 1
        # isolated spikes against the neighbours
        for k in range(1, len(T) - 1):
            p = units(T[k], c) - (units(T[k - 1], c) + units(T[k + 1], c)) / 2
            q = model[key(T[k], c)] - (model[key(T[k - 1], c)] + model[key(T[k + 1], c)]) / 2
            n = int(T[k]["n"])
            if abs(p - q) >= SPIKE and key(T[k], c) not in NOTED                     and not any(rp == pk and rc == c and a - 1 <= n <= b + 1 for rp, rc, a, b in runs):
                found.append((f"p. {T[k]['ppage']} {pk} {T[k]['n']} {NAMES[c]} (neighbours)", show(T[k], c),
                              f"the neighbours {show(T[k - 1], c)} and {show(T[k + 1], c)}; computed "
                              f"{fmt(model[key(T[k - 1], c)], c)}, {fmt(model[key(T[k], c)], c)}, "
                              f"{fmt(model[key(T[k + 1], c)], c)}"))


# the lines above the first table of each planet
def abjad(word):
    if word == "{0}":
        return 0
    if word.startswith("ا") and len(word) > 2:            # a leading alif counts the thousand (اقضا = 1191)
        return 1000 + abjad(word[1:])
    return sum(ABJAD[ch] for ch in word)


for page in read("planets_pages.tsv"):
    if not page["above_ar"]:
        continue
    words = page["above_ar"].split()
    la = [int(x) for x in re.findall(r"\d+", page["above_la"])]
    i = words.index("القرنين")
    ar_vals = [abjad(words[words.index("اقضا")])] + [abjad(w) for w in words[i + 1:i + 3]]
    if "ليوم" in words:
        j = words.index("ليوم")
        ar_vals += [abjad(w) for w in words[j + 1:j + 3]]
    w = f"p. {page['ppage']} apogee line"
    printed[w] = " ".join(words[i + 1:i + 3])
    if ar_vals != la[:len(ar_vals)]:
        found.append((w, " ".join(words[i + 1:]), f"Arabic {ar_vals}, Latin {la}"))
    else:
        agree[0] += 1


def main():
    rows = read("planets_discrepancies.tsv")
    ledger = {r["where"] for r in rows if r["kind"] != "noted"}
    noted = {r["where"]: r for r in rows if r["kind"] == "noted"}
    problems = [f"no ledger entry for Nallino's emendation: {w} (printed {printed.get(w)})" for w in NOTED if w not in noted]
    problems += [f"{w}: the ledger says printed {noted[w]['printed']}, the table has {printed.get(w)}"
                 for w in NOTED if w in noted and noted[w]["printed"] != printed.get(w)]
    open_ = [f for f in found if f[0] not in ledger]
    print(f"values within tolerance {agree[0]}, differ {len(found)} (ledgered {len(found) - len(open_)}, open {len(open_)}); "
          f"Nallino's emendations {len(NOTED)}, problems {len(problems)}")
    if "--stats" in sys.argv:
        for (pk, c), (mx, w2) in stats.items():
            print(f"  {pk} {NAMES[c]}: largest departure {mx:.1f}, within 2: {w2} of 180")
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

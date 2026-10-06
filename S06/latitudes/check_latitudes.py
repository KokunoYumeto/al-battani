"""Check of Nallino's Part II pp. 140-141 (the latitudes of the planets), from latitudes_p2.tsv. The argument n is the
true anomaly, counted from the true apogee of the epicycle. Elements (Ptolemy's, as Nallino gives them, Part II pp.
247-255): radius of the epicycle r and eccentricity e in parts of which the deferent has 60, inclination of the
deferent to the ecliptic i0 and of the epicycle to the deferent i: Saturn 6;30, 3;25, 2;30, 4;30; Jupiter 11;30, 2;45,
1;30, 2;30; Mars 39;30, 6, 1, 2;15; Venus 43;10, 1;15, inclination 2;30, obliquity 3;30; Mercury 22;30, 3, 6;15, 7.
1. Saturn, Jupiter, Mars (p. 140): the latitude with the centre of the epicycle at the northern and at the southern
   limit of the deferent, the apogee of the epicycle tilted by i towards the ecliptic (Nallino pp. 247-249). The limits
   lie 50° before the apogee of the deferent for Saturn, 20° after it for Jupiter, at the apogee for Mars; the distance d
   of the centre of the epicycle is taken there (at the true centre). With the planet at the anomaly n:
   x = d cos i0 + r cos n cos(i0 - i), y = r sin n, z = d sin i0 + r cos n sin(i0 - i), latitude = atan(z / hypot(x, y)).
2. Venus, Mercury, Inclinatio (p. 141): the latitude produced by the inclination i of the diameter through the apogee of
   the epicycle, with the centre of the epicycle at a node, 90° from the apogee of the deferent (Nallino p. 251):
   sin(incl.) = r |cos n| sin i / sqrt((d + r cos n cos i)^2 + (r sin n)^2 + (r cos n sin i)^2).
3. Venus, Mercury, Obliquitas: Ptolemy takes the obliquity proportional to the equation of the anomaly at the mean
   distance, the greatest equation (46° for Venus, 22° for Mercury) giving the greatest obliquity, 2° 30′ (Nallino
   p. 253). The equation is al-Battani's own column VI of the tables of Venus and Mercury (../planets/planets_p2.tsv).
4. Portiones latitudinum (p. 141): twelve times the latitude of the Moon (greatest latitude 5°) at the distance n from
   the limit, the latitude taken to whole minutes (Nallino p. 254): every value a multiple of 12′, the same at n and
   180° - n, and its twelfth within 1′ of asin(sin 5° |cos n|) rounded to the minute.
A value more than TOL off its computation is listed when it, or a value of its run (consecutive values off in the same
direction), is more than LIST off; a single value is also listed when it departs from the mean of its two neighbours by
SPIKE more than the computation does. Every listed difference must be in latitudes_discrepancies.tsv; the cells on
which Nallino's notes comment need ledger entries of kind «noted». --list shows the ledgered entries too, --stats the
largest departure of each column."""
import csv, math, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOL, LIST, SPIKE = 3, 4, 2
SUP = {"sat": (6.5, 3 + 25 / 60, 2.5, 4.5, 50), "jup": (11.5, 2.75, 1.5, 2.5, 20), "mars": (39.5, 6.0, 1.0, 2.25, 0)}
INF = {"ven": (43 + 10 / 60, 1.25, 2.5, 46), "mer": (22.5, 3.0, 6.25, 22)}
NAMES = {"sat_n": "Saturn north", "sat_s": "Saturn south", "jup_n": "Jupiter north", "jup_s": "Jupiter south",
         "mars_n": "Mars north", "mars_s": "Mars south", "ven_inc": "Venus inclination", "ven_obl": "Venus obliquity",
         "mer_inc": "Mercury inclination", "mer_obl": "Mercury obliquity", "portio": "portions"}
NOTED = ["p. 140 sat_s 180", "p. 141 mer_obl 30"]
rad = math.radians


def read(name, folder=HERE):
    return list(csv.DictReader(open(folder / name, encoding="utf-8"), delimiter="\t"))


def dist(key, m, e):
    """the distance of the centre of the epicycle from the Earth at the mean centre m (Nallino p. 240; Mercury p. 243)"""
    mr = rad(m)
    if key == "mer":
        ie = 2 * e * math.cos(mr / 2)
        a = 1.5 * mr
        eh = ie * math.cos(a) + math.sqrt(3600 - (ie * math.sin(a)) ** 2)
        return math.hypot(eh + e * math.cos(mr), e * math.sin(mr))
    hs = math.sqrt(3600 - (e * math.sin(mr)) ** 2)
    return math.hypot(hs + e * math.cos(mr), 2 * e * math.sin(mr))


def dist_true(key, k, e):
    """the distance at the true centre k: the mean centre m solves m - q(m) = k, q the equation of the centre"""
    m = k
    for _ in range(60):
        ne = (e if key == "mer" else 2 * e) * math.sin(rad(m))
        m = k + math.degrees(math.asin(ne / dist(key, m, e)))
    return dist(key, m, e)


def sup_lat(n, d, r, i0, i):
    x = d * math.cos(rad(i0)) + r * math.cos(rad(n)) * math.cos(rad(i0 - i))
    z = d * math.sin(rad(i0)) + r * math.cos(rad(n)) * math.sin(rad(i0 - i))
    return math.degrees(math.atan2(z, math.hypot(x, r * math.sin(rad(n))))) * 60


def inf_inc(n, d, r, i):
    c, s = math.cos(rad(n)), math.sin(rad(n))
    et = math.sqrt((d + r * c * math.cos(rad(i))) ** 2 + (r * s) ** 2 + (r * c * math.sin(rad(i))) ** 2)
    return math.degrees(math.asin(r * abs(c) * math.sin(rad(i)) / et)) * 60


R = read("latitudes_p2.tsv")
VI = {(p["planet"], int(p["n"])): int(p["c6_d"]) * 60 + int(p["c6_m"]) for p in read("planets_p2.tsv", HERE.parent / "planets")}
cols = {}
for r in R:
    cols.setdefault(r["column"], []).append(r)
model, extra = {}, {}
for key, (r, e, i0, i, lim) in SUP.items():
    dn, ds = dist_true(key, lim, e), dist_true(key, 180 - lim, e)
    extra[key] = (dn, ds)
    model[f"{key}_n"] = lambda n, d=dn, r=r, i0=i0, i=i: sup_lat(n, d, r, i0, i)
    model[f"{key}_s"] = lambda n, d=ds, r=r, i0=i0, i=i: sup_lat(n, d, r, i0, i)
for key, (r, e, i, pmax) in INF.items():
    dnode = dist_true(key, 90, e)
    extra[key] = (dnode,)
    model[f"{key}_inc"] = lambda n, d=dnode, r=r, i=i: inf_inc(n, d, r, i)
    model[f"{key}_obl"] = lambda n, key=key, pmax=pmax: VI[(key, n)] * 2.5 / pmax
model["portio"] = lambda n: 12 * round(60 * math.degrees(math.asin(math.sin(rad(5)) * abs(math.cos(rad(n))))))


def dm(u):
    return f"{int(u // 60)}° {u % 60:.1f}′" if isinstance(u, float) else f"{u // 60}° {u % 60}′"


found, printed, agree, stats, identities = [], {}, [0], {}, [0, 0]
for col, T in cols.items():
    pg = T[0]["ppage"]
    ns = [int(r["n"]) for r in T]
    vals = [int(r["d"]) * 60 + int(r["m"]) for r in T]
    comp = [model[col](n) for n in ns]
    for r, n in zip(T, ns):
        printed[f"p. {pg} {col} {n}"] = f"{r['d']}° {r['m']}′"
        if int(r["n2"]) == 360 - n:
            identities[0] += 1
        else:
            found.append((f"p. {pg} {col} {n} 360-n", r["n2"], str(360 - n)))
    tol, lst = (TOL, LIST) if col != "portio" else (12, 12)
    if col == "portio":
        by_n = dict(zip(ns, vals))
        for n, v in zip(ns, vals):
            ok = v % 12 == 0 and (180 - n not in by_n or by_n[180 - n] == v)
            identities[1] += ok
            if not ok:
                found.append((f"p. {pg} portio {n} (12′, symmetry)", dm(v), f"at {180 - n}°: {dm(by_n.get(180 - n, 0))}"))
    dev = [v - c for v, c in zip(vals, comp)]
    stats[col] = (max(abs(x) for x in dev), max(range(len(dev)), key=lambda k: abs(dev[k])))
    runs = []
    k = 0
    while k < len(T):
        w = f"p. {pg} {col} {ns[k]}"
        if abs(dev[k]) > tol and w not in NOTED:
            j = k
            while j + 1 < len(T) and abs(dev[j + 1]) > tol and (dev[j + 1] > 0) == (dev[k] > 0) \
                    and f"p. {pg} {col} {ns[j + 1]}" not in NOTED:
                j += 1
            worst = max(range(k, j + 1), key=lambda q: abs(dev[q]))
            if abs(dev[worst]) > lst:
                runs.append((ns[k], ns[j]))
                found.append((f"p. {pg} {col} {ns[k]}" + (f"-{ns[j]}" if j > k else ""),
                              ", ".join(dm(vals[q]) for q in range(k, j + 1)),
                              f"computed {', '.join(dm(comp[q]) for q in range(k, j + 1))}"))
            else:
                agree[0] += j - k + 1
            k = j + 1
        else:
            agree[0] += 1
            k += 1
    if col == "portio":
        continue
    for k in range(1, len(T) - 1):
        p = vals[k] - (vals[k - 1] + vals[k + 1]) / 2
        q = comp[k] - (comp[k - 1] + comp[k + 1]) / 2
        w = f"p. {pg} {col} {ns[k]}"
        if abs(p - q) >= SPIKE and w not in NOTED and not any(a - 6 <= ns[k] <= b + 6 for a, b in runs):
            found.append((w + " (neighbours)", dm(vals[k]),
                          f"the neighbours {dm(vals[k - 1])} and {dm(vals[k + 1])}; computed {dm(comp[k - 1])}, "
                          f"{dm(comp[k])}, {dm(comp[k + 1])}"))


def main():
    rows = read("latitudes_discrepancies.tsv")
    ledger = {r["where"] for r in rows if r["kind"] != "noted"}
    noted = {r["where"]: r for r in rows if r["kind"] == "noted"}
    problems = [f"no ledger entry for Nallino's note: {w} (printed {printed.get(w)})" for w in NOTED if w not in noted]
    problems += [f"{w}: the ledger says printed {noted[w]['printed']}, the table has {printed.get(w)}"
                 for w in NOTED if w in noted and noted[w]["printed"] != printed.get(w)]
    open_ = [f for f in found if f[0] not in ledger]
    n = len(R)
    print(f"360 - n {identities[0]} of {n}; portions multiples of 12′ and symmetric {identities[1]} of 30; values within "
          f"tolerance {agree[0]}, differ {len(found)} (ledgered {len(found) - len(open_)}, open {len(open_)}); "
          f"Nallino's notes {len(NOTED)}, problems {len(problems)}")
    if "--stats" in sys.argv:
        for key, d in extra.items():
            print(f"  {key}: distance{'s at the limits' if len(d) == 2 else ' at the node'} "
                  + ", ".join(f"{x:.2f}" for x in d))
        for col, (mx, k) in stats.items():
            print(f"  {NAMES[col]}: largest departure {mx:.1f}′ at {6 * (k + 1)}°")
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

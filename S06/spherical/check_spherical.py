"""Check of Nallino's Part II pp. 55-60.
  sines (pp. 55-56)        the supplement is 180° - arc; the sine is 60 sin(arc) in parts, minutes and seconds
  declination (pp. 57-58)  sin δ = sin λ sin ε with ε = 23° 35′ (al-Battānī's obliquity); the four arcs of equal
                           declination are λ, 180° - λ, 180° + λ and 360° - λ
  right ascensions (p. 58) tan α = cos ε tan λ for λ = 10° ... 90°, and the «sinus ascensionum» 60 sin α
  longest day (p. 59)      half the increase of the longest day, arcsin(tan φ tan ε), for φ = 0° 30′ ... 60°;
                           consecutive values beyond the tolerance are reported as one run
  shadows (p. 60)          the shadow of a gnomon of 12 digits, 12 cot h, for h = 1° ... 90°
A value off by more than 3 units of its last place must be in
spherical_discrepancies.tsv. --list shows the ledgered differences too; --dist shows how far the values lie from the
computation. Exit code 1 on anything open."""
import csv, math, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EPS = math.radians(23 + 35 / 60)
TOL = 3


def read(name):
    return list(csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t"))


def sec(*v):
    x = 0
    for a in v:
        x = x * 60 + int(a)
    return x


def dms(x):
    x = round(x)
    return f"{x // 3600}° {x // 60 % 60}′ {x % 60}″"


ledger = {r["where"] for r in read("spherical_discrepancies.tsv")}
found, dist = [], {"sines": Counter(), "declination": Counter(), "right ascension": Counter()}


def compare(where, printed, exp, table, tol=TOL, shown=None):
    dev = printed - exp
    dist[table][round(abs(dev))] += 1
    if abs(dev) > tol:
        found.append((where, shown or dms(printed), f"{dev:+.1f}″ from the computation ({dms(exp)})"))


sines = read("sines_p2.tsv")
for r in sines:
    th = int(r["arc_d"]) + int(r["arc_m"]) / 60
    w = f"p. {r['ppage']} sine {r['arc_d']}° {r['arc_m']}′"
    if sec(r["supp_d"], r["supp_m"]) != round((180 - th) * 60):
        found.append((w + " supplement", f"{r['supp_d']}° {r['supp_m']}′", f"180° - arc = {dms((180 - th) * 3600)}"))
    p = sec(r["sin_p"], r["sin_m"], r["sin_s"])
    compare(w, p, 60 * math.sin(math.radians(th)) * 3600, "sines", shown=f"{r['sin_p']}p {r['sin_m']}′ {r['sin_s']}″")

for r in read("decl_p2.tsv"):
    lam = int(r["lam"])
    w = f"p. {r['ppage']} declination {lam}°"
    exp = math.degrees(math.asin(math.sin(math.radians(lam)) * math.sin(EPS))) * 3600
    compare(w, sec(r["decl_d"], r["decl_m"], r["decl_s"]), exp, "declination")
    for k, e in zip("abcd", (lam, 180 - lam, 180 + lam, 360 - lam)):
        if int(r["arc_" + k]) != e:
            found.append((f"{w} arc {k}", r["arc_" + k], f"{e}"))

for r in read("ra10_p2.tsv"):
    lam = int(r["decade"])
    w = f"p. 58 right ascension {lam}°"
    exp = 90 * 3600 if lam == 90 else math.degrees(math.atan(math.cos(EPS) * math.tan(math.radians(lam)))) * 3600
    a = sec(r["ra_d"], r["ra_m"], r["ra_s"])
    compare(w, a, exp, "right ascension")
    s = sec(r["sin_p"], r["sin_m"], r["sin_s"])
    compare(w + " sine", s, 60 * math.sin(math.radians(exp / 3600)) * 3600, "right ascension",
            shown=f"{r['sin_p']}p {r['sin_m']}′ {r['sin_s']}″")

# p. 59: half the increase of the longest day, arcsin(tan φ tan ε), in minutes; consecutive deviations form one run
dist["longest day"] = Counter(); dist["shadows"] = Counter()
run = []


def close_run():
    if run:
        a, b = run[0], run[-1]
        worst = max(run, key=lambda x: abs(x[2]))
        found.append((f"p. 59 latitudes {a[0]}-{b[0]}", ", ".join(x[1] for x in run),
                      f"{len(run)} values {'above' if worst[2] > 0 else 'below'} the computation, the largest by {worst[2]:+.1f}′ at {worst[0]}"))
        run.clear()


for r in read("days59_p2.tsv"):
    phi = int(r["phi_d"]) + int(r["phi_m"]) / 60
    exp = math.degrees(math.asin(math.tan(math.radians(phi)) * math.tan(EPS))) * 60
    dev = sec(r["inc_d"], r["inc_m"]) - exp
    dist["longest day"][round(abs(dev))] += 1
    if abs(dev) > TOL:
        run.append((f"{r['phi_d']}° {r['phi_m']}′", f"{r['inc_d']}° {r['inc_m']}′", dev))
    else:
        close_run()
close_run()

# p. 60: the shadow of a gnomon of 12 digits, 12 cot h, in digits and minutes
for r in read("shadows60_p2.tsv"):
    h = int(r["alt"])
    exp = 0.0 if h == 90 else 12 / math.tan(math.radians(h)) * 60
    dev = sec(r["dig"], r["min"]) - exp
    dist["shadows"][round(abs(dev))] += 1
    if abs(dev) > TOL:
        found.append((f"p. 60 shadow {h}°", f"{r['dig']} dig. {r['min']}′", f"{dev:+.1f}′ from 12 cot h"))

# pp. 61-64: right ascension from the beginning of Capricorn, and the equation of days with their nights, computed
# from al-Battani's elements (solar apogee 82° 17′, greatest equation of the Sun 1° 59′ 10″): mean longitude minus
# right ascension of the true longitude, less its least value in the year; the table's zero point is fitted (median)
APOGEE, ECC = 82 + 17 / 60, math.sin(math.radians(1 + 59 / 60 + 10 / 3600))


def ra_deg(lam):
    l = math.radians(lam)
    return math.degrees(math.atan2(math.cos(EPS) * math.sin(l), math.cos(l))) % 360


def mean_long(lam):
    v = math.radians(lam - APOGEE); m = v
    for _ in range(20):
        m = v + math.atan2(ECC * math.sin(m), 1 + ECC * math.cos(m))
    return (APOGEE + math.degrees(m)) % 360


def eq_raw(lam):
    return ((mean_long(lam) - ra_deg(lam)) + 180) % 360 - 180


EQMIN = min(eq_raw(x / 10) for x in range(3600))
TOL_EQ = 4      # the reconstruction of the equation agrees with the table to 3′ for 310 of the 360 values;
                # a stretch of values more than 3′ off is listed when one of them is more than 4′ off
raeq = read("raeq_p2.tsv")
dist["ascensions"] = Counter(); dist["equation"] = Counter()
for r in raeq:
    lam = int(r["lam"])
    exp = ((ra_deg(lam) - 270) % 360) * 60
    got = sec(r["asc_d"], r["asc_m"]) % 21600
    dev = (got - exp + 10800) % 21600 - 10800
    dist["ascensions"][round(abs(dev))] += 1
    if abs(dev) > TOL:
        found.append((f"p. {r['ppage']} ascension {r['sign']} {r['row']}", f"{r['asc_d']}° {r['asc_m']}′",
                      f"{dev:+.1f}′ from the computation"))
dev_eq = {int(r["lam"]): sec(r["eq_d"], r["eq_m"]) - (eq_raw(int(r["lam"])) - EQMIN) * 60 for r in raeq}
ZERO = sorted(dev_eq.values())[len(dev_eq) // 2]          # the table's zero point against the computation
by_lam = {int(r["lam"]): r for r in raeq}
order = list(range(271, 361)) + list(range(1, 271))      # the year as the pages run, from Capricorn 1°
run = []


def close_eq_run():
    """a stretch of consecutive values more than 3′ off, reported when its largest deviation exceeds 4′"""
    if run and max(abs(x[1]) for x in run) <= TOL_EQ:
        run.clear()
    if run:
        a, b = by_lam[run[0][0]], by_lam[run[-1][0]]
        worst = max(run, key=lambda x: abs(x[1]))
        w = by_lam[worst[0]]
        pages_ = a["ppage"] + ("" if b["ppage"] == a["ppage"] else "-" + b["ppage"])
        span = (f"{a['sign']} {a['row']}-{b['row']}" if b["sign"] == a["sign"] else f"{a['sign']} {a['row']} - {b['sign']} {b['row']}")
        found.append((f"p. {pages_} equation {span}",
                      ", ".join(f"{by_lam[l]['eq_d']}° {by_lam[l]['eq_m']}′" for l, _ in run),
                      f"{len(run)} values {'above' if worst[1] > 0 else 'below'} the computation, the largest by "
                      f"{worst[1]:+.1f}′ at {w['sign']} {w['row']}"))
        run.clear()


for lam in order:
    d = dev_eq[lam] - ZERO
    dist["equation"][round(abs(d))] += 1
    if abs(d) > TOL and (not run or (d > 0) == (run[-1][1] > 0)):
        run.append((lam, d))
    elif abs(d) > TOL:
        close_eq_run(); run.append((lam, d))
    else:
        close_eq_run()
close_eq_run()

open_ = [f for f in found if f[0] not in ledger]
n = sum(sum(c.values()) for c in dist.values())
print(f"values compared {n}, differ {len(found)} (ledgered {len(found) - len(open_)}, open {len(open_)})")
for where, p, e in (found if "--list" in sys.argv else open_):
    print(f"  {where}: {p}; {e}" + ("" if where in ledger else "   << not in the ledger"))
if "--dist" in sys.argv:
    within = sum(abs(v - ZERO) <= 3 for v in dev_eq.values())
    print(f"  equation: zero point {ZERO:+.2f}′; within 3′ of the computation {within} of {len(dev_eq)}")
    for t, c in dist.items():
        u = "′" if t in ("longest day", "shadows", "ascensions", "equation") else "″"
        print(f"  {t}: " + ", ".join(f"{k}{u}: {v}" for k, v in sorted(c.items())))
stale = [w for w in ledger if w not in {f[0] for f in found}]
for w in stale:
    print("  ledger entry without a difference:", w)
sys.exit(1 if open_ or stale else 0)

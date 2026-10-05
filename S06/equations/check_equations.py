"""Check of Nallino's Part II pp. 78-83, for every degree n = 1 ... 180 (and 360 - n), against al-Battani's elements
(Nallino, Part II pp. 223-227):
  Sun        tan q = e sin n / (1 + e cos n), e = 2;4,45 / 60
  Moon       tan q = r sin n / (1 + r cos n), r = 5;15 / 60 (the simple equation)
  latitude   sin b = sin n sin 5
  prosneusis tan p = e' sin n / (rho + e' cos n), e' = 10;19 / 60, rho = e' cos n + sqrt((1 - e')^2 - e'^2 sin^2 n)
  minutes    60 (asin(r / rho) - asin(r)) / (asin(r / (1 - 2 e')) - asin(r)), to the nearest minute
  increment  the equation at the perigee of the eccentre (distance 1 - 2 e') less the equation at the apogee
The Sun, the Moon and the latitude agree with the computation within 3″ for most values (al-Battani's own computation
departs by up to 3″, «perraro» more, as Nallino says): consecutive values more than 3″ off in the same direction form one
entry, listed when one of them is more than 5″ off. The minutes lie within 1.5 of the computation, because al-Battani
dropped the seconds of Ptolemy's column (Nallino). The prosneusis and the increment, which al-Battani took
from Ptolemy and interpolated, are compared with the computation the same way, and in addition every value whose
second difference with its neighbours reaches 3′ is listed (a break in the run of the table). The arguments must be n
and 360 - n. The three cells that Nallino emends on p. 79 need ledger entries of kind «noted» that state the printed
values. --list shows the ledgered entries too, --dist the distribution of the deviations. Exit code 1 on anything open."""
import csv, math, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
E_SUN = (2 + 4 / 60 + 45 / 3600) / 60
R_MOON = 5.25 / 60
E_MOON = (10 + 19 / 60) / 60
NOTED = ["p. 79 moon 35", "p. 79 moon 36", "p. 79 moon 37"]


def read(name):
    return list(csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t"))


def eq(n, e, dist=1.0):
    m = math.radians(n)
    return math.degrees(math.atan2(e * math.sin(m), dist + e * math.cos(m)))


def rho(n):
    m = math.radians(n)
    return E_MOON * math.cos(m) + math.sqrt((1 - E_MOON) ** 2 - (E_MOON * math.sin(m)) ** 2)


def prosneusis(n):
    m = math.radians(n)
    return math.degrees(math.atan2(E_MOON * math.sin(m), rho(n) + E_MOON * math.cos(m)))


def minutes(n):
    a = math.asin(R_MOON); p = math.asin(R_MOON / (1 - 2 * E_MOON))
    return 60 * (math.asin(R_MOON / rho(n)) - a) / (p - a)


def increment(n):
    rp = R_MOON / (1 - 2 * E_MOON)
    return eq(n, rp) - eq(n, R_MOON)


def latitude(n):
    return math.degrees(math.asin(math.sin(math.radians(n)) * math.sin(math.radians(5))))


def units(r, k, places):
    v = 0
    for x in ([r[k + "_d"], r[k + "_m"], r[k + "_s"]] if places == 3 else [r[k + "_d"], r[k + "_m"]] if places == 2 else [r[k]]):
        v = v * 60 + int(x)
    return v


def show(r, k, places):
    if places == 3:
        return f"{r[k + '_d']}° {r[k + '_m']}′ {r[k + '_s']}″"
    if places == 2:
        return f"{r[k + '_d']}° {r[k + '_m']}′"
    return r[k]


def fmt(x, places):
    if places == 3:
        return f"{int(x // 3600)}° {int(x // 60 % 60)}′ {x % 60:.1f}″"
    if places == 2:
        return f"{int(x // 60)}° {x % 60:.1f}′"
    return f"{x:.1f}"


rows = sorted(read("equations_p2.tsv"), key=lambda r: int(r["n"]))
ledger_rows = read("equations_discrepancies.tsv")
ledger = {r["where"] for r in ledger_rows if r["kind"] != "noted"}
noted = {r["where"]: r for r in ledger_rows if r["kind"] == "noted"}
found, problems, dist = [], [], {}
for i, r in enumerate(rows):
    if int(r["n"]) != i + 1 or int(r["n_inv"]) != 359 - i:
        problems.append(f"argument of row {i + 1}: {r['n']} / {r['n_inv']}")

# (column, places, computation, tolerance, threshold for listing a stretch, unit)
COLS = [("sun", 3, lambda n: eq(n, E_SUN) * 3600, 3, 5, "″"), ("moon", 3, lambda n: eq(n, R_MOON) * 3600, 3, 5, "″"),
        ("lat", 3, lambda n: latitude(n) * 3600, 3, 5, "″"), ("min", 1, minutes, 1.5, 1.5, ""),
        ("pro", 2, lambda n: prosneusis(n) * 60, 3, 3, "′"), ("inc", 2, lambda n: increment(n) * 60, 3, 3, "′")]
cells = {}
for key, places, f, tol, show_tol, unit in COLS:
    dist[key] = Counter(); run = []

    def close():
        if run and max(abs(x[2]) for x in run) <= show_tol:
            run.clear()
        if run:
            a, b = run[0][0], run[-1][0]
            worst = max(run, key=lambda x: abs(x[2]))
            ra_, rb_ = rows[a - 1], rows[b - 1]
            pages = ra_["ppage"] + ("" if rb_["ppage"] == ra_["ppage"] else "-" + rb_["ppage"])
            found.append((f"p. {pages} {key} {a}" + (f"-{b}" if b != a else ""), ", ".join(x[1] for x in run),
                          f"{len(run)} value{'s' if len(run) > 1 else ''} {'above' if worst[2] > 0 else 'below'} the "
                          f"computation, the largest by {worst[2]:+.1f}{unit} at {worst[0]}"))
            run.clear()
    for r in rows:
        n = int(r["n"])
        dev = units(r, key, places) - f(n)
        dist[key][round(abs(dev))] += 1
        where = f"p. {r['ppage']} {key} {n}"
        cells[where] = show(r, key, places)
        if where in NOTED:                   # Nallino's own emendations are checked separately
            close()
            continue
        if abs(dev) > tol and (not run or (dev > 0) == (run[-1][2] > 0)):
            run.append((n, show(r, key, places), dev))
            continue
        close()
        if abs(dev) > tol:
            run.append((n, show(r, key, places), dev))
    close()

# breaks in the run of the two columns taken from Ptolemy: second differences of 3′ or more
for key in ("pro", "inc"):
    v = [units(r, key, 2) for r in rows]
    for i in range(1, len(v) - 1):
        d2 = v[i - 1] - 2 * v[i] + v[i + 1]
        if abs(d2) >= 3:
            r = rows[i]
            found.append((f"p. {r['ppage']} {key} {r['n']} break", show(r, key, 2),
                          f"second difference {d2:+d}′ ({show(rows[i - 1], key, 2)}, {show(r, key, 2)}, {show(rows[i + 1], key, 2)})"))

for w in NOTED:
    if w not in noted:
        problems.append(f"no ledger entry for the cell Nallino emends: {w} (printed {cells.get(w)})")
    elif noted[w]["printed"] != cells.get(w):
        problems.append(f"{w}: the ledger says printed {noted[w]['printed']}, the table has {cells.get(w)}")
for w in noted:
    if w not in NOTED:
        problems.append(f"ledger entry of kind «noted» not among Nallino's emendations: {w}")

open_ = [x for x in found if x[0] not in ledger]
n_vals = sum(sum(c.values()) for c in dist.values())
print(f"values compared {n_vals}, differ {len(found)} (ledgered {len(found) - len(open_)}, open {len(open_)}); "
      f"Nallino's emendations {len(NOTED)}, problems {len(problems)}")
for where, p, e in (found if "--list" in sys.argv else open_):
    print(f"  {where}: {p}; {e}" + ("" if where in ledger else "   << not in the ledger"))
for p in problems:
    print("  " + p)
if "--dist" in sys.argv:
    for key, places, f, tol, show_tol, unit in COLS:
        u = unit or " min"
        print(f"  {key}: " + ", ".join(f"{k}{u}: {v}" for k, v in sorted(dist[key].items())))
stale = [w for w in ledger if w not in {x[0] for x in found}]
for w in stale:
    print("  ledger entry without a difference:", w)
sys.exit(1 if open_ or stale or problems else 0)

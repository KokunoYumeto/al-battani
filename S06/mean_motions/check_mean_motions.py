"""Check of Nallino's Part II pp. 19-28 and 72-77, 102-107 (mean motions in the Arab and in the Roman calendar; p. 107
the motion of the fixed stars, fs_p2.tsv, against one degree in 66 Roman years).
pp. 19-23 (mm_p2.tsv): the Sun, the Moon, the lunar anomaly and the node, in degrees, minutes and seconds;
pp. 24-28 (mm5_p2.tsv): Saturn, Jupiter, Mars, and the anomalies of Venus and Mercury, in degrees and minutes.
Each motion column is a linear function of time: value = a + b * t (mod 360 degrees), with t the number of days
(collected years: 10631 days per 30 years; single years: 354 days, 355 in the leap years 2 5 7 10 13 16 18 21 24 26
29 of the cycle; months: the cumulative 30- and 29-day months, dhu 'l-hijjah 354, or 355 in a leap year; days;
hours / 24). The script fits each column by least squares on the rows near its line and lists every value that lies
off its line by more than 3 units of the last place (the accumulated rounding of the tables reaches about 2); each
must be in mm_discrepancies.tsv. It also checks the arguments, the cross-table identities (dhu 'l-hijjah = 1 single
year; 24 hours = 1 day), and that every cell Nallino emends in his notes (Part II, p. 204) is printed as its ledger
entry states. --list shows the ledgered differences too; --resid shows the largest deviation within the tolerance in
each column. Exit code 1 on anything open."""
import csv, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
LEAP = {2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29}
MONTHS = [30, 59, 89, 118, 148, 177, 207, 236, 266, 295, 325, 354, 355]
SETS = [                                    # starting rates in degrees per day; the fit refines them
    {"file": "mm_p2.tsv", "places": 3, "groups": ["sun", "moon", "anom", "node"],
     "rate": {"sun": 0.9856518, "moon": 13.1763987, "anom": 13.0649829, "node": 0.0529509}},
    {"file": "mm5_p2.tsv", "places": 2, "groups": ["sat", "jup", "mars", "ven", "mer"],
     "rate": {"sat": 0.0334995, "jup": 0.0831342, "mars": 0.5240743, "ven": 0.6165256, "mer": 3.1067021}},
    {"file": "mmr_p2.tsv", "places": 3, "groups": ["sun", "moon", "anom", "node"], "calendar": "roman",
     "rate": {"sun": 0.9856518, "moon": 13.1763987, "anom": 13.0649829, "node": 0.0529509},
     "intervals": [20, 40, 60, 80, 100, 200, 300, 400, 500, 600]},
    {"file": "mm5r_p2.tsv", "places": 2, "groups": ["sat", "jup", "mars", "ven", "mer"], "calendar": "roman",
     "rate": {"sat": 0.0334995, "jup": 0.0831342, "mars": 0.5240743, "ven": 0.6165256, "mer": 3.1067021},
     "intervals": [40, 60, 80, 100, 200, 400, 600]},
]
ROMAN_MONTHS = [31, 61, 92, 122, 153, 184, 214, 245, 275, 306, 337, 365, 366]
INTERVALS = [20, 40, 60, 80, 100, 200, 300, 400, 500, 600]
TOL = 3                                     # units of the last place
# the cells Nallino emends in his notes to pp. 22-23 (Part II, p. 204): each needs a ledger entry of kind «noted»
NOTED = ["p. 22 days 10 sun", "p. 22 days 21 node", "p. 23 hours 3 sun", "p. 23 hours 23 anom"]


def read(name):
    return list(csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t"))


def units(r, g, places):
    v = int(r[g + "_d"]) * 60 + int(r[g + "_m"])
    return v * 60 + int(r[g + "_s"]) if places == 3 else v


def show(r, g, places):
    s = f"{r[g + '_d']}° {r[g + '_m']}′"
    return s + f" {r[g + '_s']}″" if places == 3 else s


def show_units(x, places):
    if places == 3:
        return f"{int(x // 3600)}° {int(x // 60 % 60)}′ {x % 60:.1f}″"
    return f"{int(x // 60)}° {x % 60:.1f}′"


def tdays(table, i, cal="arab", intervals=INTERVALS):
    if cal == "roman":                       # Julian years: 365 days, 366 in every fourth; 7305 days in 20 years
        return {"collected": lambda: 7305 * i, "single": lambda: 365 * (i + 1) + (i + 1) // 4,
                "months": lambda: ROMAN_MONTHS[i], "days": lambda: i + 1, "hours": lambda: (i + 1) / 24,
                "intervals": lambda: 365.25 * intervals[i]}[table]()
    if table == "collected":
        return 10631 * i
    if table == "single":
        return sum(355 if n in LEAP else 354 for n in range(1, i + 2))
    if table == "months":
        return MONTHS[i]
    if table == "days":
        return i + 1
    if table == "hours":
        return (i + 1) / 24


def fit(u, t, b, MOD):
    """Line a + b t through the values u (mod MOD): start from the given rate and the median intercept, then refit
    by least squares on the points within a band that narrows to the tolerance."""
    unwrapped = u[0] + ((u - u[0] - b * (t - t[0]) + MOD / 2) % MOD - MOD / 2) + b * (t - t[0])
    a = np.median(unwrapped - b * t)
    for band in (MOD / 8, 600, 120, 30, 10, TOL, TOL, TOL):
        unwrapped = u + MOD * np.round(((a + b * t) - u) / MOD)
        keep = np.abs(unwrapped - (a + b * t)) <= band
        if keep.sum() >= 3:
            b, a = np.polyfit(t[keep], unwrapped[keep], 1)
    unwrapped = u + MOD * np.round(((a + b * t) - u) / MOD)
    return a, b, unwrapped - (a + b * t)


ledger = read("mm_discrepancies.tsv")
ledger_keys = {r["where"] for r in ledger if r["kind"] != "noted"}
found, agree, worst, problems, cells = [], 0, {}, [], {}
for S in SETS:
    rows = read(S["file"]); P = S["places"]; unit = "″" if P == 3 else "′"
    MOD = 360 * 60 ** (P - 1)
    cal = S.get("calendar", "arab")
    for table in ("collected", "single", "months", "days", "hours") + (("intervals",) if cal == "roman" else ()):
        T = [r for r in rows if r["table"] == table]
        t = np.array([tdays(table, i, cal, S.get("intervals", INTERVALS)) for i in range(len(T))], float)
        first, step = (931, 20) if cal == "roman" else (1, 30)
        exp_args = {"collected": [str(first + step * i) for i in range(len(T))], "single": [str(i + 1) for i in range(len(T))],
                    "days": [str(i + 1) for i in range(len(T))], "hours": [str(i + 1) for i in range(len(T))],
                    "intervals": [str(n) for n in S.get("intervals", INTERVALS)]}.get(table)
        if exp_args and [r["arg"] for r in T] != exp_args:
            found.append((f"{S['file']} {table} arguments", "", ""))
        for g in S["groups"]:
            u = np.array([units(r, g, P) for r in T], float)
            a, b, res = fit(u, t, S["rate"][g] * 60 ** (P - 1), MOD)
            ok = np.abs(res) <= TOL
            worst[f"p. {T[0]['ppage']} {table} {g}"] = float(np.abs(res[ok]).max())
            for i, r in enumerate(T):
                where = f"p. {r['ppage']} {table} {r['arg']} {g}"
                line = (a + b * t[i]) % MOD
                cells[where] = (show(r, g, P), show_units(line, P))
                if abs(res[i]) > TOL:
                    found.append((where, show(r, g, P), f"{res[i]:+.1f}{unit} from the line ({show_units(line, P)})"))
                else:
                    agree += 1
    # cross-table identities
    one_year = [r for r in rows if r["table"] == "single"][0]
    comm = [r for r in rows if r["table"] == "months"][11]
    day1 = [r for r in rows if r["table"] == "days"][0]
    h24 = [r for r in rows if r["table"] == "hours"][23]
    month = "subat comm." if cal == "roman" else "dhu 'l-hijjah" + (" comm." if P == 3 else "")
    for g in S["groups"]:
        if units(one_year, g, P) != units(comm, g, P):
            found.append((f"identity single year 1 = {month} ({g})",
                          f"{show(comm, g, P)} (p. {comm['ppage']})", f"{show(one_year, g, P)} (p. {one_year['ppage']})"))
        if units(day1, g, P) != units(h24, g, P):
            found.append((f"identity day 1 = hour 24{' (Roman)' if cal == 'roman' else ''} ({g})", show(h24, g, P), show(day1, g, P)))
    if cal == "roman" and S["intervals"][0] == 20:            # 20 single years = the interval of 20 years
        y20 = [r for r in rows if r["table"] == "single"][19]
        i20 = [r for r in rows if r["table"] == "intervals"][0]
        for g in S["groups"]:
            if units(y20, g, P) != units(i20, g, P):
                found.append((f"identity single year 20 = interval 20 ({g})", show(i20, g, P), show(y20, g, P)))

# the days and hours of the Roman calendar (pp. 75-76) are the same motions as those of pp. 22-23
arab = read("mm_p2.tsv"); roman = read("mmr_p2.tsv")
for table in ("days", "hours"):
    A = [r for r in arab if r["table"] == table]; R = [r for r in roman if r["table"] == table]
    for ra_, rr in zip(A, R):
        for g in ("sun", "moon", "anom", "node"):
            if units(ra_, g, 3) != units(rr, g, 3):
                found.append((f"identity p. {rr['ppage']} {table} {rr['arg']} {g} = p. {ra_['ppage']}", show(rr, g, 3),
                              f"{show(ra_, g, 3)} on p. {ra_['ppage']}"))

# p. 103: the motions in 20 years printed under the single years, to the thirds, against the single year 20 (rounded
# to the minute) and against the step of the collected years of p. 102
def sexa(v):
    whole, frac = v.split(";")
    x = float(whole)
    for j, d in enumerate(frac.split(",")):
        x += int(d) / 60 ** (j + 1)
    return x


line20 = {r["item"]: r for r in read("mm5r_extra.tsv")}["years20"]
planets = read("mm5r_p2.tsv")
y20 = [r for r in planets if r["table"] == "single"][19]
coll = [r for r in planets if r["table"] == "collected"]
for g in ("sat", "jup", "mars", "ven", "mer"):
    v = sexa(line20[g]) * 60                               # minutes of arc
    if round(v) % 21600 != units(y20, g, 2):
        found.append((f"identity p. 103 line of 20 years = year 20 ({g})", show(y20, g, 2), f"{line20[g]} under the table"))
    steps = [(units(b, g, 2) - units(a, g, 2)) % 21600 for a, b in zip(coll, coll[1:])]
    near = sum(1 for st in steps if abs(((st - v + 10800) % 21600) - 10800) <= 1)
    if near < len(steps) - 2:
        found.append((f"identity p. 103 line of 20 years = step of p. 102 ({g})", line20[g],
                       f"{near} of {len(steps)} steps of p. 102 within 1′"))

# pp. 105-106 (hours, days in the Roman calendar) are the same motions as pp. 28-27
arab5 = read("mm5_p2.tsv")
for table in ("days", "hours"):
    A = [r for r in arab5 if r["table"] == table]; R = [r for r in planets if r["table"] == table]
    for ra_, rr in zip(A, R):
        for g in ("sat", "jup", "mars", "ven", "mer"):
            if units(ra_, g, 2) != units(rr, g, 2):
                found.append((f"identity p. {rr['ppage']} {table} {rr['arg']} {g} = p. {ra_['ppage']}", show(rr, g, 2),
                              f"{show(ra_, g, 2)} on p. {ra_['ppage']}"))

# p. 107, the motion of the fixed stars: one degree in 66 years (al-Battani's precession; Nallino, Part II p. 293), the
# Roman year of 365 1/4 days; each value within one unit of its last place (three for thirds)
FS_RATE = 3600 / 66                                       # seconds of arc per Roman year
for r in read("fs_p2.tsv"):
    years = {"collected": lambda: int(r["arg"]), "single": lambda: int(r["arg"]),
             "months": lambda: int(r["days"]) / 365.25, "days": lambda: int(r["arg"]) / 365.25}[r["table"]]()
    exact = years * FS_RATE                               # seconds
    places = [p for p in ("d", "m", "s", "t") if r[p] != ""]
    scale = {"d": 3600, "m": 60, "s": 1, "t": 1 / 60}     # seconds per unit of each place
    unit = scale[places[-1]]                              # the last printed place
    dev = (sum(int(r[p]) * scale[p] for p in places) - exact) / unit
    tol = 3 if places[-1] == "t" else 1
    where = f"p. 107 fixed stars {r['table']} {r['arg'].split()[0]}"
    if abs(dev) > tol:
        shown = " ".join(r[p] + {"d": "°", "m": "′", "s": "″", "t": "‴"}[p] for p in places)
        found.append((where, shown, f"{exact // 60:.0f}′ {exact % 60:.2f}″ at one degree in 66 years ({dev:+.1f} units)"))
    else:
        agree += 1

# the cells Nallino emends: the ledger entry must exist and give the value printed in the table
noted = {r["where"]: r for r in ledger if r["kind"] == "noted"}
for w in NOTED:
    if w not in noted:
        problems.append(f"no ledger entry for the cell Nallino emends: {w} (printed {cells[w][0]}, line {cells[w][1]})")
    elif noted[w]["printed"] != cells[w][0]:
        problems.append(f"{w}: the ledger says printed {noted[w]['printed']}, the table has {cells[w][0]}")
for w in noted:
    if w not in NOTED:
        problems.append(f"ledger entry of kind «noted» not among Nallino's emendations: {w}")

open_ = [f for f in found if f[0] not in ledger_keys]
print(f"values on their lines {agree}, differ {len(found)} (ledgered {len(found) - len(open_)}, open {len(open_)}); "
      f"cells Nallino emends {len(NOTED)}, problems {len(problems)}")
for where, p, e in (found if "--list" in sys.argv else open_):
    print(f"  {where}: {p} {e}" + ("" if where in ledger_keys else "   << not in the ledger"))
if "--list" in sys.argv:
    for w in NOTED:
        print(f"  Nallino emends {w}: printed {cells[w][0]}, line {cells[w][1]}")
for p in problems:
    print("  " + p)
if "--resid" in sys.argv:
    for col, w in worst.items():
        print(f"  largest deviation within the tolerance, {col}: {w:.2f}")
stale = [w for w in ledger_keys if w not in {f[0] for f in found}]
for w in stale:
    print("  ledger entry without a difference:", w)
sys.exit(1 if open_ or stale or problems else 0)

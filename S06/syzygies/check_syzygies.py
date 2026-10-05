"""Check of Nallino's Part II pp. 29-32 (mean syzygies in Egyptian years).
Every number is in three sexagesimal places (days ; ′ ″, or ′ ″ ‴ in the table of intervals; degrees ′ ″) and is
compared in units of its last place:
  pp. 29-30  collected years 915, 940 ... 1690: each column is a line a + b k in the period number k (25 Egyptian
             years each); and each row of p. 29 minus the row of p. 30 is the half lunation of p. 31 («Monsis
             dimidium»): 14;45,55 days, 14° 33′ 12″, 192° 54′ 30″, 195° 20′ 7″.
  p. 31      1-12 lunations: each column is n times the motion in one lunation; the parts of a month are 1/6, 1/4,
             1/3 and 1/2 of that motion (whole revolutions included); the intervals of 50 ... 600 years are N/25
             times the period of 25 years printed under p. 32 (and 0;2,47,5 days, by which 9125 days exceed 309
             lunations).
  p. 32      single years 1-24: year n holds k = ceil(365 n / L) lunations; each motion is a line in k, and the day
             is k L - 365 n (a line in k modulo 365 days).
  25 years   the line under p. 32 against the steps of p. 29 and against 309 lunations of 29;31,50,8,20 days.
A value off its line by more than 3 units of its last place must be in syz_discrepancies.tsv; the cells Nallino
emends in his notes (Part II pp. 206-209) need entries of kind «noted» that state the printed value. --list shows the
ledgered differences too. Exit code 1 on anything open."""
import csv, math, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
G = ["day", "lum", "anom", "lat"]
TOL = 3
DEG = 360 * 3600
L = 29 + 31 / 60 + 50 / 3600 + 8 / 216000 + 20 / 12960000          # days in a mean lunation (29;31,50,8,20)
NOTED = ["p. 32 single 6 day", "p. 32 single 11 day", "p. 32 single 14 day", "p. 32 single 19 day",
         "p. 32 eclipse_sun 191° 16′", "p. 32 eclipse_sun 348° 44′"]


def read(name):
    return list(csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t"))


def u(r, g):
    return (int(r[g + "_1"]) * 60 + int(r[g + "_2"])) * 60 + int(r[g + "_3"])


def show(r, g, units="d"):
    a, b, c = r[g + "_1"], r[g + "_2"], r[g + "_3"]
    if g != "day":
        return f"{a}° {b}′ {c}″"
    return f"{a}′ {b}″ {c}‴" if units == "′" else f"{a}ᵈ {b}′ {c}″"


def sexa(x, places=3, first="°"):
    """x in units of the last of `places` places -> «a° b′ c.c″» (or days)."""
    s = x % 60; m = int(x // 60) % 60; d = int(x // 3600)
    return f"{d}{first} {m}′ {s:.1f}″"


def fit(uu, t, b, MOD):
    unwrapped = uu[0] + ((uu - uu[0] - b * (t - t[0]) + MOD / 2) % MOD - MOD / 2) + b * (t - t[0])
    a = np.median(unwrapped - b * t)
    for band in (MOD / 8, 600, 120, 30, 10, TOL, TOL, TOL):
        unwrapped = uu + MOD * np.round(((a + b * t) - uu) / MOD)
        keep = np.abs(unwrapped - (a + b * t)) <= band
        if keep.sum() >= 3:
            b, a = np.polyfit(t[keep], unwrapped[keep], 1)
    unwrapped = uu + MOD * np.round(((a + b * t) - uu) / MOD)
    return a, b, unwrapped - (a + b * t)


def centred(x, MOD):
    return (x + MOD / 2) % MOD - MOD / 2


rows = read("syz_p2.tsv")
T = {t: [r for r in rows if r["table"] == t] for t in ("conj", "opp", "parts", "months", "intervals", "single")}
ledger = read("syz_discrepancies.tsv")
keys = {r["where"] for r in ledger if r["kind"] != "noted"}
found, agree, worst, printed = [], 0, (0.0, ""), {}


def line_check(table, t, rates, mods, label=None):
    """Fit each column of `table` against t; record values off by more than TOL."""
    global agree, worst
    lines = {}
    for g in G:
        uu = np.array([u(r, g) for r in T[table]], float)
        a, b, res = fit(uu, np.array(t, float), rates[g], mods[g])
        lines[g] = (a, b)
        for i, r in enumerate(T[table]):
            where = f"p. {r['ppage']} {table} {r['arg'] if table != 'parts' else i + 1} {g}"
            printed[where] = show(r, g)
            if abs(res[i]) > TOL:
                found.append((where, show(r, g), f"{res[i]:+.1f} units from the line ({sexa((a + b * t[i]) % mods[g])})"))
            else:
                agree += 1; worst = max(worst, (abs(res[i]), where))
    return lines


# pp. 29-30: lines in the period number k
PER = {"day": -(2 * 3600 + 47 * 60 + 5) / 60, "lum": -21504.9, "anom": 206504.0, "lat": 421925.86}   # per 25 years
MODS = {"day": 365 * 3600, "lum": DEG, "anom": DEG, "lat": DEG}
k = list(range(32))
conj = line_check("conj", k, PER, MODS)
line_check("opp", k, PER, MODS)
half = T["parts"][3]                                      # «Monsis dimidium»: half a lunation
for i, (rc, ro) in enumerate(zip(T["conj"], T["opp"])):
    for g in G:
        diff = (u(rc, g) - u(ro, g)) % MODS[g]
        if abs(centred(diff - u(half, g), MODS[g])) > 1 and not any(
                f[0] in (f"p. 29 conj {rc['arg']} {g}", f"p. 30 opp {ro['arg']} {g}") for f in found):
            found.append((f"p. 30 opp {ro['arg']} {g} (p. 29 minus p. 30)", show(ro, g),
                          f"p. 29 minus p. 30 is {sexa(diff)}, half a lunation {show(half, g)}"))

# p. 31: lunations 1-12 (lines through the origin), parts of a month, intervals of years
months = line_check("months", list(range(1, 13)), {"day": L * 3600, "lum": 104784.67, "anom": 92940.0, "lat": 110414.0}, MODS)
full = {}
for g in G:                                               # the motion in one lunation, whole revolutions included
    turns = {"day": 0, "lum": 0, "anom": 1, "lat": 1}[g]
    full[g] = months[g][1] + turns * DEG
for i, (r, f) in enumerate(zip(T["parts"], (1 / 6, 1 / 4, 1 / 3, 1 / 2))):
    for g in G:
        exp = f * full[g]
        where = f"p. 31 parts {i + 1} {g}"
        printed[where] = show(r, g)
        if abs(u(r, g) - exp) > TOL:
            found.append((where, show(r, g), f"{f:.4f} of a lunation gives {sexa(exp)}"))
        else:
            agree += 1; worst = max(worst, (abs(u(r, g) - exp), where))
extra = {r["item"]: r for r in read("syz_extra.tsv")}
p25 = extra["period25"]["value"].split("|")


def sexa_value(s):
    """«354;1,35,6,26» -> degrees (float)."""
    whole, frac = s.split(";")
    v = float(whole)
    for j, x in enumerate(frac.split(",")):
        v += int(x) / 60 ** (j + 1)
    return v


PERIOD = {"day": (9125 - 309 * L) * 216000,                # thirds of a day: 0;2,47,5
          "lum": sexa_value(p25[2]) * 3600, "anom": sexa_value(p25[3]) * 3600, "lat": sexa_value(p25[4]) * 3600}
for r in T["intervals"]:
    n = int(r["arg"]) / 25
    for g in G:
        exp = (n * PERIOD[g]) % (DEG if g != "day" else 10 ** 9)
        where = f"p. 31 intervals {r['arg']} {g}"
        printed[where] = show(r, g, "′")
        err = centred(u(r, g) - exp, DEG)
        if abs(err) > TOL:
            found.append((where, show(r, g, "′"), f"{n:g} periods of 25 years give {sexa(exp, first='′' if g == 'day' else '°')}"))
        else:
            agree += 1; worst = max(worst, (abs(err), where))

# p. 32: lines in the number of lunations
kn = [math.ceil(365 * n / L) for n in range(1, 25)]
single = line_check("single", kn, {"day": L * 3600, "lum": 104784.67, "anom": 92940.0, "lat": 110414.0}, MODS)

# the line for 25 years under p. 32
excess = 309 * L - 9124                                   # 309 lunations beyond 9124 days
day25 = sexa_value(p25[1])
if abs(day25 - excess) * 216000 > 1:
    found.append(("p. 32 period25 day", "0ᵈ 57′ 13″ 5‴ 0ⁱᵛ",
                  "309 lunations of 29;31,50,8,20 days are 9124;57,12,55,0 days"))
for g, j in (("lum", 2), ("anom", 3), ("lat", 4)):
    step = (conj[g][1]) % DEG                             # the fitted step of p. 29 per 25 years
    if abs(centred(sexa_value(p25[j]) * 3600 - step, DEG)) > 1:
        found.append((f"p. 32 period25 {g}", p25[j], f"the step of p. 29 is {sexa(step)}"))

# the eclipse limits: the solar numbers Nallino later emends must be printed as the ledger says
sun = extra["eclipse_sun"]["text"]
for w in ("p. 32 eclipse_sun 191° 16′", "p. 32 eclipse_sun 348° 44′"):
    printed[w] = w.split("eclipse_sun ")[1] if w.split("eclipse_sun ")[1] in sun else "(absent)"

noted = {r["where"]: r for r in ledger if r["kind"] == "noted"}
problems = []
for w in NOTED:
    if w not in noted:
        problems.append(f"no ledger entry for the cell Nallino emends: {w} (printed {printed.get(w)})")
    elif noted[w]["printed"] != printed.get(w):
        problems.append(f"{w}: the ledger says printed {noted[w]['printed']}, the edition has {printed.get(w)}")
for w in noted:
    if w not in NOTED:
        problems.append(f"ledger entry of kind «noted» not among Nallino's emendations: {w}")
noted_cells = {w for w in NOTED if "eclipse" not in w}
found = [f for f in found if f[0] not in noted_cells]     # Nallino's own emendations are checked above

open_ = [f for f in found if f[0] not in keys]
print(f"values on their lines {agree} (largest deviation {worst[0]:.1f} units, {worst[1]}), differ {len(found)} "
      f"(ledgered {len(found) - len(open_)}, open {len(open_)}); Nallino's emendations {len(NOTED)}, problems {len(problems)}")
for where, p, e in (found if "--list" in sys.argv else open_):
    print(f"  {where}: {p}; {e}" + ("" if where in keys else "   << not in the ledger"))
for p in problems:
    print("  " + p)
stale = [w for w in keys if w not in {f[0] for f in found}]
for w in stale:
    print("  ledger entry without a difference:", w)
sys.exit(1 if open_ or stale or problems else 0)

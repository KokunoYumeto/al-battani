"""Check of Nallino's Part II pp. 19-23 (mean motions in Arab years, months, days and hours).
Each motion column is a linear function of time: value = a + b * t (mod 360 degrees), with t the number of days
(collected years: 10631 days per 30 years; single years: 354 days, 355 in the leap years 2 5 7 10 13 16 18 21 24 26
29 of the cycle; months: the cumulative 30- and 29-day months, dhu 'l-hijjah 354 or 355; days; hours / 24).
The script fits each column by least squares on all its rows and lists every value that lies off its
line by more than 3 seconds (accumulated rounding in the tables reaches about 2); each must be in mm_discrepancies.tsv. It also checks the arguments and two cross-table identities
(dhu 'l-hijjah comm. = 1 single year; 24 hours = 1 day). Exit code 1 on anything open."""
import csv, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
LEAP = {2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29}
MOD = 360 * 3600
GROUPS = ["sun", "moon", "anom", "node"]
RATE = {"sun": 0.98564734, "moon": 13.1763964, "anom": 13.0649929, "node": 0.0529539}     # degrees per day


def read(name):
    return list(csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t"))


def secs(r, g):
    return (int(r[g + "_d"]) * 60 + int(r[g + "_m"])) * 60 + int(r[g + "_s"])


def tdays(table, i):
    if table == "collected":
        return 10631 * i
    if table == "single":
        return sum(355 if n in LEAP else 354 for n in range(1, i + 2))
    if table == "months":
        return [30, 59, 89, 118, 148, 177, 207, 236, 266, 295, 325, 354, 355][i]
    if table == "days":
        return i + 1
    if table == "hours":
        return (i + 1) / 24


rows = read("mm_p2.tsv")
ledger = {r["where"] for r in read("mm_discrepancies.tsv")}
found, agree, worst = [], 0, 0.0
for table in ("collected", "single", "months", "days", "hours"):
    T = [r for r in rows if r["table"] == table]
    t = np.array([tdays(table, i) for i in range(len(T))], float)
    exp_args = {"collected": [str(1 + 30 * i) for i in range(len(T))], "single": [str(i + 1) for i in range(len(T))],
                "days": [str(i + 1) for i in range(len(T))], "hours": [str(i + 1) for i in range(len(T))]}.get(table)
    if exp_args and [r["arg"] for r in T] != exp_args:
        found.append((f"{table} arguments", "", ""))
    for g in GROUPS:
        u = np.array([secs(r, g) for r in T], float)
        b = RATE[g] * 3600
        a = u[0] - b * t[0]
        keep = np.ones(len(T), bool)
        for _ in range(4):                       # unwrap about the current line, refit, drop points far from it
            unwrapped = u + MOD * np.round(((a + b * t) - u) / MOD)
            b, a = np.polyfit(t[keep], unwrapped[keep], 1)
            res = unwrapped - (a + b * t)
            keep = np.abs(res) < 30
        unwrapped = u + MOD * np.round(((a + b * t) - u) / MOD)
        res = unwrapped - (a + b * t)
        for i, r in enumerate(T):
            if abs(res[i]) > 3:
                found.append((f"p. {r['ppage']} {table} {r['arg']} {g}", f"{r[g + '_d']}° {r[g + '_m']}′ {r[g + '_s']}″",
                              f"{res[i]:+.1f}″ from the line"))
            else:
                agree += 1
                worst = max(worst, abs(res[i]))
# cross-table identities
one_year = [r for r in rows if r["table"] == "single"][0]
comm = [r for r in rows if r["table"] == "months"][11]
day1 = [r for r in rows if r["table"] == "days"][0]
h24 = [r for r in rows if r["table"] == "hours"][23]
for g in GROUPS:
    if secs(one_year, g) != secs(comm, g):
        found.append((f"identity single year 1 = dhu 'l-hijjah comm. ({g})", "", ""))
    if secs(day1, g) != secs(h24, g):
        found.append((f"identity day 1 = hour 24 ({g})", "", ""))

open_ = [f for f in found if f[0] not in ledger]
print(f"values on their lines {agree} (largest deviation {worst:.1f}″), differ {len(found)} "
      f"(ledgered {len(found) - len(open_)}, open {len(open_)})")
for where, p, e in (found if "--list" in sys.argv else open_):
    print(f"  {where}: {p} {e}" + ("" if where in ledger else "   << not in the ledger"))
stale = [w for w in ledger if w not in {f[0] for f in found}]
for w in stale:
    print("  ledger entry without a difference:", w)
sys.exit(1 if open_ or stale else 0)

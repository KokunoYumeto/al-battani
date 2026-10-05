"""Check of Nallino's Part II pp. 7-8 against the calendar arithmetic (calendars.py).
p. 7, scheme I (left): the sign of a Hijra year N = 30k + n is the sign of the collected years 30k (5k mod 7) plus the
  sign of the single year n (the weekday of 1 al-Muharram of year n, 1 = Sunday); the sign of a month is the number
  of days before it in the year, mod 7 (0 printed for al-Muharram and shawwal).
  Scheme II (right): the single years and the months shifted by 5 (Nallino, Part II p. 198: «signum primi anni
  hegirae erit nempe 7 + 5 = 5»), i.e. single years + 2 and months + 5; the collected years as in I; B marks the
  leap years 2 5 7 10 13 16 18 21 24 26 29; the months alternate 30 and 29 days.
p. 8: the weekday of the first day of each Syrian month for the 28 years of the solar cycle, row r for the
  Seleucid years Y with (Y + 1) mod 28 = r («per 28 dividenda et uno anno augenda»), the year beginning in Aylul;
  the bissextile column 15, 30, 45, B (quarters of a day in sixtieths).
Exit code 1 on any difference not in signs_discrepancies.tsv."""
import csv, sys
from pathlib import Path
import calendars as C

HERE = Path(__file__).resolve().parent


def read(name):
    return list(csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t"))


def s7(x):
    return (x - 1) % 7 + 1


found, agree = [], 0


def cmp(where, printed, expected):
    global agree
    if printed == expected:
        agree += 1
    else:
        found.append((where, printed, expected))


LEAP = {2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29}
days_before = 0
months = [r for r in read("p7_signs.tsv") if r["part"] == "month"]
lens = {}
for r in read("p7_signs.tsv"):
    part, sch, key = r["part"], r["scheme"], r["key"]
    if part == "collected":
        cmp(f"p7 {sch} collected {key}", r["sign"], str(s7(5 * int(key) // 30)))
    elif part == "single":
        n = int(key); w = C.weekday_sign(C.hijra_year_start(n))
        cmp(f"p7 {sch} single {n}", r["sign"], str(w if sch == "I" else s7(w + 2)))
        if sch == "II":
            cmp(f"p7 II bissextile {n}", r["bis"], "B" if n in LEAP else "")
names = []
for r in months:
    if r["key"] not in names:
        names.append(r["key"])
for i, name in enumerate(names):
    before = sum(30 if j % 2 == 0 else 29 for j in range(i))
    for r in months:
        if r["key"] != name:
            continue
        exp = str(before % 7) if r["scheme"] == "I" else str(s7(before % 7 + 5))
        cmp(f"p7 {r['scheme']} month {name}", r["sign"], exp)
        cmp(f"p7 {r['scheme']} days {name}", r["days"], str(30 if i % 2 == 0 else 29))

SY = [(9, "Aylūl"), (10, "Tishrīn I"), (11, "Tishrīn II"), (12, "Kānūn I"), (1, "Kānūn II"), (2, "Subāṭ"),
      (3, "Ādhār"), (4, "Nīsān"), (5, "Ayyār"), (6, "Ḥazīrān"), (7, "Tammūz"), (8, "Āb")]
for r in read("p8_signs.tsv"):
    k = int(r["year"]); Y = 924 + (k - 1); y0 = Y - 312
    assert (Y + 1) % 28 == k % 28
    for m, name in SY:
        cmp(f"p8 year {k} {name}", r[name], str(C.weekday_sign(C.jd_julian(y0 if m >= 9 else y0 + 1, m, 1))))
    cmp(f"p8 year {k} bissextile", r["bis"], "B" if k % 4 == 0 else str((k % 4) * 15))
LENGTH = {9: 30, 10: 31, 11: 30, 12: 31, 1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31}
for r in read("signs_heads.tsv"):
    if r["page"] == "8" and r["item"].startswith("month "):
        i = int(r["item"].split()[1]) - 1
        cmp(f"p8 head {SY[i][1]} days", r["la"].split(" / ")[2], f"{LENGTH[SY[i][0]]} d.")

ledger = {r["where"] for r in read("signs_discrepancies.tsv")}
open_ = [f for f in found if f[0] not in ledger]
print(f"agree {agree}, differ {len(found)} (ledgered {len(found) - len(open_)}, open {len(open_)})")
for where, p, e in (found if "--list" in sys.argv else open_):
    print(f"  {where}: printed {p!r} | computed {e!r}" + ("" if where in ledger else "   << not in the ledger"))
stale = [w for w in ledger if w not in {f[0] for f in found}]
for w in stale:
    print("  ledger entry without a difference:", w)
sys.exit(1 if open_ or stale else 0)

"""Check of Nallino's Part II pp. 9-18 (Tabulae I-X): every printed row against the calendar computed in calendars.py
(arithmetical Hijra calendar, al-Battani's epoch Thursday 15 July 622 = JD 1948439, which Nallino states on Part II
p. 199; Julian dates; weekday signs 1 = Sunday; the Seleucid year counted from 1 September, as the order of the
months on p. 8 shows). Also checked: a month name stands at the top of each half and wherever the month changes,
and a ditto mark » everywhere else.
Every difference must be in conc_discrepancies.tsv; exit code 1 otherwise. --list prints all of them."""
import csv, sys
from pathlib import Path
import calendars as C

HERE = Path(__file__).resolve().parent


def read(name):
    return list(csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t"))


rows = read("conc_p2.tsv")
ledger = {r["where"] for r in read("conc_discrepancies.tsv")} if (HERE / "conc_discrepancies.tsv").exists() else set()
found, agree = [], 0
prev = None
for r in rows:
    n = int(r["ah"])
    if r["row"] == "1":
        prev = None
    jd = C.hijra_year_start(n)
    y, m, d = C.julian_from_jd(jd)
    exp = {"wd": str(C.weekday_sign(jd)), "sy": str(y + 312 if m >= 9 else y + 311), "day": str(d)}
    name = C.SYRIAN[m]
    exp_month = name if name != prev else "»"
    prev = name
    for f in ("wd", "sy", "day"):
        where = f"AH {n} {f}"
        if r[f] == exp[f]:
            agree += 1
        else:
            found.append((where, r[f], exp[f]))
    if r["month"] == exp_month:
        agree += 1
    else:
        found.append((f"AH {n} month", r["month"], exp_month))
years = [int(r["ah"]) for r in rows]
if years != list(range(1, 601)):
    found.append(("Hijra years", "not 1-600 in order", ""))

open_ = [f for f in found if f[0] not in ledger]
print(f"cells agree {agree}, differ {len(found)} (ledgered {len(found) - len(open_)}, open {len(open_)})")
for where, printed, computed in (found if "--list" in sys.argv else open_):
    print(f"  {where}: printed {printed} | computed {computed}" + ("" if where in ledger else "   << not in the ledger"))
stale = [w for w in ledger if w not in {f[0] for f in found}]
for w in stale:
    print("  ledger entry without a difference:", w)
sys.exit(1 if open_ or stale else 0)

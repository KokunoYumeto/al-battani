"""Check of Nallino's Part II pp. 187-188, from revolutions_p2.tsv.
1. p. 187, the increments of the mean motions for the revolutions of the years: each column is n times the motion in
   one tropical year, modulo 360°, for n = 1 ... 12. The motion in one year is fitted to each column (setting aside
   values more than TOL from the line), and compared with al-Battani's daily motions, taken from the collected Arab
   years of his tables of mean motions (../mean_motions/mm_p2.tsv, mm5_p2.tsv), times his tropical year of
   365d 5h 46m 24s (Nallino p. 295). A value more than TOL minutes from its line is listed. The cells that Nallino
   emends (p. 295: the last numbers of Jupiter) need ledger entries of kind «noted».
2. p. 188, the table of the revolutions of the years: the «tempora ascensionum» of n years are n times 86° 36′, the
   5h 46m 24s by which the tropical year exceeds 365 days turned into degrees (Nallino p. 295), modulo 360°; the
   collected years 20 ... 200 and the single years 1 ... 20 must agree exactly, and 20 single years with the first
   collected line.
3. p. 188, the altitudes of the Sun at the ends of the twelve temporal hours of the days of the solstices at
   ar-Raqqah: latitude 36° 0′, the Sun 66° 25′ and 113° 35′ from the pole (obliquity 23° 35′; Nallino p. 296). The
   hour angle at the end of hour k is the half-day arc times (6 - k) / 6. A value more than TOL minutes from the
   computation is listed; hours k and 12 - k must be equal.
4. p. 188, the directions of the hours: the angle of the Sun's azimuth from the east-west line at the ends of the
   first six hours, to the north or the south (Nallino's brackets). The printed numbers are Schiaparelli's, with which
   Delambre's agree; Nallino gives the numbers of the codex (p. 296), which need ledger entries of kind «noted». A
   value more than TOL_DIR seconds from the computation is listed, and so is a quarter that disagrees with it.
Every listed difference must be in revolutions_discrepancies.tsv. --list shows the ledgered entries too, --stats the
fitted motions and the largest departures."""
import csv, math, sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
MM = HERE.parent / "mean_motions"
TOL, TOL_DIR = 3, 30
PHI, EPS = 36.0, 23 + 35 / 60
YEAR = 365 + 5 / 24 + 46 / 1440 + 24 / 86400
STEP = 86 * 60 + 36                                   # 5h 46m 24s in minutes of time-degrees
RATE_COL = {"moon": ("mm_p2.tsv", "moon", 3), "moon_anom": ("mm_p2.tsv", "anom", 3), "node": ("mm_p2.tsv", "node", 3),
            "sat": ("mm5_p2.tsv", "sat", 2), "jup": ("mm5_p2.tsv", "jup", 2), "mars": ("mm5_p2.tsv", "mars", 2),
            "ven_anom": ("mm5_p2.tsv", "ven", 2), "mer_anom": ("mm5_p2.tsv", "mer", 2)}
START = {"moon": 13.1763987, "anom": 13.0649829, "node": 0.0529509, "sat": 0.0334995, "jup": 0.0831342,
         "mars": 0.5240743, "ven": 0.6165256, "mer": 3.1067021}
NOTED = ["p. 187 jup 6", "p. 187 jup 8", "p. 187 jup 9", "p. 187 jup 10", "p. 187 jup 11", "p. 187 jup 12"] + \
        [f"p. 188 direction {c} {k}" for c in ("can", "cap") for k in range(1, 7)]


def read(name, folder=HERE):
    return list(csv.DictReader(open(folder / name, encoding="utf-8"), delimiter="\t"))


def daily_rate(fname, g, places):
    """al-Battani's daily motion from the 30-year steps (10631 days) of his collected Arab years"""
    rows = [r for r in read(fname, MM) if r["table"] == "collected"]
    u = []
    for r in rows:
        v = 0
        for suf in ["_d", "_m", "_s"][:places]:
            v = v * 60 + int(r[g + suf])
        u.append(v / 60 ** (places - 1))
    u, t = np.array(u), np.arange(len(rows)) * 10631.0
    un = u + 360 * np.round((u[0] + START[g] * t - u) / 360)
    use = np.ones(len(u), bool)
    for _ in range(3):
        b, a = np.polyfit(t[use], un[use], 1)
        use = np.abs(un - (a + b * t)) * 60 ** (places - 1) <= 3
    return b


def dms(x, secs=False):
    if secs:
        s = round(x * 3600)
        return f"{s // 3600}° {s % 3600 // 60}′ {s % 60}″"
    m = round(x * 60, 1)
    return f"{int(m // 60)}° {m % 60:.1f}′".replace(".0′", "′")


R = read("revolutions_p2.tsv")
found, printed, agree, stats = [], {}, [0], {}


def where(r):
    return f"p. {r['ppage']} {r['table'] if r['table'] in ('altitude', 'direction') else r['column'] if r['table'] == 'increments' else 'years ' + r['column']}" \
           + (f" {r['column']}" if r["table"] in ("altitude", "direction") else "") + f" {r['arg']}"


for r in R:
    printed[where(r)] = f"{r['d']}° {r['m']}′" + (f" {r['s']}″" if r["s"] else "")

# 1. p. 187
for col, (fname, g, places) in RATE_COL.items():
    T = [r for r in R if r["table"] == "increments" and r["column"] == col]
    n = np.array([int(r["arg"]) for r in T], float)
    v = np.array([int(r["d"]) * 60 + int(r["m"]) for r in T], float)
    year = (daily_rate(fname, g, places) * YEAR) % 360 * 60          # minutes per tropical year
    inc = v[0]
    use = np.ones(12, bool)
    for _ in range(3):                    # refine the yearly motion: least squares on the unwrapped values used
        un = v + 21600 * np.round((n * inc - v) / 21600)
        inc = float(np.sum(un[use] * n[use]) / np.sum(n[use] ** 2))
        res = ((v - n * inc + 10800) % 21600) - 10800
        use = np.abs(res) <= TOL
    res = ((v - n * inc + 10800) % 21600) - 10800
    res_al = ((v - n * year + 10800) % 21600) - 10800
    stats[col] = (inc, year, float(np.abs(res[use]).max()), float(np.abs(res_al).max()))
    for r, x in zip(T, res):
        if abs(x) > TOL:
            found.append((where(r), printed[where(r)], f"{x:+.1f}′ from the line (n x {dms(inc / 60)} gives "
                                                        f"{dms((int(r['arg']) * inc % 21600) / 60)})"))
        else:
            agree[0] += 1

# 2. the tempora ascensionum
years = {(r["column"], int(r["arg"])): int(r["d"]) * 60 + int(r["m"]) for r in R if r["table"] == "years"}
for (col, k), u in years.items():
    exp = k * STEP % 21600
    if u != exp:
        found.append((f"p. 188 years {col} {k}", printed[f"p. 188 years {col} {k}"], dms(exp / 60)))
    else:
        agree[0] += 1
if years[("single", 20)] != years[("collected", 20)]:
    found.append(("identity p. 188 single 20 = collected 20", "", ""))

# 3. the altitudes and 4. the directions
COMP = {}
for key, dec in (("can", EPS), ("cap", -EPS)):
    ph, d = math.radians(PHI), math.radians(dec)
    h0 = math.acos(-math.tan(ph) * math.tan(d))
    for k in range(1, 13):
        t = h0 * (6 - k) / 6
        alt = math.degrees(math.asin(math.sin(ph) * math.sin(d) + math.cos(ph) * math.cos(d) * math.cos(t)))
        north = math.cos(ph) * math.sin(d) - math.sin(ph) * math.cos(d) * math.cos(t)
        east = math.cos(d) * math.sin(t)
        amp = math.degrees(math.atan2(north, abs(east))) if k < 6 else (90.0 if north > 0 else -90.0)
        COMP[(key, k)] = (max(alt, 0.0), amp)
dev_alt, dev_dir, prev = {}, {}, {}
for r in R:
    if r["table"] == "altitude":
        k = int(r["arg"]); u = int(r["d"]) + int(r["m"]) / 60
        dev = (u - COMP[(r["column"], k)][0]) * 60
        dev_alt[(r["column"], k)] = dev
        if abs(dev) > TOL:
            found.append((where(r), printed[where(r)], f"computed {dms(COMP[(r['column'], k)][0])}"))
        else:
            agree[0] += 1
    elif r["table"] == "direction":
        k = int(r["arg"]); u = int(r["d"]) + int(r["m"]) / 60 + int(r["s"]) / 3600
        amp = COMP[(r["column"], k)][1]
        dev = (u - abs(amp)) * 3600
        dev_dir[(r["column"], k)] = dev
        quarter = r["quarter"] if r["quarter"] != "id." else prev[r["column"]]
        prev[r["column"]] = quarter
        if (quarter == "ad bor.") != (amp > 0):
            found.append((where(r) + " quarter", r["quarter"], "north" if amp > 0 else "south"))
        if abs(dev) > TOL_DIR:
            found.append((where(r), printed[where(r)], f"computed {dms(abs(amp), True)}"))
        else:
            agree[0] += 1
alt = {(r["column"], int(r["arg"])): r["d"] + " " + r["m"] for r in R if r["table"] == "altitude"}
sym = sum(alt[(c, k)] == alt[(c, 12 - k)] for c in ("can", "cap") for k in range(1, 6))
for c in ("can", "cap"):
    for k in range(1, 6):
        if alt[(c, k)] != alt[(c, 12 - k)]:
            found.append((f"identity p. 188 altitude {c} {k} = {12 - k}", alt[(c, k)], alt[(c, 12 - k)]))
    if alt[(c, 12)] != "0 0":
        found.append((f"p. 188 altitude {c} 12", alt[(c, 12)], "0° 0′"))


def main():
    rows = read("revolutions_discrepancies.tsv")
    ledger = {r["where"] for r in rows if r["kind"] != "noted"}
    noted = {r["where"]: r for r in rows if r["kind"] == "noted"}
    problems = [f"no ledger entry for Nallino's note: {w} (printed {printed.get(w)})" for w in NOTED if w not in noted]
    problems += [f"{w}: the ledger says printed {noted[w]['printed']}, the table has {printed.get(w)}"
                 for w in NOTED if w in noted and noted[w]["printed"] != printed.get(w)]
    open_ = [f for f in found if f[0] not in ledger]
    print(f"values on their computation {agree[0]}, differ {len(found)} (ledgered {len(found) - len(open_)}, open "
          f"{len(open_)}); altitudes symmetric {sym} of 10; Nallino's notes {len(NOTED)}, problems {len(problems)}")
    if "--stats" in sys.argv:
        for col, (inc, year, mx, mx_al) in stats.items():
            print(f"  p. 187 {col}: fitted motion in one year {dms(inc / 60)} ({inc / 60:.5f}°), al-Battani's daily "
                  f"motion x 365d 5h 46m 24s {year / 60:.5f}°, difference {(inc - year) * 60:+.1f}″ a year; largest "
                  f"departure from the fitted line {mx:.1f}′, from al-Battani's motion {mx_al:.1f}′")
        print("  altitudes, printed minus computed (′): " + "; ".join(
            f"{c} " + " ".join(f"{dev_alt[(c, k)]:+.1f}" for k in range(1, 7)) for c in ("can", "cap")))
        print("  directions, printed minus computed (″): " + "; ".join(
            f"{c} " + " ".join(f"{dev_dir[(c, k)]:+.0f}" for k in range(1, 7)) for c in ("can", "cap")))
    for w, p, e in (found if "--list" in sys.argv else open_):
        print(f"  {w}: {p}; {e}" + ("" if w in ledger else "   << not in the ledger"))
    for p in problems:
        print("  " + p)
    stale = [w for w in ledger if w not in {f[0] for f in found}]
    for w in stale:
        print("  ledger entry without a difference:", w)
    sys.exit(1 if open_ or stale or problems else 0)


if __name__ == "__main__":
    main()

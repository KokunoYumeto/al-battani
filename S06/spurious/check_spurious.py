"""Check of Nallino's Part II pp. 300-307 (the spurious tables), from spurious_p2.tsv and spurious_heads.tsv.
Weekdays are numbered 1 (Sunday) ... 7 (Saturday); a sign is compared modulo 7 (the sign 0 equals 7).
  p. 300  Maslamah's signs of the beginnings of the Arab years (the decades 0 ... 210 and the years 1 ... 9 after each):
          the weekday of 1 al-muharram less one (Nallino p. 314); 1 al-muharram AH 1 was a Thursday, the year has 354
          days and 355 in the years 2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29 of the 30-year cycle. The signs of the
          months are one more than the days before the month, modulo 7; the months have 30 and 29 days in turn.
  p. 301  the collected years 30k: the weekday shift of 30k years (10,631 days a cycle), 5k modulo 7; the single
          years n and their signs as on p. 300; the signs of the months as on p. 300; the Persian months: the weekday
          of the first of the month in a year of Yazdegerd whose number leaves the remainder c of the column when
          divided by 7 (1 farwardin of year 1 a Tuesday; months of 30 days, the five added days after aban; p. 314).
  p. 302  the weekdays of the firsts of the months of the Seleucid years 1 ... 28, beginning on Monday 1 October 312 BC,
          with the leap day at the end of February (Nallino p. 315: the signs show it there, whatever the title says);
          the column of intercalation (30, 45, Bisext., 15 for the years 1 ... 4); the multiples of 28.
  p. 303  the weekdays of the firsts of the Coptic months, the era beginning on a Friday (p. 316), twelve months of 30
          days, five added days, and a sixth at the end of the years 2, 6, 10 ...; the column of the bisextiles.
  p. 304  the conversion of the eras: for 30k Arab years (10,631k days), the Roman and the Coptic years (of 365 1/4
          days, twelve months of 30 days) from their initia 932 y 9 m 17 d 0' and 337 y 10 m 19 d 45' before the Hijra,
          the fractions in sixtieths of a day; the Persian years (of 365 days) from their initium 9 y 11 m 9 d after
          the Hijra (Nallino pp. 316-317). The initia in the heads (Maghribi abjad) must equal their Latin.
  p. 305  the same for the single Arab years 1 ... 30 (the Syrian years as the Roman ones, from the Hijra); the B
          marks the leap years; the months: the months and days of 30 to the end of each Arab month.
  pp. 306-307  the mean conjunctions and oppositions in collected Arab years 1, 31 ... 631: column I advances by 20
          minutes a line; each of II, III and IV advances by a constant step (fitted; every value within TOL_SYZ
          seconds of its line); IV of the conjunctions is IV of the oppositions plus 6 signs (Nallino p. 317), and
          I of the conjunctions is I of the oppositions plus 14d 18h 22m. The steps and the first lines are compared
          with al-Battani's mean motions (../mean_motions/mm_p2.tsv) in --stats.
Every listed difference must be in spurious_discrepancies.tsv; Nallino's restorations of p. 304 (the last two lines)
need entries of kind «noted». --list shows the ledgered entries too, --stats the syzygy elements."""
import csv, math, sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TOL_SYZ = 2
LEAP_ARAB = {2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29}
NOTED = ["p. 304 R 630", "p. 304 R 660", "p. 304 C 630", "p. 304 C 660"]
ABJAD = dict(zip("ابجدهوزحطيكلمنصعفضقرستثخذظغش",
                 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800,
                  900, 1000]))


def read(name, folder=HERE):
    return list(csv.DictReader(open(folder / name, encoding="utf-8"), delimiter="\t"))


R = read("spurious_p2.tsv")
V = {}
for r in R:
    V.setdefault((r["ppage"], r["table"]), {}).setdefault(r["arg"], {})[r["column"]] = r["value"]
found, agree, ident = [], [0], {}


def same_sign(a, b):
    return (int(a) - int(b)) % 7 == 0


def cmp(where, printed, computed, sign=False):
    ok = same_sign(printed, computed) if sign else str(printed) == str(computed)
    if ok:
        agree[0] += 1
    else:
        found.append((where, str(printed), str(computed)))


def identity(name, ok, where="", printed="", computed=""):
    ident.setdefault(name, [0, 0])
    ident[name][0 if ok else 1] += 1
    if not ok:
        found.append((where, printed, computed))


# the Arab calendar
def arab_days_before(n):
    if n <= 0:
        return -354 * (1 - n)
    q, r = divmod(n - 1, 30)
    return 10631 * q + 354 * r + sum(1 for y in range(1, r + 1) if y in LEAP_ARAB)


def arab_weekday(n):
    return (4 + arab_days_before(n)) % 7 + 1                      # AH 1 began on a Thursday (5)


MONTH_DAYS = [30, 29] * 6
BEFORE = [sum(MONTH_DAYS[:m]) for m in range(12)]
MONTH_SIGN = [b % 7 + 1 for b in BEFORE]

# p. 300
for D, row in V[("300", "decades")].items():
    D = int(D)
    cmp(f"p. 300 decade {D}", row["decade"], arab_weekday(D) - 1, sign=True)
    for j in range(1, 10):
        cmp(f"p. 300 year {D + j}", row[str(j)], arab_weekday(D + j) - 1, sign=True)
for i, (m, row) in enumerate(V[("300", "months")].items()):
    cmp(f"p. 300 month {m} sign", row["sign"], MONTH_SIGN[i])
    cmp(f"p. 300 month {m} days", row["days"], str(MONTH_DAYS[i]) if i < 11 else "29 et {sfrac:11/30}")
r0, r210 = V[("300", "decades")]["0"], V[("300", "decades")]["210"]
identity("p. 300: the decade 210 repeats the decade 0 (210 years = 74,417 days, 10,631 weeks)",
         all(same_sign(r0[k], r210[k]) for k in r0), "identity p. 300 210 = 0", "", "")
# Nallino's example (p. 314): the beginning of AH 680 = 3 x 210 + 50: the sign of 50 plus that of al-muharram
ex680 = (int(V[("300", "decades")]["50"]["decade"]) + 1 - 1) % 7 + 1
identity("p. 300: Nallino's example, AH 680 began on a Monday", ex680 == 2 == arab_weekday(680),
         "p. 300 example 680", str(ex680), "2")

# p. 301
for coll, row in V[("301", "years")].items():
    k = int(coll) // 30
    cmp(f"p. 301 collected {coll}", row["collected_sign"], 10631 * k % 7, sign=True)
    cmp(f"p. 301 single {k} number", row["single"], k)
    cmp(f"p. 301 single {k}", row["single_sign"], arab_weekday(k) - 1, sign=True)
for i, (m, row) in enumerate(V[("301", "arab_months")].items()):
    cmp(f"p. 301 month {m} sign", row["sign"], MONTH_SIGN[i])
PERS_BEFORE = [30 * m for m in range(8)] + [245, 275, 305, 335]
for i, (m, row) in enumerate(V[("301", "persian")].items()):
    for c in range(1, 8):
        cmp(f"p. 301 persian {m} {c}", row[str(c)], (2 + (c - 1) + PERS_BEFORE[i]) % 7 + 1)
pers200 = int(V[("301", "persian")]["tīr-māh"]["4"])
identity("p. 301: Nallino's example, tir-mah of Y 200 (200 = 7 x 28 + 4) began on a Thursday", pers200 == 5,
         "p. 301 example 200", str(pers200), "5")

# p. 302: the Seleucid years from Monday 1 October 312 BC; February of year n in the astronomical year n - 311
SYR = ["oct", "nov", "dec", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep"]
SYR_BEFORE = [0, 31, 61, 92, 123, 151, 182, 212, 243, 273, 304, 335]
leap = lambda n: (n - 311) % 4 == 0
days = 0
for n in range(1, 29):
    row = V[("302", "grid")][str(n)]
    for k, mname in enumerate(SYR):
        cmp(f"p. 302 year {n} {mname}", row[mname], (1 + days + SYR_BEFORE[k] + (1 if k >= 5 and leap(n) else 0)) % 7 + 1)
    exp = {1: "30", 2: "45", 3: "Bisext." if n == 3 else "B", 0: "15"}[n % 4]
    cmp(f"p. 302 year {n} inter", row["inter"], exp)
    identity("p. 302: March has the sign of February in the common years, one more in the leap years "
             "(the leap day at the end of February)",
             (int(row["mar"]) - int(row["feb"])) % 7 == (1 if leap(n) else 0), f"identity p. 302 year {n} feb-mar",
             f"{row['feb']} {row['mar']}", "")
    identity("p. 302: January has the sign of December plus 3 (31 = 4 x 7 + 3)",
             (int(row["jan"]) - int(row["dec"])) % 7 == 3, f"identity p. 302 year {n} dec-jan",
             f"{row['dec']} {row['jan']}", "")
    days += 366 if leap(n) else 365
for a, row in V[("302", "multiples")].items():
    k = int(a) // 28
    identity("p. 302: the multiples of 28 (28k and 28(k + 29))", int(a) == 28 * k and int(row["value"]) == 28 * (k + 29),
             f"p. 302 multiple {a}", f"{a} {row['value']}", f"{28 * k} {28 * (k + 29)}")

# p. 303: the Coptic years, the era beginning on a Friday; the sixth added day at the end of the years 2, 6, 10 ...
COPT = ["tut", "babah", "hatur", "kiyahk", "tubah", "amshir", "barmahut", "barmudhah", "bashans", "bawunah", "abib",
        "misri"]
days = 0
for n in range(1, 29):
    row = V[("303", "grid")][str(n)]
    for k, mname in enumerate(COPT):
        cmp(f"p. 303 year {n} {mname}", row[mname], (5 + days + 30 * k) % 7 + 1)
    cmp(f"p. 303 year {n} bisext", row["bisext"], {1: "45", 2: "Bisext." if n == 2 else "B", 3: "15", 0: "30"}[n % 4])
    days += 366 if n % 4 == 2 else 365


# pp. 304-305: the conversion of the eras
def ymdf(T, year=365.25):
    Y = int(T // year)
    rem = T - Y * year
    M = int(rem // 30)
    D = int(rem - 30 * M + 1e-9)
    F = round((rem - 30 * M - D) * 60)
    if F == 60:
        D, F = D + 1, 0
    return [Y, M, D, F]


EPOCH = {"R": 932 * 365.25 + 9 * 30 + 17, "C": 337 * 365.25 + 10 * 30 + 19 + 45 / 60, "P": 9 * 365 + 11 * 30 + 9}
PLACES = ["anni", "menses", "dies", "fract"]
for a, row in V[("304", "conversion")].items():
    t = 10631 * int(a) // 30
    comp = {"R": ymdf(EPOCH["R"] + t), "C": ymdf(EPOCH["C"] + t), "P": ymdf(t - EPOCH["P"], 365)[:3]}
    for era, vals in comp.items():
        pr = [row[f"{era}_{p}"] for p in PLACES[:len(vals)]]
        w = f"p. 304 {era} {a}"
        if [int(x) for x in pr] == vals:
            agree[0] += len(vals)
        else:
            found.append((w, " ".join(pr), " ".join(map(str, vals))))
for n, row in V[("305", "years")].items():
    n = int(n)
    T = 354 * n + sum(1 for y in range(1, n + 1) if y in LEAP_ARAB)
    comp = {"S": ymdf(T), "P": ymdf(T, 365)[:3]}
    for era, vals in comp.items():
        pr = [row[f"{era}_{p}"] for p in PLACES[:len(vals)]]
        if [int(x) for x in pr] == vals:
            agree[0] += len(vals)
        else:
            found.append((f"p. 305 {era} {n}", " ".join(pr), " ".join(map(str, vals))))
    cmp(f"p. 305 year {n} bisext", row.get("bisext", ""), "B" if n in LEAP_ARAB else "")
for i, (m, row) in enumerate(V[("305", "months")].items()):
    M, D = divmod(BEFORE[i] + MONTH_DAYS[i], 30)
    cmp(f"p. 305 month {m}", f"{row['menses']} {row['dies']}", f"{M} {D}")
# the initia in the heads of p. 304
HEADS = {(h["ppage"], h["key"]): h for h in read("spurious_heads.tsv")}


def abjad(word):
    return 0 if word == "{0}" else sum(ABJAD[ch] for ch in word)


heads_ok = 0
for key, nums in (("R", [932, 9, 17, 0]), ("C", [337, 10, 19, 45]), ("P", [9, 11, 9])):
    ar = HEADS[("304", key)]["ar"].replace(" / ", " ").split()
    i = ar.index("الهجرة", ar.index("قبل" if key != "P" else "بعد"))
    vals = [abjad(w) for w in ar[i + 1:]]
    la = HEADS[("304", key)]["la"]
    import re
    la_nums = [int(x) for x in re.findall(r"(\d+) (?:an|a|m|d|fract)\.", la.replace(" / ", " "))]
    if vals == nums == la_nums:
        heads_ok += 1
    else:
        found.append((f"p. 304 head {key}", " ".join(ar[i + 1:]), f"abjad {vals}, Latin {la_nums}"))

# pp. 306-307: the syzygies
SYZ, STEP = {}, {}


def arcsec(row, c):
    return ((int(row[c + "_s"]) * 30 + int(row[c + "_d"])) * 60 + int(row[c + "_m"])) * 60 + int(row[c + "_sec"])


def show(x):
    x = round(x) % 1296000
    return f"{x // 108000}s {x % 108000 // 3600}° {x % 3600 // 60}′ {x % 60}″"


for pp, table in (("306", "conjunctions"), ("307", "oppositions")):
    T = V[(pp, table)]
    args = sorted(T, key=int)
    if args != [str(1 + 30 * k) for k in range(22)]:
        found.append((f"p. {pp} arguments", " ".join(args), ""))
    d0, hm0 = int(T["1"]["I_dies"]), int(T["1"]["I_horae"]) * 60 + int(T["1"]["I_min"])
    for k, a in enumerate(args):
        row = T[a]
        cmp(f"p. {pp} {a} I", f"{row['I_dies']} {int(row['I_horae']) * 60 + int(row['I_min'])}", f"{d0} {hm0 + 20 * k}")
    for c in ("II", "III", "IV"):
        v = np.array([arcsec(T[a], c) for a in args], float)
        un = np.unwrap(v / 1296000 * 2 * np.pi) / (2 * np.pi) * 1296000
        k = np.arange(len(v))
        b, a0 = np.polyfit(k, un, 1)
        res = un - (a0 + b * k)
        STEP[(pp, c)] = (b % 1296000, float(np.abs(res).max()))
        for a, x in zip(args, res):
            if abs(x) > TOL_SYZ:
                found.append((f"p. {pp} {a} {c}", show(arcsec(T[a], c)), f"{x:+.1f}″ from the line"))
            else:
                agree[0] += 1
    SYZ[pp] = T
for a in SYZ["306"]:
    cj, op = SYZ["306"][a], SYZ["307"][a]
    identity("pp. 306-307: IV of the conjunctions = IV of the oppositions + 6 signs",
             (arcsec(cj, "IV") - arcsec(op, "IV")) % 1296000 == 648000, f"identity pp. 306-307 {a} IV",
             f"{show(arcsec(cj, 'IV'))}, {show(arcsec(op, 'IV'))}", "6s")
    dt = (int(cj["I_dies"]) * 1440 + int(cj["I_horae"]) * 60 + int(cj["I_min"])) - \
         (int(op["I_dies"]) * 1440 + int(op["I_horae"]) * 60 + int(op["I_min"]))
    identity("pp. 306-307: I of the conjunctions = I of the oppositions + 14d 18h 22m", dt == 14 * 1440 + 18 * 60 + 22,
             f"identity pp. 306-307 {a} I", str(dt), str(14 * 1440 + 18 * 60 + 22))


def battani():
    """al-Battani's radices at the epoch and daily motions, from the collected Arab years of his tables (degrees)"""
    MM = [r for r in read("mm_p2.tsv", HERE.parent / "mean_motions") if r["table"] == "collected"]
    out = {}
    for g, start in (("sun", 0.98565), ("moon", 13.1764), ("anom", 13.06498), ("node", 0.05295)):
        u = np.array([(int(r[g + "_d"]) * 60 + int(r[g + "_m"])) * 60 + int(r[g + "_s"]) for r in MM], float) / 3600
        t = np.arange(len(u)) * 10631.0
        un = u + 360 * np.round((u[0] + start * t - u) / 360)
        b, a = np.polyfit(t, un, 1)
        out[g] = (a, b)
    return out


def stats():
    B = battani()
    (s0, sr), (m0, mr), (a0, ar), (n0, nr) = B["sun"], B["moon"], B["anom"], B["node"]
    month = 360 / (mr - sr)
    t360 = 360 * month
    print(f"  al-Battani's synodic month {month:.7f} d; 360 months = 10,631 d + {(t360 - 10631) * 1440:.2f} min")
    model = {"II": sr * t360, "III": ar * t360, "IV": (mr + nr) * t360}
    for pp in ("306", "307"):
        for c in ("II", "III", "IV"):
            st, mx = STEP[(pp, c)]
            print(f"  p. {pp} {c}: step {show(st)} ({st:.2f}″), largest departure from the line {mx:.2f}″; "
                  f"al-Battani's motion in 360 months {show(model[c] * 3600)} ({(model[c] * 3600) % 1296000:.2f}″)")
    el0 = (m0 - s0) % 360
    for pp, target in (("306", 360), ("307", 180)):
        t = (target - el0) / (mr - sr)
        row = SYZ[pp]["1"]
        print(f"  p. {pp}, first line: {row['I_dies']}d {row['I_horae']}h {row['I_min']}m, II {show(arcsec(row, 'II'))}, "
              f"III {show(arcsec(row, 'III'))}, IV {show(arcsec(row, 'IV'))}; al-Battani's first mean "
              f"{'conjunction' if pp == '306' else 'opposition'} after the epoch: {int(t)}d {(t % 1) * 24:.3f}h, "
              f"the Sun {show((s0 + sr * t) * 3600)}, the anomaly {show((a0 + ar * t) * 3600)}, the argument of "
              f"latitude {show((m0 + n0 + (mr + nr) * t) * 3600)}")


def main():
    rows = read("spurious_discrepancies.tsv")
    ledger = {r["where"] for r in rows if r["kind"] != "noted"}
    noted = {r["where"]: r for r in rows if r["kind"] == "noted"}
    printed = {}
    for era in ("R", "C"):
        for a in ("630", "660"):
            row = V[("304", "conversion")][a]
            printed[f"p. 304 {era} {a}"] = " ".join(row[f"{era}_{p}"] for p in PLACES)
    problems = [f"no ledger entry for Nallino's restoration: {w} (printed {printed.get(w)})" for w in NOTED if w not in noted]
    problems += [f"{w}: the ledger says printed {noted[w]['printed']}, the table has {printed.get(w)}"
                 for w in NOTED if w in noted and noted[w]["printed"] != printed.get(w)]
    open_ = [f for f in found if f[0] not in ledger]
    print(f"values on their computation {agree[0]}, differ {len(found)} (ledgered {len(found) - len(open_)}, open "
          f"{len(open_)}); heads of p. 304 {heads_ok} of 3; Nallino's restorations {len(NOTED)}, problems {len(problems)}")
    for name, (ok, bad) in ident.items():
        print(f"  {name}: {ok} of {ok + bad}")
    if "--stats" in sys.argv:
        stats()
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

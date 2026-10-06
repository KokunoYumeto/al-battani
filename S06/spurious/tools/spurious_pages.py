"""Read Part II pp. 300-307, the spurious tables at the end of the codex (Nallino, Part II pp. 308-317):
  p. 300 (PDF 749)  Maslamah's signs (weekdays) of the beginnings of the Arab years and months
  p. 301 (PDF 750)  the signs of the Arab years (collected, single) and months; the signs of the Persian months
  p. 302 (PDF 751)  the signs of the Syrian (Seleucid, from October) months for 28 years, and the multiples of 28
  p. 303 (PDF 752)  the signs of the Coptic months for 28 years
  p. 304 (PDF 753)  the conversion of eras by collected Arab years
  p. 305 (PDF 754)  the conversion of eras by single Arab years and months
  p. 306 (PDF 755)  the mean conjunctions in collected Arab years
  p. 307 (PDF 756)  the mean oppositions in collected Arab years
Each table is computed (calendar arithmetic; for the syzygies, constant steps fitted to the table) and the computation
is the expected value of the reading: the glyph reader and the OCR text layer classify each cell (motion_page.run;
A both give the value, B one, C neither: read again by eye). The computation here only guides the reading; the check
scripts in S06/spurious/ compare the data with the computation and list every difference.
Weekday signs: 1 Sunday ... 7 Saturday."""
import motion_page as mp
import p2cols, wide_kit as wk

LEAP_ARAB = {2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29}


def arab_days_before(n):
    """days from 1 Muharram AH 1 to 1 Muharram of year n (n >= 0; year 0 has 354 days)"""
    if n <= 0:
        return -354 * (1 - n)
    q, r = divmod(n - 1, 30)
    return 10631 * q + 354 * r + sum(1 for y in range(1, r + 1) if y in LEAP_ARAB)


def arab_year_weekday(n):
    return (5 - 1 + arab_days_before(n)) % 7 + 1          # AH 1 began on a Thursday (5), astronomical epoch


ARAB_MONTH_DAYS = [0, 30, 59, 89, 118, 148, 177, 207, 236, 266, 295, 325]


def p300_expected():
    """rows 0, 10 ... 210: the decade sign and the signs of years D+1 ... D+9 (Maslamah: weekday - 1)"""
    rows = []
    for D in range(0, 211, 10):
        rows.append([(arab_year_weekday(D + j) - 2) % 7 + 1 for j in range(10)])
    return rows


def run300(tag="e"):
    y0, y1 = 357, 738
    rules = [x for x in p2cols.rules_banded(749, y0 + 10, y1 - 5) if x < 382]
    exp = p300_expected()
    tv = [[r[j] for r in exp] for j in range(10)]
    args = list(range(0, 211, 10))
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 6
    return mp.run(749, y0, y1, rules, tv, args=args, nsub=[1] * 10, mods=[1000] * 10, fixed=[(0, 1)] * 10,
                  keep=keep, tag=tag)


def p301_expected():
    """years: (collected sign of 30k = the weekday shift of 30k years, single n, sign of year n = weekday - 1);
    Persian months: the weekday of the first of month m in a year whose number leaves the remainder c (1-7) by 7"""
    years = [((10631 * k) % 7 or 7, k, (arab_year_weekday(k) - 2) % 7 + 1) for k in range(1, 31)]
    pers_days = [30 * m for m in range(8)] + [245, 275, 305, 335]
    persian = [[(3 - 1 + (c - 1) + d) % 7 + 1 for c in range(1, 8)] for d in pers_days]
    months = [(d % 7) + 1 for d in ARAB_MONTH_DAYS]
    return years, persian, months


def run301(tag="e"):
    years, persian, months = p301_expected()
    out = {}
    tv = [[y[0] for y in years], [y[1] for y in years], [y[2] for y in years]]
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 2
    out["years"] = mp.run(750, 325, 745, [66.5, 107.7, 131.6, 172.7, 196.0], tv, args=list(range(30, 901, 30)),
                          nsub=[1] * 3, mods=[1000] * 3, fixed=[(0, 1)] * 3, keep=keep, tag=tag + "y")
    tv = [[row[c] for row in persian] for c in range(7)]
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 4
    out["persian"] = mp.run(750, 335, 735, [362.0, 374.8, 391.4, 407.5, 423.1, 439.4, 455.8, 471.6, 487.0], tv,
                            nsub=[1] * 7, mods=[1000] * 7, fixed=[(0, 1)] * 7, keep=keep, tag=tag + "p")
    return out


SYR_MONTHS = ["oct", "nov", "dec", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep"]
SYR_BEFORE = [0, 31, 61, 92, 123, 151, 182, 212, 243, 273, 304, 335]    # days before the month, common year


def syr_leap(n):
    """the Seleucid year n (from 1 October) contains a 29 February when its February falls in a Julian leap year:
    the February of year n is in the astronomical year n - 311"""
    return (n - 311) % 4 == 0


def p302_expected():
    """rows 1-28: the weekdays of the firsts of the months October ... September of Seleucid year n (era Monday 1 October
    312 BC), the intercalation column (30, 45, B, 15), and the multiples of 28"""
    rows, days = [], 0
    for n in range(1, 29):
        w = []
        for k, d in enumerate(SYR_BEFORE):
            extra = 1 if (k >= 5 and syr_leap(n)) else 0
            w.append((2 - 1 + days + d + extra) % 7 + 1)
        rows.append(w)
        days += 366 if syr_leap(n) else 365
    inter = [{1: "30", 2: "45", 3: "B", 0: "15"}[n % 4] for n in range(1, 29)]
    mult = [(28 * k, 28 * (k + 29)) for k in range(1, 30)]
    return rows, inter, mult


def run302(tag="e"):
    rows, inter, mult = p302_expected()
    out = {}
    tv = [[r[k] for r in rows] for k in range(3)] + [[int(v) if v != "B" else 60 for v in inter]] +          [[r[k] for r in rows] for k in range(3, 12)]
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 7
    out["grid"] = mp.run(751, 312, 742, [118.0, 145.3, 169.1, 192.9, 216.5, 251.1, 275.2, 298.5, 322.6, 346.2, 370.1,
                                         393.6, 417.6, 440.4, 463.2], tv, args=list(range(1, 29)), nsub=[1] * 13,
                         mods=[1000] * 13, fixed=[(0, 1)] * 13, keep=keep, tag=tag + "g")
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 1
    out["mult"] = mp.run(751, 312, 756, [463.2, 497.9, 540.0], [[b for a, b in mult]], args=[a for a, b in mult],
                         nsub=[1], mods=[10000], fixed=[(0, 1)], keep=keep, tag=tag + "m")
    return out


COPT_MONTHS = ["tut", "babah", "hatur", "kiyahk", "tubah", "amshir", "barmahat", "barmudhah", "bashans", "bawunah",
               "abib", "misri"]


def copt_leap(n):
    """year n of the table has a sixth epagomenal day (the Bisext. column marks years 2, 6, 10 ...)"""
    return n % 4 == 2


def p303_expected():
    """rows 1-28: the weekdays of the firsts of the twelve Coptic months (Tut ... Misri, 30 days each, Misri with the
    epagomenal days) of year n, the era beginning on a Friday; the column of the bisextiles (45, B, 15, 30)"""
    rows, days = [], 0
    for n in range(1, 29):
        rows.append([(6 - 1 + days + 30 * k) % 7 + 1 for k in range(12)])
        days += 366 if copt_leap(n) else 365
    bis = [{1: "45", 2: "B", 3: "15", 0: "30"}[n % 4] for n in range(1, 29)]
    return rows, bis


def run303(tag="e"):
    rows, bis = p303_expected()
    tv = [[r[k] for r in rows] for k in range(12)] + [[int(v) if v != "B" else 60 for v in bis]]
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 7
    return {"grid": mp.run(752, 312, 745, [70.0, 104.7, 133.7, 162.5, 191.7, 220.8, 250.1, 279.2, 308.2, 337.4, 366.6,
                                           395.9, 424.8, 453.9, 488.7], tv, args=list(range(1, 29)), nsub=[1] * 13,
                           mods=[1000] * 13, fixed=[(0, 1)] * 13, keep=keep, tag=tag + "g")}


def to_ymdf(T, year=365.25):
    """a number of days as years (of `year` days: 12 months of 30 days and the epagomenal days), months, days and the
    fraction of a day in sixtieths"""
    Y = int(T // year)
    rem = T - Y * year
    M = int(rem // 30)
    D = int(rem - 30 * M)
    F = round((rem - 30 * M - D) * 60)
    if F == 60:
        D, F = D + 1, 0
    return Y, M, D, F


ROMAN_EPOCH = 932 * 365.25 + 9 * 30 + 17          # the Hijra in the Roman (Seleucid) count: 932 y 9 m 17 d 0'
COPTIC_EPOCH = 337 * 365.25 + 10 * 30 + 19 + 45 / 60   # 337 y 10 m 19 d 45'
PERSIAN_AFTER = 9 * 365 + 11 * 30 + 9             # the Persian era begins 9 y 11 m 9 d after the Hijra (3624 days)


def p304_expected():
    """rows 30, 60 ... 660 Arab years (10631 days each 30): the Roman and Coptic counts (years of 365 1/4 days) and the
    Persian count (years of 365 days)"""
    rows = []
    for k in range(1, 23):
        t = 10631 * k
        r = to_ymdf(ROMAN_EPOCH + t); c = to_ymdf(COPTIC_EPOCH + t); pr = to_ymdf(t - PERSIAN_AFTER, 365)
        rows.append(list(r) + list(c) + list(pr[:3]))
    return rows


def run304(tag="e"):
    rows = p304_expected()
    tv = [[r[k] for r in rows] for k in range(11)]
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 6
    return {"grid": mp.run(753, 376, 752, [119.6, 148.1, 190, 222, 252, 289.2, 331, 361, 392, 430.2, 475, 505, 541.0],
                           tv, args=list(range(30, 661, 30)), nsub=[1] * 11, mods=[10000] * 11, fixed=[(0, 1)] * 11,
                           keep=keep, tag=tag + "g")}


def p305_expected():
    """rows 1-30 single Arab years: B in the leap years; the Syrian (Roman) count of n Arab years (years of 365 1/4
    days) and the Persian count (years of 365 days); the months: the months and days to the end of each Arab month"""
    rows = []
    for n in range(1, 31):
        T = 354 * n + sum(1 for y in range(1, n + 1) if y in LEAP_ARAB)
        rows.append(["B" if n in LEAP_ARAB else ""] + list(to_ymdf(T)) + list(to_ymdf(T, 365)[:3]))
    months = [divmod(d, 30) for d in ARAB_MONTH_DAYS[1:] + [354]]
    return rows, months


def run305(tag="e"):
    rows, months = p305_expected()
    out = {}
    tv = [[0] * 30] + [[r[k] for r in rows] for k in range(1, 8)]
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 4
    out["years"] = mp.run(754, 295, 752, [68.7, 96.5, 124.3, 156, 186, 217, 255.4, 287, 316, 353.9], tv,
                          args=list(range(1, 31)), nsub=[1] * 8, mods=[10000] * 8, fixed=[(0, 1)] * 8, keep=keep,
                          tag=tag + "y")
    tv = [[m[0] for m in months], [m[1] for m in months]]
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 1
    out["months"] = mp.run(754, 360, 752, [420.0, 433.7, 459.3, 487.6], tv, nsub=[1, 1], mods=[1000, 1000],
                           fixed=[(0, 1)] * 2, keep=keep, tag=tag + "m")
    return out


def sec(sg, d, m, s_):
    return ((sg * 30 + d) * 60 + m) * 60 + s_


def unsec(x):
    x = round(x) % (360 * 3600)
    sg, r = divmod(x, 30 * 3600)
    d, r = divmod(r, 3600)
    m, s_ = divmod(r, 60)
    return sg, d, m, s_


# the first and the last line of each table as read by eye at 350 dpi (rows 1 and 631): days, hours, minutes; then
# signs, degrees, minutes, seconds of columns II, III, IV
SYZ_ENDS = {755: ((29, 1, 23), [(4, 22, 36, 31), (4, 6, 9, 19), (0, 2, 30, 58)],
                  (29, 8, 23), [(7, 20, 38, 14), (6, 0, 26, 57), (1, 1, 56, 23)]),
            756: ((14, 7, 1), [(4, 8, 3, 15), (9, 23, 13, 49), (6, 2, 30, 58)],
                  (14, 14, 1), [(7, 6, 5, 0), (11, 17, 31, 59), (7, 1, 56, 23)])}


def syz_expected(pdf):
    """rows k = 0 ... 21 (Arab years 1 + 30k): the days; the hours and minutes, 20 minutes more each line; columns II-IV
    interpolated linearly between the first and the last line (the number of whole turns from the approximate steps
    1s 8° 28′ 39″, 9s 24° 0′ 50″ and 8s 1° 24′ 4″)"""
    (d0, h0, m0), v0, (d1, h1, m1), v1 = SYZ_ENDS[pdf]
    approx = [sec(1, 8, 28, 39), sec(9, 24, 0, 50), sec(8, 1, 24, 4)]
    rows = []
    for k in range(22):
        hm = h0 * 60 + m0 + 20 * k
        row = [d0, divmod(hm, 60)]
        for a, b, ap in zip(v0, v1, approx):
            A, B = sec(*a), sec(*b)
            turns = round((A + 21 * ap - B) / (360 * 3600))
            step = (B + turns * 360 * 3600 - A) / 21
            row.append(unsec(A + k * step))
        rows.append(row)
    return rows


SYZ_RULES = {755: [117.4, 151.9, 176, 231.7, 258, 333.0, 359, 434.7, 461, 539.8],
             756: [63.3, 98.2, 120, 176.6, 202, 278.4, 304, 380.6, 406, 483.4]}


def run_syz(pdf, tag="e"):
    rows = syz_expected(pdf)
    tv = [[r[0] for r in rows], [r[1][0] * 60 + r[1][1] for r in rows]]
    for c in range(2, 5):
        tv.append([r[c][0] for r in rows])
        tv.append([r[c][1] * 3600 + r[c][2] * 60 + r[c][3] for r in rows])
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 8
    return {"grid": mp.run(pdf, 360, 735, SYZ_RULES[pdf], tv, args=[1 + 30 * k for k in range(22)],
                           nsub=[1, 2, 1, 3, 1, 3, 1, 3], mods=[100, 24, 12, 30, 12, 30, 12, 30], fixed=[(0, 1)] * 8,
                           keep=keep, tag=tag + "g")}


if __name__ == "__main__":
    import sys
    from collections import Counter
    which = sys.argv[1] if len(sys.argv) > 1 else "300"
    res = {"300": run300, "301": run301, "302": run302, "303": run303, "304": run304, "305": run305, "306": lambda: run_syz(755), "307": lambda: run_syz(756)}[which]()
    for name, out in (res.items() if which != "300" else [("grid", res)]):
        bad = [(i + 1, r["arg"], r.get("arg_exp")) for i, r in enumerate(out["rows"]) if r.get("arg_ok") is False]
        print(which, name, len(out["rows"]), out["classes"], "flags", len(out["flags"]),
              Counter(int(f[1]) for f in out["flags"] if f[0] != "fit"), "args off", bad[:6])

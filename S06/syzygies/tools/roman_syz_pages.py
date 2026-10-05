"""Read Part II pp. 84-87: the mean syzygies in Roman (Julian) years.
  p. 84  conjunctions in collected Roman years 879, 903 ... 1623 (24-year periods): the day of adhar on which the first
         mean conjunction of the year falls, the mean longitude of the luminaries, the lunar anomaly, the argument of
         latitude
  p. 85  oppositions in the same years
  p. 86  single Roman years 1-24
  p. 87  parts of a month; the Roman months; intervals of 48 ... 480 years
Models (L = 29;31,50,8,20 days): in a 24-year period the day moves by delta (fitted, about 297 L - 8766 days) modulo L;
the motions are linear in the number of lunations N_k = 297 k - (number of wraps of the day). Single years: k_n = the
least number of lunations exceeding D_n = 365 n + [n/4] days; day = k_n L - D_n; motions k_n M. Output: MP{pdf}{tag}.json."""
import math
import motion_page as mp

L = 29 + 31 / 60 + 50 / 3600 + 8 / 216000 + 20 / 12960000
DAILY = {"sun": 0.98565176, "anom": 13.06498287, "lat": 13.17639871 + 0.05295093}
M = {k: (L * v) % 360 for k, v in DAILY.items()}                 # motion in one lunation, mod 360 (degrees)
FULL = {"sun": L * DAILY["sun"], "anom": L * DAILY["anom"], "lat": L * DAILY["lat"]}   # whole revolutions included
DELTA = 297 * L - 8766


def wraps(d0, n):
    """number of wraps of the day column (d0 + k delta mod L) up to row k, and the day values"""
    out, w = [], 0
    for k in range(n):
        out.append(int((d0 + k * DELTA) // L))
    return out


def collected(pdf, d0, y0, y1, rules, tag=""):
    ks = list(range(32))
    w = wraps(d0, 32)
    N = [297 * k - w[k] for k in ks]
    tv = [ks, N, N, N]
    rates = [DELTA * 3600, M["sun"] * 3600, M["anom"] * 3600, M["lat"] * 3600]
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 8
    return mp.run(pdf, y0, y1, rules, tv, args=[879 + 24 * k for k in ks], nsub=3, rates=rates, mods=[L, 360, 360, 360],
                  keep=keep, tag=tag)


def single(pdf, y0, y1, rules, tag=""):
    ns = list(range(1, 25))
    D = [365 * n + n // 4 for n in ns]
    K = [math.ceil(d / L) for d in D]
    tv = [[round((k * L - d) * 3600) for k, d in zip(K, D)]] + [[round((k * M[c]) % 360 * 3600) for k in K] for c in ("sun", "anom", "lat")]
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 8
    return mp.run(pdf, y0, y1, rules, tv, args=ns, nsub=3, mods=[400, 360, 360, 360], fixed=[(0, 1)] * 4, keep=keep, tag=tag)


def single2(pdf, y0, y1, rules, tag="b"):
    """second pass of p. 86 against the empirical curves (the exact values plus the running median of the agreed
    residuals)"""
    ns = list(range(1, 25))
    D = [365 * n + n // 4 for n in ns]
    K = [math.ceil(d / L) for d in D]
    tv = [[round((k * L - d) * 3600) for k, d in zip(K, D)]] + [[round((k * M[c]) % 360 * 3600) for k in K] for c in ("sun", "anom", "lat")]
    tv = mp.empirical_tv(str(pdf), tv, [400, 360, 360, 360], [3, 3, 3, 3])
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 8
    return mp.run(pdf, y0, y1, rules, tv, args=ns, nsub=3, mods=[400, 360, 360, 360], fixed=[(0, 1)] * 4, keep=keep, tag=tag)


def parts(pdf, y0, y1, rules, tag=""):
    fr = [1 / 2, 1 / 3, 1 / 4, 1 / 6]
    tv = [[round(f * L * 3600) for f in fr]] + [[round(f * FULL[c] % 360 * 3600) for f in fr] for c in ("sun", "anom", "lat")]
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 8
    return mp.run(pdf, y0, y1, rules, tv, nsub=3, mods=[400, 360, 360, 360], fixed=[(0, 1)] * 4, tag=tag, keep=keep)


def months(pdf, y0, y1, rules, tag=""):
    ms = list(range(1, 13))
    tv = [[round(m * L * 3600) for m in ms]] + [[round(m * FULL[c] % 360 * 3600) for m in ms] for c in ("sun", "anom", "lat")]
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 9
    return mp.run(pdf, y0, y1, rules, [[d for d in (31, 61, 92, 122, 153, 184, 214, 245, 275, 306, 337, 365)]] + tv,
                  nsub=[1, 3, 3, 3, 3], mods=[1000, 400, 360, 360, 360], fixed=[(0, 1)] * 5, tag=tag, keep=keep)


def intervals(pdf, y0, y1, rules, tag=""):
    """intervals of 24 m years: the day moves by m delta (modulo L); the motions are those of N = 297 m - (wraps)
    lunations; delta and the motions per lunation are those fitted on p. 84 (MP533.json)"""
    import json
    import wide_kit as wk
    lines = json.load(open(wk.OUT + "MP533.json", encoding="utf-8"))["lines"]
    delta = lines[0][1] / 3600
    per = [lines[g][1] for g in (1, 2, 3)]                       # seconds of arc per lunation
    ms = [2, 3, 4, 8, 12, 16, 20]
    days = [(m * delta) % L for m in ms]
    N = [297 * m - int(m * delta // L) for m in ms]
    tv = [[round(d * 3600) for d in days]] + [[round((n * p) % (360 * 3600)) for n in N] for p in per]
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 8
    return mp.run(pdf, y0, y1, rules, tv, args=[24 * m for m in ms], nsub=3, mods=[400, 360, 360, 360],
                  fixed=[(0, 1)] * 4, tag=tag, keep=keep)


def intervals_old(pdf, y0, y1, rules, tag=""):
    ms = [2, 3, 4, 8, 12, 16, 20]
    tv = [ms] * 4
    rates = [DELTA * 3600] + [((297 * FULL[c]) % 360) * 3600 for c in ("sun", "anom", "lat")]
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 8
    return mp.run(pdf, y0, y1, rules, tv, args=[24 * m for m in ms], nsub=3, rates=rates, mods=[L, 360, 360, 360], tag=tag,
                  keep=keep)


if __name__ == "__main__":
    import sys
    jobs = {
        "533": lambda: collected(533, 13 + 58 / 60 + 4 / 3600, 284, 740, [111.1, 157.8, 251.4, 344.5, 437.9, 532.2]),
        "534": lambda: collected(534, 28 + 43 / 60 + 59 / 3600, 282, 736, [64.9, 114.2, 207.6, 300.7, 394.2, 485.6]),
        "535": lambda: single(535, 288, 730, [116.4, 164.6, 257.6, 351.0, 444.4, 537.6]),
        "535b": lambda: single2(535, 288, 730, [116.4, 164.6, 257.6, 351.0, 444.4, 537.6]),
        "536a": lambda: parts(536, 192, 254, [63.5, 163.6, 243.7, 324.6, 404.6, 484.2], tag="a"),
        "536m": lambda: months(536, 400, 586, [63.5, 128.2, 163.6, 243.7, 324.6, 404.6, 484.2], tag="m"),
        "536i": lambda: intervals(536, 640, 742, [63.7, 163.4, 243.7, 323.8, 404.2, 483.6], tag="i"),
    }
    for name in sys.argv[1:] or jobs:
        out = jobs[name]()
        bad = [(i + 1, r["arg"], r["arg_exp"]) for i, r in enumerate(out["rows"]) if r.get("arg_ok") is False]
        print(name, len(out["rows"]), out["classes"], "flags", len(out["flags"]), "args off", bad[:5])
        for f in out["flags"][:30]:
            print("    ", f)
        print("    lines", [None if l is None else (round(l[0], 1), round(l[1], 2)) for l in out["lines"]])

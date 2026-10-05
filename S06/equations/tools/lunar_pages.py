"""Read Part II pp. 78-83: for every degree n = 1 ... 180 (and 360 - n): the equation of the Sun, the simple equation of
the Moon, the equation of the anomaly (the prosneusis of the epicycle), the minutes to be added (sixtieths of the
longinquity), the least longinquity (the increment of the equation at the perigee of the eccentre), and the latitude
of the Moon. Models with al-Battani's elements (Nallino, Part II pp. 223-227):
  Sun        tan q = e sin n / (1 + e cos n), e = 2;4,45 / 60
  Moon       tan q = r sin n / (1 + r cos n), r = 5;15 / 60
  prosneusis tan p = e' sin n / (rho + e' cos n), e' = 10;19 / 60, rho = e' cos n + sqrt((1 - e')^2 - e'^2 sin^2 n)
  minutes    60 (asin(r / rho) - asin(r)) / (asin(r / (1 - 2 e')) - asin(r))
  increment  q at the perigee distance 1 - 2 e' less q at the apogee
  latitude   sin b = sin n sin 5
The first column block holds two numbers (n and 360 - n): it is split by a rule at the gap. Output: MP{pdf}.json."""
import math
import motion_page as mp

E_SUN = (2 + 4 / 60 + 45 / 3600) / 60
R_MOON = 5.25 / 60
E_MOON = (10 + 19 / 60) / 60


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
    return eq(n, R_MOON, 1 - 2 * E_MOON) - eq(n, R_MOON)        # in the units of r relative to the distance


def increment_v(n):
    m = math.radians(n)
    rp = R_MOON / (1 - 2 * E_MOON)
    return math.degrees(math.atan2(rp * math.sin(m), 1 + rp * math.cos(m))) - eq(n, R_MOON)


def latitude(n):
    return math.degrees(math.asin(math.sin(math.radians(n)) * math.sin(math.radians(5))))


LEFT = {527: 119.6, 528: 57.1, 529: 115.1, 530: 65.5, 531: 114.2, 532: 66.0}
SPLIT = {527: 151.0, 528: 91.0, 529: 146.5, 530: 102.0, 531: 147.0, 532: 98.0}
RULES = {527: [186.7, 253.4, 319.9, 379.6, 414.2, 474.4, 542.4],
         528: [127.0, 193.1, 259.8, 319.6, 353.9, 413.6, 480.8],
         529: [182.3, 249.0, 315.4, 375.5, 410.2, 469.3, 538.4],
         530: [135.2, 201.6, 268.0, 327.7, 362.4, 422.2, 489.1],
         531: [180.0, 246.7, 313.0, 373.3, 407.9, 466.9, 535.8],
         532: [134.4, 200.6, 267.1, 326.9, 361.2, 421.0, 487.0]}


def expected(pdf):
    n0 = 30 * (pdf - 527)
    ns = [n0 + i for i in range(1, 31)]
    return ns, [ns, [360 - n for n in ns],
                [round(eq(n, E_SUN) * 3600) for n in ns], [round(eq(n, R_MOON) * 3600) for n in ns],
                [round(prosneusis(n) * 60) for n in ns], [round(minutes(n)) for n in ns],
                [round(increment_v(n) * 60) for n in ns], [round(latitude(n) * 3600) for n in ns]]


def run_page(pdf, y0=285, y1=745):
    ns, tv = expected(pdf)
    rules = [LEFT[pdf] - 5, LEFT[pdf], SPLIT[pdf]] + RULES[pdf]
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 10
    return mp.run(pdf, y0, y1, rules, tv, nsub=[1, 1, 3, 3, 2, 1, 2, 3], mods=[1000, 1000, 360, 360, 360, 1000, 360, 360],
                  fixed=[(0, 1)] * 8, keep=keep)


if __name__ == "__main__":
    import sys
    for pdf in [int(a) for a in sys.argv[1:]] or range(527, 533):
        out = run_page(pdf)
        print(pdf, len(out["rows"]), out["classes"], "flags", len(out["flags"]))
        from collections import Counter
        print("    flags by column", Counter(f[1] for f in out["flags"]))
        k, files = mp.sheet(pdf)
        print("    sheet", k, [f.split("\\")[-1] for f in files])


def agreed_values():
    """(column, n) -> units, for the cells where both readers give the same number with confidence"""
    import json
    import wide_kit as wk
    out = {}
    for pdf in range(527, 533):
        d = json.load(open(wk.OUT + f"MP{pdf}.json", encoding="utf-8"))
        for i, r in enumerate(d["rows"]):
            n = 30 * (pdf - 527) + i + 1
            for gi, g in enumerate(r["groups"]):
                if all(c and c["read"] and c["read"] == c.get("tl") and c["conf"] >= 0.85 for c in g):
                    u = 0
                    for c in g:
                        u = u * 60 + int(c["read"])
                    out[(gi, n)] = u
    return out


def empirical(col, model, agreed, half=4):
    """the model plus the running median of the residuals of the agreed values (window 2 half + 1): for the columns
    that al-Battani took over from Ptolemy and interpolated (prosneusis, increment), whose values depart smoothly
    from the computation"""
    import statistics
    res = {n: agreed[(col, n)] - model(n) for n in range(1, 181) if (col, n) in agreed}
    out = {}
    for n in range(1, 181):
        near = [res[k] for k in range(n - half, n + half + 1) if k in res]
        out[n] = model(n) + (statistics.median(near) if near else 0)
    return out


def run_page2(pdf, y0=285, y1=745):
    """second pass: the prosneusis and the increment resolved against the empirical curves"""
    ns, tv = expected(pdf)
    ag = agreed_values()
    pro = empirical(4, lambda n: prosneusis(n) * 60, ag)
    inc = empirical(6, lambda n: increment_v(n) * 60, ag)
    tv[4] = [round(pro[n]) for n in ns]
    tv[6] = [round(inc[n]) for n in ns]
    rules = [LEFT[pdf] - 5, LEFT[pdf], SPLIT[pdf]] + RULES[pdf]
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 10
    return mp.run(pdf, y0, y1, rules, tv, nsub=[1, 1, 3, 3, 2, 1, 2, 3], mods=[1000, 1000, 360, 360, 360, 1000, 360, 360],
                  fixed=[(0, 1)] * 8, keep=keep, tag="b")


def run_page3(pdf, y0=285, y1=745):
    """third pass: every computed column resolved against its empirical curve (the computation plus the running median
    of the residuals of the agreed values), so that smooth runs of al-Battani's departures resolve and only isolated
    cells remain for reading by eye"""
    ns, tv = expected(pdf)
    ag = agreed_values()
    curves = {2: (lambda n: eq(n, E_SUN) * 3600, 3), 3: (lambda n: eq(n, R_MOON) * 3600, 3),
              4: (lambda n: prosneusis(n) * 60, 4), 6: (lambda n: increment_v(n) * 60, 4), 7: (lambda n: latitude(n) * 3600, 3)}
    for col, (f, half) in curves.items():
        cur = empirical(col, f, ag, half)
        tv[col] = [round(cur[n]) for n in ns]
    rules = [LEFT[pdf] - 5, LEFT[pdf], SPLIT[pdf]] + RULES[pdf]
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 10
    return mp.run(pdf, y0, y1, rules, tv, nsub=[1, 1, 3, 3, 2, 1, 2, 3], mods=[1000, 1000, 360, 360, 360, 1000, 360, 360],
                  fixed=[(0, 1)] * 8, keep=keep, tag="c")

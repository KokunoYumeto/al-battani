"""Check of Nallino's Part II pp. 88-91 (the tables for computing eclipses) against the computation with the elements
that the tables themselves use:
  p. 88  hourly motions: the Sun's mean hourly motion (0.98565176° / 24) times 1 - q'(n), and the Moon's (13.17639871°
         / 24) less q'(n) times the hourly motion in anomaly (13.06498287° / 24), where q is the equation of the
         eccentre (e = 2;4,45) or of the epicycle (r = 5;15) and q'(n) = e (e + cos n) / (1 + 2 e cos n + e^2);
         the increments are n″ for n degrees.
  p. 89  correction: the portions are 60′ times (d(0) - d(n)) / (d(0) - d(180)), d(n) the Moon's distance with the
         epicycle at the apogee of the eccentre (60 and 5;15); the values at odd multiples of 6° are the means of their
         neighbours. Epicycle: 12 times the same fraction; eccentre: 32 times the fraction of the distance of the
         centre of the epicycle (eccentricity 10;19) at the double elongation n. Areas: the part of the disc covered
         when d twelfths of its diameter are covered, the occulting disc equal (Sun) or of 2 3/5 radii (the shadow,
         Moon). Inclinations: sin i = 1 - d / D (D = 12.4 for the Sun, 21.6 for the Moon), and at the end of the
         immersion sin i = (3.6 - d / 6) / 1.6.
  p. 90  the latitude falls from S = r_u + r_m by 2 r_m / 12 a digit; incidence sqrt(S^2 - b^2), less the half
         duration sqrt((r_u - r_m)^2 - b^2) once the eclipse is total (S and r_m from the first row and from the
         latitude of 12 digits: 53′ and 14′ 45″; 63′ 36″ and 17′ 40″); the last row is the latitude 0.
  p. 91  the latitude falls from S = r_s + r_m by 2 r_s / 12, r_s = 16′ 15″ (the stated interval 2′ 42″ 30‴);
         incidence sqrt(S^2 - b^2).
  texts  the eclipse limits of p. 88 against those of p. 32, and the Arabic numbers (Maghribi abjad) against the Latin;
         the intervals under pp. 90-91 against their Arabic and against the latitude columns.
A value off by more than the tolerance of its column is listed (consecutive ones in the same direction as one entry)
and must be in ecl_discrepancies.tsv; the cells that Nallino emends (Part II p. 231) need entries of kind «noted».
--list shows the ledgered entries too. Exit code 1 on anything open."""
import csv, math, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
E_SUN = (2 + 4 / 60 + 45 / 3600) / 60
R_EPI = 5.25 / 60
E_ECC = (10 + 19 / 60) / 60
V_SUN, V_MOON, V_ANOM = (0.98565176 / 24 * 3600, 13.17639871 / 24 * 3600, 13.06498287 / 24 * 3600)
NOTED = ["p. 89 correction 18 portion", "p. 88 limits 191° 16′", "p. 88 limits 348° 44′"]
ABJAD = dict(zip("ابجدهوزحطيكلمنصعفضقرستثخذظغش",
                 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800,
                  900, 1000]))                                   # Maghribi order (ص 60, ض 90, س 300, ش 1000)


def read(name):
    return list(csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t"))


def dq(n, e):
    c = math.cos(math.radians(n))
    return e * (e + c) / (1 + 2 * e * c + e * e)


def dist(n):
    return math.sqrt(60 ** 2 + 5.25 ** 2 + 2 * 60 * 5.25 * math.cos(math.radians(n)))


def fraction(n):
    return (dist(0) - dist(n)) / (dist(0) - dist(180))


def eccentre(n):
    m, e = math.radians(n), E_ECC
    rho = e * math.cos(m) + math.sqrt((1 - e) ** 2 - (e * math.sin(m)) ** 2)
    return 32 * (1 - rho) / (2 * e)


def overlap(R, r, s):
    if s >= R + r:
        return 0.0
    if s <= abs(R - r):
        return math.pi * min(R, r) ** 2
    a = R * R * math.acos((s * s + R * R - r * r) / (2 * s * R))
    b = r * r * math.acos((s * s + r * r - R * R) / (2 * s * r))
    return a + b - 0.5 * math.sqrt((-s + R + r) * (s + R - r) * (s - R + r) * (s + R + r))


def area(d, ratio):
    return 12 * overlap(1, ratio, 1 + ratio - d / 6) / math.pi


def asind(x):
    return math.degrees(math.asin(max(0.0, min(1.0, x))))


def ms(x, unit="′"):
    """seconds -> «a′ b″» (unit ′) or minutes of a digit -> «aᵈ b′»"""
    if unit == "dig":
        return f"{int(x // 60)}ᵈ {x % 60:.1f}′"
    return f"{int(x // 60)}′ {x % 60:.1f}″"


def dms(x):
    """digits -> «aᵈ b′ c″»"""
    s = round(x * 3600)
    return f"{s // 3600}ᵈ {s // 60 % 60}′ {s % 60}″"


def abjad(word):
    return 0 if word == "{0}" else sum(ABJAD[ch] for ch in word)


found, printed, model, agree = [], {}, {}, [0]


def report(prefix, items, tol, fmt):
    """items: (label, printed units, expected units, printed text, key suffix); runs of values off by more than tol in
    the same direction form one entry; NOTED cells are left to the ledger"""
    run = []

    def close():
        if run:
            a, b = run[0][0], run[-1][0]
            worst = max(run, key=lambda x: abs(x[2]))
            found.append((f"{prefix.format(a + ('-' + b if b != a else ''))}", ", ".join(x[1] for x in run),
                           f"computed {', '.join(fmt(x[3]) for x in run)}; the largest departure {worst[2]:+.1f} at {worst[0]}"))
            run.clear()
    for label, p, e, text in items:
        key = prefix.format(label)
        printed[key], model[key] = text, e
        dev = p - e
        if key in NOTED:
            close(); continue
        if abs(dev) > tol:
            if run and (dev > 0) != (run[-1][2] > 0):
                close()
            run.append((label, text, dev, e))
        else:
            close(); agree[0] += 1
    close()


# p. 88
M = read("motions_p2.tsv")
H = [r for r in M if r["table"] == "hourly"]
for col, f in (("sun", lambda n: V_SUN * (1 - dq(n, E_SUN))), ("moon", lambda n: V_MOON - dq(n, R_EPI) * V_ANOM)):
    report("p. 88 hourly {} " + col, [(r["arg"], int(r[col + "_1"]) * 60 + int(r[col + "_2"]), f(int(r["arg"])),
                                       f"{r[col + '_1']}′ {r[col + '_2']}″") for r in H], 2, ms)
    for r in H:
        assert int(r["arg"]) + int(r["arg2"]) == 360
report("p. 88 increments {}", [(r["arg"], int(r["inc_1"]) * 60 + int(r["inc_2"]), int(r["arg"]), f"{r['inc_1']}′ {r['inc_2']}″")
                                for r in M if r["table"] == "increments"], 0, ms)

# p. 89: correction
C = read("correction_p2.tsv")
por = {0: 0, **{int(r["arg"]): int(r["portion_1"]) * 60 + int(r["portion_2"]) for r in C}}
txt = {int(r["arg"]): f"{r['portion_1']}′ {r['portion_2']}″" for r in C}
report("p. 89 correction {} portion", [(str(n), por[n], 3600 * fraction(n), txt[n]) for n in range(12, 181, 12)], 5, ms)
report("p. 89 correction {} portion", [(str(n), por[n], (por[n - 6] + por[n + 6]) / 2, txt[n]) for n in range(6, 180, 12)], 0.5,
       ms)
for col, f in (("epicycle", lambda n: 12 * fraction(n)), ("eccentre", eccentre)):
    report("p. 89 correction {} " + col, [(r["arg"], int(r[col]), f(int(r["arg"])), r[col] + "′") for r in C], 1,
           lambda x: f"{x:.2f}′")
    for r in C:
        assert int(r["arg"]) + int(r["arg2"]) == 360

# p. 89: areas and inclinations
G = read("digits_p2.tsv")
A = [r for r in G if r["table"] == "areas"]
for col, ratio in (("sun", 1.0), ("moon", 2.6)):
    report("p. 89 areas {} " + col, [(r["arg"], int(r[col + "_1"]) * 60 + int(r[col + "_2"]), 60 * area(int(r["arg"]), ratio),
                                      f"{r[col + '_1']}ᵈ {r[col + '_2']}′") for r in A], 5, lambda x: ms(x, "dig"))
I = [r for r in G if r["table"] == "inclinations"]
dg = lambda r: 21.6 if r["arg"] == "compl." else int(r["arg"])
for col, f in (("sun_incl", lambda d: asind(1 - d / 12.4)), ("moon_begin", lambda d: asind(1 - d / 21.6)),
               ("moon_end", lambda d: asind((3.6 - d / 6) / 1.6) if 12 <= d < 21.6 else 0.0)):
    report("p. 89 inclinations {} " + col, [(r["arg"], int(r[col]), f(dg(r)), r[col] + "°") for r in I], 1, lambda x: f"{x:.2f}°")

# pp. 90-91
E = read("eclipses_p2.tsv")


def label(r, R):
    return r["digits"] if r is not R[-1] else "end"


def dtol(s):
    """seconds of a digit: 3 when the seconds are printed, else half a minute and 3"""
    return 3 if len(s.split()) == 3 else 33


def digits_value(s):
    p = [int(x) for x in s.split()]
    return p[0] + (p[1] / 60 if len(p) > 1 else 0) + (p[2] / 3600 if len(p) > 2 else 0)


params = {}
for table, pp in (("lunar_max", "90"), ("lunar_min", "90")):
    R = [r for r in E if r["table"] == table]
    u = lambda r, c: int(r[c + "_1"]) * 60 + int(r[c + "_2"])
    S = u(R[0], "lat") / 60
    rm = (S - u(R[12], "lat") / 60) / 2                       # 12 digits: the latitude is r_u - r_m
    ru = S - rm
    params[table] = (S, rm, ru)
    lat, inc, mora = [], [], []
    for r in R[:-1]:
        d = int(r["digits"])
        b = S - d * 2 * rm / 12
        tot = math.sqrt(max(0.0, (ru - rm) ** 2 - b * b)) if b < ru - rm else 0.0
        lat.append((r["digits"], u(r, "lat"), 60 * b, f"{r['lat_1']}′ {r['lat_2']}″"))
        inc.append((r["digits"], u(r, "inc"), 60 * (math.sqrt(S * S - b * b) - tot), f"{r['inc_1']}′ {r['inc_2']}″"))
        mora.append((r["digits"], u(r, "mora"), 60 * tot, f"{r['mora_1']}′ {r['mora_2']}″"))
    end = R[-1]
    lat.append(("end", u(end, "lat"), 0, f"{end['lat_1']}′ {end['lat_2']}″"))
    inc.append(("end", u(end, "inc"), 60 * 2 * rm, f"{end['inc_1']}′ {end['inc_2']}″"))
    mora.append(("end", u(end, "mora"), 60 * (ru - rm), f"{end['mora_1']}′ {end['mora_2']}″"))
    for name, items in (("lat", lat), ("inc", inc), ("mora", mora)):
        report(f"p. {pp} {table} {{}} {name}", items, 3, ms)
    report(f"p. {pp} {table} {{}} digits", [("end", digits_value(end["digits"]) * 3600, 12 * S / (2 * rm) * 3600,
                                            dms(digits_value(end["digits"])))], dtol(end["digits"]), lambda x: dms(x / 3600))
for table, pp in (("solar_max", "91"), ("solar_min", "91")):
    R = [r for r in E if r["table"] == table]
    u = lambda r, c: int(r[c + "_1"]) * 60 + int(r[c + "_2"])
    S = u(R[0], "lat") / 60
    rs = 16.25
    params[table] = (S, S - rs, rs)
    lat, inc = [], []
    for r in R:
        d = int(r["digits"]) if r is not R[-1] else 12 * S / (2 * rs)
        b = S - d * 2 * rs / 12
        lat.append((label(r, R), u(r, "lat"), 60 * b, f"{r['lat_1']}′ {r['lat_2']}″"))
        inc.append((label(r, R), u(r, "inc"), 60 * math.sqrt(max(0.0, S * S - b * b)), f"{r['inc_1']}′ {r['inc_2']}″"))
    report(f"p. {pp} {table} {{}} lat", lat, 3, ms)
    report(f"p. {pp} {table} {{}} inc", inc, 3, ms)
    report(f"p. {pp} {table} {{}} digits", [("end", digits_value(R[-1]["digits"]) * 3600, 12 * S / (2 * rs) * 3600,
                                            dms(digits_value(R[-1]["digits"])))], dtol(R[-1]["digits"]), lambda x: dms(x / 3600))

# texts: the eclipse limits; the intervals under pp. 90-91
T = {r["item"]: r["text"] for r in read("ecl_text.tsv")}
x32 = {r["item"]: r["text"] for r in read("../syzygies/syz_extra.tsv")}
nums = lambda s: re.findall(r"(\d+)°(?: (\d+)′)?", s)
for body in ("sun", "moon"):
    la = [(int(a), int(b or 0)) for a, b in nums(T[f"limits_la_{body}"])]
    p32 = [(int(a), int(b or 0)) for a, b in nums(x32[f"eclipse_{body}"])]
    if la != p32:
        found.append((f"p. 88 limits {body} = p. 32", str(la), f"p. 32: {p32}"))
    words = T[f"limits_ar_{body}"].split()
    words = words[words.index("من"):]                       # the ranges: من A B الى C D ومن ... الى تمام سص فانه
    ar, cur = [], []
    for w in words:
        if w in ("من", "ومن", "الى", "فانه"):
            if cur:
                ar.append(tuple(abjad(x) for x in cur) + (0,) * (2 - len(cur)))
            cur = []
            if w == "فانه":
                break
            continue
        if w != "تمام":
            cur.append(w)
    if ar != la:
        found.append((f"p. 88 limits {body}: Arabic = Latin", str(ar), f"Latin: {la}"))
    for a, b in la:
        printed[f"p. 88 limits {a}° {b}′"] = f"{a}° {b}′"
pages = {r["table"]: r for r in read("ecl_pages.tsv")}
for table in ("lunar_max", "lunar_min", "solar_max", "solar_min"):
    pg = pages[table]
    la = tuple(int(x) for x in re.findall(r"\d+", pg["footer_la"].split("intervallum")[1]))
    ar = tuple(abjad(w) for w in pg["footer_ar"].split()[1:])
    if la != ar:
        found.append((f"p. {pg['ppage']} {table} interval: Arabic = Latin", str(ar), f"Latin: {la}"))
    S, a, b = params[table]
    step = 2 * (a if table.startswith("lunar") else b) / 12 * 3600            # thirds of a degree a digit
    stated = ((la[1] * 60 + la[2]) * 60 + la[3])
    key = f"p. {pg['ppage']} {table} interval"
    printed[key] = f"{la[0]}° {la[1]}′ {la[2]}″ {la[3]}‴"
    if abs(stated - step) > 1:
        found.append((key, printed[key], f"the latitude column falls by {int(step // 3600)}′ {int(step // 60 % 60)}″ "
                                          f"{step % 60:.0f}‴ a digit"))
    else:
        agree[0] += 1


def main():
    ledger_rows = read("ecl_discrepancies.tsv")
    ledger = {r["where"] for r in ledger_rows if r["kind"] != "noted"}
    noted = {r["where"]: r for r in ledger_rows if r["kind"] == "noted"}
    problems = []
    for wh in NOTED:
        if wh not in noted:
            problems.append(f"no ledger entry for the cell Nallino emends: {wh} (printed {printed.get(wh)})")
        elif noted[wh]["printed"] != printed.get(wh):
            problems.append(f"{wh}: the ledger says printed {noted[wh]['printed']}, the edition has {printed.get(wh)}")
    for wh in noted:
        if wh not in NOTED:
            problems.append(f"ledger entry of kind «noted» not among Nallino's emendations: {wh}")
    open_ = [f for f in found if f[0] not in ledger]
    print(f"values within tolerance {agree[0]}, differ {len(found)} (ledgered {len(found) - len(open_)}, open {len(open_)}); "
          f"Nallino's emendations {len(NOTED)}, problems {len(problems)}")
    print("  " + "; ".join(f"{t}: S {s * 60:.0f}″, {'r_m ' + format(a * 60, '.0f') + '″, r_u ' + format(b * 60, '.0f') + '″' if t.startswith('lunar') else 'r_m ' + format(a * 60, '.0f') + '″, r_s ' + format(b * 60, '.0f') + '″'}"
                       for t, (s, a, b) in params.items()))
    for where, p, e in (found if "--list" in sys.argv else open_):
        print(f"  {where}: {p}; {e}" + ("" if where in ledger else "   << not in the ledger"))
    for p in problems:
        print("  " + p)
    stale = [w for w in ledger if w not in {f[0] for f in found}]
    for w in stale:
        print("  ledger entry without a difference:", w)
    sys.exit(1 if open_ or stale or problems else 0)


if __name__ == "__main__":
    main()

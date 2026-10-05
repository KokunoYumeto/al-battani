"""Write S06/syzygies/rsyz_discrepancies.tsv: the differences found by check_roman_syzygies.py (Part II pp. 84-87),
each confirmed on the scan, and the cells that Nallino emends in his notes (Part II p. 230). The numbers in the notes
are computed here from rsyz_p2.tsv and syz_p2.tsv; the codex readings are those Nallino reports."""
import csv, math
from collections import Counter
from pathlib import Path

import check_roman_syzygies as c

HERE = Path(__file__).resolve().parent
res = c.compute()
T, M, P = res["T"], res["model"], res["printed"]
F = {f[0]: f for f in res["found"]}
L84 = res["lines84"]
DEG, L, LS, sx, show, u = c.DEG, c.L, c.LS, c.sx, c.show, c.u
half = T["parts"][0]


def row(table, arg):
    return next(r for r in T[table] if r["arg"].split()[0] == str(arg))


def key(table, arg, g):
    return f"p. {row(table, arg)['ppage']} {table} {arg} {g}"


def for_(printed, computed):
    """«247° 3′ 0″», «247° 3′ 51″» -> «0″ for 51″» (the places that differ)"""
    a, b = printed.split(), computed.split()
    return " ".join(x for x, y in zip(a, b) if x != y) + " for " + " ".join(y for x, y in zip(a, b) if x != y)


def sign(arg):
    """+1 when the opposition of p. 85 precedes the conjunction of p. 84 (p. 85 = p. 84 less half a lunation)"""
    return 1 if u(row("opp", arg), "day") < u(row("conj", arg), "day") else -1


def secs(x, places=1):
    t = f"{x:+.{places}f}″"
    return t[1:] if float(t[:-1]) == 0 else t


def words(xs):
    xs = [str(x) for x in xs]
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


NUM = {1: "one", 2: "two", 3: "three"}


entries = []

# p. 84, 1623: the argument of latitude
w = key("conj", 1623, "lat")
alt = (u(row("opp", 1623), "lat") + sign(1623) * u(half, "lat")) % DEG
entries.append((w, P[w], sx(M[w], "lat", 0), "value",
                f"{for_(P[w], sx(M[w], 'lat', 0))}: the line of the column gives {sx(M[w], 'lat')}, and the argument of "
                f"latitude of p. 85 ({show(row('opp', 1623), 'lat')}) {'plus' if sign(1623) > 0 else 'less'} that of half "
                f"a lunation ({show(half, 'lat')}, p. 87) gives {sx(alt, 'lat', 0)}"))

# p. 85, 1623: the day
w = key("opp", 1623, "day")
alt = u(row("conj", 1623), "day") - sign(1623) * u(half, "day")
entries.append((w, P[w], sx(M[w], "day", 0), "value",
                f"{for_(P[w], sx(M[w], 'day', 0))}: the line of the column gives {sx(M[w], 'day')}, and the day of p. 84 "
                f"({show(row('conj', 1623), 'day')}) {'less' if sign(1623) > 0 else 'plus'} half a lunation "
                f"({show(half, 'day')}, p. 87) gives {sx(alt, 'day', 0)}"))

# pp. 84-85: stretches in which p. 84 less p. 85 departs from half a lunation
args = [r["arg"] for r in T["conj"]]
pair_keys = [k for k in F if k.endswith("(p. 84 less p. 85)")]
in_runs = set()
for k in pair_keys:
    a, b = k.split()[3].split("-")
    in_runs |= set(args[args.index(a):args.index(b) + 1])


def wraps(table):
    """rows at which the day drops a lunation, with the longitude of the lunation subtracted there"""
    R = T[table]
    steps = [((u(y, "lum") - u(x, "lum")) % DEG, u(y, "day") < u(x, "day"), y["arg"]) for x, y in zip(R, R[1:])]
    plain = Counter(s for s, wr, _ in steps if not wr).most_common(1)[0][0]
    return {a: (plain - s) % DEG for s, wr, a in steps if wr}, plain


w84, plain84 = wraps("conj")
w85, _ = wraps("opp")
others = sorted({sx(sign(a) * (u(row("conj", a), "lum") - u(row("opp", a), "lum")), "lum", 0)
                 for a in args if a not in in_runs})
for k in pair_keys:
    a, b = k.split()[3].split("-")
    rr = args[args.index(a):args.index(b) + 1]
    comp = [sx(u(row("conj", x), "lum") - sign(x) * u(half, "lum"), "lum", 0) for x in rr]
    r84 = [c.centred(u(row("conj", x), "lum") - M[key("conj", x, "lum")], DEG) for x in rr]
    r85 = [c.centred(u(row("opp", x), "lum") - M[key("opp", x, "lum")], DEG) for x in rr]
    nxt = min(x for x in w85 if args.index(x) > args.index(b))
    groups = {}
    for x, v in w84.items():
        if x != a:
            groups.setdefault(sx(v, "lum", 0), []).append(x)
    elsewhere = [f"{v} at {words(xs)}" for v, xs in groups.items()]
    entries.append((k, F[k][1], ", ".join(comp), "run",
                    f"p. 84 less p. 85 is {F[k][2].split(' is ')[1].split(',')[0]} in these rows, and "
                    f"{' or '.join(others)} in all the others; half a lunation is {show(half, 'lum')} (p. 87). The "
                    f"longitudes of both pages lie within 2″ of their lines here (p. 84 {', '.join(secs(x) for x in r84)}; "
                    f"p. 85 {', '.join(secs(x) for x in r85)}). The rows run from a lunation subtracted on p. 84, at {a}, "
                    f"with a longitude of {sx(w84[a], 'lum', 0)} (elsewhere {', '.join(elsewhere)}), to the next one "
                    f"subtracted on p. 85, at {nxt}"))

# p. 86: the longitude of years 8-12
k = "p. 86 single 8-12 lum"
dev = {int(r["arg"]): c.centred(u(r, "lum") - M[key("single", r["arg"], "lum")], DEG) for r in T["single"]}
p32 = {int(r["arg"]): r for r in c.read("syz_p2.tsv") if r["table"] == "single"}
same = [n for n in range(1, 25) if math.ceil(365 * n / L) == math.ceil((365 * n + n // 4) / L)]
d32 = {n: c.centred(u(row("single", n), "lum") - u(p32[n], "lum"), DEG) for n in same}
up = [n for n in range(6, 13) if n in same]
rest = [d32[n] for n in same if n not in up]
entries.append((k, F[k][1], ", ".join(sx(M[key("single", n, "lum")], "lum") for n in range(8, 13)), "run",
                f"the departures from the line of the column rise from {secs(dev[6])} in year 6 to {secs(dev[12])} in "
                f"year 12 ({', '.join(secs(dev[n]) for n in range(6, 13))}), and lie between {secs(min(dev[n] for n in range(13, 25)))} "
                f"and {secs(max(dev[n] for n in range(13, 25)))} in years 13-24. Where p. 86 and p. 32 (the Egyptian years) "
                f"hold the same number of lunations, every year but {', '.join(str(n) for n in range(1, 25) if n not in same).replace(', ', ' and ')}, "
                f"p. 86 less p. 32 is {', '.join(secs(d32[n], 0) for n in up)} in years {words(up)}, "
                f"and between {secs(min(rest), 0)} and {secs(max(rest), 0)} in the others. Nallino, Part II p. 230: the seconds of "
                f"this column differ by about 2″ from those of p. 32; al-Battānī appears to have computed it anew, perhaps "
                f"with a very slightly different daily motion of the elongation"))

# p. 87 against p. 31
for k in [k for k in F if k.endswith("= p. 31")]:
    table, arg, g = k.split()[2], k.split()[3], k.split()[4]
    other = F[k][2].split(" on p. 31")[0]
    what = {"parts": "a quarter of a lunation is", "months": "three lunations give"}[table]
    entries.append((k, f"{F[k][1]} (p. 87)", f"{other} (p. 31)", "identity",
                    f"{what} {sx(M[key(table, arg, g)], g, 2)}; Nallino, Part II p. 206, notes this difference between the "
                    f"two tables"))

# p. 87, intervals: the longitude of 480 years
k = "p. 87 intervals 480 lum"
R = T["conj"]
plain_lum = [(u(y, "lum") - u(x, "lum")) % DEG for x, y in zip(R, R[1:]) if u(y, "day") > u(x, "day")]
step = Counter(plain_lum).most_common(1)[0][0]
W = res["intervals_w"]
rule = {r["arg"]: (int(r["arg"]) // 24 * step - W[r["arg"]] * L84["lum"]) % DEG for r in T["intervals"]}
fit = max(abs(c.centred(u(r, "lum") - rule[r["arg"]], DEG)) for r in T["intervals"])
how_many = (f"all {len(plain_lum)}" if plain_lum.count(step) == len(plain_lum)
            else f"{plain_lum.count(step)} of the {len(plain_lum)}")
entries.append((k, P[k], sx(M[k], "lum", 0), "value",
                f"{297 * 20 - W['480']} lunations (297 × 20 less the {W['480']} that the day drops) give {sx(M[k], 'lum')}. "
                f"The longitude of p. 84 advances by {sx(step, 'lum', 0)} in {how_many} steps between rows without a "
                f"subtracted lunation; 20 such steps less {W['480']} lunations of {sx(L84['lum'], 'lum', 2)} give "
                f"{sx(rule['480'], 'lum')}, and this rule gives all seven longitudes of the intervals within {fit:.1f}″"))

# p. 87, intervals: the argument of latitude
def lat_of(n):
    return (n * L84["lat"]) % DEG


k = "p. 87 intervals 192 lat"
m, w_ = 8, W["192"]
entries.append((k, P[k], sx(M[k], "lat", 0), "value",
                f"the printed value is the motion of {297 * m} lunations (297 × {m}; {sx(lat_of(297 * m), 'lat')}). The day "
                f"({show(row('intervals', 192), 'day')}) drops {NUM[w_]} lunation, and the longitude and the anomaly drop its "
                f"motions ({297 * m - w_} lunations); reduced in the same way, the argument of latitude is "
                f"{sx(M[k], 'lat')}. Nallino's notes do not mention this cell; see the entries for 288, 384 and 480 years"))

NOTE = {
    "p. 86 single 6 day": None,
    "p. 87 intervals 72 lat": ("52″ for 54″", "the codex has 6″ (و)"),
    "p. 87 intervals 288 anom": ("184° (قفد) for 189° (قفط)", None),
    "p. 87 intervals 288 lat": ("51′ for 56′", "the codex has 18′ (يح)"),
    "p. 87 intervals 384 lat": ("275° 48′ 22″ for 306° 28′ 36″", "the codex has 275° 4′ 10″"),
    "p. 87 intervals 480 lat": ("321° 45′ 17″ for 23° 5′ 45″", "the codex has 291° 0′ 40″"),
}
SCHIA = {"p. 87 intervals 288 lat": "229° 51′ 27″", "p. 87 intervals 384 lat": "275° 48′ 22″",
         "p. 87 intervals 480 lat": "321° 45′ 17″"}


def to_units(s):
    a, b, d = (int("".join(ch for ch in x if ch.isdigit())) for x in s.split())
    return (a * 60 + b) * 60 + d


# p. 86, year 6: the day
k = "p. 86 single 6 day"
n = 6
D6 = 365 * n + n // 4
k6 = math.ceil(D6 / L)
exact = (k6 * L - D6) * 3600
rule6 = u(row("single", 5), "day") + (18 * 60 + 53) * 60 + 52
entries.append((k, P[k], sx(M[k], "day", 0), "noted",
                f"Nallino, Part II p. 230: «pro 40″, ut impressum est, restituatur 50″». Year 6 holds {k6} lunations, and "
                f"{k6} × 29;31,50,8,20 - {D6} days = {sx(exact, 'day')}; the rule of the same note, year 5 "
                f"({show(row('single', 5), 'day')}) plus 18ᵈ 53′ 52″, gives {sx(rule6, 'day', 0)}. Both support the printed "
                f"40″. On p. 207 Nallino corrects the same seconds in the table of Egyptian years (p. 32, year 6) the other "
                f"way: 40″ for 50″"))

for k in [k for k in NOTE if "intervals" in k]:
    arg, g = k.split()[3], k.split()[4]
    m, w_ = int(arg) // 24, W[arg]
    reading, codex = NOTE[k]
    rate = L84[g]
    text = f"Nallino, Part II p. 230, after Schiaparelli: {reading}" + (f"; {codex}" if codex else "") + ". "
    if g == "anom" or w_ == 0:
        text += f"{297 * m - w_} lunations (297 × {m}" + (f" less the {w_} that the day drops" if w_ else "") + \
                f") give {sx(M[k], g)}"
    else:
        s = to_units(SCHIA[k])
        ns = round(c.centred(s - lat_of(297 * m), DEG) / rate)
        printed_is = round(c.centred(to_units(P[k]) - lat_of(297 * m), DEG) / rate)
        dp = abs(c.centred(to_units(P[k]) - lat_of(297 * m + printed_is), DEG))
        if ns == printed_is:
            text += (f"Schiaparelli's reading, {SCHIA[k]}, is the motion of {297 * m + ns} lunations (297 × {m}; "
                     f"{sx(lat_of(297 * m + ns), 'lat')}), from which the printed value differs in the minutes. ")
        else:
            text += (f"The printed value {'is' if dp <= c.TOL else 'is near'} the motion of {297 * m + printed_is} lunations "
                     f"(297 × {m}" + (f" less {-printed_is}" if printed_is else "") + f"; {sx(lat_of(297 * m + printed_is), 'lat')}), "
                     f"Schiaparelli's reading that of {297 * m + ns} ({sx(lat_of(297 * m + ns), 'lat')}). ")
        text += (f"The day ({show(row('intervals', arg), 'day')}) drops {NUM[w_]} lunation{'s' if w_ > 1 else ''}, and the "
                 f"longitude and the anomaly drop their motions ({297 * m - w_} lunations), which give {sx(M[k], 'lat')} "
                 f"for the argument of latitude")
    entries.append((k, P[k], sx(M[k], g, 0), "noted", text))

with open(HERE / "rsyz_discrepancies.tsv", "w", encoding="utf-8", newline="") as f:
    wr = csv.writer(f, delimiter="\t", lineterminator="\n")
    wr.writerow(["where", "printed", "computed", "kind", "note"])
    wr.writerows(entries)
print(len(entries), "ledger rows")

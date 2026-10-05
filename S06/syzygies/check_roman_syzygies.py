"""Check of Nallino's Part II pp. 84-87 (mean syzygies in Roman years), from rsyz_p2.tsv. Every number has three
sexagesimal places (days ; ′ ″ or degrees ° ′ ″) and is compared in units of its last place; L = 29;31,50,8,20 days.
  pp. 84-85  collected years 879, 903 ... 1623: each row adds about 4d 35′ 11″ to the day and the motions of that
             interval; when the day passes a lunation, a lunation and its motions are subtracted (Nallino, Part II
             p. 230). So the day is a line in the period number k modulo L, and each motion is a line in the number of
             lunations N = 297 k - (lunations subtracted so far). Each row of p. 84 less the row of p. 85 is half a
             lunation (p. 87, «Dimidium mensis»), in the direction in which the opposition falls.
  p. 86      single years 1-24: year n holds k lunations, the least number that exceeds D = 365 n + [n/4] days; the
             day is k L - D, and each motion is a line in k.
  p. 87      the months are m times the motion in one lunation of p. 84 (and m L days), the parts of a month 1/2, 1/3,
             1/4 and 1/6 of it (whole revolutions included); both are compared with the same tables of p. 31. The
             intervals of 24 m years: the day is m times the period of p. 84 less the lunations it passes, w, and each
             motion is that of 297 m - w lunations.
A value off its line by more than 3 units of its last place is listed (consecutive ones in the same direction as one
entry) and must be in rsyz_discrepancies.tsv; the cells that Nallino emends (Part II p. 230) need entries of kind
«noted» that give the printed and the computed value. --list shows the ledgered entries too. Exit code 1 on anything
open."""
import csv, math, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
G = ["day", "lum", "anom", "lat"]
TOL = 3
DEG = 360 * 3600
L = 29 + 31 / 60 + 50 / 3600 + 8 / 216000 + 20 / 12960000
LS = L * 3600                                             # one lunation in seconds of a day
NOTED = ["p. 86 single 6 day", "p. 87 intervals 72 lat", "p. 87 intervals 288 anom", "p. 87 intervals 288 lat",
         "p. 87 intervals 384 lat", "p. 87 intervals 480 lat"]
TURNS = {"day": 0, "lum": 0, "anom": 1, "lat": 1}       # whole revolutions in one lunation


def read(name):
    return list(csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t"))


def u(r, g):
    return (int(r[g + "_1"]) * 60 + int(r[g + "_2"])) * 60 + int(r[g + "_3"])


def show(r, g):
    a, b, c = r[g + "_1"], r[g + "_2"], r[g + "_3"]
    return f"{a}ᵈ {b}′ {c}″" if g == "day" else f"{a}° {b}′ {c}″"


def sx(x, g, places=1):
    """seconds -> «a° b′ c.c″» (days: «aᵈ b′ c.c″»); places=0 rounds to the second"""
    x = round(x % (DEG if g != "day" else 10 ** 9), places)
    s = f"{x % 60:.{places}f}"
    return (f"{int(x // 3600)}ᵈ " if g == "day" else f"{int(x // 3600)}° ") + f"{int(x // 60 % 60)}′ {s}″"


def centred(x, mod):
    return (x + mod / 2) % mod - mod / 2


def fit_line(t, v, mod, rate):
    """least-squares line a + b t through v (modulo mod), from the given rate; refitted on the points near it"""
    t = np.array(t, float); v = np.array(v, float)
    b = rate
    unw = v[0] + centred(v - v[0] - b * (t - t[0]), mod) + b * (t - t[0])
    a = np.median(unw - b * t)
    for band in (mod / 8, 600, 60, 10, TOL, TOL):
        unw = v + mod * np.round(((a + b * t) - v) / mod)
        keep = np.abs(unw - (a + b * t)) <= band
        if keep.sum() >= 3:
            b, a = np.polyfit(t[keep], unw[keep], 1)
    return a, b


def compute():
    rows = read("rsyz_p2.tsv")
    T = {t: [r for r in rows if r["table"] == t] for t in ("conj", "opp", "single", "parts", "months", "intervals")}
    found, printed, model, agree = [], {}, {}, [0]

    def key(table, r, g):
        return f"p. {r['ppage']} {table} {r['arg'].split()[0]} {g}"

    def report(table, g, expected):
        """list runs of values off by more than TOL in the same direction; the cells of NOTED are left to the ledger"""
        run = []

        def close():
            if run:
                a, b = run[0][0], run[-1][0]
                worst = max(run, key=lambda x: abs(x[2]))
                found.append((f"p. {T[table][0]['ppage']} {table} {a}" + (f"-{b}" if b != a else "") + f" {g}",
                               ", ".join(x[1] for x in run),
                               f"{len(run)} value{'s' if len(run) > 1 else ''} {'above' if worst[2] > 0 else 'below'} "
                               f"the line, the largest by {worst[2]:+.1f} at {worst[0]}"))
                run.clear()
        for r, e in zip(T[table], expected):
            where = key(table, r, g)
            printed[where], model[where] = show(r, g), e
            dev = centred(u(r, g) - e, DEG if g != "day" else 10 ** 9)
            if where in NOTED:
                close(); continue
            if abs(dev) > TOL:
                if run and (dev > 0) != (run[-1][2] > 0):
                    close()
                run.append((r["arg"].split()[0], show(r, g), dev))
            else:
                close(); agree[0] += 1
        close()

    # pp. 84-85: the day a line in k modulo L; the motions lines in N = 297 k - w
    PER_LUN = {"lum": 104784.78, "anom": 92940.14, "lat": 110414.0}      # starting rates, seconds per lunation
    lines84 = {}
    for table in ("conj", "opp"):
        R = T[table]
        k = list(range(len(R)))
        a, b = fit_line(k, [u(r, "day") for r in R], LS, (297 * L - 8766) * 3600)
        report(table, "day", [(a + b * kk) % LS for kk in k])
        w = [int((a + b * kk) // LS) for kk in k]           # lunations subtracted so far, from the line of the day
        N = [297 * kk - ww for kk, ww in zip(k, w)]
        if table == "conj":
            lines84["day"] = b
        for g in ("lum", "anom", "lat"):
            a2, b2 = fit_line(N, [u(r, g) for r in R], DEG, PER_LUN[g])
            report(table, g, [(a2 + b2 * n) % DEG for n in N])
            if table == "conj":
                lines84[g] = b2

    # p. 84 less p. 85: half a lunation (p. 87, «Dimidium mensis»), unless one of the two cells is off its line;
    # consecutive rows off by more than 1″ in the same direction form one entry
    half = T["parts"][0]
    off = {f[0] for f in found}
    for g in G:
        mod = LS * 2 if g == "day" else DEG
        run = []

        def flush():
            if run:
                a, b = run[0][0], run[-1][0]
                found.append((f"p. 85 opp {a}" + (f"-{b}" if b != a else "") + f" {g} (p. 84 less p. 85)",
                              ", ".join(x[1] for x in run), "p. 84 less p. 85 is " + ", ".join(x[3] for x in run)
                              + f"; half a lunation {show(half, g)}"))
                run.clear()
        for rc, ro in zip(T["conj"], T["opp"]):
            sign = 1 if u(ro, "day") < u(rc, "day") else -1   # the opposition before or after the conjunction
            diff = sign * (u(rc, g) - u(ro, g))
            dev = centred(diff - u(half, g), mod)
            if abs(dev) > 1 and not {key("conj", rc, g), key("opp", ro, g)} & off:
                if run and (dev > 0) != (run[-1][2] > 0):
                    flush()
                run.append((ro["arg"], show(ro, g), dev, sx(diff % mod, g, 0)))
            else:
                flush()
        flush()

    # p. 86: single years
    R = T["single"]
    ns = [int(r["arg"]) for r in R]
    D = [365 * n + n // 4 for n in ns]
    K = [math.ceil(d / L) for d in D]
    a, b = fit_line(K, [u(r, "day") + d * 3600 for r, d in zip(R, D)], 10 ** 12, LS)
    report("single", "day", [a + b * kk - d * 3600 for kk, d in zip(K, D)])
    for g in ("lum", "anom", "lat"):
        a2, b2 = fit_line(K, [u(r, g) for r in R], DEG, lines84[g])
        report("single", g, [(a2 + b2 * kk) % DEG for kk in K])

    # p. 87: the months and the parts of a month, from the motion in one lunation of p. 84
    one = {"day": LS, **{g: lines84[g] + TURNS[g] * DEG for g in ("lum", "anom", "lat")}}
    for table, fr in (("parts", [1 / 2, 1 / 3, 1 / 4, 1 / 6]), ("months", list(range(1, 13)))):
        for g in G:
            report(table, g, [(f * one[g]) % (DEG if g != "day" else 10 ** 9) for f in fr])
    p31 = [r for r in read("syz_p2.tsv") if r["table"] in ("parts", "months")]
    by_name = {"Dimidium": "Monsis", "Tertia": "Tertia", "Quarta": "Quarta", "Sexta": "Sexta"}
    p31_parts = {r["arg"].split()[0]: r for r in p31 if r["table"] == "parts"}
    pairs = [(r, p31_parts[by_name[r["arg"].split()[0]]], "parts") for r in T["parts"]]
    pairs += [(r, r31, "months") for r, r31 in zip(T["months"], [r for r in p31 if r["table"] == "months"])]
    for r, r31, table in pairs:
        for g in G:
            if u(r, g) != u(r31, g):
                found.append((f"{key(table, r, g)} = p. 31", show(r, g),
                              f"{show(r31, g)} on p. 31 ({r31['arg']}); {sx(model[key(table, r, g)], g)} computed"))

    # p. 87: intervals of 24 m years
    R = T["intervals"]
    ms = [int(r["arg"]) // 24 for r in R]
    w = [int(m * lines84["day"] // LS) for m in ms]
    report("intervals", "day", [m * lines84["day"] - ww * LS for m, ww in zip(ms, w)])
    for g in ("lum", "anom", "lat"):
        report("intervals", g, [((297 * m - ww) * lines84[g]) % DEG for m, ww in zip(ms, w)])
    return {"found": found, "agree": agree[0], "printed": printed, "model": model, "lines84": lines84, "T": T,
            "intervals_w": dict(zip([r["arg"] for r in R], w))}


def main():
    res = compute()
    found, printed, model = res["found"], res["printed"], res["model"]
    ledger_rows = read("rsyz_discrepancies.tsv")
    ledger = {r["where"] for r in ledger_rows if r["kind"] != "noted"}
    noted = {r["where"]: r for r in ledger_rows if r["kind"] == "noted"}
    problems = []
    for wh in NOTED:
        g = wh.split()[-1]
        if wh not in noted:
            problems.append(f"no ledger entry for the cell Nallino emends: {wh} (printed {printed.get(wh)}, "
                            f"computed {sx(model[wh], g, 0)})")
            continue
        if noted[wh]["printed"] != printed.get(wh):
            problems.append(f"{wh}: the ledger says printed {noted[wh]['printed']}, the table has {printed.get(wh)}")
        if noted[wh]["computed"] != sx(model[wh], g, 0):
            problems.append(f"{wh}: the ledger says computed {noted[wh]['computed']}, the line gives {sx(model[wh], g)}")
    for wh in noted:
        if wh not in NOTED:
            problems.append(f"ledger entry of kind «noted» not among Nallino's emendations: {wh}")
    open_ = [f for f in found if f[0] not in ledger]
    L84 = res["lines84"]
    print(f"values on their lines {res['agree']}, differ {len(found)} (ledgered {len(found) - len(open_)}, open "
          f"{len(open_)}); Nallino's emendations {len(NOTED)}, problems {len(problems)}")
    print(f"  period of p. 84: {L84['day'] / 3600:.6f} days ({sx(L84['day'], 'day', 2)}; 297 L - 8766 days = "
          f"{297 * L - 8766:.6f}); in one lunation: " + ", ".join(f"{g} {sx(L84[g], g, 2)}" for g in ("lum", "anom", "lat")))
    for where, p, e in (found if "--list" in sys.argv else open_):
        print(f"  {where}: {p}; {e}" + ("" if where in ledger else "   << not in the ledger"))
    for p in problems:
        print("  " + p)
    stale = [w_ for w_ in ledger if w_ not in {f[0] for f in found}]
    for w_ in stale:
        print("  ledger entry without a difference:", w_)
    sys.exit(1 if open_ or stale or problems else 0)


if __name__ == "__main__":
    main()

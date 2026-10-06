"""Check of Nallino's Part II pp. 93-94 (parallaxes of the Sun and the Moon in altitude), from parallax_p2.tsv. The
argument is the true zenith distance z = 2, 4 ... 90 (Nallino, Part II pp. 235-237).
  Sun, first term, second less first: tan p = sin pi sin z / (1 - sin pi cos z), sin pi = 1 / distance in Earth radii
      (the Sun 1210; the Moon 64;10 and 53;50, Ptolemy's first two terms); tolerance 3″.
  third term, fourth less third: the values at 90° are the horizontal parallaxes 79′ and 104′ less 79′; the columns
      grow by steps that never increase (by more than 1″) from one row to the next, and stand below the computation
      with those horizontal parallaxes by up to about a minute (al-Battānī's emendation of Ptolemy's numbers).
  sixtieths (epicycle with its centre at the apogee and at the perigee of the eccentre; argument half the true anomaly;
      eccentre, argument the mean elongation): computed at every 6° of z and divided in thirds between. A value at a
      multiple of 6° must lie within 5″ of the computation (60 times the fraction of the change of the distance:
      epicycle 5;15 about a centre at 60 or 39;22; eccentricity 10;19) unless the rows on both sides of it agree on
      another value; the rows between must lie within 1″ of the thirds. The epicycle column at the apogee must also
      equal the portions of p. 89 at twice the argument (S06/eclipses/correction_p2.tsv).
A value off by more than its tolerance is listed and must be in par_discrepancies.tsv. --list shows the ledgered
entries too. Exit code 1 on anything open."""
import csv, math, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
R_EPI = 5.25
E_ECC = 10 + 19 / 60
NOTED = []


def read(name):
    return list(csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t"))


def par(z, pi_min):
    s = math.sin(math.radians(pi_min / 60))
    zz = math.radians(z)
    return math.degrees(math.atan2(s * math.sin(zz), 1 - s * math.cos(zz))) * 3600


def pi_of(dist):
    return math.degrees(math.asin(1 / dist)) * 60


def epi(alpha, centre):
    d = lambda a: math.sqrt(centre ** 2 + R_EPI ** 2 + 2 * centre * R_EPI * math.cos(math.radians(a)))
    return 3600 * (d(0) - d(alpha)) / (d(0) - d(180))


def ecc(eta2):
    m, e, R = math.radians(eta2), E_ECC, 60 - E_ECC
    rho = e * math.cos(m) + math.sqrt(R * R - (e * math.sin(m)) ** 2)
    return 3600 * (60 - rho) / (2 * E_ECC)


def u(r, c, n=2):
    v = 0
    for k in range(1, n + 1):
        v = v * 60 + int(r[f"{c}_{k}"])
    return v


def show(x, n=2):
    x = round(x)
    return f"{x // 3600}° {x // 60 % 60}′ {x % 60}″" if n == 3 else f"{x // 60}′ {x % 60}″"


def show1(x):
    return f"{int(x // 60)}′ {x % 60:.1f}″"


R = read("parallax_p2.tsv")
Z = [int(r["z"]) for r in R]
row = {int(r["z"]): r for r in R}
found, agree, model, printed = [], [0], {}, {}
NAMES = {"sun": "Sun", "t1": "first term", "d2": "second less first", "t3": "third term", "d4": "fourth less third",
         "epa": "epicycle (apogee)", "epp": "epicycle (perigee)", "ecc": "eccentre"}


def key(z, c):
    return f"p. {row[z]['ppage']} {z} {c}"


# Sun, first term, second less first
PI_SUN, PI_1, PI_2 = pi_of(1210), pi_of(64 + 10 / 60), pi_of(53 + 50 / 60)
for c, f in (("sun", lambda z: par(z, PI_SUN)), ("t1", lambda z: par(z, PI_1)), ("d2", lambda z: par(z, PI_2) - par(z, PI_1))):
    for z in Z:
        p, e = u(row[z], c), f(z)
        printed[key(z, c)], model[key(z, c)] = show(p), e
        if abs(p - e) > 3:
            found.append((key(z, c), show(p), f"computed {show1(e)}"))
        else:
            agree[0] += 1

# third term, fourth less third: the last row, and steps that never increase
for c, n, last in (("t3", 3, 79 * 60), ("d4", 2, 25 * 60)):
    vals = [u(row[z], c, n) for z in Z]
    for z, v in zip(Z, vals):
        printed[key(z, c)] = show(v, n)
        model[key(z, c)] = par(z, 79) if c == "t3" else par(z, 104) - par(z, 79)
    if vals[-1] != last:
        found.append((key(90, c), show(vals[-1], n), f"the horizontal parallax {show(last, n)}"))
    steps = [b - a for a, b in zip([0] + vals[:-1], vals)]
    for i in range(2, len(steps)):                          # from the second row (the first step starts at 0)
        if steps[i] > steps[i - 1] + 1:
            found.append((key(Z[i], c), show(vals[i], n), f"the step rises from {steps[i - 1]}″ to {steps[i]}″ "
                                                            f"(rows {Z[i - 1]}-{Z[i]})"))
        else:
            agree[0] += 1

# sixtieths: values at multiples of 6° against the computation (or against both neighbours), thirds between
p89 = {int(r["arg"]): int(r["portion_1"]) * 60 + int(r["portion_2"])
       for r in csv.DictReader(open(HERE / ".." / "eclipses" / "correction_p2.tsv", encoding="utf-8"), delimiter="\t")}
for c, f in (("epa", lambda z: epi(2 * z, 60)), ("epp", lambda z: epi(2 * z, 60 - 2 * E_ECC)), ("ecc", lambda z: ecc(2 * z))):
    v = {0: 0, **{z: u(row[z], c) for z in Z}}
    node = {}
    for z in range(6, 91, 6):
        printed[key(z, c)], model[key(z, c)] = show(v[z]), f(z)
        left = v[z - 2] + (v[z - 2] - v[z - 4]) if z - 4 >= 0 else None
        right = v[z + 2] - (v[z + 4] - v[z + 2]) if z + 4 <= 90 else None
        sides = [s for s in (left, right) if s is not None]
        agree_sides = len(sides) == 2 and abs(left - right) <= 2
        node[z] = v[z]
        if abs(v[z] - f(z)) > 5 and not (agree_sides and abs(v[z] - left) <= 2):
            node[z] = round((left + right) / 2) if agree_sides else v[z]
            found.append((key(z, c), show(v[z]), f"computed {show1(f(z))}"
                          + (f"; the rows on both sides give {show(node[z])}" if agree_sides else "")
                          + (f"; p. 89 has {show(p89[2 * z])} at {2 * z}°" if c == "epa" else "")))
        else:
            agree[0] += 1
    node[0] = 0
    for z in Z:
        if z % 6:
            a, b = 6 * (z // 6), 6 * (z // 6) + 6
            interp = node[a] + (node[b] - node[a]) * (z - a) / 6
            printed[key(z, c)], model[key(z, c)] = show(v[z]), interp
            if abs(v[z] - interp) > 1:
                found.append((key(z, c), show(v[z]), f"a third between {a}° and {b}° gives {show1(interp)}; "
                                                       f"computed {show1(f(z))}"))
            else:
                agree[0] += 1
    if c == "epa":
        for z in range(6, 91, 6):
            if v[z] != p89[2 * z] and key(z, c) not in {x[0] for x in found}:
                found.append((f"{key(z, c)} = p. 89", show(v[z]), f"{show(p89[2 * z])} on p. 89 ({2 * z}°)"))


def main():
    ledger_rows = read("par_discrepancies.tsv")
    ledger = {r["where"] for r in ledger_rows if r["kind"] != "noted"}
    open_ = [f for f in found if f[0] not in ledger]
    t3 = max(abs(u(row[z], "t3", 3) - par(z, 79)) for z in Z)
    d4 = max(abs(u(row[z], "d4") - par(z, 104) + par(z, 79)) for z in Z)
    print(f"values within tolerance {agree[0]}, differ {len(found)} (ledgered {len(found) - len(open_)}, open {len(open_)})")
    print(f"  third term below the computation with 79′ by up to {t3:.1f}″, fourth less third (104′) by up to {d4:.1f}″")
    for where, p, e in (found if "--list" in sys.argv else open_):
        print(f"  {where}: {p}; {e}" + ("" if where in ledger else "   << not in the ledger"))
    stale = [w for w in ledger if w not in {f[0] for f in found}]
    for w in stale:
        print("  ledger entry without a difference:", w)
    sys.exit(1 if open_ or stale else 0)


if __name__ == "__main__":
    main()

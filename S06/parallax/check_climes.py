"""Check of Nallino's Part II pp. 95-101 (the parallaxes of the Moon in longitude and latitude in the seven climes),
from clime_p2.tsv and clime_pages.tsv.
  mirror    the tables of signs placed symmetrically to the meridian of the solstices print the same values backwards
            in time: Leo and Gemini, Virgo and Taurus, Libra and Aries, Scorpio and Pisces, Sagittarius and Aquarius; Cancer
            and Capricorn each with itself. Every row must equal the row of the mirror table read from the other end.
  hours     the half-day arcs in the first and last rows: those of opposite declination add up to 12h (within 1 minute),
            Libra and Aries have 6h, and each agrees with the computation for the latitude of the clime in its title
            and the obliquity 23° 35′ (within 1 minute; within 3 minutes in the first clime, whose arcs are rounded to
            5 minutes); the longest day of the title is twice the half-day of Cancer.
A difference must be in clime_discrepancies.tsv; --list shows the ledgered ones too. Exit code 1 on anything open."""
import csv, math, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EPS = 23 + 35 / 60
MIRROR = {"Leo": "Gemini", "Gemini": "Leo", "Virgo": "Taurus", "Taurus": "Virgo", "Libra": "Aries", "Aries": "Libra",
          "Scorpio": "Pisces", "Pisces": "Scorpio", "Sagittarius": "Aquarius", "Aquarius": "Sagittarius",
          "Cancer": "Cancer", "Capricorn": "Capricorn"}
LON = {"Aries": 0, "Taurus": 30, "Gemini": 60, "Cancer": 90, "Leo": 120, "Virgo": 150, "Libra": 180, "Scorpio": 210,
       "Sagittarius": 240, "Capricorn": 270, "Aquarius": 300, "Pisces": 330}


def read(name):
    return list(csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t"))


R = read("clime_p2.tsv")
P = {r["ppage"]: r for r in read("clime_pages.tsv") if r["half"] == "top"}
T = {}
for r in R:
    T.setdefault((r["ppage"], r["sign"]), []).append(r)
found, agree, printed, model = [], [0], {}, {}
NOTED = ["p. 97 Cancer 6 = Cancer 10", "p. 95 title latitude", "p. 96 title latitude", "p. 101 title latitude"]


def cell(r):
    return f"{r['long']}′ {r['north']}{r['lat']}′"


# mirror
for (pp, sign), rows in T.items():
    m = T[(pp, MIRROR[sign])]
    n = len(rows)
    if len(m) != n:
        found.append((f"p. {pp} {sign} rows", str(n), f"{len(m)} rows in {MIRROR[sign]}"))
        continue
    for i, r in enumerate(rows):
        q = m[n - 1 - i]
        if (sign, i) > (MIRROR[sign], n - 1 - i):                      # each pair once
            continue
        if (r["long"], r["lat"], r["north"]) != (q["long"], q["lat"], q["north"]):
            found.append((f"p. {pp} {sign} {r['row']} = {MIRROR[sign]} {q['row']}", cell(r), f"{cell(q)} in {MIRROR[sign]}"))
        else:
            agree[0] += 1


# hours
def hm(label):
    m = re.match(r"(\d+)ʰ(?: (\d+)′)?$", label)
    return int(m.group(1)) * 60 + int(m.group(2) or 0)


for pp, page in P.items():
    lat = [int(x) for x in re.findall(r"\d+", page["title_la"].split("latitudo")[1].split("et horae")[0])]
    phi = lat[0] + (lat[1] / 60 if len(lat) > 1 else 0)
    hours = [int(x) for x in re.findall(r"\d+", page["title_la"].split("et horae")[1])]
    longest = hours[0] * 60 + (hours[1] if len(hours) > 1 else 0)
    half = {sign: hm(T[(pp, sign)][0]["hour"]) for (p, sign) in T if p == pp}
    if 2 * half["Cancer"] != longest:
        found.append((f"p. {pp} title hours", f"{longest // 60}h {longest % 60}m", f"twice the half-day of Cancer, {2 * half['Cancer']} min"))
    for a, b in (("Cancer", "Capricorn"), ("Leo", "Sagittarius"), ("Virgo", "Scorpio"), ("Libra", "Aries")):
        s = half[a] + half[b]
        if abs(s - 720) > 1:
            found.append((f"p. {pp} {a} + {b}", f"{half[a]} + {half[b]} min", "12h"))
        else:
            agree[0] += 1
    # the latitude for which the longest day of the title holds, against the latitude of the title
    phi_l = math.degrees(math.atan(-math.cos(math.radians(longest / 8)) / math.tan(math.radians(EPS))))
    key = f"p. {pp} title latitude"
    printed[key] = f"{lat[0]}°" + (f" {lat[1]}′" if len(lat) > 1 else "")
    model[key] = phi_l
    if abs(phi - phi_l) * 60 > 1:
        found.append((key, printed[key], f"the longest day {longest // 60}h {longest % 60}m holds at "
                                         f"{int(phi_l)}° {(phi_l % 1) * 60:.1f}′"))
    else:
        agree[0] += 1
    tol = 3 if pp == "95" else 1
    for sign, h in half.items():
        d = math.asin(math.sin(math.radians(EPS)) * math.sin(math.radians(LON[sign])))
        H = math.degrees(math.acos(-math.tan(math.radians(phi_l)) * math.tan(d))) * 4        # minutes of time
        if abs(h - H) > tol:
            found.append((f"p. {pp} {sign} half-day", T[(pp, sign)][0]["hour"],
                           f"computed {int(H // 60)}h {H % 60:.1f}m"))
        else:
            agree[0] += 1
    # the last row repeats the half-day (an integer one without its mark)
    for (p, sign), rows in T.items():
        if p == pp:
            first, last = rows[0]["hour"], rows[-1]["hour"]
            if not (last == first or (last + "ʰ") == first):
                found.append((f"p. {pp} {sign} last hour", last, f"first {first}"))


def main():
    rows = read("clime_discrepancies.tsv")
    ledger = {r["where"] for r in rows if r["kind"] != "noted"}
    noted = {r["where"]: r for r in rows if r["kind"] == "noted"}
    problems = [f"no ledger entry for Nallino's emendation: {w}" for w in NOTED if w not in noted]
    problems += [f"ledger entry of kind «noted» not among Nallino's emendations: {w}" for w in noted if w not in NOTED]
    fnd = [f for f in found if f[0] not in NOTED]
    missing = [w for w in NOTED if w not in {f[0] for f in found}]
    problems += [f"Nallino's emendation without a difference: {w}" for w in missing]
    open_ = [f for f in fnd if f[0] not in ledger]
    print(f"checks passed {agree[0]}, differ {len(fnd)} (ledgered {len(fnd) - len(open_)}, open {len(open_)}); "
          f"Nallino's emendations {len(NOTED)}, problems {len(problems)}")
    for where, p, e in ((found if "--list" in sys.argv else open_)):
        print(f"  {where}: {p}; {e}" + ("" if where in ledger or where in NOTED else "   << not in the ledger"))
    for p in problems:
        print("  " + p)
    stale = [w for w in ledger if w not in {f[0] for f in fnd}]
    for w in stale:
        print("  ledger entry without a difference:", w)
    sys.exit(1 if open_ or stale or problems else 0)


if __name__ == "__main__":
    main()

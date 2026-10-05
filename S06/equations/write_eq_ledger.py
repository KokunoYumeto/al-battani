"""Write S06/equations/equations_discrepancies.tsv: the departures found by check_equations.py (pp. 78-83), each cell
read by eye on the scan, with the computed values, and the three cells that Nallino emends on p. 79."""
import csv, math, sys

D = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani/S06/equations/"
sys.path.insert(0, D)
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


def increment(n):
    return eq(n, R_MOON / (1 - 2 * E_MOON)) - eq(n, R_MOON)


def latitude(n):
    return math.degrees(math.asin(math.sin(math.radians(n)) * math.sin(math.radians(5))))


F = {"sun": (lambda n: eq(n, E_SUN), 3), "moon": (lambda n: eq(n, R_MOON), 3), "lat": (latitude, 3),
     "pro": (prosneusis, 2), "inc": (increment, 2)}
rows = {int(r["n"]): r for r in csv.DictReader(open(D + "equations_p2.tsv", encoding="utf-8"), delimiter="\t")}


def printed(key, n):
    r = rows[n]
    if F[key][1] == 3:
        return f"{r[key + '_d']}° {r[key + '_m']}′ {r[key + '_s']}″"
    return f"{r[key + '_d']}° {r[key + '_m']}′"


def computed(key, n):
    x = F[key][0](n)
    if F[key][1] == 3:
        s = x * 3600
        return f"{int(s // 3600)}° {int(s // 60 % 60)}′ {s % 60:.1f}″"
    m = x * 60
    return f"{int(m // 60)}° {m % 60:.1f}′"


def page(n):
    return str(77 + (n - 1) // 30 + 1)


def secs(key, n):
    r = rows[n]
    return (int(r[key + "_d"]) * 60 + int(r[key + "_m"])) * 60 + int(r[key + "_s"])


def dms(x, signed=False):
    sg = "-" if x < 0 else ""
    x = abs(round(x))
    if x >= 3600:
        return f"{sg}{x // 3600}° {x // 60 % 60}′ {x % 60}″"
    return f"{sg}{x // 60}′ {x % 60}″" if x >= 60 else f"{sg}{x}″"


def steps_note(key, n, prefix=""):
    """the printed steps from n - 1 to n and from n to n + 1, against the computed steps (seconds), from the data"""
    f = F[key][0]
    p_prev, p_n, p_next = secs(key, n - 1), secs(key, n), secs(key, n + 1)
    c_prev, c_n, c_next = f(n - 1) * 3600, f(n) * 3600, f(n + 1) * 3600
    return (prefix + f"the printed steps from {n - 1}° ({printed(key, n - 1)}) and to {n + 1}° ({printed(key, n + 1)}) are "
            f"{dms(p_n - p_prev)} and {dms(p_next - p_n)}; the computed steps are {dms(c_n - c_prev)} and {dms(c_next - c_n)}")


def entry(key, a, b, kind, note):
    ns = range(a, b + 1)
    p0, p1 = page(a), page(b)
    where = f"p. {p0 if p0 == p1 else p0 + '-' + p1} {key} {a}" + (f"-{b}" if b != a else "")
    return (where, ", ".join(printed(key, n) for n in ns), ", ".join(computed(key, n) for n in ns), kind, note)


RUN = "al-Battānī's values depart from the computation in this stretch"
PTOL = ("al-Battānī took this column from Ptolemy (values for every sixth degree in the first and fourth quadrants, every "
        "third in the second and third) and interpolated the rest; Delambre found Ptolemy's column right to 1′ or 2′")
L = [
    entry("sun", 58, 64, "run", RUN),
    entry("sun", 104, 104, "value", steps_note("sun", 104)),
    entry("sun", 105, 107, "run", RUN),
    entry("sun", 128, 136, "run", RUN),
    entry("sun", 151, 166, "run", RUN + "; the largest departure in the column"),
    entry("moon", 19, 19, "value", steps_note("moon", 19, "31′ for 30′: ")),
    entry("moon", 25, 28, "run", RUN),
    entry("moon", 41, 41, "value", steps_note("moon", 41)),
    entry("moon", 61, 61, "value", steps_note("moon", 61)),
    entry("moon", 63, 63, "value", steps_note("moon", 63)),
    entry("moon", 73, 73, "value", steps_note("moon", 73, "38′ for 39′: ")),
    entry("moon", 93, 99, "run", RUN + "; Nallino names 96° (5° 0′ 57″ for 5° 1′ 9″) among the larger differences of al-Battānī's seconds"),
    entry("moon", 106, 109, "run", RUN + "; Nallino names 108° (4° 53′ 30″ for 4° 53′ 19″) and 109° (4° 52′ 10″ for 4° 52′ 3″)"),
    entry("moon", 112, 115, "run", RUN + "; Nallino names 114° (4° 44′ 6″ for 4° 44′ 17″)"),
    entry("moon", 131, 134, "run", RUN),
    entry("moon", 136, 139, "run", RUN),
    entry("lat", 63, 63, "value", steps_note("lat", 63, "26′ for 27′: ")),
    entry("lat", 133, 138, "run", RUN + "; the equal latitudes of 42°-47° agree with the computation within 1″, and those "
                                 "of 133°-138° stand 3″, 10″, 10″, 20″, 20″ and 20″ above them"),
    entry("pro", 123, 129, "run", PTOL),
    entry("pro", 147, 153, "run", PTOL),
    entry("pro", 172, 177, "run", PTOL),
    entry("inc", 22, 50, "run", PTOL + "; the excess over the computation grows from 0.6′ at 6° to 5.5′ at 44°, and the "
                                 "values at 6°, 12°, 18°, 24° and 30° are 14′, 28′, 42′, 56′ and 70′"),
    entry("inc", 53, 54, "run", PTOL),
]
for n, (pr, nal, exact) in {35: ("2° 40′ 12″", "2° 40′ 52″", "2° 40′ 52.6″"), 36: ("2° 45′ 17″", "2° 44′ 57″", "2° 44′ 59.5″"),
                            37: ("2° 49′ 42″", "2° 49′ 2″", "2° 49′ 4″")}.items():
    L.append((f"p. 79 moon {n}", pr, nal, "noted",
              f"Nallino, Part II p. 226: an error of the codex to be corrected to {nal} (exactly {exact})"))
with open(D + "equations_discrepancies.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["where", "printed", "computed", "kind", "note"])
    w.writerows(L)
print(len(L), "ledger rows")

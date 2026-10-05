"""Write S06/spherical/spherical_discrepancies.tsv: the differences found by check_spherical.py (pp. 55-60), each
confirmed on the scan. The computed values of the two runs on p. 59 are computed here from the data."""
import csv, math

D = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani/S06/spherical/"
EPS = math.radians(23 + 35 / 60)
rows59 = list(csv.DictReader(open(D + "days59_p2.tsv", encoding="utf-8"), delimiter="\t"))


def run(a, b):
    sel = [r for r in rows59 if a <= int(r["phi_d"]) + int(r["phi_m"]) / 60 <= b]
    printed = ", ".join(f"{r['inc_d']}° {r['inc_m']}′" for r in sel)
    comp = []
    for r in sel:
        phi = int(r["phi_d"]) + int(r["phi_m"]) / 60
        c = math.degrees(math.asin(math.tan(math.radians(phi)) * math.tan(EPS))) * 60
        comp.append(f"{int(c // 60)}° {c % 60:.1f}′")
    return printed, ", ".join(comp)


p1, c1 = run(7, 9)
p2, c2 = run(24, 28.5)
L = [
    ("p. 58 right ascension 20° sine", "18ᵖ 57′ 10″", "18ᵖ 59′ 9″", "value",
     "57 for 59: the sine of the printed ascension 18° 26′ 51″ is 18ᵖ 59′ 9″; it lies between the sines of 18° 0′ "
     "(18ᵖ 32′ 27″) and 18° 30′ (19ᵖ 2′ 18″) on p. 55, and the seconds agree"),
    ("p. 59 latitudes 7° 0′-9° 0′", p1, c1, "run",
     "the printed values rise by 14′ for every half degree from 5° to 8°, where the computed rise is about 13⅓′, and "
     "by 13′ and 12′ alternately from 8° to 10°; they lie above the computation from 5° to 10° 30′, by more than 3′ from 7° to 9° "
     "(largest +5.0′ at 8°)"),
    ("p. 59 latitudes 24° 0′-28° 30′", p2, c2, "run",
     "the printed values lie above the computation from 21° to 29° 30′, by more than 3′ from 24° to 28° 30′ "
     "(largest +6.9′ at 25° 30′); 30° agrees again"),
]
# pp. 61-64: the equation of days, computed from al-Battani's elements with the table's zero point (median)
APOGEE, ECC = 82 + 17 / 60, math.sin(math.radians(1 + 59 / 60 + 10 / 3600))


def ra_deg(lam):
    l = math.radians(lam)
    return math.degrees(math.atan2(math.cos(EPS) * math.sin(l), math.cos(l))) % 360


def mean_long(lam):
    v = math.radians(lam - APOGEE); m = v
    for _ in range(20):
        m = v + math.atan2(ECC * math.sin(m), 1 + ECC * math.cos(m))
    return (APOGEE + math.degrees(m)) % 360


def eq_raw(lam):
    return ((mean_long(lam) - ra_deg(lam)) + 180) % 360 - 180


EQMIN = min(eq_raw(x / 10) for x in range(3600))
raeq = list(csv.DictReader(open(D + "raeq_p2.tsv", encoding="utf-8"), delimiter="\t"))
by = {(r["sign"], int(r["row"])): r for r in raeq}
dev = sorted(int(r["eq_d"]) * 60 + int(r["eq_m"]) - (eq_raw(int(r["lam"])) - EQMIN) * 60 for r in raeq)
ZERO = dev[len(dev) // 2]
ORDER = ["Capricornus", "Aquarius", "Pisces", "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio",
         "Sagittarius"]


def eq_run(sign0, row0, sign1, row1):
    seq, on = [], False
    for s_ in ORDER:
        for n in range(1, 31):
            if (s_, n) == (sign0, row0):
                on = True
            if on:
                seq.append(by[(s_, n)])
            if (s_, n) == (sign1, row1):
                on = False
    printed = ", ".join(f"{r['eq_d']}° {r['eq_m']}′" for r in seq)
    comp = []
    for r in seq:
        c = (eq_raw(int(r["lam"])) - EQMIN) * 60 + ZERO
        comp.append(f"{int(c // 60)}° {c % 60:.1f}′")
    return printed, ", ".join(comp)


for key, a_, b_, note in (
        ("p. 62 equation Gemini 4-7", ("Gemini", 4), ("Gemini", 7),
         "the printed values fall from 5° 33′ to 5° 29′ and the computed values from 5° 30.0′ to 5° 25.8′; largest +4.7′ at Gemini 6"),
        ("p. 63 equation Leo 20 - Virgo 10", ("Leo", 20), ("Virgo", 10),
         "the printed values rise by 2′ a degree to Leo 22 and by 3′ a degree to Virgo 4 (3° 57′), while the computed rise "
         "grows from 2′ to 4′; from Virgo 5 they rise by 4′ and 5′ and come back towards the computation; largest -7.3′ at "
         "Virgo 4 (computed 4° 4.3′)"),
        ("p. 64 equation Libra 16-25", ("Libra", 16), ("Libra", 25),
         "largest +6.3′ at Libra 21 (printed 7° 34′)"),
        ("p. 64 equation Scorpio 21-30", ("Scorpio", 21), ("Scorpio", 30),
         "largest +4.1′ at Scorpio 24 (printed 7° 31′)")):
    pr, cp = eq_run(a_[0], a_[1], b_[0], b_[1])
    L.append((key, pr, cp, "run", note + f"; computed from al-Battānī's elements with the table's zero point ({ZERO:+.1f}′)"))

# pp. 65-67: oblique ascensions and seasonal hours, computed for the latitude of the head
def asc_diff(lam, phi):
    d = math.asin(math.sin(math.radians(lam)) * math.sin(EPS))
    return math.degrees(math.asin(math.tan(math.radians(phi)) * math.tan(d)))


def oa(lam, phi):
    return (ra_deg(lam) - asc_diff(lam, phi)) % 360


def hr(lam, phi):
    return (180 + 2 * asc_diff(lam, phi)) / 12


def fm(x):
    return f"{int(x)}° {x % 1 * 60:.1f}′"


H = 36 + 40 / 60
for key, pr, comp, note in (
        ("p. 65 latitude 16° 39′ 50", "42° 3′", fm(oa(50, 16 + 39 / 60)),
         "3.1′ above the computation; at 130° the column gives 127° 0′, 3.0′ above"),
        ("p. 65 latitude 20° 28′ 210", "212° 21′", fm(oa(210, 20 + 28 / 60)),
         "5.7′ above the computation; the neighbouring columns of the row give 211° 23′ and 213° 7′"),
        ("p. 65 latitude 27° 28′ 250", "267° 32′", fm(oa(250, 27 + 28 / 60)),
         "267 for 260: across the row the values rise by 1° 44′ from column to column (255° 19′, 257° 3′, 258° 47′, "
         "260° 32′, 262° 16′, 264° 0′)"),
        ("p. 65 latitude 30° 40′ 250", "260° 16′", fm(oa(250, 30 + 40 / 60)),
         "260 for 262 (see the entry for 27° 28′)"),
        ("p. 66 latitude 43° 25′ 80", "55° 14′", fm(oa(80, 43 + 25 / 60)),
         "3.2′ above; the column as a whole fits the latitude 43° 23.4′, and the values at 80° and 280° are symmetric "
         "(55° 14′ + 304° 46′ = 360°)"),
        ("p. 66 latitude 43° 25′ 280", "304° 46′", fm(oa(280, 43 + 25 / 60)),
         "3.2′ below (see the entry for 80°)"),
        ("p. 67 Baghdad hours 320-330", "12° 20′, 12° 43′", fm(hr(320, 33 + 9 / 60)) + ", " + fm(hr(330, 33 + 9 / 60)),
         "12 for 13 in both: the hours of the neighbouring rows are 12° 59′ (310°) and 14° 8′ (340°)"),
        ("p. 67 Harran ascensions 90-100", "70° 59′, 82° 13′", fm(oa(90, H)) + ", " + fm(oa(100, H)),
         "the ascensions and the seasonal hours of Ḥarrān both fit the latitude 36° 45′ (36° 44.5′ and 36° 44.1′), not "
         "the 36° 40′ of the head; these values, near the solstice, are the most sensitive to the latitude"),
        ("p. 67 Harran ascensions 260-270", "277° 47′, 289° 1′", fm(oa(260, H)) + ", " + fm(oa(270, H)),
         "see the entry for 90°-100°")):
    L.append((key, pr, comp, "value" if "-" not in key.split()[-1] else "run", note))

L.append(("p. 71 Aquarius 30 hours", "13° 33′", "13° 34′", "noted",
          f"Nallino, Part II p. 222: 13° 34′ for the 13° 33′ of the codex and of the translation; computed for 36° 0′: "
          f"{fm(hr(330, 36.0))}"))

with open(D + "spherical_discrepancies.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["where", "printed", "computed", "kind", "note"])
    w.writerows(L)
print(len(L), "ledger rows")
print(c1); print(c2)

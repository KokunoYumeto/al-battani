"""Write S06/eclipses/ecl_discrepancies.tsv: the differences found by check_eclipses.py (Part II pp. 88-91), each read
by eye on the scan, and the numbers that Nallino emends (Part II p. 231). The numbers in the notes are computed here
from the data and the check's model."""
import csv, math
from pathlib import Path

import check_eclipses as c

HERE = Path(__file__).resolve().parent
F = {f[0]: f for f in c.found}
M, P = c.model, c.printed


def r0(x, unit="′"):
    """seconds -> «a′ b″» rounded to the second"""
    s = round(x)
    return f"{s // 60}′ {s % 60}″"


def r1(x):
    return f"{int(x // 60)}′ {x % 60:.1f}″"


def dig(x):
    """minutes of a digit -> «aᵈ b′»"""
    s = round(x)
    return f"{s // 60}ᵈ {s % 60}′"


def dig1(x):
    return f"{int(x // 60)}ᵈ {x % 60:.1f}′"


def cells(key_fmt, labels):
    return [key_fmt.format(l) for l in labels]


def labels_of(key):
    """«p. 90 lunar_min 19-end mora» -> the row labels of the run"""
    a, *b = key.split()[3].split("-")
    return a, (b[0] if b else a)


E = c.read("eclipses_p2.tsv")
C = c.read("correction_p2.tsv")
G = c.read("digits_p2.tsv")
entries = []

# p. 89: portions
por = {int(r["arg"]): (int(r["portion_1"]) * 60 + int(r["portion_2"])) for r in C}
por[0] = 0
grid = [n for n in range(12, 181, 12)]
far = [n for n in grid if abs(por[n] - 3600 * c.fraction(n)) > 5]
near = max(abs(por[n] - 3600 * c.fraction(n)) for n in grid if n not in far)
k = "p. 89 correction 12-24 portion"
entries.append((k, F[k][1], ", ".join(r0(3600 * c.fraction(n)) for n in (12, 24)), "run",
                f"the portions are 60′ times the fraction of the change of the Moon's distance (epicycle 5;15 at the "
                f"apogee of the eccentre): {r1(3600 * c.fraction(12))} and {r1(3600 * c.fraction(24))}. The other values at "
                f"multiples of 12° lie within {near:.1f}″ of the computation (132° excepted), and those at odd multiples of "
                f"6° are the means of their neighbours: 30° ({r0(por[30])}) of 24° and 36° ({r0(por[24])}, {r0(por[36])}). "
                f"Nallino, Part II p. 231: the column is Ptolemy's (Almagest VI 8), and Theon's Handy Tables have all "
                f"its columns"))
k = "p. 89 correction 132 portion"
entries.append((k, F[k][1], r0(3600 * c.fraction(132)), "value",
                f"the computation gives {r1(3600 * c.fraction(132))}; the neighbouring means follow the printed value: "
                f"126° ({r0(por[126])}) of 120° and 132° ({r0(por[120])}, {r0(por[132])}), and 138° ({r0(por[138])}) of "
                f"132° and 144° ({r0(por[144])})"))

# p. 89: areas
A = [r for r in G if r["table"] == "areas"]
for k, ratio, body in (("p. 89 areas 9-11 sun", 1.0, "Sun"), ("p. 89 areas 1 moon", 2.6, "Moon"),
                       ("p. 89 areas 9-10 moon", 2.6, "Moon")):
    a, b = labels_of(k)
    ds = range(int(a), int(b) + 1)
    col = k.split()[-1]
    rest = max(abs(int(r[col + "_1"]) * 60 + int(r[col + "_2"]) - 60 * c.area(int(r["arg"]), ratio)) for r in A
               if int(r["arg"]) not in (1, 9, 10, 11))
    what = ("the part of the solar disc covered when the lunar disc, of the same size, covers d twelfths of its diameter"
            if body == "Sun" else "the part of the lunar disc covered by the shadow, of 2 3/5 lunar radii, when it covers "
            "d twelfths of the diameter")
    entries.append((k, F[k][1], ", ".join(dig(60 * c.area(d, ratio)) for d in ds), "run" if len(ds) > 1 else "value",
                    f"{what}: {', '.join(dig1(60 * c.area(d, ratio)) for d in ds)}. The printed values are multiples of 5′; "
                    f"in digits 2-8 they lie within {rest:.1f}′ of the computation. Nallino, Part II p. 231: the columns are "
                    f"in Ptolemy (Almagest VI 8) and Theon; in the third column, line 3, Ptolemy has 2 1/15 (2ᵈ 4′) and "
                    f"Theon 2 1/5"))

# pp. 90-91
def tab(t):
    return [r for r in E if r["table"] == t]


def u(r, col):
    return int(r[col + "_1"]) * 60 + int(r[col + "_2"])


S, rm, ru = c.params["lunar_max"]
LM = tab("lunar_max")
k = "p. 90 lunar_max 3-5 inc"
entries.append((k, F[k][1], ", ".join(r0(M[f"p. 90 lunar_max {d} inc"]) for d in ("3", "4", "5")), "run",
                f"the arc of incidence sqrt(S² - b²) with S = {r0(S * 60)} (the latitude of 0 digits) and the printed "
                f"latitudes b ({', '.join(LM[d]['lat_1'] + '′ ' + LM[d]['lat_2'] + '″' for d in (3, 4, 5))}): "
                f"{', '.join(r1(M[f'p. 90 lunar_max {d} inc']) for d in ('3', '4', '5'))}. At the least distance the same "
                f"rows agree with the computation. At 5 digits the printed 16″ stands for the computed 56″; in Maghribi "
                f"abjad 16 is يو and 56 نو"))
for d in ("12", "14"):
    k = f"p. 90 lunar_max {d} inc"
    entries.append((k, F[k][1], r0(M[k]), "value",
                    f"the computation gives {r1(M[k])} (latitude {LM[int(d)]['lat_1']}′ {LM[int(d)]['lat_2']}″"
                    + (", where the eclipse becomes total" if d == "12" else
                       f", half duration {LM[int(d)]['mora_1']}′ {LM[int(d)]['mora_2']}″") + ")"))
k = "p. 90 lunar_max end digits"
entries.append((k, F[k][1], c.dms(M[k] / 3600), "value",
                f"at latitude 0 the eclipse covers 12 S / (2 r_m) = 12 × 53′ / 29′ 30″ = {M[k] / 3600:.4f} digits, "
                f"{c.dms(M[k] / 3600)}; at the least distance 12 × 63′ 36″ / 35′ 20″ = 21ᵈ 36′, as printed"))
S2, rm2, ru2 = c.params["lunar_min"]
Lm = tab("lunar_min")
k = "p. 90 lunar_min 19-end mora"
entries.append((k, F[k][1], ", ".join(r0(M[f"p. 90 lunar_min {d} mora"]) for d in ("19", "20", "21", "end")), "run",
                f"the half duration sqrt((r_u - r_m)² - b²) with r_u - r_m = {r0((ru2 - rm2) * 60)}, the latitude of 12 "
                f"digits: {', '.join(r1(M[f'p. 90 lunar_min {d} mora']) for d in ('19', '20', '21', 'end'))}. At latitude 0 "
                f"it is r_u - r_m itself, and the incidence in the same row is 2 r_m ({Lm[-1]['inc_1']}′ {Lm[-1]['inc_2']}″, "
                f"as printed). The last two values exceed the computation by 40″; in Maghribi abjad 13 is يج and 53 نج, 16 "
                f"يو and 56 نو"))
LX = tab("solar_max")
for d in ("5", "10"):
    k = f"p. 91 solar_max {d} inc"
    entries.append((k, F[k][1], r0(M[k]), "value",
                    f"sqrt(S² - b²) with S = 31′ and the printed latitude {LX[int(d)]['lat_1']}′ {LX[int(d)]['lat_2']}″ gives "
                    f"{r1(M[k])}"))
k = "p. 91 solar_max end digits"
entries.append((k, F[k][1], c.dms(M[k] / 3600), "value",
                f"at latitude 0: 12 S / (2 r_s) = 12 × 31′ / 32′ 30″ = {M[k] / 3600:.4f} digits, {c.dms(M[k] / 3600)}; at the "
                f"least distance 12 × 34′ / 32′ 30″ = {c.dms(12 * 34 / 32.5)}, printed 12ᵈ 33′"))
LN = tab("solar_min")
k = "p. 91 solar_min 4 inc"
entries.append((k, F[k][1], r0(M[k]), "value",
                f"sqrt(S² - b²) with S = 34′ and the printed latitude {LN[4]['lat_1']}′ {LN[4]['lat_2']}″ gives {r1(M[k])}"))
k = "p. 90 lunar_min interval"
first, last = Lm[0], Lm[-2]
entries.append((k, F[k][1], "0° 2′ 56″ 40‴", "value",
                f"the latitude column falls from {first['lat_1']}′ {first['lat_2']}″ to {last['lat_1']}′ {last['lat_2']}″ in "
                f"21 digits, 2′ 56″ 40‴ a digit, a twelfth of the lunar diameter 35′ 20″; the Arabic line has the same "
                f"30‴ (ب نو ل)"))

# Nallino's emendations
k = "p. 89 correction 18 portion"
entries.append((k, P[k], r0(M[k]), "noted",
                f"Nallino, Part II p. 231: 1′ 42″ for 1′ 22″, the mean of 12° and 24° ({r0(por[12])}, {r0(por[24])}), as at "
                f"the other odd multiples of 6°. The distance computation gives {r1(3600 * c.fraction(18))}"))
for k, read_ in (("p. 88 limits 191° 16′", "190° 56′"), ("p. 88 limits 348° 44′", "349° 4′")):
    entries.append((k, P[k], read_, "noted",
                    "Nallino, Part II p. 231 (as p. 209): the solar limits are to be read 159° 44′-190° 56′, 0°-20° 16′ and "
                    "349° 4′-360°, here and on p. 32; the Arabic text has the same numbers as the Latin (قضا يو, سمح مد)"))

with open(HERE / "ecl_discrepancies.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["where", "printed", "computed", "kind", "note"])
    w.writerows(entries)
print(len(entries), "ledger rows")

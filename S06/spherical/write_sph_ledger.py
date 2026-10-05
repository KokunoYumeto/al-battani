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
with open(D + "spherical_discrepancies.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["where", "printed", "computed", "kind", "note"])
    w.writerows(L)
print(len(L), "ledger rows")
print(c1); print(c2)

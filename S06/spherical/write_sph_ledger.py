"""Write S06/spherical/spherical_discrepancies.tsv: the differences found by check_spherical.py (pp. 55-58), each
confirmed on the scan."""
import csv

OUT = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani/S06/spherical/spherical_discrepancies.tsv"
L = [
    ("p. 58 right ascension 20° sine", "18ᵖ 57′ 10″", "18ᵖ 59′ 9″", "value",
     "57 for 59: the sine of the printed ascension 18° 26′ 51″ is 18ᵖ 59′ 9″; it lies between the sines of 18° 0′ "
     "(18ᵖ 32′ 27″) and 18° 30′ (19ᵖ 2′ 18″) on p. 55, and the seconds agree"),
]
with open(OUT, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["where", "printed", "computed", "kind", "note"])
    w.writerows(L)
print(len(L), "ledger rows")

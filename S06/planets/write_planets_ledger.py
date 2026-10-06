"""Write S06/planets/planets_discrepancies.tsv: the differences found by check_planets.py (Part II pp. 108-137), each
read by eye on the scan, and the cells that Nallino emends (Part II p. 238). The numbers in the notes are computed here
from the data and the check's model."""
import csv
from pathlib import Path

import check_planets as c

HERE = Path(__file__).resolve().parent
F = {f[0]: f for f in c.found}
M, P = c.model, c.printed
ROWS = {(r["planet"], int(r["n"])): r for r in c.R}


def m(pk, n, col):
    return M[f"p. {ROWS[(pk, n)]['ppage']} {pk} {n} {col}"]


def pr(pk, n, col):
    return P[f"p. {ROWS[(pk, n)]['ppage']} {pk} {n} {col}"]


def dm(x, places=0):
    x = round(x, places)
    return f"{int(x // 60)}° {x % 60:.{places}f}′"


entries = []
k = "p. 118 jup 121 III (neighbours)"
seq = ", ".join(f"{pr('jup', n, 'III')} ({n}°)" for n in range(120, 125))
entries.append((k, F[k][1], dm(m("jup", 121, "III")), "value",
                f"the printed values run {seq}: 121° repeats the value of 122°, and the other steps of the stretch are 5′ and 3′; "
                f"the computation gives {', '.join(dm(m('jup', n, 'III'), 1) for n in range(120, 125))}, and the printed "
                f"values stand 1′ to 1.5′ above it at 120° and 122°-124°. The 5 is printed damaged"))
k = "p. 125 mars 164-165 VI"
entries.append((k, F[k][1], ", ".join(dm(m("mars", n, "VI")) for n in (164, 165)), "value",
                f"each value is a degree and 2′ below the computation ({dm(m('mars', 164, 'VI'), 1)}, "
                f"{dm(m('mars', 165, 'VI'), 1)}); the neighbouring values {pr('mars', 163, 'VI')} (163°), "
                f"{pr('mars', 166, 'VI')} (166°) and {pr('mars', 167, 'VI')} (167°) lie within 3′ of it "
                f"({dm(m('mars', 163, 'VI'), 1)}, {dm(m('mars', 166, 'VI'), 1)}, {dm(m('mars', 167, 'VI'), 1)})"))
k = "p. 125 mars 169 VI"
entries.append((k, F[k][1], dm(m("mars", 169, "VI")), "value",
                f"the computation gives {dm(m('mars', 169, 'VI'), 1)}; the neighbouring values {pr('mars', 168, 'VI')} "
                f"(168°) and {pr('mars', 170, 'VI')} (170°) lie within 3′ of theirs ({dm(m('mars', 168, 'VI'), 1)}, "
                f"{dm(m('mars', 170, 'VI'), 1)})"))
k = "p. 125 mars 159-162 VII"
entries.append((k, F[k][1], ", ".join(dm(m("mars", n, "VII"), 1) for n in range(159, 163)), "run",
                "al-Battānī's values depart from the computation in this stretch; the steps of the printed column are "
                "regular"))
page = next(p for p in c.read("planets_pages.tsv") if p["ppage"] == "126")
entries.append(("p. 126 apogee line", "قب يد", "فب يد", "value",
                "the Arabic line gives the apogee of Venus as قب يد, 102° 14′ in abjad; the Latin has 82° 14′ (فب يد). "
                "Al-Battānī gives Venus the apogee of the Sun (Schiaparelli, t. I, p. 242), 82° 17′ in his elements"))
for n in (90, 91):
    k = f"p. {ROWS[('jup', n)]['ppage']} jup {n} III"
    entries.append((k, P[k], "5° 15′", "noted",
                    f"Nallino, Part II p. 238: in the third column of p. 116, last line, and of p. 117, line 1, read 5° 15′ "
                    f"(يه) for 5° 14′ (يد). The computation gives {dm(M[k], 1)}"))

with open(HERE / "planets_discrepancies.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["where", "printed", "computed", "kind", "note"])
    w.writerows(entries)
print(len(entries), "ledger rows")

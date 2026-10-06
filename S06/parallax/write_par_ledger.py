"""Write S06/parallax/par_discrepancies.tsv: the differences found by check_parallax.py (Part II pp. 93-94), each read
by eye on the scan. The numbers in the notes are computed here from the data and the check's model."""
import csv
from pathlib import Path

import check_parallax as c

HERE = Path(__file__).resolve().parent
F = {f[0]: f for f in c.found}
v = {col: {0: 0, **{z: c.u(c.row[z], col) for z in c.Z}} for col in ("epa", "epp", "ecc")}
model = {"epa": lambda z: c.epi(2 * z, 60), "epp": lambda z: c.epi(2 * z, 60 - 2 * c.E_ECC), "ecc": lambda z: c.ecc(2 * z)}


def for_(printed, right):
    a, b = printed.split(), right.split()
    return " ".join(x for x, y in zip(a, b) if x != y) + " for " + " ".join(y for x, y in zip(a, b) if x != y)


entries = []
for k in sorted(F, key=lambda k: (k.split()[1], int(k.split()[2]))):
    _, pp, z, col = k.split()
    z = int(z)
    V = v[col]
    if z % 6 == 0:
        s1, s2 = V[z - 2] - V[z - 4], V[z + 4] - V[z + 2]
        right = c.show(V[z - 2] + s1)
        note = (f"{for_(c.show(V[z]), right)}: the rows on both sides give {right}, {c.show(V[z - 2])} plus the step "
                f"of {s1}″ from {z - 6}° and {c.show(V[z + 2])} less the step of {s2}″ to {z + 6}°")
        if col == "epa":
            note += f"; p. 89 has {c.show(c.p89[2 * z])} at {2 * z}°"
    else:
        a, b = 6 * (z // 6), 6 * (z // 6) + 6
        third = V[a] + (V[b] - V[a]) * (z - a) / 6
        right = c.show(third)
        note = (f"{for_(c.show(V[z]), right)}: a third of the way from {a}° ({c.show(V[a])}) to {b}° ({c.show(V[b])}) "
                f"gives {c.show1(third)}")
    note += f"; the computation gives {c.show1(model[col](z))}"
    entries.append((k, F[k][1], right, "value", note))

with open(HERE / "par_discrepancies.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["where", "printed", "computed", "kind", "note"])
    w.writerows(entries)
print(len(entries), "ledger rows")

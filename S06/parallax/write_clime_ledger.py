"""Write S06/parallax/clime_discrepancies.tsv: the numbers of Part II pp. 95-101 that Nallino emends in his notes (Part II
p. 237), with what the check computes for them. The computed values come from check_climes.py."""
import csv
from pathlib import Path

import check_climes as c

HERE = Path(__file__).resolve().parent
F = {f[0]: f for f in c.found}


def dm(x):
    return f"{int(x)}° {(x % 1) * 60:.1f}′"


entries = []
k = "p. 97 Cancer 6 = Cancer 10"
rows = c.T[("97", "Cancer")]
before, after = rows[5], rows[9]
entries.append((k, f"{after['long']}′ (row {after['row']})", f"{before['long']}′", "noted",
                f"Nallino, Part II p. 237: at the second hour of Cancer after culmination read 22′ for 21′ in the longitude. "
                f"The second hour before culmination has {c.cell(before)}, and every value of a clime is printed twice"))
EM = {"95": ("16° 39′ (لط)", "16° 32′ (لب)", "16° 38′ 48″"),
      "96": ("24° 5′ (ه)", "24° (with the zero sign for the minutes, which the print omits)", "24° 4′ 47″"),
      "101": ("48° 53′ (نج)", "48° 13′ (يج)", "48° 52′ 46″")}
for pp, (right, codex, precise) in EM.items():
    k = f"p. {pp} title latitude"
    phi = c.model[k]
    entries.append((k, c.printed[k], right.split(" (")[0], "noted",
                    f"Nallino, Part II p. 237: {right} for the codex's {codex}, precisely {precise}. The longest day of the "
                    f"title, {F[k][2].split('the longest day ')[1].split(' holds')[0].replace('h 0m', 'ʰ').replace('h ', 'ʰ ').replace('m', 'ᵐ')}, holds "
                    f"at {dm(phi)} with the obliquity 23° 35′, and the half-days of the table agree with it"))

with open(HERE / "clime_discrepancies.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["where", "printed", "computed", "kind", "note"])
    w.writerows(entries)
print(len(entries), "ledger rows")

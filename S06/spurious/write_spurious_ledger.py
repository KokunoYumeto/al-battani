"""Write S06/spurious/spurious_discrepancies.tsv: the last two lines of the conversion by collected Arab years (p. 304),
which Nallino prints as he restored them, with the numbers of the codex (Part II p. 317). check_spurious.py finds no
other difference."""
import csv
from pathlib import Path

OUT = Path(__file__).resolve().parent / "spurious_discrepancies.tsv"
NOTE = ("Nallino, Part II p. 317: the table probably ended at AH 600; an interpolator extended it, treating the Roman and "
        "the Coptic year as twelve months only (without the 5 1/4 added days), and the codex has here {codex}. Nallino "
        "prints the correct numbers, which the computation gives")
L = [
    ("p. 304 R 630", "1544 0 5 0", "1544 0 5 0", "noted", NOTE.format(codex="1544 years 0 months 10 days 15 fractions")),
    ("p. 304 R 660", "1573 1 13 45", "1573 1 13 45", "noted", NOTE.format(codex="1573 years 1 month 19 days 0 fractions")),
    ("p. 304 C 630", "949 1 7 45", "949 1 7 45", "noted",
     NOTE.format(codex="928 (sic) years 1 month 13 days 0 fractions")),
    ("p. 304 C 660", "978 2 16 30", "978 2 16 30", "noted",
     NOTE.format(codex="967 (sic) years 2 months 21 days 45 fractions")),
]
with open(OUT, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["where", "printed", "computed", "kind", "note"])
    w.writerows(L)
print(len(L), "ledger rows")

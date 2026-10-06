"""Write S06/stations/stations_discrepancies.tsv: the differences found by check_stations.py (none) and the cells on
which Nallino's notes report a reading of the codex (Part II p. 245, note 2)."""
import csv
from pathlib import Path

OUT = Path(__file__).resolve().parent / "stations_discrepancies.tsv"
L = [
    ("p. 138 mars 90", "163° 22′ (Statio II 196° 38′)", "163° 22.5′", "noted",
     "Nallino, Part II p. 245 n. 2, after Schiaparelli: Theon and the Escorial codex have the minutes 25′ and 35′ for "
     "the correct 22′ and 38′; the table prints 22′ and 38′. 163° 22′ is the mean of the values at 84° and 96° "
     "(162° 47′ and 163° 57′), as every value of the column between two multiples of 12° is the mean of its neighbours; "
     "the computation gives 163° 22.5′, and 163° 25′ would leave the two steps 38′ and 32′"),
]
with open(OUT, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["where", "printed", "computed", "kind", "note"])
    w.writerows(L)
print(len(L), "ledger rows")

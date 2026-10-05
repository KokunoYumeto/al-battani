"""Append one page of checked rows to the star-catalogue TSV files.
Usage: python add_page_rows.py ROWFILE   (ROWFILE is a small Python file defining P3, P3FN, P3PAGE, P2, P2NOTES, P2PAGE;
each a list of tuples in the column order of the target TSV; missing names are skipped).
Refuses to append rows for a page that is already present in the target file."""
import csv, runpy, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGETS = {"P3": "p3_stars.tsv", "P3FN": "p3_footnotes.tsv", "P3PAGE": "p3_pages.tsv",
           "P2": "p2_stars.tsv", "P2NOTES": "p2_notes.tsv", "P2PAGE": "p2_pages.tsv"}
data = runpy.run_path(sys.argv[1])
for name, fname in TARGETS.items():
    rows = data.get(name)
    if not rows:
        continue
    path = HERE / fname
    header = open(path, encoding="utf-8").readline().rstrip("\n").split("\t")
    have = {r[0] for r in csv.reader(open(path, encoding="utf-8"), delimiter="\t")}
    pages = {str(r[0]) for r in rows}
    if pages & have:
        sys.exit(f"{fname}: page(s) {sorted(pages & have)} already present; nothing appended")
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        for r in rows:
            r = [str(v) for v in r]
            if len(r) != len(header):
                sys.exit(f"{fname}: row has {len(r)} fields, header has {len(header)}: {r}")
            f.write("\t".join(r) + "\n")
    print(f"{fname}: +{len(rows)}")

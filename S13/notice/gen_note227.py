"""Nallino's notice before the tables, Part III p. 227 (PDF 925): line by line as printed, centred, right to left.
Usage: python gen_note227.py  (reads note227.tsv, writes p3_note227.tex)"""
import csv
from pathlib import Path
from gen_stars import PREAMBLE, AR_DIGITS, markup

HERE = Path(__file__).resolve().parent
rows = list(csv.DictReader(open(HERE / "note227.tsv", encoding="utf-8"), delimiter="\t"))
out = [PREAMBLE, r"\begin{document}", r"{\large \textarabic{" + rows[0]["ppage"].translate(AR_DIGITS) + r"}}\par\vspace{12mm}",
       r"\begin{Arabic}\begin{center}"]
GAP = {"L08": r"\\[6mm]", "L12": r"\\[6mm]", "L13": r"\\[2mm]", "L14": ""}   # paragraph breaks as printed
for r in rows:
    t = markup(r["text"], False)
    if r["kind"] == "title":
        out.append(r"{\large " + t + r"}\\[8mm]")
    else:
        out.append(t + GAP.get(r["line"], r"\\"))
out += [r"\end{center}\end{Arabic}", r"\end{document}"]
(HERE / "p3_note227.tex").write_text("\n".join(out) + "\n", encoding="utf-8")
print("wrote p3_note227.tex")

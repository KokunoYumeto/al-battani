"""The disposition of every page of the master scan from PDF 417 to PDF 449: the blank leaf after the last page of
Part I (PDF 417) and the front matter of Part II, pp. [I]-[XXXII] (PDF 418-449), with what each page holds and where
its record is. Writes page_disposition.tsv.  python write_disposition.py"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIND = {418: "half-title", 419: "blank verso of the half-title", 420: "title page", 421: "imprint (verso of the title)",
        449: "blank verso of p. XXXI"}
CONTENT = [(422, 427, "Praefatio"), (428, 432, "Conspectus librorum orientalium"),
           (433, 443, "Addenda et emendanda ad tomum primum"),
           (444, 444, "Addenda et emendanda ad tomum primum, concluded; ad tomum secundum, begun"),
           (445, 446, "Addenda et emendanda ad tomum secundum"),
           (447, 447, "Addenda et emendanda ad tomum secundum, concluded; Emendanda ad tomum tertium, begun"),
           (448, 448, "Emendanda ad tomum tertium, concluded; the tailpiece")]


def main():
    rows = [("417", "AB01-PDF0417", "", "blank leaf after Part I, p. 327",
             "no print: the edges of the binding and the mark of the digitization only, not imported; recorded blank",
             "")]
    for pdf in range(418, 450):
        rec = json.loads((HERE / "records" / f"AB01-PDF{pdf:04d}.json").read_text(encoding="utf-8"))
        n = sum(len(sec["lines"]) for sec in rec["sections"])
        kind = KIND.get(pdf)
        if kind is None:
            kind = next(c for lo, hi, c in CONTENT if lo <= pdf <= hi) if pdf >= 422 else ""
        disp = ("recorded blank, set as a blank page of the edition" if rec.get("blank")
                else f"transcribed: {n} anchored line{'' if n == 1 else 's'}")
        rows.append((str(pdf), rec["anchor"], rec["printed_page"], kind, disp, f"records/{rec['anchor']}.json"))
    with open(HERE / "page_disposition.tsv", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("master_pdf_page\tanchor\tprinted_page\tcontent\tdisposition\trecord\n")
        for r in rows:
            fh.write("\t".join(r) + "\n")
    print(len(rows), "pages")


if __name__ == "__main__":
    main()

"""Write page_disposition.tsv: every one of the 136 PDF pages of the article (Suhayl 9, pp. 13-148), its content and
what this session does with it. The Arabic pages are taken from the page files; the sections of the article from
its running heads and section headings. python write_disposition.py"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOT = "not reproduced (the article's own text, CC BY-NC-ND 3.0 ES)"
SECTIONS = [  # first PDF page, last PDF page, content, role, disposition
    (1, 4, "the article's title, abstract, introduction and notes on the edition, translation and commentary",
     "MODERN_EDITORIAL", "read as a comparator; " + NOT),
    (68, 119, "the commentary on the text and the 21 horoscopes",
     "MODERN_EDITORIAL", "read as a comparator; cited in the observations by the article's page; " + NOT),
    (120, 124, "the end of the commentary; Appendix A, recomputation of the horoscopes, from the middle of p. 132",
     "MODERN_EDITORIAL", "not used; " + NOT),
    (125, 131, "the end of Appendix A; Appendix B, analysis of the horoscopes, from the middle of p. 137",
     "MODERN_EDITORIAL", "not used; " + NOT),
    (132, 132, "the end of Appendix B; Appendix C, planetary parameters, from the middle of p. 144",
     "MODERN_EDITORIAL", "not used; " + NOT),
    (133, 136, "the end of Appendix C; the bibliography, from the middle of p. 145 to p. 148",
     "MODERN_EDITORIAL", "not used; " + NOT),
]


def main():
    rows = []
    recs = {int(p.stem[-4:]): json.loads(p.read_text(encoding="utf-8"))
            for p in sorted((HERE / "records").glob("AB02-PDF*.json"))}
    for pdf in range(1, 137):
        printed = str(pdf + 12)
        anchor = f"AB02-PDF{pdf:04d}"
        if pdf in recs:
            r = recs[pdf]
            charts = ", ".join(c["id"] for c in r["charts"])
            folios = [l["folio"] for l in r["lines"] if l["folio"]]
            if pdf == 5:
                content = "the title page of the edition: the Arabic title as an image, the English title below it"
                disp = "the Arabic title transcribed (3 lines); the English title not reproduced"
                role = "AB_SMALL_WORK (the title, as the edition prints it)"
            else:
                content = (f"the Arabic edition (page image), f. {folios[0]}: {len(r['lines'])} lines"
                           + ((", charts " if len(r["charts"]) > 1 else ", chart ") + charts if charts else "")
                           + f", {len(r['apparatus'])} line"
                           + ("s" if len(r["apparatus"]) != 1 else "") + " of apparatus")
                disp = ("transcribed: text, line numbers, folio, headings"
                        + ((", charts" if len(r["charts"]) > 1 else ", chart") if charts else "") + ", apparatus")
                role = "AB_SMALL_WORK; MODERN_EDITORIAL (apparatus, line numbers, brackets)"
            rows.append((pdf, anchor, printed, content, role, disp,
                         f"pages/{anchor}.txt"))
            continue
        if 7 <= pdf <= 67 and pdf % 2 == 1:
            rows.append((pdf, anchor, printed, "the English translation facing the Arabic page " + str(pdf + 11),
                         "MODERN_EDITORIAL", "read as a comparator; " + NOT, ""))
            continue
        for a, b, content, role, disp in SECTIONS:
            if a <= pdf <= b:
                rows.append((pdf, anchor, printed, content, role, disp, ""))
                break
        else:
            raise SystemExit(f"PDF {pdf} has no disposition")
    with open(HERE / "page_disposition.tsv", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("pdf_page\tanchor\tprinted_page\tcontent\trole\tdisposition\ttranscription\n")
        for r in rows:
            fh.write("\t".join(str(x) for x in r) + "\n")
    print(len(rows), "pages;", sum(1 for r in rows if r[6]), "transcribed")


if __name__ == "__main__":
    main()

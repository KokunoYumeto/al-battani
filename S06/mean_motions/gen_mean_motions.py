"""Generate the edition of Nallino's Part II pp. 19-23 (mean motions) from mm_p2.tsv and mm_pages.tsv: one page per
printed page, with the running head, the folio line, the framed table (Arabic and Latin title, the argument column
head set vertically, four motion heads), and the rows in groups of five; the first row carries the marks ° ′ ″ as
printed. Output: p2_mean_motions.tex"""
from pathlib import Path

from gen_stars import PREAMBLE, markup, read

HERE = Path(__file__).resolve().parent
GROUPS = ["sun", "moon", "anom", "node"]


def nl(s):
    return markup(s).replace(" / ", r"\\")


def ar(s):
    return r"\textarabic{" + s + "}"


def page_tex(page, rows):
    pp = int(page["ppage"])
    head = (r"\noindent\makebox[\textwidth]{\hfill{\scriptsize AL-BATTANI OPUS ASTRONOMICUM}\hfill\llap{" + str(pp) + "}}"
            if pp % 2 else r"\noindent\makebox[\textwidth]{\rlap{" + str(pp) + r"}\hfill{\scriptsize C. A. NALLINO}\hfill}")
    out = [r"\clearpage", head, r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{1mm}",
           r"\begin{center}{\small " + page["fol"] + r"}\end{center}\vspace{-3mm}"]
    months = rows[0]["table"] == "months"
    argw = "32mm" if months else "13mm"
    trip = r"r@{\hspace{1.5mm}}r@{\hspace{1.5mm}}r"
    spec = "|" + (r">{\raggedright\arraybackslash}p{" + argw + "}" if months else r">{\centering\arraybackslash}p{" + argw + "}") + \
           "|" + "|".join([trip] * 4) + "|"
    tl = page["title_la"].split(" / ")
    out.append(r"\begin{center}\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.05}\begin{tabular}{" + spec + r"}\hline\hline")
    out.append(r"\multicolumn{13}{||c||}{\parbox{150mm}{\centering\vspace{1mm}{\large " + ar(page["title_ar"]) + r"}\\\textbf{" +
               markup(tl[0]) + r"}\\\textbf{" + markup(tl[1]) + r"}\vspace{1mm}}} \\ \hline")
    heads = [h.split("/", 1) for h in page["heads"].split("|")]
    first = heads[0]
    if months:
        c0 = r"\parbox[c]{" + argw + r"}{\centering\scriptsize " + ar(first[0]) + r"\\" + nl(first[1].strip()) + "}"
    else:
        c0 = r"\rotatebox{90}{\scriptsize\begin{tabular}{@{}c@{}}" + ar(first[0]) + r"\\" + nl(first[1].strip()) + r"\end{tabular}}"
    cells = [c0] + [r"\multicolumn{3}{c|}{\parbox[c]{30mm}{\centering\scriptsize " + ar(a) + r"\\" + nl(l.strip()) + "}}"
                    for a, l in heads[1:]]
    out.append(" & ".join(cells) + r" \\ \hline\hline")
    for i, r in enumerate(rows):
        line = [nl(r["arg"])]
        for g in GROUPS:
            d, m, s = r[g + "_d"], r[g + "_m"], r[g + "_s"]
            if i == 0:
                d, m, s = d + r"\rlap{°}", m + r"\rlap{′}", s + r"\rlap{″}"
            line += [d, m, s]
        gap = ""
        if months:
            gap = r"[2.2mm]" if i < len(rows) - 2 else ""
        elif i % 5 == 4 and i < len(rows) - 1:
            gap = r"[1.2mm]"
        out.append(" & ".join(line) + r" \\" + gap)
    out.append(r"\hline\hline\end{tabular}\end{center}")
    return "\n".join(out)


def document():
    pages = read("mm_pages.tsv"); rows = read("mm_p2.tsv")
    out = [PREAMBLE.replace("margin=16mm", "margin=14mm"), r"\begin{document}"]
    for page in pages:
        out.append(page_tex(page, [r for r in rows if r["pdf"] == page["pdf"]]))
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p2_mean_motions.tex").write_text(document(), encoding="utf-8")
    print("wrote p2_mean_motions.tex")

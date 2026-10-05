"""Generate the edition of Nallino's Part II pp. 19-28 (mean motions) from mm_p2.tsv / mm_pages.tsv (pp. 19-23: four
motions in degrees, minutes and seconds) and mm5_p2.tsv / mm5_pages.tsv (pp. 24-28: five motions in degrees and
minutes): one page per printed page, with the running head, the folio line, the framed table (Arabic and Latin title,
the argument column head set vertically, the motion heads), and the rows in groups of five; each motion is one
centred column whose degrees, minutes and seconds stand in boxes of fixed width; the first row carries the marks
° ′ ″ as printed. Output: p2_mean_motions.tex"""
from pathlib import Path

from gen_stars import PREAMBLE, markup, read

HERE = Path(__file__).resolve().parent
SETS = [("mm_pages.tsv", "mm_p2.tsv", ["sun", "moon", "anom", "node"], 3),
        ("mm5_pages.tsv", "mm5_p2.tsv", ["sat", "jup", "mars", "ven", "mer"], 2)]
WIDTHS = r"\newlength{\Dw}\newlength{\Mw}\settowidth{\Dw}{000}\settowidth{\Mw}{00}"


def nl(s):
    return markup(s).replace(" / ", r"\\")


def ar(s):
    return r"\textarabic{" + s + "}"


def page_tex(page, rows, groups, places):
    pp = int(page["ppage"])
    head = (r"\noindent\makebox[\textwidth]{\hfill{\scriptsize AL-BATTANI OPUS ASTRONOMICUM}\hfill\llap{" + str(pp) + "}}"
            if pp % 2 else r"\noindent\makebox[\textwidth]{\rlap{" + str(pp) + r"}\hfill{\scriptsize C. A. NALLINO}\hfill}")
    out = [r"\clearpage", head, r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{1mm}",
           r"\begin{center}{\small " + page["fol"] + r"}\end{center}\vspace{-3mm}"]
    months = rows[0]["table"] == "months"
    argw = "32mm" if months else "13mm"
    headw = "30mm" if places == 3 else "26mm"
    ncol = 1 + len(groups)
    spec = "|" + (r">{\raggedright\arraybackslash}p{" + argw + "}" if months else r">{\centering\arraybackslash}p{" + argw + "}") + \
           "|" + "|".join([r">{\centering\arraybackslash}p{" + headw + "}"] * len(groups)) + "|"
    tl = page["title_la"].split(" / ")
    title = r"{\large " + ar(page["title_ar"]) + "}" + "".join(r"\\\textbf{" + markup(x) + "}" for x in tl)
    out.append(r"\begin{center}\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.05}\begin{tabular}{" + spec + r"}\hline\hline")
    out.append(r"\multicolumn{" + str(ncol) + r"}{||c||}{\parbox{150mm}{\centering\vspace{1mm}" + title + r"\vspace{1mm}}} \\ \hline")
    heads = [h.split("/", 1) for h in page["heads"].split("|")]
    first = heads[0]
    if months:
        c0 = r"\parbox[c]{" + argw + r"}{\centering\scriptsize " + ar(first[0]) + r"\\" + nl(first[1].strip()) + r"\par\vspace{0.7mm}}"
    else:
        c0 = r"\rotatebox{90}{\scriptsize\begin{tabular}{@{}c@{}}" + ar(first[0]) + r"\\" + nl(first[1].strip()) + r"\end{tabular}}"
    cells = [c0] + [r"\parbox[c]{" + headw + r"}{\centering\scriptsize " + ar(a) + r"\\" + nl(l.strip()) + r"\par\vspace{0.7mm}}"
                    for a, l in heads[1:]]
    out.append(" & ".join(cells) + r" \\ \hline\hline")
    tight_last = rows[-1]["arg"] == "bisext."          # p. 21: dhu 'l-hijjah comm. and bisext. are set close together
    marks = [r"\rlap{°}", r"\rlap{′}", r"\rlap{″}"]
    for i, r in enumerate(rows):
        line = [nl(r["arg"])]
        for g in groups:
            vals = [r[g + "_d"], r[g + "_m"]] + ([r[g + "_s"]] if places == 3 else [])
            if i == 0:
                vals = [v + marks[k] for k, v in enumerate(vals)]
            line.append(r"\hspace{2.6mm}".join(r"\makebox[" + (r"\Dw" if k == 0 else r"\Mw") + "][r]{" + v + "}"
                                               for k, v in enumerate(vals)))
        gap = ""
        if months:
            gap = r"[2.2mm]" if i < len(rows) - (2 if tight_last else 1) else ""
        elif i % 5 == 4 and i < len(rows) - 1:
            gap = r"[1.2mm]"
        out.append(" & ".join(line) + r" \\" + gap)
    out.append(r"\hline\hline\end{tabular}\end{center}")
    return "\n".join(out)


def document():
    out = [PREAMBLE.replace("margin=16mm", "margin=14mm"), WIDTHS, r"\begin{document}"]
    for pages_file, rows_file, groups, places in SETS:
        rows = read(rows_file)
        for page in read(pages_file):
            out.append(page_tex(page, [r for r in rows if r["pdf"] == page["pdf"]], groups, places))
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p2_mean_motions.tex").write_text(document(), encoding="utf-8")
    print("wrote p2_mean_motions.tex")

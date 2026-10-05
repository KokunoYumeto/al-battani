"""Generate the edition of Nallino's Part II pp. 9-18 (Tabulae I-X: the Hijra years 1-600 with the weekday of
1 Muharram, the Seleucid year and the Syrian day and month) from conc_p2.tsv and conc_pages.tsv: one page per printed
page, with the running head, the folio line, the framed table (Arabic and Latin title, column heads, two halves of
30 rows in groups of five), and the signature where one is printed.  Output: p2_concordance.tex"""
from pathlib import Path

from gen_stars import PREAMBLE, markup, read

HERE = Path(__file__).resolve().parent
LAT_HEADS = ["Anni hegirae.", "Nomen primi diei / mensis muḥarram.", "Anni aerae / Dhū ’l-qarnayn.",
             "Dies transacti / mensis Romani / in quem / incidit initium / mensis muḥarram."]


def nl(s):
    return markup(s).replace(" / ", r"\\")


def rot(text, ar=None):
    inner = (r"\textarabic{" + ar + r"}\\" if ar else "") + nl(text)
    return r"\rotatebox{90}{\scriptsize\begin{tabular}{@{}c@{}}" + inner + r"\end{tabular}}"


def head_cells(page, half):
    ar = page["heads_ar"].split("|") if (page["heads_ar"] and half == "L") else [None] * 4
    last = LAT_HEADS[3]
    if half == "R" and "no final period" in page["note"]:
        last = last.rstrip(".")
    four = r"\parbox[c]{30mm}{\centering\scriptsize " + (
        r"\textarabic{" + r"\\".join(ar[3].split(" / ")) + r"}\\" if ar[3] else "") + nl(last) + "}"
    return [rot(LAT_HEADS[0], ar[0]), rot(LAT_HEADS[1], ar[1]), rot(LAT_HEADS[2], ar[2]), r"\multicolumn{2}{c|}{" + four + "}"]


def page_tex(page, rows):
    pp = int(page["ppage"])
    head = (r"\noindent\makebox[\textwidth]{\hfill{\scriptsize AL-BATTANI OPUS ASTRONOMICUM}\hfill\llap{" + str(pp) + "}}"
            if pp % 2 else
            r"\noindent\makebox[\textwidth]{\rlap{" + str(pp) + r"}\hfill{\scriptsize C. A. NALLINO}\hfill}")
    out = [r"\clearpage", head, r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{1mm}",
           r"\begin{center}{\small " + page["fol"] + r"}\end{center}\vspace{-3mm}"]
    col = r"p{9mm}|>{\centering\arraybackslash}p{11mm}|>{\centering\arraybackslash}p{12mm}|r@{\hspace{2mm}}p{17mm}"
    spec = "|" + r">{\centering\arraybackslash}" + col + "||" + r">{\centering\arraybackslash}" + col + "|"
    tl = page["title_la"].split(" / ")
    out.append(r"\begin{center}\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.05}"
               r"\begin{tabular}{" + spec + r"}\hline\hline")
    out.append(r"\multicolumn{10}{||c||}{\parbox{150mm}{\centering\vspace{1mm}{\large\textarabic{" + page["title_ar"] +
               r"}}\\\textbf{" + markup(tl[0]) + r"}\\\textbf{" + markup(tl[1]) + r"}\vspace{1mm}}} \\ \hline")
    out.append(" & ".join(head_cells(page, "L") + head_cells(page, "R")) + r" \\ \hline\hline")
    L = [r for r in rows if r["half"] == "L"]; R = [r for r in rows if r["half"] == "R"]
    for i in range(30):
        cells = []
        for r in (L[i], R[i]):
            mon = r["month"]
            cells += [r["ah"], r["wd"], r["sy"], r["day"], (markup(mon) if mon != "»" else r"\hspace{3mm}»")]
        gap = r"[1.2mm]" if i % 5 == 4 and i < 29 else ""
        out.append(" & ".join(cells) + r" \\" + gap)
    out.append(r"\hline\hline\end{tabular}\end{center}")
    if page["signature"]:
        out.append(r"\vspace{-2mm}\noindent\hfill{\scriptsize " + page["signature"] + r"}\hspace{25mm}")
    return "\n".join(out)


def document():
    pages = read("conc_pages.tsv"); rows = read("conc_p2.tsv")
    out = [PREAMBLE.replace("margin=16mm", "margin=14mm"), r"\begin{document}"]
    for page in pages:
        out.append(page_tex(page, [r for r in rows if r["pdf"] == page["pdf"]]))
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p2_concordance.tex").write_text(document(), encoding="utf-8")
    print("wrote p2_concordance.tex")

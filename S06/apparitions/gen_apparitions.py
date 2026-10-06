"""Generate the edition of Nallino's Part II pp. 142-143 (the elongations for the apparitions and occultations of the
planets at latitude 36°) from apparitions_p2.tsv and apparitions_pages.tsv: one page per printed page, with the running
head, the folio line and the framed table (title; the head of the column of the signs; the heads of the planets, over
two columns on p. 143; the heads of the single columns; 12 rows, the first carrying the marks as printed).
Output: p2_apparitions.tex"""
from pathlib import Path

from gen_stars import PREAMBLE, markup, read

HERE = Path(__file__).resolve().parent
WIDTHS = r"\newlength{\Dw}\newlength{\Mw}\settowidth{\Dw}{00}\settowidth{\Mw}{00}"
THICK = r"!{\vrule width 1.1pt}"


def ar(s, sep=r"\\"):
    return sep.join(r"\textarabic{" + markup(x, False) + "}" for x in s.split(" / "))


def nl(s):
    return markup(s).replace(" / ", r"\\")


def running_head(pp):
    return (r"\noindent\makebox[\textwidth]{\hfill{\scriptsize AL-BATTANI OPUS ASTRONOMICUM}\hfill\llap{" + str(pp) + "}}"
            if pp % 2 else r"\noindent\makebox[\textwidth]{\rlap{" + str(pp) + r"}\hfill{\scriptsize C. A. NALLINO}\hfill}")


def dm(d, m, first):
    return (r"\makebox[\Dw][r]{" + d + (r"\rlap{°}" if first else "") + r"}\hspace{3mm}\makebox[\Mw][r]{" + m
            + (r"\rlap{′}" if first else "") + "}")


def page(pg, rows):
    pp = int(pg["ppage"])
    groups = []
    for g in pg["groups"].split("|"):
        cols, text = g.split(":", 1)
        groups.append((cols.split(), *text.split("‖")))
    order = [c for cols, _, _ in groups for c in cols]
    subs = [s.split("‖") for s in pg["subheads"].split("|")]
    narrow = len(order) == 8
    sw, nw = ("18mm", "22.5mm") if narrow else ("23mm", "30mm")
    col = r">{\centering\arraybackslash}p{" + sw + "}"
    spec = "||" + r">{\raggedright\arraybackslash}p{" + nw + "}" + THICK
    if narrow:
        spec += THICK.join(col + "|" + col for _ in groups) + "||"
    else:
        spec += THICK.join("|".join(col for _ in range(2)) for _ in range(3)) + "||"
    ncol = 1 + len(order)
    out = [r"\clearpage", running_head(pp), r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{2mm}",
           r"\begin{center}{\small " + pg["fol"] + r"}\end{center}\vspace{-2mm}",
           r"\begin{center}\setlength{\tabcolsep}{" + ("2pt" if narrow else "2.5pt") + r"}\renewcommand{\arraystretch}{1.1}\begin{tabular}{" + spec
           + r"}\hline\hline"]
    la = "".join(r"\\\textbf{" + markup(x) + "}" for x in pg["title_la"].split(" / "))
    out.append(r"\multicolumn{" + str(ncol) + r"}{||c||}{\parbox{" + ("170mm" if narrow else "165mm")
               + r"}{\centering\vspace{2mm}{\large " + ar(pg["title_ar"]) + "}" + la + r"\vspace{2mm}}} \\ \hline")
    sa, sl = pg["signs_head"].split("‖")
    signs = (r"\multicolumn{1}{||c" + THICK + r"}{\multirow{2}{*}{\parbox[c]{" + nw + r"}{\centering\small "
             + ar(sa) + r"\\{}" + nl(sl) + "}}}")
    if narrow:
        heads = []
        for k, (cols, ha, hl) in enumerate(groups):
            sep = "||" if k == len(groups) - 1 else THICK
            heads.append(r"\multicolumn{2}{c" + sep + r"}{\parbox[c][13mm][c]{37mm}{\centering\small " + ar(ha)
                         + r"\\{}" + nl(hl) + "}}")
        out.append(signs + " & " + " & ".join(heads) + r" \\ \cline{2-" + str(ncol) + "}")
        cells = []
        for a, l in subs:
            cells.append(r"\parbox[c][31mm][c]{" + sw + r"}{\centering\footnotesize " + ar(a, r"\\[0.3ex]")
                         + r"\\[0.6ex]\scriptsize\bfseries " + nl(l) + "}")
        out.append(r"\multicolumn{1}{||c" + THICK + "}{} & " + " & ".join(cells) + r" \\ \hline\hline")
    else:
        heads = []
        for k, (cols, ha, hl) in enumerate(groups):
            sep = "||" if k == len(groups) - 1 else (THICK if k % 2 else "|")
            heads.append(r"\multicolumn{1}{c" + sep + r"}{\parbox[c][15mm][c]{" + sw + r"}{\centering\small " + ar(ha)
                         + r"\\{}" + nl(hl) + "}}")
        out.append(signs + " & " + " & ".join(heads) + r" \\ \cline{2-" + str(ncol) + "}")
        cells = []
        for a, l in subs:
            cells.append(r"\parbox[c][11mm][c]{" + sw + r"}{\centering\scriptsize " + (ar(a) + r"\\{}" if a else "")
                         + r"\bfseries " + nl(l) + "}")
        out.append(r"\multicolumn{1}{||c" + THICK + "}{} & " + " & ".join(cells) + r" \\ \hline\hline")
    by_row = {}
    for r in rows:
        by_row.setdefault(int(r["row"]), {})[r["column"]] = r
    out.append(r"\multicolumn{1}{||c" + THICK + "}{}" + " &" * len(order) + r" \\[-2mm]")
    for i in sorted(by_row):
        rr = by_row[i]
        sign = next(iter(rr.values()))["sign"] + "."
        cells = [(r"\hspace{1mm}" if narrow else r"\hspace{1.5mm}") + sign] + [dm(rr[c]["d"], rr[c]["m"], i == 1) for c in order]
        out.append(" & ".join(cells) + r" \\[2.4mm]")
    out.append(r"\hline\hline\end{tabular}\end{center}")
    if pg["signature"]:
        out.append(r"\vspace{-2mm}\noindent\hfill{\small " + pg["signature"] + r"}\hspace*{14mm}")
    return "\n".join(out)


def document():
    pages = read("apparitions_pages.tsv"); rows = read("apparitions_p2.tsv")
    out = [PREAMBLE.replace("margin=16mm", "margin=13mm"), WIDTHS, r"\begin{document}"]
    for pg in pages:
        out.append(page(pg, [r for r in rows if r["ppage"] == pg["ppage"]]))
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p2_apparitions.tex").write_text(document(), encoding="utf-8", newline="\n")
    print("wrote p2_apparitions.tex")

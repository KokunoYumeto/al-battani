"""Generate the edition of Nallino's Part II pp. 108-137 (the equations of the five planets) from planets_p2.tsv and
planets_pages.tsv: one page per printed page, with the running head, the folio line, the line above the first table of
each planet, and the framed table (title, heads, 30 rows in groups of five; the first row carries the marks as printed;
the notes «Decrescunt» and «Crescunt» stand over the sixtieths where they begin), and the signature where one is printed.
Output: p2_planets.tex"""
from pathlib import Path

from gen_stars import PREAMBLE, markup, read

HERE = Path(__file__).resolve().parent
WIDTHS = r"\newlength{\Dw}\newlength{\Mw}\settowidth{\Dw}{000}\settowidth{\Mw}{00}"
W = {"n": "9mm", "n2": "10mm", "c3": "21mm", "c4": "19mm", "c5": "21mm", "c6": "22mm", "c7": "21mm"}


def ar(s):
    return r"\\".join(r"\textarabic{" + markup(x, False) + "}" for x in s.split(" / "))


def nl(s):
    return markup(s).replace(" / ", r"\\")


def running_head(pp):
    return (r"\noindent\makebox[\textwidth]{\hfill{\scriptsize AL-BATTANI OPUS ASTRONOMICUM}\hfill\llap{" + str(pp) + "}}"
            if pp % 2 else r"\noindent\makebox[\textwidth]{\rlap{" + str(pp) + r"}\hfill{\scriptsize C. A. NALLINO}\hfill}")


def dm(d, m, first):
    return (r"\makebox[\Dw][r]{" + d + (r"\rlap{°}" if first else "") + r"}\hspace{2.6mm}\makebox[\Mw][r]{" + m
            + (r"\rlap{′}" if first else "") + "}")


def head(a, l, w):
    text = (ar(a) + r"\\{}" if a else "") + nl(l)
    return r"\parbox[c][22mm][c]{" + w + r"}{\centering\scriptsize " + text + "}"


def page(pg, rows):
    pp = int(pg["ppage"])
    out = [r"\clearpage", running_head(pp), r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{1mm}",
           r"\begin{center}{\small " + pg["fol"] + r"}\end{center}\vspace{-3mm}"]
    if pg["above_ar"]:
        out.append(r"\begin{center}\textarabic{" + markup(pg["above_ar"], False) + r"}\\[1mm]{\small " + markup(pg["above_la"])
                   + r"}\end{center}\vspace{-2mm}")
    spec = "||" + "|".join(r">{\centering\arraybackslash}p{" + W[c] + "}" for c in W) + "||"
    out.append(r"\begin{center}\setlength{\tabcolsep}{2.5pt}\renewcommand{\arraystretch}{1.05}\begin{tabular}{" + spec
               + r"}\hline\hline")
    la = "".join(r"\\\textbf{" + markup(x) + "}" for x in pg["title_la"].split(" / "))
    out.append(r"\multicolumn{7}{||c||}{\parbox{150mm}{\centering\vspace{1mm}{\large " + ar(pg["title_ar"]) + "}" + la
               + r"\vspace{1mm}}} \\ \hline")
    hs = [h.split("‖") for h in pg["heads"].split("|")]
    top = (r"\multicolumn{2}{c|}{\parbox[c][16mm][c]{19mm}{\centering\scriptsize " + (ar(hs[0][0]) + r"\\{}" if hs[0][0] else "")
           + nl(hs[0][1]) + "}}")
    rest = [head(a, l, W[c]) for (a, l), c in zip(hs[3:], ("c3", "c4", "c5", "c6", "c7"))]
    out.append(top + " & " + " & ".join(rest) + r" \\ \cline{1-2}")
    sub = [r"\shortstack{\scriptsize " + (ar(a) + r"\\" if a else "") + r"\scriptsize " + nl(l) + "}" for a, l in hs[1:3]]
    out.append(" & ".join(sub) + " & & & & & " + r"\\ \hline\hline")
    notes = dict((int(x.split(":")[0]), x.split(":")[1]) for x in pg["notes"].split())
    for i, r in enumerate(rows):
        first = i == 0
        n = int(r["n"])
        c4 = r["c4"] + ("′" if first else "")
        if n in notes:
            c4 = r"\rule{0pt}{3.6ex}\makebox[0pt]{\raisebox{2.1ex}{\tiny " + notes[n] + "}}" + c4
        cells = [r["n"] + ("°" if first else ""), r["n2"] + ("°" if first else ""), dm(r["c3_d"], r["c3_m"], first), c4,
                 dm(r["c5_d"], r["c5_m"], first), dm(r["c6_d"], r["c6_m"], first), dm(r["c7_d"], r["c7_m"], first)]
        gap = r"[1.6mm]" if i % 5 == 4 and i < len(rows) - 1 else ""
        out.append(" & ".join(cells) + r" \\" + gap)
    out.append(r"\hline\hline\end{tabular}\end{center}")
    if pg["signature"]:
        out.append(r"\vspace{-2mm}\noindent\hfill{\small " + pg["signature"] + r"}\hspace*{14mm}")
    return "\n".join(out)


def document():
    pages = read("planets_pages.tsv"); rows = read("planets_p2.tsv")
    out = [PREAMBLE.replace("margin=16mm", "margin=13mm"), WIDTHS, r"\begin{document}"]
    for pg in pages:
        out.append(page(pg, [r for r in rows if r["ppage"] == pg["ppage"]]))
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p2_planets.tex").write_text(document(), encoding="utf-8", newline="\n")
    print("wrote p2_planets.tex")

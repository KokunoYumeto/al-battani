"""Generate the edition of Nallino's Part II pp. 93-101 (parallaxes; pp. 95-101 by gen_climes.py) from
parallax_p2.tsv and par_pages.tsv: one page per printed page, with the running head, the folio line and the framed table
(title, two levels of heads, rows in groups of four; each column a centred group of fixed-width numbers; the first row
carries the marks as printed). Output: p2_parallax.tex"""
import re
from pathlib import Path

from gen_stars import PREAMBLE, markup, read

HERE = Path(__file__).resolve().parent
WIDTHS = r"\newlength{\Dw}\newlength{\Mw}\settowidth{\Dw}{000}\settowidth{\Mw}{00}"
COLS = [("sun", 2), ("t1", 2), ("d2", 2), ("t3", 3), ("d4", 2), ("epa", 2), ("epp", 2), ("ecc", 2)]
WIDTH = {"arg": "9mm", "sun": "15mm", "t1": "16mm", "d2": "16mm", "t3": "21mm", "d4": "17mm", "epa": "17mm", "epp": "17mm",
         "ecc": "16mm"}


def nl(s):
    s = re.sub(r"\{sm:([^}]*)\}", lambda m: r"{\tiny " + m.group(1) + "}", s)
    return markup(s).replace(" / ", r"\\").replace(r"\\[", r"\\{}[")


def ar(s):
    return r"\\".join(r"\textarabic{" + markup(x, False) + "}" for x in s.split(" / "))


def nums(vals, marks=None):
    marks = marks or [""] * len(vals)
    return r"\hspace{2.2mm}".join(r"\makebox[\Mw][r]{" + v + "}" + (r"\rlap{" + m + "}" if m else "")
                                  for v, m in zip(vals, marks))


def running_head(pp):
    return (r"\noindent\makebox[\textwidth]{\hfill{\scriptsize AL-BATTANI OPUS ASTRONOMICUM}\hfill\llap{" + str(pp) + "}}"
            if pp % 2 else r"\noindent\makebox[\textwidth]{\rlap{" + str(pp) + r"}\hfill{\scriptsize C. A. NALLINO}\hfill}")


def head(a, l, w, rotate=False):
    text = (ar(a) + r"\\{}" if a else "") + nl(l)              # {} keeps a following [ from being an argument of \\
    if rotate:
        return r"\rotatebox{90}{\parbox{27mm}{\centering\tiny " + text + "}}"
    return r"\parbox[c][27mm][c]{" + w + r"}{\centering\scriptsize " + text + "}"


def page(pg, rows):
    pp = int(pg["ppage"])
    out = [r"\clearpage", running_head(pp), r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{1mm}",
           r"\begin{center}{\small " + pg["fol"] + r"}\end{center}\vspace{-3mm}"]
    spec = "||" + "|".join(r">{\centering\arraybackslash}p{" + WIDTH[c] + "}" for c in ["arg"] + [c for c, _ in COLS]) + "||"
    out.append(r"\begin{center}\setlength{\tabcolsep}{2.5pt}\renewcommand{\arraystretch}{1.05}\begin{tabular}{" + spec
               + r"}\hline\hline")
    la = "".join(r"\\\textbf{" + markup(x) + "}" for x in pg["title_la"].split(" / "))
    out.append(r"\multicolumn{9}{||c||}{\parbox{140mm}{\centering\vspace{1mm}{\large " + ar(pg["title_ar"]) + "}" + la
               + r"\vspace{1mm}}} \\ \hline")
    hs = [h.split("‖") for h in pg["heads"].split("|")]
    groups = [g.split(":")[0] for g in pg["groups"].split("|")]
    out.append(r" & & \multicolumn{4}{c|}{\small " + groups[0] + r"} & \multicolumn{3}{c||}{\small " + groups[1]
               + r"} \\ \cline{3-9}")
    out.append(head(*hs[0], WIDTH["arg"], rotate=True) + " & " + head(*hs[1], WIDTH["sun"]) + " & "
               + " & ".join(head(a, l, WIDTH[c]) for (a, l), (c, _) in zip(hs[2:], COLS[1:])) + r" \\ \hline\hline")
    for i, r in enumerate(rows):
        first = i == 0
        cells = [r["z"]]
        for c, n in COLS:
            vals = [r[f"{c}_{k}"] for k in range(1, n + 1)]
            marks = (["°", "′", "″"] if n == 3 else ["′", "″"]) if first else None
            cells.append(nums(vals, marks))
        gap = r"[1.2mm]" if i % 4 == 3 and i < len(rows) - 1 else ""
        out.append(" & ".join(cells) + r" \\" + gap)
    out.append(r"\hline\hline\end{tabular}\end{center}")
    return "\n".join(out)


def document():
    pages = read("par_pages.tsv"); rows = read("parallax_p2.tsv")
    out = [PREAMBLE.replace("margin=16mm", "margin=12mm"), WIDTHS, r"\begin{document}"]
    for pg in pages:
        out.append(page(pg, [r for r in rows if r["ppage"] == pg["ppage"]]))
    import gen_climes
    out += gen_climes.pages_tex(running_head)
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p2_parallax.tex").write_text(document(), encoding="utf-8", newline="\n")
    print("wrote p2_parallax.tex")

"""Generate the edition of Nallino's Part II pp. 140-141 (the latitudes of the planets) from latitudes_p2.tsv and
latitudes_pages.tsv: one page per printed page, with the running head, the folio line and the framed table (title, the
heads of the argument columns and of the planets, the heads of the two columns of each planet, 30 rows in groups of
five with a rule after 90°; the first row carries the marks as printed). The inscription in the right margin of p. 140
is set vertically beside the table. Output: p2_latitudes.tex"""
import re
from pathlib import Path

from gen_stars import PREAMBLE, markup, read

HERE = Path(__file__).resolve().parent
WIDTHS = r"\newlength{\Dw}\newlength{\Mw}\settowidth{\Dw}{00}\settowidth{\Mw}{00}"
THICK = r"!{\vrule width 1.1pt}"
GREEK = re.compile(r"([Ͱ-Ͽἀ-῿]+)")


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
    heads = []
    for h in pg["heads"].split("|"):
        keys, text = h.split(":", 1)
        heads.append((keys.split(), *text.split("‖")))
    subs = [s.split("‖") for s in pg["subheads"].split("|")]
    order = [k for keys, _, _ in heads for k in keys]
    single = [keys for keys, _, _ in heads if len(keys) == 1]
    sw = "23mm" if len(order) == 6 else "25mm"
    out = [r"\clearpage", running_head(pp), r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{1mm}",
           r"\begin{center}{\small " + pg["fol"] + r"}\end{center}\vspace{-3mm}"]
    col = r">{\centering\arraybackslash}p{" + sw + "}"
    groups = []
    for keys, _, _ in heads:
        groups.append("|".join(col for _ in keys))
    spec = ("||" + r">{\centering\arraybackslash}p{9mm}|>{\centering\arraybackslash}p{10mm}" + THICK
            + THICK.join(groups) + "||")
    ncol = 2 + len(order)
    out.append(r"\begin{center}\setlength{\tabcolsep}{2.5pt}\renewcommand{\arraystretch}{1.08}\makebox[\textwidth]{"
               r"\begin{tabular}{" + spec + r"}\hline\hline")
    la = "".join(r"\\\textbf{" + markup(x) + "}" for x in pg["title_la"].split(" / "))
    out.append(r"\multicolumn{" + str(ncol) + r"}{||c||}{\parbox{160mm}{\centering\vspace{1.5mm}{\large "
               + ar(pg["title_ar"]) + "}" + la + r"\vspace{1.5mm}}} \\ \hline")
    a, l = pg["arg_head"].split("‖")
    cells = [r"\multicolumn{2}{||c" + THICK + r"}{\multirow{3}{*}{\parbox[c]{20mm}{\centering\scriptsize "
             + ar(a, r"\\[0.4ex]") + r"\\[0.3ex]" + nl(l) + "}}}"]
    for k, (keys, ha, hl) in enumerate(heads):
        sep = "||" if k == len(heads) - 1 else THICK
        w = f"{2 * 23 + 5}mm" if len(keys) == 2 else sw
        body = (r"\parbox[c][18mm][c]{" + w + r"}{\centering\footnotesize " + ar(ha, r"\\[0.2ex]") + r"\\[0.3ex]"
                + nl(hl) + "}")
        if len(keys) == 1:
            body = r"\multirow{3}{*}{\parbox[c]{" + sw + r"}{\centering\footnotesize " + ar(ha, r"\\[0.2ex]") \
                   + r"\\[0.3ex]" + nl(hl) + "}}"
        cells.append(r"\multicolumn{" + str(len(keys)) + "}{c" + sep + "}{" + body + "}")
    last_pair = 2 + sum(len(k) for k, _, _ in heads if len(k) == 2)
    out.append(" & ".join(cells) + r" \\ \cline{3-" + str(last_pair) + "}")
    subcells = [r"\multicolumn{2}{||c" + THICK + "}{}"]
    si = 0
    for keys, _, _ in heads:
        if len(keys) == 1:
            subcells.append("")
            continue
        for _ in keys:
            sa, sl = subs[si]; si += 1
            subcells.append(r"\parbox[c][9mm][c]{" + sw + r"}{\centering\small " + (ar(sa) + r"\\{}" if sa else "")
                            + nl(sl) + "}")
    out.append(" & ".join(subcells) + r" \\ \hline\hline")
    by_n = {}
    for r in rows:
        by_n.setdefault(int(r["n"]), {})[r["column"]] = r
    for i, n in enumerate(sorted(by_n)):
        first = i == 0
        rr = by_n[n]
        any_r = next(iter(rr.values()))
        cells = [str(n) + ("°" if first else ""), any_r["n2"] + ("°" if first else "")]
        cells += [dm(rr[c]["d"], rr[c]["m"], first) for c in order]
        if n == 96:
            cells[0] = r"\rule{0pt}{3.4ex}" + cells[0]
        if n == 90:
            end = r" \\[0.9mm] \hline"
        elif i % 5 == 4 and i < len(by_n) - 1:
            end = r" \\[1.6mm]"
        else:
            end = r" \\"
        out.append(" & ".join(cells) + end)
    out.append(r"\hline\hline\end{tabular}")
    if pg["margin"]:
        ma, ml = pg["margin"].split("‖")
        ml = GREEK.sub(lambda m: r"\textgreek{" + m.group(1) + "}", markup(ml))
        out.append(r"\rlap{\hspace{1.5mm}\raisebox{3.2cm}[0pt][0pt]{\rotatebox{-90}{\small \textarabic{" + markup(ma, False)
                   + r"}\quad " + ml + "}}}")
    out.append(r"}\end{center}")
    if pg["signature"]:
        out.append(r"\vspace{-2mm}\noindent\hfill{\small " + pg["signature"] + r"}\hspace*{14mm}")
    return "\n".join(out)


def document():
    pages = read("latitudes_pages.tsv"); rows = read("latitudes_p2.tsv")
    out = [PREAMBLE.replace("margin=16mm", "margin=13mm"), WIDTHS, r"\begin{document}"]
    for pg in pages:
        out.append(page(pg, [r for r in rows if r["ppage"] == pg["ppage"]]))
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p2_latitudes.tex").write_text(document(), encoding="utf-8", newline="\n")
    print("wrote p2_latitudes.tex")

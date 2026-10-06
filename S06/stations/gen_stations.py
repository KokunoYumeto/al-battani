"""Generate the edition of Nallino's Part II pp. 138-139 (the stations of the planets) from stations_p2.tsv and
stations_pages.tsv: one page per printed page, with the running head, the folio line and the framed table (title, the
heads of the argument columns, of the planets and of the two stations, 30 rows in groups of five; the first row carries
the marks as printed). Output: p2_stations.tex"""
from pathlib import Path

from gen_stars import PREAMBLE, markup, read

HERE = Path(__file__).resolve().parent
WIDTHS = r"\newlength{\Dw}\newlength{\Mw}\settowidth{\Dw}{000}\settowidth{\Mw}{00}"
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
    planets = [p.split(":", 1) for p in pg["planets"].split("|")]
    stations = [s.split("‖") for s in pg["stations"].split("|")]
    sw = "23mm" if len(planets) == 3 else "36mm"
    out = [r"\clearpage", running_head(pp), r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{1mm}",
           r"\begin{center}{\small " + pg["fol"] + r"}\end{center}\vspace{-3mm}"]
    col = r">{\centering\arraybackslash}p{" + sw + "}"
    spec = ("||" + r">{\centering\arraybackslash}p{9mm}|>{\centering\arraybackslash}p{10mm}" + THICK
            + THICK.join(col + "|" + col for _ in planets) + "||")
    ncol = 2 + 2 * len(planets)
    out.append(r"\begin{center}\setlength{\tabcolsep}{2.5pt}\renewcommand{\arraystretch}{1.08}\begin{tabular}{" + spec
               + r"}\hline\hline")
    la = "".join(r"\\\textbf{" + markup(x) + "}" for x in pg["title_la"].split(" / "))
    out.append(r"\multicolumn{" + str(ncol) + r"}{||c||}{\parbox{" + ("165mm" if len(planets) == 3 else "160mm")
               + r"}{\centering\vspace{1.5mm}{\large " + ar(pg["title_ar"]) + "}" + la + r"\vspace{1.5mm}}} \\ \hline")
    a, l = pg["arg_head"].split("‖")
    arg = (r"\multicolumn{2}{||c" + THICK + r"}{\multirow{3}{*}{\parbox[c]{20mm}{\centering\scriptsize "
           + ar(a, r"\\[0.4ex]") + r"\\[0.3ex]" + nl(l) + "}}}")
    tops = []
    for k, (key, text) in enumerate(planets):
        pa, pl = text.split("‖")
        sep = "||" if k == len(planets) - 1 else THICK
        tops.append(r"\multicolumn{2}{c" + sep + r"}{\parbox[c][14mm][c]{40mm}{\centering\small " + ar(pa) + r"\\{}"
                    + nl(pl) + "}}")
    out.append(arg + " & " + " & ".join(tops) + r" \\ \cline{3-" + str(ncol) + "}")
    subs = [r"\parbox[c][9mm][c]{" + sw + r"}{\centering\small " + (ar(sa) + r"\\{}" if sa else "") + nl(sl) + "}"
            for sa, sl in stations]
    out.append(r"\multicolumn{2}{||c" + THICK + "}{} & " + " & ".join(subs) + r" \\ \hline\hline")
    by_n = {}
    for r in rows:
        by_n.setdefault(int(r["n"]), {})[r["planet"]] = r
    for i, n in enumerate(sorted(by_n)):
        first = i == 0
        rr = by_n[n]
        any_r = next(iter(rr.values()))
        cells = [str(n) + ("°" if first else ""), any_r["n2"] + ("°" if first else "")]
        for key, _ in planets:
            r = rr[key]
            cells += [dm(r["s1_d"], r["s1_m"], first), dm(r["s2_d"], r["s2_m"], first)]
        gap = r"[1.6mm]" if i % 5 == 4 and i < len(by_n) - 1 else ""
        out.append(" & ".join(cells) + r" \\" + gap)
    out.append(r"\hline\hline\end{tabular}\end{center}")
    if pg["signature"]:
        out.append(r"\vspace{-2mm}\noindent\hfill{\small " + pg["signature"] + r"}\hspace*{14mm}")
    return "\n".join(out)


def document():
    pages = read("stations_pages.tsv"); rows = read("stations_p2.tsv")
    out = [PREAMBLE.replace("margin=16mm", "margin=13mm"), WIDTHS, r"\begin{document}"]
    for pg in pages:
        out.append(page(pg, [r for r in rows if r["ppage"] == pg["ppage"]]))
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p2_stations.tex").write_text(document(), encoding="utf-8", newline="\n")
    print("wrote p2_stations.tex")

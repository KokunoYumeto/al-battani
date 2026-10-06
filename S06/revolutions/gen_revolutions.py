"""Generate the edition of Nallino's Part II pp. 187-188 from revolutions_p2.tsv and revolutions_pages.tsv: p. 187, the
increments of the mean motions for the revolutions of the years (heads set upright as printed, turned through 90°);
p. 188, the table of the revolutions of the years beside the tables of the hours (altitudes) and of the directions of
the hours. The first row of each table carries the marks as printed. Output: p2_revolutions.tex"""
from pathlib import Path

from gen_stars import PREAMBLE, markup, read

HERE = Path(__file__).resolve().parent
EXTRA = r"\newlength{\Dw}\newlength{\Mw}\settowidth{\Dw}{000}\settowidth{\Mw}{00}"


def ar(s, sep=r"\\"):
    return sep.join(r"\textarabic{" + markup(x, False) + "}" for x in s.split(" / "))


def nl(s):
    return markup(s).replace(" / ", r"\\")


def running_head(pp):
    return (r"\noindent\makebox[\textwidth]{\hfill{\scriptsize AL-BATTANI OPUS ASTRONOMICUM}\hfill\llap{" + str(pp) + "}}"
            if pp % 2 else r"\noindent\makebox[\textwidth]{\rlap{" + str(pp) + r"}\hfill{\scriptsize C. A. NALLINO}\hfill}")


def dm(d, m, first, dw=r"\Dw"):
    return (r"\makebox[" + dw + "][r]{" + d + (r"\rlap{°}" if first else "") + r"}\hspace{2.5mm}\makebox[\Mw][r]{" + m
            + (r"\rlap{′}" if first else "") + "}")


def turned(a, l, height, width):
    """a head set along the column, read from the foot upwards"""
    text = (r"\textarabic{" + markup(a, False) + r"}\\{}" if a else "") + nl(l)
    return (r"\rotatebox{90}{\parbox[c]{" + height + r"}{\centering\scriptsize " + text + r"}}")


def page187(pg, rows):
    heads = [h.split("‖") for h in pg["heads"].split("|")]
    cols = ["moon", "moon_anom", "node", "sat", "jup", "mars", "ven_anom", "mer_anom"]
    spec = r"||>{\centering\arraybackslash}p{9mm}" + r"|>{\centering\arraybackslash}p{16mm}" * 8 + "||"
    out = [r"\clearpage", running_head(187), r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{1mm}",
           r"\begin{center}{\small " + pg["fol"] + r"}\end{center}\vspace{-3mm}",
           r"\begin{center}\setlength{\tabcolsep}{3.2pt}\renewcommand{\arraystretch}{1.1}\begin{tabular}{" + spec
           + r"}\hline\hline"]
    la = "".join(r"\\\textbf{" + markup(x) + "}" for x in pg["title_la"].split(" / "))
    out.append(r"\multicolumn{9}{||c||}{\parbox{150mm}{\centering\vspace{2mm}{\Large " + ar(pg["title_ar"]) + "}" + la
               + r"\vspace{2mm}}} \\ \hline")
    out.append(" & ".join(turned(a, l, "40mm", "") for a, l in heads) + r" \\ \hline\hline")
    by_n = {}
    for r in rows:
        by_n.setdefault(int(r["arg"]), {})[r["column"]] = r
    for n in sorted(by_n):
        rr = by_n[n]
        cells = [r"\rule{0pt}{8.5mm}\textbf{" + str(n) + "}"] + [dm(rr[c]["d"], rr[c]["m"], n == 1) for c in cols]
        out.append(" & ".join(cells) + r" \\")
    out.append(r"\hline\hline\end{tabular}\end{center}")
    return "\n".join(out)


def page188(pg, rows):
    t_ar = pg["title_ar"].split("‖"); t_la = pg["title_la"].split("‖")
    heads = [h.split("‖") for h in pg["heads"].split("|")]
    years = {(r["column"], int(r["arg"])): r for r in rows if r["table"] == "years"}
    alt = {(r["column"], int(r["arg"])): r for r in rows if r["table"] == "altitude"}
    dirs = {(r["column"], int(r["arg"])): r for r in rows if r["table"] == "direction"}
    # left: the revolutions of the years; each collected line spans two single lines
    L = [r"\begin{tabular}[t]{|c|c||c|c|}\hline",
         r"\multicolumn{4}{|c|}{\parbox{68mm}{\centering\vspace{2mm}{\large " + ar(t_ar[0]) + r"}\\\textbf{"
         + nl(t_la[0]) + r"}\vspace{2mm}}} \\ \hline"]
    L.append(" & ".join(turned(a, l, "27mm", "") for a, l in heads[:4]) + r" \\ \hline\hline")
    for k in range(1, 21):
        cells = []
        if k % 2 == 1:
            c = years[("collected", (k + 1) * 10)]
            cells += [r"\multirow{2}{*}{" + c["arg"] + "}",
                      r"\multirow{2}{*}{" + dm(c["d"], c["m"], k == 1) + "}"]
        else:
            cells += ["", ""]
        s = years[("single", k)]
        cells += [s["arg"], dm(s["d"], s["m"], k == 1)]
        L.append(" & ".join(cells) + r" \\[1.2mm]")
    L.append(r"\hline\end{tabular}")
    # right: the hours
    Rt = [r"\begin{tabular}[t]{|c|c|c|}\hline",
          r"\multicolumn{3}{|c|}{\parbox{80mm}{\centering\vspace{2mm}{\large " + ar(t_ar[1]) + r"}\\[1mm]\textbf{"
          + nl(t_la[1]) + r"}\vspace{2mm}}} \\ \hline"]
    h_ar, h_la = heads[4]
    Rt.append(turned(h_ar, h_la, "18mm", "") + " & "
              + " & ".join(r"\parbox[c][20mm][c]{34mm}{\centering\small " + ar(a, r"\\[1.2ex]") + r"\\{}" + nl(l) + "}"
                           if False else r"\parbox[c][20mm][c]{34mm}{\centering\small "
                           + r"\textarabic{" + markup(a.split(" / ")[0], False) + r"}\\" + nl(l.split(" / ")[0])
                           + r"\\[2ex]\textarabic{" + markup(a.split(" / ")[1], False) + r"}\\" + nl(l.split(" / ")[1]) + "}"
                           for a, l in heads[5:7]) + r" \\ \hline\hline")
    for k in range(1, 13):
        Rt.append(" & ".join([str(k), dm(alt[("cap", k)]["d"], alt[("cap", k)]["m"], k == 1, r"\Mw"),
                              dm(alt[("can", k)]["d"], alt[("can", k)]["m"], k == 1, r"\Mw")]) + r" \\")
    Rt.append(r"\hline\hline")
    Rt.append(r"\multicolumn{3}{|c|}{\parbox{80mm}{\centering\vspace{3mm}{\large " + ar(t_ar[2]) + r"}\\[1mm]\textbf{"
              + nl(t_la[2]) + r"}\vspace{3mm}}} \\ \hline")
    n_ar, n_la = heads[7]
    Rt.append(turned(n_ar, n_la, "22mm", "") + " & "
              + " & ".join(r"\parbox[c][24mm][c]{37mm}{\centering\small \textarabic{" + markup(a.split(" / ")[0], False)
                           + r"}\\" + nl(l.split(" / ")[0]) + r"\\[2ex]\textarabic{" + markup(a.split(" / ")[1], False)
                           + r"}\\" + nl(l.split(" / ")[1]) + "}" for a, l in heads[8:10]) + r" \\ \hline\hline")

    def dms(r, first):
        return (r"\makebox[\Mw][r]{" + r["d"] + (r"\rlap{°}" if first else "") + r"}\hspace{1.6mm}\makebox[\Mw][r]{"
                + r["m"] + (r"\rlap{′}" if first else "") + r"}\hspace{1.6mm}\makebox[\Mw][r]{" + r["s"]
                + (r"\rlap{″}" if first else "") + r"}\hspace{1.5mm}\makebox[13.5mm][l]{\footnotesize [" + r["quarter"] + "]}")
    for k in range(1, 7):
        Rt.append(" & ".join([str(k), dms(dirs[("can", k)], k == 1), dms(dirs[("cap", k)], k == 1)]) + r" \\")
    Rt.append(r"\hline\end{tabular}")
    out = [r"\clearpage", running_head(188), r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{1mm}",
           r"\begin{center}{\small " + pg["fol"] + r"}\end{center}\vspace{-3mm}",
           r"\begin{center}\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.1}",
           "\n".join(L), r"\hspace{1mm}", "\n".join(Rt), r"\end{center}"]
    return "\n".join(out)


def document():
    pages = read("revolutions_pages.tsv"); rows = read("revolutions_p2.tsv")
    out = [PREAMBLE.replace("margin=16mm", "margin=13mm"), EXTRA, r"\begin{document}"]
    for pg in pages:
        rr = [r for r in rows if r["ppage"] == pg["ppage"]]
        out.append(page187(pg, rr) if pg["ppage"] == "187" else page188(pg, rr))
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p2_revolutions.tex").write_text(document(), encoding="utf-8", newline="\n")
    print("wrote p2_revolutions.tex")

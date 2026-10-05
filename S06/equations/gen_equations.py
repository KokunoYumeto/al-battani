"""Generate the edition of Nallino's Part II pp. 78-83 (equation of the Sun; simple equation of the Moon, equation of
the anomaly, minutes to be added, least longinquity; latitude of the Moon) from equations_p2.tsv and
equations_pages.tsv: one page per printed page, with the running head, the folio line, the framed table (Arabic and
Latin title, the two-level heads) and the rows in groups of five; each column is centred, with its numbers in boxes of
fixed width; the first row carries the marks as printed. Output: p2_equations.tex"""
from pathlib import Path

from gen_stars import PREAMBLE, read
from gen_stars import markup as _markup

HERE = Path(__file__).resolve().parent
WIDTHS = r"\newlength{\Dw}\newlength{\Mw}\settowidth{\Dw}{000}\settowidth{\Mw}{00}"


def markup(s):
    return _markup(s).replace(" / ", r"\\")


def ar(s):
    return r"\textarabic{" + s + "}"


def num(vals, marks=None, gap="1.6mm"):
    vals = [v + (r"\rlap{" + m + "}" if m else "") for v, m in zip(vals, marks or [""] * len(vals))]
    return (r"\hspace{" + gap + "}").join(r"\makebox[" + (r"\Dw" if k == 0 else r"\Mw") + "][r]{" + v + "}"
                                          for k, v in enumerate(vals))


def head(a, l, w):
    return r"\parbox[c]{" + w + r"}{\centering\scriptsize " + (ar(a) + r"\\" if a else "") + markup(l) + r"\par\vspace{0.5mm}}"


def vhead(a, l):
    """a head set vertically, as printed («Portiones longinquit.»)"""
    inner = (ar(a) + r"\\" if a else "") + markup(l)
    return r"\rotatebox{90}{\scriptsize\begin{tabular}{@{}c@{}}" + inner + r"\end{tabular}}"


W = {"n": "9mm", "inv": "9mm", "sun": "20mm", "moon": "20mm", "pro": "15mm", "min": "11mm", "inc": "15mm", "lat": "20mm"}


def page_tex(p, rows):
    pp = int(p["ppage"])
    rh = (r"\noindent\makebox[\textwidth]{\hfill{\scriptsize AL-BATTANI OPUS ASTRONOMICUM}\hfill\llap{" + str(pp) + "}}"
          if pp % 2 else r"\noindent\makebox[\textwidth]{\rlap{" + str(pp) + r"}\hfill{\scriptsize C. A. NALLINO}\hfill}")
    out = [r"\clearpage", rh, r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{1mm}",
           r"\begin{center}{\small " + p["fol"] + r"}\end{center}\vspace{-3mm}"]
    cols = ["n", "inv", "sun", "moon", "pro", "min", "inc", "lat"]
    spec = "||" + "|".join(r">{\centering\arraybackslash}p{" + W[c] + "}" for c in cols) + "||"
    la = "".join(r"\\\textbf{" + _markup(x) + "}" for x in p["title_la"].split(" / "))
    out.append(r"\begin{center}\setlength{\tabcolsep}{2.5pt}\renewcommand{\arraystretch}{1.0}\begin{tabular}{" + spec + r"}\hline")
    out.append(r"\multicolumn{8}{||c||}{\parbox{176mm}{\centering\vspace{1mm}{\large " + ar(p["title_ar"]) + "}" + la +
               r"\vspace{1mm}}} \\ \hline")
    H = [h.split("‖") for h in p["heads"].split("|")]          # numerorum, rectus, inversus, sun, moon, anomaly,
    #                                                            portiones, minuta, longinquitas, latitude
    tall = lambda a, l, w: r"\multirow{2}{*}{" + head(a, l, w) + "}"
    out.append(r"\multicolumn{2}{||c|}{" + head(H[0][0], H[0][1], "20mm") + "} & " + tall(*H[3], W["sun"]) + " & " +
               tall(*H[4], W["moon"]) + " & " + tall(*H[5], W["pro"]) + " & " + vhead(H[6][0], H[6][1]) + " & " +
               tall(*H[8], W["inc"]) + " & " + tall(*H[9], W["lat"]) + r" \\ \cline{1-2}\cline{6-6}")
    out.append(head(H[1][0], H[1][1], W["n"]) + " & " + head(H[2][0], H[2][1], W["inv"]) + " & & & & " +
               head(H[7][0], H[7][1], W["min"]) + r" & & \\ \hline\hline")
    for i, r in enumerate(rows):
        first = i == 0
        m3 = ["°", "′", "″"] if first else None
        m2 = ["°", "′"] if first else None
        line = [r["n"], r["n_inv"],
                num([r["sun_d"], r["sun_m"], r["sun_s"]], m3), num([r["moon_d"], r["moon_m"], r["moon_s"]], m3),
                num([r["pro_d"], r["pro_m"]], m2), r["min"] + (r"\rlap{′}" if first else ""),
                num([r["inc_d"], r["inc_m"]], m2), num([r["lat_d"], r["lat_m"], r["lat_s"]], m3)]
        out.append(" & ".join(line) + r" \\" + (r"[1.2mm]" if i % 5 == 4 and i < len(rows) - 1 else ""))
    out.append(r"\hline\end{tabular}\end{center}")
    return "\n".join(out)


def document():
    pages = read("equations_pages.tsv"); rows = read("equations_p2.tsv")
    out = [PREAMBLE.replace("margin=16mm", "margin=12mm"), WIDTHS, r"\begin{document}"]
    for p in pages:
        out.append(page_tex(p, [r for r in rows if r["pdf"] == p["pdf"]]))
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p2_equations.tex").write_text(document(), encoding="utf-8", newline="\n")
    print("wrote p2_equations.tex")

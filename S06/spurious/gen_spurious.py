"""Generate the edition of Nallino's Part II pp. 297 and 300-307 (the half-title «Tabulae spuriae» and the spurious
tables) from spurious_p2.tsv and spurious_heads.tsv: one page per printed page, with the running head, the folio line
and the framed table; heads set along their columns where they are so printed (read from the foot upwards); the month
blocks of pp. 300, 301 and 305 placed beside the rows as printed, evenly spaced from the first month to the last.
p. 299 (the astrological figure) is in S13. Output: p2_spurious.tex
The head rows have fixed heights (struts), so that a head spanning two of them can be hung from the first: hang()."""
from pathlib import Path

from gen_stars import PREAMBLE, markup, read

HERE = Path(__file__).resolve().parent
EXTRA = r"""\newlength{\Dw}\newlength{\Mw}\settowidth{\Dw}{000}\settowidth{\Mw}{00}
\setlength{\unitlength}{1mm}"""
TH = r"!{\vrule width 1.1pt}"
R = 5.6                                       # row pitch (mm) of the tables with a month block
STRUT = r"\rule[-1.6mm]{0pt}{5.6mm}"


def rcol(w):
    return r">{\raggedleft\arraybackslash}p{" + str(w) + "mm}"


def ccol(w):
    return r">{\centering\arraybackslash}p{" + str(w) + "mm}"


def lcol(w):
    return r">{\raggedright\arraybackslash}p{" + str(w) + "mm}"


def strut(above, below):
    return rf"\rule[-{below}mm]{{0pt}}{{{above + below}mm}}"


def ar(s, sep=r"\\"):
    return sep.join(r"\textarabic{" + markup(x, False) + "}" for x in s.split(" / "))


def nl(s):
    return markup(s).replace(" / ", r"\\{}")               # {} keeps a following «[» from being read as an argument


def running_head(pp):
    return (r"\noindent\makebox[\textwidth]{\hfill{\scriptsize AL-BATTANI OPUS ASTRONOMICUM}\hfill\llap{" + str(pp) + "}}"
            if pp % 2 else r"\noindent\makebox[\textwidth]{\rlap{" + str(pp) + r"}\hfill{\scriptsize C. A. NALLINO}\hfill}")


H = {(h["ppage"], h["key"]): (h["ar"], h["la"]) for h in read("spurious_heads.tsv")}
D = read("spurious_p2.tsv")


def table(pp, name):
    """{arg: {column: value}} in the order printed"""
    out = {}
    for r in D:
        if r["ppage"] == pp and r["table"] == name:
            out.setdefault(r["arg"], {})[r["column"]] = r["value"]
    return out


def head(pp, key, size=r"\scriptsize", sep=r"\\{}"):
    a, l = H[(pp, key)]
    return (ar(a) + sep if a else "") + size + " " + nl(l)


def turned(pp, key, length, size=r"\scriptsize"):
    """a head set along the column, read from the foot upwards"""
    return r"\rotatebox{90}{\parbox[c]{" + length + r"}{\centering" + size + " " + head(pp, key, "") + "}}"


def hang(box, below):
    """a box hung from the baseline of the first of two head rows, its foot `below` mm under that baseline"""
    return r"\smash{\raisebox{-" + f"{below}mm" + "}{" + box + "}}"


def start(pp):
    fol = H[(str(pp), "fol")][1]
    return [r"\clearpage", running_head(pp), r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{1mm}",
            r"\begin{center}{\small " + fol + r"}\end{center}\vspace{-3mm}"]


def title(pp, key, ncol, width, spec="||c||"):
    a, l = H[(pp, key)]
    la = "".join(r"\\\textbf{" + markup(x) + "}" for x in l.split(" / "))
    return (r"\multicolumn{" + str(ncol) + "}{" + spec + r"}{\parbox{" + width + r"}{\centering\vspace{2mm}{\large "
            + ar(a) + "}" + la + r"\vspace{2mm}}}")


def spread(entries, first, last, width, align="c", y0=0.0, ypos=None, rule=None):
    """the entries of a month block as a zero-size picture placed in a cell of the first row: entry k with its baseline
    (first + k (last - first) / (n - 1)) rows below the baseline of that row (or at ypos[k] mm below it). In a centred
    column the picture stands at the middle of the cell, in a left-aligned one (align "l") at its left edge; rule: the
    depth (mm) of a horizontal rule across the cell"""
    n = len(entries)
    x = 0.0 if align == "l" else -width / 2
    out = [r"\begin{picture}(0,0)"]
    for k, e in enumerate(entries):
        y = ypos[k] if ypos else (first + k * (last - first) / (n - 1)) * R
        out.append(rf"\put({x:.2f},{-(y - y0):.2f}){{\makebox[{width}mm][{align}]{{{e}}}}}")
    if rule is not None:                              # across the cell, \tabcolsep (1.8pt) on either side
        out.append(rf"\put({x - 0.63:.2f},{-rule:.2f}){{\line(1,0){{{width + 1.26:.2f}}}}}")
    out.append(r"\end{picture}")
    return "".join(out)


MONTHS = ["al-muḥarram", "ṣafar", "rabīʿ I", "rabīʿ II", "ǵumādà I", "ǵumādà II", "raǵab", "shaʿbān", "ramaḍān",
          "shawwāl", "dhū ’l-qaʿdah", "dhū ’l-ḥiǵǵah"]


def page297():
    return "\n".join([r"\clearpage", r"\vspace*{95mm}", r"\begin{center}{\LARGE " + H[("297", "halftitle")][1]
                      + r"}\end{center}", r"\vfill\noindent\hfill{\small " + H[("297", "signature")][1]
                      + r"}\hspace*{30mm}\vspace*{20mm}"])


def page300():
    T = table("300", "decades"); M = table("300", "months")
    w = {"arg": 13, "dec": 9, "s": 7, "days": 13, "names": 27, "sign": 8}
    spec = ("||" + ccol(w["arg"]) + "|" + ccol(w["dec"]) + "||" + "|".join([ccol(w["s"])] * 9) + "||"
            + ccol(w["days"]) + "|" + lcol(w["names"]) + "|" + ccol(w["sign"]) + "||")
    out = start(300)
    out.append(r"\begin{center}\setlength{\tabcolsep}{1.5pt}\renewcommand{\arraystretch}{1}\begin{tabular}{" + spec
               + r"}\hline\hline")
    out.append(title("300", "title", 14, "150mm") + r" \\ \hline")
    # head rows: 22 mm above the first baseline and 1.5 below it; the second 6 above and 2 below
    tl = lambda key: hang(turned("300", key, "30mm"), 8.75)
    out.append(strut(22, 1.5) + tl("decades_arg") + " & " + tl("decade") + r" & \multicolumn{9}{c||}{\raisebox{8mm}{"
               + r"\parbox[c]{60mm}{\centering\small " + head("300", "singles", r"\small") + "}}} & " + tl("days") + " & "
               + hang(r"\parbox[b]{25mm}{\centering\small " + head("300", "names", r"\small") + "}", -1.0)
               + " & " + tl("sign") + r" \\ \cline{3-11}")
    out.append(" & & " + " & ".join(strut(6, 2) + rf"\small {j}" for j in range(1, 10)) + r" & & & \\ \hline\hline")
    days = [m["days"] for m in M.values()]; signs = [m["sign"] for m in M.values()]
    for i, (dec, row) in enumerate(T.items()):
        cells = [STRUT + dec, row["decade"]] + [row[str(j)] for j in range(1, 10)]
        if i == 0:
            cells += [spread([markup(d) for d in days], 0.0, 20.83, w["days"]),
                      spread([r"\hspace{2mm}" + m for m in MONTHS], 0.0, 20.83, w["names"], "l"),
                      spread(signs, 0.0, 20.83, w["sign"])]
        else:
            cells += ["", "", ""]
        out.append(" & ".join(cells) + r" \\")
    out.append(r"\hline\hline\end{tabular}\end{center}")
    return "\n".join(out)


def page301():
    Y = table("301", "years"); A = table("301", "arab_months"); P = table("301", "persian")
    spec = ("||" + ccol(11) + "|" + ccol(5) + TH + ccol(11) + "|" + ccol(5) + TH + lcol(24) + "|" + ccol(6) + "||"
            + lcol(31) + "".join("|" + ccol(4.5) for _ in range(7)) + "||")
    out = start(301)
    out.append(r"\begin{center}\setlength{\tabcolsep}{1.5pt}\renewcommand{\arraystretch}{1}\begin{tabular}{" + spec
               + r"}\hline\hline")
    out.append(title("301", "title_arab", 6, "68mm", "||c||") + " & " + title("301", "title_pers", 8, "74mm", "c||")
               + r" \\ \hline")
    # head rows: 10 mm above the first baseline and 1.5 below; the second 15 above and 1.5 below
    sm = r"\parbox[b]{14mm}{\centering\scriptsize "
    out.append(r"\multicolumn{2}{||c" + TH + "}{" + strut(10, 1.5) + sm + head("301", "collected", r"\scriptsize")
               + "}} & " + r"\multicolumn{2}{c" + TH + "}{" + sm + head("301", "single", r"\scriptsize") + "}} & "
               + hang(r"\parbox[b]{24mm}{\centering\small " + head("301", "menses", r"\small") + "}", 8)
               + " & " + hang(turned("301", "signa", "24mm"), 17.5) + " & "
               + r"\multicolumn{8}{c||}{\parbox[b]{60mm}{\centering\small " + head("301", "maslamah", r"\small")
               + r"}} \\ \cline{1-4}\cline{7-14}")
    num = r"\parbox[b]{11mm}{\centering\tiny " + head("301", "numerus", r"\tiny") + r"\par\vspace{2mm}}"
    sig = r"\rotatebox{90}{\parbox[c]{13mm}{\centering\tiny " + head("301", "signa", r"\tiny") + "}}"
    out.append(strut(15, 1.5) + num + " & " + sig + " & " + num + " & " + sig + " & & & "
               + r"\parbox[b]{31mm}{\centering\scriptsize " + head("301", "pnames", r"\scriptsize") + r"\par\vspace{2mm}} & "
               + " & ".join(rf"\small\textbf{{{c}}}" for c in range(1, 8)) + r" \\ \hline\hline")
    signs = [m["sign"] for m in A.values()]
    pnames = list(P)
    for i, (coll, row) in enumerate(Y.items()):
        cells = [STRUT + coll, row["collected_sign"], row["single"], row["single_sign"]]
        if i == 0:
            cells += [spread([r"\hspace{1mm}" + m for m in MONTHS], 1.0, 28.15, 24, "l"), spread(signs, 1.0, 28.15, 6),
                      spread([r"\hspace{1mm}" + p for p in pnames], 1.0, 28.15, 31, "l")]
            cells += [spread([P[p][str(c)] for p in pnames], 1.0, 28.15, 4.5) for c in range(1, 8)]
        else:
            cells += [""] * 10
        out.append(" & ".join(cells) + r" \\")
    out.append(r"\hline\hline\end{tabular}\end{center}")
    return "\n".join(out)


def page302():
    G = table("302", "grid"); Mu = table("302", "multiples")
    cols = ["oct", "nov", "dec", "inter", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep"]
    spec = ("||" + ccol(8) + TH + "|".join([ccol(6.6)] * 3) + "|" + ccol(11) + "|" + "|".join([ccol(6.6)] * 9) + TH
            + ccol(10) + "|" + ccol(10) + "||")
    out = start(302)
    out.append(r"\begin{center}\setlength{\tabcolsep}{1.5pt}\renewcommand{\arraystretch}{1.05}\begin{tabular}{" + spec
               + r"}\hline\hline")
    out.append(title("302", "title", 16, "160mm") + r" \\ \hline")
    # head rows: the days of the months (3.5 mm above the baseline, 1.5 below); the names (27 above, 1.5 below)
    tl = lambda key: hang(turned("302", key, "31mm"), 29.5)
    first = []
    for k in cols:
        first.append(tl("inter") if k == "inter" else r"\tiny " + H[("302", k)][1].split("|")[1])
    out.append(strut(3.5, 1.5) + tl("arg") + " & " + " & ".join(first) + r" & \multicolumn{2}{c||}{"
               + hang(r"\parbox[b]{20mm}{\centering\tiny " + head("302", "multiples", r"\tiny") + "}", 19)
               + r"} \\ \cline{2-4}\cline{6-14}")
    names = []
    for k in cols:
        if k == "inter":
            names.append("")
        else:
            a, l = H[("302", k)]
            names.append(r"\rotatebox{90}{\parbox[c]{27mm}{\centering\tiny \textarabic{" + markup(a, False) + r"}\\{}"
                         + markup(l.split("|")[0]) + "}}")
    out.append(strut(0, 1.5) + " & " + " & ".join(names) + r" & \multicolumn{2}{c||}{} \\ \hline\hline")
    mult = list(Mu.items())
    for i in range(29):
        if i < 28:
            row = G[str(i + 1)]
            cells = [str(i + 1)] + [row[k] for k in cols]
        else:
            cells = [""] * 14
        cells += [mult[i][0], mult[i][1]["value"]]
        gap = r"[1.5mm]" if i % 4 == 3 and i < 27 else ""
        out.append(" & ".join(cells) + r" \\" + gap)
    out.append(r"\hline\hline\end{tabular}\end{center}")
    return "\n".join(out)


def page303():
    G = table("303", "grid")
    cols = ["tut", "babah", "hatur", "kiyahk", "tubah", "amshir", "barmahut", "barmudhah", "bashans", "bawunah", "abib",
            "misri"]
    spec = "||" + ccol(9) + TH + "|".join([ccol(8.2)] * 12) + TH + ccol(12) + "||"
    out = start(303)
    out.append(r"\begin{center}\setlength{\tabcolsep}{1.5pt}\renewcommand{\arraystretch}{1.05}\begin{tabular}{" + spec
               + r"}\hline\hline")
    out.append(title("303", "title", 14, "150mm") + r" \\ \hline")
    # head rows: the names (25 mm above the baseline, 1.5 below); the days (3.5 above, 1.5 below)
    names = []
    for k in cols:
        a, l = H[("303", k)]
        names.append(r"\rotatebox{90}{\parbox[c]{25mm}{\centering\scriptsize \textarabic{" + markup(a, False) + r"}\\{}"
                     + markup(l.split("|")[0]) + "}}")
    tl = lambda key: hang(turned("303", key, "29mm"), 6.0)
    out.append(strut(0, 1.5) + tl("arg") + " & " + " & ".join(names) + " & " + tl("bisext") + r" \\ \cline{2-13}")
    out.append(" & " + " & ".join(strut(3.5, 1.5) + r"\small " + H[("303", k)][1].split("|")[1] for k in cols)
               + r" & \\ \hline\hline")
    for n in range(1, 29):
        row = G[str(n)]
        cells = [str(n)] + [row[k] for k in cols] + [row["bisext"]]
        gap = r"[1.5mm]" if n % 4 == 0 and n < 28 else ""
        out.append(" & ".join(cells) + r" \\" + gap)
    out.append(r"\hline\hline\end{tabular}\end{center}")
    return "\n".join(out)


def page304():
    T = table("304", "conversion")
    spec = ("||" + ccol(9) + TH + "|".join(rcol(w) for w in (10, 8, 8, 9)) + TH
            + "|".join(rcol(w) for w in (10, 8, 8, 9)) + TH + "|".join(rcol(w) for w in (10, 8, 8)) + "||")
    out = start(304)
    out.append(r"\begin{center}\setlength{\tabcolsep}{2pt}\renewcommand{\arraystretch}{1.25}\begin{tabular}{" + spec
               + r"}\hline\hline")
    out.append(title("304", "title", 12, "150mm") + r" \\ \hline")

    def big(key, ncol, width, last=False):
        a, l = H[("304", key)]
        return (r"\multicolumn{" + str(ncol) + "}{c" + ("||" if last else TH) + r"}{\parbox[b][40mm][c]{" + width
                + r"}{\centering\scriptsize " + ar(a, r"\\[0.3ex]") + r"\\[1ex]\scriptsize " + nl(l) + "}}")
    # head rows: 40 mm above the first baseline, 1.5 below; the second 9 above, 1.5 below
    out.append(strut(40, 1.5) + hang(turned("304", "arg", "48mm"), 11.5) + " & " + big("R", 4, "40mm") + " & "
               + big("C", 4, "40mm") + " & " + big("P", 3, "30mm", True) + r" \\ \cline{2-12}")
    sub = [r"\parbox[b][9mm][c]{9mm}{\centering\tiny " + head("304", k, r"\tiny") + "}"
           for k in ("anni", "menses", "dies", "fract")]
    out.append(strut(0, 1.5) + " & " + " & ".join(sub + sub + sub[:3]) + r" \\ \hline\hline")
    for a, row in T.items():
        cells = [a] + [row[f"{e}_{p}"] for e in ("R", "C") for p in ("anni", "menses", "dies", "fract")] \
                + [row[f"P_{p}"] for p in ("anni", "menses", "dies")]
        out.append(" & ".join(cells) + r" \\")
    out.append(r"\hline\hline\end{tabular}\end{center}")
    return "\n".join(out)


def page305():
    Y = table("305", "years"); M = table("305", "months")
    spec = ("||" + ccol(7) + "|" + ccol(6) + TH + "|".join(rcol(w) for w in (8, 9, 8, 8)) + TH
            + "|".join(rcol(w) for w in (8, 9, 8)) + TH + lcol(28) + "|" + ccol(7) + "|" + ccol(7) + "||")
    out = start(305)
    out.append(r"\begin{center}\setlength{\tabcolsep}{1.8pt}\renewcommand{\arraystretch}{1}\begin{tabular}{" + spec
               + r"}\hline\hline")
    out.append(title("305", "title", 12, "160mm") + r" \\ \hline")
    # head rows: 17 mm above the first baseline, 1.5 below; the second 4.5 above, 1.5 below. The head of the months
    # reaches down into the body, to the rule above al-muharram (about 26 mm under the first baseline), as printed
    tl = lambda key: hang(turned("305", key, "23mm", r"\tiny"), 6.75)
    tm = lambda key: hang(turned("305", key, "41mm"), 26)
    out.append(strut(17, 1.5) + tl("arg") + " & " + tl("bisext") + r" & \multicolumn{4}{c" + TH
               + r"}{\parbox[b][17mm][c]{38mm}{\centering\scriptsize " + head("305", "S") + r"}} & \multicolumn{3}{c"
               + TH + r"}{\parbox[b][17mm][c]{30mm}{\centering\scriptsize " + head("305", "P") + "}} & "
               + hang(r"\parbox[t]{27mm}{\centering\scriptsize " + head("305", "mhead") + "}", -9.0) + " & "
               + tm("menses") + " & " + tm("dies") + r" \\ \cline{3-9}")
    sub = [strut(4.5, 1.5) + r"\tiny " + x for x in H[("305", "sub")][1].split("|")]
    out.append(" & & " + " & ".join(sub + sub[:3]) + r" & & & \\ \cline{1-9}\noalign{\vskip\doublerulesep}\cline{1-9}")
    # the rows: pitch R, a gap of G after every fifth; the months from 375 to 725 pt of the scan, on the scan's own
    # row positions (row 1 at 306.8 pt, 14.0 pt a row, 6.3 pt more after every fifth)
    G = 1.6
    yrow = lambda i: i * R + (i // 5) * G                      # the baseline of row i (0-based) below row 0, in mm
    scan = [306.8 + i * 14.0 + (i // 5) * 6.3 for i in range(30)]

    def to_mm(pt):
        for i in range(29):
            if scan[i] <= pt <= scan[i + 1]:
                return yrow(i) + (pt - scan[i]) / (scan[i + 1] - scan[i]) * (yrow(i + 1) - yrow(i))
        return yrow(29)
    ypos = [to_mm(375 + k * (725 - 375) / 11) for k in range(12)]
    for i, (n, row) in enumerate(Y.items()):
        cells = [STRUT + n, row.get("bisext", "")] + [row[f"S_{p}"] for p in ("anni", "menses", "dies", "fract")] \
                + [row[f"P_{p}"] for p in ("anni", "menses", "dies")]
        if i == 0:
            line = to_mm(341.5)                       # the rule under the head of the months, as printed
            cells += [spread([r"\hspace{1mm}" + m for m in MONTHS], 0, 0, 28, "l", ypos=ypos, rule=line),
                      spread([v["menses"] for v in M.values()], 0, 0, 7, ypos=ypos, rule=line),
                      spread([v["dies"] for v in M.values()], 0, 0, 7, ypos=ypos, rule=line)]
        else:
            cells += ["", "", ""]
        out.append(" & ".join(cells) + r" \\" + (rf"[{G}mm]" if i % 5 == 4 and i < 29 else ""))
    out.append(r"\hline\hline\end{tabular}\end{center}")
    out.append(r"\vspace{-1mm}\noindent\hfill{\small " + H[("305", "signature")][1] + r"}\hspace*{14mm}")
    return "\n".join(out)


def page_syz(pp, table_name):
    T = table(pp, table_name)
    spec = ("||" + ccol(10) + TH + "|".join(rcol(w) for w in (8, 8, 8)) + TH
            + TH.join("|".join(rcol(w) for w in (7, 8, 7, 7)) for _ in range(3)) + "||")
    out = start(int(pp))
    out.append(r"\begin{center}\setlength{\tabcolsep}{2pt}\renewcommand{\arraystretch}{1.25}\begin{tabular}{" + spec
               + r"}\hline\hline")
    out.append(title(pp, "title", 16, "150mm") + r" \\ \hline")

    def grp(key, ncol, last=False):
        return (r"\multicolumn{" + str(ncol) + "}{c" + ("||" if last else TH) + r"}{\parbox[b][22mm][c]{"
                + ("24mm" if ncol == 3 else "30mm") + r"}{\centering\scriptsize " + head(pp, key) + "}}")
    # head rows: 22 mm above the first baseline, 1.5 below; the second 7 above, 1.5 below
    out.append(strut(22, 1.5) + hang(turned(pp, "arg", "29mm"), 9.5) + " & " + grp("I", 3) + " & " + grp("II", 4)
               + " & " + grp("III", 4) + " & " + grp("IV", 4, True) + r" \\ \cline{2-16}")
    subs = [r"\parbox[b][7mm][c]{8mm}{\centering\tiny " + nl(s) + "}" for s in H[(pp, "sub")][1].split("|")]
    out.append(strut(0, 1.5) + " & " + " & ".join(subs[:3] + subs[3:] * 3) + r" \\ \hline\hline")
    for k, (a, row) in enumerate(T.items()):
        first = k == 0
        # the marks of the first row; the other rows keep their width, so that the digits stand under one another
        sup = (lambda v, m: v + (r"\textsuperscript{" + m + "}" if first else r"\phantom{\textsuperscript{" + m + "}}"))
        mark = (lambda v, m: v + (m if first else r"\phantom{" + m + "}"))
        cells = [a, sup(row["I_dies"], "d"), sup(row["I_horae"], "h"), sup(row["I_min"], "m")]
        for g in ("II", "III", "IV"):
            cells += [sup(row[f"{g}_s"], "s"), mark(row[f"{g}_d"], "°"), mark(row[f"{g}_m"], "′"),
                      mark(row[f"{g}_sec"], "″")]
        out.append(" & ".join(cells) + r" \\")
    out.append(r"\hline\hline\end{tabular}\end{center}")
    return "\n".join(out)


def document():
    out = [PREAMBLE.replace("margin=16mm", "margin=13mm"), EXTRA, r"\begin{document}",
           page297(), page300(), page301(), page302(), page303(), page304(), page305(),
           page_syz("306", "conjunctions"), page_syz("307", "oppositions"), r"\end{document}"]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p2_spurious.tex").write_text(document(), encoding="utf-8", newline="\n")
    print("wrote p2_spurious.tex")

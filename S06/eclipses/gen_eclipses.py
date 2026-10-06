"""Generate the edition of Nallino's Part II pp. 88-91 (the tables for computing eclipses) from motions_p2.tsv,
correction_p2.tsv, digits_p2.tsv, eclipses_p2.tsv, ecl_pages.tsv and ecl_text.tsv: one page per printed page, with the
running head, the folio line and the framed tables (titles, heads, rows in groups as printed; each column a centred
group of fixed-width numbers; the first row of a table carries the marks as printed). p. 88: the hourly motions, the
small table of increments and the eclipse limits in Arabic and Latin; p. 89: the table of correction and the table of
digits, whose left part (digits 1-12) stands on every other line of the right part (digits 0-21); pp. 90-91: two
tables side by side, each with the interval of its latitudes below. Output: p2_eclipses.tex"""
from pathlib import Path

from gen_stars import PREAMBLE, markup, read

HERE = Path(__file__).resolve().parent
WIDTHS = r"\newlength{\Dw}\newlength{\Mw}\settowidth{\Dw}{000}\settowidth{\Mw}{00}"
DIES = r"\raisebox{0.75ex}{\fontsize{5.5}{6}\selectfont\itshape dig.}"


def nl(s):
    return markup(s).replace(" / ", r"\\").replace(r"\\[", r"\\{}[")


def ar(s):
    return r"\\".join(r"\textarabic{" + markup(x, False) + "}" for x in s.split(" / "))


def box(v, w=r"\Mw", mark=""):
    return r"\makebox[" + w + "][r]{" + v + "}" + (r"\rlap{" + mark + "}" if mark else "")


def nums(vals, marks=None, widths=None, gap="2.6mm"):
    marks = marks or [""] * len(vals)
    widths = widths or [r"\Dw" if k == 0 else r"\Mw" for k in range(len(vals))]
    return (r"\hspace{" + gap + "}").join(box(v, w, m) for v, w, m in zip(vals, widths, marks))


def running_head(pp):
    return (r"\noindent\makebox[\textwidth]{\hfill{\scriptsize AL-BATTANI OPUS ASTRONOMICUM}\hfill\llap{" + str(pp) + "}}"
            if pp % 2 else r"\noindent\makebox[\textwidth]{\rlap{" + str(pp) + r"}\hfill{\scriptsize C. A. NALLINO}\hfill}")


def page_start(pp, fol):
    return [r"\clearpage", running_head(pp), r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{1mm}",
            r"\begin{center}{\small " + fol + r"}\end{center}\vspace{-3mm}"]


def heads(page):
    return [h.split("‖") for h in page["heads"].split("|")]


def head(a, l, width, size=r"\scriptsize", height=None):
    text = (ar(a) + r"\\" if a else "") + nl(l)
    h = "[" + height + "][c]" if height else ""
    return r"\parbox[c]" + h + "{" + width + r"}{\centering" + size + " " + text + r"\par\vspace{0.7mm}}"


def rhead(a, l, length, size=r"\scriptsize"):
    """a head turned to read upwards"""
    text = (ar(a) + r"\\" if a else "") + nl(l)
    return r"\rotatebox{90}{\parbox{" + length + r"}{\centering" + size + " " + text + "}}"


def title(a, l, width, ncols, size=r"\large"):
    la = "".join(r"\\\textbf{" + markup(x) + "}" for x in l.split(" / ")) if l else ""
    return (r"\multicolumn{" + str(ncols) + r"}{||c||}{\parbox{" + width + r"}{\centering\vspace{1mm}{" + size + " " + ar(a)
            + "}" + la + r"\vspace{1mm}}} \\")


def gap(i, n, group):
    return r"[1.2mm]" if group and i % group == group - 1 and i < n - 1 else ""


def page88(pages, rows, text):
    P = {p["table"]: p for p in pages}
    H = [r for r in rows if r["table"] == "hourly"]
    S = [r for r in rows if r["table"] == "increments"]
    out = page_start(88, P["hourly"]["fol"])
    out.append(r"\begin{center}\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.05}\begin{tabular}{||c||c||}\hline\hline")
    out.append(title(P["hourly"]["title_ar"], P["hourly"]["title_la"], "165mm", 2) + r" \hline")
    left = [r"\begin{tabular}[t]{>{\centering\arraybackslash}p{21mm}|>{\centering\arraybackslash}p{24mm}|"
            r">{\centering\arraybackslash}p{24mm}}"]
    left.append(" & ".join(head(a, l, w) for (a, l), w in zip(heads(P["hourly"]), ("20mm", "23mm", "23mm"))) + r" \\ \hline")
    for i, r in enumerate(H):
        first = i == 0
        cells = [nums([r["arg"], r["arg2"]], gap="3.5mm"),
                 nums([r["sun_1"], r["sun_2"]], ["′", "″"] if first else None, [r"\Mw", r"\Mw"]),
                 nums([r["moon_1"], r["moon_2"]], ["′", "″"] if first else None, [r"\Mw", r"\Mw"])]
        left.append(" & ".join(cells) + r" \\" + gap(i, len(H), 4))
    left.append(r"\end{tabular}")
    right = [r"\begin{minipage}[t]{76mm}\vspace{0pt}\centering\begin{tabular}{||>{\centering\arraybackslash}p{30mm}|"
             r">{\centering\arraybackslash}p{30mm}||}"]
    right.append(" & ".join(head(a, l, "29mm") for a, l in heads(P["increments"])) + r" \\ \hline")
    for i, r in enumerate(S):
        right.append(box(r["arg"], r"\Mw", "°" if i == 0 else "") + " & "
                     + nums([r["inc_1"], r["inc_2"]], ["′", "″"] if i == 0 else None, [r"\Mw", r"\Mw"]) + r" \\")
    right.append(r"\hline\hline\end{tabular}\par\vspace{8mm}")
    T = {t["item"]: t["text"] for t in text}
    for item in ("limits_ar_sun", "limits_ar_moon"):
        right.append(r"\begin{Arabic}\noindent\hangindent=-6mm\hangafter=1 " + markup(T[item], False)
                     + r"\par\end{Arabic}\vspace{3mm}")
    right.append(r"\vspace{6mm}")
    for item in ("limits_la_sun", "limits_la_moon"):
        right.append(r"{\small\noindent\hangindent=6mm\hangafter=1 " + markup(T[item]) + r"\par}\vspace{3mm}")
    right.append(r"\end{minipage}")
    out.append("\n".join(left) + "\n&\n" + "\n".join(right) + r" \\")
    out.append(r"\hline\hline\end{tabular}\end{center}")
    return "\n".join(out)


def page89(pages, corr, digits):
    P = {p["table"]: p for p in pages}
    out = page_start(89, P["correction"]["fol"])
    out.append(r"\begin{center}\setlength{\tabcolsep}{2.5pt}\renewcommand{\arraystretch}{1.05}")
    # the table of correction
    L = [r"\begin{tabular}[t]{||>{\centering\arraybackslash}p{19mm}|>{\centering\arraybackslash}p{15mm}|"
         r">{\centering\arraybackslash}p{7mm}|>{\centering\arraybackslash}p{7mm}||}\hline\hline"]
    L.append(title(P["correction"]["title_ar"], P["correction"]["title_la"], "52mm", 4) + r" \hline")
    h = heads(P["correction"])
    L.append(" & ".join([head(*h[0], "18mm"), head(*h[1], "14mm"), rhead(*h[2], "22mm"), rhead(*h[3], "22mm")]) + r" \\ \hline")
    for i, r in enumerate(corr):
        first = i == 0
        L.append(" & ".join([nums([r["arg"], r["arg2"]], gap="3mm"),
                             nums([r["portion_1"], r["portion_2"]], ["′", "″"] if first else None, [r"\Mw", r"\Mw"], "2mm"),
                             box(r["epicycle"], r"\Mw", "′" if first else ""), box(r["eccentre"], r"\Mw", "′" if first else "")])
                 + r" \\" + gap(i, len(corr), 5))
    L.append(r"\hline\hline\end{tabular}")
    # the table of digits: the areas on every other line of the inclinations
    A = [r for r in digits if r["table"] == "areas"]
    I = [r for r in digits if r["table"] == "inclinations"]
    R = [r"\begin{tabular}[t]{||>{\centering\arraybackslash}p{8mm}|>{\centering\arraybackslash}p{15mm}|"
         r">{\centering\arraybackslash}p{15mm}||>{\centering\arraybackslash}p{9mm}|>{\centering\arraybackslash}p{9mm}|"
         r">{\centering\arraybackslash}p{9mm}|>{\centering\arraybackslash}p{9mm}||}\hline\hline"]
    R.append(title(P["areas"]["title_ar"], P["areas"]["title_la"], "92mm", 7) + r" \hline")
    hs = heads(P["areas"]) + heads(P["inclinations"])
    R.append(" & ".join(rhead(a, l, "60mm", r"\tiny") for a, l in hs) + r" \\ \hline")
    for j, r in enumerate(I):
        cells = ["", "", ""]
        if j % 2 == 0:
            a = A[j // 2]
            mk = [DIES, "′"] if j == 0 else None
            cells = [a["arg"], nums([a["sun_1"], a["sun_2"]], mk, [r"\Mw", r"\Mw"], "3.6mm"),
                     nums([a["moon_1"], a["moon_2"]], mk, [r"\Mw", r"\Mw"], "3.6mm")]
        arg = r"{\scriptsize compl.}" if r["arg"] == "compl." else box(r["arg"], r"\Mw", DIES if j == 0 else "")
        deg = "°" if j == 0 else ""
        R.append(" & ".join(cells + [arg, box(r["sun_incl"], r"\Mw", deg), box(r["moon_begin"], r"\Mw", deg),
                                     box(r["moon_end"], r"\Mw", deg)]) + r" \\")
    R.append(r"\hline\hline\end{tabular}")
    out.append("\n".join(L) + r"\hspace{1mm}" + "\n".join(R))
    out.append(r"\end{center}")
    out.append(r"\vspace{-2mm}\noindent\hfill{\small " + P["inclinations"]["footer_la"] + r"}\hspace*{6mm}")
    return "\n".join(out)


def eclipse_table(page, rows, lunar):
    cols = ["lat", "inc", "mora", "digits"] if lunar else ["lat", "digits", "inc"]
    spec = "||" + "|".join(r">{\centering\arraybackslash}p{" + ("17mm" if c != "digits" else "19mm") + "}" for c in cols) + "||"
    out = [r"\begin{tabular}[t]{" + spec + r"}\hline\hline"]
    out.append(title(page["title_ar"], page["title_la"], "70mm" if lunar else "54mm", len(cols)) + r" \hline")
    out.append(" & ".join(head(a, l, "16mm" if c != "digits" else "18mm", height="25mm" if lunar else "22mm")
                          for (a, l), c in zip(heads(page), cols)) + r" \\ \hline")
    for i, r in enumerate(rows):
        first = i == 0
        cells = []
        for c in cols:
            if c == "digits":
                p = r["digits"].split()
                if len(p) == 1:
                    cells.append(r["digits"])
                else:
                    marks = [r"\textsuperscript{d}", "′", "″"][:len(p)]
                    cells.append(" ".join(v + m for v, m in zip(p, marks)))
            else:
                cells.append(nums([r[c + "_1"], r[c + "_2"]], ["′", "″"] if first else None, [r"\Mw", r"\Mw"]))
        out.append(" & ".join(cells) + r" \\" + gap(i, len(rows), 4))
    out.append(r"\hline\hline\end{tabular}")
    return "\n".join(out)


def footer(page):
    la = markup(page["footer_la"]).replace(" / ", r"\\")
    return (r"\parbox[t]{82mm}{\centering\textarabic{" + markup(page["footer_ar"], False) + r"}\\" + la + "}")


def page9x(pp, pages, rows, lunar):
    P = {p["table"]: p for p in pages}
    names = ("lunar_max", "lunar_min") if lunar else ("solar_max", "solar_min")
    out = page_start(pp, P[names[0]]["fol"])
    out.append(r"\begin{center}\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.05}")
    t = [eclipse_table(P[n], [r for r in rows if r["table"] == n], lunar) for n in names]
    out.append(t[0] + (r"\hspace{4mm}" if lunar else r"\hspace{22mm}") + t[1])
    out.append(r"\end{center}\vspace{1mm}")
    out.append(r"\noindent\makebox[\textwidth]{" + footer(P[names[0]]) + r"\hspace{4mm}" + footer(P[names[1]]) + "}")
    return "\n".join(out)


def document():
    pages = read("ecl_pages.tsv")
    out = [PREAMBLE.replace("margin=16mm", "margin=13mm"), WIDTHS, r"\begin{document}"]
    out.append(page88(pages, read("motions_p2.tsv"), read("ecl_text.tsv")))
    out.append(page89(pages, read("correction_p2.tsv"), read("digits_p2.tsv")))
    rows = read("eclipses_p2.tsv")
    out.append(page9x(90, pages, rows, True))
    out.append(page9x(91, pages, rows, False))
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p2_eclipses.tex").write_text(document(), encoding="utf-8", newline="\n")
    print("wrote p2_eclipses.tex")

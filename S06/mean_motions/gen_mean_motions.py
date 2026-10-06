"""Generate the edition of Nallino's Part II pp. 19-28 (mean motions) from mm_p2.tsv / mm_pages.tsv (pp. 19-23: four
motions in degrees, minutes and seconds) and mm5_p2.tsv / mm5_pages.tsv (pp. 24-28: five motions in degrees and
minutes): one page per printed page, with the running head, the folio line, the framed table (Arabic and Latin title,
the argument column head set vertically, the motion heads), and the rows in groups of five; each motion is one
centred column whose degrees, minutes and seconds stand in boxes of fixed width; the first row carries the marks
° ′ ″ as printed. Output: p2_mean_motions.tex"""
from pathlib import Path

from gen_stars import PREAMBLE, markup, read

HERE = Path(__file__).resolve().parent
SETS = [("mm_pages.tsv", "mm_p2.tsv", ["sun", "moon", "anom", "node"], 3),
        ("mm5_pages.tsv", "mm5_p2.tsv", ["sat", "jup", "mars", "ven", "mer"], 2),
        ("mmr_pages.tsv", "mmr_p2.tsv", ["sun", "moon", "anom", "node"], 3),
        ("mm5r_pages.tsv", "mm5r_p2.tsv", ["sat", "jup", "mars", "ven", "mer"], 2)]
WIDTHS = r"\newlength{\Dw}\newlength{\Mw}\settowidth{\Dw}{000}\settowidth{\Mw}{00}"


def nl(s):
    """line breaks at « / »; the places beyond the thirds ({iv}, {v}, {vi}) as small-capital superscripts"""
    s = markup(s).replace(" / ", r"\\")
    for p in ("vi", "iv", "v"):
        s = s.replace("{" + p + "}", r"\textsuperscript{\textsc{" + p + "}}")
    return s


def ar(s):
    return r"\\".join(r"\textarabic{" + x + "}" for x in s.split(" / "))


def page_tex(page, rows, groups, places):
    pp = int(page["ppage"])
    head = (r"\noindent\makebox[\textwidth]{\hfill{\scriptsize AL-BATTANI OPUS ASTRONOMICUM}\hfill\llap{" + str(pp) + "}}"
            if pp % 2 else r"\noindent\makebox[\textwidth]{\rlap{" + str(pp) + r"}\hfill{\scriptsize C. A. NALLINO}\hfill}")
    out = [r"\clearpage", head, r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{1mm}",
           r"\begin{center}{\small " + page["fol"] + r"}\end{center}\vspace{-3mm}"]
    months = rows[0]["table"] == "months"
    upright = 521 <= int(page["pdf"]) <= 526          # pp. 72-77: the first head stands upright in a narrow column
    argw = ("38mm" if "[" in rows[0]["arg"] else "32mm") if months else ("17mm" if upright else "13mm")
    headw = "30mm" if places == 3 else "26mm"
    ncol = 1 + len(groups)
    spec = "|" + (r">{\raggedright\arraybackslash}p{" + argw + "}" if months else r">{\centering\arraybackslash}p{" + argw + "}") + \
           "|" + "|".join([r">{\centering\arraybackslash}p{" + headw + "}"] * len(groups)) + "|"
    tl = page["title_la"].split(" / ")
    title = r"{\large " + ar(page["title_ar"]) + "}" + "".join(r"\\\textbf{" + markup(x) + "}" for x in tl)
    out.append(r"\begin{center}\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.05}\begin{tabular}{" + spec + r"}\hline\hline")
    out.append(r"\multicolumn{" + str(ncol) + r"}{||c||}{\parbox{150mm}{\centering\vspace{1mm}" + title + r"\vspace{1mm}}} \\ \hline")
    heads = [h.split("‖") if "‖" in h else h.split("/", 1) for h in page["heads"].split("|")]   # Arabic, Latin
    first = heads[0]
    if months or upright:
        c0 = r"\parbox[c]{" + argw + r"}{\centering\scriptsize " + ar(first[0]) + r"\\" + nl(first[1].strip()) + r"\par\vspace{0.7mm}}"
    else:
        c0 = r"\rotatebox{90}{\scriptsize\begin{tabular}{@{}c@{}}" + ar(first[0]) + r"\\" + nl(first[1].strip()) + r"\end{tabular}}"
    cells = [c0] + [r"\parbox[c]{" + headw + r"}{\centering\scriptsize " + (ar(a) + r"\\{}" if a else "") + nl(l.strip()) +
                    r"\par\vspace{0.7mm}}" for a, l in heads[1:]]
    out.append(" & ".join(cells) + r" \\ \hline\hline")
    tight_last = rows[-1]["arg"] == "bisext."          # p. 21: dhu 'l-hijjah comm. and bisext. are set close together
    # rows stand in groups of five, of four in the tables of hours and on p. 72 (as printed)
    group = 4 if rows[0]["table"] == "hours" or rows[0]["pdf"] == "521" else 5
    marks = [r"\rlap{°}", r"\rlap{′}", r"\rlap{″}"]

    def body(rows, italic=False):
        lines = []
        for i, r in enumerate(rows):
            line = [r"\textit{" + nl(r["arg"]) + "}" if italic else nl(r["arg"])]
            for g in groups:
                vals = [r[g + "_d"], r[g + "_m"]] + ([r[g + "_s"]] if places == 3 else [])
                if i == 0:
                    vals = [v + marks[k] for k, v in enumerate(vals)]
                line.append(r"\hspace{2.6mm}".join(r"\makebox[" + (r"\Dw" if k == 0 else r"\Mw") + "][r]{" + v + "}"
                                                   for k, v in enumerate(vals)))
            gap = ""
            if months:
                gap = r"[2.2mm]" if i < len(rows) - (2 if tight_last else 1) else ""
            elif i % group == group - 1 and i < len(rows) - 1:
                gap = r"[1.2mm]"
            lines.append(" & ".join(line) + r" \\" + gap)
        return lines

    if page["pdf"] == "552":                            # p. 103: the single years, the line of 20 years, the sums
        out += body([r for r in rows if r["table"] == "single"])
        line20 = {r["item"]: r for r in read("mm5r_extra.tsv")}["years20"]
        cells = []
        for g in groups:
            whole, frac = line20[g].split(";")
            parts = frac.split(",")
            v = f"{whole}° {parts[0]}′ {parts[1]}″"
            cells.append(r"\parbox[t]{" + headw + r"}{\centering " + v + (r"\\" + parts[2] + r"\textsuperscript{\textsc{iii}}"
                                                                          if len(parts) > 2 else "") + "}")
        out.append(r"\cline{2-" + str(ncol) + "}")
        out.append(r"\multicolumn{1}{|c}{} & " + " & ".join(r"\multicolumn{1}{c" + ("|" if k == len(cells) - 1 else "") + "}{" + c + "}"
                                                         for k, c in enumerate(cells)) + r" \\[1mm] \hline\hline")
        out.append(r"\multicolumn{" + str(ncol) + r"}{||c||}{\rule{0pt}{6mm}" + markup(page["subtitle"]) + r"} \\[2mm] \hline\hline")
        out += body([r for r in rows if r["table"] == "intervals"], italic=True)
    else:
        out += body(rows)
    out.append(r"\hline\hline\end{tabular}\end{center}")
    if page.get("signature"):
        out.append(r"\vspace{-2mm}\noindent\hfill{\small " + page["signature"] + r"}\hspace*{14mm}")
    return "\n".join(out)


MARK = {"d": "°", "m": "′", "s": "″", "t": "‴"}


def fs_value(r, marks):
    places = [p for p in ("d", "m", "s", "t") if r[p] != ""]
    return r"\hspace{2mm}".join(r"\makebox[\Mw][r]{" + r[p] + "}" + (r"\rlap{" + MARK[p] + "}" if marks else "")
                                for p in places)


def rot(ar_text, la):
    return (r"\rotatebox{90}{\parbox{22mm}{\centering\scriptsize " + (r"\textarabic{" + ar_text + r"}\\{}" if ar_text else "")
            + la + "}}")


def headbox(ar_text, la, w):
    return (r"\parbox[c][22mm][c]{" + w + r"}{\centering\scriptsize " + (r"\textarabic{" + ar_text + r"}\\{}" if ar_text else "")
            + la.replace(" / ", r"\\{}") + "}")


def page107():
    """p. 107: the motion of the fixed stars; four tables in one frame (collected years, single years, months, days)"""
    R = read("fs_p2.tsv")
    T = {t: [r for r in R if r["table"] == t] for t in ("collected", "single", "months", "days")}
    head = (r"\noindent\makebox[\textwidth]{\hfill{\scriptsize AL-BATTANI OPUS ASTRONOMICUM}\hfill\llap{107}}")
    out = [r"\clearpage", head, r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{1mm}",
           r"\begin{center}{\small f. 208,r.}\end{center}\vspace{-3mm}", r"\begin{center}\setlength{\tabcolsep}{3pt}"]
    blocks = []
    # collected years
    b = [r"\begin{tabular}[t]{>{\centering\arraybackslash}p{9mm}|>{\centering\arraybackslash}p{22mm}}",
         rot("سنو الروم المجموعة", r"Anni Romani / collecti.".replace(" / ", r"\\")) + " & "
         + headbox("مسيرها المجموع", "Motus / in annis Romanis / collectis.", "21mm") + r" \\ \hline"]
    for i, r in enumerate(T["collected"]):
        b.append(r["arg"] + " & " + fs_value(r, i == 0) + r" \\[1.9mm]")
    blocks.append("\n".join(b) + r"\end{tabular}")
    # single years
    b = [r"\begin{tabular}[t]{>{\centering\arraybackslash}p{7mm}|>{\centering\arraybackslash}p{24mm}}",
         r"\multicolumn{2}{c}{\parbox[c][9mm][c]{30mm}{\centering\scriptsize [Motus\\in singulis annis\\Romanis.]}} \\ \hline",
         rot("سنو الروم المبسوطة", "Anni singuli.") + " & " + headbox("مسيرها المبسوط", "Motus / in annis singulis.", "23mm")
         + r" \\ \hline", r"\multicolumn{2}{c}{} \\[1.2mm]"]
    for i, r in enumerate(T["single"]):
        b.append(r["arg"] + " & " + fs_value(r, i in (0, 19)) + r" \\[1.9mm]")
    blocks.append("\n".join(b) + r"\end{tabular}")
    # months
    b = [r"\begin{tabular}[t]{>{\raggedright\arraybackslash}p{24mm}|>{\centering\arraybackslash}p{15mm}}",
         r"\multicolumn{2}{c}{\parbox[c][9mm][c]{38mm}{\centering\scriptsize [Motus\\in mensibus Romanis.]}} \\ \hline",
         headbox("اسماء الشهور الرومية", "Nomina mensium.", "23mm") + " & " + headbox("مسيرها في الشهور", "Motus / in / mensibus.", "14mm")
         + r" \\ \hline", r"\multicolumn{2}{c}{} \\[1.2mm]"]
    for i, r in enumerate(T["months"]):
        name, la = r["arg"].split(" [")
        b.append(name + r" \\")
        b.append(r"\hspace*{2mm}[" + la + " & " + fs_value(r, i == 0) + r" \\[2.6mm]")
    blocks.append("\n".join(b) + r"\end{tabular}")
    # days
    b = [r"\begin{tabular}[t]{>{\centering\arraybackslash}p{8mm}|>{\centering\arraybackslash}p{19mm}}",
         rot("ايام الشهور", "Dies mensis.") + " & " + headbox("في الايام", "[Motus] / in diebus.", "18mm") + r" \\ \hline"]
    for i, r in enumerate(T["days"]):
        gap = r"[1.6mm]" if i % 5 == 4 and i < 29 else ""
        b.append(r["arg"] + " & " + fs_value(r, i in (0, 29)) + r" \\" + gap)
    blocks.append("\n".join(b) + r"\end{tabular}")
    out.append(r"\begin{tabular}{||c||c||c||c||}\hline\hline")
    out.append(r"\multicolumn{4}{||c||}{\parbox{170mm}{\centering\vspace{1mm}{\large \textarabic{جداول حركات الكواكب الثابتة وهي حركة واحدة للجميع}}"
               r"\\\textbf{Tabulae motus stellarum fixarum, qui omnibus est unus et idem.}\vspace{1mm}}} \\ \hline")
    out.append(" & ".join(r"\begin{minipage}[t]{" + w + "}\n" + blk + r"\end{minipage}"
                          for w, blk in zip(("33mm", "33mm", "41mm", "29mm"), blocks)) + r" \\ \hline\hline")
    out.append(r"\end{tabular}\end{center}")
    return "\n".join(out)


def document():
    out = [PREAMBLE.replace("margin=16mm", "margin=14mm"), WIDTHS, r"\begin{document}"]
    for pages_file, rows_file, groups, places in SETS:
        rows = read(rows_file)
        for page in read(pages_file):
            out.append(page_tex(page, [r for r in rows if r["pdf"] == page["pdf"]], groups, places))
    out.append(page107())
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p2_mean_motions.tex").write_text(document(), encoding="utf-8", newline="\n")
    print("wrote p2_mean_motions.tex")

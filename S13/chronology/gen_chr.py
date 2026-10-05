"""Generate the two diplomatic editions of al-Battani's chronological tables (kings, intervals between the eras, caliphs):
  p3_chronology.tex - Nallino Part III (Arabic, Maghribi abjad), one page per source page, as printed
  p2_chronology.tex - Nallino Part II (Latin, Western numerals), one page per source page
Data: chr_p3.tsv, chr_p3_footnotes.tsv, chr_p3_pages.tsv, chr_p2.tsv, chr_p2_pages.tsv.
Part III rows: line R.. / L.. = right / left panel of the table of kings (right panel first); a second table on a page
has line ids with the prefix 2. Sections: K kings, I intervals, C caliphs. Part II rows: kind L / R (columns of the
table of kings), Lhead / Rhead (headings inside a column), T (rows of a one-column table), title, colhead."""
import re
from pathlib import Path

from gen_stars import PREAMBLE, AR_DIGITS, markup, read

HERE = Path(__file__).resolve().parent
NUMS = ("reg_y", "reg_m", "reg_d", "sum_y", "sum_m", "sum_d")


def nl(s, latin=False):
    return markup(s, latin).replace(" / ", r"\newline ")


def table_key(line):
    return line[0] if line[:1].isdigit() else "1"


def body(line):
    return line[1:] if line[:1].isdigit() else line


# ---------------------------------------------------------------- Part III
def p3_kings_panel(rows, heads):
    h1, h2, h3 = (heads + ["", "", ""])[:3]
    out = [r"\setlength{\tabcolsep}{2.5pt}\begin{tabular}{|p{44mm}|>{\centering\arraybackslash}p{7mm}|>{\centering\arraybackslash}p{9mm}|}\hline",
           r"\centering " + markup(h1, False) + r" & \rotatebox{90}{\small " + markup(h2, False) + r"} & \rotatebox{90}{\small "
           + markup(h3, False) + r"} \\ \hline"]
    for r in rows:
        if r["kind"] == "heading":
            out.append(r"\hline\multicolumn{3}{|c|}{" + markup(r["text"], False) + r"} \\ \hline")
            continue
        name = "{}" + nl(r["text"])
        out.append(" & ".join([name, markup(r["reg_y"], False), markup(r["sum_y"], False)]) + r" \\")
    out.append(r"\hline\end{tabular}")
    return "\n".join(out)


def p3_intervals(rows):
    out = [r"\noindent\begin{tabular}{|p{\dimexpr\textwidth-22mm\relax}|>{\centering\arraybackslash}p{12mm}|}\hline"]
    for r in rows:
        out.append("{}" + nl(r["text"]) + " & " + markup(r["reg_y"], False) + r" \\")
    out.append(r"\hline\end{tabular}")
    return "\n".join(out)


def p3_caliphs(rows, heads):
    parts = (heads + [""] * 9)[:9]                 # name | reign | total | y | m | d | y | m | d
    c = r">{\centering\arraybackslash}p{6.5mm}"
    w = r"\dimexpr\textwidth-60mm\relax"
    # the name head is a bottom-aligned box in the first head row (no \multirow: a three-line head would overflow
    # into the first data row); the sub-heads are upright, as printed; a double rule between reign and total;
    # the name column is bottom-aligned (b), so the numbers of a two-line name stand on its last line, as printed
    out = [r"\setlength{\tabcolsep}{2pt}\noindent\begin{tabular}{|b{" + w + "}|" + "|".join([c] * 3) + "||" + "|".join([c] * 3) + "|}\\hline",
           r"\parbox[b]{" + w + r"}{\centering\small " + nl(parts[0]) + r"} & \multicolumn{3}{c||}{\small "
           + markup(parts[1], False) + r"} & \multicolumn{3}{c|}{\small " + markup(parts[2], False) + r"} \\ \cline{2-7}",
           " & " + " & ".join(r"{\scriptsize " + markup(p, False) + "}" for p in parts[3:9]) + r" \\ \hline"]
    for r in rows:
        if r["kind"] == "heading":
            out.append(r"\multicolumn{7}{|r|}{" + markup(r["text"], False) + r"} \\")
            continue
        out.append(" & ".join(["{}" + nl(r["text"])] + [markup(r[f], False) for f in NUMS]) + r" \\")
    out.append(r"\hline\end{tabular}")
    return "\n".join(out)


def p3_document():
    rows = read("chr_p3.tsv"); notes = read("chr_p3_footnotes.tsv")
    pages = {p["pdf"]: p for p in read("chr_p3_pages.tsv")}
    out = [PREAMBLE, r"\begin{document}"]
    for pdf in sorted({r["pdf"] for r in rows}, key=int, reverse=True):
        R = [r for r in rows if r["pdf"] == pdf]
        out.append(r"\clearpage")
        out.append(r"{\large \textarabic{" + R[0]["ppage"].translate(AR_DIGITS) + r"}}\par\vspace{1mm}")
        keys = []
        for r in R:
            if table_key(r["line"]) not in keys:
                keys.append(table_key(r["line"]))
        for i, key in enumerate(keys):
            T = [r for r in R if table_key(r["line"]) == key]
            if i:
                out.append(r"\par\vspace{5mm}")
            out.append(r"\begin{Arabic}")
            for r in T:
                if r["kind"] == "above":
                    out.append(r"\begin{center}" + markup(r["text"], False) + r"\end{center}\vspace{-2mm}")
                elif r["kind"] == "fol":
                    out.append(r"\begin{center}\textenglish{" + markup(r["text"]) + r"}\end{center}\vspace{-2mm}")
            for r in T:
                if r["kind"] == "title":
                    out.append(r"\noindent\fbox{\parbox{\dimexpr\textwidth-2\fboxsep-2\fboxrule}{\centering\large " + markup(r["text"], False) + r"}}\par\vspace{0.5mm}")
            heads = next((r["text"].split("|") for r in T if r["kind"] == "colhead"), [])
            sec = next((r["section"] for r in T if r["kind"] == "row"), "")
            data = [r for r in T if r["kind"] in ("row", "heading")]
            if sec == "K":
                right = [r for r in data if body(r["line"]).startswith("R")]
                left = [r for r in data if body(r["line"]).startswith("L")]
                out.append(r"\noindent\begin{minipage}[t]{0.495\textwidth}" + p3_kings_panel(right, heads) + r"\end{minipage}\hfill"
                           r"\begin{minipage}[t]{0.495\textwidth}" + p3_kings_panel(left, heads) + r"\end{minipage}")
            elif sec == "I":
                out.append(p3_intervals(data))
            elif sec == "C":
                out.append(p3_caliphs(data, heads))
            out.append(r"\end{Arabic}")
        F = [n for n in notes if n["pdf"] == pdf]
        if F:
            out.append(r"\par\vspace{3mm}\noindent\rule{40mm}{.4pt}\par\vspace{1mm}{\small " +
                       " --- ".join(f"{n['n']}) " + markup(n["text"]) for n in F) + r"}")
        if (pages.get(pdf) or {}).get("signature"):
            out.append(r"\par\vfill\hfill " + pages[pdf]["signature"])
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- Part II
def two_lines(s):
    """« Arabic // Latin // Latin » in a title or head: one line each. A line without Latin letters is one Arabic run,
    so that Nallino's folio bar « | » inside it stays in place."""
    lines = []
    for x in s.split("//"):
        if re.search(r"[A-Za-z]", x):
            lines.append(markup(x))
        else:                                       # an Arabic line may itself run over two printed lines (« / »)
            lines.extend(r"\textarabic{" + markup(y, False) + "}" for y in x.split(" / "))
    return r"\\".join(lines)


def p2_kings_column(rows, heads):
    h = (heads + ["", "", ""])[:3]
    out = [r"\begin{tabular}{p{43mm}|r|r}"]
    out.append(r"\shortstack{" + two_lines(h[0]) + r"} & \rotatebox{90}{\shortstack[l]{" + two_lines(h[1]) + r"}} & \rotatebox{90}{\shortstack[l]{"
               + two_lines(h[2]) + r"}} \\ \hline")
    for r in rows:
        if r["kind"].endswith("head"):
            out.append(r"\hline\multicolumn{3}{c}{\shortstack{" + two_lines(r["name"]) + r"}} \\ \hline")
            continue
        name = r"\hangindent=4mm\hangafter=1 " + nl(r["name"], True)
        vals = [markup(r["reg_y"]), markup(r["sum_y"])]
        extra = r["name"].count(" / ")
        if extra:
            vals = [r"\raisebox{-%d\normalbaselineskip}[0pt][0pt]{%s}" % (extra, v) if v else v for v in vals]
        out.append(" & ".join([name] + vals) + r" \\")
    out.append(r"\end{tabular}")
    return "\n".join(out)


def p2_intervals(rows):
    out = [r"\noindent\begin{tabular}{|p{\dimexpr\textwidth-24mm\relax}|r|}\hline"]
    for r in rows:
        name = r"\hangindent=4mm\hangafter=1 " + nl(r["name"], True)
        val = markup(r["reg_y"])
        extra = r["name"].count(" / ")
        if extra:
            val = r"\raisebox{-%d\normalbaselineskip}[0pt][0pt]{%s}" % (extra, val)
        out.append(name + " & " + val + r" \\")
    out.append(r"\hline\end{tabular}")
    return "\n".join(out)


def p2_caliphs(rows, heads):
    h = (heads + [""] * 6)[:6]                     # name | reign | total | Anni | Menses | Dies
    c = r">{\raggedleft\arraybackslash}p{5.5mm}"
    out = [r"\setlength{\tabcolsep}{2.5pt}\noindent\begin{tabular}{|p{\dimexpr\textwidth-60mm\relax}|" + "|".join([c] * 3) + "|" + "|".join([c] * 3) + "|}\\hline",
           r"\parbox[b]{\dimexpr\textwidth-62mm\relax}{\centering\small\vspace{1mm}" + two_lines(h[0]) + r"\vspace{1mm}} & \multicolumn{3}{c|}{\parbox[b]{23mm}{\centering\small "
           + two_lines(h[1]) + r"\vspace{1mm}}} & \multicolumn{3}{c|}{\parbox[b]{23mm}{\centering\small " + two_lines(h[2]) + r"\vspace{1mm}}} \\ \cline{2-7}",
           " & " + " & ".join(r"\rotatebox{90}{\scriptsize\shortstack[l]{" + two_lines(x) + "}}" for x in [h[3], h[4], h[5]] * 2) + r" \\ \hline"]
    for r in rows:
        name = r"\hangindent=4mm\hangafter=1 " + nl(r["name"], True)
        vals = [markup(r[f]) for f in NUMS]
        extra = r["name"].count(" / ")
        if extra:
            vals = [r"\raisebox{-%d\normalbaselineskip}[0pt][0pt]{%s}" % (extra, v) if v else v for v in vals]
        out.append(" & ".join([name] + vals) + r" \\")
    out.append(r"\hline\end{tabular}")
    return "\n".join(out)


def p2_document():
    rows = read("chr_p2.tsv"); pages = {p["pdf"]: p for p in read("chr_p2_pages.tsv")}
    out = [PREAMBLE, r"\begin{document}"]
    for pdf in sorted({r["pdf"] for r in rows}, key=int):
        R = [r for r in rows if r["pdf"] == pdf]; P = pages.get(pdf, {})
        out.append(r"\clearpage")
        if P.get("head"):
            l, c, rr = (P["head"].split("|") + ["", "", ""])[:3]
            out.append(r"\noindent\makebox[\textwidth]{\textbf{" + l + r"}\hfill{\small " + c + r"}\hfill\textbf{" + rr + r"}}\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{2mm}")
        for part in filter(None, (P.get("above") or "").split("}//{")):
            kind, _, txt = part.strip("{}").partition(":")
            size = r"\small " if kind == "small" else ""
            out.append(r"\begin{center}" + size + markup(txt).replace("//", r"\\") + r"\end{center}")
        sections = []
        for r in R:
            if r["section"] not in sections:
                sections.append(r["section"])
        for sec in sections:
            S = [r for r in R if r["section"] == sec]
            for r in S:
                if r["kind"] == "title":
                    out.append(r"\begin{center}\fbox{\parbox{0.95\textwidth}{\centering\bfseries " + two_lines(r["name"]) + r"}}\end{center}")
            heads = next((r["name"].split("|") for r in S if r["kind"] == "colhead"), [])
            if sec == "K":
                left = [r for r in S if r["kind"] in ("L", "Lhead")]; right = [r for r in S if r["kind"] in ("R", "Rhead")]
                out.append(r"\noindent\begin{minipage}[t]{0.5\textwidth}{\small " + p2_kings_column(left, heads) + r"}\end{minipage}\vrule\,\vrule\hfill"
                           r"\begin{minipage}[t]{0.48\textwidth}{\small " + p2_kings_column(right, heads) + r"}\end{minipage}\par\vspace{4mm}")
            elif sec == "I":
                out.append(p2_intervals([r for r in S if r["kind"] == "T"]))
            elif sec == "C":
                out.append(p2_caliphs([r for r in S if r["kind"] == "T"], heads))
        if P.get("signature"):
            out.append(r"\par\vfill\hfill " + P["signature"])
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p3_chronology.tex").write_text(p3_document(), encoding="utf-8", newline="\n")
    (HERE / "p2_chronology.tex").write_text(p2_document(), encoding="utf-8", newline="\n")
    print("wrote p3_chronology.tex, p2_chronology.tex")

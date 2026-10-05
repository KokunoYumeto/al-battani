"""Generate the two diplomatic editions of al-Battani's geographical tables (94 regions, then the cities):
  p3_geography.tex - Nallino Part III (Arabic, Maghribi abjad), one page per source page, two panels as printed
  p2_geography.tex - Nallino Part II (Latin transliteration, Western numerals, notes), one page per source page
Data: geo_p3.tsv, geo_p3_footnotes.tsv, geo_p3_pages.tsv, geo_p2.tsv, geo_p2_notes.tsv, geo_p2_pages.tsv.
Part III rows: line R.. = right panel, L.. = left panel (reading order: right panel first). Part II rows: kind L/R =
left/right column of the page. The two panels/columns are independent tables, as in the print."""
import re
from pathlib import Path

from gen_stars import PREAMBLE, AR_DIGITS, markup, read

HERE = Path(__file__).resolve().parent


def p3_panel(rows, head):
    out = [r"\setlength{\tabcolsep}{2.2pt}\begin{tabular}{|p{55mm}|>{\centering\arraybackslash}p{4.8mm}>{\centering\arraybackslash}p{4.8mm}|"
           r">{\centering\arraybackslash}p{4.8mm}>{\centering\arraybackslash}p{4.8mm}|}\hline"]
    out.append(r"\centering " + markup(head, False) + r" & \multicolumn{2}{c|}{الطول} & \multicolumn{2}{c|}{العرض} \\ \hline")
    for r in rows:
        name = "{}" + markup(r["text"], False).replace(" / ", r"\newline ")   # {} keeps a leading [ from reading as \\[..]
        vals = [markup(r[f], False) for f in ("lon_d", "lon_m", "lat_d", "lat_m")]
        extra = r["text"].count(" / ")
        if extra:
            vals = [r"\raisebox{-%d\normalbaselineskip}[0pt][0pt]{%s}" % (extra, v) if v else v for v in vals]
        out.append(" & ".join([name] + vals) + r" \\")
    out.append(r"\hline\end{tabular}")
    return "\n".join(out)


def table_key(line):
    """A page can hold more than one table: line ids of the second table carry the prefix 2 (2R01, 2H01, ...)."""
    return line[0] if line[:1].isdigit() else "1"


def p3_document():
    rows = read("geo_p3.tsv"); notes = read("geo_p3_footnotes.tsv")
    pages = {p["pdf"]: p for p in read("geo_p3_pages.tsv")}
    out = [PREAMBLE, r"\begin{document}"]
    for pdf in sorted({r["pdf"] for r in rows}, key=int, reverse=True):
        R = [r for r in rows if r["pdf"] == pdf]
        out.append(r"\clearpage")
        out.append(r"{\large \textarabic{" + R[0]["ppage"].translate(AR_DIGITS) + r"}}\par\vspace{1mm}")
        if (pages.get(pdf) or {}).get("above"):
            out.append(r"\begin{center}" + pages[pdf]["above"] + r"\end{center}")
        keys = []
        for r in R:
            if table_key(r["line"]) not in keys:
                keys.append(table_key(r["line"]))
        for i, key in enumerate(keys):
            T = [r for r in R if table_key(r["line"]) == key]
            body = (lambda s: s[1:]) if key != "1" else (lambda s: s)
            if i:
                out.append(r"\par\vspace{6mm}")
            for r in T:
                if r["kind"] == "fol":                                  # e.g. « Fol. 176,r. » above a table
                    out.append(r"\begin{center}" + markup(r["text"]) + r"\end{center}\vspace{-2mm}")
            title = [r for r in T if r["kind"] == "title"]
            heads = [r for r in T if r["kind"] == "colhead"]
            shared = next((r["text"] for r in heads if not r["line"].endswith(("R", "L"))), "من اسماء البلدان")
            head_r = next((r["text"] for r in heads if r["line"].endswith("R")), shared)   # a panel may have its own head
            head_l = next((r["text"] for r in heads if r["line"].endswith("L")), shared)
            out.append(r"\begin{Arabic}")
            if title:
                out.append(r"\noindent\fbox{\parbox{\dimexpr\textwidth-2\fboxsep-2\fboxrule}{\centering\large " + markup(title[0]["text"], False) + r"}}\par\vspace{0.5mm}")
            right = [r for r in T if r["kind"] == "row" and body(r["line"]).startswith("R")]
            left = [r for r in T if r["kind"] == "row" and body(r["line"]).startswith("L")]
            out.append(r"\noindent\begin{minipage}[t]{0.495\textwidth}" + p3_panel(right, head_r) + r"\end{minipage}\hfill"
                       r"\begin{minipage}[t]{0.495\textwidth}" + p3_panel(left, head_l) + r"\end{minipage}")
            out.append(r"\end{Arabic}")
        F = [n for n in notes if n["pdf"] == pdf]
        if F:
            out.append(r"\par\vspace{3mm}\noindent\rule{40mm}{.4pt}\par\vspace{1mm}{\small " +
                       " --- ".join(f"{n['n']}) " + markup(n["text"]) for n in F) + r"}")
        if (pages.get(pdf) or {}).get("signature"):
            out.append(r"\par\vfill\hfill " + pages[pdf]["signature"])
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


def p2_column(rows, head):
    out = [r"\begin{tabular}{p{40mm}|r@{\hspace{1.4mm}}r|r@{\hspace{1.4mm}}r}"]
    out.append(r"\centering " + head + r" & \multicolumn{2}{c|}{Longit.} & \multicolumn{2}{c}{Latitudo.} \\ \hline")
    for r in rows:
        if r["extra"] == "print:nonum":                         # continuation of a row begun on the previous page
            label = r"\phantom{" + r["no"] + ".}"
        elif r["extra"].startswith("print:") and not r["extra"].startswith("print:values"):
            label = r["extra"][6:]
        else:
            label = r["no"] + "."
        name = r"\hangindent=4mm\hangafter=1 " + label + " " + markup(r["name"]).replace(" / ", r"\newline ")
        if r["kind"].endswith("part"):                          # a row whose values stand on the next page
            out.append(name + r" & & & & \\")
            continue
        vals = [markup(r[f]) for f in ("lon_d", "lon_m", "lat_d", "lat_m")]
        if r["extra"].startswith("lat:"):                       # e.g. « 12 austr. » in place of the minutes
            vals[3] = r"{\scriptsize\bfseries " + r["extra"][4:] + "}"
        extra = r["name"].count(" / ")
        if r["extra"] == "print:values-low":
            extra += 1                                          # Nallino's slip: the values stand one line low
        if extra:
            vals = [r"\raisebox{-%d\normalbaselineskip}[0pt][0pt]{%s}" % (extra, v) if v else v for v in vals]
        out.append(" & ".join([name] + vals) + r" \\")
    out.append(r"\end{tabular}")
    return "\n".join(out)


def p2_ttable(rows, tnotes):
    """Part II table with a notes column (Urbes | Longitudines | Latitudines | Notae), as on pp. 219-220."""
    out = [r"{\small\setlength{\tabcolsep}{3pt}\noindent\begin{tabular}{|p{38mm}|r@{\hspace{1.4mm}}r|r@{\hspace{1.4mm}}r|p{\dimexpr\textwidth-76mm\relax}|}\hline"]
    out.append(r"\centering\textsc{Urbes} & \multicolumn{2}{c|}{\shortstack{Longitu-\\dines}} & \multicolumn{2}{c|}{Latitudines} & "
               r"\centering\textsc{Notae}\tabularnewline\hline")
    for r in rows:
        vals = [markup(r[f]) for f in ("lon_d", "lon_m", "lat_d", "lat_m")]
        out.append(" & ".join([markup(r["name"])] + vals + [r"\raggedright " + markup(tnotes.get(r["no"], ""))]) + r"\tabularnewline")
    out.append(r"\hline\end{tabular}}")
    return "\n".join(out)


def p2_document():
    rows = read("geo_p2.tsv"); notes = read("geo_p2_notes.tsv"); pages = {p["pdf"]: p for p in read("geo_p2_pages.tsv")}
    out = [PREAMBLE, r"\begin{document}"]
    for pdf in sorted({r["pdf"] for r in rows}, key=int):
        R = [r for r in rows if r["pdf"] == pdf]; P = pages.get(pdf, {})
        out.append(r"\clearpage")
        if P.get("head"):
            l, c, rr = (P["head"].split("|") + ["", "", ""])[:3]
            out.append(r"\noindent\makebox[\textwidth]{\textbf{" + l + r"}\hfill{\small " + c + r"}\hfill\textbf{" + rr + r"}}\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{2mm}")
        for part in filter(None, (P.get("above") or "").split("}//{")):
            kind, _, txt = part.strip("{}").partition(":")
            if kind == "title":
                out.append(r"\begin{center}\fbox{\parbox{0.95\textwidth}{\centering\large\bfseries " + markup(txt).replace("//", r"\\") + r"}}\end{center}")
            else:
                out.append(r"\begin{center}{\small " + markup(txt) + r"}\end{center}")
        T = [r for r in R if r["kind"] == "T"]
        tnos = {r["no"] for r in T}
        if T:                                                           # a table with a notes column (pp. 219-220)
            out.append(p2_ttable(T, {n["no"]: n["text"] for n in notes if n["pdf"] == pdf and n["no"] in tnos}))
        else:
            first = min(int(r["no"]) for r in R if r["kind"] in ("L", "R", "Lpart", "Rpart"))
            head = "Nomina urbium." if first >= 94 else "Regionum nomina."
            left = [r for r in R if r["kind"] in ("L", "Lpart")]; right = [r for r in R if r["kind"] in ("R", "Rpart")]
            out.append(r"\noindent\begin{minipage}[t]{0.5\textwidth}{\small " + p2_column(left, head) + r"}\end{minipage}\vrule\,\vrule\hfill"
                       r"\begin{minipage}[t]{0.48\textwidth}{\small " + p2_column(right, head) + r"}\end{minipage}")
        for n in notes:                                                 # text paragraphs printed between table and notes
            if n["pdf"] == pdf and n["no"].startswith("¶"):
                out.append(r"\par\vspace{3mm}" + markup(n["text"]))
        N = [n for n in notes if n["pdf"] == pdf and n["no"] != "*" and n["text"] and n["no"] not in tnos and not n["no"].startswith("¶")]
        if N:
            out.append(r"\par\vspace{3mm}{\small")
            for n in N:
                lab = n["label"] + " " if n["label"] else ""
                out.append(r"\par\hangindent=8mm\hangafter=1 " + lab + markup(n["text"]))
            out.append(r"\par}")
        FN = [n for n in notes if n["pdf"] == pdf and n["no"] == "*"]          # Nallino's footnotes (1), (2), ... below a rule
        if FN:
            out.append(r"\par\vspace{2mm}\begin{center}\rule{40mm}{.4pt}\end{center}")
            for n in FN:
                out.append(r"{\small " + n["label"] + " " + markup(n["text"]) + r"}\par")
        if P.get("signature"):
            out.append(r"\par\vfill\hfill " + P["signature"])
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p3_geography.tex").write_text(p3_document(), encoding="utf-8", newline="\n")
    (HERE / "p2_geography.tex").write_text(p2_document(), encoding="utf-8", newline="\n")
    print("wrote p3_geography.tex, p2_geography.tex")

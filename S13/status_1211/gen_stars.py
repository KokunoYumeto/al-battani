"""Generate the two diplomatic editions of al-Battani's star catalogue from the checked TSV data:
  p3_star_catalogue.tex - Nallino Part III (Arabic, codex numerals in Maghribi abjad), one page per source page
  p2_star_catalogue.tex - Nallino Part II (Latin, Western numerals, notes), one page per source page
Markup in the TSV text: {fnN} footnote mark, {ov:..} overlined numeral, {0} zero sign, {sp:..} letter-spaced name,
{sfrac:a/b} small fraction, **bold**, *italic*, ' / ' line break inside a cell, {BR:word:n}/{BR} direction bracket."""
import csv, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARABIC_RUN = re.compile(r"([\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]+(?:[ \u060C][\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]+)*)")
AR_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


def read(name):
    return [{k: (v or "") for k, v in r.items()} for r in csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t")]


def markup(s, latin=True):
    s = s.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#")
    s = re.sub(r"\{fn(\d+)\}", r"\\textsuperscript{\1}", s)
    s = re.sub(r"\{ov:([^}]*)\}", r"\\AbjadOver{\1}", s)
    s = re.sub(r"\{rd:(.)=.\}", r"\1", s)                  # print the glyph as printed
    s = re.sub(r"\{zero:([^}]*)\}", r"\1", s)              # a word printed for "none" (read as 0 by the check)
    s = re.sub(r"\{sc:([^}]*)\}", r"\\textsc{\1}", s)
    s = s.replace("{0}", "\uFDFC")      # placeholder inside the Arabic block: a zero sign stays in its Arabic run (RTL order)
    s = re.sub(r"\{sp:([^}]*)\}", r"\\Name{\1}", s)
    s = re.sub(r"\{sfrac:([^/}]+)/([^}]+)\}", lambda m: "$\\tfrac{" + m.group(1).replace("°", "^\\circ") + "}{" + m.group(2) + "}$", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"\*([^*]+)\*", r"\\textit{\1}", s)
    if latin:  # Arabic words inside Latin text
        s = ARABIC_RUN.sub(lambda m: r"\textarabic{" + m.group(1) + "}", s)
    return s.replace("﷼", r"\AbjadZero{}")


PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[paperwidth=210mm,paperheight=297mm,margin=16mm]{geometry}
\usepackage{fontspec,amsmath,array,multirow,graphicx}
\usepackage{polyglossia}
\setmainlanguage{latin}\setotherlanguages{arabic,greek}
\setmainfont{Linux Libertine O}[Ligatures=TeX]
\newfontfamily\arabicfont{Amiri}[Script=Arabic]
\newfontfamily\greekfont{FreeSerif}[Script=Greek]
\newfontfamily\NallinoSigns{NallinoSigns.otf}[Path=./fonts/]
\newcommand{\AbjadZero}{{\NallinoSigns\symbol{"E000}}}
\newcommand{\AbjadOver}[1]{\leavevmode\vbox{\hrule height .45pt\kern1.2pt\hbox{#1}}}
\newcommand{\Name}[1]{{\addfontfeatures{LetterSpace=12}#1}}
\pagestyle{empty}\setlength{\parindent}{0pt}
\renewcommand{\arraystretch}{1.18}
"""


def p3_document():
    rows = read("p3_stars.tsv")
    notes = read("p3_footnotes.tsv")
    sigs = {r["pdf"]: r["signature"] for r in read("p3_pages.tsv")} if (HERE / "p3_pages.tsv").exists() else {}
    out = [PREAMBLE, r"\begin{document}"]
    for pdf in sorted({r["pdf"] for r in rows}, key=int, reverse=True):      # Arabic reading order: descending PDF
        R = [r for r in rows if r["pdf"] == pdf]
        ppage = R[0]["ppage"]
        out.append(r"\clearpage")
        out.append(r"{\large " + r"\textarabic{" + ppage.translate(AR_DIGITS) + r"}}\par\vspace{2mm}")
        for r in R:
            if r["kind"] == "above":
                out.append(r"\begin{center}\textbf{" + markup(r["text"]) + r"}\end{center}")
        out.append(r"\begin{Arabic}\begin{tabular}{|p{84mm}|>{\centering\arraybackslash}p{9mm}|>{\centering\arraybackslash}p{9mm}|>{\centering\arraybackslash}p{9mm}|>{\centering\arraybackslash}p{9mm}|>{\centering\arraybackslash}p{14mm}|>{\centering\arraybackslash}p{17mm}|}\hline")
        for r in R:
            k = r["kind"]
            if k == "title":
                out.append(r"\multicolumn{7}{|c|}{\parbox{168mm}{\centering\large " + markup(r["text"], False).replace(" / ", r"\\") + r"}} \\ \hline")
            elif k == "colhead":
                out.append(r"\multirow{2}{*}{\parbox{80mm}{\centering " + markup(r["text"], False) + r"}} & \multicolumn{2}{c|}{الطول} & \multicolumn{2}{c|}{العرض} & \multirow{2}{*}{\parbox{13mm}{\centering\small علامات الجهة}} & \multirow{2}{*}{\parbox{16mm}{\centering\small مراتب العظمة}} \\ \cline{2-5}")
                out.append(r" & {\small درج} & {\small دقائق} & {\small درج} & {\small دقائق} & & \\ \hline")
            elif k == "heading":
                out.append(r"\multicolumn{7}{|c|}{\large " + markup(r["text"], False) + r"} \\ \hline")
            elif k == "star":
                d = r["dir"]
                m = re.fullmatch(r"\{BR:(.+):(\d+)\}", d)
                if m:
                    d = r"\multirow{" + m.group(2) + r"}{*}{\rotatebox[origin=c]{-90}{\large " + m.group(1) + "}}"
                elif d == "{BR}":
                    d = ""
                else:
                    d = markup(d, False)                     # e.g. the zero sign in the direction column
                extra = r["text"].count(" / ")
                cells = [markup(r["text"], False).replace(" / ", r"\newline ")] + [markup(r[f], False) for f in ("lon_d", "lon_m", "lat_d", "lat_m")] + [d, markup(r["mag"], False)]
                if extra:
                    cells = cells[:1] + [r"\raisebox{-%d\normalbaselineskip}[0pt][0pt]{%s}" % (extra, c) if c and not c.startswith(r"\multirow") else c for c in cells[1:]]
                out.append(" & ".join(cells) + r" \\")
            elif k == "centerline":                          # a line across the whole table, column rules interrupted
                out.append(r"\multicolumn{7}{|c|}{" + markup(r["text"], False) + r"} \\")
            if k in ("star", "centerline"):
                nxt = R[R.index(r) + 1] if R.index(r) + 1 < len(R) else None
                if nxt is None or nxt["kind"] not in ("star", "centerline"):
                    out.append(r"\hline")
        out.append(r"\end{tabular}\end{Arabic}")
        F = [n for n in notes if n["pdf"] == pdf]
        if F:
            out.append(r"\par\vspace{3mm}\noindent\rule{40mm}{.4pt}\par\vspace{1mm}{\small " +
                       " --- ".join(f"{n['n']}) " + markup(n["text"]) for n in F) + r"}")
        if sigs.get(pdf):
            out.append(r"\par\vfill\hfill " + sigs[pdf])
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


def p2_document():
    rows = read("p2_stars.tsv"); notes = read("p2_notes.tsv"); pages = {p["pdf"]: p for p in read("p2_pages.tsv")}
    labels = {}
    for r in rows:
        if r["kind"] == "heading" and re.search(r"\*\*([^*]+)\*\*", r["desc"]):   # a bracketed lacuna note has no bold label
            labels[r["section"]] = re.search(r"\*\*([^*]+)\*\*", r["desc"]).group(1)
    seen_sections = set()
    out = [PREAMBLE, r"\begin{document}"]
    for pdf in sorted({r["pdf"] for r in rows}, key=int):
        R = [r for r in rows if r["pdf"] == pdf]; P = pages.get(pdf, {})
        out.append(r"\clearpage")
        if P.get("head"):
            l, c, rr = (P["head"].split("|") + ["", "", ""])[:3]
            out.append(r"\noindent\makebox[\textwidth]{\textbf{" + l + r"}\hfill{\small " + c + r"}\hfill\textbf{" + rr + r"}}\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{2mm}")
        for part in filter(None, (P.get("above") or "").split("}//{")):
            part = part.strip("{}")
            kind, _, txt = part.partition(":")
            if kind == "small":
                out.append(r"\begin{center}{\small " + markup(txt) + r"}\end{center}")
            elif kind == "title":
                out.append(r"\begin{center}{\large\bfseries " + markup(txt).replace("//", r"\\") + r"}\end{center}")
            elif kind == "rule":
                out.append(r"\begin{center}\rule{30mm}{.4pt}\end{center}")
            elif kind == "center":
                out.append(r"\begin{center}" + markup(txt) + r"\end{center}")
        out.append(r"\begin{center}\begin{tabular}{r||p{78mm}|r@{\hspace{2.2mm}}r|r@{\hspace{2.2mm}}r|c|c||l}\cline{2-8}")
        out.append(r" & \centering Stellarum descriptio. & \multicolumn{2}{c|}{Longitudo.} & \multicolumn{2}{c|}{Latitudo.} & \parbox{9mm}{\centering\small Plaga Caeli.} & Magnitudo. & \\ \cline{2-8}")
        for r in R:
            if r["kind"] == "heading":
                out.append(r" & \multicolumn{7}{c||}{\parbox{150mm}{\centering\rule{0pt}{5mm}" + markup(r["desc"]).replace(" / ", r"\\") + r"}} & \\ \cline{2-8}")
            elif r["kind"] == "subheading":
                out.append(r" & \multicolumn{7}{l}{\hspace*{4mm}" + markup(r["desc"]) + r"} & \\")
            elif r["kind"] == "centerline":                    # a line centred across the table, inner rules interrupted
                out.append(r" & \multicolumn{7}{c||}{" + markup(r["desc"]) + r"} & \\")
            else:
                top = r["desc"].startswith("{top}")
                rd = r["desc"][5:] if top else r["desc"]
                desc = markup(rd).replace(" / ", r"\newline\hspace*{4mm}")
                cells = [r["no"], desc] + [markup(r[f]) for f in ("lon_d", "lon_m", "lat_d", "lat_m", "plaga", "mag", "ident")]
                # numbers sit on the last line of a wrapped description (zero-height lowering keeps the row height)
                extra = 0 if top else rd.count(" / ")
                if extra:
                    cells = [r["no"], desc] + [r"\raisebox{-%d\normalbaselineskip}[0pt][0pt]{%s}" % (extra, c) if c else c for c in cells[2:]]
                out.append(" & ".join(cells) + r" \\")
        out.append(r"\cline{2-8}\end{tabular}\end{center}")
        N = [n for n in notes if n["pdf"] == pdf and n["no"] not in ("*", "label") and n["text"]]
        printed = {n["section"]: n["text"] for n in notes if n["pdf"] == pdf and n["no"] == "label"}
        if N:
            out.append(r"{\small")
            for n in N:
                if n["section"] not in seen_sections and n["no"] != "cont":
                    seen_sections.add(n["section"])
                    # the "(1)" call of a footnote stands after the section label only where the print puts it there
                    star = any(x["pdf"] == pdf and x["section"] == n["section"] and x["no"] == "*" and "print:label-mark" in x["codex"] for x in notes)
                    out.append(r"\par\hspace*{8mm}\textbf{" + printed.get(n["section"], labels.get(n["section"], n["section"])) + r"}" + (" (1)" if star else "") + ":")
                num = "" if n["no"] == "cont" else n["no"] + (" " if "print:no-period" in n["codex"] else ". ")   # Nallino's slip: "5 Long."
                out.append(r"\par\hangindent=12mm\hangafter=1 " + num + markup(n["text"]))
            out.append(r"\par}")
        for n in notes:
            if n["pdf"] == pdf and n["no"] == "*":
                out.append(r"\par\vspace{2mm}\begin{center}\rule{40mm}{.4pt}\end{center}{\small " + markup(n["text"]) + r"}")
        if P.get("signature"):
            out.append(r"\par\vfill\hfill " + P["signature"])
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":                                 # importable: gen_status.py reuses markup() and PREAMBLE
    (HERE / "p3_star_catalogue.tex").write_text(p3_document(), encoding="utf-8", newline="\n")
    (HERE / "p2_star_catalogue.tex").write_text(p2_document(), encoding="utf-8", newline="\n")
    print("wrote p3_star_catalogue.tex, p2_star_catalogue.tex")

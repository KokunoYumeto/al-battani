"""S15 - al-Battani's book on the indications of the conjunctions and the eclipses (his astrological history), the
Arabic text as edited by George Saliba in E. S. Kennedy, B. van Dalen, G. Saliba and J. Samso, "Al-Battani's
astrological history", Suhayl 9 (2009-2010), pp. 13-148, where it is reproduced as page images: the title on p. 17
and the text on the even pages 18-78 (PDF pages 5-66 of the publication). The text and the editors' apparatus are
transcribed from those images,
one line of this edition for each printed line; the horoscope charts are transcribed cell by cell and drawn again.
The translation and the commentary of the article are not reproduced.

Page files (pages/AB02-PDF####.txt):
  @page PDF PRINTED        the page of the publication (PDF page, printed page)
  % ...                    a comment
  TEXT                     one printed line of the Arabic text; prefixes: "@c " a centred line, "@h " a heading
                           (centred, bold), "@p " a line printed with a paragraph indent, "@s " a line set in a
                           smaller type than the lines around it; inline: {f:٢٧ظ} the
                           folio of the manuscript printed in the margin beside the line, {n:٥} the line number
                           printed in the margin (checked against the count), {sup:٢} a raised sign, {h:TEXT} words
                           set in the larger, heavier type of the headings within a line of text, {b:TEXT} bold,
                           {ov:TEXT} letters printed with a line above them (abjad numbers), {0} the sign printed
                           for zero in an abjad number (it has the form of a small ح with a flat top; the records
                           keep {0}, the PDF draws it with ح), {br} the break between the two printed lines of
                           a heading that the editors count as one line
  @chart ID                a horoscope chart after the line before it, then lines "@cell POS: TEXT | TEXT ..."
                           (POS: top, bottom, left, right, centre, top-left-top, top-left-left, top-right-top,
                           top-right-right, bottom-left-left, bottom-left-bottom, bottom-right-bottom,
                           bottom-right-right; « | » separates the printed lines of a cell), closed by @endchart
  @app                     the lines that follow are the editors' apparatus at the foot of the page
  @obs TEXT                an observation on the print, kept in the record
Writes historia.tex, records/AB02-PDF####.json, anchors.tsv, apparatus.tsv, folios.tsv, charts.tsv.
python build_historia.py"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
AR_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
POS = {  # the centroid of each cell on a 9 x 9 square: a 3 x 3 grid, the corner squares halved by their diagonals
    "top": (4.5, 7.5), "bottom": (4.5, 1.5), "left": (1.5, 4.5), "right": (7.5, 4.5), "centre": (4.5, 4.5),
    "top-left-top": (2.0, 8.0), "top-left-left": (1.0, 7.0), "top-right-top": (7.0, 8.0), "top-right-right": (8.0, 7.0),
    "bottom-left-left": (1.0, 2.0), "bottom-left-bottom": (2.0, 1.0), "bottom-right-bottom": (7.0, 1.0),
    "bottom-right-right": (8.0, 2.0)}
RIGHT_ANGLE = {  # the right-angled corner of each triangular cell: cells of several lines are drawn nearer to it
    "top-left-top": (3, 9), "top-left-left": (0, 6), "top-right-top": (6, 9), "top-right-right": (9, 6),
    "bottom-left-left": (0, 3), "bottom-left-bottom": (3, 0), "bottom-right-right": (9, 3), "bottom-right-bottom": (6, 0)}


def folio_label(s):
    """٢٧ظ -> 27v, ٢٨و -> 28r"""
    m = re.fullmatch(r"([٠-٩]+)\s*([ظو])", s.strip())
    return m.group(1).translate(AR_DIGITS) + ("v" if m.group(2) == "ظ" else "r")


def esc(s):
    return (s.replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%").replace("$", r"\$")
            .replace("#", r"\#").replace("_", r"\_").replace("{", r"\{").replace("}", r"\}"))


def artex(s):
    """TeX for a line: TeX specials escaped; {sup:X} raised; {h:X} in the type of the headings; {b:X} bold;
    {ov:X} overlined; {0} the zero sign"""
    s = s.replace("{0}", "").replace("{br}", "")
    out, pos = [], 0
    for m in re.finditer(r"\{(sup|h|b|ov):([^}]*)\}", s):
        out.append(esc(s[pos:m.start()]))
        body = esc(m.group(2))
        out.append({"sup": r"\textsuperscript{" + body + "}", "h": r"{\bfseries\large " + body + "}",
                    "b": r"{\bfseries " + body + "}", "ov": r"\Ov{" + body + "}"}[m.group(1)])
        pos = m.end()
    out.append(esc(s[pos:]))
    return "".join(out).replace("", r"\ZeroSign{}").replace("", r"\\")


def parse(path):
    rec = {"pdf": None, "printed": None, "lines": [], "charts": [], "app": [], "obs": [], "comment": []}
    mode, chart = "text", None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        if raw.startswith("%"):
            rec["comment"].append(raw[1:].strip())
            continue
        if raw.startswith("@page"):
            _, pdf, printed = raw.split()
            rec["pdf"], rec["printed"] = int(pdf), printed
            continue
        if raw.startswith("@obs"):
            rec["obs"].append(raw[4:].strip())
            continue
        if raw.startswith("@app"):
            mode = "app"
            continue
        if raw.startswith("@chart"):
            chart = {"id": raw.split()[1], "after_line": len(rec["lines"]), "cells": []}
            mode = "chart"
            continue
        if raw.startswith("@endchart"):
            rec["charts"].append(chart)
            chart, mode = None, "text"
            continue
        if mode == "chart":
            m = re.match(r"@cell ([a-z-]+):\s*(.*)$", raw)
            assert m and m.group(1) in POS, (path.name, raw)
            chart["cells"].append({"pos": m.group(1), "lines": [x.strip() for x in m.group(2).split("|")]})
            continue
        if mode == "app":
            rec["app"].append(raw.strip())
            continue
        kind = "text"
        if raw.startswith("@c "):
            kind, raw = "centre", raw[3:]
        elif raw.startswith("@h "):
            kind, raw = "heading", raw[3:]
        elif raw.startswith("@p "):
            kind, raw = "indent", raw[3:]
        elif raw.startswith("@s "):
            kind, raw = "small", raw[3:]
        folio = None
        m = re.search(r"\{f:([^}]*)\}", raw)
        if m:
            folio = m.group(1).strip()
        num = None
        m = re.search(r"\{n:([^}]*)\}", raw)
        if m:
            num = int(m.group(1).strip().translate(AR_DIGITS))
        text = re.sub(r"\{[fn]:[^}]*\}", "", raw).strip()
        text = re.sub(r"\s+", " ", text)
        rec["lines"].append({"kind": kind, "text": text, "folio": folio, "printed_number": num})
    return rec


def chart_tex(ch):
    out = [r"\par\medskip\begin{center}\begin{tikzpicture}[x=12mm,y=12mm,line width=0.5pt]",
           r"\draw (0,0) rectangle (9,9); \draw (3,0)--(3,9) (6,0)--(6,9) (0,3)--(9,3) (0,6)--(9,6);",
           r"\draw (0,9)--(3,6) (9,9)--(6,6) (0,0)--(3,3) (9,0)--(6,3);"]
    for cell in ch["cells"]:
        x, y = POS[cell["pos"]]
        n = len([t for t in cell["lines"] if t])
        body = r"\\".join(r"\RL{\ArC " + artex(t) + "}" for t in cell["lines"] if t)
        if cell["pos"] in RIGHT_ANGLE and n >= 3:
            # a triangle of three lines or more: the block is set into its right-angled corner, where it has room
            rx, ry = RIGHT_ANGLE[cell["pos"]]
            ix, iy = (1 if rx in (0, 6) else -1), (1 if ry in (0, 6) else -1)   # towards the inside of the square
            anchor = ("south" if iy > 0 else "north") + (" west" if ix > 0 else " east")
            align = "left" if ix > 0 else "right"
            out.append(rf"\node[anchor={anchor},align={align},font=\scriptsize,inner sep=0pt] "
                       rf"at ({rx + 0.12 * ix},{ry + 0.12 * iy}) {{{body}}};")
            continue
        if cell["pos"] in RIGHT_ANGLE:
            f = min(0.15 * (n - 1), 0.45)
            rx, ry = RIGHT_ANGLE[cell["pos"]]
            x, y = round(x + f * (rx - x), 3), round(y + f * (ry - y), 3)
        out.append(rf"\node[align=center,font=\scriptsize,inner sep=0pt] at ({x},{y}) {{{body}}};")
    out.append(r"\end{tikzpicture}\end{center}\medskip")
    return "\n".join(out)


PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[a4paper,left=26mm,right=34mm,top=22mm,bottom=22mm]{geometry}
\usepackage{fontspec,tikz,needspace}
\usepackage[unicode,hidelinks]{hyperref}
\usepackage{polyglossia}
\setmainlanguage{english}
\setotherlanguages{arabic}
\setmainfont{Linux Libertine O}[Ligatures=TeX]
\newfontfamily\arabicfont{Amiri}[Script=Arabic]
\newfontfamily\ArBody{Amiri}[Script=Arabic,Scale=1.08]
\newfontfamily\ArApp{Amiri}[Script=Arabic,Scale=0.92]
\newfontfamily\ArC{Amiri}[Script=Arabic]
\hypersetup{pdftitle={al-Battani, Kitab fi dala'il al-qiranat wa-l-kusufat (astrological history), ed. G. Saliba (Suhayl 9). S15},pdfauthor={al-Battani; ed. George Saliba}}
\setlength{\parindent}{0pt}\setlength{\parskip}{0pt}
\tracinglostchars=2
\newcommand{\PageHead}[3]{\par\bigskip\penalty-300\pdfbookmark[1]{p. #2 (PDF #1)}{pg-#1}\hypertarget{AB02-PDF#3}{}%
 {\large\bfseries p.\,#2}\enspace{\footnotesize (PDF #1)}\par\smallskip}
% one printed line: right to left; in the right margin its number and, where printed, the folio of the manuscript
\newcommand{\EdL}[4]{\par\noindent\hypertarget{#2}{}\hbox to\linewidth{\parbox[t]{\linewidth}{\setRTL\ArBody\raggedleft #4\par}\rlap{\hspace{3mm}\footnotesize #1\enspace #3}}\par}
\newcommand{\EdLc}[4]{\par\noindent\hypertarget{#2}{}\hbox to\linewidth{\parbox[t]{\linewidth}{\setRTL\ArBody\centering #4\par}\rlap{\hspace{3mm}\footnotesize #1\enspace #3}}\par}
\newcommand{\EdLh}[4]{\EdLc{#1}{#2}{#3}{\bfseries #4}}
\newcommand{\EdLp}[4]{\EdL{#1}{#2}{#3}{\hspace*{6mm}#4}}
\newcommand{\EdLs}[4]{\EdL{#1}{#2}{#3}{\small #4}}
% an abjad number printed with a line above it; the sign printed for zero (drawn with the letter it resembles)
\newcommand{\Ov}[1]{\leavevmode\vbox{\hrule height .4pt\kern 1.0pt\hbox{\RL{#1}}}}
\newcommand{\ZeroSign}{ح}
\newcommand{\AppL}[2]{\par\noindent\hypertarget{#1}{}\parbox[t]{\linewidth}{\setRTL\ArApp\raggedleft #2\par}\par}
\begin{document}
"""


def front():
    return "\n".join([
        r"\thispagestyle{empty}",
        r"\begin{center}\Large AL-BATTĀNĪ\par\vspace{4mm}\LARGE The book on the indications of the conjunctions"
        r" and the eclipses\par\vspace{2mm}\large(his astrological history)\par\vspace{4mm}"
        r"\large\RL{\ArBody كتاب في دلائل القرانات والكسوفات}\par\vspace{5mm}"
        r"\normalsize Ankara, Dil ve Tarih-Coğrafya Fakültesi, collection Saib, 199/2, ff.\,27v–42v\par\vspace{4mm}"
        r"The Arabic text as edited by George Saliba, in E.\,S. Kennedy, B. van Dalen, G. Saliba and J. Samsó,\\"
        r"«Al-Battānī’s Astrological History of the Prophet and the Early Caliphate», \textit{Suhayl} 9 "
        r"(2009–2010), pp.\,13–148: the Arabic title on p.\,17 and the Arabic text on pp.\,18–78\par"
        r"\vspace{4mm}\large S15 --- the Arabic text, line by line\end{center}\vspace{6mm}",
        r"\noindent The edition of the Arabic text is printed in the article as images of George Saliba’s typeset "
        r"edition: its title on p.\,17 and the text on the even pages 18–78. This file transcribes those pages: every "
        r"printed line is one line here, numbered in the right margin as the editors number it, with the folio of "
        r"the manuscript where the edition prints it; the fifteen horoscope charts are transcribed cell by cell and "
        r"drawn again as a square of nine cells, the houses running anticlockwise from the ascendant in the top "
        r"cell; the editors’ apparatus follows each page. The numbers written in letters keep the line that the "
        r"text prints above them; the sign that the edition prints for zero, a small flat-topped \RL{\ArBody ح}, "
        r"is drawn here with the letter \RL{\ArBody ح}. Headings set at the end of a line of text are set there "
        r"in bold. The justification of the print (the long joins of the letters) is "
        r"not transcribed; the tanwīn of the accusative is written on the letter before the final alif (on the "
        r"lām-alif in \RL{\ArBody لاً}) wherever the print sets it; lines printed with a paragraph indent are "
        r"indented here too. The English translation and the commentary of the article are not reproduced. The "
        r"article is licensed CC BY-NC-ND 3.0 ES, and this transcription is distributed under the same licence, "
        r"with the attribution above. The transcription is AI-integrated work (Claude); no person has reviewed it."
        r"\par\clearpage"])


def main():
    pages = sorted((HERE / "pages").glob("AB02-PDF*.txt"))
    tex = [PREAMBLE, front()]
    anchors, app, folios, charts = [], [], [], []
    (HERE / "records").mkdir(exist_ok=True)
    problems = 0
    for p in pages:
        rec = parse(p)
        pid = f"AB02-PDF{rec['pdf']:04d}"
        if any(ch["after_line"] == 0 for ch in rec["charts"]):
            tex.append(r"\par\needspace{130mm}")   # keep the heading of the page with a chart that opens it
        tex.append(r"\PageHead{" + str(rec["pdf"]) + "}{" + rec["printed"] + "}{" + f"{rec['pdf']:04d}" + "}")
        out_lines = []
        charts_after = {}
        for ch in rec["charts"]:
            charts_after.setdefault(ch["after_line"], []).append(ch)
        for ch in charts_after.get(0, []):
            tex.append(chart_tex(ch))
        for k, ln in enumerate(rec["lines"], 1):
            aid = f"{pid}-L{k:02d}"
            if ln["printed_number"] is not None and ln["printed_number"] != k:
                print(f"{pid}: line {k} carries the printed number {ln['printed_number']}")
                problems += 1
            fol = folio_label(ln["folio"]) if ln["folio"] else ""
            if fol:
                folios.append((fol, ln["folio"], aid))
            macro = {"text": r"\EdL", "centre": r"\EdLc", "heading": r"\EdLh", "indent": r"\EdLp",
                     "small": r"\EdLs"}[ln["kind"]]
            tex.append(macro + "{" + str(k) + "}{" + aid + "}{" + (r"\RL{\ArBody " + esc(ln["folio"]) + "}" if fol else "")
                       + "}{" + artex(ln["text"]) + "}")
            anchors.append((aid, rec["printed"], str(k), fol, ln["kind"], ln["text"]))
            out_lines.append({"id": aid, "n": k, "kind": ln["kind"], "text": ln["text"], "folio": fol or None,
                              "printed_number": ln["printed_number"]})
            for ch in charts_after.get(k, []):
                tex.append(chart_tex(ch))
        for ch in rec["charts"]:
            for cell in ch["cells"]:
                charts.append((f"{pid}-{ch['id']}", ch["id"], f"{pid}-L{ch['after_line']:02d}" if ch["after_line"] else pid,
                               cell["pos"], " | ".join(cell["lines"])))
        if rec["app"]:
            tex.append(r"\par\smallskip\noindent\rule{40mm}{0.4pt}\par")
            for j, a in enumerate(rec["app"], 1):
                aid = f"{pid}-A{j:02d}"
                tex.append(r"\AppL{" + aid + "}{" + artex(a) + "}")
                app.append((aid, rec["printed"], a))
        out = {"anchor": pid, "pdf_page": rec["pdf"], "printed_page": rec["printed"],
               "source": "Suhayl 9 (2009-2010), the edition of the Arabic text by George Saliba (page image)",
               "role": "AB_SMALL_WORK (text and charts); MODERN_EDITORIAL (apparatus, line numbers, brackets)",
               "comment": " ".join(rec["comment"]), "lines": out_lines,
               "charts": rec["charts"], "apparatus": [{"id": f"{pid}-A{j:02d}", "text": a} for j, a in enumerate(rec["app"], 1)],
               "observations": rec["obs"]}
        (HERE / "records" / f"{pid}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                                                     encoding="utf-8", newline="\n")
    tex.append(r"\end{document}")
    (HERE / "historia.tex").write_text("\n".join(tex) + "\n", encoding="utf-8", newline="\n")

    def tsv(name, head, rows):
        with open(HERE / name, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\t".join(head) + "\n")
            for r in rows:
                fh.write("\t".join(str(x) for x in r) + "\n")
    tsv("anchors.tsv", ["anchor", "printed_page", "line", "folio", "kind", "text"], anchors)
    tsv("apparatus.tsv", ["anchor", "printed_page", "text"], app)
    tsv("folios.tsv", ["folio", "printed", "anchor"], folios)
    tsv("charts.tsv", ["chart", "id", "after", "cell", "text"], charts)
    print(f"{len(pages)} pages, {len(anchors)} lines, {len(app)} apparatus lines, {len(folios)} folios, "
          f"{len({c[0] for c in charts})} charts; {problems} problems")


if __name__ == "__main__":
    main()

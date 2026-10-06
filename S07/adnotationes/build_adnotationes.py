"""Build the line-anchored diplomatic edition of Nallino's Adnotationes to the tables of Part II (printed pp. 189-317,
master PDF pages 638-766) from the page transcriptions in pages/ (one file per printed page, AB01-PDF####.txt).

Output, beside this script: p2_adnotationes.tex (XeLaTeX; the layout, macros and line anchors of the S02 edition of
Part I), records/AB01-PDF####.json (page records in the S02 schema) and anchors.tsv (one row per printed line).

Transcription format (UTF-8; one printed line per source line, as printed, with its hyphens and its line breaks):
  @page PDF PRINTED      the first line of the file
  @title TEXT            a large centred line (the head ADNOTATIONES)
  @center TEXT           a centred line (the head of each note, «Ad pag. ...»)
  @vspace MM             vertical space
  @rule / @rule2         a short centred rule / the double rule across the text
  @blank                 the page is blank
  @verse H1 | H2         an Arabic verse, its two hemistichs in reading order (the first is set on the right)
  @raw ... @endraw       a LaTeX block passed through (tables, displayed formulas)
  @notes                 the footnotes follow, left column; @col switches to the right column; @notes1 one column
  @sig TEXT              the signature at the foot of the page
  @obs TEXT              an observation on the print (a letter that did not print, a broken sign), kept in the record
  ^ TEXT                 a line that begins a paragraph or a footnote (indented)
  % TEXT                 a comment, not printed
Inline markup: *italic*, **bold**, {sp:Name} letter-spaced, {sc:...} small capitals, {sup:...} superscript,
{sfrac:a/b} a small fraction, {0} the zero sign of the tables, {ar:...} an Arabic phrase with its own brackets and
punctuation, set as one right-to-left run, \\* a literal asterisk; runs of Arabic, Greek, Hebrew
and Syriac letters are set in their fonts. & % # are escaped; $...$ is mathematics; every other character is literal."""
import csv, json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
_AL = r"\u0600-\u065F\u066A-\u06EF\u06FA-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF"
ARABIC_RUN = re.compile(r"([" + _AL + r"]+(?:[ \u060C][" + _AL + r"]+)*)")
_GR = r"\u0370-\u03FF\u1F00-\u1FFF"
GREEK_RUN = re.compile(r"([" + _GR + r"](?:[" + _GR + r"\u0300-\u036F’ ,·]*[" + _GR + r"])?)")
HEBREW_RUN = re.compile("([ְ-ׇא-תװ-״]+(?: [ְ-ׇא-תװ-״]+)*)")
SYRIAC_RUN = re.compile("([܀-ݏ]+(?: [܀-ݏ]+)*)")
ETHIOPIC_RUN = re.compile("([ሀ-፿]+(?: [ሀ-፿]+)*)")

PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[paperwidth=220mm,paperheight=320mm,left=16mm,right=16mm,top=18mm,bottom=18mm,headheight=16pt,headsep=10pt,footskip=14pt]{geometry}
\usepackage{fix-cm}
\usepackage{fontspec,amsmath,amssymb,graphicx,array,multirow}
\usepackage[unicode,hidelinks]{hyperref}
\usepackage{polyglossia}
\setmainlanguage{latin}
\setotherlanguages{arabic,greek,hebrew,syriac}
\setmainfont{Linux Libertine O}[Ligatures=TeX]
\newfontfamily\greekfont{FreeSerif}[Script=Greek]
\newfontfamily\arabicfont{Amiri}[Script=Arabic]
\newfontfamily\hebrewfont{Frank Ruhl Hofshi}[Script=Hebrew]
\newfontfamily\syriacfont{Segoe UI Historic}[Script=Syriac]
\newfontfamily\CapFont{Noto Serif}
\newfontfamily\EthiopicFont{Ebrima}
\newcommand{\textethiopic}[1]{{\EthiopicFont #1}}
\newfontfamily\NallinoSigns{NallinoSigns.otf}[Path=./fonts/]
\newcommand{\AbjadZero}{{\NallinoSigns\symbol{"E000}}}
\hypersetup{pdftitle={Al-Battani, Opus astronomicum. Nallino, Adnotationes ad tabulas (Pars II, pp. 189-317). S07},pdfauthor={Al-Battani; Carlo Alfonso Nallino (notes)}}
\makeatletter
\def\ps@sourceedition{%
\def\@oddhead{\vbox{\hbox to\textwidth{\fontsize{8}{10}\selectfont C. A. NALLINO — ADNOTATIONES AD TABULAS\hfil\leftmark}\vskip3pt\hrule height.25pt}}%
\let\@evenhead\@oddhead
\def\@oddfoot{\hbox to\textwidth{\fontsize{7}{9}\selectfont\rightmark\hfil\thepage}}%
\let\@evenfoot\@oddfoot}
\makeatother
\pagestyle{sourceedition}
\setlength{\parindent}{0pt}\setlength{\parskip}{0pt}
\newcommand{\BeginSource}[2]{\clearpage\markboth{PAG. #2}{#1}\hypertarget{#1}{}\pdfbookmark[0]{#1 — p. #2}{bk-#1}\fontsize{11.1}{13.8}\selectfont}
\tracinglostchars=2
\newcommand{\Name}[1]{{\addfontfeatures{LetterSpace=4.0}#1}}
\newcommand{\Indent}{\hspace*{1.6em}}
\newcommand{\qfrac}[2]{{}^{#1}\!/_{{#2}}}
\newcommand{\sa}{\textsuperscript{\textit{a}}}\newcommand{\sm}{\textsuperscript{\textit{m}}}\newcommand{\sd}{\textsuperscript{\textit{d}}}
\newcommand{\RawBlock}[1]{\par\vspace{3pt}\noindent#1\par\vspace{3pt}}
\newcommand{\CenterLine}[1]{\makebox[\linewidth][c]{#1}}
\newlength{\FullSourceWidth}\newlength{\GutterOffset}\newif\ifNumbersLeft
\newcommand{\DSource}[2]{\BeginSource{AB01-PDF#1}{#2}%
 \setlength{\FullSourceWidth}{\textwidth}\setlength{\GutterOffset}{0pt}%
 \ifodd#2\relax\NumbersLefttrue\else\NumbersLeftfalse\fi}
\newsavebox{\DLBox}
\newcommand{\DLine}[3]{%
 \par\noindent\hypertarget{#1}{}%
 \ifx\relax#2\relax\else
   \ifNumbersLeft
    \rlap{\kern-\GutterOffset\llap{\fontsize{7}{8}\selectfont #2\hspace{3mm}}}%
   \else
    \rlap{\kern\dimexpr\FullSourceWidth-\GutterOffset\relax\hspace{3mm}{\fontsize{7}{8}\selectfont #2}}%
   \fi
 \fi
 \sbox{\DLBox}{\strut #3}%
 \ifdim\wd\DLBox>\linewidth\typeout{DIPLOMATICWIDTH|#1|\the\wd\DLBox|\the\linewidth}\fi
 \usebox{\DLBox}\strut\par}
"""
NOTICE = r"""\thispagestyle{empty}
\begin{center}\Large AL-BATTĀNĪ\par\vspace{4mm}\LARGE OPUS ASTRONOMICUM\par
\vspace{5mm}\large Caroli Alphonsi Nallino adnotationes ad tabulas (pars II)\par\vspace{8mm}
\Large S07 --- editio diplomatica in progressu\par\vspace{4mm}\large Paginae impressae 189--LASTPAGE\end{center}
\vspace{12mm}\noindent Singulae lineae paginarum impressarum singulis lineis huius editionis respondent, cum
divisionibus vocabulorum, signis et generibus litterarum (rectis, inclinatis, distantibus). Textus ex imaginibus
paginarum transcriptus est; litterae Graecae et Arabicae, numeri et signa in imaginibus amplificatis lecta sunt.
Haec transcriptio a nullo homine recognita est.\par
"""


def markup(s):
    keep = []

    def stash(m):  # {ar:...}: an Arabic phrase with its own punctuation and brackets, set as one right-to-left run
        keep.append(r"\textarabic{" + m.group(1) + "}")
        return f"\uE003{len(keep) - 1}\uE004"

    s = re.sub(r"\{ar:([^}]*)\}", stash, s)
    s = s.replace("\\*", "\uE002").replace("&", r"\&").replace("%", r"\%").replace("#", r"\#")
    s = re.sub(r"\{sp:([^}]*)\}", r"\\Name{\1}", s)
    s = re.sub(r"\{sc:([^}]*)\}", r"\\textsc{\1}", s)
    s = re.sub(r"\{sup:([^}]*)\}", r"\\textsuperscript{\1}", s)
    s = re.sub(r"\{sfrac:([^/}]+)/([^}]+)\}", r"$\\qfrac{\1}{\2}$", s)
    s = s.replace("{0}", "\uE001")
    s = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"\*([^*]+)\*", r"\\textit{\1}", s)
    s = ARABIC_RUN.sub(lambda m: r"\textarabic{" + m.group(1) + "}", s)
    s = GREEK_RUN.sub(lambda m: r"\textgreek{" + m.group(1) + "}", s)
    s = HEBREW_RUN.sub(lambda m: r"\texthebrew{" + m.group(1) + "}", s)
    s = SYRIAC_RUN.sub(lambda m: r"\textsyriac{" + m.group(1) + "}", s)
    s = ETHIOPIC_RUN.sub(lambda m: r"\textethiopic{" + m.group(1) + "}", s)
    s = s.replace("⸿", r"{\CapFont ⸿}")  # the capitulum of the Spanish quotations
    s = s.replace("\uE001", r"\AbjadZero{}").replace("\uE002", "*")
    return re.sub("\uE003(\\d+)\uE004", lambda m: keep[int(m.group(1))], s)


def parse(path):
    lines = path.read_text(encoding="utf-8").split("\n")
    m = re.match(r"@page (\d+) (\d+)", lines[0])
    rec = {"pdf": int(m.group(1)), "pp": int(m.group(2)), "body": [], "notes_left": [], "notes_right": [],
           "notes": [], "sig": "", "blank": False, "obs": []}
    part, raw = "body", None
    for ln in lines[1:]:
        if raw is not None:
            if ln.strip() == "@endraw":
                rec[part].append(("raw", "\n".join(raw)))
                raw = None
            else:
                raw.append(ln)
            continue
        if not ln.strip() or ln.startswith("% ") or ln == "%":
            continue
        if ln.startswith("@"):
            cmd, _, arg = ln.partition(" ")
            if cmd == "@raw":
                raw = []
            elif cmd in ("@notes", "@col", "@notes1"):
                part = {"@notes": "notes_left", "@col": "notes_right", "@notes1": "notes"}[cmd]
            elif cmd == "@sig":
                rec["sig"] = arg
            elif cmd == "@obs":
                rec["obs"].append(arg)
            elif cmd == "@blank":
                rec["blank"] = True
            elif cmd in ("@title", "@center", "@vspace", "@rule", "@rule2", "@verse"):
                rec[part].append((cmd[1:], arg))
            else:
                raise SystemExit(f"{path.name}: unknown directive {cmd}")
            continue
        rec[part].append(("line", ln))
    if raw is not None:
        raise SystemExit(f"{path.name}: @raw without @endraw")
    return rec


def section(items, prefix, role, numbered):
    """the TeX of one section and its line records"""
    out, recs, n, par, tab = [], [], 0, 0, 0
    for kind, text in items:
        if kind in ("line", "center", "title", "verse"):
            n += 1
            lid = f"{prefix}-{role}-L{n:03d}"
            src = text[2:] if kind == "line" and text.startswith("^ ") else text
            if kind == "verse":  # an Arabic verse: first hemistich | second hemistich, the first set on the right
                h1, h2 = [h.strip() for h in src.split("|")]
                tex = (r"\CenterLine{\makebox[56mm][c]{\textarabic{" + h2 + r"}}\hspace{8mm}\makebox[56mm][c]{"
                       r"\textarabic{" + h1 + "}}}")
            else:
                tex = markup(src)
            sem = None
            if kind == "line" and text.startswith("^ "):
                tex = r"\Indent " + tex
                note = re.match(r"\((\d+)\)", src)
                if note and role != "body":
                    sem = f"{prefix}-N{int(note.group(1)):02d}"
                else:
                    par += 1
                    sem = f"{prefix}-P{par:02d}"
            elif kind == "center":
                tex = r"\CenterLine{" + tex + "}"
                sem = f"{prefix}-H{n:02d}"
            elif kind == "title":
                tex = r"\CenterLine{\fontsize{24}{28}\selectfont " + tex + "}"
            if sem:
                out.append(r"\hypertarget{" + sem + "}{}")
            show = str(n) if numbered and n % 5 == 0 else ""
            out.append(r"\DLine{" + lid + "}{" + show + "}{" + tex + "}")
            recs.append({"id": lid, "source_line_no": n if numbered else None, "tex": tex, "transcription": src,
                         "semantic_anchor": sem,
                         "source_role": "NALLINO_ADNOTATIONES" if role == "body" else "NALLINO_APPARATUS"})
        elif kind == "vspace":
            out.append(r"\par\vspace{" + text + "mm}")
        elif kind == "rule":
            out.append(r"\par\noindent\makebox[\linewidth][c]{\rule[.5ex]{18mm}{.4pt}}\par")
        elif kind == "rule2":
            out.append(r"\par\noindent\rule{\linewidth}{1.2pt}\par\vspace{1pt}\noindent\rule{\linewidth}{.4pt}\par")
        elif kind == "raw":
            tab += 1
            tid = f"{prefix}-{role}-T{tab:02d}"
            out.append(r"\hypertarget{" + tid + "}{}" + text)
            recs.append({"id": tid, "source_line_no": None, "tex": text, "transcription": text, "semantic_anchor": None,
                         "source_role": "NALLINO_TABLE"})
    return out, recs


def page(rec):
    prefix = f"AB01-PDF{rec['pdf']:04d}"
    out = [r"\DSource{" + f"{rec['pdf']:04d}" + "}{" + str(rec["pp"]) + "}"]
    sections = []
    if rec["blank"]:
        out.append(r"\null")
    tex, recs = section(rec["body"], prefix, "body", True)
    out += tex
    sections.append({"role": "body", "lines": recs})
    if rec["notes"]:
        out.append(r"\par\vspace{6pt}\hrule height.25pt\vspace{5pt}{\fontsize{9}{11.5}\selectfont")
        tex, recs = section(rec["notes"], prefix, "notes", False)
        out += tex + ["}"]
        sections.append({"role": "notes", "lines": recs})
    elif rec["notes_left"] or rec["notes_right"]:
        out.append(r"\par\vspace{6pt}\hrule height.25pt\vspace{5pt}")
        for k, role in enumerate(("notes_left", "notes_right")):
            out.append((r"\hfill" if k else r"\noindent") + r"\begin{minipage}[t]{.48\textwidth}\vspace{0pt}"
                       r"\fontsize{9}{11.5}\selectfont\setlength{\GutterOffset}{0pt}")
            tex, recs = section(rec[role], prefix, role, False)
            out += tex + [r"\end{minipage}"]
            sections.append({"role": role, "lines": recs})
    if rec["sig"]:
        out.append(r"\par\vspace{5mm}\hfill{\fontsize{8}{10}\selectfont " + markup(rec["sig"]) + r"}\hspace{10mm}")
    record = {"anchor": prefix, "master_pdf_page": rec["pdf"], "printed_page": rec["pp"], "source": "SRC01",
              "status": "LINE_ANCHORED_TRANSCRIPTION", "blank": rec["blank"], "signature": rec["sig"] or None, "observations": rec["obs"],
              "source_authority": "Controlling master page image. Embedded text is not the authority for a reading.",
              "transcription_convention": "Source line breaks, hyphenation, quotation signs and word-level type "
                                          "distinctions retained. L numbers count text-bearing lines.",
              "review_responsibility": "Transcribed by Claude from the page images; Greek, Arabic, numbers and signs "
                                       "read on enlarged images. Not reviewed by a person.",
              "sections": sections}
    return "\n".join(out), record


def document():
    files = sorted((HERE / "pages").glob("AB01-PDF*.txt"))
    recs = [parse(p) for p in files]
    for a, b in zip(recs, recs[1:]):
        if b["pdf"] != a["pdf"] + 1 or b["pp"] != a["pp"] + 1:
            raise SystemExit(f"pages not consecutive: PDF {a['pdf']} p. {a['pp']} then PDF {b['pdf']} p. {b['pp']}")
    for r in recs:
        if r["pdf"] - r["pp"] != 449:
            raise SystemExit(f"PDF {r['pdf']} is not printed p. {r['pdf'] - 449}")
    (HERE / "records").mkdir(exist_ok=True)
    body, rows = [], []
    for r in recs:
        tex, record = page(r)
        body.append(tex)
        (HERE / "records" / f"{record['anchor']}.json").write_text(json.dumps(record, ensure_ascii=False, indent=1),
                                                                    encoding="utf-8", newline="\n")
        for s in record["sections"]:
            for ln in s["lines"]:
                rows.append((ln["id"], r["pp"], s["role"], ln["transcription"]))
    last = recs[-1]["pp"] if recs else 189
    tex = (PREAMBLE + r"\begin{document}" + "\n" + NOTICE.replace("LASTPAGE", str(last)) + "\n".join(body)
           + "\n" + r"\end{document}" + "\n")
    (HERE / "p2_adnotationes.tex").write_text(tex, encoding="utf-8", newline="\n")
    with open(HERE / "anchors.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n", quoting=csv.QUOTE_NONE, escapechar="\\")
        w.writerow(["anchor", "printed_page", "section", "transcription"])
        w.writerows(rows)
    print(f"wrote p2_adnotationes.tex: {len(recs)} pages (pp. {recs[0]['pp']}-{last}), {len(rows)} lines")


if __name__ == "__main__":
    document()

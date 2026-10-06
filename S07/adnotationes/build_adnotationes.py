"""Build the line-anchored diplomatic edition of Nallino's Adnotationes to the tables of Part II (printed pp. 189-317,
master PDF pages 638-766) from the page transcriptions in pages/ (one file per printed page, AB01-PDF####.txt).

Output, beside this script: p2_adnotationes.tex (XeLaTeX; the layout, macros and line anchors of the S02 edition of
Part I), records/AB01-PDF####.json (page records in the S02 schema) and anchors.tsv (one row per printed line).

Transcription format (UTF-8; one printed line per source line, as printed, with its hyphens and its line breaks):
  @page PDF PRINTED      the first line of the file
  @title TEXT            a large centred line (the head ADNOTATIONES)
  @center TEXT           a centred line (the head of each note, «Ad pag. ...»)
  @vspace MM             vertical space
  @rule / @rule2 [MM]    a short centred rule / the double rule across the text (or MM wide, over a table)
  @blank                 the page is blank
  @verse H1 | H2         an Arabic verse, its two hemistichs in reading order (the first is set on the right)
  @calc L | S | A | B | C | T   a line of a worked computation: label, sign, three numbers, tail (fixed columns;
                         a label beginning with > is set flush right); @calcrule the rule under the numbers;
                         @calcset INDENT LABEL SIGN NUM the column widths in mm
  @cols INDENT C ...     the columns of a small table (widths in mm with l, r or c; | a vertical rule);
  @hrow H | C1 | ...     a head row H mm tall in the same columns, cells centred; {rot:A//B} and {rotb:A//B}
                         (bold) set the lines A, B turned through 90 degrees
  @row C1 | C2 | ...     one row of it (~ hangs a unit sign: 159~°; {brace2} a brace over two rows; a cell
                         beginning with > is the indented second line of a name);
                         @rowrule - | | - ... a rule under the columns marked -; || in @cols is a double rule,
                         <|| and ||> the double rules of the edges of a boxed table; a cell beginning with >N is
                         indented N mm, one beginning with _ is set half a line lower; @rule2 cols and @hrule cols
                         are a double and a thin rule across the table;
                         @rowgap MM an empty stretch of the table that carries its rules; @brace under|over A B
                         a horizontal brace across the columns A..B between two rows; @rowsep MM an extra
                         gap after every following @row (0 ends it); @colpad A B the space before and after
                         each rule (mm; default 3 2)
  @hspan C1 | C2 ...     a row whose cells may span columns (TEXT:N spans N columns; the rules between them are
                         left out); @spanbrace MM | C1 | ... a strip MM high under such a row, carrying the rules at
                         the cell boundaries, with a brace under each cell written br:N; @cellrule - | | - ... a thin
                         rule under the columns marked -, in a strip that carries all the rules of the table;
                         @hrule cols PT a rule PT thick across the table; in @spanbrace hr:N (HR:N heavy) is a rule across
                         the span; @hrow cells may span columns too; ! in @cols is a heavy rule
  @at X:T | X:T ...      a line whose pieces begin at X mm from the left edge and keep their height (formulas)
  @pos X:T | X>:T | ...  a line whose pieces stand at X mm from the left edge (> right-aligned, ^ centred, _ half a
                         line lower; ~ hangs a unit sign); @posrule X1 X2 [| X1 X2] rules between two lines;
                         @posbrace under|over X1 X2 [| X1 X2] horizontal braces between two lines
  @small / @normal       the following lines in small type (9 on 12 pt) / in the type of the text;
                         @fontsize PT LEAD any other size
  > TEXT                 a continuation line of a hanging paragraph (indented 2.5 em)
  @mcols W1 W2 ...       columns of short lines side by side (widths as fractions of the text width); @mcnext
                         starts the next column, @mcend closes the block; inside, @chead TEXT is the small bold
                         head of a group and @skip N leaves N lines (N may be 0.5)
  @raw ... @endraw       a LaTeX block passed through (tables, displayed formulas)
  @wrap FRAC FILE [MM] ... @endwrap   a figure redrawn in figures/FILE.tex (indented MM), FRAC of the width on the
                         left, with the
                         printed lines between the two directives set beside it
  @wrapr X FILE ... @endwrap   the same with the figure on the right, from X mm; the lines in a box on the left
  @notes                 the footnotes follow, left column; @col switches to the right column; @notes1 one column
  @sig TEXT              the signature at the foot of the page
  @obs TEXT              an observation on the print (a letter that did not print, a broken sign), kept in the record
  ^ TEXT                 a line that begins a paragraph or a footnote (indented); ^^ TEXT indented twice
  % TEXT                 a comment, not printed
Inline markup: *italic*, **bold**, {gb:...} bold grotesque (the «Pag.» heads), {sp:Name} letter-spaced,
{spsc:...} letter-spaced small capitals, {fs:...} the small type of table heads, {sm:...} a smaller type,
{xs:...} the smallest type (the heads of narrow columns),
{sc:...} small capitals, {sup:...} superscript, {sub:...} subscript,
{sfrac:a/b} a small fraction, {0} the zero sign of the tables, {ar:...} an Arabic phrase with its own brackets and
punctuation, set as one right-to-left run, {rtl:...} a phrase of Arabic numerals and Latin words that the print sets
right to left, given in reading order, \\* a literal asterisk; runs of Arabic, Greek, Hebrew
and Syriac letters are set in their fonts. & % # are escaped; $...$ is mathematics; every other character is literal."""
import csv, json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
_AL = r"\u0600-\u065F\u066A-\u06EF\u06FA-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF"
ARABIC_RUN = re.compile(r"([" + _AL + r"]+(?:[ \u060C][" + _AL + r"]+)*)")
_GR = r"\u0370-\u03FF\u1F00-\u1FFF"
GREEK_RUN = re.compile(r"([" + _GR + r"](?:[" + _GR + r"\u0300-\u036F’ ,·]*[" + _GR + r"])?)")
HEBREW_RUN = re.compile("([\u05B0-\u05C7\u05D0-\u05EA\u05F0-\u05F4]+(?: [\u05B0-\u05C7\u05D0-\u05EA\u05F0-\u05F4]+)*)")
SYRIAC_RUN = re.compile("([\u0700-\u074F]+(?: [\u0700-\u074F]+)*)")
ETHIOPIC_RUN = re.compile("([\u1200-\u137F]+(?: [\u1200-\u137F]+)*)")

PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[paperwidth=220mm,paperheight=320mm,left=16mm,right=16mm,top=18mm,bottom=18mm,headheight=16pt,headsep=10pt,footskip=14pt]{geometry}
\usepackage{fix-cm}
\usepackage{fontspec,amsmath,amssymb,graphicx,array,multirow,tikz}
\usepackage[unicode,hidelinks]{hyperref}
\usepackage{polyglossia}
\setmainlanguage{latin}
\setotherlanguages{arabic,greek,hebrew,syriac}
\setmainfont{Linux Libertine O}[Ligatures=TeX]
\setsansfont{Linux Biolinum O}[Ligatures=TeX]
\newfontfamily\greekfont{FreeSerif}[Script=Greek]
\newfontfamily\arabicfont{Amiri}[Script=Arabic]
\newfontfamily\hebrewfont{Frank Ruhl Hofshi}[Script=Hebrew]
\newfontfamily\syriacfont{Segoe UI Historic}[Script=Syriac]
\newfontfamily\CapFont{Noto Serif}
\newfontfamily\MoonFont{FreeSerif}
\newcommand{\MoonSym}{\text{\MoonFont ☾}}\newcommand{\SunSym}{\text{\MoonFont ⊙}}
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
% an Arabic run inside a Latin line: its descenders do not open the line (the printed lines are evenly spaced)
\newcommand{\ArabicRun}[1]{\smash[b]{\textarabic{#1}}}
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


def rtl_phrase(s):
    """{rtl:...}: a phrase of Arabic numerals and Latin words that the print sets right to left (\u00AB\u0642\u0646\u0637 pro \u0642\u0646\u062F\u00BB =
    159 pro 154), given in reading order and set in visual order; a trailing punctuation mark of a word is set on
    the visual right of the word read after it, as printed"""
    words = s.split()
    punct = [""] * (len(words) + 1)
    for k, w in enumerate(words):
        m = re.match(r"^(.*?)([;,.:]*)$", w)
        words[k] = m.group(1)
        punct[k + 1] += m.group(2)
    vis = []
    for k, w in enumerate(words):
        t = r"\ArabicRun{" + w + "}" if ARABIC_RUN.search(w) else w
        vis.append(t + punct[k])
    return " ".join(reversed(vis)) + punct[len(words)]


def markup(s):
    keep = []

    def stash(m):  # {ar:...}: an Arabic phrase with its own punctuation and brackets, set as one right-to-left run
        keep.append(r"\ArabicRun{" + m.group(1) + "}")
        return f"\uE003{len(keep) - 1}\uE004"

    def stash_rtl(m):
        keep.append(rtl_phrase(m.group(1)))
        return f"\uE003{len(keep) - 1}\uE004"

    s = re.sub(r"\{ar:([^}]*)\}", stash, s)
    s = re.sub(r"\{rtl:([^}]*)\}", stash_rtl, s)
    s = s.replace("\\*", "\uE002").replace("&", r"\&").replace("%", r"\%").replace("#", r"\#")
    s = re.sub(r"\{sp:([^}]*)\}", r"\\Name{\1}", s)
    s = re.sub(r"\{sc:([^}]*)\}", r"\\textsc{\1}", s)
    s = re.sub(r"\{spsc:([^}]*)\}", r"\\Name{\\textsc{\1}}", s)
    s = re.sub(r"\{fs:([^}]*)\}", r"{\\fontsize{7.5}{9}\\selectfont \1}", s)
    s = re.sub(r"\{sm:([^}]*)\}", r"{\\fontsize{9.5}{11}\\selectfont \1}", s)
    s = re.sub(r"\{xs:([^}]*)\}", r"{\\fontsize{6.6}{8}\\selectfont \1}", s)
    s = re.sub(r"\{gb:([^}]*)\}", r"\\textbf{\\textsf{\1}}", s)
    s = re.sub(r"\{sup:([^}]*)\}", r"\\textsuperscript{\1}", s)
    s = re.sub(r"\{sub:([^}]*)\}", r"\\textsubscript{\1}", s)
    s = re.sub(r"\{sfrac:([^/}]+)/([^}]+)\}", r"$\\qfrac{\1}{\2}$", s)
    s = s.replace("{0}", "\uE001")
    s = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"\*([^*]+)\*", r"\\textit{\1}", s)
    s = ARABIC_RUN.sub(lambda m: r"\ArabicRun{" + m.group(1) + "}", s)
    s = GREEK_RUN.sub(lambda m: r"\textgreek{" + m.group(1) + "}", s)
    s = HEBREW_RUN.sub(lambda m: r"\texthebrew{" + m.group(1) + "}", s)
    s = SYRIAC_RUN.sub(lambda m: r"\textsyriac{" + m.group(1) + "}", s)
    s = ETHIOPIC_RUN.sub(lambda m: r"\textethiopic{" + m.group(1) + "}", s)
    s = s.replace("⸿", r"{\CapFont ⸿}")  # the capitulum of the Spanish quotations
    s = s.replace("☾", r"\MoonSym{}").replace("⊙", r"\SunSym{}")
    s = s.replace("\uE001", r"\AbjadZero{}").replace("\uE002", "*")
    s = re.sub("\uE003(\\d+)\uE004", lambda m: keep[int(m.group(1))], s)
    return rotate_heads(s)


def rotate_heads(s):
    """{rot:A//B//C} (and {rotb:...}, bold): the lines A, B, C stacked and turned through 90 degrees, as the heads of
    narrow table columns are printed; the argument may contain braces"""
    out, i = [], 0
    while True:
        m = re.compile(r"\{rot(b?):").search(s, i)
        if not m:
            return "".join(out) + s[i:]
        depth, j = 1, m.end()
        while depth:
            depth += {"{": 1, "}": -1}.get(s[j], 0)
            j += 1
        body = s[m.end():j - 1].replace("//", r"\\")
        bold = r"\bfseries" if m.group(1) else ""
        out.append(s[i:m.start()] + r"\rotatebox{90}{" + bold + r"\shortstack{" + body + "}}")
        i = j


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
            elif cmd in ("@title", "@center", "@vspace", "@rule", "@rule2", "@verse", "@calc", "@calcrule",
                         "@calcset", "@cols", "@row", "@rowrule", "@mcols", "@mcnext", "@mcend", "@chead", "@skip",
                         "@small", "@normal", "@rowgap", "@hrule", "@wrap", "@wrapr", "@endwrap", "@brace", "@pos",
                         "@posrule", "@posbrace", "@hrow", "@at", "@rowsep", "@colpad", "@hspan", "@spanbrace",
                         "@cellrule",
                         "@fontsize"):
                rec[part].append((cmd[1:], arg))
            else:
                raise SystemExit(f"{path.name}: unknown directive {cmd}")
            continue
        rec[part].append(("line", ln))
    if raw is not None:
        raise SystemExit(f"{path.name}: @raw without @endraw")
    return rec


CALC_DEFAULT = {"indent": 30, "label": 74, "sign": 7, "num": 7}  # mm; @calcset INDENT LABEL SIGN NUM, per page
CALC = dict(CALC_DEFAULT)


def calc_cell(c):
    """a number of a worked computation, right-aligned on its last digit; its unit sign hangs to the right"""
    m = re.match(r"^(.*\d)(\D*)$", c)
    if not m:
        return r"\makebox[" + str(CALC["num"]) + "mm][r]{" + markup(c) + "}"
    return r"\makebox[" + str(CALC["num"]) + "mm][r]{" + markup(m.group(1)) + r"}\rlap{" + markup(m.group(2)) + "}"


def calc_tex(src):
    """@calc LABEL | SIGN | A | B | C | TAIL: one line of a worked computation in fixed columns; a label that begins
    with > is set flush right against the sign column"""
    cells = [c.strip() for c in src.split("|")] + [""] * 6
    label, sign, nums, tail = cells[0], cells[1], cells[2:5], cells[5]
    right = label.startswith(">")
    label = label[1:] if right else label
    return (r"\hspace*{" + str(CALC["indent"]) + r"mm}\makebox[" + str(CALC["label"]) + "mm][" + ("r" if right else "l")
            + "]{" + markup(label) + r"}\makebox[" + str(CALC["sign"]) + "mm][c]{" + markup(sign) + "}"
            + "".join(calc_cell(c) for c in nums) + (r"\hspace{2.5mm}" + markup(tail) if tail else ""))


COLS = {"indent": 0, "cols": [], "pad": (3.0, 2.0)}
BRACE2 = r"\smash{\raisebox{-6.9pt}{$\left\{\rule[-10pt]{0pt}{20pt}\right.$}}"  # a brace over this row and the next


def set_cols(spec):
    """@cols INDENT COL ...: the columns of the following @row lines; a column is a width in mm and an alignment
    (12r, 30l, 6c), and | is a vertical rule"""
    toks = spec.split()
    COLS["indent"] = float(toks[0])
    COLS["cols"] = [t if t in SEPS else (float(t[:-1]), t[-1]) for t in toks[1:]]


def row_tex(src):
    """@row C1 | C2 | ...: one printed row of a small table, in the columns of @cols. In a cell, ~ separates the
    number from a unit sign that hangs to its right (159~°); {brace2} is a brace over this row and the next; a cell
    TEXT:N spans N columns (the rules between them are left out) and takes the alignment of the first"""
    out = [r"\hspace*{" + str(COLS["indent"]) + "mm}"]
    for item in span_layout(span_cells(src)):
        if item[0] == "sep":
            out.append(rule_piece(item[1], r"\rule[-\dp\strutbox]{.4pt}{\baselineskip}"))
            continue
        c, w, a = item[1], f"{item[2]:.2f}", item[3]
        ind = re.match(r"^>(\d+(?:\.\d+)?)? ", c)
        pre = ""
        if ind:  # a continuation line within the cell, indented (6 mm, or >N N mm); markup applies to the rest only
            pre = r"\hspace*{" + (ind.group(1) or "6") + "mm}"
            c = c[ind.end():]
        if c.startswith("_ "):  # set half a line lower: a head beside a head of two lines
            out.append(r"\makebox[" + str(w) + "mm][" + a + r"]{\smash{\raisebox{-.5\baselineskip}{" + markup(c[2:])
                       + "}}}")
            continue
        if c == "{brace2}":
            out.append(r"\makebox[" + str(w) + "mm][" + a + "]{" + BRACE2 + "}")
        elif "~" in c:
            main, hang = c.split("~", 1)
            out.append(r"\makebox[" + str(w) + "mm][" + a + "]{" + pre + markup(main) + r"\rlap{" + markup(hang) + "}}")
        else:  # smashed, so that a tall Arabic numeral does not open the line and break the vertical rules
            out.append(r"\makebox[" + str(w) + "mm][" + a + r"]{\smash{" + pre + markup(c) + "}}")
    return "".join(out)


def hrow_tex(src):
    """@hrow H | C1 | C2 ...: a head row H mm tall in the columns of @cols, in the small type of table heads; each
    cell is centred in its column, horizontally and vertically, and the rules run through the whole height"""
    h, _, rest = src.partition("|")
    H = float(h)
    out = [r"\hspace*{" + str(COLS["indent"]) + "mm}"]
    rule = r"\rule[-1mm]{.4pt}{" + f"{H:.2f}" + "mm}"
    for item in span_layout(span_cells(rest)):  # a cell TEXT:N spans N columns, as in @hspan
        if item[0] == "sep":
            out.append(rule_piece(item[1], rule))
            continue
        out.append(r"\raisebox{-1mm}{\parbox[b][" + f"{H:.2f}" + "mm][c]{" + f"{item[2]:.2f}" + r"mm}{\centering"
                   r"\fontsize{7.5}{9}\selectfont " + markup(item[1]) + "}}")
    return "".join(out)


def span_cells(src):
    """the cells of a @hspan or @spanbrace line: TEXT:N spans N columns of @cols (one column when :N is omitted)"""
    cells = []
    for c in src.split("|"):
        c = c.strip()
        m = re.match(r"^(.*?):(\d+)$", c)
        cells.append((m.group(1).strip(), int(m.group(2))) if m else (c, 1))
    n, widths = sum(k for _, k in cells), [c for c in COLS["cols"] if c not in SEPS]
    if n != len(widths):
        raise SystemExit(f"a spanning line covers {n} of {len(widths)} columns: {src}")
    return cells


def sep_width(col):
    """the width in mm of a column separator, its spaces included (as rule_piece sets it)"""
    pt = 25.4 / 72.27
    a, b = COLS["pad"]
    return {"|": a + b + 0.4 * pt, "||": a + b + 2.0 * pt, "<||": b + 2.0 * pt, "||>": a + 2.0 * pt,
            "!": a + b + 1.0 * pt}[col]


def span_layout(cells):
    """the separators at the cell boundaries, ("sep", col), and the cells, ("cell", text, width in mm, alignment of
    the first column), of a line in the current @cols whose cells may span columns; a separator inside a span adds
    its width to the cell"""
    out, ci, rem, acc, align = [], 0, 0, 0.0, "c"
    for col in COLS["cols"]:
        if col in SEPS:
            if rem:
                acc += sep_width(col)
            else:
                out.append(("sep", col))
            continue
        if not rem:
            rem, acc, align = cells[ci][1], 0.0, col[1]
        acc += col[0]
        rem -= 1
        if not rem:
            out.append(("cell", cells[ci][0], acc, align))
            ci += 1
    return out


def hspan_tex(src):
    """@hspan C1 | C2 ...: a row of a small table whose cells may span several columns of @cols (TEXT:N), centred
    in the span; the rules between the spanned columns are left out, the others have the height of the row"""
    out = [r"\hspace*{" + str(COLS["indent"]) + "mm}"]
    for item in span_layout(span_cells(src)):
        if item[0] == "sep":
            out.append(rule_piece(item[1], r"\rule[-\dp\strutbox]{.4pt}{\baselineskip}"))
        else:
            out.append(r"\makebox[" + f"{item[2]:.2f}" + r"mm][c]{\smash{" + markup(item[1]) + "}}")
    return "".join(out)


def spanbrace_tex(src):
    """@spanbrace MM | C1 | C2 ...: a strip MM high under a @hspan row, carrying the rules at the boundaries of its
    cells (TEXT:N as in @hspan); a cell written br:N has a brace across its span that points up to the head"""
    mm, _, rest = src.partition("|")
    mm = float(mm)
    out = [r"\par\nointerlineskip\noindent\hspace*{" + str(COLS["indent"]) + "mm}"]
    for item in span_layout(span_cells(rest)):
        if item[0] == "sep":
            out.append(rule_piece(item[1], r"\rule{.4pt}{" + f"{mm:.2f}" + "mm}"))
        elif item[1] in ("hr", "HR"):  # a thin (hr) or heavy (HR) rule across the span
            a, b = COLS["pad"]
            out.append(r"\makebox[" + f"{item[2]:.2f}" + r"mm][l]{\hspace*{-" + f"{b:.2f}" + r"mm}\rule["
                       + f"{mm / 2:.2f}" + "mm]{" + f"{item[2] + a + b:.2f}" + "mm}{"
                       + (".4pt" if item[1] == "hr" else "1.2pt") + "}}")
        elif item[1] == "br":
            out.append(r"\makebox[" + f"{item[2]:.2f}" + r"mm][c]{\smash{\raisebox{" + f"{mm / 2 - 1.2:.2f}"
                       + r"mm}{$\overbrace{\hspace{" + f"{item[2] - 3:.2f}" + "mm}}$}}}")
        else:
            out.append(r"\hspace{" + f"{item[2]:.2f}" + "mm}")
    return "".join(out) + r"\par\nointerlineskip"


def cellrule_tex(src):
    """@cellrule - | | - ...: a thin rule under each column marked -, in a strip 2.5 pt high that carries the rules
    of all the separators; each rule stops short of the column edges"""
    cells = [c.strip() for c in src.split("|")]
    widths = [c for c in COLS["cols"] if c not in SEPS]
    if len(cells) != len(widths):
        raise SystemExit(f"@cellrule has {len(cells)} cells for {len(widths)} columns: {src}")
    out, k = [r"\par\nointerlineskip\noindent\hspace*{" + str(COLS["indent"]) + "mm}"], 0
    for col in COLS["cols"]:
        if col in SEPS:
            out.append(rule_piece(col, r"\rule{.4pt}{2.5pt}"))
            continue
        w = col[0]
        out.append(r"\makebox[" + str(w) + r"mm][c]{" + (r"\rule[1pt]{" + f"{w + 1.0:.2f}" + "mm}{.3pt}"
                                                       if cells[k] == "-" else "") + "}")
        k += 1
    return "".join(out) + r"\par\nointerlineskip"


def rowrule_tex(src):
    """@rowrule - | - | | ...: a rule under each column of the @cols marked with -, between two rows"""
    cells = [c.strip() for c in src.split("|")]
    widths = [c for c in COLS["cols"] if c not in SEPS]
    if len(cells) != len(widths):
        raise SystemExit(f"@rowrule has {len(cells)} cells for {len(widths)} columns: {src}")
    out, k = [r"\par\nointerlineskip\vspace{1pt}\noindent\hspace*{" + str(COLS["indent"]) + "mm}"], 0
    for col in COLS["cols"]:
        if col in SEPS:
            out.append(r"\phantom{" + rule_piece(col, r"\rule{.4pt}{1pt}") + "}")
            continue
        w = col[0]
        out.append((r"\rule{" if cells[k] == "-" else r"\hspace{") + str(w) + ("mm}{.4pt}" if cells[k] == "-" else "mm}"))
        k += 1
    return "".join(out) + r"\par\nointerlineskip\vspace{2pt}"


SEPS = ("|", "||", "<||", "||>", "!")


def rule_piece(col, rule):
    """the space and rule(s) of a column separator: | a rule, || a double rule, <|| and ||> the double rules of
    the left and the right edge of a boxed table; the space before and after a rule is set by @colpad"""
    a, b = (rf"\hspace{{{x}mm}}" for x in COLS["pad"])
    if col == "|":
        return a + rule + b
    if col == "!":  # a heavy rule, 1 pt
        return a + rule.replace("{.4pt}", "{1pt}", 1) + b
    if col == "<||":
        return rule + r"\hspace{1.2pt}" + rule + b
    if col == "||>":
        return a + rule + r"\hspace{1.2pt}" + rule
    return a + rule + r"\hspace{1.2pt}" + rule + b


def cols_width():
    """the width in mm of a table in the current @cols, separators included"""
    pt = 25.4 / 72.27
    a, b = COLS["pad"]
    pad = {"|": a + b + 0.4 * pt, "||": a + b + 2.0 * pt, "<||": b + 2.0 * pt, "||>": a + 2.0 * pt,
           "!": a + b + 1.0 * pt}
    return sum(pad[c] if c in SEPS else c[0] for c in COLS["cols"])


def rowgap_tex(mm):
    """@rowgap MM: an empty stretch of the table, MM high, that carries its vertical rules (no anchor)"""
    out = [r"\par\nointerlineskip\noindent\hspace*{" + str(COLS["indent"]) + "mm}"]
    for col in COLS["cols"]:
        if col in SEPS:
            out.append(rule_piece(col, r"\rule{.4pt}{" + mm + "mm}"))
        else:
            out.append(r"\hspace{" + str(col[0]) + "mm}")
    return "".join(out) + r"\par\nointerlineskip"


def brace_tex(src):
    """@brace under|over A B: a horizontal brace across the columns A..B of the current @cols, set between two rows
    without opening the line spacing; «under» has its point downward, «over» upward"""
    kind, _, spans = src.partition(" ")
    widths = [c[0] for c in COLS["cols"] if c not in SEPS]
    pieces = []
    for span in spans.split("|"):  # several braces on one strip: under 1 6 | 8 13
        a, b = (int(v) for v in span.split())
        x = COLS["indent"] + sum(widths[:a - 1])
        w = sum(widths[a - 1:b])
        if kind == "under":  # a brace with its point downward, in a strip of 5 pt between the two rows
            br = r"\raisebox{1.5pt}{$\underbrace{\hspace{" + f"{w:.2f}" + "mm}}$}"
        else:
            br = r"\raisebox{-5.5pt}{$\overbrace{\hspace{" + f"{w:.2f}" + "mm}}$}"
        pieces.append(r"\rlap{\hspace*{" + f"{x:.2f}" + r"mm}\smash{" + br + "}}")
    return (r"\par\nointerlineskip\vspace{1pt}\noindent" + "".join(pieces)
            + r"\par\nointerlineskip\vspace{4pt}\prevdepth=\dp\strutbox")


def pos_item(it):
    """one item of a @pos line: X[flags]:TEXT, X in mm from the left edge of the text; flags > right-aligned at X,
    ^ centred at X, _ lowered by half a line (a fraction set between two printed lines); in TEXT, ~ hangs the rest
    to the right of the alignment point (17~° right-aligned on its digits)"""
    m = re.match(r"^(\d+(?:\.\d+)?)([>^_]*):(.*)$", it)
    if not m:
        raise SystemExit(f"@pos item without a position: {it}")
    x, flags, text = float(m.group(1)), m.group(2), m.group(3).strip()
    main, _, hang = text.partition("~")
    if ">" in flags:
        box = r"\llap{" + markup(main) + "}" + (r"\rlap{" + markup(hang) + "}" if hang else "")
    elif "^" in flags:
        box = r"\makebox[0pt][c]{" + markup(text.replace("~", "")) + "}"
    else:
        box = r"\rlap{" + markup(text.replace("~", "")) + "}"
    if "_" in flags:
        box = r"\raisebox{-.55\baselineskip}{" + box + "}"
    return r"\rlap{\hspace*{" + f"{x:.2f}" + r"mm}\smash{" + box + "}}"


def at_tex(src):
    """@at X:TEXT | X:TEXT ...: a line whose pieces begin at X mm from the left edge; unlike @pos the pieces keep
    their height, so that displayed formulas open the line spacing as they do on the print"""
    out = [r"\mbox{}"]
    for it in src.split(" | "):
        m = re.match(r"^(\d+(?:\.\d+)?):(.*)$", it.strip())
        if not m:
            raise SystemExit(f"@at item without a position: {it}")
        out.append(r"\rlap{\hspace*{" + f"{float(m.group(1)):.2f}" + r"mm}" + markup(m.group(2).strip()) + "}")
    return "".join(out)


def pos_tex(src):
    """@pos ITEM | ITEM ...: a line whose pieces are set at given positions (Nallino's worked computations)"""
    return r"\mbox{}" + "".join(pos_item(it.strip()) for it in src.split(" | "))


def posrule_tex(src):
    """@posrule X1 X2 [| X1 X2 ...]: rules from X1 to X2 mm between two lines"""
    pieces = []
    for span in src.split("|"):
        x1, x2 = (float(v) for v in span.split())
        pieces.append(r"\rlap{\hspace*{" + f"{x1:.2f}" + r"mm}\rule{" + f"{x2 - x1:.2f}" + r"mm}{.4pt}}")
    return (r"\par\nointerlineskip\vspace{1pt}\noindent" + "".join(pieces)
            + r"\par\nointerlineskip\vspace{2pt}")


def posbrace_tex(src):
    """@posbrace under|over X1 X2 [| X1 X2 ...]: horizontal braces from X1 to X2 mm between two lines"""
    kind, _, spans = src.partition(" ")
    pieces = []
    for span in spans.split("|"):
        x1, x2 = (float(v) for v in span.split())
        if kind == "under":
            br = r"\raisebox{1.5pt}{$\underbrace{\hspace{" + f"{x2 - x1:.2f}" + "mm}}$}"
        else:
            br = r"\raisebox{-5.5pt}{$\overbrace{\hspace{" + f"{x2 - x1:.2f}" + "mm}}$}"
        pieces.append(r"\rlap{\hspace*{" + f"{x1:.2f}" + r"mm}\smash{" + br + "}}")
    return (r"\par\nointerlineskip\vspace{1pt}\noindent" + "".join(pieces)
            + r"\par\nointerlineskip\vspace{4pt}\prevdepth=\dp\strutbox")


def mc_width(tok):
    """a column of @mcols: W or W/H, in mm when greater than 1, else a fraction of the text width; H is the width
    within which the heads of the column are centred"""
    def unit(x):
        return x + "mm" if float(x) > 1 else x + r"\textwidth"
    w, _, h = tok.partition("/")
    return unit(w), (unit(h) if h else None)


def mc_begin(w):
    return r"\begin{minipage}[t]{" + w + r"}\vspace{0pt}"


def section(items, prefix, role, numbered):
    """the TeX of one section and its line records"""
    out, recs, n, par, tab, fig = [], [], 0, 0, 0, 0
    wrapr = None  # the figure of an open @wrapr block, set after its lines
    mc = None  # the column widths of an open @mcols block, and the column being set
    rowsep = "0"
    for kind, text in items:
        if kind == "cols":
            set_cols(text)
            continue
        if kind == "colpad":  # @colpad A B: the space in mm before and after each column rule (default 3 2)
            COLS["pad"] = tuple(float(x) for x in text.split())
            continue
        if kind == "rowrule":
            out.append(rowrule_tex(text))
            continue
        if kind == "mcols":  # columns of short lines set side by side (the index of the cities); rows stay aligned
            mc = {"w": [mc_width(t) for t in text.split()], "k": 0}
            out.append(r"\par\vspace{2pt}\noindent{\lineskiplimit=-\maxdimen" + mc_begin(mc["w"][0][0]))
            continue
        if kind == "mcnext":
            mc["k"] += 1
            out.append(r"\end{minipage}" + mc_begin(mc["w"][mc["k"]][0]))
            continue
        if kind == "mcend":
            if mc["k"] != len(mc["w"]) - 1:
                raise SystemExit(f"{prefix}: @mcols block with {len(mc['w'])} widths has {mc['k'] + 1} columns")
            out.append(r"\end{minipage}}\par")
            mc = None
            continue
        if kind == "small":
            out.append(r"\par\fontsize{9}{12}\selectfont")
            continue
        if kind == "fontsize":  # @fontsize PT LEAD: the type of the following lines
            pt, lead = text.split()
            out.append(r"\par\fontsize{" + pt + "}{" + lead + r"}\selectfont")
            continue
        if kind == "normal":
            out.append(r"\par\fontsize{11.1}{13.8}\selectfont")
            continue
        if kind == "brace":
            out.append(brace_tex(text))
            continue
        if kind == "posrule":
            out.append(posrule_tex(text))
            continue
        if kind == "posbrace":
            out.append(posbrace_tex(text))
            continue
        if kind == "rowgap":
            out.append(rowgap_tex(text))
            continue
        if kind == "spanbrace":
            out.append(spanbrace_tex(text))
            continue
        if kind == "cellrule":
            out.append(cellrule_tex(text))
            continue
        if kind == "rowsep":  # @rowsep MM: an extra gap carrying the rules after every following @row (0: none)
            rowsep = text.strip()
            continue
        if kind == "skip":
            out.append(r"\par\vspace{" + text + r"\baselineskip}")
            continue
        if kind == "wrap":  # @wrap FRAC FILE: the figure figures/FILE.tex on the left, the following lines beside it
            # the boxes hang from their top: the strut height is taken back, so that the first line keeps its
            # ordinary distance from the line above (not at the head of a section, where no line stands above)
            frac, fname, *ind = text.split()
            frac, gap = float(frac), 0.02
            ind = r"\hspace*{" + ind[0] + "mm}" if ind else ""
            fig += 1
            fid = f"{prefix}-{role}-F{fig:02d}"
            out.append(r"\par" + (r"\vspace{-\ht\strutbox}" if n else "") + r"\noindent\begin{minipage}[t]{" + f"{frac:.3f}" + r"\FullSourceWidth}\vspace{0pt}"
                       + r"\hypertarget{" + fid + r"}{}" + ind + r"\input{figures/" + fname + r"}\end{minipage}\hfill"
                       + r"\begin{minipage}[t]{" + f"{1 - frac - gap:.3f}" + r"\FullSourceWidth}\vspace{0pt}"
                       + r"\setlength{\GutterOffset}{" + f"{frac + gap:.3f}" + r"\FullSourceWidth}")
            recs.append({"id": fid, "source_line_no": None, "tex": r"\input{figures/" + fname + "}",
                         "transcription": f"[figure, redrawn: figures/{fname}.tex]", "semantic_anchor": None,
                         "source_role": "NALLINO_FIGURE"})
            continue
        if kind == "wrapr":  # @wrapr X FILE: the lines in a box on the left, the figure from X mm on the right
            x, fname = text.split()
            fig += 1
            fid = f"{prefix}-{role}-F{fig:02d}"
            wrapr = (float(x), fname, fid)
            out.append(r"\par" + (r"\vspace{-\ht\strutbox}" if n else "") + r"\noindent\begin{minipage}[t]{" + f"{float(x) - 2:.2f}" + r"mm}\vspace{0pt}"
                       + r"\setlength{\GutterOffset}{0pt}")
            recs.append({"id": fid, "source_line_no": None, "tex": r"\input{figures/" + fname + "}",
                         "transcription": f"[figure, redrawn: figures/{fname}.tex]", "semantic_anchor": None,
                         "source_role": "NALLINO_FIGURE"})
            continue
        if kind == "endwrap":
            if wrapr:
                x, fname, fid = wrapr
                out.append(r"\end{minipage}\hspace{2mm}\begin{minipage}[t]{" + f"{188 - x:.2f}" + r"mm}\vspace{0pt}"
                           + r"\hypertarget{" + fid + r"}{}\input{figures/" + fname + r"}\end{minipage}\par")
                wrapr = None
                continue
            out.append(r"\end{minipage}\par")
            continue
        if kind in ("line", "center", "title", "verse", "calc", "row", "chead", "pos", "hrow", "at", "hspan"):
            n += 1
            lid = f"{prefix}-{role}-L{n:03d}"
            src = (text[3:] if kind == "line" and text.startswith("^^ ") else
                   text[2:] if kind == "line" and text.startswith(("^ ", "> ")) else text)
            if kind == "verse":  # an Arabic verse: first hemistich | second hemistich, the first set on the right
                h1, h2 = [h.strip() for h in src.split("|")]
                tex = (r"\CenterLine{\makebox[56mm][c]{\textarabic{" + h2 + r"}}\hspace{8mm}\makebox[56mm][c]{"
                       r"\textarabic{" + h1 + "}}}")
            elif kind == "calc":
                tex = calc_tex(src)
                src = " ".join(c.strip().lstrip(">") for c in src.split("|") if c.strip())
            elif kind == "row":
                tex = row_tex(src)
                src = " | ".join(re.sub(r"^(?:>(?:\d+(?:\.\d+)?)? |_ )", "", t)
                                 for t, _ in span_cells(src)).replace("~", "")
            elif kind == "hrow":
                tex = hrow_tex(src)
                src = " | ".join(t for t, _ in span_cells(src.partition("|")[2]))
            elif kind == "hspan":
                tex = hspan_tex(src)
                src = " | ".join(t for t, _ in span_cells(src) if t)
            elif kind == "at":
                tex = at_tex(src)
                src = " ".join(re.sub(r"^[\d.]+:", "", it.strip()) for it in src.split(" | "))
            elif kind == "pos":
                tex = pos_tex(src)
                src = " ".join(re.sub(r"^[\d.]+[>^_]*:", "", it.strip()).replace("~", "") for it in src.split(" | "))
            else:
                tex = markup(src)
            sem = None
            if kind == "line" and text.startswith("> "):  # a continuation line of a hanging paragraph
                tex = r"\hspace*{2.5em}" + tex
            elif kind == "line" and text.startswith(("^ ", "^^ ")):
                tex = (r"\Indent\Indent " if text.startswith("^^ ") else r"\Indent ") + tex
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
            elif kind == "chead":  # the head of a group in the columns, small bold, centred in its column
                hw = mc["w"][mc["k"]][1] if mc else None
                inner = r"\fontsize{8.5}{10}\selectfont\textbf{" + tex + "}"
                tex = (r"\makebox[" + hw + "][c]{" + inner + "}") if hw else (r"\CenterLine{" + inner + "}")
                sem = f"{prefix}-H{n:02d}"
            if sem and mc is not None:  # inside the columns the anchor goes into the line, not between lines
                tex = r"\hypertarget{" + sem + "}{}" + tex
            elif sem:
                out.append(r"\hypertarget{" + sem + "}{}")
            show = str(n) if numbered and n % 5 == 0 and mc is None else ""
            out.append(r"\DLine{" + lid + "}{" + show + "}{" + tex + "}")
            recs.append({"id": lid, "source_line_no": n if numbered else None, "tex": tex, "transcription": src,
                         "semantic_anchor": sem,
                         "source_role": "NALLINO_ADNOTATIONES" if role == "body" else "NALLINO_APPARATUS"})
            if kind == "row" and float(rowsep) > 0:
                out.append(rowgap_tex(rowsep))
        elif kind == "calcset":
            CALC.update(zip(("indent", "label", "sign", "num"), (float(x) for x in text.split())))
        elif kind == "calcrule":  # the rule under the three number columns of a worked computation
            out.append(r"\par\nointerlineskip\vspace{1pt}\noindent\hspace*{" + str(CALC["indent"] + CALC["label"]
                                                                                  + CALC["sign"])
                       + r"mm}\rule{" + str(3 * CALC["num"] + 1) + r"mm}{.4pt}\par\nointerlineskip\vspace{2pt}")
        elif kind == "vspace":
            out.append(r"\par\vspace{" + text + "mm}")
        elif kind == "rule":
            out.append(r"\par\noindent\makebox[\linewidth][c]{\rule[.5ex]{18mm}{.4pt}}\par")
        elif kind == "rule2":  # the double rule across the text, or across a table (@rule2 MM, @rule2 cols); with
            toks = text.split()  # «join» the next row of the table follows without a gap, so that its rules meet it
            ind = r"\hspace*{" + str(COLS["indent"]) + "mm}" if toks[:1] == ["cols"] else ""
            w = (f"{cols_width():.2f}mm" if toks[:1] == ["cols"] else
                 toks[0] + "mm" if toks else r"\linewidth")
            out.append(r"\par\noindent" + ind + r"\rule{" + w + r"}{1.2pt}\par\nointerlineskip\vspace{1pt}\noindent"
                       + ind + r"\rule{" + w + r"}{.4pt}\par" + (r"\nointerlineskip" if "join" in toks else ""))
        elif kind == "hrule":  # a thin rule across a table (@hrule cols) or MM wide, between its rows; @hrule cols PT
            toks = text.split()  # a rule PT thick
            ind = r"\hspace*{" + str(COLS["indent"]) + "mm}" if toks[0] == "cols" else ""
            w = f"{cols_width():.2f}mm" if toks[0] == "cols" else toks[0] + "mm"
            th = (toks[1] if len(toks) > 1 else ".4") + "pt"
            out.append(r"\par\nointerlineskip\noindent" + ind + r"\rule{" + w + "}{" + th + r"}\par\nointerlineskip")
        elif kind == "raw":
            tab += 1
            tid = f"{prefix}-{role}-T{tab:02d}"
            out.append(r"\hypertarget{" + tid + "}{}" + text)
            recs.append({"id": tid, "source_line_no": None, "tex": text, "transcription": text, "semantic_anchor": None,
                         "source_role": "NALLINO_TABLE"})
    return out, recs


def page(rec):
    CALC.clear()
    CALC.update(CALC_DEFAULT)
    COLS.update({"indent": 0, "cols": [], "pad": (3.0, 2.0)})
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
                       r"\fontsize{9}{11.5}\selectfont\setlength{\GutterOffset}{0pt}\setlength{\FullSourceWidth}{\linewidth}")
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

"""The English translation of C. A. Nallino's Latin apparatus to al-Battani's Zij: check the unit files against the
line-anchored Latin transcriptions and write the TeX.

The Latin is read from the anchors.tsv of the transcriptions (one printed line per row: anchor, printed page, section,
transcription): S03/versio and S04/versio (Part I, pp. 110-327) and S07/adnotationes (the notes on the tables, Part II,
pp. 189-317, whose rows may hold a whole TeX table over several lines, escaped as the csv writer escapes them); and
from the line-anchored transcription of S01 (the front matter of Part I: title, dedication, preface, bibliography,
addenda; pp. VII-LXXX).
units.tsv lists the units in the order of the edition: unit, part, title, and its lines (RANGES, as below; no line is
in two units). Each unit is one file text/<unit>.txt:
  @unit ID
  % ...                       a comment
  @part RANGES                the title of a part of the edition; the English on the next line
  @h RANGES                   a heading
  @c RANGES                   a centred line (the lemmas of the commentary)
  @p RANGES                   a paragraph
  @m RANGES                   display formulas, one per line, in TeX math; a line may begin with [[label]]
  @t [spec=lrr] [size=footnotesize] RANGES   a table: one row per line, cells separated by " | "; a row beginning
                              "! " is a heading; the size (default small) is that of the whole table
  @f KEY RANGES               one of Nallino's footnotes; the block that calls it has [^KEY] where his number stands
  @fig FILE ANCHOR            a redrawn figure of S03, S04 or S07 (figures/FILE.tex) and its anchor in the transcription
                              (AB01-PDF0252-body-F01); a caption may follow
  @grid RANGES                a table set as the Latin edition sets it, by the column machinery of S07
                              (build_adnotationes.py): the lines of its page file in English, the directives written
                              .cols, .colpad, .center, .vspace, .figl, .rowgap, .rowsep, .rule2 (for @cols …) and
                              every other line a row (@row); .figl FILE | TEXT sets the head figure FILE, from
                              figures/ here when it has English labels, TEXT being the English of its labels
  @n TEXT                     a translator's note to the block before it
RANGES is FIRST..LAST, or one anchor, or several of these joined by " + "; or - for a heading that the print gives only
as a running head (PRAEFATIO). An anchor is written in full (AB01-PDF0242-body-L004) or short (0242b004; nl, nr, n,
nf and s for notes_left, notes_right, notes, notes_full and section). Every line
of a unit belongs to one block; a line may also end one block and begin another, where a sentence ends inside it. Every
footnote is called once, and every figure of the unit's pages is set.
Inline: *...* italics, **...** bold, $...$ and \\[...\\] TeX math; Arabic, Greek, Hebrew and Syriac are set in their
fonts; {ar:...} is an Arabic phrase with its own brackets or punctuation, set as one right-to-left run; {img:NAME}
(or {img:NAME:H:D}, H em high and D em below the line) is a glyph that the transcription of S01 keeps as an image of the print.

python build_nallino.py   (writes nallino_en.tex, alignment.tsv and checkpoint.json; fails on any error)"""
import csv
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCES = {"S01": ROOT / "S01", "S03": ROOT / "S03" / "versio", "S04": ROOT / "S04" / "versio",
           "S07": ROOT / "S07" / "adnotationes"}
ESCAPED = {"S07"}   # read with the csv writer's escape character: its rows may hold a whole TeX table
SEC = {"b": "body", "nl": "notes_left", "nr": "notes_right", "n": "notes", "nf": "notes_full", "s": "section"}
csv.field_size_limit(10 ** 8)


def read_tsv(path, escaped=False):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar=chr(92) if escaped else None))


def roman(n):
    out = ""
    for v, s in ((50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while n >= v:
            out, n = out + s, n - v
    return out


def read_s01(d):
    """the line-anchored transcription of S01 (the front matter of Part I, PDF 10-89) as the rows of an anchors.tsv;
    its pages are numbered in roman figures, PDF 16 being p. VII"""
    rows = []
    for line in (d / "transcription" / "S01_NALLINO_SOURCE_v003.txt").read_text(encoding="utf-8").splitlines():
        m = re.match(r"(AB01-PDF(\d{4})-(\w+)-L\d{3})\t(.*)$", line)
        if m:
            pdf = int(m.group(2))
            rows.append({"anchor": m.group(1), "printed_page": roman(pdf - 9) if pdf >= 16 else "",
                         "section": m.group(3), "transcription": m.group(4)})
    return rows


def load_sources():
    rows, where = [], {}
    for name, d in SOURCES.items():
        for r in read_s01(d) if name == "S01" else read_tsv(d / "anchors.tsv", name in ESCAPED):
            where[r["anchor"]] = len(rows)
            rows.append({"anchor": r["anchor"], "page": r["printed_page"], "section": r["section"],
                         "text": r["transcription"], "source": name, "pdf": int(r["anchor"][8:12])})
    return rows, where


def full(a):
    m = re.fullmatch(r"(\d{4})(b|nl|nr|nf|n|s)(\d{3})", a)
    return f"AB01-PDF{m.group(1)}-{SEC[m.group(2)]}-L{m.group(3)}" if m else a


def ranges_of(spec):
    if spec.strip() == "-":   # a heading that is a running head of the print, not one of its lines
        return []
    out = []
    for part in spec.split(" + "):
        a, _, z = part.strip().partition("..")
        out.append((full(a), full(z or a)))
    return out


def parse(path):
    unit, blocks = None, []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.startswith("%"):
            continue
        if raw.startswith("@unit "):
            unit = raw.split()[1]
            continue
        if raw.startswith("@n "):
            blocks[-1]["notes"].append(raw[3:].strip())
            continue
        m = re.match(r"@(part|h|c|p|m|ar|grid) (.+)$", raw)
        if m:
            blocks.append({"kind": m.group(1), "ranges": ranges_of(m.group(2)), "text": [], "notes": []})
            continue
        m = re.match(r"@t (?:spec=(\S+) )?(?:size=(\w+) )?(.+)$", raw)
        if m:
            blocks.append({"kind": "t", "spec": m.group(1), "size": m.group(2), "ranges": ranges_of(m.group(3)), "text": [],
                           "notes": []})
            continue
        m = re.match(r"@f (\S+) (.+)$", raw)
        if m:
            blocks.append({"kind": "f", "key": m.group(1), "ranges": ranges_of(m.group(2)), "text": [], "notes": []})
            continue
        m = re.match(r"@fig (\S+)(?: (.+))?$", raw)
        if m:
            blocks.append({"kind": "fig", "file": m.group(1), "ranges": ranges_of(m.group(2)) if m.group(2) else [],
                           "text": [], "notes": []})
            continue
        if raw.startswith("@"):
            raise SystemExit(f"{path.name}: unknown line {raw[:50]}")
        blocks[-1]["text"].append(raw.rstrip() if blocks[-1]["kind"] in ("m", "t", "grid") else raw.strip())
    return unit, blocks


def figures_of(pdfs):
    """the figures that the page files of these master pages set (not the ornaments)"""
    out = []
    for p in pdfs:
        for d in SOURCES.values():
            f = d / "pages" / f"AB01-PDF{p:04d}.txt"
            if f.exists():
                for line in f.read_text(encoding="utf-8").splitlines():
                    m = re.match(r"@(?:wrap|wrapr) \S+ (\S+)|@figc (\S+)", line)
                    if m:
                        name = m.group(1) or m.group(2)
                        if (d / "figures" / f"{name}.tex").exists() and "-F" in name:
                            out.append(name)
    return out


def check(unit, blocks, rows, where, allowed):
    errors, count, ends = [], {}, {}
    for k, b in enumerate(blocks):
        if b["kind"] not in ("fig", "ar") and not b["text"]:
            errors.append(f"block {k}: no English")
        for a, z in b["ranges"]:
            if a not in where or z not in where:
                errors.append(f"block {k}: unknown anchor {a if a not in where else z}")
                continue
            i, j = where[a], where[z]
            if i > j or any(x not in allowed for x in range(i, j + 1)):
                errors.append(f"block {k}: range {a}..{z} out of order or outside the unit")
                continue
            for x in range(i, j + 1):
                count[x] = count.get(x, 0) + 1
                ends.setdefault(x, []).append("first" if x == i else "last" if x == j else "mid")
    for x, n in count.items():
        if n > 2 or (n == 2 and sorted(ends[x]) != ["first", "last"]):
            errors.append(f"{rows[x]['anchor']} is in {n} blocks")
    missing = [rows[x]["anchor"] for x in sorted(allowed) if x not in count]
    if missing:
        errors.append(f"not translated: {', '.join(missing[:6])}{' …' if len(missing) > 6 else ''} ({len(missing)})")
    keys = [b["key"] for b in blocks if b["kind"] == "f"]
    calls = [c for b in blocks for line in b["text"] for c in re.findall(r"\[\^([^\]]+)\]", line) if c != "n"]
    for k, b in enumerate(blocks):
        if sum(line.count("[^n]") for line in b["text"]) > len(b["notes"]):
            errors.append(f"block {k}: more [^n] marks than notes")
    for key in set(keys) | set(calls):
        if keys.count(key) != 1 or calls.count(key) != 1:
            errors.append(f"footnote {key}: {keys.count(key)} texts, {calls.count(key)} calls")
    pdfs = sorted({rows[x]["pdf"] for x in allowed})
    want, got = figures_of(pdfs), [b["file"] for b in blocks if b["kind"] == "fig"]
    errors += [f"figure {f} is not on the pages of the unit" for f in got if f not in want]
    return [f"{unit}: {e}" for e in errors]


def tex_escape(s):
    return (s.replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%").replace("$", r"\$")
            .replace("#", r"\#").replace("_", r"\_").replace("{", r"\{").replace("}", r"\}").replace("^", r"\^{}")
            .replace("~", r"\textasciitilde{}"))


SUP = {"ᵖ": "p", "ᵃ": "a", "ᵐ": "m", "ᵈ": "d", "ʰ": "h", "ˢ": "s", "ᵗ": "t", "ʳ": "r", "ʸ": "y"}
# Greek and Coptic runs as in the Latin edition: the Coptic letters of the Greek block (ϣ, ϩ …) and combining marks
# belong to the Coptic run, which is set bold, as printed
_GR = f"{chr(0x370)}-{chr(0x3E1)}{chr(0x3F0)}-{chr(0x3FF)}{chr(0x1F00)}-{chr(0x1FFF)}"
_CO = f"{chr(0x2C80)}-{chr(0x2CFF)}{chr(0x3E2)}-{chr(0x3EF)}"
_MARKS = f"{chr(0x300)}-{chr(0x36F)}"
GREEK_RUN = re.compile(rf"([{_GR}](?:[{_GR}{_MARKS}\s’',.]*[{_GR}])?)")
COPTIC_RUN = re.compile(rf"([{_CO}][{_CO}{_MARKS}]*)")


def plain(s):
    keep = []

    def stash(m):  # {ar:...}: an Arabic phrase with its own brackets or punctuation, set as one right-to-left run; a
        # Latin word in it, such as Nallino's (sic), is set left to right
        keep.append(r"\RL{\ArNote " + re.sub(r"[A-Za-z]+", lambda w: r"\LR{" + w.group(0) + "}", tex_escape(m.group(1)))
                    + "}")
        return f"{len(keep) - 1}"
    s = re.sub(r"\{ar:([^{}]*)\}", stash, s)

    def image(m):  # {img:NAME[:H[:D]]}: a glyph that S01 keeps as an image of the print, H em high, D em below the line
        keep.append(r"\raisebox{-" + (m.group(3) or ".25") + r"em}{\includegraphics[height=" + (m.group(2) or "1.05")
                    + "em]{../../S01/source/presentation/" + m.group(1) + ".png}}")
        return f"{len(keep) - 1}"
    s = re.sub(r"\{img:(AB01-PDF\d{4}-[FG]\d{2})(?::([\d.]+))?(?::([\d.]+))?\}", image, s)
    s = plain_runs(s)
    return re.sub("(\\d+)", lambda m: keep[int(m.group(1))], s)


def plain_runs(s):
    s = tex_escape(s).replace(r"\{0\}", r"\AbjadZero{}")  # {0}: Nallino's sign for zero in abjad numbers
    s = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"\*([^*]+)\*", r"\\emph{\1}", s)
    # a stop between Arabic words stays in the run, and so does a zero-width non-joiner (بيره‌جك)
    s = re.sub(r"([؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿][؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿\s«».‌]*[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]|[؀-ۿ])", r"\\RL{\\ArNote \1}", s)
    s = s.replace("\u00a0", "~")  # a no-break space, as between the groups of an abjad number (inside its RL run)
    s = GREEK_RUN.sub(r"{\\greekfont \1}", s)
    s = re.sub(r"([֐-׿][֐-׿\s]*[֐-׿])", r"\\RL{\\hebrewfont \1}", s)
    s = re.sub(r"([܀-ݏ](?:[܀-ݏ\s]*[܀-ݏ])?)", r"\\RL{\\syriacfont \1}", s)
    s = re.sub(f"([{chr(0x1200)}-{chr(0x137F)}]+(?: [{chr(0x1200)}-{chr(0x137F)}]+)*)", r"{\\EthiopicFont \1}", s)
    s = s.replace(chr(0x2E3F), r"{\CapFont " + chr(0x2E3F) + "}")  # the capitulum of the Spanish quotations
    s = COPTIC_RUN.sub(r"{\\CopticFont\\bfseries \1}", s)
    s = re.sub(r"([☉☽☾♈-♓☿♀♂♃♄⊙☊☋])", r"{\\MoonFont\\upshape \1}", s)  # FreeSerif Italic lacks these signs
    s = re.sub("[" + "".join(SUP) + "]", lambda m: r"\textsuperscript{\itshape " + SUP[m.group(0)] + "}", s)
    return s


LABEL = r"\[\[((?:[^\[\]]|\[\^n\])+)\]\]\s*(.*)$"


def display(label, math, notes, tn):
    return (r"\par\noindent\hspace*{1.5em}\makebox[2.6em][l]{" + inline(label, notes, tn) + r"}$\displaystyle "
            + math + r"$\par")


def inline(s, notes=None, tn=None):
    """the English of a block: math passes as TeX; [^KEY] becomes Nallino's footnote, [^n] the next note of the
    translator; a display \\[ [[label]] math \\] is set with its label beside it"""
    out = []
    for part in re.split(r"(\\\[.*?\\\]|\$[^$]+\$|\[\^[^\]]+\])", s):
        if part == "[^n]":
            out.append(r"\footnoteT{" + tn.pop(0) + "}")
        elif part.startswith("[^"):
            out.append(r"\footnote{" + notes[part[2:-1]] + "}")
        elif part.startswith(r"\["):
            m = re.match(LABEL, part[2:-2].strip())
            out.append(display(m.group(1), m.group(2), notes, tn) if m else part)
        elif part.startswith("$"):
            out.append(part)
        else:
            out.append(plain(part))
    return "".join(out)


PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[a4paper,left=28mm,right=32mm,top=25mm,bottom=25mm,marginparwidth=18mm,marginparsep=4mm]{geometry}
\usepackage{fontspec,amsmath,amssymb,xcolor,needspace,longtable,array,booktabs,graphicx,tikz,trimclip}
\usepackage{manyfoot,perpage}
\usetikzlibrary{decorations.pathreplacing}
\usepackage[unicode,hidelinks]{hyperref}
\usepackage{polyglossia}
\setmainlanguage{english}
\setotherlanguages{arabic,greek,hebrew}
\setmainfont{Linux Libertine O}[Ligatures=TeX]
\setlength{\emergencystretch}{1.5em}
\newfontfamily\arabicfont{Amiri}[Script=Arabic]
\newfontfamily\ArNote{Amiri}[Script=Arabic,Scale=1.05]
\newfontfamily\greekfont{FreeSerif}[Script=Greek]
\newfontfamily\hebrewfont{Frank Ruhl Hofshi}[Script=Hebrew]
\newfontfamily\syriacfont{Segoe UI Historic}[Script=Syriac]
\newfontfamily\EthiopicFont{Ebrima}
\newfontfamily\CapFont{Noto Serif}
\newfontfamily\MoonFont{FreeSerif}
\newcommand{\MoonSym}{\text{\MoonFont ☾}}\newcommand{\SunSym}{\text{\MoonFont ⊙}}
\newfontfamily\CopticFont{FreeSerif}
\newfontfamily\NallinoSigns{NallinoSigns.otf}[Path=../../S04/versio/fonts/]
\newcommand{\AbjadZero}{{\NallinoSigns\symbol{"E000}}}
\newcommand{\ARsign}{\mbox{\clipbox{0pt 0pt {.48\width} 0pt}{A}\kern-.10em R}}
\newcommand{\Name}[1]{#1}
% the macros of the Latin edition (S07) that its column machinery uses for the tables set by @grid
\newsavebox{\DLBox}\newlength{\GridWidth}
\newcommand{\DLine}[3]{\par\noindent\sbox{\DLBox}{\strut #3}\usebox{\DLBox}\strut\par}
\newcommand{\CenterLine}[1]{\makebox[\linewidth][c]{#1}}
\newcommand{\qfrac}[2]{{}^{#1}\!/_{{#2}}}
\newcommand{\ArabicRun}[1]{\smash[b]{\textarabic{#1}}}
\DeclareNewFootnote{T}[alph]
\MakePerPage{footnote}\MakePerPage{footnoteT}
\hypersetup{pdftitle={C. A. Nallino, notes on al-Battani's Zij: an English translation},pdfauthor={C. A. Nallino}}
\setlength{\parindent}{0pt}\setlength{\parskip}{0.55em}
\tracinglostchars=2
\newcommand{\Pg}[1]{\marginpar{\footnotesize\color{gray}#1}}
\newcommand{\PartHead}[2]{\clearpage\pdfbookmark[0]{#1}{part-#2}{\centering\LARGE #1\par}\bigskip}
\newcommand{\UnitHead}[2]{\par\setcounter{footnoteT}{0}\needspace{8\baselineskip}\bigskip\pdfbookmark[1]{#1}{unit-#2}\hypertarget{EN-#2}{}%
 {\large\bfseries\interlinepenalty=10000 #1\par}\nobreak\medskip}
\begin{document}
"""


def front(done):
    return "\n".join([
        r"\thispagestyle{empty}",
        r"\begin{center}\Large C. A. NALLINO\par\vspace{4mm}\LARGE Notes on al-Battānī's \emph{Zīj}\par"
        r"\vspace{2mm}\large from \emph{Al-Battānī sive Albatenii Opus astronomicum} (Milan, 1899–1907)\par"
        r"\vspace{5mm}\normalsize translated from the Latin\end{center}\vspace{8mm}",
        r"\noindent Nallino's edition of al-Battānī's \emph{Zīj} gives the Arabic text (Part III, 1899), a Latin "
        r"translation of the canons with a commentary on them (Part I, 1903), and the tables in Latin with notes on "
        r"them, a glossary and indexes (Part II, 1907). The canons themselves are translated into English from the "
        r"Arabic in the English \emph{Zīj} of this edition; this volume translates Nallino's own writing, which is "
        r"in Latin and has not been translated before. It is made from the line-by-line transcription of his Latin "
        r"in this edition (S03, S04 and S07). Every sentence is translated, in Nallino's order; nothing is summarised or "
        r"left out. His Arabic, Greek and Hebrew quotations stand in their scripts, as he prints them, with his "
        r"translations of them in English. Proper names are given in a modern transliteration. In the headings of "
        r"the commentary, «p.» and «l.» are the pages and lines of Nallino's Latin translation (Part I, pp. 1–150); "
        r"«t. III» is the Arabic text, whose pages the English \emph{Zīj} gives in its margin; in the heads of the notes on "
        r"the tables, «p.» is a page of the tables (Part II). Nallino's footnotes "
        r"are numbered; the few notes of the translator are lettered. Nallino's own corrections in the «Addenda et "
        r"emendanda» of Part II are followed and noted. The pages of Nallino's volumes are given in the margin.",
        r"\par\smallskip\noindent " + done + ". It is AI-translated (Claude), 2026; no person has proofread it. "
        r"Nallino's work is in the public domain; the translation is dedicated to the public domain (CC0 1.0).",
        r"\par\clearpage"])


def table_tex(b, notes, tn):
    """cells are split at |; a cell «<N> text» spans N columns, and « // » breaks a line within a cell"""
    def span(c):
        m = re.match(r"<(\d+)>\s*", c)
        return (int(m.group(1)), c[m.end():]) if m else (1, c)

    rows = [re.split(r"\s*\|\s*", r[2:] if r.startswith("! ") else r) for r in b["text"] if r.strip() != "---"]
    n = max(sum(span(c)[0] for c in r) for r in rows)
    spec = b.get("spec") or "l" * n
    size = b.get("size") or "small"
    out, texts, ttexts = [r"\begin{center}" + "\\" + size + r"\begin{tabular}{" + spec + "}"], [], []

    def cell(c):
        parts = []
        for part in re.split(r"(\[\^[^\]]+\])", c):
            if part == "[^n]":
                parts.append(r"\footnotemarkT{}")
                ttexts.append(tn.pop(0))
            elif part.startswith("[^"):
                parts.append(r"\footnotemark{}")  # {} keeps the space after the mark
                texts.append(notes[part[2:-1]])
            else:
                parts.append(inline(part))
        return "".join(parts)

    def lines(c, head):
        parts = [(r"\emph{" + cell(p) + "}") if head and p.strip() else cell(p) for p in c.split(" // ")]
        return parts[0] if len(parts) == 1 else r"\begin{tabular}[b]{@{}c@{}}" + r"\\".join(parts) + r"\end{tabular}"
    for r in b["text"]:
        if r.strip() == "---":
            out.append(r"\midrule")
            continue
        head = r.startswith("! ")
        cells = [span(c) for c in re.split(r"\s*\|\s*", r[2:] if head else r)]
        cells += [(1, "")] * (n - sum(k for k, _ in cells))
        cells = [lines(c, head) if k == 1 else r"\multicolumn{" + str(k) + "}{c}{" + lines(c, head) + "}"
                 for k, c in cells]
        out.append(" & ".join(cells) + r" \\")
    out.append(r"\end{tabular}\end{center}")
    if texts:
        out.append(r"\addtocounter{footnote}{-" + str(len(texts)) + "}" + "".join(
            r"\stepcounter{footnote}\footnotetext{" + t + "}" for t in texts))
    if ttexts:
        out.append(r"\addtocounter{footnoteT}{-" + str(len(ttexts)) + "}" + "".join(
            r"\stepcounter{footnoteT}\footnotetextT{" + t + "}" for t in ttexts))
    return "\n".join(out)


def math_tex(b, notes, tn):
    out = []
    for line in b["text"]:
        m = re.match(LABEL, line.strip())
        out.append(display(m.group(1), m.group(2), notes, tn) if m else r"\[" + line.strip() + r"\]")
    return r"\par\smallskip" + "\n".join(out) + r"\par\smallskip"


def arabic_tex(b, idx, rows):
    """an Arabic quotation that Nallino prints as a block: the English gives it as printed (from the transcription,
    when the block has no lines of its own), right to left"""
    text = " ".join(b["text"]) if b["text"] else " ".join(rows[x]["text"] for x in idx)
    text = re.sub(r"\{ar:([^{}]*)\}", r"\1", text)
    text = re.sub(r"\{sup:\*?([^{}]*)\}", lambda m: "@@" + m.group(0)[5:-1] + "@@", text)
    text = tex_escape(text)
    text = re.sub(r"@@([^@]*)@@", r"\\textsuperscript{\1}", text)
    return r"\par\begin{Arabic}\ArNote " + text + r"\end{Arabic}\par"


S07_BUILD = []


def grid_tex(b, mark, prefix):
    """a @grid table: its lines go to the section builder of S07 as the items of a page, the table in a minipage of
    the type of the Latin edition (11.1 on 13.8 pt), so that its rows meet the rules of the head figure; the minipage
    is as wide as the frame of the table where that is wider than the text (its rows and the strips that carry its
    rules must not be broken), and stands out into the right margin by the difference"""
    if not S07_BUILD:
        spec = importlib.util.spec_from_file_location("build_adnotationes", SOURCES["S07"] / "build_adnotationes.py")
        S07_BUILD.append(importlib.util.module_from_spec(spec))
        spec.loader.exec_module(S07_BUILD[0])
    s7 = S07_BUILD[0]
    s7.COLS.update({"indent": 0, "cols": [], "pad": (3.0, 2.0)})
    items = [(m.group(1), m.group(2)) if (m := re.match(r"\.(\w+)\s?(.*)$", line)) else ("row", line)
             for line in b["text"]]
    pad = next(text for kind, text in items if kind == "colpad")
    s7.COLS["pad"] = tuple(float(x) for x in pad.split())
    s7.set_cols(next(text for kind, text in items if kind == "cols"))
    width = s7.cols_width() + 0.5
    s7.COLS.update({"indent": 0, "cols": [], "pad": (3.0, 2.0)})
    out, _ = s7.section(items, prefix, "grid", False)
    return (r"\par\noindent" + mark + r"\setlength{\GridWidth}{" + f"{width:.2f}" + r"mm}\ifdim\GridWidth<\linewidth"
            r"\setlength{\GridWidth}{\linewidth}\fi\makebox[\linewidth][l]{\begin{minipage}{\GridWidth}"
            r"\setlength{\parskip}{0pt}\fontsize{11.1}{13.8}\selectfont" + "\n" + "\n".join(out)
            + r"\par\end{minipage}}\par")


def fig_tex(b):
    """the figure with English labels from figures/ here, where its labels have words; else the redrawn original"""
    cap = (r"\par{\footnotesize " + inline(" ".join(b["text"])) + "}") if b["text"] else ""
    if (HERE / "figures" / f"{b['file']}.tex").exists():
        return r"\begin{center}\input{figures/" + b["file"] + "}" + cap + r"\end{center}"
    for d in SOURCES.values():
        if (d / "figures" / f"{b['file']}.tex").exists():
            rel = (d / "figures" / f"{b['file']}.tex").relative_to(ROOT).as_posix()
            cap = (r"\par{\footnotesize " + inline(" ".join(b["text"])) + "}") if b["text"] else ""
            return r"\begin{center}\input{../../" + rel + "}" + cap + r"\end{center}"
    raise SystemExit(f"figure {b['file']} not found")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rows, where = load_sources()
    units = read_tsv(HERE / "units.tsv")
    body, align, errors, done, covered, words = [], [], [], [], set(), 0
    owner = {}
    for u in units:
        u["set"] = set()
        for a, z in ranges_of(u["lines"]):
            for x in range(where[a], where[z] + 1):
                if x in owner:
                    errors.append(f"units.tsv: {rows[x]['anchor']} in {owner[x]} and {u['unit']}")
                owner[x] = u["unit"]
                u["set"].add(x)
    last_part, last_page = None, None
    for u in units:
        path = HERE / "text" / f"{u['unit']}.txt"
        if not path.exists():
            continue
        unit, blocks = parse(path)
        if unit != u["unit"]:
            errors.append(f"{path.name}: @unit {unit}")
        errors += check(u["unit"], blocks, rows, where, u["set"])
        if errors:
            continue
        done.append(u)
        notes = {}
        for b in blocks:
            if b["kind"] == "f":
                notes[b["key"]] = inline(" ".join(b["text"])) + "".join(
                    r" [\emph{Translator:} " + inline(x) + "]" for x in b["notes"])
        vol = "II" if u["part"] in ("P2", "T", "G", "I") else "I"
        for k, b in enumerate(blocks):
            idx = [x for a, z in b["ranges"] for x in range(where[a], where[z] + 1)]
            covered.update(idx)
            if b["kind"] == "f":
                continue
            pages = []
            for x in idx:
                if rows[x]["section"] == "body" and rows[x]["page"] not in pages:
                    pages.append(rows[x]["page"])
            mark = "".join(r"\Pg{" + vol + " " + p + "}" for p in pages if p != last_page)
            last_page = pages[-1] if pages else last_page
            text = " ".join(b["text"])
            tn = [inline(x) for x in b["notes"]]
            if b["kind"] in ("part", "h", "c", "p"):
                text = inline(text, notes, tn)
            elif b["kind"] == "m":
                text = math_tex(b, notes, tn)
            tnotes = "".join(r"\footnoteT{" + x + "}" for x in tn)
            if b["kind"] == "part":
                if u["part"] != last_part:
                    body.append(r"\PartHead{" + text + "}{" + u["part"] + "}" + mark)
            elif b["kind"] == "h":
                body.append(r"\UnitHead{" + text + tnotes + "}{" + u["unit"] + "}" + mark)
            elif b["kind"] == "c":
                body.append(r"\par\begin{center}" + mark + text + tnotes + r"\end{center}")
            elif b["kind"] == "p":
                body.append(r"\par " + mark + text + tnotes + r"\par")
            elif b["kind"] == "m":
                body.append(mark + text + tnotes)
            elif b["kind"] == "t":
                body.append(mark + table_tex(b, notes, tn) + "".join(r"\footnoteT{" + x + "}" for x in tn))
            elif b["kind"] == "fig":
                body.append(fig_tex(b) + tnotes)
            elif b["kind"] == "grid":
                body.append(grid_tex(b, mark, f"EN-{u['unit']}-G{k:02d}") + tnotes)
                text = " ".join(x.partition(" | ")[2] if x.startswith(".figl ") else x[8:] if x.startswith(".center ")
                                else "" for x in b["text"])   # the words of a table: its head and its title
            elif b["kind"] == "ar":
                body.append(mark + arabic_tex(b, idx, rows) + tnotes)
            words_of = text if b["kind"] == "grid" else " ".join(b["text"])
            n = len(re.sub(r"\$[^$]*\$|\\\[.*?\\\]", "", words_of).split())
            words += n
            align.append((f"EN-{u['unit']}-B{k:02d}", u["unit"], b["kind"],
                          " + ".join(f"{a}..{z}" for a, z in b["ranges"]), " ".join(pages), n))
        last_part = u["part"]
    set_figs = [b["file"] for u in done for b in parse(HERE / "text" / f"{u['unit']}.txt")[1] if b["kind"] == "fig"]
    wanted = []   # a figure printed on several pages (an ornament) is set once on each of them
    for pdf in sorted({r["pdf"] for r in rows}):
        lines = [x for x, r in enumerate(rows) if r["pdf"] == pdf]
        if lines and all(x in covered for x in lines):
            wanted += figures_of([pdf])
    for f in sorted(set(wanted)):
        if set_figs.count(f) != wanted.count(f):
            errors.append(f"figure {f} is set {set_figs.count(f)} times on {wanted.count(f)} pages that print it")
    if errors:
        for e in errors:
            print("ERROR", e)
        raise SystemExit(1)
    held = []
    for part, name in (("P1", "the front matter of Part I"), ("A", "the commentary of Part I"),
                       ("T", "the notes on the tables of Part II")):
        mine = [u for u in units if u["part"] == part]
        got = [u for u in done if u["part"] == part]
        page_of = {}   # the printed page of each master page (roman in the front matter)
        for x in sorted(x for u in got for x in u["set"]):
            if rows[x]["page"]:
                page_of.setdefault(rows[x]["pdf"], rows[x]["page"])
        first, last = (page_of[min(page_of)], page_of[max(page_of)]) if page_of else ("", "")
        if got:
            held.append(("the whole of " if len(got) == len(mine) else "") + name + f" (pp. {first}–{last})")
    status = "The translation is in progress. This version holds " + ", ".join(held[:-1]) + " and " + held[-1] \
        if len(held) > 1 else "The translation is in progress. This version holds " + "".join(held)
    tex = [PREAMBLE, front(status)] + body + [r"\end{document}"]
    (HERE / "nallino_en.tex").write_text("\n".join(tex) + "\n", encoding="utf-8", newline="\n")
    with open(HERE / "alignment.tsv", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("block\tunit\tkind\tlines\tpages\tenglish_words\n")
        for row in align:
            fh.write("\t".join(str(x) for x in row) + "\n")
    h = hashlib.sha256()
    for u in done:
        f = HERE / "text" / f"{u['unit']}.txt"
        h.update(f.name.encode() + b"\0" + f.read_bytes())
    ck = {"edition": "EN: English translation of Nallino's Latin apparatus to al-Battani's Zij",
          "units_done": [u["unit"] for u in done], "latin_lines_translated": len(covered), "blocks": len(align),
          "english_words": words, "canonical_source_checkpoint_sha256": h.hexdigest(),
          "canonical_source_checkpoint_note": "SHA-256 over the unit files in order: file name, a NUL byte, the bytes"}
    (HERE / "checkpoint.json").write_text(json.dumps(ck, ensure_ascii=False, indent=1) + "\n", encoding="utf-8",
                                          newline="\n")
    print(f"{len(done)} units: {len(covered)} Latin lines, {len(align)} blocks, {words} words")


if __name__ == "__main__":
    main()

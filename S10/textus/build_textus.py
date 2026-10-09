"""Build the line-anchored diplomatic edition of al-Battānī's Arabic text as printed in Nallino's Part III (master PDF
1153 and 1151 down to 1073 for S10: the title, the list of chapters and the text to printed p. 79) from the page
transcriptions in pages/ and the measured page geometry in geometry/.

Every printed line is set at its printed baseline and with its printed right edge (PDF points measured on the scan;
the printed page is centred on the edition page); a line that fills the measure is justified to its printed width,
a short line keeps its natural width; a line wider than its printed width is narrowed to it. Headings and display
lines are centred where printed. Margin items (the codex's folio numbers, Nallino's line numbers) stand where printed.

Output, beside this script: p3_textus.tex (XeLaTeX, twice: the lines are placed with TikZ overlays), records/
AB01-PDF####.json (one per page) and anchors.tsv (one row per printed line).

Page files (UTF-8, pages/AB01-PDF####.txt; one source line per printed line, in reading order, with the vowel signs
as printed):
  @page PDF PRINTED   first line; PRINTED is the page number as printed (Arabic-Indic digits), - if none
  @kind KIND          text (default), title or blank
  TEXT                a line of the text (it takes the next line of geometry/PDF####.json)
  @h1 TEXT            a chapter heading, centred (takes a geometry line)
  @h2 TEXT            the line under a chapter heading, centred (takes a geometry line)
  @c SIZE TEXT        a centred display line set in SIZE pt (takes a geometry line)
  @rule Y LEN         a short centred rule LEN pt long at Y (no geometry line)
  @orn Y              the printed ornament, centred at Y (no geometry line)
  @notes              the footnotes follow, one source line per printed line (Latin with Arabic; they take the
                      geometry's note lines)
  @obs TEXT           an observation on the print, kept in the record
  % TEXT              a comment
Inline markup: {n:N} a note reference (superscript, as printed); {ov:...} overlined letters (abjad numerals);
{num:X} the overlined numeral of a chapter in the list of chapters, set in the margin column on the right;
{mL:TEXT} / {mR:TEXT} a margin item beside this line, on the left / right (the codex's folio, f. 4,v., and
Nallino's line numbers 5, 10, 15, 20), set where the geometry has it; * the asterisk of a new folio of the codex;
{0} the zero sign of the codex (set in fonts/NallinoSigns.otf, as in the other editions of the project).
Long joins (kashida) are not transcribed. In the notes: *italic*, {sc:...} small capitals, {sp:...} letter-spaced; Arabic runs are set in
the Arabic font."""
import json
import re
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAME = "p3_textus"
OUT_W, OUT_H = 623.62, 907.09            # the edition page: 220 x 320 mm, as the other editions of the project
_AL = r"\u0600-\u065F\u066A-\u06EF\u06FA-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF"
ARABIC_RUN = re.compile(r"([" + _AL + r"]+(?:[ \u060C.:،][" + _AL + r"]+)*)")
AR_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
WEST = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")

PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[paperwidth=220mm,paperheight=320mm,left=16mm,right=16mm,top=18mm,bottom=18mm,headheight=16pt,headsep=10pt,footskip=14pt]{geometry}
\usepackage{fontspec,graphicx,tikz}
\usepackage[unicode,hidelinks]{hyperref}
\usepackage{polyglossia}
\setmainlanguage{latin}
\setotherlanguages{arabic}
\setmainfont{Linux Libertine O}[Ligatures=TeX]
\newfontfamily\arabicfont{Amiri}[Script=Arabic]
\newfontfamily\ArBody{Amiri}[Script=Arabic]
\newfontfamily\OrnFont{FreeSerif}
\newfontfamily\NallinoSigns{NallinoSigns.otf}[Path=./fonts/]
\newcommand{\AbjadZero}{{\NallinoSigns\symbol{"E000}}}
\hypersetup{pdftitle={Al-Battani, Kitab az-Zij as-Sabi'. Textus Arabicus (Nallino, Pars III). S10},pdfauthor={Al-Battani; Carlo Alfonso Nallino (ed.)}}
\makeatletter
\def\ps@sourceedition{%
\def\@oddhead{\vbox{\hbox to\textwidth{\fontsize{8}{10}\selectfont AL-BATTĀNĪ — TEXTUS ARABICUS (NALLINO, PARS III)\hfil\leftmark}\vskip3pt\hrule height.25pt}}%
\let\@evenhead\@oddhead
\def\@oddfoot{\hbox to\textwidth{\fontsize{7}{9}\selectfont\rightmark\hfil\thepage}}%
\let\@evenfoot\@oddfoot}
\makeatother
\pagestyle{sourceedition}
\setlength{\parindent}{0pt}\setlength{\parskip}{0pt}
\tracinglostchars=2
\newcommand{\DSource}[2]{\clearpage\markboth{#2}{AB01-PDF#1}\pdfbookmark[0]{AB01-PDF#1 — #2}{bk-#1}\null}
% place #3 with its anchor #1 at (#2) from the top left corner of the page
\newcommand{\At}[3]{\begin{tikzpicture}[remember picture,overlay]\node[anchor=#1,inner sep=0pt,outer sep=0pt] at ([shift={(#2)}]current page.north west) {#3};\end{tikzpicture}}
\newsavebox{\LBox}
% a right-to-left line #2 justified to the width #1 (\RLJ) or at its natural width (\RLN); narrowed to #1 if wider
\newcommand{\RLJ}[2]{\sbox{\LBox}{\RL{#2}}%
 \ifdim\wd\LBox>#1\relax\typeout{NARROWED|\the\wd\LBox|#1}\resizebox{#1}{\ht\LBox}{\usebox{\LBox}}%
 \else\makebox[#1][s]{\RL{#2}}\fi}
\newcommand{\RLN}[2]{\sbox{\LBox}{\RL{#2}}%
 \ifdim\wd\LBox>#1\relax\typeout{NARROWED|\the\wd\LBox|#1}\resizebox{#1}{\ht\LBox}{\usebox{\LBox}}%
 \else\usebox{\LBox}\fi}
% a letter-spaced name in the notes (R e i n a u d on p. 25: 2.55 pt between the letters at 9.2 pt)
\newcommand{\Name}[1]{{\addfontfeatures{LetterSpace=27}#1}}
\newcommand{\Note}[1]{\textsuperscript{\fontsize{8}{8}\selectfont\addfontfeatures{Numbers=Lining}#1}}
\newcommand{\Ov}[1]{\vbox{\hrule height .4pt\kern 1.0pt\hbox{#1}}}
\newcommand{\ArRun}[1]{\textarabic{#1}}
"""

NOTICE = r"""\thispagestyle{empty}
\begin{center}\Large AL-BATTĀNĪ\par\vspace{4mm}\LARGE KITĀB AZ-ZĪJ AṢ-ṢĀBIʾ\par
\vspace{5mm}\large textus Arabicus a Carolo Alphonso Nallino editus (pars III)\par\vspace{8mm}
\Large S10 --- editio diplomatica\par\vspace{4mm}\large RANGE\end{center}
\vspace{12mm}\noindent Singulae lineae paginarum impressarum singulis lineis huius editionis respondent et ibi
collocantur ubi in pagina impressa stant (lineae quae totam latitudinem implent ad eandem latitudinem
extenduntur). Textus Arabicus cum signis vocalium, ut impressa sunt, ex imaginibus paginarum transcriptus est;
productiones litterarum (kashida) non transcribuntur. Numeri foliorum codicis et numeri linearum Nallini in
marginibus stant ubi impressi sunt. Haec transcriptio a nullo homine recognita est.\par
"""


def tex_escape_latin(s):
    return s.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#").replace("_", r"\_")


def ar_inline(s):
    """markup inside an Arabic line"""
    s = s.replace("{0}", "")         # the zero sign of the codex, also inside {ov:...}
    s = re.sub(r"\{n:([^}]*)\}", lambda m: r"\Note{" + m.group(1) + "}", s)
    s = re.sub(r"\{ov:([^}]*)\}", lambda m: r"\Ov{" + m.group(1) + "}", s)
    return s.replace("%", r"\%").replace("#", r"\#").replace("", r"\AbjadZero{}")


def latin_inline(s):
    """markup of a footnote line (Latin with Arabic runs)"""
    keep = []

    def stash(m):
        keep.append(r"\ArRun{" + m.group(1) + "}")
        return f"\uE003{len(keep) - 1}\uE004"

    s = ARABIC_RUN.sub(stash, s)
    s = tex_escape_latin(s)
    s = re.sub(r"\{sc:([^}]*)\}", r"\\textsc{\1}", s)
    s = re.sub(r"\{sp:([^}]*)\}", r"\\Name{\1}", s)
    s = re.sub(r"\*([^*]+)\*", r"\\textit{\1}", s)
    s = re.sub(r"\{n:([^}]*)\}", lambda m: r"\Note{" + m.group(1) + "}", s)
    return re.sub("\uE003(\\d+)\uE004", lambda m: keep[int(m.group(1))], s)


def strip_markup(s):
    s = s.replace("{0}", "")         # the zero sign stays {0} in the plain text of the records
    s = re.sub(r"\{(?:n|mL|mR|num)(?:@[\d.]+)?:[^}]*\}", "", s)
    s = re.sub(r"\{ov:([^}]*)\}", r"\1", s)
    return re.sub(r"\s+", " ", s).strip().replace("", "{0}")


def parse(path):
    lines = path.read_text(encoding="utf-8").split("\n")
    head = lines[0].split()
    assert head[0] == "@page", path
    page = {"pdf": int(head[1]), "printed": head[2], "kind": "text", "items": [], "notes": [], "obs": []}
    section = "items"
    table = None
    for raw in lines[1:]:
        ln = unicodedata.normalize("NFC", raw.rstrip("\r"))
        if not ln.strip() or ln.startswith("%"):
            continue
        if table is not None:
            if ln.startswith("@endtable"):
                page["items"].append(("table", table["name"], table["rows"]))
                table = None
            elif ln.startswith("@tr "):
                table["rows"].append([c.strip() for c in ln[4:].split("|")])
            else:
                raise SystemExit(f"{path.name}: inside @table only @tr rows and @endtable")
            continue
        if ln.startswith("@sig "):
            page["sig"] = ln[5:].strip()
        elif ln.startswith("@table "):
            table = {"name": ln.split()[1], "rows": []}
        elif ln.startswith("@lab "):
            page["items"].append(("label", ln[5:].strip()))
        elif ln.startswith("@kind "):
            page["kind"] = ln.split()[1]
        elif ln.startswith("@notes"):
            section = "notes"
        elif ln.startswith("@obs "):
            page["obs"].append(ln[5:].strip())
        elif section == "notes":
            page["notes"].append(ln)
        elif ln.startswith("@h1 "):
            page["items"].append(("h1", ln[4:].strip()))
        elif ln.startswith("@h2 "):
            page["items"].append(("h2", ln[4:].strip()))
        elif ln.startswith("@c "):
            size, text = ln[3:].strip().split(" ", 1)
            page["items"].append(("display", text.strip(), float(size)))
        elif ln.startswith("@rule "):
            y, length = ln.split()[1:3]
            page["items"].append(("rule", float(y), float(length)))
        elif ln.startswith("@orn "):
            page["items"].append(("orn", float(ln.split()[1])))
        elif ln.startswith("@"):
            raise SystemExit(f"{path.name}: unknown directive {ln.split()[0]}")
        else:
            page["items"].append(("text", ln.strip()))
    return page


def margin_items(s):
    """(side, text) of every {mL:...} / {mR:...}; an explicit position stays in the text as @X:TEXT"""
    return [(side, (pos + ":" if pos else "") + txt) for side, pos, txt in
            re.findall(r"\{m([LR])(@[\d.]+)?:([^}]*)\}", s)]


def page_tex(page, geo, recs, anchors):
    pdf = page["pdf"]
    printed = page["printed"]
    pw, ph = geo["page"]
    dx, dy = (OUT_W - pw) / 2, (OUT_H - ph) / 2
    bx0, bx1 = geo["block"]
    printed_w = printed.translate(WEST) if printed != "-" else "-"
    out = [r"\DSource{" + f"{pdf}" + "}{" + ("PAG. " + printed_w if printed != "-" else "SINE NUMERO") + "}"]
    rec = {"source_page": f"AB01-PDF{pdf:04}", "printed_page": printed, "kind": page["kind"], "lines": [],
           "notes": [], "observations": page["obs"]}
    glines = geo["lines"]
    gi = 0
    k = 0
    # Nallino's line numbers: the integer margin items 5, 10, 15, 20 give the grid of the page
    grid = []

    def at(anchor, x, y, body):
        return r"\At{" + anchor + "}{" + f"{x + dx:.2f}pt,{-(y + dy):.2f}pt" + "}{" + body + "}"

    def band(side, yb):
        """the margin items on SIDE beside the line with baseline yb"""
        return [m for m in geo.get("margin", []) if m["side"] == side and m["y1"] > yb - 20 and m["y0"] < yb + 5]

    def numeral_x1(yb):
        """the right edge of a chapter numeral beside the line: the bar over it (a thin rule 8-17 pt wide), else the
        innermost item on the right, else the right edge of the block (p. 1, where the numerals stand inside it)"""
        cands = [m for m in band("R", yb) if m["x0"] < bx1 + 30]
        bars = [m for m in cands if m["y1"] - m["y0"] < 1.8 and 8 <= m["x1"] - m["x0"] <= 17]
        if bars:
            return max(m["x1"] for m in bars)
        if cands:
            first = min(cands, key=lambda m: m["x0"])
            return first["x1"]
        return bx1

    def place_margin(text_line, yb, aid):
        """{mL:} / {mR:}: the folio of the codex and Nallino's line numbers, where printed; on the right they stand
        beyond the column of the chapter numerals. {mR@X:} / {mL@X:} give the left / right edge X explicitly."""
        res = []
        has_num = "{num:" in text_line
        for side, txt in margin_items(text_line):
            m_at = re.match(r"@([\d.]+):(.*)", txt)
            xfix = float(m_at.group(1)) if m_at else None
            txt = m_at.group(2) if m_at else txt
            cands = band(side, yb)
            if not cands and txt.strip().isdigit():
                # a line number standing on the grid between a heading and the text (p. 20): the nearest item
                near = [m for m in geo.get("margin", []) if m["side"] == side and abs(m["y1"] - yb) < 30]
                cands = sorted(near, key=lambda m: abs(m["y1"] - yb))[:1]
            if side == "R" and has_num:
                nx = numeral_x1(yb)
                cands = [m for m in cands if m["x0"] > nx + 1]
            # Nallino's line numbers stand on his grid of 27 pt, not always on a printed line (beside a heading):
            # a number is set at its own measured baseline (the foot of its digits)
            ym = yb
            if txt.strip().isdigit() and cands:
                ym = max(m["y1"] for m in cands)
            if side == "L":
                x = xfix or (max(m["x1"] for m in cands) if cands else bx0 - 10)
                res.append(at("base east", x, ym, r"{\fontsize{8}{9}\selectfont " + tex_escape_latin(txt) + "}"))
            else:
                x = xfix or (min(m["x0"] for m in cands) if cands else bx1 + 10)
                res.append(at("base west", x, ym, r"{\fontsize{8}{9}\selectfont " + tex_escape_latin(txt) + "}"))
            if txt.strip().isdigit():
                grid.append((int(txt.strip()), ym))
        return res

    tables = geo.get("tables", [])
    labels = geo.get("labels", [])
    ti = li = 0

    def tikz_lines(segs, width):
        """straight rules in page coordinates (PDF points of the scan)"""
        draw = "".join(r"\draw[line width=" + f"{width:.2f}pt" + "] ([shift={(" + f"{x0 + dx:.2f}pt,{-(y0 + dy):.2f}pt" +
                       ")}]current page.north west) -- ([shift={(" + f"{x1 + dx:.2f}pt,{-(y1 + dy):.2f}pt" +
                       ")}]current page.north west);" for x0, y0, x1, y1 in segs)
        return r"\begin{tikzpicture}[remember picture,overlay]" + draw + r"\end{tikzpicture}"

    for item in page["items"]:
        kind = item[0]
        if kind == "table":
            # a ruled table: the rules where printed (geometry "tables"), every cell's words at the centre of its
            # printed ink (or of the cell), horizontal (a cell written =TEXT) or turned through the table's angle
            _, name, rows = item
            tg = tables[ti]
            ti += 1
            xr, yr = tg["x"], tg["y"]
            fw, rw, gap = tg.get("frame", 0.9), tg.get("rule", 0.4), tg.get("gap", 0.0)
            gt, gb = (gap, gap) if not isinstance(gap, list) else gap   # the inner rules stop short of the rows
            segs_frame = [(xr[0], yr[0], xr[-1], yr[0]), (xr[0], yr[-1], xr[-1], yr[-1]),
                          (xr[0], yr[0], xr[0], yr[-1]), (xr[-1], yr[0], xr[-1], yr[-1])]
            segs = [(xr[0], y, xr[-1], y) for y in yr[1:-1]]
            for x in xr[1:-1]:
                for ya, yb_ in zip(yr[:-1], yr[1:]):
                    segs.append((x, ya + gt, x, yb_ - gb))
            out.append(tikz_lines(segs_frame, fw))
            out.append(tikz_lines(segs, rw))
            centres = {(c["r"], c["c"]): c for c in tg.get("cells", [])}
            size = tg.get("size", 11.0)
            rot = tg.get("rot", 45.0)
            ncol = len(xr) - 1
            trec = {"name": name, "anchor": f"AB01-PDF{pdf:04}-{name}", "rows": rows, "rot": rot}
            for r, row in enumerate(rows, 1):
                if len(row) != ncol:
                    raise SystemExit(f"AB01-PDF{pdf:04} {name}: row {r} has {len(row)} cells, the grid {ncol}")
                for c, cell in enumerate(row, 1):
                    if not cell:
                        continue
                    ci = ncol - c                        # columns are counted from the right
                    cm = centres.get((r, c))
                    cx = cm["cx"] if cm else (xr[ci] + xr[ci + 1]) / 2
                    cy = cm["cy"] if cm else (yr[r - 1] + yr[r]) / 2
                    horiz = cell.startswith("=")
                    body = ar_inline(cell.lstrip("="))
                    aid = f"AB01-PDF{pdf:04}-{name}-R{r:02}-C{c:02}"
                    node = (r"\hypertarget{" + aid + r"}{}{\fontsize{" + f"{size}" + "}{" + f"{size * 1.2:.1f}" +
                            r"}\ArBody\RL{" + body + "}}")
                    if horiz:
                        out.append(at("center", cx, cy, node))
                    else:
                        out.append(r"\At{center}{" + f"{cx + dx:.2f}pt,{-(cy + dy):.2f}pt" + r"}{\rotatebox{" +
                                   f"{rot:.0f}" + "}{" + node + "}}")
                    anchors.append((aid, pdf, printed, "cell", strip_markup(cell.lstrip("="))))
            rec.setdefault("tables", []).append(trec)
            continue
        if kind == "label":
            # a letter set beside a table or a figure (the sides of a table), where printed
            lg = labels[li]
            li += 1
            # the bar over a label stands at the same height over every letter (11 pt over the baseline)
            body = ar_inline(item[1]).replace(r"\Ov{", r"\Ov{\rule{0pt}{10.2pt}")
            out.append(at("base", lg["x"], lg["base"], r"{\fontsize{" + f"{lg.get('size', 13.8)}" + r"}{20}\ArBody\RL{" +
                          body + "}}"))
            rec.setdefault("labels", []).append({"text": item[1], "x": lg["x"], "baseline": lg["base"]})
            continue
        if kind == "rule":
            _, y, length = item
            x = (bx0 + bx1) / 2
            out.append(at("center", x, y, r"\rule{" + f"{length:.1f}" + "pt}{0.5pt}"))
            rec["lines"].append({"anchor": None, "kind": "rule", "y": y, "length_pt": length})
            continue
        if kind == "orn":
            _, y = item
            out.append(at("center", (bx0 + bx1) / 2, y, r"{\OrnFont\fontsize{20}{20}\selectfont ❦}"))
            rec["lines"].append({"anchor": None, "kind": "ornament", "y": y})
            continue
        if gi >= len(glines):
            raise SystemExit(f"AB01-PDF{pdf:04}: more lines than the geometry has ({len(glines)})")
        g = glines[gi]
        gi += 1
        k += 1
        aid = f"AB01-PDF{pdf:04}-L{k:02}"
        text = item[1]
        yb, x0, x1 = g["base"], g["x0"], g["x1"]
        body = ar_inline(re.sub(r"\{(?:mL|mR|num)(?:@[\d.]+)?:[^}]*\}", "", text)).strip()
        target = r"\hypertarget{" + aid + "}{}"
        if kind in ("h1", "h2", "display"):
            size = {"h1": 21.0, "h2": 15.5}.get(kind, item[2] if kind == "display" else 14.5)
            xc = (x0 + x1) / 2
            out.append(at("base", xc, yb, target + r"{\fontsize{" + f"{size}" + "}{" + f"{size * 1.2:.1f}" +
                          r"}\ArBody\RL{" + body + "}}"))
        else:
            width = x1 - x0
            macro = r"\RLJ" if x0 <= bx0 + 6 else r"\RLN"
            out.append(at("base east", x1, yb, target + r"{\fontsize{13.8}{27}\ArBody" + macro + "{" +
                          f"{width:.2f}pt" + "}{" + body + "}}"))
        num = re.findall(r"\{num:([^}]*)\}", text)
        for nm in num:
            # the chapter numeral: the innermost item on the right beside the line (its overline included), or the
            # right edge of the block when the numerals stand inside it (p. 1)
            out.append(at("base east", numeral_x1(yb), yb, r"{\fontsize{13.8}{27}\ArBody\Ov{" + nm + "}}"))
        out += place_margin(text, yb, aid)
        plain = strip_markup(text)
        rec["lines"].append({"anchor": aid, "kind": kind, "text": text, "plain": plain, "baseline": yb,
                             "x0": x0, "x1": x1, "margin": [{"side": s, "text": t} for s, t in margin_items(text)],
                             "numeral": num[0] if num else None})
        anchors.append((aid, pdf, printed, kind, plain))
    if gi != len(glines):
        raise SystemExit(f"AB01-PDF{pdf:04}: {len(glines)} geometry lines, {gi} transcribed")
    if ti != len(tables) or li != len(labels):
        raise SystemExit(f"AB01-PDF{pdf:04}: {len(tables)} tables / {len(labels)} labels measured, {ti} / {li} transcribed")
    if page.get("sig"):
        # the printer's signature at the foot of the first page of a sheet, where printed
        s = geo.get("sig")
        if not s:
            raise SystemExit(f"AB01-PDF{pdf:04}: @sig without a measured place (geometry 'sig')")
        out.append(at("base west", s["x0"], s["base"], r"{\fontsize{9}{10}\selectfont\bfseries " +
                      tex_escape_latin(page["sig"]) + "}"))
        rec["signature"] = {"text": page["sig"], "x0": s["x0"], "baseline": s["base"]}
    elif geo.get("sig"):
        raise SystemExit(f"AB01-PDF{pdf:04}: a signature is measured but not transcribed (@sig)")
    # Nallino's line number of every line, from the grid of the printed numbers (27 pt apart)
    if grid:
        for ln in rec["lines"]:
            if ln.get("anchor"):
                n0, y0 = min(grid, key=lambda t: abs(t[1] - ln["baseline"]))
                ln["nallino_line"] = int(round(n0 + (ln["baseline"] - y0) / 27.0))
    if page["notes"]:
        gnotes = geo.get("notes", [])
        if len(gnotes) != len(page["notes"]):
            raise SystemExit(f"AB01-PDF{pdf:04}: {len(gnotes)} note lines measured, {len(page['notes'])} transcribed")
        if geo.get("rule"):
            r = geo["rule"]
            out.append(at("west", r[0], (r[1] + r[3]) / 2, r"\rule{" + f"{r[2] - r[0]:.1f}" + "pt}{0.5pt}"))
        for j, (nt, gn) in enumerate(zip(page["notes"], gnotes), 1):
            aid = f"AB01-PDF{pdf:04}-N{j:02}"
            body = latin_inline(nt.lstrip("<").strip())
            width = gn["x1"] - gn["x0"]
            if nt.startswith("<") or gn["x1"] < bx1 - 8:
                box = body
            else:
                box = r"\makebox[" + f"{width:.2f}pt" + "][s]{" + body + "}"
            out.append(at("base west", gn["x0"], gn["y"], r"\hypertarget{" + aid + r"}{}{\fontsize{9.2}{11}\selectfont " +
                          box + "}"))
            rec["notes"].append({"anchor": aid, "text": nt, "baseline": gn["y"]})
            anchors.append((aid, pdf, printed, "note", nt))
    recs.append(rec)
    return "\n".join(out)


def main():
    pages = sorted((HERE / "pages").glob("AB01-PDF*.txt"), key=lambda p: -int(p.stem[8:]))
    # reading order: the title (PDF 1153), then the printed pages from p. 1 (PDF 1151) down the PDF
    body, recs, anchors = [], [], []
    for p in pages:
        page = parse(p)
        geo = json.load(open(HERE / "geometry" / f"PDF{page['pdf']:04}.json", encoding="utf-8"))
        body.append(page_tex(page, geo, recs, anchors))
    first = recs[0]["printed_page"] if recs else "-"
    printed_nums = [r["printed_page"].translate(WEST) for r in recs if r["printed_page"] != "-"]
    rng = "Titulus; paginae impressae " + (f"{printed_nums[0]}--{printed_nums[-1]}" if printed_nums else "")
    tex = (PREAMBLE + "\\begin{document}\n" + NOTICE.replace("RANGE", rng) + "\n".join(body) + "\n\\end{document}\n")
    (HERE / f"{NAME}.tex").write_text(tex, encoding="utf-8")
    (HERE / "records").mkdir(exist_ok=True)
    for r in recs:
        (HERE / "records" / f"{r['source_page']}.json").write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n",
                                                                    encoding="utf-8")
    with open(HERE / "anchors.tsv", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("anchor\tpdf\tprinted\tkind\ttext\n")
        for a in anchors:
            fh.write("\t".join(str(v) for v in a) + "\n")
    print(f"wrote {NAME}.tex: {len(recs)} pages, {len(anchors)} anchored lines")


if __name__ == "__main__":
    main()

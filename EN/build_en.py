"""The English translation of al-Battani's Zij: check the chapter files against the Arabic and write the TeX.

Chapter files (text/C##.txt), one per chapter (C00 is the invocation and the list of chapters):
  @chapter N
  % ...                       a comment
  @h FIRST..LAST              a heading; the English follows on the next lines
  @s FIRST..LAST | LETTER     the heading of one of the eight short chapters that follow chapter 57 (Nallino's A-H)
  @c FIRST..LAST              a centred line (the invocation)
  @p FIRST..LAST              a paragraph
  @li FIRST..LAST | NUMBER    an item of the list of chapters
  @skip FIRST..LAST | WHY     Arabic lines that are not part of al-Battani's text (Nallino's title page)
  @table FIRST..LAST | TITLE  a table printed in the text: its cells (kind cell); then one line per row, the cells
                              separated by |, in the order of the printed columns from right to left, which the
                              English sets from left to right
  @figure FIRST..LAST         a figure: the labels of a printed figure (kind figure); then one line per label, in the
                              order of the anchors. The figure is redrawn from the geometry measured for the Arabic
                              edition (S10-S12 textus/geometry), with these labels where the Arabic ones stand
  @n TEXT                     a note to the block before it
FIRST..LAST are the anchors of the first and the last Arabic line that the block translates (S10-S12 anchors.tsv).
Two consecutive blocks may share their boundary line, where a sentence ends inside a line; otherwise every line of the
Arabic text of the chapter (kinds display, text, h1, h2, cell, figure) belongs to exactly one block. Nallino's notes
(kind note) and the Latin title lines are not translated. The letters of the figures are transliterated: ا A, ب B,
ج G, د D, ه H, و W, ز Z, ح Ḥ, ط Ṭ, ي Y, ك K, ل L, م M, ن N, س S, ع ʿ, ف F, ص Ṣ,
ق Q, ر R, ش Sh, ت T, ث Th, خ Kh, ذ Dh, ض Ḍ, ظ Ẓ, غ Gh, and لا (lām-alif) LA.
Inline: *...* emphasis; Arabic in «» is set in the Arabic font.

python build_en.py   (writes zij_en.tex, alignment.tsv and checkpoint.json; fails on any coverage error)"""
import hashlib
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "tools"))
import sources  # noqa: E402
sys.path.insert(0, str(HERE))
import build_tables  # noqa: E402

REQUIRED = {"display", "text", "h1", "h2", "cell", "figure"}
TEXTUS = [HERE.parent / s / "textus" for s in ("S10", "S11", "S12")]


def row_class(kind):
    """the kind of block that translates a line of this kind"""
    return {"cell": "table", "figure": "figure"}.get(kind, "text")
WESTERN = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


def parse(path):
    blocks, n = [], None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.startswith("%"):
            continue
        if raw.startswith("@chapter"):
            n = int(raw.split()[1])
            continue
        m = re.match(r"@(h|s|c|p|li|skip|table|figure) (\S+)\.\.(\S+)(?: \| (.*))?$", raw)
        if m:
            blocks.append({"kind": m.group(1), "first": m.group(2), "last": m.group(3), "arg": m.group(4) or "",
                           "text": [], "notes": []})
            continue
        if raw.startswith("@n "):
            blocks[-1]["notes"].append(raw[3:].strip())
            continue
        if raw.startswith("@"):
            raise SystemExit(f"{path.name}: unknown line {raw[:40]}")
        blocks[-1]["text"].append(raw.strip())
    return n, blocks


def check(n, blocks, rows):
    """every required line belongs to one block: table blocks own the cells of their range, figure blocks the labels
    of their figure, the other blocks the other required lines; consecutive text blocks may share their boundary line"""
    idx = {r["anchor"]: i for i, r in enumerate(rows)}
    req = [i for i, r in enumerate(rows) if r["kind"] in REQUIRED]
    owner = {}
    errors = []
    for cls in ("table", "figure", "text"):
        prev_last, prev_k = None, None
        for k, b in enumerate(blocks):
            if b["kind"] in ("table", "figure"):
                if b["kind"] != cls:
                    continue
            elif cls != "text":
                continue
            if b["first"] not in idx or b["last"] not in idx:
                errors.append(f"block {k}: unknown anchor {b['first']} or {b['last']}")
                continue
            a, z = idx[b["first"]], idx[b["last"]]
            if a > z:
                errors.append(f"block {k}: {b['first']} after {b['last']}")
            if prev_last is not None and a < prev_last:
                errors.append(f"block {k}: begins before the end of the block before it")
            if b["kind"] != "skip" and not b["text"]:
                errors.append(f"block {k}: no English")
            for i in range(a, z + 1):
                kind = rows[i]["kind"]
                if kind not in REQUIRED or row_class(kind) != cls:
                    continue
                if i in owner and not (i == a and owner[i] == prev_k and i == prev_last):
                    errors.append(f"block {k}: {rows[i]['anchor']} already in block {owner[i]}")
                owner[i] = k
            if cls == "table":
                cells = [i for i in range(a, z + 1) if rows[i]["kind"] == "cell"]
                ncells = sum(len(r.split("|")) for r in b["text"])
                if ncells != len(cells):
                    errors.append(f"block {k}: {ncells} English cells for {len(cells)} printed cells")
            if cls == "figure":
                labels = [i for i in range(a, z + 1) if rows[i]["kind"] == "figure"]
                if len(b["text"]) != len(labels):
                    errors.append(f"block {k}: {len(b['text'])} English labels for {len(labels)} printed labels")
            prev_last, prev_k = z, k
    missing = [rows[i]["anchor"] for i in req if i not in owner]
    if missing:
        errors.append(f"not translated: {', '.join(missing[:8])}{' …' if len(missing) > 8 else ''} ({len(missing)})")
    return errors


def figure_geometry(anchor):
    """the figure measured for the Arabic edition to which the label anchor AB01-PDF####-F##-T## belongs"""
    m = re.match(r"AB01-PDF(\d{4})-(F\d\d)-T\d\d$", anchor)
    if not m:
        raise SystemExit(f"{anchor}: not the anchor of a figure label")
    for t in TEXTUS:
        path = t / "geometry" / f"PDF{m.group(1)}.json"
        if path.exists():
            for fg in json.loads(path.read_text(encoding="utf-8")).get("figures", []):
                if fg["name"] == m.group(2):
                    return fg
    raise SystemExit(f"{anchor}: no measured figure")


FLOAT_HEIGHT = 450      # points: a figure taller than this, about two thirds of the text height, floats
MAX_WIDTH = 420         # points: a figure wider than this is drawn smaller, to fit the text width (425 pt)


def figure_extent(fg):
    """the box (x0, y0, x1, y1) of the measured figure, in page points with y downwards"""
    xs, ys = [], []
    for c in fg.get("circles", []) + fg.get("arcs", []) + fg.get("discs", []):
        xs += [c["cx"] - c["r"], c["cx"] + c["r"]]
        ys += [c["cy"] - c["r"], c["cy"] + c["r"]]
    for s in fg.get("segments", []):
        xs += [s["x0"], s["x1"]]
        ys += [s["y0"], s["y1"]]
    for q in fg.get("paths", []):
        xs += [x for x, _ in q["pts"]]
        ys += [y for _, y in q["pts"]]
    for t in fg["texts"]:
        xs.append(t["x"])
        ys.append(t["y"])
    return min(xs), min(ys), max(xs), max(ys)


def figure_height(fg):
    _, y0, _, y1 = figure_extent(fg)
    return y1 - y0


def figure_tex(fg, labels):
    """the figure redrawn from its measured geometry (page points, y downwards) at its printed size: hatched half
    discs, circles, arcs, straight lines, traced curves and dots with their stroke widths, and the English labels at
    the centres of the Arabic ones, turned where these are turned; a label that stands in a hatched half disc is set on
    white. A figure wider than the text is drawn smaller as a whole; its strokes and labels keep their sizes"""
    x0, _, x1, y1 = figure_extent(fg)
    scale = min(1.0, MAX_WIDTH / (x1 - x0))

    def pt(x, y):
        return f"({x - x0:.2f}pt,{y1 - y:.2f}pt)"

    def style(e):
        d = f", dash pattern=on {e['dash'][0]:.2f}pt off {e['dash'][1]:.2f}pt" if e.get("dash") else ""
        return "[line width=" + f"{e['w']:.2f}pt" + d + "]"

    # a hatched half disc ("hatches"): the part of the circle cx, cy, r on the side "into" (a unit vector) of the chord
    # x0, y0 - x1, y1, filled with parallel lines "w" thick at "angle" degrees (counter-clockwise, the line of the text
    # at 0), "pitch" apart, one of them "phase" from the centre of the circle along their normal (as the Arabic edition
    # draws it, S11 build_textus.py)
    def hatch(h):
        t = math.radians(h["angle"])
        ux, uy, nx, ny = math.cos(t), -math.sin(t), math.sin(t), math.cos(t)
        ex, ey = h["x1"] - h["x0"], h["y1"] - h["y0"]
        el = math.hypot(ex, ey)
        ex, ey = ex / el * h["r"] * 0.4, ey / el * h["r"] * 0.4
        ix, iy = h["into"][0] * h["r"] * 2.3, h["into"][1] * h["r"] * 2.3
        ax, ay, bx, by = h["x0"] - ex, h["y0"] - ey, h["x1"] + ex, h["y1"] + ey
        body = (r"\clip " + pt(h["cx"], h["cy"]) + f" circle[radius={h['r']:.2f}pt];" + r"\clip " + pt(ax, ay) +
                " -- " + pt(bx, by) + " -- " + pt(bx + ix, by + iy) + " -- " + pt(ax + ix, ay + iy) + " -- cycle;")
        j0, j1 = math.ceil((-h["r"] - h["phase"]) / h["pitch"]), math.floor((h["r"] - h["phase"]) / h["pitch"])
        for j in range(j0, j1 + 1):
            sj = h["phase"] + j * h["pitch"]
            half = math.sqrt(max(h["r"] ** 2 - sj ** 2, 0.0)) + 0.5
            qx, qy = h["cx"] + sj * nx, h["cy"] + sj * ny
            body += (r"\draw[line width=" + f"{h['w']:.2f}pt] " + pt(qx - half * ux, qy - half * uy) + " -- " +
                     pt(qx + half * ux, qy + half * uy) + ";")
        return r"\begin{scope}" + body + r"\end{scope}"

    def hatched(t):
        return any((t["x"] - h["cx"]) ** 2 + (t["y"] - h["cy"]) ** 2 < h["r"] ** 2 and
                   (t["x"] - h["x0"]) * h["into"][0] + (t["y"] - h["y0"]) * h["into"][1] > 0
                   for h in fg.get("hatches", []))

    out = [hatch(h) for h in fg.get("hatches", [])]
    for c in fg.get("circles", []):
        out.append(r"\draw" + style(c) + " " + pt(c["cx"], c["cy"]) + " circle[radius=" + f"{c['r']:.2f}pt];")
    for s in fg.get("segments", []):
        out.append(r"\draw" + style(s) + " " + pt(s["x0"], s["y0"]) + " -- " + pt(s["x1"], s["y1"]) + ";")
    for q in fg.get("paths", []):
        out.append(r"\draw" + style(q) + " " + " -- ".join(pt(x, y) for x, y in q["pts"]) + ";")
    for a in fg.get("arcs", []):
        sx = a["cx"] + a["r"] * math.cos(math.radians(a["a0"]))
        sy = a["cy"] - a["r"] * math.sin(math.radians(a["a0"]))
        out.append(r"\draw" + style(a) + " " + pt(sx, sy) + " arc[start angle=" + f"{a['a0']:.2f}, end angle=" +
                   f"{a['a1']:.2f}, radius={a['r']:.2f}pt];")
    for c in fg.get("discs", []):
        out.append(r"\fill " + pt(c["cx"], c["cy"]) + " circle[radius=" + f"{c['r']:.2f}pt];")
    for lab, t in zip(labels, fg["texts"]):
        # the ʿayn (ʿ) is a small sign and is set larger to be legible as a label
        size = r"\LARGE" if lab == "ʿ" else (r"\normalsize" if len(lab) <= 2 else r"\scriptsize")
        rot = f", rotate={t['rot']:.1f}" if t.get("rot") else ""
        box = "inner sep=0.6pt, fill=white" if hatched(t) else "inner sep=0pt"
        out.append(r"\node[" + box + rot + "] at " + pt(t["x"], t["y"]) + " {" + size + " " + inline(lab) + "};")
    opts = f"[scale={scale:.4f}]" if scale < 1 else ""
    return r"\begin{tikzpicture}" + opts + "\n".join(out) + r"\end{tikzpicture}"


def tex_escape(s):
    s = (s.replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%").replace("$", r"\$")
         .replace("#", r"\#").replace("_", r"\_").replace("{", r"\{").replace("}", r"\}"))
    return s


def inline(s):
    s = tex_escape(s)
    s = re.sub(r"\*([^*]+)\*", r"\\emph{\1}", s)
    s = re.sub(r"([؀-ۿ][؀-ۿ\s]*[؀-ۿ]|[؀-ۿ])", r"\\RL{\\ArNote \1}", s)
    return s


PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[a4paper,left=30mm,right=30mm,top=25mm,bottom=25mm,marginparwidth=16mm,marginparsep=4mm]{geometry}
\usepackage{fontspec,xcolor,pdflscape,needspace,tikz,longtable,array}
\usepackage[unicode,hidelinks]{hyperref}
\usepackage{polyglossia}
\setmainlanguage{english}
\setotherlanguages{arabic}
\setmainfont{Linux Libertine O}[Ligatures=TeX]
\newfontfamily\arabicfont{Amiri}[Script=Arabic]
\newfontfamily\ArNote{Amiri}[Script=Arabic,Scale=1.05]
\hypersetup{pdftitle={al-Battani, al-Zij al-Sabi: an English translation of the canons},pdfauthor={al-Battani}}
\setlength{\parindent}{0pt}\setlength{\parskip}{0.55em}
\tracinglostchars=2
\newcommand{\ArPage}[1]{\marginpar{\footnotesize\color{gray}Ar.\,p.\,#1}}
\newcommand{\ChapterHead}[4]{\par\needspace{8\baselineskip}\bigskip\pdfbookmark[1]{#1}{ch-#2}\hypertarget{EN-C#2}{}%
 {\large\bfseries\interlinepenalty=10000 #1#4{\normalfont\normalsize#3}\par}\nobreak\medskip}
\newcommand{\SectionHead}[4]{\par\needspace{6\baselineskip}\medskip\pdfbookmark[2]{#1}{sec-#2}\hypertarget{EN-S#2}{}%
 {\bfseries\interlinepenalty=10000 #1#4{\normalfont#3}\par}\nobreak\smallskip}
\begin{document}
"""


def front(done, total_lines):
    return "\n".join([
        r"\thispagestyle{empty}",
        r"\begin{center}\Large AL-BATTĀNĪ\par\vspace{4mm}\LARGE The Sabian Zīj\par\vspace{2mm}"
        r"\large \emph{al-Zīj al-Ṣābiʾ}\par\vspace{5mm}\normalsize the canons, translated from the Arabic\par"
        r"\vspace{2mm}in Nallino's edition, Part III (Rome, 1899)\end{center}\vspace{8mm}",
        r"\noindent This is an English translation of the canons of al-Battānī's \emph{Zīj}, made from the Arabic "
        r"text as Nallino printed it. Every sentence of the Arabic is translated, in the order of the text; the "
        r"numbers are given in figures. Words added for the sense stand in square brackets. The notes identify "
        r"quotations, record where the translation follows a correction of Nallino's, and explain terms. The pages "
        r"of the Arabic text are given in the margin. Nallino's Latin translation (Part I, Milan, 1903) was used as "
        r"a check on the meaning throughout; its wording is not followed.",
        r"\par\smallskip\noindent " + done + ". It is AI-integrated work "
        r"(Claude), 2026; no person has proofread it. It is dedicated to the public domain (CC0 1.0).",
        r"\par\clearpage"])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    allrows = sources.arabic_rows()
    files = sorted((HERE / "text").glob("C*.txt"))
    tex = [PREAMBLE]
    body, align, errors, chapters, nlines = [], [], [], [], 0
    for f in files:
        n, blocks = parse(f)
        rows = sources.arabic_chapter(allrows, n)
        errs = check(n, blocks, rows)
        errors += [f"{f.name}: {e}" for e in errs]
        chapters.append(n)
        idx = {r["anchor"]: i for i, r in enumerate(rows)}
        last_page, carry = None, ""
        for k, b in enumerate(blocks):
            if b["kind"] == "skip":
                align.append((f"EN-C{n:02d}-B{k:02d}", n, "skip", b["first"], b["last"], "", 0, b["arg"]))
                continue
            a, z = idx.get(b["first"], 0), idx.get(b["last"], 0)
            pages = []
            for i in range(a, z + 1):
                p = rows[i]["printed"].translate(WESTERN)
                if p not in pages:
                    pages.append(p)
            nlines += sum(1 for i in range(a, z + 1) if rows[i]["kind"] in REQUIRED)
            mark = carry + "".join(r"\ArPage{" + p + "}" for p in pages if p != last_page and p != "-")
            carry = ""
            last_page = pages[-1] if pages else last_page
            text = " ".join(b["text"])
            notes = r"\textsuperscript{,}".join(r"\footnote{" + inline(x) + "}" for x in b["notes"])
            if b["kind"] == "h":
                body.append(r"\ChapterHead{" + inline(text) + "}{" + f"{n:02d}" + "}{" + mark + "}{" + notes + "}")
            elif b["kind"] == "s":
                body.append(r"\SectionHead{" + inline(text) + "}{" + f"{n:02d}{b['arg']}" + "}{" + mark + "}{" + notes +
                            "}")
            elif b["kind"] == "c":
                body.append(r"\begin{center}" + mark + inline(text) + notes + r"\end{center}")
            elif b["kind"] == "table":
                rows_en = [[c.strip() for c in r.split("|")] for r in b["text"]]
                ncol = max(len(r) for r in rows_en)
                spec = "|" + "c|" * ncol
                lines = [r"\hline " + " & ".join(inline(c) for c in r) + r" \\" for r in rows_en]
                body.append(r"\begin{landscape}\begin{center}" + mark + r"{\bfseries " + inline(b["arg"]) + "}" +
                            notes + r"\par\medskip{\footnotesize\setlength{\tabcolsep}{3pt}\begin{tabular}{" +
                            spec + "}" + "\n".join(lines) + r"\hline\end{tabular}}\end{center}\end{landscape}")
                text = " ".join(b["text"]).replace("|", " ")
            elif b["kind"] == "figure":
                fg = figure_geometry(b["first"])
                if figure_height(fg) > FLOAT_HEIGHT:
                    # a figure that fills most of a page floats to the top of a page, so that the text runs on
                    # beside it; its notes stand under it and its page mark goes to the next block
                    under = "".join(r"\par\smallskip{\footnotesize " + inline(x) + "}" for x in b["notes"])
                    body.append(r"\begin{figure}[tp]\centering" + figure_tex(fg, b["text"]) + under + r"\end{figure}")
                    carry = mark
                else:
                    body.append(r"\par\begin{center}" + mark + figure_tex(fg, b["text"]) + notes + r"\end{center}")
            elif b["kind"] == "li":
                body.append(r"\par\noindent\hangindent=2em\hangafter=1 " + mark + r"\makebox[2em][l]{" + b["arg"] +
                            ".}" + inline(text) + notes + r"\par")
            else:
                body.append(r"\par " + mark + inline(text) + notes + r"\par")
            align.append((f"EN-C{n:02d}-B{k:02d}", n, b["kind"], b["first"], b["last"], " ".join(pages),
                          len(text.split()), ""))
    if errors:
        for e in errors:
            print("ERROR", e)
        raise SystemExit(1)
    if chapters == list(range(58)):
        done = ("This version holds all the canons: the list of chapters, chapters 1 to 57 and the eight short "
                "chapters without numbers that follow chapter 57 in the Escorial codex (Nallino's A to H). The "
                "names, descriptions and headings of the tables of Part III are to follow")
    else:
        done = (f"The translation is in progress. This version holds the list of chapters and "
                f"chapter{'s' if len(chapters) > 2 else ''} {', '.join(str(c) for c in chapters if c)}")
    tex.append(front(done, nlines))
    tex += body
    build_tables.main()
    if (HERE / "tables_en.tex").exists():
        tex.append(r"\input{tables_en.tex}")
    tex.append(r"\end{document}")
    (HERE / "zij_en.tex").write_text("\n".join(tex) + "\n", encoding="utf-8", newline="\n")
    with open(HERE / "alignment.tsv", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("block\tchapter\tkind\tfirst_arabic_line\tlast_arabic_line\tarabic_pages\tenglish_words\tnote\n")
        for row in align:
            fh.write("\t".join(str(x) for x in row) + "\n")
    h = hashlib.sha256()
    for f in files:
        h.update(f.name.encode() + b"\0" + f.read_bytes())
    ck = {"edition": "EN: English translation of the canons of the Zij", "chapters_done": chapters,
          "arabic_lines_translated": nlines, "blocks": len(align),
          "english_words": sum(r[6] for r in align),
          "canonical_source_checkpoint_sha256": h.hexdigest(),
          "canonical_source_checkpoint_note": "SHA-256 over the chapter files in order: file name, a NUL byte, the bytes"}
    (HERE / "checkpoint.json").write_text(json.dumps(ck, ensure_ascii=False, indent=1) + "\n", encoding="utf-8",
                                          newline="\n")
    print(f"chapters {chapters}: {nlines} Arabic lines translated, {len(align)} blocks, {ck['english_words']} words")


if __name__ == "__main__":
    main()

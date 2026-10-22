"""The English translation of al-Battani's Zij: check the chapter files against the Arabic and write the TeX.

Chapter files (text/C##.txt), one per chapter (C00 is the invocation and the list of chapters):
  @chapter N
  % ...                       a comment
  @h FIRST..LAST              a heading; the English follows on the next lines
  @c FIRST..LAST              a centred line (the invocation)
  @p FIRST..LAST              a paragraph
  @li FIRST..LAST | NUMBER    an item of the list of chapters
  @skip FIRST..LAST | WHY     Arabic lines that are not part of al-Battani's text (Nallino's title page)
  @table FIRST..LAST | TITLE  a table printed in the text: its cells (kind cell); then one line per row, the cells
                              separated by |, in the order of the printed columns from right to left, which the
                              English sets from left to right
  @n TEXT                     a note to the block before it
FIRST..LAST are the anchors of the first and the last Arabic line that the block translates (S10-S12 anchors.tsv).
Two consecutive blocks may share their boundary line, where a sentence ends inside a line; otherwise every line of the
Arabic text of the chapter (kinds display, text, h1, h2, cell) belongs to exactly one block. Nallino's notes (kind note),
the labels of figures and the Latin title lines are not translated.
Inline: *...* emphasis; Arabic in «» is set in the Arabic font.

python build_en.py   (writes zij_en.tex, alignment.tsv and checkpoint.json; fails on any coverage error)"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "tools"))
import sources  # noqa: E402

REQUIRED = {"display", "text", "h1", "h2", "cell"}
WESTERN = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


def parse(path):
    blocks, n = [], None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.startswith("%"):
            continue
        if raw.startswith("@chapter"):
            n = int(raw.split()[1])
            continue
        m = re.match(r"@(h|c|p|li|skip|table) (\S+)\.\.(\S+)(?: \| (.*))?$", raw)
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
    """every required line belongs to one block: table blocks own the cells of their range, the other blocks the
    other required lines; consecutive text blocks may share their boundary line"""
    idx = {r["anchor"]: i for i, r in enumerate(rows)}
    req = [i for i, r in enumerate(rows) if r["kind"] in REQUIRED]
    owner = {}
    errors = []
    for cls in ("table", "text"):
        prev_last, prev_k = None, None
        for k, b in enumerate(blocks):
            if (b["kind"] == "table") != (cls == "table"):
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
                if kind not in REQUIRED or (kind == "cell") != (cls == "table"):
                    continue
                if i in owner and not (i == a and owner[i] == prev_k and i == prev_last):
                    errors.append(f"block {k}: {rows[i]['anchor']} already in block {owner[i]}")
                owner[i] = k
            if cls == "table":
                cells = [i for i in range(a, z + 1) if rows[i]["kind"] == "cell"]
                ncells = sum(len(r.split("|")) for r in b["text"])
                if ncells != len(cells):
                    errors.append(f"block {k}: {ncells} English cells for {len(cells)} printed cells")
            prev_last, prev_k = z, k
    missing = [rows[i]["anchor"] for i in req if i not in owner]
    if missing:
        errors.append(f"not translated: {', '.join(missing[:8])}{' …' if len(missing) > 8 else ''} ({len(missing)})")
    return errors


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
\usepackage{fontspec,xcolor,pdflscape}
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
\newcommand{\ChapterHead}[4]{\par\bigskip\penalty-300\pdfbookmark[1]{#1}{ch-#2}\hypertarget{EN-C#2}{}%
 {\large\bfseries #1#4}#3\par\medskip}
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
        r"\par\smallskip\noindent The translation is in progress. " + done + ". It is AI-integrated work "
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
        last_page = None
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
            mark = "".join(r"\ArPage{" + p + "}" for p in pages if p != last_page and p != "-")
            last_page = pages[-1] if pages else last_page
            text = " ".join(b["text"])
            notes = "".join(r"\footnote{" + inline(x) + "}" for x in b["notes"])
            if b["kind"] == "h":
                body.append(r"\ChapterHead{" + inline(text) + "}{" + f"{n:02d}" + "}{" + mark + "}{" + notes + "}")
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
    done = (f"This version holds the list of chapters and chapter{'s' if len(chapters) > 2 else ''} "
            f"{', '.join(str(c) for c in chapters if c)}")
    tex.append(front(done, nlines))
    tex += body
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

"""The English translation of al-Battani's commentary on Ptolemy's Tetrabiblos: check the chapter files against the
Arabic and write the TeX. The Arabic is Nadine Löhr's transcription of the Escorial manuscript (PAL, CC BY 4.0) as S14
edits it; its lines and anchors are S14/commentarius/anchors.tsv, its 40 chapters S14/commentarius/chapters.tsv.

Chapter files (text/K##.txt), one per chapter of PAL (K00 is the title page and the invocation):
  @chapter N
  % ...                       a comment
  @h FIRST..LAST              the heading of the chapter; the English follows on the next lines
  @c FIRST..LAST              a centred line (the title page, the invocation)
  @p FIRST..LAST              a paragraph
  @n TEXT                     a note to the block before it
FIRST..LAST are the anchors of the first and the last line of the manuscript that the block translates. A chapter runs
from the line of its heading to the line before the next heading, or to that line itself where the next heading begins
inside it; two consecutive blocks may share their boundary line, where a sentence ends inside a line, and so may the
last block of a chapter and the heading of the next. Otherwise every line belongs to exactly one block.
The two tables of ff. 80r-80v are set from tables.tsv (their headings and words in English) and S14's cells.
Inline: *...* emphasis; Arabic letters are set in the Arabic font.

python build_commentary.py   (writes commentary_en.tex, alignment.tsv and checkpoint.json; fails on any coverage error)"""
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S14 = HERE.parent.parent / "S14" / "commentarius"


def read_tsv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE))


def chapters_of(rows):
    """chapter number -> (first index, last index) of its lines"""
    idx = {r["anchor"]: i for i, r in enumerate(rows)}
    heads = [(int(c["pal_id"].split(".")[1]), idx[c["anchor"]]) for c in read_tsv(S14 / "chapters.tsv")]
    out = {0: (0, heads[0][1] - 1)}
    for k, (n, a) in enumerate(heads):
        if k + 1 < len(heads):
            b = heads[k + 1][1]
            # the next heading begins its line (after a folio mark of the Berlin manuscript, «/B4r/»)
            starts = re.sub(r"^\s*/B\d+[rv]/", "", rows[b]["text"]).lstrip()[:1] in ("〈", "〈")
            out[n] = (a, b - 1 if starts else b)
        else:
            out[n] = (a, len(rows) - 1)
    return out


def parse(path):
    blocks, n = [], None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.startswith("%"):
            continue
        if raw.startswith("@chapter"):
            n = int(raw.split()[1])
            continue
        m = re.match(r"@(h|c|p) (\S+)\.\.(\S+)$", raw)
        if m:
            blocks.append({"kind": m.group(1), "first": m.group(2), "last": m.group(3), "text": [], "notes": []})
            continue
        if raw.startswith("@n "):
            blocks[-1]["notes"].append(raw[3:].strip())
            continue
        if raw.startswith("@"):
            raise SystemExit(f"{path.name}: unknown line {raw[:40]}")
        blocks[-1]["text"].append(raw.strip())
    return n, blocks


def check(blocks, rows, a0, z0):
    """every line from a0 to z0 belongs to one block; consecutive blocks may share their boundary line"""
    idx = {r["anchor"]: i for i, r in enumerate(rows)}
    owner, errors, prev = {}, [], None
    for k, b in enumerate(blocks):
        if b["first"] not in idx or b["last"] not in idx:
            errors.append(f"block {k}: unknown anchor {b['first']} or {b['last']}")
            continue
        a, z = idx[b["first"]], idx[b["last"]]
        if a > z:
            errors.append(f"block {k}: {b['first']} after {b['last']}")
        if a < a0 or z > z0:
            errors.append(f"block {k}: outside the chapter ({rows[a0]['anchor']}..{rows[z0]['anchor']})")
        if prev is not None and a < prev:
            errors.append(f"block {k}: begins before the end of the block before it")
        if not b["text"]:
            errors.append(f"block {k}: no English")
        for i in range(a, z + 1):
            if i in owner and not (i == a and i == prev):
                errors.append(f"block {k}: {rows[i]['anchor']} already in block {owner[i]}")
            owner[i] = k
        prev = z
    missing = [rows[i]["anchor"] for i in range(a0, z0 + 1) if i not in owner]
    if missing:
        errors.append(f"not translated: {', '.join(missing[:8])}{' …' if len(missing) > 8 else ''} ({len(missing)})")
    return errors


def tex_escape(s):
    return (s.replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%").replace("$", r"\$")
            .replace("#", r"\#").replace("_", r"\_").replace("{", r"\{").replace("}", r"\}"))


def inline(s):
    s = tex_escape(s)
    s = re.sub(r"([⟨⟩⟦⟧])", r"{\\mdseries \1}", s)        # the bold font has no angle brackets
    s = re.sub(r"\*([^*]+)\*", r"\\emph{\1}", s)
    s = re.sub(r"([؀-ۿ][؀-ۿ\s]*[؀-ۿ]|[؀-ۿ])", r"\\RL{\\ArNote \1}", s)
    return s


PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[a4paper,left=30mm,right=30mm,top=25mm,bottom=25mm,marginparwidth=16mm,marginparsep=4mm]{geometry}
\usepackage{fontspec,xcolor,needspace,longtable,array}
\usepackage[unicode,hidelinks]{hyperref}
\usepackage{polyglossia}
\setmainlanguage{english}
\setotherlanguages{arabic}
\setmainfont{Linux Libertine O}[Ligatures=TeX]
\newfontfamily\arabicfont{Amiri}[Script=Arabic]
\newfontfamily\ArNote{Amiri}[Script=Arabic,Scale=1.05]
\hypersetup{pdftitle={al-Battani, commentary on Ptolemy's Tetrabiblos: an English translation},pdfauthor={al-Battani}}
\setlength{\parindent}{0pt}\setlength{\parskip}{0.55em}
\tracinglostchars=2
\newcommand{\Fol}[1]{\marginpar{\footnotesize\color{gray}f.\,#1}}
\newcommand{\ChapterHead}[4]{\par\needspace{8\baselineskip}\bigskip\pdfbookmark[1]{#1}{ch-#2}\hypertarget{EN-K#2}{}%
 {\large\bfseries\interlinepenalty=10000 #1#4{\normalfont\normalsize#3}\par}\nobreak\medskip}
\begin{document}
"""


def front(done):
    return "\n".join([
        r"\thispagestyle{empty}",
        r"\begin{center}\Large AL-BATTĀNĪ\par\vspace{4mm}\LARGE Commentary on Ptolemy's \emph{Tetrabiblos}\par"
        r"\vspace{2mm}\large \emph{Sharḥ Kitāb al-Arbaʿ maqālāt fī aḥkām ʿilm al-nujūm}\par\vspace{5mm}\normalsize "
        r"translated from the Arabic of the Escorial manuscript, árabe 969, ff. 20r–80v\end{center}\vspace{8mm}",
        r"\noindent This is an English translation of al-Battānī's commentary on the \emph{Tetrabiblos}, the earliest "
        r"that survives. It is made from Nadine Löhr's transcription of the Escorial manuscript in \emph{Ptolemaeus "
        r"Arabus et Latinus} (Bavarian Academy of Sciences and Humanities, 2021, CC BY 4.0). The commentary follows "
        r"Ptolemy's work chapter by chapter, restating his doctrine and adding al-Battānī's own explanations, examples "
        r"and procedures; the notes give the chapter of the \emph{Tetrabiblos} in F.~E. Robbins's numbering, which "
        r"was used as a check on the meaning, and explain terms. Every sentence of the Arabic is translated, in the "
        r"order of the text; numbers are given in figures. Words added for the sense stand in square brackets; words "
        r"supplied by the editor of the transcription in angle brackets ⟨ ⟩. Words that the editor marks as additions "
        r"of the copyist, such as invocations, stand in double brackets ⟦ ⟧, and words struck out by the copyist are "
        r"left out. A doubtful reading of the transcription is marked (?). The folios of the manuscript are given in "
        r"the margin.",
        r"\par\smallskip\noindent " + done + ". It is AI-integrated work (Claude), 2026; no person has proofread it. "
        r"The translation is dedicated to the public domain (CC0 1.0); the Arabic it translates is Löhr's "
        r"transcription, used under its licence (CC BY 4.0).",
        r"\par\clearpage"])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rows = read_tsv(S14 / "anchors.tsv")
    ranges = chapters_of(rows)
    files = sorted((HERE / "text").glob("K*.txt"))
    body, align, errors, chapters, covered = [], [], [], [], set()
    idx = {r["anchor"]: i for i, r in enumerate(rows)}
    last_fol = None
    for f in files:
        n, blocks = parse(f)
        a0, z0 = ranges[n]
        errors += [f"{f.name}: {e}" for e in check(blocks, rows, a0, z0)]
        chapters.append(n)
        for k, b in enumerate(blocks):
            a, z = idx.get(b["first"], 0), idx.get(b["last"], 0)
            fols = []
            for i in range(a, z + 1):
                if rows[i]["folio"] not in fols:
                    fols.append(rows[i]["folio"])
            covered.update(range(a, z + 1))
            mark = "".join(r"\Fol{" + p + "}" for p in fols if p != last_fol)
            last_fol = fols[-1] if fols else last_fol
            text = " ".join(b["text"])
            notes = r"\textsuperscript{,}".join(r"\footnote{" + inline(x) + "}" for x in b["notes"])
            if b["kind"] == "h":
                body.append(r"\ChapterHead{" + inline(text) + "}{" + f"{n:02d}" + "}{" + mark + "}{" + notes + "}")
            elif b["kind"] == "c":
                body.append(r"\begin{center}" + mark + inline(text) + notes + r"\end{center}")
            else:
                body.append(r"\par " + mark + inline(text) + notes + r"\par")
            align.append((f"EN-K{n:02d}-B{k:02d}", n, b["kind"], b["first"], b["last"], " ".join(fols),
                          len(text.split())))
    if errors:
        for e in errors:
            print("ERROR", e)
        raise SystemExit(1)
    done_all = chapters == list(range(41))
    done = ("This version holds the whole commentary" if done_all else
            "The translation is in progress. This version holds " +
            ("the title page and " if 0 in chapters else "") +
            f"chapter{'s' if len([c for c in chapters if c]) > 1 else ''} " +
            ", ".join(str(c) for c in chapters if c))
    tex = [PREAMBLE, front(done)] + body + [r"\end{document}"]
    (HERE / "commentary_en.tex").write_text("\n".join(tex) + "\n", encoding="utf-8", newline="\n")
    with open(HERE / "alignment.tsv", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("block\tchapter\tkind\tfirst_line\tlast_line\tfolios\tenglish_words\n")
        for row in align:
            fh.write("\t".join(str(x) for x in row) + "\n")
    h = hashlib.sha256()
    for f in files:
        h.update(f.name.encode() + b"\0" + f.read_bytes())
    ck = {"edition": "EN: English translation of al-Battani's commentary on the Tetrabiblos", "chapters_done": chapters,
          "manuscript_lines_translated": len(covered), "blocks": len(align), "english_words": sum(r[6] for r in align),
          "canonical_source_checkpoint_sha256": h.hexdigest(),
          "canonical_source_checkpoint_note": "SHA-256 over the chapter files in order: file name, a NUL byte, the bytes"}
    (HERE / "checkpoint.json").write_text(json.dumps(ck, ensure_ascii=False, indent=1) + "\n", encoding="utf-8",
                                          newline="\n")
    print(f"chapters {chapters}: {len(covered)} of {len(rows)} manuscript lines, {len(align)} blocks, "
          f"{ck['english_words']} words")


if __name__ == "__main__":
    main()

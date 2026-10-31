"""English edition of the tables of Part II that Part III does not print in Arabic (S06).

The readers of S06 (S06/FAMILY/p2_FAMILY.tex) reproduce Nallino's pages: the Arabic heads of the codex, his Latin
translation of them and the numbers. This script makes the same pages with English in place of the Latin:

  python build_tables_en.py list      the text runs that need English and have none in heads_en.tsv
  python build_tables_en.py build     writes FAMILY_en.tex for every family, checks that every run with Latin words
                                      has its English and that every row of heads_en.tsv is used, compiles each with
                                      XeLaTeX and joins the pages, in Nallino's order, into tables_en.pdf

heads_en.tsv has two columns, the run as it stands in the reader (white space collapsed, \\\\ for a line break) and
its English. A run is the visible text between TeX commands; runs of numbers, of transliterated Arabic and Syriac
words and of the folio marks of the codex stand as they are. The numbers, the Arabic and the layout are not touched.
The spurious tables of pp. 297-307 are in English in ../nallino/ and are not repeated here."""
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S06 = HERE.parent.parent / "S06"
FAMILIES = ["signs", "concordance", "mean_motions", "syzygies", "spherical", "equations", "eclipses", "parallax",
            "planets", "stations", "latitudes", "apparitions", "revolutions"]
ARABIC = re.compile("[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\u200c\u200d]+")
DIM = re.compile(r"^-?[\d.]+(mm|pt|cm|em|ex|in|bp|sp)$")
LAYOUT = {"begin", "end", "setlength", "settowidth", "addtolength", "newlength", "rule", "vspace", "hspace",
          "rotatebox", "multicolumn", "multirow", "parbox", "makebox", "raisebox", "llap", "rlap", "includegraphics",
          "newfontfamily", "setmainfont", "fontsize", "symbol", "kern", "resizebox", "scalebox", "colorbox", "color",
          "textcolor", "arrayrulecolor", "cline", "hhline", "label", "ref", "phantom", "hphantom", "vphantom",
          "renewcommand", "newcommand", "AbjadOver", "setcounter", "fbox", "framebox", "addfontfeatures",
          "extracolsep", "cmidrule", "rotatebox", "rotcell", "Rot", "rot", "vrule", "hrule", "raggedleft",
          "centering", "raggedright", "arraybackslash"}
TEXTARG = {"parbox", "makebox", "multicolumn", "rotatebox", "multirow", "raisebox", "colorbox", "fbox", "framebox",
           "llap", "rlap", "textcolor"}
MARKS = "āīūēōḥṣṭḍẓǵġḫẖḳṯḏšžčćśñàèìòùáéíóúâêîôûäëïöüçÿ‘’ʿʾĀĪŪḤṢṬḌẒǴŠŽČ"
ROMAN = re.compile(r"^(?=[ivxlc]+$)(c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})$", re.I)
KEEP = {"NALLINO", "f", "v", "r", "a", "b", "c", "d", "e", "g", "h", "k", "l", "m", "n", "o", "p", "q", "s", "t",
        "u", "w", "x", "y", "z"}


def runs(tex):
    """(start, end, key) of every visible text run of the document body"""
    start = tex.index(r"\begin{document}") + len(r"\begin{document}")
    body = tex[start:]
    body = re.sub(r"(?<!\\)%.*", lambda m: " " * len(m.group(0)), body)
    body = ARABIC.sub(lambda m: " " * len(m.group(0)), body)
    n, out, i = len(body), [], 0
    cur = []   # (index, char)

    def flush():
        # a run begins and ends with its text: line breaks, spaces and thin spaces at its ends stay outside it
        while cur and (cur[0][1].isspace() or cur[0][1] in "\x00\\"):
            cur.pop(0)
        while cur and (cur[-1][1].isspace() or cur[-1][1] in "\x00\\"):
            cur.pop()
        if not cur:
            return
        a, e = cur[0][0], cur[-1][0] + 1
        raw = body[a:e]
        key = re.sub(r"\s+", " ", raw).strip()
        cur.clear()
        if re.search(r"[^\W\d_]{2,}", key) and not DIM.match(key):
            out.append((start + a, start + e, key))

    def group_end(j):
        op = body[j]
        cl = "}" if op == "{" else "]"
        depth = 0
        while j < n:
            c = body[j]
            if c == "\\":
                j += 2
                continue
            if c == op:
                depth += 1
            elif c == cl:
                depth -= 1
                if depth == 0:
                    return j + 1
            j += 1
        return j

    while i < n:
        c = body[i]
        if c == "\\" and body[i + 1:i + 2] == "\\":
            j = i + 2
            m = re.match(r"\s*\[[^\]]*\]", body[j:])
            if m:   # a spaced line break ends the run: the lines are separate entries of a column
                flush()
                i = j + m.end()
                continue
            cur.append((i, "\\"))
            cur.append((i + 1, "\\"))
            i += 2
            continue
        if c == "\\":
            m = re.match(r"\\([A-Za-z@]+)\*?", body[i:])
            if not m:   # \, \; \& and the like
                if body[i + 1:i + 2] in (",", ";", " ", "!", ":"):
                    cur.append((i, "\x00"))
                    cur.append((i + 1, "\x00"))
                    i += 2
                    continue
                flush()
                i += 2
                continue
            name = m.group(1)
            flush()
            i += m.end()
            if name in LAYOUT:
                args = []
                while i < n and body[i] in "{[":
                    e = group_end(i)
                    args.append((i, e))
                    i = e
                if name in TEXTARG and args and body[args[-1][0]] == "{":
                    i = args[-1][0] + 1
            continue
        if c in "{}&$^_~#":
            flush()
            i += 1
            continue
        cur.append((i, c))
        i += 1
    flush()
    return out


TIKZ = {"circle", "cycle", "at", "align", "center", "rotate", "font", "mm", "pt", "anchor", "left", "right", "above",
        "below", "scale", "inner", "sep", "xshift", "yshift", "draw", "fill", "line", "width", "node"}


def plain(key):
    """a run that stands as it is: numbers, transliterations, Greek, folio marks, Roman numerals, drawing code"""
    toks = re.findall(r"[^\W\d_]+", key)
    if toks and all(t in TIKZ for t in toks) and re.search(r"[()=;\]\[]", key):
        return True
    for word in re.split(r"[\s\\]+", key):
        if any(ch in MARKS for ch in word) or re.search("[Ͱ-Ͽἀ-῿]", word):
            continue   # a transliterated or a Greek word
        for tok in re.findall(r"[^\W\d_]+", word):
            if tok in KEEP or len(tok) == 1 or ROMAN.match(tok):
                continue
            return False
    return True


def load_heads():
    heads = {}
    path = HERE / "heads_en.tsv"
    for k, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 2:
            raise SystemExit(f"heads_en.tsv line {k}: {len(parts)} columns")
        if parts[0] in heads:
            raise SystemExit(f"heads_en.tsv line {k}: the run is there twice: {parts[0]}")
        heads[parts[0]] = parts[1]
    return heads


def english(fam, tex, heads, used, missing):
    spans = runs(tex)
    out, last = [], 0
    for a, e, key in spans:
        if key in heads:
            out.append(tex[last:a])
            out.append(heads[key])
            last = e
            used.add(key)
        elif not plain(key):
            missing.append((fam, key))
    out.append(tex[last:])
    t = "".join(out)
    t = t.replace(r"\setmainlanguage{latin}", r"\setmainlanguage{english}")
    t = t.replace("Path=./fonts/", f"Path=../../S06/{fam}/fonts/")
    return t


HEAD = re.compile(r"\\noindent\\makebox\[\\textwidth\]\{(?:\\rlap\{(\d+)\}\\hfill|\\hfill\{\\scriptsize [^{}]*\}\\hfill"
                  r"\\llap\{(\d+)\}\})")


def page_numbers(tex):
    """Nallino's page number of every page of a reader, from its running head (\\llap on the right-hand pages,
    \\rlap on the left-hand ones)"""
    return [int(m.group(1) or m.group(2)) for m in HEAD.finditer(tex)]


def title_of(fam):
    head = (S06 / fam / "README.md").read_text(encoding="utf-8").splitlines()[0]
    return re.sub(r"^# S06 — | \(Part II pp?\..*\)$", "", head)


def ranges(nums):
    out, a, b = [], nums[0], nums[0]
    for p in nums[1:]:
        if p == b + 1:
            b = p
            continue
        out.append((a, b))
        a = b = p
    out.append((a, b))
    return out


FRONT = r"""\documentclass[11pt]{article}
\usepackage[paperwidth=210mm,paperheight=297mm,margin=25mm]{geometry}
\usepackage{fontspec,polyglossia}
\setmainlanguage{english}
\setmainfont{Linux Libertine O}[Ligatures=TeX]
\pagestyle{empty}\setlength{\parindent}{0pt}\setlength{\parskip}{0.6em}
\begin{document}
\begin{center}{\LARGE al-Battānī, \textit{al-Zīj al-Ṣābiʾ}}\\[2mm]
{\Large The tables of Part II of Nallino's edition, in English}\end{center}
\vspace{6mm}
C. A. Nallino prints al-Battānī's tables in Part II of \textit{Al-Battānī sive Albatenii opus astronomicum} (Milan,
1907) from the Escorial codex, with the Arabic heads of the codex and his Latin translation of them. The tables that
Part III also prints in Arabic (the chronological and the geographical tables, the circular diagrams, the star
catalogue and the tables of the stars for the year 1211) are translated from the Arabic in the English \textit{Zīj};
the spurious tables of pp. 297--307 are in English with Nallino's notes on them. This volume gives the other tables of
Part II as the transcription of this repository reproduces them (S06), with English in place of Nallino's Latin. The
numbers, the Arabic, the folio marks of the codex and Nallino's page numbers stand as printed; his square brackets
mark what he supplies. The terms are those of the English \textit{Zīj} and its glossary.

\vspace{4mm}
\begin{tabular}{@{}p{135mm}@{\hspace{4mm}}l@{}}
ROWS\end{tabular}

\vfill
{\small The English: AI-translated (Claude), 2026. No person has proofread it. Dedicated to the public domain
(CC0 1.0). Nallino's edition is in the public domain.}
\end{document}
"""


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    mode = sys.argv[1] if len(sys.argv) > 1 else "build"
    heads = load_heads() if (HERE / "heads_en.tsv").exists() else {}
    used, missing = set(), []
    texts = {}
    for fam in FAMILIES:
        tex = (S06 / fam / f"p2_{fam}.tex").read_text(encoding="utf-8")
        texts[fam] = english(fam, tex, heads, used, missing)
    if mode == "list":
        seen = {}
        for fam, key in missing:
            seen.setdefault(key, []).append(fam)
        for key, fams in seen.items():
            print(f"{key}\t{','.join(sorted(set(fams)))}\t{len(fams)}")
        print(f"{len(seen)} runs without English", file=sys.stderr)
        return
    if missing:
        for fam, key in missing[:40]:
            print(f"no English: {fam}: {key}")
        raise SystemExit(f"{len(missing)} runs without English")
    unused = sorted(set(heads) - used)
    if unused:
        raise SystemExit("rows of heads_en.tsv not used: " + "; ".join(unused[:20]))
    from pypdf import PdfReader, PdfWriter

    def xelatex(name):
        r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", name], cwd=HERE,
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        stem = name[:-4]
        log = (HERE / f"{stem}.log").read_text(encoding="utf-8", errors="replace")
        if r.returncode != 0:
            raise SystemExit(f"{stem}: XeLaTeX failed:\n" + r.stdout[-2000:])
        for ext in ("aux", "log"):
            (HERE / f"{stem}.{ext}").unlink(missing_ok=True)
        return sorted(set(re.findall(r"Missing character: There is no (.) ", log)))

    pages, bad = [], []
    for fam in FAMILIES:
        texfile = HERE / f"{fam}_en.tex"
        texfile.write_text(texts[fam], encoding="utf-8", newline="\n")
        miss = xelatex(texfile.name)
        nums = page_numbers(texts[fam])
        count = len(PdfReader(str(HERE / f"{fam}_en.pdf")).pages)
        if count != len(nums):
            raise SystemExit(f"{fam}: {count} pages in the PDF, {len(nums)} running heads")
        print(f"{fam}: pp. {', '.join(f'{a}-{b}' for a, b in ranges(nums))} ({count}), missing characters: "
              f"{''.join(miss) or 'none'}")
        bad += miss
        pages += [(p, fam, k) for k, p in enumerate(nums, 1)]
    pages.sort()
    if len({p for p, _, _ in pages}) != len(pages):
        raise SystemExit("a page of Part II is in two readers")
    rows = []
    for fam in FAMILIES:
        nums = [p for p, f, _ in pages if f == fam]
        rows.append(title_of(fam) + r" & pp. " + ", ".join(f"{a}--{b}" if a != b else str(a) for a, b in ranges(nums))
                    + r" \\")
    (HERE / "front_en.tex").write_text(FRONT.replace("ROWS", "\n".join(rows)), encoding="utf-8", newline="\n")
    bad += xelatex("front_en.tex")
    if bad:
        raise SystemExit("missing characters: " + "".join(sorted(set(bad))))
    readers = {fam: PdfReader(str(HERE / f"{fam}_en.pdf")) for fam in FAMILIES}
    w = PdfWriter()
    w.add_page(PdfReader(str(HERE / "front_en.pdf")).pages[0])
    pos = {}
    for p, fam, k in pages:
        pos[p] = len(w.pages)
        w.add_page(readers[fam].pages[k - 1])
    marks = sorted((a, b, fam) for fam in FAMILIES for a, b in ranges([p for p, f, _ in pages if f == fam]))
    for a, b, fam in marks:
        w.add_outline_item(f"{title_of(fam)}, pp. {a}-{b}" if a != b else f"{title_of(fam)}, p. {a}", pos[a])
    w.add_metadata({"/Title": "al-Battani, the tables of Part II of Nallino's edition, in English",
                    "/Creator": "build_tables_en.py"})
    with open(HERE / "tables_en.pdf", "wb") as f:
        w.write(f)
    for name in [f"{fam}_en.pdf" for fam in FAMILIES] + ["front_en.pdf"]:   # joined into tables_en.pdf
        (HERE / name).unlink()
    print(f"tables_en.pdf: {len(pages)} pages of tables and a front page, Part II pp. {pages[0][0]}-{pages[-1][0]}")


main()

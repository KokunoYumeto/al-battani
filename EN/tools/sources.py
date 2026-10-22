"""The sources of one chapter of the Zij for the English translation, side by side in reading order: al-Battani's
Arabic as transcribed from Nallino's Part III (S10-S12, with Nallino's apparatus), and Nallino's Latin translation of the
same chapter with his footnotes (Part I: S02 candidate v009 for pp. 1-53, S02/versio pp. 54-109, S03/versio, S04/versio).
Chapter 0 is the title, the invocation and the list of the 57 chapters.

python sources.py CHAPTER [OUTDIR]   (writes CHAPTER.txt into OUTDIR, default: the current folder)"""
import csv
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50}


def roman(s):
    total, prev = 0, 0
    for ch in reversed(s):
        v = ROMAN[ch]
        total += -v if v < prev else v
        prev = max(prev, v)
    return total


def arabic_rows():
    rows = []
    for s in ("S10", "S11", "S12"):
        with open(REPO / s / "textus" / "anchors.tsv", encoding="utf-8", newline="") as fh:
            rows += list(csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE))
    return rows


def arabic_chapter(rows, n):
    heads = [i for i, r in enumerate(rows) if r["kind"] == "h1" and r["text"].startswith("الباب")]
    assert len(heads) == 57, len(heads)
    if n == 0:
        first = next(i for i, r in enumerate(rows) if r["kind"] != "latin")
        return rows[first:heads[0]]
    end = heads[n] if n < 57 else len(rows)
    return rows[heads[n - 1]:end]


def clean_html(t):
    return re.sub(r"<[^>]+>", "", t)


def clean_tex(t):
    """a reading form of a line kept only as TeX in the v009 records"""
    t = re.sub(r"\\qfrac\{([^}]*)\}\{([^}]*)\}", r"\1/\2", t)
    t = re.sub(r"\\(?:CenterLine|textgreek|textit|textbf|emph)\{", "{", t)
    t = re.sub(r"\{\\(?:itshape|bfseries|scshape)\s*", "{", t)
    t = re.sub(r"\\(?:Indent|noindent|par|hfill|quad)\b\s*", "", t)
    t = re.sub(r"\\[a-zA-Z]+\s*", "", t)
    return t.replace("{", "").replace("}", "").replace("$", "").strip()


def latin_lines():
    """every line of Nallino's translation, pp. 1-150 (PDF 90-239), as (anchor, printed page, section, text)"""
    out = []
    v9 = REPO / "S02" / "candidate_v009_print001-053" / "transcription" / "pages"
    for f in sorted(v9.glob("AB01-PDF*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        for s in d["sections"]:
            for ln in s["lines"]:
                t = clean_html(ln["text"]) if "text" in ln else clean_tex(ln.get("tex", ""))
                if t:
                    out.append((ln["id"], d["printed_page"], s["role"], t))
    for sess in ("S02", "S03", "S04"):
        for f in sorted((REPO / sess / "versio" / "pages").glob("AB01-PDF*.txt")):
            pdf = int(f.stem[-4:])
            if pdf >= 240:
                continue
            printed, section, k = None, "body", 0
            for raw in f.read_text(encoding="utf-8").splitlines():
                if raw.startswith("@page"):
                    printed = raw.split()[2]
                    continue
                if raw.startswith("@notes"):
                    section, k = "notes", 0
                    continue
                if raw.startswith(("@obs", "@col", "%")) or not raw.strip():
                    continue
                k += 1
                out.append((f"AB01-PDF{pdf:04d}-{section}-L{k:03d}", printed, section, raw))
    return out


def latin_chapter(lines, n):
    heads = {}
    for i, (a, p, s, t) in enumerate(lines):
        m = re.search(r"CAPUT ([LXVI]+)\.", t)
        if m and s == "body":
            heads.setdefault(roman(m.group(1)), i)
    assert sorted(heads) == list(range(1, 58)), sorted(set(range(1, 58)) - set(heads))
    if n == 0:
        return lines[:heads[1]]
    end = heads[n + 1] if n < 57 else len(lines)
    # the notes and margins of the page on which the next chapter begins stand after its body lines
    tail = [x for x in lines[end:] if x[1] == lines[end - 1][1] and x[2] != "body"] if n < 57 else []
    return lines[heads[n]:end] + tail


def main():
    n = int(sys.argv[1])
    outdir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd()
    ar = arabic_chapter(arabic_rows(), n)
    la = latin_chapter(latin_lines(), n)
    text = [f"# Chapter {n}: Arabic (Nallino, Part III), {len(ar)} lines", ""]
    text += [f"{r['anchor']}\t{r['printed']}\t{r['kind']}\t{r['text']}" for r in ar]
    text += ["", f"# Chapter {n}: Nallino's Latin translation (Part I), {len(la)} lines", ""]
    text += [f"{a}\t{p}\t{s}\t{t}" for a, p, s, t in la]
    out = outdir / f"C{n:02d}.txt"
    out.write_text("\n".join(text) + "\n", encoding="utf-8", newline="\n")
    print(f"{out.name}: {len(ar)} Arabic lines, {len(la)} Latin lines")


if __name__ == "__main__":
    main()

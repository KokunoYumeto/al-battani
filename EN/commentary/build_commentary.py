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
        r"Ptolemy's work chapter by chapter, restating its doctrine and adding al-Battānī's own explanations, examples "
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


ABJAD = {"ا": 1, "ب": 2, "ج": 3, "د": 4, "ه": 5, "و": 6, "ز": 7, "ح": 8, "ط": 9, "ى": 10, "ي": 10, "ك": 20, "ل": 30,
         "م": 40, "ن": 50, "ص": 60, "ع": 70, "ف": 80, "ض": 90, "ق": 100, "ر": 200, "س": 300, "ت": 400, "ث": 500,
         "خ": 600, "ذ": 700, "ظ": 800, "غ": 900, "ش": 1000}                  # Maghribi values
YEAR = 365 * 1440 + 5 * 60 + 46 + 24 / 60       # the year of the revolution of the Zij (ch. 53), in minutes of time
SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn",
         "Aquarius", "Pisces"]
HOUSE = dict(zip(SIGNS, ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn",
                         "Saturn", "Jupiter"]))
# Ptolemy's triangles (Tetrabiblos I.18): the lord by day, the lord by night, the planet joined to the triangle
TRIANGLE = [("Sun", "Jupiter", "Mars"), ("Venus", "Moon", "Saturn"), ("Saturn", "Mercury", "Jupiter"),
            ("Mars", "Mars", "Venus / Moon")]
# Ptolemy's terms as Robbins tabulates them (Tetrabiblos I.21); Robbins's table prints Saturn for Mars as the last of Libra
TERMS = dict(zip(SIGNS, [re.findall(r"\w+ \d", s) for s in [
    "Jupiter 6 Venus 8 Mercury 7 Mars 5 Saturn 4", "Venus 8 Mercury 7 Jupiter 7 Saturn 2 Mars 6",
    "Mercury 7 Jupiter 6 Venus 7 Mars 6 Saturn 4", "Mars 6 Jupiter 7 Mercury 7 Venus 7 Saturn 3",
    "Jupiter 6 Mercury 7 Saturn 6 Venus 6 Mars 5", "Mercury 7 Venus 6 Jupiter 5 Saturn 6 Mars 6",
    "Saturn 6 Venus 5 Mercury 5 Jupiter 8 Mars 6", "Mars 6 Venus 7 Jupiter 8 Mercury 6 Saturn 3",
    "Jupiter 8 Venus 6 Mercury 5 Saturn 6 Mars 5", "Venus 6 Mercury 6 Jupiter 7 Saturn 6 Mars 5",
    "Saturn 6 Mercury 6 Venus 8 Jupiter 5 Mars 5", "Venus 8 Jupiter 6 Mercury 6 Mars 5 Saturn 5"]]))


def number(raw):
    """a cell of abjad numerals: (its value or None, the cell as the English gives it)"""
    s = raw.strip()
    doubt = s.startswith("{") and s.endswith("}")
    s = s.strip("{}").strip()
    if s in ("", "--"):
        return None, "–"
    if s == "؟":
        return None, "?"
    v = 0 if s == "۰" else sum(ABJAD[c] for c in s if c != " ")
    return v, f"{v}" + (" (?)" if doubt else "")


def read_en(path):
    en = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            k, v = line.split("\t")[:2]
            en[k] = v
    return en


def table_tex(errors):
    """the two tables of ff. 80r-80v in English, with notes on how their numbers and names compare with the
    computation from the year of the revolution and with Ptolemy's triangles and terms"""
    en = read_en(HERE / "tables.tsv")
    t1 = {(int(r["row"]), int(r["col"])): r["text"] for r in read_tsv(S14 / "tables" / "AB03-F080r-T01.tsv")}
    t2 = {(int(r["row"]), int(r["col"])): r["text"] for r in read_tsv(S14 / "tables" / "AB03-F080v-T01.tsv")}
    need = [f"80r:R{r}C{c}" for (r, c), x in t1.items() if r <= 2 and x.strip()]
    need += [f"80v:R1C{c}" for (r, c), x in t2.items() if r == 1 and x.strip()]
    need += ["sign:" + x.strip() for (r, c), x in t2.items() if c == 14 and r > 1 and x.strip()]
    need += sorted({"planet:" + ch for (r, c), x in t2.items() if r > 1 and r % 2 == 0 and c < 14
                    for ch in re.findall(r"[؀-ۿ]", x)})
    errors += [f"tables.tsv: no English for {k}" for k in need if k not in en]
    if any(k not in en for k in need):
        return ""
    E = lambda k: inline(en[k])                                                     # noqa: E731

    # f. 80r, left: the months of the revolution
    rows_a, notes_a = [], []
    for n in range(1, 14):
        r = 2 * n + 1
        cells = [number(t1[(r, c)]) for c in (4, 3, 2, 1)]
        total = n * YEAR / 13
        want = [n, int(total // 1440), int(total % 1440 // 60), total % 60]
        shown = []
        for k, ((v, s), w) in enumerate(zip(cells, want)):
            bad = v is not None and (abs(v - w) > 1 if k == 3 else v != w)
            shown.append(s + ("†" if bad else ""))
            if bad:
                what = ["month", "days", "hours", "minutes"][k]
                notes_a.append(f"month {n}, {what}: {v}, where the computation gives {round(w) if k == 3 else w}")
        rows_a.append(" & ".join(shown) + r" \\")
    # f. 80r, right: the days of the months and the increment of the lot of the revolution
    rate = 30 * 169 * 1440 / YEAR                                                 # degrees a day
    rows_b, notes_b = [], []
    for n in range(1, 29):
        r = n + 2
        (dv, ds), (gv, gs), (mv, ms) = (number(t1[(r, c)]) for c in (8, 7, 6))
        want = n * rate * 60
        wd, wm = int(round(want) // 60 % 360), int(round(want) % 60)
        bad_d = dv != n
        if gv is None:                                                            # no degrees: the minutes alone
            d = (mv - want) % 60 if mv is not None else 0
            bad_g = min(d, 60 - d) > 2.5
        else:
            bad_g = abs((gv * 60 + (mv or 0) - want + 10800) % 21600 - 10800) > 2.5
        raw_g = t1[(r, 7)].strip("{} ")
        if " " in raw_g:                                    # letters apart: read one by one, not added up
            gs, bad_g = " ".join(str(number(g)[0]) for g in raw_g.split()) + " (?)", True
            notes_b.append(f"day {n}: the degrees read {raw_g}, {gs.replace(' (?)', '')} letter by letter, where "
                           f"the computation gives {wd}° {wm}′")
        elif bad_g:
            doubt = " (?)" if "(?)" in gs + ms else ""
            notes_b.append(f"day {n}: {gs.replace(' (?)', '')}° {ms.replace(' (?)', '')}′{doubt}, where the "
                           f"computation gives {wd}° {wm}′")
        rows_b.append(" & ".join([ds + ("†" if bad_d else ""), gs + ("†" if bad_g and gv is not None else ""),
                                  ms + ("†" if bad_g and gv is None else "")]) + r" \\")
    groups = " ".join(str(number(g)[0]) for g in t1[(31, 8)].strip("{} ").split()) + " (?)"   # read letter by letter
    rows_b.append(" & ".join([groups] + [number(t1[(31, c)])[1] for c in (7, 6)]) + r" \\")
    rows_b.append(" & ".join(number(t1[(32, c)])[1] for c in (8, 7, 6)) + r" \\")

    # f. 80v: the triplicities, the faces and the terms
    def planet(cell):
        doubt = "{" in cell
        names = [en["planet:" + ch] for ch in re.findall(r"[؀-ۿ]", cell)]
        return " / ".join(names) + (" (?)" if doubt else "")
    the = lambda p: "the " + p.lower() if p in ("Sun", "Moon") else p               # noqa: E731
    rows_c, trip_notes, term_notes, faces_ok = [], [], [], 0
    for i in range(12):
        r = 2 * i + 2
        sign = en["sign:" + t2[(r, 14)].strip()]
        trip = [planet(t2[(r, c)]) for c in (3, 2, 1)]
        face = [planet(t2[(r, c)]) for c in (7, 6, 5)]
        terms = [f"{planet(t2[(r, c)])} {number(t2[(r + 1, c)])[1]}" for c in (13, 12, 11, 10, 9)]
        if sign != SIGNS[i]:
            errors.append(f"80v row {r}: sign {sign}, expected {SIGNS[i]}")
        for k, (got, want) in enumerate(zip(trip, TRIANGLE[i % 4])):
            if got.replace(" (?)", "") != want:
                trip_notes.append(f"in {sign} the table has {the(got)} in the {['first', 'second', 'third'][k]} "
                                  f"place, where Ptolemy has {the(want)}")
        faces_ok += [x.replace(" (?)", "") for x in face] == [HOUSE[SIGNS[(i + 4 * k) % 12]] for k in range(3)]
        if terms != TERMS[sign]:
            term_notes.append(f"in {sign} the table has {', '.join(terms)}, and Robbins's table "
                              f"{', '.join(TERMS[sign])}")
        rows_c.append(" & ".join([sign, ", ".join(trip), ", ".join(face), ", ".join(terms)]) + r" \\")
    if faces_ok != 12:
        errors.append(f"80v: the faces follow the triplicities in {faces_ok} of 12 signs")

    def notes(items):
        return "".join(r"\item " + inline(x) for x in items)

    def differs(items, what):
        return (f" A number marked † differs from {what}: " + "; ".join(items) + ".") if items else \
            f" Every number agrees with {what}."
    count = {0: "every sign", 1: "every sign but one", 2: "every sign but two"}
    note_a = [
        "The months of the revolution divide the year of the revolution of the *Zīj*, 365 days 5 hours 46 minutes "
        "24 seconds (chapter 53), into thirteen months of 28 days 2 hours 17 minutes 25 seconds; the fractions "
        "are minutes of an hour." + differs(notes_a, "that computation")]
    note_b = [
        "The days of the months give the place of the day of chapter 39: thirty degrees, one sign, for each "
        "thirteenth of a month, 2 days 3 hours 52 minutes, which makes 13° 52′ 53″ a day; the degrees are "
        "counted round the whole circle. PAL notes that the table gives multiples of about 13;52,54,30° a day, "
        "that its scribal mistakes are not corrected, and that J. Chabás and B. R. Goldstein, *A Survey of "
        "European Astronomical Tables in the Late Middle Ages* (Leiden: Brill, 2012), pp. 100 and 221, publish a "
        "copy with different errors." + differs(notes_b, "the computation by more than two minutes") +
        " A dash stands for an empty cell.",
        "The last two rows are not clear in the transcription. The first has {كا مز كح} in the column of the days, "
        "given here letter by letter, and 30 degrees, which is where the increment stands at the end of a month of "
        "the revolution, 28 days 2 hours 17 minutes: thirteen signs, 30° beyond the whole circle. The second has 0 "
        "degrees and 0 minutes."]
    note_c = [
        "The letters of the table stand for the planets: ل Saturn, ي Jupiter, خ Mars, س the sun, ة Venus, د "
        "Mercury, ر the moon. The lords of the triplicities are those of Ptolemy's four triangles (*Tetrabiblos* "
        "I.18): the lord by day, the lord by night, and the planet that Ptolemy joins to each triangle, Mars to the "
        "fiery, Saturn to the earthy and Jupiter to the airy one; the watery triangle Mars governs by day and by "
        "night, with Venus by day and the moon by night." +
        "".join(" " + x[0].upper() + x[1:] + "." for x in trip_notes),
        "Ptolemy's work has no faces of this kind. In every sign the table gives the three faces to the lords of "
        "the three signs of its triplicity, in the order of the signs and beginning with its own lord (Aries: "
        "Mars, the sun, Jupiter); the astrological figure of the *Zīj* has the Chaldean faces (Aries: Mars, the "
        "sun, Venus).",
        f"The terms agree with Ptolemy's, as Robbins tabulates them (I.21), in {count.get(len(term_notes), 'most signs')}"
        "; Robbins prints Saturn for Mars as the last lord of Libra." +
        "".join(" " + x[0].upper() + x[1:] + "." for x in term_notes)]

    out = [r"\ChapterHead{[The tables]}{T}{\Fol{80r}}{}",
           r"\begin{center}\footnotesize",
           r"\begin{minipage}[t]{0.47\textwidth}\centering",
           r"\begin{tabular}[t]{@{}>{\raggedright}p{16mm}>{\raggedright}p{14mm}>{\raggedright}p{12mm}>{\raggedright\arraybackslash}p{13mm}@{}}",
           " & ".join(E(f"80r:R1C{c}") for c in (4, 3, 2, 1)) + r" \\",
           " & ".join(r"\emph{" + E(f"80r:R2C{c}") + "}" for c in (4, 3, 2, 1)) + r" \\[2pt]",
           "\n".join(rows_a), r"\end{tabular}\end{minipage}\hfill",
           r"\begin{minipage}[t]{0.47\textwidth}\centering",
           r"\begin{tabular}[t]{@{}>{\raggedright}p{22mm}>{\raggedright}p{14mm}>{\raggedright\arraybackslash}p{14mm}@{}}",
           r"\multicolumn{3}{@{}p{54mm}@{}}{" + E("80r:R1C6") + r"} \\",
           " & ".join(r"\emph{" + E(f"80r:R2C{c}") + "}" for c in (8, 7, 6)) + r" \\[2pt]",
           "\n".join(rows_b), r"\end{tabular}\end{minipage}", r"\end{center}",
           r"\begin{itemize}\footnotesize" + notes(note_a + note_b) + r"\end{itemize}",
           r"\clearpage\noindent\Fol{80v}{\footnotesize",
           r"\begin{longtable}{@{}>{\raggedright}p{19mm}>{\raggedright}p{30mm}>{\raggedright}p{30mm}>{\raggedright\arraybackslash}p{60mm}@{}}",
           " & ".join(E(f"80v:R1C{c}") for c in (14, 1, 5, 9)) + r" \\[2pt]\endhead",
           "\n".join(rows_c), r"\end{longtable}}",
           r"\begin{itemize}\footnotesize" + notes(note_c) + r"\end{itemize}"]
    return "\n".join(out)


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
    tables = table_tex(errors)
    if errors:
        for e in errors:
            print("ERROR", e)
        raise SystemExit(1)
    body.append(tables)
    for fol, tab in (("80r", "AB03-F080r-T01"), ("80v", "AB03-F080v-T01")):
        align.append((f"EN-T{fol}", "", "table", tab, tab, fol, 0))
    done_all = chapters == list(range(41))
    done = ("This version holds the whole commentary and its two tables" if done_all else
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

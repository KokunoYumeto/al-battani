"""English labels for the redrawn figures of Nallino's commentary: copies in EN/nallino/figures/ with the Latin words
of the labels in English (only lines that set a node; comments untouched)."""
import re
import sys
from pathlib import Path

B = Path(__file__).resolve().parents[3]
OUT = B / "EN" / "nallino" / "figures"
OUT.mkdir(exist_ok=True)
WORDS = [(r"\bumbra cxtensa\b", "horizontal shadow"), (r"\bumbra crecta\b", "vertical shadow"),
         (r"\baequator\b", "equator"), (r"\bPolus\b", "Pole"), (r"\becliptica\b", "ecliptic"),
         (r"\bConus\b", "Cone"), (r"\bumbrae\b", "of the shadow"), (r"\bTerra\b", "Earth"),
         (r"\bmane\b", "morning"), (r"\bvesper\b", "evening"), (r"\bmeridianus\b", "meridian")]
# words set letter by letter along a curve: each Latin letter node takes the English letter at its place
LETTERS = {"AB01-PDF0337-F01": dict(zip("domus", "house"))}   # «X domus» … «III domus» → «X house» …
# words set letter by letter whose English is the Latin word less some letters: those letters' nodes are left out
DROP = {"AB01-PDF0347-F01": [("ecliptica", "ecliptic"), ("meridianus", "meridian")],
        "AB01-PDF0348-F01": [("ecliptica", "ecliptic"), ("aequator", "equator")],
        "AB01-PDF0404-F01": [("ecliptica", "ecliptic"), ("aequator", "equator")],
        "AB01-PDF0405-F01": [("ecliptica", "ecliptic"), ("aequator", "equator")]}


# words set letter by letter whose English has as many letters: the letters are replaced one for one, in order
SEQ = {"AB01-PDF0364-F02": [("umbraTerrae", "Earthshadow")], "AB01-PDF0365-F01": [("umbraTerrae", "Earthshadow")]}


def height(c):
    """the height of a letter in ems, roughly: capitals, ascenders, t, i and the x-height letters"""
    return 0.66 if c.isupper() else 0.70 if c in "bdfhkl" else 0.58 if c == "t" else 0.65 if c == "i" else 0.44


def letter_nodes(lines):
    return [(i, m.group(1)) for i, line in enumerate(lines)
            if not line.startswith("%") and (m := re.search(r"\{(\S)\}\};\s*(%.*)?$", line))]


def replace_letters(lines, pairs):
    """the lines with the letter nodes of a Latin word replaced, in order, by those of the English word"""
    one, lines = letter_nodes(lines), list(lines)
    for latin, english in pairs:
        for k in range(len(one) - len(latin) + 1):
            if "".join(c for _, c in one[k:k + len(latin)]) == latin:
                for (i, c), e in zip(one[k:k + len(latin)], english):
                    if c != e:   # the English letter takes the printed letter's size: its height scales by letter class
                        new = re.sub(r"\{" + re.escape(c) + r"\}\};", "{" + e + "}};", lines[i])
                        lines[i] = re.sub(r"\\resizebox\{[^{}]*\}\{([\d.]+)pt\}",
                                          lambda m: r"\resizebox{!}{%.2fpt}" % (float(m.group(1)) * height(e) / height(c)),
                                          new)
                break
        else:
            raise SystemExit(f"{latin} not found")
    return lines


def drop_letters(lines, pairs):
    """the lines without the letter nodes that the English word does not keep"""
    one = [(i, m.group(1)) for i, line in enumerate(lines)
           if not line.startswith("%") and (m := re.search(r"\{(\S)\}\};\s*(%.*)?$", line))]
    drop = set()
    for latin, english in pairs:
        for k in range(len(one) - len(latin) + 1):
            if "".join(c for _, c in one[k:k + len(latin)]) == latin:
                j = 0
                for i, c in one[k:k + len(latin)]:
                    if j < len(english) and c == english[j]:
                        j += 1
                    else:
                        drop.add(i)
                break
        else:
            raise SystemExit(f"{latin} not found")
    return [line for i, line in enumerate(lines) if i not in drop]


# the figures of the notes on the tables (S07/adnotationes/figures). The wheel of p. 299: the planets and the signs in
# English; «Inpiter», «Iupitor», «Venns» and «Verus» are misprints of the print for Iupiter and Venus.
WHEEL = {"AB01-PDF0748-F01": [(r"\bSaturnus\b", "Saturn"), (r"\b(?:Iupiter|Inpiter|Iupitor)\b", "Jupiter"),
                              (r"\bMercurius\b", "Mercury"), (r"\b(?:Verus|Venns)\b", "Venus"), (r"\bSol\b", "Sun"),
                              (r"\bLuna\b", "Moon"), (r"\bScorpius\b", "Scorpio"), (r"\bCapricornus\b", "Capricorn"),
                              # the box of the wheel is 430 pt wide, the English text 426.8 pt: it loses some of the
                              # white at its sides (the names of the signs end within 206 pt of the centre)
                              (r"^\\path \(-215,-214\.75\) rectangle \(215,215\.01\);",
                               r"\\path (-213.3,-214.75) rectangle (213.3,215.01);")]}
# the heads of the spurious tables (pp. 300-307): each Latin label, as the node sets it, and its English. An English
# label wider than its place (between the rules about it, or the width of the Latin where that is more) is set in a
# smaller size that fits.
MONTHS = dict(zip("Ianuarius Februarius Martius Aprilis Maius Iunius Iulius Augustus".split(),
                  "January February March April May June July August".split()))
HEADS = {
    "AB01-PDF0749-F01": {
        "Tabula ad invenienda signa initiorum annorum et mensium Arabum.":
            "Table for finding the signs of the beginnings of the Arab years and months.",
        "Ex opere astronomico Maslamae.": "From the astronomical work of Maslama.",
        "Anni Arabum collecti": "Collected Arab years", "[ab aera] per decades.": "[from the era] by decades.",
        "Signa decadum.": "Signs of the decades.", "Singuli Arabum anni.": "Single Arab years.",
        "Numerus dierum": "Number of days", "[singulorum] mensium.": "of the [single] months.",
        "Nomina mensium.": "Names of the months.", "Eorum signa.": "Their signs."},
    "AB01-PDF0750-F01": {
        "Tabula signorum Arabum.": "Table of the signs of the Arabs.", "[Anni] collecti.": "Collected [years].",
        "[Anni] singuli.": "Single [years].", "Numerus": "Number", "[annorum].": "[of years].", "Signa.": "Signs.",
        "Menses.": "Months.", "Tabula signorum Persarum.": "Table of the signs of the Persians.",
        "Ex opere astronomico Maslamae.": "From the astronomical work of Maslama.", "Nomina mensium": "Names of the",
        "Persicorum.": "Persian months.", r"\textarabic{علامات} Signa.": r"\textarabic{علامات} Signs."},
    "AB01-PDF0751-F01": {
        "Tabula signorum Syrorum, intercalatione mense Decembri posita":
            "Table of the signs of the Syrians, with the intercalation put",
        "secundum methodum Romanorum.": "in the month of December, according to the method of the Romans.",
        "Numerus annorum.": "Number of years.", "Columna intercalationis.": "Column of the intercalation.",
        "31 dies": "31 days", **{m + ".": MONTHS[m] + "." for m in MONTHS}},
    "AB01-PDF0752-F01": {
        "Tabula ad cognoscenda initia annorum et mensium Coptorum;":
            "Table for knowing the beginnings of the years and months",
        "et est intercalatio in fine anni.": "of the Copts; and the intercalation is at the end of the year.",
        "Numeri [annorum].": "Numbers [of the years].", "Bisextiles.": "Leap years."},
    "AB01-PDF0753-F01": {
        "Tabula conversionis aerarum in alias, secundum annos Arabicos collectos.":
            "Table for converting the eras into one another, by the collected Arab years.",
        "Anni Arabum collecti [ab aera].": "Collected Arab years [from the era].", "Anni.": "Years.",
        "Menses.": "Months.", "Dies.": "Days.", "Fraction.": "Fract."},
    "AB01-PDF0754-F01": {
        "Tabula conversionis aerarum in alias, secundum singulos Arabum annos":
            "Table for converting the eras into one another,",
        "et menses.": "by the single Arab years and months.", "Anni Arabum singuli.": "Single Arab years.",
        "Bisextiles Arabum.": "Arab leap years.", "Anni singuli Syrorum": "Single years of the Syrians",
        "cum intercalatione.": "with intercalation.", "Anni singuli Persarum": "Single years of the Persians",
        "sine intercalatione.": "without intercalation.", "Anni.": "Years.", "Menses.": "Months.", "Dies.": "Days.",
        "Fract.": "Fract.", "Menses [harum aerarum].": "Months [of these eras]."},
    "AB01-PDF0755-F01": {
        "Tabula coniunctionum Solis et Lunae in annis Arabicis collectis.":
            "Table of the conjunctions of Sun and Moon in the collected Arab years.",
        "Anni Arabici collecti": "Collected Arab years", "[ab aera].": "[from the era].",
        "Dies incrementi": "Days of the increment", "supra aeram.": "over the era.",
        "Amborum luminarium": "Mean motion of", "motus medius.": "both luminaries.",
        "Anomalia Lunae.": "Anomaly of the Moon.", "Motus latitudinis.": "Motion in latitude.", "Dies.": "Days.",
        "Horae.": "Hours.", "Minuta.": "Minutes.", "Signa": "Zodiacal", "zodiaci.": "signs.",
        "Gradus.": "Degrees.", "Min.": "Min.", "Sec.": "Sec."},
}
HEADS["AB01-PDF0756-F01"] = {**HEADS["AB01-PDF0755-F01"], "Anni Arabum collecti": "Collected Arab years",
                             "Tabula oppositionum Solis et Lunae in annis Arabicis collectis.":
                                 "Table of the oppositions of Sun and Moon in the collected Arab years."}
# a printed block of several justified lines (one node a line or a piece of a line): its first and last Latin pieces
# and the English, set again as one justified paragraph of the block's width (to the right end of its widest line,
# or to the rule on its right less 0.6 mm), with the indent or the hanging first line of the print; a fourth item
# "ragged" sets it ragged right (a narrow column)
BLOCKS = {
    "AB01-PDF0751-F01": [("Columnae", "multipli",
                          "Columns of [the numbers] to be subtracted, [which are] multiples of 28", "ragged")],
    "AB01-PDF0753-F01": [
        ("Anni Romanorum, intercala-", "9 m., 17 d., 0 fract.",
         "Roman years, with intercalation, converted by the hijra years. Epoch, before the hijra: "
         "932~y., 9~m., 17~d., 0~fract."),
        ("Anni Coptorum, intercalatio-", "19 d., 45 fract.",
         "Coptic years, with intercalation, converted by the hijra years. Epoch, before the hijra: "
         "337~y., 10~m., 19~d., 45~fract."),
        ("Anni Persarum, sine", "p. heg., 9 a., 11 m., 9 d.",
         "Persian years, without intercalation, converted by the hijra years. Epoch, after the hijra: "
         "9~y., 11~m., 9~d.")],
    "AB01-PDF0754-F01": [("Menses Arabum,", "serviunt.",
                          "The months of the Arabs, which serve [the conversions] of all these eras.")],
}
NODE = re.compile(r"^\\node\[(?P<opt>[^\]]*)\] at \((?P<x>-?[\d.]+),(?P<y>-?[\d.]+)\) \{\\fontsize\{(?P<fs>[\d.]+)\}"
                  r"\{(?P<ls>[\d.]+)\}\\selectfont(?P<bf>\\bfseries)? ?(?P<text>.*)\};\s*$")
RECT = re.compile(r"^\\fill \((-?[\d.]+),(-?[\d.]+)\) rectangle \((-?[\d.]+),(-?[\d.]+)\);")
_METRICS = {}


def text_mm(text, bold, size):
    """the width in mm of a label in Linux Libertine (the font of the figures) at a size in pt"""
    import subprocess
    from fontTools.ttLib import TTFont
    name = "LinLibertine_RB.otf" if bold else "LinLibertine_R.otf"
    if name not in _METRICS:   # the font of the TeX installation
        f = TTFont(subprocess.run(["kpsewhich", name], capture_output=True, text=True, check=True).stdout.strip())
        _METRICS[name] = (f.getBestCmap(), f["hmtx"].metrics, f["head"].unitsPerEm)
    cmap, hm, upm = _METRICS[name]
    text = re.sub(r"\\textarabic\{[^{}]*\}", "", text).replace("~", " ")   # the Arabic of a label is not changed
    return sum(hm[cmap[ord(c)]][0] for c in text if ord(c) in cmap) / upm * size * 25.4 / 72.27


def rules(lines):
    """the rules of a table head: vertical ones as (x0, x1, ylow, yhigh), horizontal ones as (y0, y1, xlow, xhigh)"""
    vert, hor = [], []
    for line in lines:
        m = RECT.match(line)
        if m:
            x0, y0, x1, y1 = (float(v) for v in m.groups())
            x0, x1, y0, y1 = min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1)
            if x1 - x0 < 1 < y1 - y0:
                vert.append((x0, x1, y0, y1))
            elif y1 - y0 < 1 < x1 - x0:
                hor.append((y0, y1, x0, x1))
    return vert, hor


def room(m, vert, hor, nodes):
    """the room of a label in mm along its line: between the rules about it (0.5 mm kept free at each end), and, for
    a centred label, up to the midpoints between it and the labels beside it on its line (0.3 mm kept free)"""
    x, y = float(m["x"]), float(m["y"])
    if "rotate=90" in m["opt"]:
        above = min((y0 for y0, y1, a, b in hor if a <= x <= b and y0 > y), default=y + 99)
        below = max((y1 for y0, y1, a, b in hor if a <= x <= b and y1 < y), default=y - 99)
        near = min((abs(float(n["y"]) - y) for n in nodes if n is not m and "rotate=90" in n["opt"]
                    and abs(float(n["x"]) - x) < 2.2), default=999)
        return min(2 * min(above - y, y - below) - 1.0, near - 0.6)
    left = max((x1 for x0, x1, a, b in vert if a <= y <= b and x1 < x), default=x - 99)
    right = min((x0 for x0, x1, a, b in vert if a <= y <= b and x0 > x), default=x + 99)
    if "base west" in m["opt"]:
        return right - x - 0.5
    near = min((abs(float(n["x"]) - x) for n in nodes if n is not m and "rotate" not in n["opt"]
                and abs(float(n["y"]) - y) < 2.2 and float(n["x"]) != x), default=999)
    return min(2 * min(x - left, right - x) - 1.0, near - 0.6)


def relabel(lines, labels):
    """each node whose label is a key of labels takes the English, in a smaller size if it would not fit"""
    vert, hor = rules(lines)
    nodes = [m for line in lines if not line.startswith("%") and (m := NODE.match(line))]
    out = []
    for line in lines:
        m = NODE.match(line)
        if line.startswith("%") or not m or m["text"] not in labels:
            out.append(line)
            continue
        m = next(n for n in nodes if n.string == line)
        en, fs, ls, bold = labels[m["text"]], float(m["fs"]), float(m["ls"]), bool(m["bf"])
        # a label of a head of two lines may be as wide as the wider of the two Latin lines
        fit = max([room(m, vert, hor, nodes)] + [text_mm(n["text"], bool(n["bf"]), float(n["fs"])) for n in nodes
                                                if n is m or (n["x"] == m["x"] and n["opt"] == m["opt"]
                                                              and "textarabic" not in n["text"])])
        k = min(1.0, fit / text_mm(en, bold, fs))
        if k < 0.8:
            raise SystemExit(f"{en}: too wide for its place ({k:.2f})")
        if k < 0.97:
            print(f"  {en}: set at {k:.2f} of the printed size")
        out.append(line[:m.start("fs")] + f"{fs * k:.2f}".rstrip("0").rstrip(".") + "}{"
                   + f"{ls * k:.2f}".rstrip("0").rstrip(".") + "}" + line[m.end("ls") + 1:m.start("text")] + en
                   + line[m.end("text"):])
    return out


def bare(text):
    """a label without the \\makebox[W][s] that stretches a justified line to its printed width"""
    m = re.match(r"\\makebox\[[\d.]+mm\]\[s\]\{(.*)\}$", text)
    return m.group(1) if m else text


def reblock(lines, blocks):
    """each block of justified lines set again as one paragraph in English (see BLOCKS); a block ends with the line
    of its last piece (a piece on the same baseline after it belongs to it)"""
    vert, _ = rules(lines)
    for first, last, en, *how in blocks:
        idx = [i for i, line in enumerate(lines) if (m := NODE.match(line)) and bare(m["text"]) == first]
        jdx = [i for i, line in enumerate(lines) if (m := NODE.match(line)) and bare(m["text"]) == last]
        if len(idx) != 1 or len(jdx) != 1 or jdx[0] < idx[0]:
            raise SystemExit(f"block {first} .. {last} not found")
        j = jdx[0]
        while j + 1 < len(lines) and (m := NODE.match(lines[j + 1])) and m["y"] == NODE.match(lines[j])["y"]:
            j += 1
        nodes = [NODE.match(line) for line in lines[idx[0]:j + 1]]
        y0 = float(nodes[0]["y"])
        firsts = [float(n["x"]) for n in nodes if float(n["y"]) == y0]
        rest = [float(n["x"]) for n in nodes if float(n["y"]) != y0]
        ys = sorted({float(n["y"]) for n in nodes}, reverse=True)
        skip = (ys[0] - ys[-1]) / (len(ys) - 1) * 72.27 / 25.4
        left, x_first = min(firsts + rest), min(firsts)
        boxes = [float(n["x"]) + float(b.group(1)) for n in nodes if (b := re.match(r"\\makebox\[([\d.]+)mm\]", n["text"]))]
        right = max(boxes) if boxes else min(x0 for x0, x1, a, b in vert if a <= y0 <= b and x0 > x_first) - 0.6
        ind = x_first - min(rest)
        start = (r"\hangindent=" + f"{-ind:.3f}" + r"mm\hangafter=1 ") if ind < 0 else (r"\hspace*{" + f"{ind:.3f}" + "mm}")
        n0 = nodes[0]
        par = (r"\node[anchor=base west] at (" + f"{left:.3f},{y0:.3f}" + r") {\parbox[t]{" + f"{right - left:.3f}"
               + r"mm}{\fontsize{" + n0["fs"] + "}{" + f"{skip:.2f}" + r"}\selectfont" + (n0["bf"] or "")
               + (r"\raggedright " if how == ["ragged"] else r"\tolerance=9999\emergencystretch=1em ") + start + en
               + "}};\n")
        lines = lines[:idx[0]] + [par] + lines[j + 1:]
    return lines


made = []
for f in sorted((B / "S07" / "adnotationes" / "figures").glob("*.tex")):
    if f.stem not in WHEEL and f.stem not in HEADS:
        continue
    lines = f.read_text(encoding="utf-8").splitlines(keepends=True)
    if f.stem in WHEEL:
        for a, b in WHEEL[f.stem]:
            lines = [line if line.startswith("%") else re.sub(a, b, line) for line in lines]
    if f.stem in BLOCKS:
        lines = reblock(lines, BLOCKS[f.stem])
    if f.stem in HEADS:
        lines = relabel(lines, HEADS[f.stem])
    head = "% The English labels of this figure; otherwise the figure of S07/adnotationes/figures as redrawn there.\n"
    (OUT / f.name).write_text(head + "".join(lines), encoding="utf-8", newline="\n")
    made.append(f.stem)
for d in ("S03", "S04"):
    for f in sorted((B / d / "versio" / "figures").glob("*.tex")):
        if int(f.stem[8:12]) < 240:
            continue
        lines, changed = [], False
        for line in f.read_text(encoding="utf-8").splitlines(keepends=True):
            if not line.startswith("%") and "\\node" in line:
                new = line
                for a, b in WORDS:
                    new = re.sub(a, b, new)
                if f.stem in LETTERS:
                    new = re.sub(r"\{([a-z])\}\};", lambda m: "{" + LETTERS[f.stem].get(m.group(1), m.group(1)) + "}};", new)
                if new != line:      # a relabelled node keeps the printed height and takes the English word's width
                    new = re.sub(r"\\resizebox\{[^{}]*\}\{([^{}]*)\}", r"\\resizebox{!}{\1}", new)
                changed |= new != line
                line = new
            lines.append(line)
        if f.stem in DROP:
            lines, changed = drop_letters(lines, DROP[f.stem]), True
        if f.stem in SEQ:
            lines, changed = replace_letters(lines, SEQ[f.stem]), True
        if changed:
            head = f"% The English labels of this figure; otherwise the figure of {d}/versio/figures as redrawn there.\n"
            (OUT / f.name).write_text(head + "".join(lines), encoding="utf-8", newline="\n")
            made.append(f.stem)
print(len(made), " ".join(made))

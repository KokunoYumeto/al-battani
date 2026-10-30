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


made = []
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

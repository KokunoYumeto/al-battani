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
                if new != line:      # a relabelled node keeps the printed height and takes the English word's width
                    new = re.sub(r"\\resizebox\{[^{}]*\}\{([^{}]*)\}", r"\\resizebox{!}{\1}", new)
                changed |= new != line
                line = new
            lines.append(line)
        if changed:
            head = f"% The English labels of this figure; otherwise the figure of {d}/versio/figures as redrawn there.\n"
            (OUT / f.name).write_text(head + "".join(lines), encoding="utf-8", newline="\n")
            made.append(f.stem)
print(len(made), " ".join(made))

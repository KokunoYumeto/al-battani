"""The Latin of a unit (or of a range of lines) in reading order, for translating and checking: one line per printed
line with its short anchor (0242b004: master page 242, body, line 4; nl, nr, n: the footnote columns), and after
each page the observations of its page record and the figures it sets.
python tools/latin.py UNIT | FIRST..LAST"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import build_nallino as bn  # noqa: E402

SHORT = {v: k for k, v in bn.SEC.items()}


def short(a):
    m = re.fullmatch(r"AB01-PDF(\d{4})-(\w+)-L(\d{3})", a)
    return f"{m.group(1)}{SHORT.get(m.group(2), m.group(2))}{m.group(3)}" if m else a


def page_notes(pdf):
    for d in bn.SOURCES.values():
        f = d / "pages" / f"AB01-PDF{pdf:04d}.txt"
        if f.exists():
            out = []
            for line in f.read_text(encoding="utf-8").splitlines():
                if line.startswith("@obs "):
                    out.append("  obs: " + line[5:])
                m = re.match(r"@(?:wrap|wrapr) \S+ (\S+)|@figc (\S+)", line)
                if m:
                    out.append("  figure: " + (m.group(1) or m.group(2)))
            return out
    return []


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rows, where = bn.load_sources()
    arg = sys.argv[1]
    if ".." in arg or "+" in arg:
        spec = arg
    else:
        spec = next(u["lines"] for u in bn.read_tsv(bn.HERE / "units.tsv") if u["unit"] == arg)
    idx = [x for a, z in bn.ranges_of(spec) for x in range(where[a], where[z] + 1)]
    pdf = None
    for x in idx:
        r = rows[x]
        if r["pdf"] != pdf:
            if pdf is not None:
                print("\n".join(page_notes(pdf)))
            pdf = r["pdf"]
            print(f"== PDF {pdf} = p. {r['page']}")
        print(f"{short(r['anchor'])}\t{r['text']}")
    if pdf is not None:
        print("\n".join(page_notes(pdf)))


if __name__ == "__main__":
    main()

"""Check the conversion against PAL's files, independently of the builder: for every page side, the text of PAL's
file (its characters outside the notes, the Berlin folio marks written /B1r/, the line breaks of the manuscript at
PAL's «||») is compared, line by line and up to runs of white space, with the lines of anchors.tsv; PAL's notes are
compared with apparatus.tsv, and the cells of the two tables with tables/*.tsv. Any difference is printed.
python check_conversion.py"""
import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def strip_notes(s):
    return re.sub(r'<span class="note">.*?</small></span>', "", s, flags=re.S)


def pal_lines(s):
    s = strip_notes(s)
    s = re.sub(r"<table.*?</table>", "", s, flags=re.S)
    s = s.replace('<span data-prae="||"></span>', "\u0001")
    s = re.sub(r'<span data-prae="(/B?\d+[rv]/)"></span>', r"\1", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = (s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'"))
    parts = [re.sub(r"\s+", " ", x).strip() for x in s.split("\u0001")]
    if parts and not parts[-1]:
        parts.pop()
    return parts


def squash(s):
    return re.sub(r"\s+", "", s)


def main():
    with open(HERE / "anchors.tsv", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    ours = {}
    for r in rows:
        ours.setdefault(r["folio"], []).append(r["text"])
    with open(HERE / "apparatus.tsv", encoding="utf-8") as fh:
        app = {r["pal_number"]: r["text"] for r in csv.DictReader(fh, delimiter="\t")}
    bad = lines = notes = 0
    for p in sorted((HERE / "source" / "pages").glob("1#*.xml")):
        fol = re.search(r"#(\d+[rv])", p.name).group(1)
        s = p.read_text(encoding="utf-8")
        pal = pal_lines(s)
        mine = ours.get(fol, [])
        if len(pal) != len(mine):
            print(f"{fol}: {len(pal)} lines in PAL, {len(mine)} in the edition")
            bad += 1
        for k, (a, b) in enumerate(zip(pal, mine), 1):
            lines += 1
            if squash(a) != squash(b):
                print(f"{fol} L{k:02d}: PAL «{a[:80]}» / edition «{b[:80]}»")
                bad += 1
        for m in re.finditer(r'<small data-prae="(\d+)" dir="ltr" id="n\d+">(.*?)</small></span>', s, flags=re.S):
            notes += 1
            t = re.sub(r"<span data-prae=\"//\"></span>", "//", m.group(2))
            t = re.sub(r"<[^>]+>", "", t).replace("&amp;", "&")
            if squash(t) != squash(app.get(m.group(1), "")):
                print(f"{fol} note {m.group(1)}: PAL «{t.strip()[:80]}» / edition «{app.get(m.group(1), '')[:80]}»")
                bad += 1
        for t_i, tm in enumerate(re.finditer(r"<table.*?</table>", s, flags=re.S), 1):
            pal_cells = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", strip_notes(c))).strip()
                         for c in re.findall(r"<td[^>]*>(.*?)</td>", tm.group(0), flags=re.S)]
            with open(HERE / "tables" / f"AB03-F{int(fol[:-1]):03d}{fol[-1]}-T{t_i:02d}.tsv", encoding="utf-8") as fh:
                mine_cells = [r["text"] for r in csv.DictReader(fh, delimiter="\t")]
            # the edition writes the lines of a cell joined with « / »
            if [squash(c) for c in pal_cells] != [squash(c.replace(" / ", " ")) for c in mine_cells]:
                print(f"{fol} table {t_i}: the cells differ")
                bad += 1
    print(f"{lines} lines and {notes} notes compared; differences: {bad}")


if __name__ == "__main__":
    main()

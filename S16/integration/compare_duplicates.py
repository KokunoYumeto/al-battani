"""S16 - the twelve master pages that two sessions transcribed (coverage_ab01.tsv, «second transcription»): the
table and figure pages inside Nallino's notes (Part II pp. 219-220, 297, 299, 300-307), transcribed by S07 with the
notes and by S06 or S13 with the tables. The canonical transcription is the table session's; S07's is a second,
independent reading. This compares the numbers of the two, page by page, as multisets (the order of reading a table
differs between the two layouts), and writes duplicates_compared.tsv. No production file is changed.
python compare_duplicates.py"""
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

AB = Path(__file__).resolve().parents[2]
csv.field_size_limit(10 ** 8)
NUM = re.compile(r"\d+")


def tsv(path):
    with open(AB / path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def s07_numbers(pdf, sections=("body",)):
    """the numbers of S07's lines of the page, without the folio line (f. 241,r.) and the title block"""
    j = json.loads((AB / f"S07/adnotationes/records/AB01-PDF{pdf:04d}.json").read_text(encoding="utf-8"))
    nums = []
    for s in j["sections"]:
        if s["role"] not in sections:
            continue
        for ln in s["lines"]:
            t = ln.get("transcription") or ""
            if re.fullmatch(r"\s*f(ol)?\.\s*\d+\s*,\s*[rv]\.\s*", t, re.I):
                continue
            if re.fullmatch(r"F\d+", ln["id"].split("-")[-1]):
                continue                                    # the block of the title and the column heads
            nums += NUM.findall(t)
    return Counter(nums)


def main():
    out = []
    # the spurious tables (S06), pp. 300-307
    sp = tsv("S06/spurious/spurious_p2.tsv")
    for pdf in range(749, 757):
        a, seen = Counter(), set()
        for r in sp:
            if r["pdf"] != str(pdf):
                continue
            a.update(NUM.findall(r["value"]))
            if (r["table"], r["row"]) not in seen:          # the argument of the row, once
                seen.add((r["table"], r["row"]))
                a.update(NUM.findall(r["arg"]))
        b = s07_numbers(pdf)
        out.append((pdf, "S06/spurious", sum(a.values()), sum(b.values()), a, b))
    # the Andalusian table (S13 geography), pp. 219-220
    geo = tsv("S13/geography/geo_p2.tsv")
    notes = tsv("S13/geography/geo_p2_notes.tsv")
    for pdf in (668, 669):
        a = Counter()
        for r in geo:
            if r["pdf"] == str(pdf):
                for k in ("lon_d", "lon_m", "lat_d", "lat_m", "extra"):
                    a.update(NUM.findall(r[k]))
        for r in notes:                                     # the column of Nallino's notes beside the table
            if r["pdf"] == str(pdf):
                a.update(NUM.findall(r["text"]))
        b = s07_numbers(pdf, ("body", "notes_left", "notes_right"))
        out.append((pdf, "S13/geography", sum(a.values()), sum(b.values()), a, b))
    with open(Path(__file__).with_name("duplicates_compared.tsv"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("master_pdf_page\tcanonical\tnumbers_canonical\tnumbers_S07\tonly_canonical\tonly_S07\n")
        for pdf, canon, na, nb, a, b in out:
            only_a = " ".join(sorted((a - b).elements(), key=int))
            only_b = " ".join(sorted((b - a).elements(), key=int))
            fh.write(f"{pdf}\t{canon}\t{na}\t{nb}\t{only_a}\t{only_b}\n")
            print(pdf, canon, na, nb, "| only canonical:", only_a[:120], "| only S07:", only_b[:120])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()

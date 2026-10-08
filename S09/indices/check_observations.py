"""Check the line numbers named in the observations of the page files (@obs body L5: ... «word» ...) against the
transcribed lines in anchors.tsv. For every observation that names lines and quotes words in «...», report the
quoted words that stand in none of the named lines but in another line of the same page; such a report is either a
wrong line number or a quotation of the context, to be decided on the scan. Quotations of printed forms that the
transcription does not reproduce (a broken letter, a kashida) are found nowhere and are not reported. Markup
({sp:...}, *...*, {sup:...}, {sfrac:a/b}) is removed before comparing. Usage: python check_observations.py [PDF ...]"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def plain(s):
    s = s.replace("{0}", "0")  # the zero sign of the tables
    s = re.sub(r"\{ov:([^{}]*)\}", r"\1", s)
    s = re.sub(r"\{(?:sp|sc|gb|sup|sub|sm|fs|xs|ar|syr|rtl|spsc):([^}]*)\}", r"\1", s)
    s = re.sub(r"\{sfrac:([^/}]+)/([^}]+)\}", r"\1/\2", s)
    return s.replace("*", "").replace("~", "")


def main():
    with open(HERE / "anchors.tsv", encoding="utf-8") as f:
        # the lines of a raw LaTeX block continue its row of the file without a tab; they are skipped
        lines = {row["anchor"]: plain(row["transcription"]) for row in csv.DictReader(f, delimiter="\t")
                 if row["anchor"].startswith("AB01-") and row["transcription"] is not None}
    pdfs = [int(a) for a in sys.argv[1:]] or sorted(int(p.stem[-4:]) for p in (HERE / "pages").glob("AB01-PDF*.txt"))
    reports = 0
    for pdf in pdfs:
        page = f"AB01-PDF{pdf:04d}"
        for ln in (HERE / "pages" / f"{page}.txt").read_text(encoding="utf-8").splitlines():
            m = re.match(r"@obs (body|col_left|col_right|notes_left|notes_right|notes) ((?:L\d+(?:-L\d+)?(?:, )?)+):(.*)", ln)
            if not m:
                continue
            role, refs, text = m.groups()
            nums = []
            for a, b in re.findall(r"L(\d+)(?:-L(\d+))?", refs):
                nums += range(int(a), int(b or a) + 1)
            named = [lines.get(f"{page}-{role}-L{n:03d}") for n in nums]
            if None in named:
                print(f"{pdf} {role} {refs}: a named line does not exist")
                reports += 1
                continue
            for q in re.findall(r"«([^»]+)»", text):
                q = plain(q)
                if len(q) < 2 or any(q in t for t in named):
                    continue
                found = [k[len(page) + 1:] for k, t in lines.items() if k.startswith(page + "-") and q in t]
                if found:
                    print(f"{pdf} {role} {refs}: «{q}» stands in {', '.join(found)}")
                    reports += 1
    print("reports:", reports)


if __name__ == "__main__":
    main()

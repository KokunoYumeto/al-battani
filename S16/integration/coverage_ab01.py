"""S16 - the coverage of AB01 (Nallino's edition, master PDF 1-1162): every claim that a session makes on a master
page, read from that session's own ledgers and records, and one canonical disposition per page.

A claim is `edited` (the page's content is transcribed, or its figure kept) or `disposed` (a blank, binding,
provider or holding-library page recorded and kept out of the scholarly body). A page with edited claims from two
sessions is a duplicate transcription: the session that owns the content by its kind is canonical (the table and
figure sessions S06 and S13 for tables and figures; S07 for Nallino's notes), and the other is recorded as a second
transcription. Writes coverage_ab01.tsv and prints the gaps and the duplicates.
python coverage_ab01.py"""
import csv
import glob
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

AB = Path(__file__).resolve().parents[2]
csv.field_size_limit(10 ** 8)


def tsv(path):
    with open(AB / path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def p2(printed):        # Part II printed page -> master PDF page
    return printed + 449


def p3(printed):        # Part III printed page (Arabic, bound in reverse) -> master PDF page
    return 1152 - printed


def ranges(text):
    """'297 and 300–307', '19–28, 72–77 and 102–107' -> pages"""
    out = []
    for a, b in re.findall(r"(\d+)(?:[–-](\d+))?", text):
        out += list(range(int(a), int(b or a) + 1))
    return out


def main():
    claims = defaultdict(list)          # pdf -> [(session, artifact, kind, note)]

    def add(pdf, session, artifact, kind, note=""):
        claims[int(pdf)].append((session, artifact, kind, note))

    # S01: the front matter of Part I, its own page ledger (PDF 1-89)
    for r in tsv("S01/ledgers/page_disposition.tsv"):
        edited = r["owned"] == "True" and r["kind"] != "intrinsic_blank_verso"
        add(r["master_pdf_page"], "S01", "S01/ledgers/page_disposition.tsv", "edited" if edited else "disposed",
            f"{r['kind']}; {r['role']}")
    # S02: pp. 1-53 in the v009 candidate (PDF 90-142); pp. 54-109 in S02/versio (PDF 143-198)
    for r in tsv("S02/candidate_v009_print001-053/ledgers/page_disposition.tsv"):
        if r["status"] != "NOT_TRANSCRIBED":
            add(r["source_anchor"][-4:], "S02", "S02/candidate_v009_print001-053", "edited", r["status"])
    # line-anchored records (S02/versio, S03, S04, S05, S07, S09)
    for folder in ("S02/versio", "S03/versio", "S04/versio", "S05/versio", "S07/adnotationes", "S09/glossarium",
                   "S09/indices"):
        for f in sorted((AB / folder / "records").glob("AB01-PDF*.json")):
            j = json.loads(f.read_text(encoding="utf-8"))
            add(j["master_pdf_page"], folder.split("/")[0], folder, "disposed" if j.get("blank") else "edited",
                "blank page" if j.get("blank") else "")
    # page ledgers with dispositions (S05: 417-449; S09: 863-867; S10: 868-872, 1152-1162)
    for path, session in (("S05/versio/page_disposition.tsv", "S05"), ("S09/indices/page_disposition.tsv", "S09"),
                          ("S10/textus/page_disposition.tsv", "S10")):
        for r in tsv(path):
            if r["master_pdf_page"] == "873-1151":
                continue                                        # S10's summary row: the records claim these pages
            disp = r["disposition"]
            edited = disp.startswith("transcribed")
            if edited and r["master_pdf_page"].isdigit() and (
                    AB / Path(path).parent / "records" / f"AB01-PDF{int(r['master_pdf_page']):04d}.json").exists():
                continue                                        # the session's record already claims the page
            for pdf in ranges(r["master_pdf_page"]):            # a row may cover a range, e.g. 1156-1160
                add(pdf, session, path, "edited" if edited else "disposed", r["content"][:80])
    # the Arabic text: S10, S11, S12 records
    for folder in ("S10/textus", "S11/textus", "S12/textus"):
        for f in sorted((AB / folder / "records").glob("AB01-PDF*.json")):
            add(int(f.stem[-4:]), folder.split("/")[0], folder, "edited")
    # S06: the tables of Part II, each family's declared pages (README «Read» line)
    for readme in sorted(AB.glob("S06/*/README.md")):
        m = re.search(r"\[Part II pp?\. ([^,\]]+(?:, [^\]]+)?), \d+ pp?\.\]", readme.read_text(encoding="utf-8"))
        assert m, readme
        for pg in ranges(m.group(1).split(", ")[0] if False else m.group(1)):
            add(p2(pg), "S06", f"S06/{readme.parent.name}", "edited")
    # S13: the tables of Part III with their Part II versions (page ledgers), the diagrams and the notice
    for f in sorted(AB.glob("S13/*/*_p[23]_pages.tsv")) + sorted(AB.glob("S13/star_catalogue/p2_pages.tsv")):
        for r in tsv(f.relative_to(AB)):
            add(r["pdf"], "S13", f"S13/{f.parent.name}", "edited")
    for r in tsv("S13/star_catalogue/p3_stars.tsv"):         # its page ledger lists only the signed pages
        add(r["pdf"], "S13", "S13/star_catalogue", "edited")
    for pdf in (909, 908, 541, 748):                            # the two circular figures, Part III and Part II
        add(pdf, "S13", "S13/diagrams", "edited")
    for r in tsv("S13/notice/note227.tsv"):
        add(r["pdf"], "S13", "S13/notice", "edited")

    rows, gaps, dups = [], [], []
    for pdf in range(1, 1163):
        cl = claims.get(pdf, [])
        uniq = sorted({(s, a, k) for s, a, k, _ in cl})
        edited = sorted({(s, a) for s, a, k in uniq if k == "edited"})
        sessions = sorted({s for s, _ in edited})
        if not uniq:
            gaps.append(pdf)
            rows.append((pdf, "", "", "GAP", ""))
            continue
        if not edited:
            s = sorted({s for s, a, k in uniq})
            rows.append((pdf, ";".join(s), "", "disposed", "; ".join(sorted({n for *_, n in cl if n}))[:120]))
            continue
        if len(sessions) == 1:
            arts = sorted({a for _, a in edited})
            rows.append((pdf, sessions[0], ";".join(arts), "edited", "two families share the page" if len(arts) > 1
                         else ""))
            continue
        # two sessions transcribe the page: the table/figure session is canonical
        canon = [s for s in sessions if s in ("S06", "S13")]
        if len(canon) == 1:
            second = [s for s in sessions if s != canon[0]]
            arts = sorted({a for s, a in edited if s == canon[0]})
            note = "second transcription: " + ";".join(sorted({a for s, a in edited if s in second}))
            if second == ["S07"]:
                # a note of Nallino that begins on the table page belongs to S07 alone
                j = json.loads((AB / f"S07/adnotationes/records/AB01-PDF{pdf:04d}.json").read_text(encoding="utf-8"))
                heads = [ln["transcription"] for s in j["sections"] for ln in s["lines"]
                         if (ln.get("transcription") or "").startswith("*Ad pag.")]
                if heads:
                    note = ("shared page: the table is canonical in " + canon[0] + "; Nallino's note "
                            + heads[0].split("—")[0].strip("* ") + " that follows it is canonical in S07, which also "
                            "transcribes the table a second time")
                    arts.append("S07/adnotationes")
            rows.append((pdf, canon[0] if len(arts) == len(set(a.split("/")[0] for a in arts)) and "S07/adnotationes"
                         not in arts else canon[0] + "+S07", ";".join(arts), "edited", note))
            dups.append((pdf, canon[0], second))
        else:
            rows.append((pdf, ";".join(sessions), "", "OVERLAP", ""))
            dups.append((pdf, None, sessions))

    with open(Path(__file__).with_name("coverage_ab01.tsv"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("master_pdf_page\tanchor\towner\tartifact\tstate\tnote\n")
        for pdf, owner, art, state, note in rows:
            fh.write(f"{pdf}\tAB01-PDF{pdf:04d}\t{owner}\t{art}\t{state}\t{note}\n")
    n_ed = sum(1 for r in rows if r[3] == "edited")
    n_di = sum(1 for r in rows if r[3] == "disposed")
    print(f"AB01: 1162 pages; {n_ed} edited, {n_di} disposed, {len(gaps)} gaps, "
          f"{sum(1 for d in dups if d[1])} second transcriptions, {sum(1 for d in dups if not d[1])} overlaps")
    if gaps:
        print("gaps:", gaps)
    for d in dups:
        print("duplicate:", d)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()

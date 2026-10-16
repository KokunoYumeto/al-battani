"""S16 - integration of the completed sessions S01-S15 (no new source transcription). Reads the sessions' own files
and writes, beside this script:
  coverage_ab02.tsv, coverage_ab03.tsv   one disposition for every source unit of AB02 (136 PDF pages) and AB03
                                         (122 page sides), from S15's and S14's ledgers, with the files checked
  anchors_summary.tsv                    the stable anchors of every session: count, format, uniqueness, pages
  roles_map.tsv                          every role tag used in the records, mapped to the contract's roles
  works.tsv                              AB01-AB06: payload, status, and the mapping of AB05/AB06 to Zij ch. 54/55
  ledgers_index.tsv                      the ledgers of every session by kind, with their rows
  canonical_receipt.tsv                  every tracked file of every session with its SHA-256; one digest per session
  integration_receipt.json               the totals and the checks
coverage_ab01.py (AB01) and compare_duplicates.py run first. python integrate.py"""
import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

AB = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
csv.field_size_limit(10 ** 8)
SESSIONS = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S13", "S14", "S15"]
CONTRACT_ROLES = {"AB_TEXT", "AB_TABLE", "AB_SMALL_WORK", "NALLINO_TRANSLATION", "NALLINO_APPARATUS",
                  "MODERN_EDITORIAL", "COPY_PROVENANCE", "SCAN_EXTRINSIC", "UNCERTAIN"}
SECTION_NAMES = {"body", "notes_left", "notes_right", "margins", "col_left", "col_right", "notes", "notes_full"}
ROLE_MAP = {  # session sub-roles -> the contract's roles
    "NALLINO_ADNOTATIONES": ("NALLINO_APPARATUS", "Nallino's notes on the tables (Part II pp. 189-318)"),
    "NALLINO_GLOSSARIUM": ("NALLINO_APPARATUS", "Nallino's glossary (Part II pp. 319-358)"),
    "NALLINO_INDEX": ("NALLINO_APPARATUS", "Nallino's indexes (Part II pp. 359-413)"),
    "NALLINO_INDEX_HEAD": ("NALLINO_APPARATUS", "the heads of Nallino's indexes"),
    "NALLINO_TABLE": ("NALLINO_APPARATUS", "a table that Nallino sets in his notes"),
    "NALLINO_FIGURE": ("NALLINO_TRANSLATION or NALLINO_APPARATUS",
                       "a figure printed in Nallino's Part I; its role is that of the section it stands in (the "
                       "translation's figures render al-Battani's diagrams in Nallino's drawing)"),
}


def tsv(path, escaped=False):
    """escaped: the ledgers of S02-S09 are written with csv.QUOTE_NONE and a backslash escape (their builders'
    dialect): a backslash or a line break inside a field is escaped with a backslash, and must be read so"""
    with open(AB / path, encoding="utf-8", newline="") as fh:
        if escaped:
            return list(csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar="\\"))
        return list(csv.DictReader(fh, delimiter="\t"))


def write(name, head, rows):
    with open(HERE / name, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\t".join(head) + "\n")
        for r in rows:
            fh.write("\t".join(str(x) for x in r) + "\n")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tracked(session):
    out = subprocess.run(["git", "-C", str(AB), "ls-files", "--", session], capture_output=True, text=True,
                         encoding="utf-8").stdout.split("\n")
    return [p for p in out if p]


def coverage_ab02_ab03(checks):
    rows = []
    for r in tsv("S15/historia/page_disposition.tsv"):
        f = r["transcription"]
        ok = (not f) or (AB / "S15/historia" / f).exists()
        rows.append((r["pdf_page"], r["anchor"], r["printed_page"], "edited" if f else "disposed", r["role"],
                     r["disposition"], f, "ok" if ok else "MISSING"))
    write("coverage_ab02.tsv", ["pdf_page", "anchor", "printed_page", "state", "role", "disposition", "file", "check"],
          rows)
    pages = [int(r[0]) for r in rows]
    checks["AB02 coverage"] = (pages == list(range(1, 137)) and all(r[7] == "ok" for r in rows),
                               f"{len(rows)} PDF pages, {sum(r[3] == 'edited' for r in rows)} transcribed, "
                               f"{sum(r[3] == 'disposed' for r in rows)} disposed (the article's own text)")
    rows = []
    for r in tsv("S14/commentarius/page_disposition.tsv"):
        rec = AB / "S14/commentarius/records" / f"{r['anchor']}.json"
        src = AB / "S14/commentarius" / r["source"]
        blank = r["content"].startswith("blank")
        state = "disposed" if blank else "edited"
        ok = rec.exists() and src.exists()
        role = ("COPY_PROVENANCE" if blank else "AB_TEXT" if r["content"] in ("text", "title page")
                else "AB_TABLE") + "; MODERN_EDITORIAL (PAL's signs and notes)"
        rows.append((r["folio"], r["anchor"], state, role, r["content"], r["lines"], r["tables"], r["source"],
                     "ok" if ok else "MISSING"))
    write("coverage_ab03.tsv", ["folio", "anchor", "state", "role", "content", "lines", "tables", "source", "check"],
          rows)
    want = [f"{n}{s}" for n in range(20, 81) for s in "rv"]
    checks["AB03 coverage"] = ([r[0] for r in rows] == want and all(r[8] == "ok" for r in rows),
                               f"{len(rows)} page sides 20r-80v, {sum(r[2] == 'edited' for r in rows)} transcribed, "
                               f"{sum(r[2] == 'disposed' for r in rows)} blank")


def anchors(checks, cov01):
    """every line anchor of every session"""
    found = defaultdict(list)            # anchor -> [session]
    per = []

    def take(session, artifact, ids):
        ids = list(ids)
        for a in ids:
            found[a].append(session)
        pages = {re.match(r"(AB0\d-(?:PDF\d{4}|F\d{3}[rv]))", a).group(1) for a in ids
                 if re.match(r"AB0\d-(?:PDF\d{4}|F\d{3}[rv])", a)}
        bad = [a for a in ids if not re.fullmatch(r"AB0[1-3]-(PDF\d{4}|F\d{3}[rv])(-[A-Za-z_]+)?(-[A-Z]\d{1,3})+|"
                                                   r"AB03-n\d{3}", a)]
        per.append([session, artifact, len(ids), len(set(ids)), len(pages), len(bad), bad[:3]])
        return pages

    def json_lines(folder, session, only=None):
        ids = []
        for f in sorted((AB / folder).glob("AB01-PDF*.json")):
            if only and int(f.stem[-4:]) not in only:
                continue
            j = json.loads(f.read_text(encoding="utf-8"))
            for s in j.get("sections", []):
                ids += [ln["id"] for ln in s.get("lines", [])]
        return take(session, folder, ids)

    json_lines("S01/transcription/pages", "S01")
    json_lines("S02/candidate_v009_print001-053/transcription/pages", "S02", set(range(90, 143)))
    for path, session in (("S02/versio/anchors.tsv", "S02"), ("S03/versio/anchors.tsv", "S03"),
                          ("S04/versio/anchors.tsv", "S04"), ("S05/versio/anchors.tsv", "S05"),
                          ("S07/adnotationes/anchors.tsv", "S07"), ("S09/glossarium/anchors.tsv", "S09"),
                          ("S09/indices/anchors.tsv", "S09"), ("S10/textus/anchors.tsv", "S10"),
                          ("S11/textus/anchors.tsv", "S11"), ("S12/textus/anchors.tsv", "S12"),
                          ("S14/commentarius/anchors.tsv", "S14"), ("S14/commentarius/apparatus.tsv", "S14"),
                          ("S15/historia/anchors.tsv", "S15"), ("S15/historia/apparatus.tsv", "S15")):
        col = "note" if path == "S14/commentarius/apparatus.tsv" else "anchor"   # S14's notes are AB03-n###
        pages = take(session, path, [r[col] for r in tsv(path, escaped=session in ("S02", "S03", "S04", "S05",
                                                                                  "S07", "S09"))])
        if path.startswith(("S02", "S03", "S04", "S05", "S07", "S09", "S10", "S11", "S12")):
            # the pages of the anchors must be pages that this session edits (S07 may hold a second transcription)
            for pg in pages:
                own = cov01.get(int(pg[-4:]))
                if not own or (session not in own["owner"] and not (session == "S07" and "S07" in own["note"])):
                    per[-1][6] = per[-1][6] + [f"page {pg} not owned ({own['owner'] if own else '-'})"]
    dup = {a: s for a, s in found.items() if len(s) > 1}
    write("anchors_summary.tsv", ["session", "artifact", "anchors", "unique", "pages", "malformed", "notes"],
          [p[:6] + ["; ".join(map(str, p[6]))] for p in per])
    total = sum(p[2] for p in per)
    checks["anchors unique across the corpus"] = (not dup, f"{total:,} anchors in {len(per)} ledgers; "
                                                         f"{len(dup)} duplicated" + (f": {list(dup)[:5]}" if dup else ""))
    checks["anchors well-formed and on owned pages"] = (all(p[5] == 0 and not p[6] for p in per),
                                                        "; ".join(f"{p[1]}: {p[6]}" for p in per if p[5] or p[6])
                                                        or "all")
    return total


def roles(checks):
    used = defaultdict(Counter)

    def walk(o, s):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("role", "source_role", "authorship", "roles") and isinstance(v, str):
                    for x in re.split(r";\s*", v):
                        x = re.sub(r"\s*\(.*$", "", x).strip()
                        if x and x not in SECTION_NAMES:
                            used[x][s] += 1
                else:
                    walk(v, s)
        elif isinstance(o, list):
            for x in o:
                walk(x, s)

    for s in SESSIONS:
        for p in tracked(s):
            if p.endswith(".json") and "/history/" not in p and "candidate_v006" not in p and "extension_" not in p:
                try:
                    walk(json.loads((AB / p).read_text(encoding="utf-8")), s)
                except (ValueError, UnicodeDecodeError):
                    pass
            elif p.endswith("page_disposition.tsv") or p.endswith("coverage_ab01.tsv"):
                for r in tsv(p):
                    for k in ("role", "roles", "source_roles"):
                        for x in re.split(r";\s*", r.get(k) or ""):
                            x = re.sub(r"\s*\(.*$", "", x).strip()
                            if x:
                                used[x][s] += 1
    rows, unmapped = [], []
    for tag, c in sorted(used.items()):
        if tag in CONTRACT_ROLES:
            rows.append((tag, tag, "the contract's role", ", ".join(f"{k} {v}" for k, v in sorted(c.items()))))
        elif tag in ROLE_MAP:
            rows.append((tag, ROLE_MAP[tag][0], ROLE_MAP[tag][1], ", ".join(f"{k} {v}" for k, v in sorted(c.items()))))
        else:
            unmapped.append(tag)
            rows.append((tag, "UNMAPPED", "", ", ".join(f"{k} {v}" for k, v in sorted(c.items()))))
    write("roles_map.tsv", ["tag", "contract_role", "meaning", "uses"], rows)
    checks["every role tag maps to the contract"] = (not unmapped, f"{len(rows)} tags" +
                                                     (f"; unmapped: {unmapped}" if unmapped else ""))
    # the sessions whose lines carry a kind instead of a role tag: the role of each kind
    kind_role = {"text": "AB_TEXT", "h1": "AB_TEXT", "h2": "AB_TEXT", "display": "AB_TEXT", "cell": "AB_TABLE",
                 "figure": "AB_TABLE", "note": "NALLINO_APPARATUS", "latin": "NALLINO_APPARATUS",
                 "centre": "AB_SMALL_WORK", "heading": "AB_SMALL_WORK", "indent": "AB_SMALL_WORK",
                 "small": "AB_SMALL_WORK"}
    rows = []
    for path in ("S10/textus/anchors.tsv", "S11/textus/anchors.tsv", "S12/textus/anchors.tsv",
                 "S15/historia/anchors.tsv"):
        for k, n in sorted(Counter(r["kind"] for r in tsv(path)).items()):
            role = "AB_SMALL_WORK" if path.startswith("S15") else kind_role.get(k, "UNMAPPED")   # AB02 is a small work
            rows.append((path, f"kind={k}", role, n))
    rows += [("S14/commentarius/anchors.tsv", "every line", "AB_TEXT (the commentary); PAL's editorial signs "
              "within the lines: MODERN_EDITORIAL", len(tsv("S14/commentarius/anchors.tsv"))),
             ("S14/commentarius/apparatus.tsv", "PAL's notes", "MODERN_EDITORIAL",
              len(tsv("S14/commentarius/apparatus.tsv"))),
             ("S15/historia/apparatus.tsv", "the editors' apparatus", "MODERN_EDITORIAL",
              len(tsv("S15/historia/apparatus.tsv")))]
    for s in ("S06", "S13"):
        for f in sorted(AB.glob(f"{s}/*/*.tsv")):
            name = f.name
            if "discrepanc" in name or name.endswith("_pages.tsv") or "joined" in name:
                continue
            role = ("NALLINO_APPARATUS" if "notes" in name or "footnotes" in name or name == "note227.tsv"
                    else "AB_TABLE")
            n = max(sum(1 for _ in open(f, encoding="utf-8")) - 1, 0)
            rows.append((f.relative_to(AB).as_posix(), "every row", role, n))
    write("roles_by_kind.tsv", ["ledger", "unit", "contract_role", "rows"], rows)
    bad = [r for r in rows if r[2] == "UNMAPPED"]
    checks["every line kind maps to the contract"] = (not bad, f"{len(rows)} ledgers or kinds" +
                                                      (f"; unmapped: {bad}" if bad else ""))


def works(checks):
    a12 = {r["anchor"]: r for r in tsv("S12/textus/anchors.tsv")}
    a03 = {r["anchor"]: r for r in tsv("S03/versio/anchors.tsv")}
    a04 = {r["anchor"]: r for r in tsv("S04/versio/anchors.tsv")}
    need = {"AB01-PDF0958-L02": a12, "AB01-PDF0954-L02": a12, "AB01-PDF0949-L04": a12,
            "AB01-PDF0218-body-L012": a03, "AB01-PDF0220-body-L039": a03, "AB01-PDF0224-body-L001": a03,
            "AB01-PDF0394-body-L007": a04, "AB01-PDF0402-body-L004": a04, "AB01-PDF0407-body-L001": a04}
    text = {k: (v[k].get("text") or v[k].get("transcription")) for k, v in need.items()}
    ok = ("الاتِّصالات" in text["AB01-PDF0958-L02"] and "مَطالِع البروج" in text["AB01-PDF0954-L02"]
          and text["AB01-PDF0218-body-L012"].startswith("CAPUT LIV") and text["AB01-PDF0220-body-L039"].startswith(
              "CAPUT LV") and "LIV" in text["AB01-PDF0394-body-L007"] and "LV." in text["AB01-PDF0402-body-L004"])
    rows = [
        ("AB01", "A", "al-Zij al-Sabi'", "secure", "complete: Nallino's three volumes, master PDF 1-1162",
         "edited: every master page transcribed or disposed (coverage_ab01.tsv)", "S01-S13", ""),
        ("AB02", "B", "Kitab fi dala'il al-qiranat wa-l-kusufat", "secure",
         "complete: Suhayl 9 (2009-2010), the Arabic edition by G. Saliba (pp. 17-78) with translation and commentary",
         "edited: the Arabic edition transcribed; the article's own text not reproduced (coverage_ab02.tsv)", "S15",
         "CC BY-NC-ND 3.0 ES, as the article"),
        ("AB03", "B", "Sharh Kitab al-arba'a li-Batlamiyus", "secure",
         "complete: PAL's transcription of Escorial ar. 969, ff. 20r-80v, exact commit 762614d9",
         "edited: converted from PAL's transcription; the manuscript images not consulted (coverage_ab03.tsv)",
         "S14", "CC BY 4.0, as PAL's transcription"),
        ("AB04", "B", "Tajrid usul tarkib al-juyub", "questioned",
         "source-unacquired: Istanbul, Carullah 1499/3, bibliographic identity only; no pixels or transcription",
         "not edited: held; no text is produced or claimed, and the attribution stays questioned", "-", ""),
        ("AB05", "A-linked", "Kitab tahqiq aqdar al-ittisalat [bi-hasab urud al-kawakib]",
         "listed by Ibn al-Nadim; independent identity unproved",
         "within AB01: the Zij, chapter 54",
         "mapped, not duplicated: Arabic ch. 54 AB01-PDF0958-L01 (Part III p. 194, title line «"
         + text["AB01-PDF0958-L02"] + "») to the line before AB01-PDF0954-L01; Nallino's Latin «CAPUT LIV» "
         "AB01-PDF0218-body-L012 (Part I p. 129) to the line before AB01-PDF0220-body-L039; his commentary «Ad caput "
         "LIV» AB01-PDF0394-body-L007 (p. 305) to the line before AB01-PDF0402-body-L004", "S03, S04, S12", ""),
        ("AB06", "A-linked", "Kitab Matali' al-buruj fi ma bayna arba' al-falak",
         "listed by Ibn al-Nadim; independent identity unproved",
         "within AB01: the Zij, chapter 55",
         "mapped, not duplicated: Arabic ch. 55 AB01-PDF0954-L01 (Part III p. 198, title line «"
         + text["AB01-PDF0954-L02"] + "») to the line before AB01-PDF0949-L04 (ch. 56); Nallino's Latin «CAPUT LV» "
         "AB01-PDF0220-body-L039 (Part I p. 131) to the line before AB01-PDF0224-body-L001; his commentary «Ad caput "
         "LV» AB01-PDF0402-body-L004 (p. 313) to the line before AB01-PDF0407-body-L001", "S03, S04, S12", ""),
    ]
    write("works.tsv", ["work", "tier", "title", "attribution", "payload", "status", "sessions", "licence"], rows)
    checks["AB05/AB06 mapped to Zij ch. 54/55 by their anchors"] = (ok, "the Arabic chapter titles and Nallino's "
                                                                       "Latin and commentary headings found")
    checks["AB04 held as source-unacquired and attribution-questioned"] = (True, "works.tsv")


def ledgers(checks):
    kinds = [("page_disposition", r"page_disposition\.tsv$"), ("anchors", r"(^|/)anchors\.tsv$"),
             ("apparatus", r"(^|/)apparatus\.tsv$"), ("table data", r"_p[23]\.tsv$|_p2\.tsv$|_p3\.tsv$"),
             ("table check (differences)", r"discrepanc"), ("readings", r"readings\.tsv$"),
             ("corrections routing", r"corrigenda_routing|working_repairs|correction"),
             ("figures", r"/figures/.*\.(tex|tsv|json|png)$|geometry/"), ("folio/page maps", r"folios\.tsv$|_pages\.tsv$"),
             ("unresolved readings", r"unresolved"), ("records", r"/records/.*\.json$")]
    rows = []
    for s in SESSIONS:
        files = tracked(s)
        for kind, pat in kinds:
            hits = [p for p in files if re.search(pat, p)]
            if not hits:
                continue
            n = 0
            for p in hits:
                if p.endswith(".tsv"):
                    with open(AB / p, encoding="utf-8") as fh:
                        n += max(sum(1 for _ in fh) - 1, 0)
            rows.append((s, kind, len(hits), n if n else "", "; ".join(hits[:4]) + (" …" if len(hits) > 4 else "")))
    write("ledgers_index.tsv", ["session", "kind", "files", "rows", "files_first"], rows)
    checks["ledgers indexed"] = (True, f"{len(rows)} ledger groups in {len(SESSIONS)} sessions")
    # corrections and findings: what each session records, and what remains open
    rows = []
    for f in sorted(AB.glob("S06/*/*discrepanc*.tsv")) + sorted(AB.glob("S13/*/*discrepanc*.tsv")):
        n = len(tsv(f.relative_to(AB)))
        rows.append((f.relative_to(AB).as_posix(), "witness variants and printed numbers that differ from the "
                     "computation or from the other witness; the transcription keeps the print", n, 0))
    for f, what in (("S05/versio/corrigenda_routing.tsv", "Nallino's Addenda et emendanda to the three volumes, "
                     "each routed to the page it concerns and recorded there as an observation"),
                    ("S10/textus/page_disposition.tsv", "Nallino's corrigenda of Part III (PDF 872), each recorded with "
                     "the page it concerns (see the S10 page files)")):
        rows.append((f, what, len(tsv(f)) if f.endswith("routing.tsv") else 1, 0))
    rows.append(("S16/integration", "proposed canonical corrections from translation (no target-language edition "
                 "exists, so none were raised)", 0, 0))
    rows.append(("S16/integration", "finding: the ledgers of S02-S09 are written in a TSV dialect with backslash "
                 "escapes (csv.QUOTE_NONE, escapechar «\\»); one field of S07/adnotationes/anchors.tsv "
                 "(AB01-PDF0647-body-T01) holds escaped line breaks. Read with the same dialect, every row is whole; "
                 "no correction is needed", 1, 0))
    write("corrections_index.tsv", ["ledger", "content", "rows", "open"], rows)
    checks["no open correction"] = (all(r[3] == 0 for r in rows), f"{len(rows)} ledgers; 0 open")


def objects(checks):
    """formulas, figures, tables and unresolved readings of every session, counted from the sessions' own ledgers
    and records; the method of each count is stated"""
    rows = []

    def count_tsv(p):
        return len(tsv(p)) if (AB / p).exists() else 0

    rows.append(("S01", "formula", count_tsv("S01/ledgers/formula_provenance.tsv"), "S01/ledgers/formula_provenance.tsv"))
    rows.append(("S01", "figure or exact image object", count_tsv("S01/ledgers/figure_provenance.tsv"),
                 "S01/ledgers/figure_provenance.tsv"))
    rows.append(("S01", "table", count_tsv("S01/ledgers/table_provenance.tsv"), "S01/ledgers/table_provenance.tsv"))
    rows.append(("S01", "unresolved reading (open)", count_tsv("S01/ledgers/unresolved_readings.tsv"),
                 "S01/ledgers/unresolved_readings.tsv: character interpretations not settled; the exact source "
                 "images are kept in the edition"))
    v9 = "S02/candidate_v009_print001-053/ledgers/"
    rows.append(("S02", "formula (pp. 1-53, v009: pp. 41-53 new; pp. 1-40 in v002's ledger)",
                 count_tsv(v9 + "new_formula_objects.tsv") + count_tsv("S02/ledgers/formula_provenance.tsv"),
                 v9 + "new_formula_objects.tsv + S02/ledgers/formula_provenance.tsv"))
    vis = json.loads((AB / (v9 + "new_visual_objects.json")).read_text(encoding="utf-8"))
    rows.append(("S02", "figure or exact image object (pp. 41-53)", len(vis) if isinstance(vis, list) else
                 len(vis.get("objects", vis)), v9 + "new_visual_objects.json"))
    rows.append(("S02", "unresolved reading (open)", count_tsv(v9 + "unresolved_readings.tsv"),
                 v9 + "unresolved_readings.tsv: one damaged character kept as an exact crop; one statement that the "
                 "final visual check of pp. 44-53 is not certified by that package"))
    for folder in ("S02/versio", "S03/versio", "S04/versio", "S05/versio", "S07/adnotationes", "S09/glossarium",
                   "S09/indices"):
        f_lines = fig = 0
        for f in sorted((AB / folder / "records").glob("AB01-PDF*.json")):
            j = json.loads(f.read_text(encoding="utf-8"))
            for s in j["sections"]:
                for ln in s["lines"]:
                    if "$" in (ln.get("tex") or ""):
                        f_lines += 1
                    if ln.get("source_role") == "NALLINO_FIGURE" or re.search(r"-F\d+$", ln["id"]):
                        fig += 1
        s = folder.split("/")[0]
        rows.append((s, f"formula-bearing line ({folder})", f_lines, "lines whose TeX holds math mode ($)"))
        rows.append((s, f"figure or table block ({folder})", fig, "lines with the role NALLINO_FIGURE or an -F## id"))
    for folder in ("S10/textus", "S11/textus", "S12/textus"):
        k = Counter(r["kind"] for r in tsv(f"{folder}/anchors.tsv"))
        s = folder.split("/")[0]
        rows.append((s, f"figure label ({folder})", k.get("figure", 0), "anchors of kind figure: the letters and "
                     "labels of the redrawn figures"))
        if k.get("cell"):
            rows.append((s, f"table cell ({folder})", k["cell"], "anchors of kind cell"))
    for s in ("S06", "S13"):
        n = 0
        for f in sorted(AB.glob(f"{s}/*/*.tsv")):
            if re.search(r"_p[23]\.tsv$|_p2\.tsv$|_p3\.tsv$", f.name) and "notes" not in f.name:
                n += len(tsv(f.relative_to(AB)))
        rows.append((s, "table row or number (data TSVs)", n, f"{s}/*/*_p2.tsv, *_p3.tsv"))
        d = sum(len(tsv(f.relative_to(AB))) for f in AB.glob(f"{s}/*/*discrepanc*.tsv"))
        rows.append((s, "recorded difference (witness or computation)", d, f"{s}/*/*discrepanc*.tsv; all explained "
                     "in their notes; the print is kept"))
    rows.append(("S13", "figure (redrawn)", 4, "S13/diagrams: the seven climes and the astrological figure, "
                 "Part III and Part II"))
    rows.append(("S14", "table", len(list((AB / "S14/commentarius/tables").glob("*.tsv"))), "S14/commentarius/tables"))
    rows.append(("S15", "horoscope chart (redrawn)", len({r["chart"] for r in tsv("S15/historia/charts.tsv")}),
                 "S15/historia/charts.tsv"))
    write("objects_index.tsv", ["session", "object", "count", "source"], rows)
    open_u = sum(r[2] for r in rows if "unresolved reading (open)" in r[1])
    checks["formulas, figures, tables indexed"] = (True, f"{len(rows)} rows; {open_u} unresolved readings stay "
                                                         "open in S01/S02, with their exact source images kept")
    return open_u


def canonical_versions(checks):
    """which artifact is canonical for each source range, and its status"""
    rows = [
        ("AB01", "master PDF 1-89 (Part I front matter)", "S01/pdf/S01_NALLINO_SOURCE_v003.pdf", "S01 v003",
         "edited; S01's README records that its independent cold audit is outstanding"),
        ("AB01", "PDF 90-142 (Part I pp. 1-53)", "S02/candidate_v009_print001-053/pdf/S02_NALLINO_SOURCE_v009.pdf",
         "S02 v009 candidate", "edited; supersedes v002 (pp. 1-30) and v006 (pp. 1-40); the package states that "
         "the final visual check of pp. 44-53 is not certified"),
        ("AB01", "PDF 143-198 (Part I pp. 54-109)", "S02/versio/p1_versio.pdf", "S02/versio", "edited"),
        ("AB01", "PDF 199-307 (Part I pp. 110-218)", "S03/versio/p1_versio.pdf", "S03/versio", "edited"),
        ("AB01", "PDF 308-416 (Part I pp. 219-327)", "S04/versio/p1_versio.pdf", "S04/versio", "edited"),
        ("AB01", "PDF 417-449 (Part II front matter)", "S05/versio/p1_versio.pdf", "S05/versio", "edited"),
        ("AB01", "PDF 450-637 (Part II tables)", "S06/*/p2_*.pdf, S13/*/p2_*.pdf", "S06, S13", "edited"),
        ("AB01", "PDF 638-767 (Part II notes)", "S07/adnotationes/p2_adnotationes.pdf", "S07",
         "edited; the table pages inside the notes are canonical in S06/S13 (coverage_ab01.tsv)"),
        ("AB01", "PDF 768-862 (glossary, indexes)", "S09/glossarium/p2_glossarium.pdf, S09/indices/p2_indices.pdf",
         "S09", "edited"),
        ("AB01", "PDF 863-872, 1152-1162 (dispositions, Part III titles, corrigenda)",
         "S09/indices/page_disposition.tsv, S10/textus", "S09, S10", "edited or disposed"),
        ("AB01", "PDF 926-1151, 1153 (Arabic text, chapters list, title)",
         "S10/textus, S11/textus, S12/textus (p3_textus.pdf)", "S10-S12", "edited"),
        ("AB01", "PDF 873-925 (Arabic tables, notice)", "S13/*/p3_*.pdf", "S13", "edited"),
        ("AB02", "Suhayl 9, PDF 1-136", "S15/historia/historia.pdf", "S15", "edited (Arabic edition); the "
         "article's own text not reproduced"),
        ("AB03", "Escorial ar. 969, ff. 20r-80v", "S14/commentarius/commentarius.pdf", "S14", "converted from PAL"),
        ("AB04", "-", "-", "-", "source-unacquired; attribution questioned; nothing produced"),
        ("AB05", "within AB01: Zij ch. 54", "the AB01 artifacts above", "-", "mapped; not duplicated"),
        ("AB06", "within AB01: Zij ch. 55", "the AB01 artifacts above", "-", "mapped; not duplicated"),
    ]
    out = []
    for w, rng, art, ver, status in rows:
        hashes = []
        for a in re.split(r",\s*", art):
            if a.endswith(".pdf") and "*" not in a and (AB / a).exists():
                hashes.append(sha256(AB / a)[:16])
        out.append((w, rng, art, ver, status, " ".join(hashes)))
    write("canonical_versions.tsv", ["work", "source_range", "artifact", "version", "status", "pdf_sha256_16"], out)
    checks["canonical version named for every range"] = (True, f"{len(out)} ranges")


def canonical(checks):
    rows, digests = [], []
    for s in SESSIONS:
        files = sorted(tracked(s))
        lines = []
        for p in files:
            h = sha256(AB / p)
            rows.append((s, p, (AB / p).stat().st_size, h))
            lines.append(f"{p}\t{h}")
        d = hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()
        done = ""
        for rd in sorted(AB.glob(f"{s}/**/README.md")):
            m = re.search(r"\*\*Done:?\*\*:?\s*([^\n]+)", rd.read_text(encoding="utf-8"))
            if m:
                done += f"{rd.relative_to(AB).as_posix()}: {m.group(1)[:160]} "
        digests.append((s, len(files), d, done.strip()))
    write("canonical_receipt.tsv", ["session", "file", "bytes", "sha256"], rows)
    write("session_digests.tsv", ["session", "tracked_files", "digest_sha256", "done"], digests)
    checks["canonical receipt"] = (True, f"{len(rows):,} tracked files of {len(SESSIONS)} sessions hashed")
    return digests


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    checks = {}
    cov01 = {int(r["master_pdf_page"]): r for r in tsv("S16/integration/coverage_ab01.tsv")}
    states = Counter(r["state"] for r in cov01.values())
    checks["AB01 coverage"] = (len(cov01) == 1162 and set(states) <= {"edited", "disposed"},
                               f"1162 master pages: {states['edited']} edited, {states['disposed']} disposed, "
                               f"{states.get('GAP', 0)} gaps, {states.get('OVERLAP', 0)} overlaps")
    dup = tsv("S16/integration/duplicates_compared.tsv")
    agree = [r for r in dup if not r["only_canonical"]]
    repairs = tsv("S16/integration/repairs.tsv")
    checks["second transcriptions agree"] = (len(agree) == len(dup),
                                             f"{len(dup)} pages compared (tables number by number, the half-title "
                                             f"and the figure word by word), "
                                             f"{sum(int(r['items_canonical']) for r in dup):,} items; every "
                                             f"canonical item found in S07's transcription; S07's further items are "
                                             f"footnote marks and the note that shares p. 220; "
                                             f"{len(repairs)} readings corrected after the comparison "
                                             f"(repairs.tsv)")
    coverage_ab02_ab03(checks)
    n_anchors = anchors(checks, cov01)
    roles(checks)
    works(checks)
    ledgers(checks)
    open_u = objects(checks)
    canonical_versions(checks)
    digests = canonical(checks)
    receipt = {"session": "S16", "step": "integration", "checks": {k: {"pass": v[0], "detail": v[1]}
                                                                   for k, v in checks.items()},
               "anchors": n_anchors, "unresolved_readings_open": open_u,
               "session_digests": {s: d for s, _, d, _ in digests}}
    (HERE / "integration_receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=1) + "\n",
                                                   encoding="utf-8", newline="\n")
    for k, (ok, detail) in checks.items():
        print(("PASS " if ok else "FAIL ") + k + ": " + detail)


if __name__ == "__main__":
    main()

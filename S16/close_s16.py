"""S16 - the closing receipts of the integration and cold audit. Reads the outputs of S16/integration, S16/assembly
and S16/audit (it computes nothing new about the sources) and writes, beside this script:
  receipts/coverage.tsv  for every work AB01-AB06: its source units, how many are edited, disposed and open, and
                         where the integration and the audit record them
  receipts/status.tsv    the status of every work, of every source range with its canonical artifact (PDF hash), of
                         the two assembled volumes, and every check of the integration, the assembly and the audit
  receipts/gaps.tsv      every known gap, with its exact boundary, what stands in its place and the record that
                         holds it
  checkpoint.json        the cumulative checkpoint of S16
  MANIFEST_SHA256.tsv    every file under S16 (this manifest excepted) with its size and SHA-256, written last
python close_s16.py"""
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
AB = HERE.parent
csv.field_size_limit(10 ** 8)
DATE = "2026-10-16"


def tsv(path):
    with open(HERE / path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write(path, head, rows):
    (HERE / path).parent.mkdir(exist_ok=True)
    with open(HERE / path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\t".join(head) + "\n")
        for r in rows:
            fh.write("\t".join(str(x) for x in r) + "\n")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def coverage():
    c1 = tsv("integration/coverage_ab01.tsv")
    c2 = tsv("integration/coverage_ab02.tsv")
    c3 = tsv("integration/coverage_ab03.tsv")
    s1, s2, s3 = (Counter(r["state"] for r in c) for c in (c1, c2, c3))
    second = sum(1 for r in c1 if r["note"].startswith("second transcription"))
    compared = tsv("integration/duplicates_compared.tsv")
    shared = {r["master_pdf_page"]: r["artifact"].replace(";", " and ") for r in c1
              if r["note"].startswith(("shared page", "two families"))}
    replay = tsv("audit/coverage_replay.tsv")
    audit = json.loads((HERE / "audit/audit_report.json").read_text(encoding="utf-8"))["checks"]
    agree = audit["AB01 coverage replay agrees with S16/integration/coverage_ab01.tsv"]["detail"]
    reproduced = Counter(r["state"] for r in c2 if r["state"] == "edited")["edited"]
    not_reproduced = Counter(r["disposition"] for r in c2 if r["state"] == "disposed")
    works = {r["work"]: r for r in tsv("integration/works.tsv")}
    rows = [
        ("AB01", "master PDF pages of Nallino's three volumes (SRC01)", len(c1), s1["edited"], s1["disposed"],
         len(c1) - s1["edited"] - s1["disposed"],
         f"every page edited or disposed once; {len(compared)} pages among Nallino's notes are transcribed a second "
         f"time by S07 and compared item by item (duplicates_compared.tsv): {second} table and figure pages, and "
         f"p. 669, whose table S13 edits and whose following note S07 edits; pages edited by two parts: "
         + "; ".join(f"{p} ({n})" for p, n in sorted(shared.items())) +
         f"; the audit's replay from the edition PDFs and the disposition ledgers ({len(replay)} pages): {agree}",
         "S16/integration/coverage_ab01.tsv; S16/audit/coverage_replay.tsv"),
        ("AB02", "PDF pages of Suhayl 9 (SRC06)", len(c2), s2["edited"], s2["disposed"],
         len(c2) - s2["edited"] - s2["disposed"],
         f"the Arabic edition transcribed on {reproduced} pages (the title page and the even pages 18-78); the "
         f"other {s2['disposed']} pages are the article's own text, read as a comparator or not used, not "
         f"reproduced (CC BY-NC-ND 3.0 ES): " + "; ".join(f"{n} {d}" for d, n in not_reproduced.most_common()),
         "S16/integration/coverage_ab02.tsv"),
        ("AB03", "page sides 20r-80v of Escorial ar. 969 in PAL's transcription (SRC07)", len(c3), s3["edited"],
         s3["disposed"], len(c3) - s3["edited"] - s3["disposed"],
         "converted from PAL's transcription (commit 762614d9); the disposed side is blank",
         "S16/integration/coverage_ab03.tsv"),
        ("AB04", "Istanbul, Carullah 1499/3 (SRC09): no local payload", 0, 0, 0, "-",
         works["AB04"]["status"], "S16/integration/works.tsv; S01/controls/03_SOURCE_WITNESS_GATE.tsv"),
        ("AB05", "within AB01: the Zij, chapter 54", "-", "-", "-", "-",
         works["AB05"]["status"], "S16/integration/works.tsv"),
        ("AB06", "within AB01: the Zij, chapter 55", "-", "-", "-", "-",
         works["AB06"]["status"], "S16/integration/works.tsv"),
    ]
    write("receipts/coverage.tsv", ["work", "source_units", "units", "edited", "disposed", "open", "detail",
                                    "record"], rows)
    return {"AB01": {"master_pdf_pages": len(c1), "edited": s1["edited"], "disposed": s1["disposed"], "open": 0},
            "AB02": {"pdf_pages": len(c2), "edited": s2["edited"], "disposed": s2["disposed"], "open": 0},
            "AB03": {"page_sides": len(c3), "edited": s3["edited"], "disposed": s3["disposed"], "open": 0},
            "AB04": "source-unacquired; attribution questioned; nothing produced",
            "AB05": "mapped to the Zij, chapter 54; not duplicated",
            "AB06": "mapped to the Zij, chapter 55; not duplicated"}


def status():
    rows = []
    for r in tsv("integration/works.tsv"):
        rows.append(("work", r["work"], r["status"], f"tier {r['tier']}; {r['title']}; attribution: "
                     f"{r['attribution']}; payload: {r['payload']}" + (f"; licence: {r['licence']}" if r["licence"]
                                                                        else ""), "S16/integration/works.tsv"))
    for r in tsv("integration/canonical_versions.tsv"):
        rows.append(("source range", f"{r['work']} {r['source_range']}", r["status"],
                     f"canonical artifact {r['artifact']} ({r['version']})" +
                     (f"; PDF sha256 {r['pdf_sha256_16']}..." if r["pdf_sha256_16"] else ""),
                     "S16/integration/canonical_versions.tsv"))
    vols = tsv("assembly/volumes.tsv")
    for v in vols:
        rows.append(("volume", v["volume"], "assembled; built twice, byte-identical",
                     f"{v['pages']} pages, {v['bookmarks']} bookmarks, sha256 {v['sha256']}, sources at commit "
                     f"{v['commit_on_cover']}", "S16/assembly/volumes.tsv; S16/assembly/assembly_receipt.tsv"))
    rows.append(("volume", "target-language editions", "none",
                 "no monolingual target-language edition of AB01-AB03 exists at this checkpoint; the translation "
                 "loop of S01/controls/09 has not started", "S16/receipts/gaps.tsv"))
    integ = json.loads((HERE / "integration/integration_receipt.json").read_text(encoding="utf-8"))
    for name, c in integ["checks"].items():
        rows.append(("integration check", name, "PASS" if c["pass"] else "FAIL", c["detail"],
                     "S16/integration/integration_receipt.json"))
    audit = json.loads((HERE / "audit/audit_report.json").read_text(encoding="utf-8"))
    for name, c in audit["checks"].items():
        rows.append(("audit check", name, "PASS" if c["pass"] else "FAIL", c["detail"],
                     "S16/audit/audit_report.json"))
    s01 = json.loads((HERE / "audit/s01_technical_audit_replay.json").read_text(encoding="utf-8"))
    n = len(s01["checks"])
    ok = sum(1 for c in s01["checks"] if c.get("pass"))
    rows.append(("audit check", "S01's own technical audit, replayed", "PASS" if ok == n else "FAIL",
                 f"{ok} of {n} checks pass on the complete S01 v003 package; S01's philological reading audit has "
                 f"not been performed", "S16/audit/s01_technical_audit_replay.json"))
    rep = tsv("integration/repairs.tsv")
    rows.append(("repairs", "readings corrected in production after S16's comparisons", f"{len(rep)}",
                 "; ".join(f"{r['id']} {r['session']} {r['item']}: {r['was']} -> {r['now']}" for r in rep),
                 "S16/integration/repairs.tsv"))
    write("receipts/status.tsv", ["kind", "item", "status", "detail", "record"], rows)
    fails = [r for r in rows if r[2] == "FAIL"]
    return integ, audit, vols, (n, ok), rep, fails


GAPS = [  # id, scope, gap, exact boundary, in its place, record
    ("G01", "AB04", "source unacquired; attribution questioned",
     "Tajrid usul tarkib al-juyub, Istanbul, Carullah 1499/3: bibliographic identity only, no pixels, no "
     "transcription", "nothing is produced or claimed",
     "S01/controls/03_SOURCE_WITNESS_GATE.tsv (SRC09); S01/controls/07_PRIOR_OUTPUT_CONTINUITY_AND_GAPS.tsv (GAP01); "
     "S16/integration/works.tsv"),
    ("G02", "AB01", "the codex not collated",
     "Escorial, arabe 908, the manuscript of the Zij: no manuscript pixels in the source gate",
     "Nallino's edition (SRC01) is the production authority; its readings of the codex stand as printed",
     "S01/controls/07_PRIOR_OUTPUT_CONTINUITY_AND_GAPS.tsv (GAP02)"),
    ("G03", "AB01", "Parts I and II read in one scan copy",
     "master PDF 1-862 (Parts I and II): the source gate has a second copy for Part III only",
     "every reading of Parts I and II rests on SRC01; Part III readings were checked in both copies where the "
     "sessions say so", "S01/controls/03_SOURCE_WITNESS_GATE.tsv (SRC01, SRC02)"),
    ("G04", "AB01", "unresolved readings (S01)",
     "11 entries of S01/ledgers/unresolved_readings.tsv (master PDF 1-89): 10 with the status "
     "DISPOSED_IMAGE_FALLBACK, whose character interpretation is not settled, and 1 DOCUMENTED_SOURCE_LOSS (the "
     "frontispiece's edges, truncated in the scan)", "the exact source images are kept in the edition",
     "S01/ledgers/unresolved_readings.tsv"),
    ("G05", "AB01", "an unresolved reading and an uncertified check (S02 v009)",
     "2 entries of S02/candidate_v009_print001-053/ledgers/unresolved_readings.tsv: S02-v009-U001, a damaged "
     "character at AB01-PDF0140-body-L001 kept as an exact crop; S02-v009-VISUAL, the final visual check of "
     "pp. 44-53 (master PDF 133-142) is not certified by that package",
     "the reading stands as transcribed, with the crop",
     "S02/candidate_v009_print001-053/ledgers/unresolved_readings.tsv"),
    ("G06", "AB01", "S01's philological reading audit not performed",
     "master PDF 1-89 (S01 v003): S01's status is «SOURCE_REVISED_CANDIDATE; INDEPENDENT_COLD_SOURCE_AUDIT_"
     "OUTSTANDING»", "S01's own technical audit (47 checks) replayed on the complete package: 47 pass",
     "S01/receipts/cumulative_checkpoint.json; S16/audit/s01_technical_audit_replay.json"),
    ("G07", "AB02", "the manuscript not consulted",
     "Ankara, Ismail Saib 199/2, ff. 27v-42v (the unique manuscript)",
     "the Arabic edition by G. Saliba in Suhayl 9 (SRC06), transcribed from the article's page images",
     "S15/historia/checkpoint.json"),
    ("G08", "AB03", "the manuscript images not consulted",
     "Escorial, arabe 969, ff. 20r-80v; and the Berlin comparator, Sprenger 1840, whose images were not acquired",
     "PAL's transcription (SRC07, commit 762614d9), converted and checked against PAL's files (0 differences); "
     "the Berlin folio correspondences as PAL records them",
     "S14/commentarius/checkpoint.json; S01/controls/07_PRIOR_OUTPUT_CONTINUITY_AND_GAPS.tsv (GAP03)"),
    ("G09", "AB01-AB03", "no target-language edition",
     "no monolingual translation of AB01, AB02 or AB03; the translation and source-check loop of "
     "S01/controls/09_MULTILINGUAL_QA_FEEDBACK_LOOP.txt has not started",
     "the canonical checkpoint a translation starts from is named in S16/checkpoint.json",
     "S16/checkpoint.json"),
    ("G10", "AB01-AB06", "the cold audit is not independent of the producer",
     "S16/audit/cold_audit.py is a separate read-only program, but it was written and run by the same AI "
     "(Claude) that produced and integrated the edition, in the same session; no separate agent and no person "
     "has audited the corpus", "16 checks, 0 failures; the visual samples were inspected by the same AI "
     "(audit_inspection.md); human review is welcome and is not a completion gate",
     "S16/audit/audit_report.md; S16/audit/audit_inspection.md"),
]


def gaps():
    gate = {r["source_id"]: r for r in csv.DictReader(open(AB / "S01/controls/03_SOURCE_WITNESS_GATE.tsv",
                                                           encoding="utf-8"), delimiter="\t")}
    rows = []
    for g in GAPS:
        if g[0] == "G03":
            g = g[:3] + (g[3] + f" (SRC02: {gate['SRC02']['physical_units']}; "
                         f"{gate['SRC02']['quality_and_topology']})",) + g[4:]
        rows.append(g)
    write("receipts/gaps.tsv", ["id", "scope", "gap", "exact_boundary", "in_its_place", "record"], rows)
    return rows


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    cov = coverage()
    integ, audit, vols, (n01, ok01), rep, fails = status()
    gp = gaps()
    checkpoint = {
        "session": "S16",
        "works": "AB01-AB06",
        "scope": "integration, monolingual assembly, correction routing and cold audit; no source unit is "
                 "transcribed in S16",
        "owned_source_units": "none",
        "last_fully_transcribed_source_unit": None,
        "last_fully_verified_source_unit": None,
        "first_untouched_source_unit": None,
        "canonical_checkpoint": {
            "commit": audit["commit"],
            "note": "the production files of S01-S15 as integrated and audited; a translation starts from this "
                    "commit and these session digests (SHA-256 of each session's tracked files and hashes)",
            "session_digests": integ["session_digests"],
        },
        "coverage": cov,
        "volumes": [{"file": f"S16/assembly/{v['volume']}", "pages": int(v["pages"]),
                     "bookmarks": int(v["bookmarks"]), "sha256": v["sha256"], "sources_at_commit":
                     v["commit_on_cover"], "build": "deterministic; built twice, byte-identical"} for v in vols],
        "target_language_editions": [],
        "anchors": integ["anchors"],
        "unresolved_readings_open": integ["unresolved_readings_open"],
        "checks": {
            "integration": f"{sum(1 for c in integ['checks'].values() if c['pass'])} of {len(integ['checks'])} pass",
            "audit": f"{len(audit['checks'])} checks, {len(audit['failures'])} failures (commit {audit['commit'][:7]})",
            "s01_technical_audit_replay": f"{ok01} of {n01} pass",
        },
        "repairs": [f"{r['id']}: {r['session']}, {r['item']}: {r['was']} -> {r['now']}" for r in rep],
        "auditor": audit["auditor"],
        "human_review": "none; welcome later; not a completion gate",
        "not_done": [f"{g[0]} {g[1]}: {g[2]}" for g in gp],
        "licence": "S16's scripts, receipts and inspection images: CC0 1.0; the assembled volumes: CC0 1.0 for the "
                   "edition, Nallino's work in the public domain (as their covers state)",
        "date": DATE,
    }
    (HERE / "checkpoint.json").write_text(json.dumps(checkpoint, ensure_ascii=False, indent=1) + "\n",
                                          encoding="utf-8", newline="\n")
    files = sorted(p for p in HERE.rglob("*") if p.is_file() and p.name != "MANIFEST_SHA256.tsv"
                   and "__pycache__" not in p.parts)
    write("MANIFEST_SHA256.tsv", ["path", "bytes", "sha256"],
          [(p.relative_to(AB).as_posix(), p.stat().st_size, sha256(p)) for p in files])
    print(f"coverage: {cov['AB01']}, {cov['AB02']}, {cov['AB03']}")
    print(f"status rows written; failing checks: {len(fails)}")
    print(f"gaps: {len(gp)}; repairs: {len(rep)}; manifest: {len(files)} files")


if __name__ == "__main__":
    main()

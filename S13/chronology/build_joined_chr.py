"""Joined dataset of the chronological tables: one row per Part III row (kings, intervals between the eras, caliphs),
with the raw Arabic cells, decoded values, Nallino's Part II values, the codex readings from his notes, the numeral
system of the row, and a status per field. Writes chronology_joined.tsv and chronology_joined.json."""
import csv, json
from pathlib import Path

import check_chr as cc

HERE = Path(__file__).resolve().parent
ledger = {r["where"].split(" | ")[0]: r for r in cc.read("chr_discrepancies.tsv")}
p2 = {r["no"]: r for r in cc.read("chr_p2.tsv") if r["kind"] in ("L", "R", "T") and r["no"]}
codex = {}
for r in cc.read("chr_p2_codex.tsv"):
    codex.setdefault(r["no"], {})[r["field"]] = r["codex"]

rows = []
for r in cc.read("chr_p3.tsv"):
    if r["kind"] != "row":
        continue
    q = p2.get(r["p2"]); cod = codex.get(r["p2"], {})
    east = (r["pdf"], r["line"]) in cc.EAST_ROWS
    out = {"pdf": r["pdf"], "page": r["ppage"], "row": r["line"], "section": r["section"], "no": r["p2"],
           "name_ar": r["text"], "p2_name": q["name"] if q else "", "p2_page": q["ppage"] if q else "",
           "numerals": "Maghribi; Eastern hundreds ض = 800, ظ = 900 (f. 155,v., p. 230 fn 8)" if east else "Maghribi",
           "doubt": r["doubt"]}
    status = []
    for f in cc.FIELDS:
        raw = r[f]; a = cc.abjad(raw, east)
        b = cc.latin_num(q[f]) if q else None
        c = cod.get(f)
        out[f + "_ar"] = raw; out[f] = "" if a is None else a
        out["p2_" + f] = "" if b is None else b; out["codex_" + f] = c or ""
        key = f"{r['pdf']} {r['line']} {r['p2']} {f}"
        if a is None and b is None and c is None:
            continue
        if key in ledger:
            st = "ledgered"
        elif c is not None and a in cc.codex_values(c):
            st = "agrees" if a == b else "codex note"
        elif a == b:
            st = "agrees"
        else:
            st = "?"
        if st != "agrees":
            status.append(f"{f}:{st}")
    if all(r[f] == "" for f in cc.FIELDS):
        status.append("no numbers")
    out["status"] = "; ".join(status) or "agrees"
    rows.append(out)

with open(HERE / "chronology_joined.tsv", "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(rows)
(HERE / "chronology_joined.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
bad = [r for r in rows if "?" in r["status"]]
print(f"{len(rows)} rows; unexplained fields: {len(bad)}")
for r in bad:
    print("  ", r["pdf"], r["row"], r["no"], r["status"])

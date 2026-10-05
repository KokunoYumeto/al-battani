"""Joined dataset of the status tables for 1211: one row per Part III star row, with the raw Arabic cells, decoded
values, Nallino's Part II values, the codex readings from his notes, and a status per field.
Writes status_1211_joined.tsv and status_1211_joined.json."""
import csv, json, re
from pathlib import Path

import check_status as cs

HERE = Path(__file__).resolve().parent
FIELDS = cs.NUM + ("dir", "mag")
ledger = {r["where"].split(" | ")[0] for r in cs.read("st_discrepancies.tsv")}
p2 = {r["no"]: r for r in cs.read("st_p2.tsv") if r["kind"] == "star"}
notes = {}
for r in cs.read("st_p2_notes.tsv"):
    for item in filter(None, r["codex"].split(";")):
        if "=" in item:
            k, v = item.split("=", 1)
            notes.setdefault(r["no"], {})[k] = v

rows, cur = [], None
for r in cs.read("st_p3.tsv"):
    if r["kind"] != "star":
        continue
    if r["dir"].strip():
        cur = cs.DIRS[r["dir"].strip()]
    q = p2.get(r["p2"]); cod = notes.get(r["p2"], {})
    out = {"pdf": r["pdf"], "page": r["ppage"], "row": r["line"], "table": r["section"], "no": r["p2"],
           "name_ar": r["text"], "doubt": r["doubt"]}
    status = []
    for f in FIELDS:
        if f == "dir":
            raw, a = r["dir"], cur
            b = cs.PLAGA.get(q["plaga"].replace("*", "").strip(), "?") if q else ""
            c = {"N": "b", "S": "a"}.get(cod.get("dir"))
        elif f == "mag":
            raw = r["mag"]; a = cs.abjad(re.sub(r"\s.*", "", raw)) if raw else None
            b = cs.latin_num(q["mag"]) if q else None
            c = cod.get("mag")
        else:
            raw = r[f]; a = cs.abjad(raw) if raw else None
            b = cs.latin_num(q[f]) if q else None
            c = cod.get(f)
        out[f + "_ar"] = raw; out[f] = "" if a is None else a
        out["p2_" + f] = "" if b is None else b; out["codex_" + f] = c or ""
        if a is None and b is None:
            continue
        key = f"{r['pdf']} {r['line']} {r['p2']} {f if f != 'mag' else 'magnitude'}"
        if key in ledger:
            st = "ledgered"
        elif a == b:
            st = "agrees"
        elif c is not None:
            st = "codex note"
        elif f == "mag" and a is None:
            st = "no magnitude in the codex"
        else:
            st = "?"
        if st != "agrees":
            status.append(f"{f}:{st}")
    out["status"] = "; ".join(status) or "agrees"
    rows.append(out)

cols = list(rows[0].keys())
with open(HERE / "status_1211_joined.tsv", "w", encoding="utf-8", newline="\n") as fh:
    w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(rows)
json.dump(rows, open(HERE / "status_1211_joined.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("joined rows:", len(rows), "| fields still '?':", sum(x["status"].count(":?") for x in rows))

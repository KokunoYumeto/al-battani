"""Joined dataset of the geographical tables: one row per Part III row (regions, cities, Andalusian and Maghribi cities),
with the raw Arabic cells, decoded values, Nallino's Part II values, the codex readings from his notes, and a status per
field. Writes geography_joined.tsv and geography_joined.json."""
import csv, json
from pathlib import Path

import check_geo as cg

HERE = Path(__file__).resolve().parent
ledger = {r["where"].split(" | ")[0] for r in cg.read("geo_discrepancies.tsv")}
p2 = {r["no"]: r for r in cg.read("geo_p2.tsv") if r["kind"] in ("L", "R", "T")}
notes, tnotes = {}, {}
for r in cg.read("geo_p2_notes.tsv"):
    for item in filter(None, r["codex"].split(";")):
        if "=" in item:
            k, v = item.split("=", 1)
            notes.setdefault(r["no"], {})[k] = v
    if r["no"] in p2 and p2[r["no"]]["kind"] == "T":
        tnotes[r["no"]] = r["text"]                                    # the notes column of Part II pp. 219-220

rows = []
for r in cg.read("geo_p3.tsv"):
    if r["kind"] != "row":
        continue
    q = p2.get(r["p2"]); cod = notes.get(r["p2"], {})
    out = {"pdf": r["pdf"], "page": r["ppage"], "row": r["line"], "section": r["section"], "no": r["p2"],
           "name_ar": r["text"], "p2_name": q["name"] if q else "", "p2_page": q["ppage"] if q else "",
           "p2_notae": tnotes.get(r["p2"], ""), "doubt": r["doubt"]}
    status = []
    for f in cg.FIELDS:
        raw = r[f]; a = cg.abjad(raw)
        b = cg.latin_num(q[f]) if q else None
        c = cod.get(f)
        out[f + "_ar"] = raw; out[f] = "" if a is None else a
        out["p2_" + f] = "" if b is None else b; out["codex_" + f] = c or ""
        key = f"{r['pdf']} {r['line']} {r['p2']} {f}"
        if key in ledger:
            st = "ledgered"
        elif a is None and f.endswith("_m") and b == 0 and c is None:
            st = "blank (Part II 0)"
        elif c is not None and a in cg.codex_values(c):
            st = "agrees" if a == b else "codex note"
        elif a == b:
            st = "agrees"
        else:
            st = "?"
        if st != "agrees":
            status.append(f"{f}:{st}")
    out["status"] = "; ".join(status) or "agrees"
    rows.append(out)

with open(HERE / "geography_joined.tsv", "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(rows)
(HERE / "geography_joined.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
bad = [r for r in rows if "?" in r["status"]]
print(f"{len(rows)} rows; unexplained fields: {len(bad)}")
for r in bad:
    print("  ", r["pdf"], r["row"], r["no"], r["status"])

"""Joined star-catalogue dataset: one row per Part III (codex) star row, with the raw Arabic cells, their decoded
values, Nallino's Part II values, his structured codex readings, and a status per field.
Writes star_catalogue_joined.tsv and star_catalogue_joined.json (same content)."""
import csv, json, re
from pathlib import Path

import check_stars as cs          # reuses the decoding and the data as loaded there (running it prints its summary)

HERE = Path(__file__).resolve().parent
ledger = {r["where"].split(" | ")[0]: r for r in csv.DictReader(open(HERE / "discrepancies.tsv", encoding="utf-8"), delimiter="\t")}
p2 = {(r["section"], r["no"]): r for r in cs.read("p2_stars.tsv") if r["kind"] == "star"}
notes = {}
for r in cs.read("p2_notes.tsv"):
    cod = dict(item.split("=", 1) for item in filter(None, r["codex"].split(";")) if "=" in item)
    notes[(r["section"], r["no"])] = cod

rows, cur_dir = [], None
for r in cs.read("p3_stars.tsv"):
    if r["kind"] != "star":
        continue
    d = r["dir"].strip()
    m = re.fullmatch(r"\{BR:(.+):(\d+)\}", d)
    if m:
        cur_dir = {"الشمال": "b", "الجنوب": "a"}[m.group(1)]
    elif d not in ("", "{BR}"):
        cur_dir = cs.DIRS[d]
    out = {"pdf": r["pdf"], "page": r["ppage"], "row": r["line"], "section": r["section"], "part2_star": r["p2"],
           "description_ar": r["text"], "doubt": r["doubt"]}
    for f in cs.FIELDS:
        out[f + "_ar"] = r[f]
        out[f] = cs.abjad(r[f]) if r[f] else ""
    out["dir_ar"], out["dir"] = d, cur_dir
    out["mag_ar"], out["mag"] = r["mag"], cs.p3_mag(r["mag"])
    q = p2.get(tuple(r["p2"].split())) if r["p2"] not in ("", "none") else None
    cod = notes.get(tuple(r["p2"].split()), {}) if q else {}
    status = []
    for f in cs.FIELDS + ("dir", "mag"):
        if q is None:
            out["p2_" + f] = ""
            continue
        if f == "dir":
            v2 = cs.PLAGA.get(q["plaga"].replace("*", "").strip(), "?")
            c = {"N": "b", "S": "a"}.get(cod.get("dir"))
            a = cur_dir
        elif f == "mag":
            v2 = q["mag"].replace("*", "").strip(); c = cod.get("mag"); a = out["mag"]
        else:
            v2 = cs.latin_num(q[f]); c = cod.get(f); a = out[f]
        out["p2_" + f] = v2
        key = f"{r['pdf']} {r['line']} {r['p2']} {f if f != 'mag' else 'magnitude'}"
        if key in ledger:
            st = "ledgered"
        elif a == v2:
            st = "agrees"
        elif c is not None:
            st = "codex note"
        else:
            st = "?"
        if st != "agrees":
            status.append(f"{f}:{st}")
        out["codex_" + f] = c or ""
    out["status"] = "codex-only row" if r["p2"] == "none" else ("; ".join(status) or "agrees")
    rows.append(out)

cols = list(rows[0].keys())
with open(HERE / "star_catalogue_joined.tsv", "w", encoding="utf-8", newline="\n") as fh:
    w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(rows)
json.dump(rows, open(HERE / "star_catalogue_joined.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("joined rows:", len(rows), "| rows with any non-agreeing field:", sum(1 for x in rows if x["status"] != "agrees"),
      "| fields still '?':", sum(x["status"].count(":?") for x in rows))

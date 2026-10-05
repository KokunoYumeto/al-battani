"""Two-way check of the geographical tables (regions and cities): Part III (codex, Maghribi abjad) against Part II
(Nallino's values and notes). For every Part III row linked to a Part II row, longitude and latitude (degrees,
minutes) must equal Part II or the codex reading in Nallino's note, and every structured codex reading must equal
the Part III reading. A blank minutes cell counts as 0 when Part II prints 0 (counted separately).
Exit code 1 on any unledgered difference."""
import csv, re, sys
from pathlib import Path

MAGHRIBI = {"ا": 1, "ب": 2, "ج": 3, "د": 4, "ه": 5, "و": 6, "ز": 7, "ح": 8, "ط": 9, "ى": 10, "ي": 10,
            "ك": 20, "ل": 30, "م": 40, "ن": 50, "ص": 60, "ع": 70, "ف": 80, "ض": 90, "ق": 100,
            "ر": 200, "س": 300, "ت": 400, "ث": 500, "خ": 600, "ذ": 700, "ظ": 800, "غ": 900, "ش": 1000}


def abjad(raw):
    """Value of a Maghribi abjad cell; {fnN} ignored, {rd:printed=read} uses the reading, {0} and {zero:..} are 0."""
    raw = re.sub(r"\{rd:.=(.)\}", r"\1", re.sub(r"\{fn\d+\}", "", raw)).replace("‌", "").strip()   # ZWNJ: print only
    if raw == "":
        return None
    if raw == "{0}" or re.fullmatch(r"\{zero:[^}]*\}", raw):
        return 0
    return sum(MAGHRIBI[c] for c in raw.replace("{0}", ""))


def latin_num(v):
    v = re.sub(r"[*°′']", "", v).strip()
    return int(v) if v.isdigit() else None

HERE = Path(__file__).resolve().parent
FIELDS = ("lon_d", "lon_m", "lat_d", "lat_m")


def read(name):
    return list(csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t"))


def codex_values(v):
    return {int(x) for x in v.split("|")}


p3 = [r for r in read("geo_p3.tsv") if r["kind"] == "row"]
p2 = {r["no"]: r for r in read("geo_p2.tsv") if r["kind"] in ("L", "R", "T")}   # T: table rows with a notes column
notes = {}
for r in read("geo_p2_notes.tsv"):
    for item in filter(None, r["codex"].split(";")):
        if "=" in item:
            k, v = item.split("=", 1)
            notes.setdefault(r["no"], {})[k] = v
ledger = {r["where"].split(" | ")[0] for r in read("geo_discrepancies.tsv")}

problems, agree, explained, blank = [], 0, 0, 0
for r in p3:
    if r["p2"] == "none":
        continue
    q = p2.get(r["p2"])
    tag = f"{r['pdf']} {r['line']} {r['p2']}"
    if q is None:
        problems.append(f"{tag}: Part II row not transcribed yet"); continue
    cod = notes.get(r["p2"], {})
    for f in FIELDS:
        a = abjad(r[f]); b = latin_num(q[f])
        if a is None and f.endswith("_m") and b == 0 and f not in cod:
            blank += 1; continue
        if f in cod and a not in codex_values(cod[f]):
            problems.append(f"{tag} {f}: Part III {a} but Nallino's codex reading {cod[f]}")
        elif a == b:
            agree += 1
        elif f in cod:
            explained += 1
        else:
            problems.append(f"{tag} {f}: Part III {a} vs Part II {b}, no codex note")

print(f"geography rows checked: {len(p3)}; cells agreeing with Part II: {agree}; explained by Nallino's codex notes: {explained}; "
      f"blank minutes cells (Part II 0): {blank}")
known = [x for x in problems if x.split(":")[0] in ledger]
new = [x for x in problems if x.split(":")[0] not in ledger]
print(f"differences already in the ledger: {len(known)}; new problems: {len(new)}")
for x in new:
    print("  ", x)
if __name__ == "__main__":
    sys.exit(1 if new else 0)

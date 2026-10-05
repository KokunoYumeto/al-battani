"""Two-way check of the star catalogue: Part III (codex, Maghribi abjad) against Part II (Nallino's values + notes).
For every Part III star row linked to a Part II star (longitude, latitude, magnitude and direction; a blank direction
cell repeats the direction above it, a bracket covers its rows):
  - a field that differs from Part II must have a codex reading in Nallino's notes equal to the Part III value;
  - a codex reading in the notes must equal the Part III value (so the notes also check the Arabic reading).
Prints a per-page summary and every problem. Exit code 1 if any problem."""
import csv, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAGHRIBI = {"ا": 1, "ب": 2, "ج": 3, "د": 4, "ه": 5, "و": 6, "ز": 7, "ح": 8, "ط": 9, "ى": 10, "ي": 10,
            "ك": 20, "ل": 30, "م": 40, "ن": 50, "ص": 60, "ع": 70, "ف": 80, "ض": 90, "ق": 100,
            "ر": 200, "س": 300, "ت": 400, "ث": 500, "خ": 600, "ذ": 700, "ظ": 800, "غ": 900, "ش": 1000}
FIELDS = ("lon_d", "lon_m", "lat_d", "lat_m")


def abjad(raw):
    raw = re.sub(r"\{rd:.=(.)\}", r"\1", re.sub(r"\{fn\d+\}", "", raw)).strip()   # {rd:printed=read}: value of the reading
    if raw == "{0}" or re.fullmatch(r"\{zero:[^}]*\}", raw):          # {zero:لا}: a word printed for "none", read as 0
        return 0
    return sum(MAGHRIBI[c] for c in raw.replace("{0}", ""))         # a zero sign after a letter (ر{0} = 200) adds nothing


def latin_num(v):
    v = re.sub(r"[*°′']", "", v).strip()
    return int(v) if v.isdigit() else None


def p3_mag(raw):
    raw = re.sub("[ً-ْٰ]", "", re.sub(r"\{fn\d+\}", "", raw))   # harakat and footnote marks do not affect the value
    parts = raw.split()
    if not parts:
        return None
    words = {"غمامي": "nebulosa", "سحابي": "nebulosa", "مظلم": "obscura", "مشهور": "conspicua"}
    q = {"كبير": " magna", "صغير": " parva"}
    if parts[0] in q:                                        # a qualifier printed without its numeral (Centaurus 11)
        return "?" + q[parts[0]]
    if parts[0] in words:                                    # e.g. غماميّ صغير = "nebulosa parva"
        return words[parts[0]] + (q.get(parts[1], "?" + parts[1]) if len(parts) > 1 else "")
    return str(abjad(parts[0])) + (q.get(parts[1], "?" + parts[1]) if len(parts) > 1 else "")


def read(name):
    return list(csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t"))


p3 = [r for r in read("p3_stars.tsv") if r["kind"] == "star"]
p2 = {(r["section"], r["no"]): r for r in read("p2_stars.tsv") if r["kind"] == "star"}
notes = {}
for r in read("p2_notes.tsv"):
    cod = {}
    for item in filter(None, r["codex"].split(";")):
        if "=" in item:
            k, v = item.split("=", 1); cod[k] = v
    notes[(r["section"], r["no"])] = cod

ledger = {(r["where"].split(" | ")[0]) for r in csv.DictReader(open(HERE / "discrepancies.tsv", encoding="utf-8"), delimiter="	")}
DIRS = {"ش": "b", "ج": "a", "{0}": "0"}                      # Part III direction letters
PLAGA = {"b": "b", "a": "a", "0": "0", "bor.": "b", "austr.": "a"}   # Part II plaga (first rows spell it out)
problems, agree, explained, codex_only = [], 0, 0, 0
cur_dir = None


def codex_values(v):
    """A note may give alternative codex readings, e.g. lon_d=342|347 ("342° vel 347°")."""
    return {int(x) for x in v.split("|")}
for r in p3:
    d = r["dir"].strip()
    m = re.fullmatch(r"\{BR:(.+):(\d+)\}", d)
    if m:
        cur_dir = {"الشمال": "b", "الجنوب": "a"}[m.group(1)]
    elif d not in ("", "{BR}"):
        cur_dir = DIRS[d]
    # a blank cell repeats the direction above it, as does every row under a bracket
    if r["p2"] == "none":                                   # a codex row Nallino left out of Part II (e.g. a repeated star)
        codex_only += 1; continue
    if not r["p2"]:
        problems.append(f"{r['pdf']} {r['line']}: no Part II link"); continue
    sec, no = r["p2"].split()
    q = p2.get((sec, no))
    if q is None:
        problems.append(f"{r['pdf']} {r['line']}: Part II row {r['p2']} not transcribed yet"); continue
    cod = notes.get((sec, no), {})
    for f in FIELDS:
        a = abjad(r[f]); b = latin_num(q[f])
        if f in cod and a not in codex_values(cod[f]):
            problems.append(f"{r['pdf']} {r['line']} {r['p2']} {f}: Part III {a} but Nallino's codex reading {cod[f]}")
        elif a == b:
            agree += 1
        elif f in cod:
            explained += 1
        else:
            problems.append(f"{r['pdf']} {r['line']} {r['p2']} {f}: Part III {a} vs Part II {b}, no codex note")
    m3 = p3_mag(r["mag"]); m2 = q["mag"].replace("*", "").strip()
    if "mag" in cod and cod["mag"] != m3:
        problems.append(f"{r['pdf']} {r['line']} {r['p2']} magnitude: Part III {m3} but Nallino's codex reading {cod['mag']}")
    elif m3 == m2:
        agree += 1
    elif "mag" in cod:
        explained += 1
    else:
        problems.append(f"{r['pdf']} {r['line']} {r['p2']} magnitude: Part III {m3} vs Part II {m2}" + (f" (note: {cod['mag']})" if "mag" in cod else ", no codex note"))
    d2 = PLAGA.get(q["plaga"].replace("*", "").strip(), "?")
    dc = {"N": "b", "S": "a"}.get(cod.get("dir"))
    if dc is not None and dc != cur_dir:
        problems.append(f"{r['pdf']} {r['line']} {r['p2']} dir: Part III {cur_dir} but Nallino's codex reading {dc}")
    elif cur_dir == d2:
        agree += 1
    elif dc is not None:
        explained += 1
    else:
        problems.append(f"{r['pdf']} {r['line']} {r['p2']} dir: Part III {cur_dir} vs Part II {d2}, no codex note")
print(f"star rows checked: {len(p3) - codex_only}; cells agreeing with Part II: {agree}; cells explained by Nallino's codex notes: {explained}"
      + (f"; codex-only rows (not in Part II): {codex_only}" if codex_only else ""))
known = [x for x in problems if x.split(":")[0] in ledger]
new = [x for x in problems if x.split(":")[0] not in ledger]
print(f"differences already in the discrepancy ledger: {len(known)}; new problems: {len(new)}")
for x in new:
    print("  ", x)
if __name__ == "__main__":                                 # importable by build_joined.py
    sys.exit(1 if new else 0)

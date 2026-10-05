"""Two-way check of the chronological tables: Part III (codex, Maghribi abjad) against Part II (Nallino's values and the
codex readings he reports in his notes, Part II pp. 191-198). Kings: years of reign and running total; intervals between
the eras: years; caliphs: years, months and days of the reign and of the running total.
For every Part III row linked to a Part II row, every number must equal Part II or the codex reading in Nallino's notes,
and every structured codex reading must equal the Part III reading. Exit code 1 on any unledgered difference."""
import csv, re, sys
from pathlib import Path

MAGHRIBI = {"ا": 1, "ب": 2, "ج": 3, "د": 4, "ه": 5, "و": 6, "ز": 7, "ح": 8, "ط": 9, "ى": 10, "ي": 10,
            "ك": 20, "ل": 30, "م": 40, "ن": 50, "ص": 60, "ع": 70, "ف": 80, "ض": 90, "ق": 100,
            "ر": 200, "س": 300, "ت": 400, "ث": 500, "خ": 600, "ذ": 700, "ظ": 800, "غ": 900, "ش": 1000}
HERE = Path(__file__).resolve().parent
FIELDS = ("reg_y", "reg_m", "reg_d", "sum_y", "sum_m", "sum_d")
# Part III p. 230, footnote 8: on f. 155,v. of the codex (from Zeno, row R16 of PDF 922, through the left panel) the
# copyist left the Eastern hundreds unconverted, «ergo hic ض = 800, ظ = 900». Only the hundreds letter (the first of a
# number) takes the Eastern value; a ض after it keeps the Maghribi 90 (ظضب = 992, ظصد = 964).
EAST_HUNDREDS = {"ض": 800, "ظ": 900}
EAST_ROWS = {("922", "R16")} | {("922", f"L{i:02}") for i in range(1, 19)}


def abjad(raw, east=False):
    """Value of a Maghribi abjad cell; {fnN} ignored, {rd:printed=read} uses the reading, {0} and {zero:..} are 0.
    A number written as two groups («ا ح», Part III p. 230) is thousands and the rest: 1 x 1000 + 8.
    east=True: the first letter takes the Eastern hundreds value of EAST_HUNDREDS (f. 155,v.)."""
    raw = re.sub(r"\{rd:.=(.)\}", r"\1", re.sub(r"\{fn\d+\}", "", raw)).replace("‌", "").strip()
    if raw == "":
        return None
    if raw == "{0}" or re.fullmatch(r"\{zero:[^}]*\}", raw):
        return 0
    if " " in raw:
        head, tail = raw.split(" ", 1)
        return 1000 * abjad(head, east) + abjad(tail, east)
    letters = raw.replace("{0}", "")
    return sum(EAST_HUNDREDS[c] if east and i == 0 and c in EAST_HUNDREDS else MAGHRIBI[c] for i, c in enumerate(letters))


def latin_num(v):
    v = re.sub(r"[*°′']", "", v).strip()
    return int(v) if v.isdigit() else None


def read(name):
    return list(csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t"))


def codex_values(v):
    return {int(x) for x in v.split("|")}


p3 = [r for r in read("chr_p3.tsv") if r["kind"] == "row"]
p2 = {r["no"]: r for r in read("chr_p2.tsv") if r["kind"] in ("L", "R", "T") and r["no"]}
codex = {}
for r in read("chr_p2_codex.tsv"):
    codex.setdefault(r["no"], {})[r["field"]] = r["codex"]
ledger = {r["where"].split(" | ")[0] for r in read("chr_discrepancies.tsv")}

problems, agree, explained = [], 0, 0
for r in p3:
    if r["p2"] in ("", "none"):
        continue
    q = p2.get(r["p2"])
    tag = f"{r['pdf']} {r['line']} {r['p2']}"
    if q is None:
        problems.append(f"{tag}: Part II row not transcribed yet"); continue
    cod = codex.get(r["p2"], {})
    east = (r["pdf"], r["line"]) in EAST_ROWS
    for f in FIELDS:
        a = abjad(r[f], east); b = latin_num(q[f])
        if a is None and b is None and f not in cod:
            continue
        if f in cod and a not in codex_values(cod[f]):
            problems.append(f"{tag} {f}: Part III {a} but Nallino's codex reading {cod[f]}")
        elif a == b:
            agree += 1
        elif f in cod:
            explained += 1
        else:
            problems.append(f"{tag} {f}: Part III {a} vs Part II {b}, no codex note")

print(f"chronology rows checked: {len(p3)}; numbers agreeing with Part II: {agree}; explained by Nallino's codex notes: {explained}")
known = [x for x in problems if x.split(":")[0] in ledger]
new = [x for x in problems if x.split(":")[0] not in ledger]
print(f"differences already in the ledger: {len(known)}; new problems: {len(new)}")
for x in new:
    print("  ", x)
if __name__ == "__main__":
    sys.exit(1 if new else 0)

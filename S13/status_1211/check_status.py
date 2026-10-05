"""Two-way check of the 1211 status tables: Part III (codex, Maghribi abjad) against Part II (Nallino's values and notes).
For every Part III row linked to a Part II star, each field (declination, direction, meridian altitude h, half-arc P,
culmination A, rising B, setting C, magnitude) must equal Part II or the codex reading in Nallino's note, and every
structured codex reading must equal the Part III reading.
Information only (not a failure): the arithmetic h = 54 deg +/- declination and P = 90 deg +/- asin(tan 36 deg tan dec),
for the latitude of al-Raqqa (36 deg), computed from the Part III values; deviations over 2' are listed.
Exit code 1 on any unledgered difference."""
import csv, math, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAGHRIBI = {"ا": 1, "ب": 2, "ج": 3, "د": 4, "ه": 5, "و": 6, "ز": 7, "ح": 8, "ط": 9, "ى": 10, "ي": 10,
            "ك": 20, "ل": 30, "م": 40, "ن": 50, "ص": 60, "ع": 70, "ف": 80, "ض": 90, "ق": 100,
            "ر": 200, "س": 300, "ت": 400, "ث": 500, "خ": 600, "ذ": 700, "ظ": 800, "غ": 900, "ش": 1000}
NUM = ("dec_d", "dec_m", "alt_d", "alt_m", "half_d", "half_m", "cul_d", "cul_m", "ris_d", "ris_m", "set_d", "set_m")
DIRS = {"ش": "b", "ج": "a", "{0}": "0"}
PLAGA = {"B": "b", "A": "a", "0": "0"}


def abjad(raw):
    raw = re.sub(r"\{rd:.=(.)\}", r"\1", re.sub(r"\{fn\d+\}", "", raw)).strip()
    if raw == "":
        return None
    if raw == "{0}" or re.fullmatch(r"\{zero:[^}]*\}", raw):
        return 0
    return sum(MAGHRIBI[c] for c in raw.replace("{0}", ""))


def latin_num(v):
    v = re.sub(r"[*°′']", "", v).strip()
    return int(v) if v.isdigit() else None


def read(name):
    return list(csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t"))


def codex_values(v):
    return {int(x) for x in v.split("|")}


p3 = [r for r in read("st_p3.tsv") if r["kind"] == "star"]
p2 = {r["no"]: r for r in read("st_p2.tsv") if r["kind"] == "star"}
notes = {}
for r in read("st_p2_notes.tsv"):
    for item in filter(None, r["codex"].split(";")):
        if "=" in item:
            k, v = item.split("=", 1)
            notes.setdefault(r["no"], {})[k] = v
ledger = {r["where"].split(" | ")[0] for r in read("st_discrepancies.tsv")}

problems, agree, explained, arith = [], 0, 0, []
cur = None
for r in p3:
    d = r["dir"].strip()
    if d:
        cur = DIRS[d]
    q = p2.get(r["p2"])
    if q is None:
        problems.append(f"{r['pdf']} {r['line']}: Part II star {r['p2']!r} not transcribed yet"); continue
    cod = notes.get(r["p2"], {})
    tag = f"{r['pdf']} {r['line']} {r['p2']}"
    for f in NUM:
        a = abjad(r[f]); b = latin_num(q[f])
        if a is None and b is None:
            continue                                     # e.g. P, B, C of the circumpolar stars
        if f in cod and a not in codex_values(cod[f]):
            problems.append(f"{tag} {f}: Part III {a} but Nallino's codex reading {cod[f]}")
        elif a == b:
            agree += 1
        elif f in cod:
            explained += 1
        else:
            problems.append(f"{tag} {f}: Part III {a} vs Part II {b}, no codex note")
    d2 = PLAGA.get(q["plaga"].replace("*", "").strip(), "?"); dc = {"N": "b", "S": "a"}.get(cod.get("dir"))
    if dc is not None and dc != cur:
        problems.append(f"{tag} dir: Part III {cur} but Nallino's codex reading {dc}")
    elif cur == d2:
        agree += 1
    elif dc is not None:
        explained += 1
    else:
        problems.append(f"{tag} dir: Part III {cur} vs Part II {d2}, no codex note")
    m3 = abjad(re.sub(r"\s.*", "", r["mag"])) if r["mag"] else None
    m2 = latin_num(q["mag"]); mc = cod.get("mag")
    if m3 is None and mc is None:
        pass                                            # no magnitude column in the codex (third table, from fol. 238,v.)
    elif mc is not None and int(mc) != m3:
        problems.append(f"{tag} magnitude: Part III {m3} but Nallino's codex reading {mc}")
    elif m3 == m2:
        agree += 1
    elif mc is not None:
        explained += 1
    else:
        problems.append(f"{tag} magnitude: Part III {m3} vs Part II {m2}, no codex note")
    # arithmetic (information): latitude 36 deg
    dec = abjad(r["dec_d"]); decm = abjad(r["dec_m"]); alt = abjad(r["alt_d"]); altm = abjad(r["alt_m"])
    sign = d2 if d2 in ("a", "b") else cur              # the codex often leaves the direction blank: use Nallino's plaga
    if None not in (dec, decm, alt, altm) and sign in ("a", "b"):
        s = 1 if sign == "b" else -1
        dmin = dec * 60 + decm
        h_exp = 54 * 60 + s * dmin
        if abs(h_exp - (alt * 60 + altm)) > 2:
            arith.append(f"{tag} h = 54 deg {'+' if s > 0 else '-'} dec gives {h_exp // 60} {h_exp % 60:02d}; Part III {alt} {altm:02d}")
        hd, hm = abjad(r["half_d"]), abjad(r["half_m"])
        x = math.tan(math.radians(36)) * math.tan(math.radians(dmin / 60))
        if None not in (hd, hm) and x < 1:
            p_exp = round((90 + s * math.degrees(math.asin(x))) * 60)
            if abs(p_exp - (hd * 60 + hm)) > 2:
                arith.append(f"{tag} P from dec gives {p_exp // 60} {p_exp % 60:02d}; Part III {hd} {hm:02d}")

print(f"status rows checked: {len(p3)}; cells agreeing with Part II: {agree}; explained by Nallino's codex notes: {explained}")
known = [x for x in problems if x.split(":")[0] in ledger]
new = [x for x in problems if x.split(":")[0] not in ledger]
print(f"differences already in the ledger: {len(known)}; new problems: {len(new)}")
for x in new:
    print("  ", x)
if "-a" in sys.argv:
    print(f"arithmetic deviations over 2' (information): {len(arith)}")
    for x in arith:
        print("   ", x)
if __name__ == "__main__":
    sys.exit(1 if new else 0)

"""Check of the diagram of the seven climes: Part III p. 243 (codex figure, Maghribi abjad) against Part II p. 92
(Nallino's Latin figure) and against Nallino's table of the codex wind names (Part II p. 234).
1. Every ring cell and axis number of Part III, decoded, against the Latin figure at the same line and ring.
2. Every wind name of Part III against the codex form in Nallino's table (azimuth from the south = t - 90).
3. The Latin values against the amplitudes computed from sin A = sin d / cos phi, with al-Battani's obliquity 23;35
   and the latitudes of the climes that Nallino gives in his note (Part II p. 232): a check of the transcription of
   Part II, reported but not required to agree.
Every difference in 1 and 2 must be in climates_discrepancies.tsv; exit code 1 otherwise. --list prints all of them."""
import csv, math, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAGHRIBI = {"ا": 1, "ب": 2, "ج": 3, "د": 4, "ه": 5, "و": 6, "ز": 7, "ح": 8, "ط": 9, "ى": 10, "ي": 10,
            "ك": 20, "ل": 30, "م": 40, "ن": 50, "ص": 60, "ع": 70, "ف": 80, "ض": 90, "ق": 100,
            "ر": 200, "س": 300, "ت": 400, "ث": 500, "خ": 600, "ذ": 700, "ظ": 800, "غ": 900, "ش": 1000}


def abjad(raw):
    """Value of a Maghribi abjad cell (as in ../chronology/check_chr.py); {0} is the zero sign."""
    raw = raw.strip()
    return 0 if raw == "{0}" else sum(MAGHRIBI[c] for c in raw)


def read(name):
    return list(csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t"))


def latin(v):
    """«24°», «41′», «13h / 30m», «2», «VII» -> number; hours with minutes -> hours + minutes/60."""
    v = v.strip()
    m = re.fullmatch(r"(\d+)h(?: / (\d+)m)?", v)
    if m:
        return int(m.group(1)) + (int(m.group(2)) / 60 if m.group(2) else 0)
    roman = {"I": 1, "IV": 4, "VII": 7}
    if v in roman:
        return roman[v]
    v = re.sub(r"[°′']", "", v)
    return int(v) if v.isdigit() else None


def arabic_hours(v):
    """«يج ل» = 13 hours and 30 (minutes): the hours, a space, the half hour as ل."""
    parts = v.split()
    return abjad(parts[0]) + (abjad(parts[1]) / 60 if len(parts) > 1 else 0)


p3, p2 = read("climates_p3.tsv"), read("climates_p2.tsv")
names = {r["az"]: r for r in read("climates_names_p2.tsv")}
ledger = {r["where"]: r for r in read("climates_discrepancies.tsv")} if (HERE / "climates_discrepancies.tsv").exists() else {}
L = {(r["kind"], r["t"], r["ring"], r["side"]): r["text"] for r in p2}

found, agree = [], 0
for r in p3:
    key = (r["kind"], r["t"], r["ring"], r["side"])
    if r["kind"] == "cell":
        a, b = abjad(r["text"]), latin(L[key])
        where = f"cell {r['t']} r{r['ring']} {r['side']}"
    elif r["kind"] == "axis":
        if r["text"] in ("الاقليم", "ساعاته"):
            continue                                          # the words الاقليم (clima) and ساعاته (horae eius)
        if r["t"] == "90":
            # top axis, by role: the Arabic has «الاقليم | ordinal» or «number | latitude» from right to left (cw | ccw);
            # the Latin «number | clima» or «number | latitude» from left to right (ccw | cw)
            ordinal = {"الاول": 1, "الرابع": 4, "السابع": 7}
            if r["text"] in ordinal:
                a, b = ordinal[r["text"]], latin(L[(r["kind"], r["t"], r["ring"], "ccw")])
            elif r["side"] == "cw":                           # the number of the clime
                a, b = abjad(r["text"]), latin(L[(r["kind"], r["t"], r["ring"], "ccw")])
            else:                                             # the latitude
                a, b = abjad(r["text"]), latin(L[(r["kind"], r["t"], r["ring"], "cw")])
        elif r["t"] == "270":
            a, b = arabic_hours(r["text"]), latin(L[key])
        else:
            a, b = abjad(r["text"]), latin(L[key])
        where = f"axis {r['t']} r{r['ring']} {r['side']}"
    elif r["kind"] == "wind":
        az = (float(r["t"]) - 90) % 360
        key_az = f"{az:g}".replace(".5", " 1/2")
        a, b = r["text"].replace("{stroke}", "..."), names[key_az]["codex"]
        where = f"wind {r['t']}"
    else:
        continue
    if a == b:
        agree += 1
        continue
    found.append((where, r["text"], a, b))

open_ = [f for f in found if f[0] not in ledger]
print(f"agree {agree}, differ {len(found)} (ledgered {len(found) - len(open_)}, open {len(open_)})")
for where, raw, a, b in (found if "--list" in sys.argv else open_):
    print(f"  {where}: Part III {raw} = {a}  |  Part II {b}" + ("" if where in ledger else "   << not in the ledger"))
stale = [w for w in ledger if w not in {f[0] for f in found}]
for w in stale:
    print("  ledger entry without a difference:", w)

# 3. computed amplitudes (al-Battani's obliquity; Nallino's latitudes of the climes, Part II p. 232)
EPS = 23 + 35 / 60
PHI = [16 + 39 / 60, 24 + 5 / 60, 30 + 40 / 60, 36 + 22 / 60, 41 + 15 / 60, 45 + 22 / 60, 48 + 53 / 60]
LAM = {"12": 30, "21": 60, "24": 90}                          # first value of each column -> longitude of the sign
bad, worst = 0, 0.0
for t in ("22.5", "45", "67.5"):
    lam = LAM[L[("cell", t, "1", "deg")].rstrip("°")]
    d = math.asin(math.sin(math.radians(EPS)) * math.sin(math.radians(lam)))
    for k in range(1, 8):
        A = math.degrees(math.asin(math.sin(d) / math.cos(math.radians(PHI[k - 1]))))
        lat = latin(L[("cell", t, str(k), "deg")]) + latin(L[("cell", t, str(k), "min")]) / 60
        worst = max(worst, abs(A - lat) * 60)
        if abs(A - lat) * 60 > 2.0:
            bad += 1
            print(f"  computed: line {t} r{k}: {A:.4f} = {int(A)}°{(A - int(A)) * 60:.1f}′ vs Part II {lat:.4f}")
print(f"Part II against the computed amplitudes: {21 - bad} of 21 within 2′ (largest difference {worst:.1f}′)")
sys.exit(1 if open_ or stale else 0)

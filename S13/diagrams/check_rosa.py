"""Check of the astrological figure: Part III p. 244 (the codex figure, as printed, codex errors kept) against Part II
p. 299 (Nallino's figure, emended «ad fidem versionis Francofurtensis Tetrabibli», Part II p. 309).
Compared item by item: the five terms of each sign (planet and degrees), the triplicity lords by day and by night, the
three faces, the house and the exaltation (planet and degrees), and the sign names. Planets are compared by identity
(Arabic names, Latin names and Nallino's symbols mapped to one key); degrees by value (Maghribi abjad against Western
numerals). Also reported: the sum of the five terms of each sign (30 in a consistent table).
Every difference must be in rosa_discrepancies.tsv (rows «note: ...» are notes on Nallino's text, not
compared items); exit code 1 otherwise. --list prints all of them."""
import csv, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAGHRIBI = {"ا": 1, "ب": 2, "ج": 3, "د": 4, "ه": 5, "و": 6, "ز": 7, "ح": 8, "ط": 9, "ى": 10, "ي": 10,
            "ك": 20, "ل": 30, "م": 40, "ن": 50, "ص": 60, "ع": 70, "ف": 80, "ض": 90, "ق": 100}
PLANET = {
    "شمس": "Sun", "قمر": "Moon", "عطارد": "Mercury", "زهرة": "Venus", "مريخ": "Mars", "بهرام": "Mars",
    "مشتري": "Jupiter", "مشترب": "Jupiter", "زحل": "Saturn", "رأس": "Head", "ذنب": "Tail",
    "Sol": "Sun", "Luna": "Moon", "Mercurius": "Mercury", "Venus": "Venus", "Verus": "Venus", "Venns": "Venus",
    "Mars": "Mars", "Iupiter": "Jupiter", "Saturnus": "Saturn",
    "☉": "Sun", "☽": "Moon", "☿": "Mercury", "♀": "Venus", "♂": "Mars", "♃": "Jupiter", "♄": "Saturn",
    "☊": "Head", "☋": "Tail", "": "",
}
SIGN = {"حمل": "Aries", "ثور": "Taurus", "جوزاه": "Gemini", "سرطان": "Cancer", "اسد": "Leo", "سنبلة": "Virgo",
        "ميزان": "Libra", "عقرب": "Scorpio", "قوس": "Sagittarius", "جدي": "Capricorn", "دلو": "Aquarius", "حوت": "Pisces",
        "Scorpius": "Scorpio", "Capricornus": "Capricorn"}


def read(name):
    return list(csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t"))


def deg(v):
    v = v.strip()
    if v in ("{0}", "0°"):
        return 0
    if re.fullmatch(r"\d+°?", v):
        return int(v.rstrip("°"))
    return sum(MAGHRIBI[c] for c in v)


def planets(text):
    return [PLANET[w] for w in text.split()]


p3, p2 = read("rosa_p3.tsv"), read("rosa_p2.tsv")
ledger = {r["where"]: r for r in read("rosa_discrepancies.tsv")} if (HERE / "rosa_discrepancies.tsv").exists() else {}
key = lambda r: (r["kind"], r["sign"], r["idx"])
L = {key(r): r for r in p2}
found, agree = [], 0


def compare(where, a, b, raw):
    global agree
    if a == b:
        agree += 1
    else:
        found.append((where, raw, a, b))


for r in p3:
    k, s, i = r["kind"], r["sign"], r["idx"]
    if k == "term":
        q = L[key(r)]
        compare(f"term {s} {i} planet", PLANET[r["planet"]], PLANET[q["planet"]], r["planet"])
        compare(f"term {s} {i} degrees", deg(r["value"]), deg(q["value"]), r["value"])
    elif k == "trip":
        compare(f"trip {s} {'day' if i == '1' else 'night'}", planets(r["text"]), planets(L[key(r)]["text"]), r["text"])
    elif k == "face":
        compare(f"face {s} {i}", PLANET[r["planet"]], PLANET[L[key(r)]["planet"]], r["planet"])
    elif k == "house":
        compare(f"house {s}", PLANET[r["planet"]], PLANET[L[key(r)]["planet"]], r["planet"])
    elif k == "exalt":
        q = L[key(r)]
        compare(f"exalt {s} planet", PLANET[r["planet"]], PLANET[q["planet"]], r["planet"])
        compare(f"exalt {s} degrees", deg(r["value"]), deg(q["value"]), r["value"])
signs3 = sorted(SIGN.get(r["text"], r["text"]) for r in p3 if r["kind"] == "sign")
signs2 = sorted(SIGN.get(r["text"], r["text"]) for r in p2 if r["kind"] == "sign")
compare("sign names", signs3, signs2, "")

open_ = [f for f in found if f[0] not in ledger]
print(f"agree {agree}, differ {len(found)} (ledgered {len(found) - len(open_)}, open {len(open_)})")
for where, raw, a, b in (found if "--list" in sys.argv else open_):
    print(f"  {where}: Part III {raw} = {a}  |  Part II {b}" + ("" if where in ledger else "   << not in the ledger"))
stale = [w for w in ledger if w not in {f[0] for f in found} and not w.startswith("note:")]   # notes on the text
for w in stale:
    print("  ledger entry without a difference:", w)

for name, rows_ in (("Part III", p3), ("Part II", p2)):
    sums = {}
    for r in rows_:
        if r["kind"] == "term":
            sums[r["sign"]] = sums.get(r["sign"], 0) + deg(r["value"])
    off = {s: v for s, v in sums.items() if v != 30}
    print(f"{name}: terms sum to 30 in {12 - len(off)} of 12 signs" + (f"; {off}" if off else ""))
sys.exit(1 if open_ or stale else 0)

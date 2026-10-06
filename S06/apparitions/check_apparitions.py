"""Check of Nallino's Part II pp. 142-143 (the elongations of the planets from the true Sun at their apparitions and
occultations, latitude 36° 0′), from apparitions_p2.tsv, apparitions_pages.tsv and apparitions_readings.tsv.
1. The anomalies in the heads of p. 143 (Maghribi abjad) equal their Latin.
2. Nallino's corrections. The printed numbers are «quantitates proxime a Schiaparelli restitutae» (Part II p. 262).
   Nallino later compared Theon's tables for the fourth clime and the Latin Almagest printed by Liechtenstein (Venice
   1515), listed their differences from the printed numbers (pp. 267-268: numbers in brackets false, in italics
   uncertain) and ruled (p. 269) that all readings of both that are neither false nor uncertain be adopted, and the
   degrees 2° of the evening setting of Venus restored. apparitions_readings.tsv holds these lists; the corrected
   table applies them. Every corrected cell needs a ledger entry of kind «noted».
3. Identities of the corrected table. The angle of the ecliptic with the horizon is the same at points equally distant
   from an equinox, and at a rising point and the opposite setting one (Nallino p. 259). With the latitude neglected,
   as for Mars (p. 260), the apparitions at λ and -λ are equal, so are the occultations, and the apparition at λ equals
   the occultation at λ + 180°. Jupiter's table is symmetric about the equinoxes as well.
4. The computation. Ptolemy's rule (Nallino p. 258): elongation = arcus visionis / sin θ ∓ latitude · cot θ, θ the
   angle of the ecliptic with the horizon at the beginning of the sign when it rises (E) or sets (W), at φ = 36° and
   obliquity 23° 35′. The arcus visionis are 13° (Saturn), 9° (Jupiter), 14° 30′ (Mars), 7° and 5° (Venus), 12°
   (Mercury). The latitude term: Saturn and Jupiter k cos(λ - λN), with the northern limits λN of al-Battani's
   apogees, 194° 28′ and 184° 28′ (Nallino p. 259); Mars none; Venus and Mercury kc cos λ + ks sin λ. The
   coefficients are fitted to each corrected column, setting aside at most three values that depart by more than three
   times the robust spread (and 10′). The horizon of each column is the one its values follow; the first two columns
   of Venus and Mercury follow the opposite horizon to that of their heads, and so does the third of Venus. The last
   column of Venus is not reproduced with either horizon and is not checked.
A corrected value more than LIST minutes from its computation is listed. Every listed difference must be in
apparitions_discrepancies.tsv. --list shows the ledgered entries too, --stats the computation of each column."""
import csv, math, sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
EPS, PHI, LIST = 23 + 35 / 60, 36.0, 30
SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpius", "Sagittarius", "Capricornus",
         "Aquarius", "Pisces"]
LAM = np.arange(12) * 30.0
MODEL = {"sat_app": ("E", 13.0, "sat"), "sat_occ": ("W", 13.0, "sat"), "jup_app": ("E", 9.0, "jup"),
         "jup_occ": ("W", 9.0, "jup"), "mars_app": ("E", 14.5, None), "mars_occ": ("W", 14.5, None),
         "ven_ort_vesp": ("E", 7.0, "free"), "ven_occ_mat": ("W", 7.0, "free"), "ven_ort_mat": ("W", 5.0, "free"),
         "mer_ort_vesp": ("E", 12.0, "free"), "mer_occ_mat": ("W", 12.0, "free"), "mer_ort_mat": ("E", 12.0, "free"),
         "mer_occ_vesp": ("W", 12.0, "free")}
HEAD = {"app": "E", "occ": "W", "ort_vesp": "W", "occ_mat": "E", "ort_mat": "E", "occ_vesp": "W"}
LIMIT = {"sat": 194 + 28 / 60, "jup": 184 + 28 / 60}
SOURCE = {"Theon": "Theon (Nallino p. 268)", "Almagest 1515": "the Latin Almagest of 1515 (p. 267)",
          "Nallino p. 269": "Nallino (p. 269)"}
ABJAD = dict(zip("ابجدهوزحطيكلمنصعفضقرستثخذظغش",
                 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800,
                  900, 1000]))


def read(name):
    return list(csv.DictReader(open(HERE / name, encoding="utf-8"), delimiter="\t"))


def angle(lam, side):
    """the angle (degrees) of the ecliptic with the horizon when the point lam rises (E) or sets (W)"""
    l, e, ph = math.radians(lam), math.radians(EPS), math.radians(PHI)
    p = np.array([math.cos(l), math.sin(l) * math.cos(e), math.sin(l) * math.sin(e)])
    dec, ra = math.asin(p[2]), math.atan2(p[1], p[0])
    h = math.acos(-math.tan(ph) * math.tan(dec))
    lst = ra - h if side == "E" else ra + h
    zen = np.array([math.cos(ph) * math.cos(lst), math.cos(ph) * math.sin(lst), math.sin(ph)])
    pole = np.array([0.0, -math.sin(e), math.cos(e)])
    return math.degrees(math.acos(abs(float(np.dot(zen, pole)))))


ANG = {s: np.array([angle(l, s) for l in LAM]) for s in "EW"}


def dm(u):
    if isinstance(u, (float, np.floating)):
        u = round(float(u), 1)
        return f"{int(u // 60)}° {u % 60:.1f}′".replace(".0′", "′")
    return f"{u // 60}° {u % 60}′"


def num(s):
    """the numeral of a reading: the last number in it (an uncertain reading carries its letters before)"""
    return int(s.split()[-1])


# the printed table and the corrected one
R = read("apparitions_p2.tsv")
PAGE, PRINTED = {}, {}
for r in R:
    PRINTED.setdefault(r["column"], [None] * 12)[int(r["row"]) - 1] = int(r["d"]) * 60 + int(r["m"])
    PAGE[r["column"]] = r["ppage"]
READINGS = read("apparitions_readings.tsv")
CORRECTED = {c: list(v) for c, v in PRINTED.items()}
CORRECTIONS = {}            # (column, row index) -> (printed, corrected, [readings])
for col in PRINTED:
    for i, sign in enumerate(SIGNS):
        rd = [x for x in READINGS if x["column"] == col and x["sign"] == sign]
        if not rd:
            continue
        deg = {num(x["deg"]) for x in rd if x["deg"] and not x["deg_mark"]}
        mn = {num(x["min"]) for x in rd if x["min"] and not x["min_mark"]}
        restored = [num(x["deg"]) for x in rd if x["source"].startswith("Nallino")]
        if restored:
            deg = set(restored)
        assert len(deg) <= 1 and len(mn) <= 1, (col, sign, deg, mn)
        p = PRINTED[col][i]
        d = deg.pop() if deg else p // 60
        m = mn.pop() if mn else p % 60
        if d * 60 + m != p:
            CORRECTED[col][i] = d * 60 + m
            CORRECTIONS[(col, i)] = (p, d * 60 + m, rd)


def fit(col, values, side=None, arcus=None, robust=True):
    """the computation of a column fitted to `values` (minutes): returns the computed values (minutes), the
    coefficients (the arcus visionis first when arcus="free"; the latitude terms in degrees) and the mask of the values
    used"""
    m_side, m_arcus, lat = MODEL.get(col, ("E", None, "free"))
    side = side or m_side
    arcus = None if arcus == "free" else (arcus if arcus is not None else m_arcus)
    th = np.radians(ANG[side]); s, c = np.sin(th), np.cos(th)
    terms = [] if lat is None else [np.cos(np.radians(LAM - LIMIT[lat]))] if lat in LIMIT else \
        [np.cos(np.radians(LAM)), np.sin(np.radians(LAM))]
    cols = ([] if arcus is not None else [60 / s]) + [t * c / s * 60 for t in terms]
    v = np.array(values, float)
    y = v - (arcus * 60 / s if arcus is not None else 0)
    use = np.ones(12, bool)
    for _ in range(3 if robust else 0):
        coef = np.linalg.lstsq(np.array(cols).T[use], y[use], rcond=None)[0] if cols else np.array([])
        res = y - (np.array(cols).T @ coef if cols else 0)
        sig = 1.4826 * np.median(np.abs(res[use] - np.median(res[use])))
        bad = [i for i in range(12) if use[i] and abs(res[i]) > max(3 * sig, 10)]
        if not bad:
            break
        use[max(bad, key=lambda i: abs(res[i]))] = False
    coef = np.linalg.lstsq(np.array(cols).T[use], y[use], rcond=None)[0] if cols else np.array([])
    comp = v - y + (np.array(cols).T @ coef if cols else 0)
    return comp, coef, use


COMP, STATS = {}, {}
for col in MODEL:
    comp, coef, use = fit(col, CORRECTED[col])
    COMP[col] = comp
    rms = lambda r: math.sqrt(float(np.mean(np.square(r))))
    other = "W" if MODEL[col][0] == "E" else "E"
    o_comp, o_coef, _ = fit(col, CORRECTED[col], side=other, arcus="free", robust=False)
    free_comp, free_coef, _ = fit(col, CORRECTED[col], arcus="free", robust=False)
    STATS[col] = {"coef": coef, "out": [SIGNS[i] for i in range(12) if not use[i]],
                  "rms_in": rms((np.array(CORRECTED[col]) - comp)[use]),
                  "rms_printed": rms(np.array(PRINTED[col]) - comp), "rms_corrected": rms(np.array(CORRECTED[col]) - comp),
                  "free_arcus": free_coef[0], "other": other, "rms_other": rms(np.array(CORRECTED[col]) - o_comp),
                  "other_arcus": o_coef[0]}


def key(col, i, reading=False):
    return f"p. {PAGE[col]} {col} {SIGNS[i]}" + (" (reading)" if reading else "")


found, agree = [], [0]
# 1. the anomalies in the heads of p. 143
heads_ok = 0
for page in read("apparitions_pages.tsv"):
    for sub in page["subheads"].split("|"):
        ar, la = sub.split("‖")
        if "الى" not in ar:
            continue
        words = ar.split(" / ")[-1].split()
        a = [0 if w == "{0}" else sum(ABJAD[ch] for ch in w) for w in (words[0], words[2])]
        b = [int(x) for x in la.replace("°", " ").split() if x.isdigit()]
        if a == b:
            heads_ok += 1
        else:
            found.append((f"p. {page['ppage']} head {la}", ar, f"abjad {a}"))
# 3. identities
IDENT = []
for i in range(1, 6):
    for col in ("jup_app", "jup_occ", "mars_app", "mars_occ"):
        IDENT.append((col, i, col, 12 - i))
for i in range(12):
    IDENT.append(("mars_app", i, "mars_occ", (i + 6) % 12))
ident_ok = {"printed": 0, "corrected": 0}
for a, i, b, j in IDENT:
    for label, tab in (("printed", PRINTED), ("corrected", CORRECTED)):
        if tab[a][i] == tab[b][j]:
            ident_ok[label] += 1
        elif label == "corrected":
            pa, pb = a.split("_")[1], b.split("_")[1]
            found.append((f"identity {a.split('_')[0]} {pa} {SIGNS[i]} = {pb} {SIGNS[j]}",
                          f"{dm(tab[a][i])}, {dm(tab[b][j])}", "equal"))
# 4. the computation
for col in MODEL:
    for i in range(12):
        corr = (col, i) in CORRECTIONS
        dev = CORRECTED[col][i] - COMP[col][i]
        if abs(dev) > LIST:
            found.append((key(col, i, corr), dm(CORRECTED[col][i]), f"computed {dm(COMP[col][i])}"))
        else:
            agree[0] += 1


def main():
    rows = read("apparitions_discrepancies.tsv")
    ledger = {r["where"] for r in rows if r["kind"] != "noted"}
    noted = {r["where"]: r for r in rows if r["kind"] == "noted"}
    problems = []
    for (col, i), (p, c, rd) in CORRECTIONS.items():
        w = key(col, i)
        if w not in noted:
            problems.append(f"no ledger entry for Nallino's correction: {w} ({dm(p)} for {dm(c)})")
        elif noted[w]["printed"] != dm(p) or noted[w]["computed"] != dm(c):
            problems.append(f"{w}: the ledger has {noted[w]['printed']} / {noted[w]['computed']}, the data {dm(p)} / {dm(c)}")
    problems += [f"ledger entry of kind noted without a correction: {w}" for w in noted
                 if not any(key(col, i) == w for col, i in CORRECTIONS)]
    open_ = [f for f in found if f[0] not in ledger]
    closer = sum(1 for (col, i) in CORRECTIONS if col in COMP
                 and abs(CORRECTED[col][i] - COMP[col][i]) < abs(PRINTED[col][i] - COMP[col][i]))
    modelled = sum(1 for (col, i) in CORRECTIONS if col in COMP)
    print(f"heads {heads_ok} of 8; identities {ident_ok['corrected']} of {len(IDENT)} with Nallino's readings "
          f"({ident_ok['printed']} as printed); values within {LIST}′ of the computation {agree[0]}, differ "
          f"{len(found)} (ledgered {len(found) - len(open_)}, open {len(open_)}); Nallino's corrections "
          f"{len(CORRECTIONS)} ({closer} of the {modelled} in computed columns lie closer to the computation than the "
          f"printed value), problems {len(problems)}")
    if "--stats" in sys.argv:
        for col, st in STATS.items():
            side, arcus, lat = MODEL[col]
            print(f"  {col}: horizon {side} (head {HEAD[col.split('_', 1)[1]]}), arcus {arcus}, latitude "
                  + (" ".join(f"{x:+.2f}°" for x in st["coef"]) or "none")
                  + f"; rms {st['rms_in']:.1f}′ (set aside: {', '.join(st['out']) or 'none'}); printed values "
                  f"{st['rms_printed']:.1f}′, corrected {st['rms_corrected']:.1f}′; free arcus {st['free_arcus']:.3f}; "
                  f"horizon {st['other']}: arcus {st['other_arcus']:.2f}, rms {st['rms_other']:.1f}′")
        for side in "EW":
            o_comp, o_coef, _ = fit("ven_occ_vesp", CORRECTED["ven_occ_vesp"], side=side, arcus="free", robust=False)
            p_comp, p_coef, _ = fit("ven_occ_vesp", PRINTED["ven_occ_vesp"], side=side, arcus="free", robust=False)
            r = lambda a, b: math.sqrt(float(np.mean(np.square(np.array(a) - b))))
            print(f"  ven_occ_vesp (not checked): horizon {side}: corrected rms {r(CORRECTED['ven_occ_vesp'], o_comp):.1f}′,"
                  f" printed rms {r(PRINTED['ven_occ_vesp'], p_comp):.1f}′")
    for where, p, e in (found if "--list" in sys.argv else open_):
        print(f"  {where}: {p}; {e}" + ("" if where in ledger else "   << not in the ledger"))
    for p in problems:
        print("  " + p)
    stale = [w for w in ledger if w not in {f[0] for f in found}]
    for w in stale:
        print("  ledger entry without a difference:", w)
    sys.exit(1 if open_ or stale or problems else 0)


if __name__ == "__main__":
    main()

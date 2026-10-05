"""Write the data of Nallino's Part II pp. 55-58 to S06/spherical/: the sines for every half degree (pp. 55-56),
the declination of the Sun for every degree with the four arcs of equal declination (pp. 57-58), the right ascensions
of every tenth degree with their sines (p. 58), the heads, and the labels of the figure of the orders of
declination (p. 58). Values come from the readings resolved against the computed values (sine_pages.py,
decl_pages.py: MP{pdf}{tag}.json); the cells in EYE were read by eye (marks of a first row, or a printed difference)."""
import csv, json, os
from collections import Counter
import wide_kit as wk

AB = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani"
OUT = os.path.join(AB, "S06", "spherical")
os.makedirs(OUT, exist_ok=True)


def write(name, fields, rows):
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n", restval="")
        w.writeheader(); w.writerows(rows)


def cells(g):
    return tuple(c["value"] for c in g), "".join(c["cls"] for c in g)


classes = Counter()
# ---------------------------------------------------------------- sines, pp. 55-56
EYE_SIN = {(504, 0, 1): ("0", "31", "25"), (504, 2, 1): ("30", "27", "8"), (505, 0, 1): ("42", "47", "42"),
           (505, 2, 1): ("58", "5", "20")}
sines = []
for pdf, pp, first in ((504, "55", 0), (505, "56", 45)):
    for k in range(3):
        d = json.load(open(wk.OUT + f"MP{pdf}s{k}.json", encoding="utf-8"))
        assert len(d["rows"]) == 30
        for i, r in enumerate(d["rows"]):
            th = first + 15 * k + 0.5 * (i + 1)
            supp, cs = cells(r["groups"][0])
            if (pdf, k, i + 1) in EYE_SIN:
                sin, cn = EYE_SIN[(pdf, k, i + 1)], "EEE"
            else:
                sin, cn = cells(r["groups"][1])
            assert None not in supp + sin, (pdf, k, i)
            classes.update(cs + cn)
            sines.append({"pdf": pdf, "ppage": pp, "section": k + 1, "row": i + 1, "arc_d": int(th), "arc_m": int(round(th % 1 * 60)),
                          "supp_d": supp[0], "supp_m": supp[1], "sin_p": sin[0], "sin_m": sin[1], "sin_s": sin[2],
                          "check": cs + " " + cn})
write("sines_p2.tsv", ["pdf", "ppage", "section", "row", "arc_d", "arc_m", "supp_d", "supp_m", "sin_p", "sin_m", "sin_s",
                       "check", "doubt"], sines)

# ---------------------------------------------------------------- declination, pp. 57-58
decl = []
for pdf, pp, tag, lam0 in ((506, "57", "L", 1), (506, "57", "R", 31), (507, "58", "L", 61)):
    d = json.load(open(wk.OUT + f"MP{pdf}{tag}.json", encoding="utf-8"))
    assert len(d["rows"]) == 30
    for i, r in enumerate(d["rows"]):
        dv, dc = cells(r["groups"][0])
        arcs = [cells(g) for g in r["groups"][1:]]
        assert None not in dv and all(a[0][0] is not None for a in arcs), (pdf, tag, i)
        classes.update(dc + "".join(a[1] for a in arcs))
        decl.append({"pdf": pdf, "ppage": pp, "half": tag, "row": i + 1, "lam": lam0 + i,
                     "decl_d": dv[0], "decl_m": dv[1], "decl_s": dv[2],
                     "arc_a": arcs[0][0][0], "arc_b": arcs[1][0][0], "arc_c": arcs[2][0][0], "arc_d": arcs[3][0][0],
                     "check": dc + " " + "".join(a[1] for a in arcs)})
write("decl_p2.tsv", ["pdf", "ppage", "half", "row", "lam", "decl_d", "decl_m", "decl_s", "arc_a", "arc_b", "arc_c", "arc_d",
                      "check", "doubt"], decl)

# ---------------------------------------------------------------- right ascensions of the decades, p. 58
EYE_RA = {(2, 1): ("18", "57", "10"), (6, 1): ("50", "45", "56")}
DOUBT_RA = {2: "minutes of the sine printed 57; interpolation in the sines of p. 55 gives 59 (see the ledger)"}
d = json.load(open(wk.OUT + "MP507RA.json", encoding="utf-8"))
assert len(d["rows"]) == 9
ra10 = []
for i, r in enumerate(d["rows"]):
    a, ac = cells(r["groups"][0])
    if (i + 1, 1) in EYE_RA:
        s, sc = EYE_RA[(i + 1, 1)], "EEE"
    else:
        s, sc = cells(r["groups"][1])
    assert None not in a + s, i
    classes.update(ac + sc)
    ra10.append({"pdf": 507, "ppage": "58", "row": i + 1, "decade": 10 * (i + 1), "ra_d": a[0], "ra_m": a[1], "ra_s": a[2],
                 "sin_p": s[0], "sin_m": s[1], "sin_s": s[2], "check": ac + " " + sc, "doubt": DOUBT_RA.get(i + 1, "")})
write("ra10_p2.tsv", ["pdf", "ppage", "row", "decade", "ra_d", "ra_m", "ra_s", "sin_p", "sin_m", "sin_s", "check", "doubt"], ra10)

# ---------------------------------------------------------------- titles and heads
ARC = "القسي المتفاضلة / بنصف جزء‖Arcus intervallo / dimidii gradus."
pages = [
    {"pdf": 504, "ppage": "55", "fol": "f. 176,v.", "table": "sines",
     "title_ar": "جدول الاوتار المنصفة والقسي المتفاضلة بنصف جزء",
     "title_la": "Tabulae sinuum et arcuum intervallo dimidii gradus descriptorum.",
     "heads": "|".join([ARC, "الاوتار المنصفة‖Sinus.", ARC, "الاوتار المنصفة‖Sinus.", ARC, "لاوتار المنصفة‖Sinus."])},
    {"pdf": 505, "ppage": "56", "fol": "f. 177,r.", "table": "sines",
     "title_ar": "تمام جداول الاوتار المنصفة والقسي المتفاضلة بنصف جزء",
     "title_la": "Finis tabularum sinuum et arcuum intervallo dimidii gradus descriptorum.",
     "heads": "|".join(["‖Arcus intervallo / dimidii gradus.", "‖Sinus."] * 3)},
    {"pdf": 506, "ppage": "57", "fol": "f. 177,v.", "table": "decl",
     "title_ar": "ابتداء جداول ميل الشمس عن فلك معدل النهار في دائرة نصف النهار",
     "title_la": "Initium tabularum declinationis Solis a circulo aequinoctiali, in meridiano.",
     "heads": "البعد من دائرة / معدل النهار‖Declinatio.|سطور العدد المربع من نطاق البروج‖Numeri quadruplices zodiaci.|"
              "حمل‖Aries.|سنبلة‖Virgo.|ميزان‖Libra.|حوت‖Pisces.|‖Declinatio.|‖Numeri quadruplices zodiaci.|"
              "ثور‖Taurus.|اسد‖Leo.|عقرب‖Scorpio.|دلو‖Aquarius."},
    {"pdf": 507, "ppage": "58", "fol": "f. 178,r.", "table": "decl",
     "title_ar": "تمام جداول ميل الشمس ونطاق البروج",
     "title_la": "Finis tabularum declinationis Solis / et [arcuum] zodiaci.",
     "heads": "‖Declinatio.|‖Numeri quadruplices zodiaci.|جوزاء‖Gemini.|سرطان‖Cancer.|قوس‖Sagittarius.|جدي‖Capricornus."},
    {"pdf": 507, "ppage": "58", "fol": "", "table": "ra10", "title_ar": "", "title_la": "",
     "heads": "عشرات العدد‖Decades / numerorum.|مطالع العشرات في / الفلك المستقيم‖Ascensiones / decadum / in sphaera recta.|"
              "واوتار المطالع المنصفة‖Sinus / ascensionum."},
    {"pdf": 507, "ppage": "58", "fol": "", "table": "figure",
     "title_ar": "مراتب الميل في الصعود والهبوط وشكلها",
     "title_la": "Ordines declinationis in ascensu et descensu / eorumque imago.", "heads": ""},
]
write("sph_pages.tsv", ["pdf", "ppage", "fol", "table", "title_ar", "title_la", "heads"], pages)

# ---------------------------------------------------------------- the figure of p. 58
# position: compass side (N = top of the page) or band cell; rot: rotation of the text in degrees (counter-clockwise)
FIG = [
    ("dir", "top", "الجنوب", "Meridies", 0), ("dir", "bottom", "الشمال", "Septentriones", 0),
    ("dir", "left", "المشرق", "Oriens", 90), ("dir", "right", "", "[Occidens]", -90),
    ("sign", "top", "الجدي", "Capricornus", 90), ("sign", "left", "الميزان", "Libra", 0),
    ("sign", "right", "الحمل", "Aries", 0), ("sign", "bottom", "السرطان", "Cancer", 90),
    ("order", "upper-left", "مراتب هبوط الجنوب", "Ordines / descensus australis", 45),
    ("order", "upper-right", "مراتب صعود الجنوب", "Ordines / ascensus australis", -45),
    ("order", "lower-left", "مراتب هبوط الشمال", "Ordines / descensus borealis", 135),
    ("order", "lower-right", "مراتب صعود الشمال", "Ordines / ascensus borealis", 225),
]
fig = [{"kind": k, "position": p, "text_ar": a, "text_la": l, "rot": r} for k, p, a, l, r in FIG]
for side, seq in (("upper-left", [15, 30, 45, 60, 75]), ("upper-right", [75, 60, 45, 30, 15]),
                  ("lower-right", [15, 30, 45, 60, 75]), ("lower-left", [75, 60, 45, 30, 15])):
    for j, v in enumerate(seq):
        fig.append({"kind": "cell", "position": f"{side} {j + 1}", "text_ar": "", "text_la": f"{v}°", "rot": ""})
for corner, v in (("left", 0), ("top", 90), ("right", 0), ("bottom", 90)):
    fig.append({"kind": "cell", "position": f"corner {corner}", "text_ar": "", "text_la": f"{v}°", "rot": ""})
write("fig58.tsv", ["kind", "position", "text_ar", "text_la", "rot"], fig)
print(len(sines), "sines;", len(decl), "declinations;", len(ra10), "right ascensions;", len(fig), "figure items;", classes)

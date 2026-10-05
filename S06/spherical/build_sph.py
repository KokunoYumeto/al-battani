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

# ---------------------------------------------------------------- p. 59: half the increase of the longest day
# every value read by eye on contact sheets (sheet59.py); the class says which readers agree with it
EYE59 = ("0;13 0;26 0;39 0;52 1;6 1;19 1;32 1;45 1;58 2;12 2;26 2;40 2;54 3;8 3;22 3;36 3;49 4;1 4;14 4;26 "
         "4;39 4;51 5;5 5;19 5;33 5;47 6;1 6;15 6;29 6;43 6;57 7;11 7;25 7;40 7;54 8;9 8;23 8;38 8;53 9;8 "
         "9;23 9;39 9;55 10;11 10;27 10;43 10;59 11;16 11;33 11;51 12;8 12;24 12;41 12;57 13;14 13;30 13;47 14;3 14;20 14;36 "
         "14;54 15;13 15;32 15;50 16;8 16;28 16;47 17;7 17;28 17;49 18;9 18;30 18;51 19;13 19;35 19;57 20;19 20;40 21;3 21;29 "
         "21;53 22;18 22;43 23;9 23;35 24;2 24;29 24;56 25;24 25;53 26;22 26;52 27;23 27;55 28;27 29;0 29;32 30;6 30;43 31;22 "
         "32;0 32;39 33;18 33;57 34;39 35;24 36;9 36;53 37;43 38;34 39;26 40;20 41;17 42;14 43;15 44;19 45;25 46;35 47;49 49;7").split()
assert len(EYE59) == 120
days59 = []
for k in range(3):
    d = json.load(open(wk.OUT + f"MP508s{k}.json", encoding="utf-8"))
    assert len(d["rows"]) == 40
    for i, r in enumerate(d["rows"]):
        phi = 20 * k + 0.5 * (i + 1)
        v = EYE59[40 * k + i].split(";")
        cl = ""
        for c, x in zip(r["groups"][0], v):
            agree = [c is not None and c["read"] == x and c["conf"] >= 0.85, c is not None and c.get("tl") == x]
            cl += "A" if all(agree) else ("B" if any(agree) else "E")
        classes.update(cl)
        days59.append({"pdf": 508, "ppage": "59", "section": k + 1, "row": i + 1, "phi_d": int(phi), "phi_m": int(round(phi % 1 * 60)),
                       "inc_d": v[0], "inc_m": v[1], "check": cl})
write("days59_p2.tsv", ["pdf", "ppage", "section", "row", "phi_d", "phi_m", "inc_d", "inc_m", "check", "doubt"], days59)

# ---------------------------------------------------------------- p. 60: shadows of a gnomon of 12 digits
EYE60 = {(0, 28): ("22", "34")}
shadows = []
for k in range(3):
    d = json.load(open(wk.OUT + f"MP509s{k}.json", encoding="utf-8"))
    assert len(d["rows"]) == 30
    for i, r in enumerate(d["rows"]):
        if (k, i + 1) in EYE60:
            v, cl = EYE60[(k, i + 1)], "EE"
        else:
            v, cl = cells(r["groups"][0])
        assert None not in v, (k, i)
        classes.update(cl)
        shadows.append({"pdf": 509, "ppage": "60", "section": k + 1, "row": i + 1, "alt": 30 * k + i + 1,
                        "dig": v[0], "min": v[1], "check": cl})
write("shadows60_p2.tsv", ["pdf", "ppage", "section", "row", "alt", "dig", "min", "check", "doubt"], shadows)

pages += [
    {"pdf": 508, "ppage": "59", "fol": "f. 178,v.", "table": "days",
     "title_ar": "جدول لمعرفة نصف زيادة النهار الاطول من قبل ارتفاع القطب في كل بلد ومعرفة ارتفاع القطب / "
                 "من قبل زيادة النهار الاطول ان شاء اللّٰه",
     "title_la": "Tabula qua cognoscuntur dimidium incrementum diei longissimi quocumque / Terrae loco per altitudinem "
                 "poli, et altitudo poli per incrementum diei lon- / gissimi, si Deus vult.",
     "heads": "|".join(["ارتفاع القطب‖Altitudo poli.", "نصف زيادة النهار / الاطول‖Dimidium incremen- / tum diei longissimi."] * 3)},
    {"pdf": 509, "ppage": "60", "fol": "f. 179,r.", "table": "shadows",
     "title_ar": "جدول لمعرفة الظل من قبل الارتفاع بالمقدار الذي تكون به اجزاء المقياس يب جزء ومعرفة الارتفاع / "
                 "من قبل هذا الظل المبسوط وبهذه الجداول وعرف احدهما من قبل الآخر",
     "title_la": "Tabula qua cognoscitur umbra per altitudinem poli iuxta rationem qua gno- / mon in 12 partes dividitur, et "
                 "altitudo poli per hanc umbram extensam. / His tabulis altera ex altera deprehenditur.",
     "heads": "|".join(["قوس الارتفاع‖Arcus / altitudinis.", "اصابع الظل‖Digiti umbrae."] * 3)},
]

# ---------------------------------------------------------------- pp. 61-64: right ascensions and equation of days
# right ascensions resolved against the computation (ra_eq_pages.py); the equation of days by agreement of the two
# readers (eq_resolve.py, EQ{pdf}.json); the cells below read by eye on contact sheets
SIGNS = {510: ["Capricornus", "Aquarius", "Pisces"], 511: ["Aries", "Taurus", "Gemini"],
         512: ["Cancer", "Leo", "Virgo"], 513: ["Libra", "Scorpio", "Sagittarius"]}
FIRST = {510: (270, 300, 330), 511: (0, 30, 60), 512: (90, 120, 150), 513: (180, 210, 240)}
EYE_ASC = {(510, 21, 2): ("81", "44"), (510, 22, 2): ("82", "40"), (511, 8, 1): ("125", "37"), (513, 26, 0): ("294", "5"),
           (513, 30, 2): ("360", "0")}
EYE_EQ = {(510, 3, 0): ("3", "25"), (511, 7, 1): ("5", "2"), (511, 8, 1): ("5", "5"), (511, 9, 1): ("5", "8"),
          (511, 10, 1): ("5", "10"), (511, 11, 1): ("5", "13"), (511, 19, 2): ("4", "56"), (512, 1, 1): ("3", "4"),
          (512, 21, 1): ("3", "19"), (513, 1, 0): ("6", "9"), (513, 7, 2): ("6", "27")}
raeq = []
for pdf in (510, 511, 512, 513):
    d = json.load(open(wk.OUT + f"MP{pdf}.json", encoding="utf-8"))
    eq = json.load(open(wk.OUT + f"EQ{pdf}.json", encoding="utf-8"))
    assert len(d["rows"]) == 30
    for i, r in enumerate(d["rows"]):
        for k in range(3):
            if (pdf, i + 1, k) in EYE_ASC:
                a, ac = EYE_ASC[(pdf, i + 1, k)], "EE"
            else:
                a, ac = cells(r["groups"][2 * k])
            vals, ec = eq[str(i + 1)][str(k)]
            for j, cl in enumerate(ec):
                if cl == "C":
                    vals[j] = EYE_EQ[(pdf, i + 1, k)][j]
            ec = ec.replace("C", "E")
            assert None not in a and None not in vals, (pdf, i, k)
            classes.update(ac + ec)
            raeq.append({"pdf": pdf, "ppage": str(pdf - 449), "row": i + 1, "sign": SIGNS[pdf][k], "lam": FIRST[pdf][k] + i + 1,
                         "asc_d": a[0], "asc_m": a[1], "eq_d": vals[0], "eq_m": vals[1], "check": ac + " " + ec})
ORDER = ["Capricornus", "Aquarius", "Pisces", "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio",
         "Sagittarius"]
raeq.sort(key=lambda x: (ORDER.index(x["sign"]), x["row"]))
write("raeq_p2.tsv", ["pdf", "ppage", "row", "sign", "lam", "asc_d", "asc_m", "eq_d", "eq_m", "check", "doubt"], raeq)

AR_SIGN = {"Capricornus": "الجدي", "Aquarius": "الدلو", "Pisces": "الحوت", "Aries": "الحمل", "Taurus": "الثور",
           "Gemini": "الجوزاء", "Cancer": "السرطان", "Leo": "الاسد", "Virgo": "السنبلة", "Libra": "الميزان",
           "Scorpio": "العقرب", "Sagittarius": "القوس"}
TITLE_AR = "من جداول مطالع البروج في الفلك المستقيم وتعديل الايام بلياليها"
EQH = "‖Aequatio / nychthemerōn."
for pdf, fol, tar, tla in ((510, "f. 179,v.", "ابتداء جداول مطالع البروج في الفلك المستقيم وتعَديل الايام بلياليها",
                            "Initium tabularum ascensionum signorum in sphaera recta et aequationis / nychthemerōn."),
                           (511, "f. 180,r.", TITLE_AR, "Ex tabulis ascensionum signorum in sphaera recta et aequationis / nychthemerōn."),
                           (512, "f. 180,v.", TITLE_AR, "Ex tabulis ascensionum signorum in sphaera recta, et aequationis / nychthemerōn."),
                           (513, "f. 181,r.", TITLE_AR, "Finis tabularum ascensionum signorum in sphaera recta, et aequationis / nychthemerōn.")):
    first = "العدد المشترك‖Numeri [omnibus] / communes." if pdf == 510 else "‖Numeri [omnibus] / communes."
    hs = [first]
    for k, s in enumerate(SIGNS[pdf]):
        hs.append(f"{AR_SIGN[s]} / درج المطالع‖{s}. / Gradus ascen- / sionum.")
        hs.append("تعديل الايام بلياليها‖Aequatio / nychthemerōn." if (pdf == 510 and k == 0) else EQH)
    pages.append({"pdf": pdf, "ppage": str(pdf - 449), "fol": fol, "table": "raeq", "title_ar": tar, "title_la": tla,
                  "heads": "|".join(hs)})

# ---------------------------------------------------------------- pp. 65-67: oblique ascensions of the decades
# resolved against the computation for the fitted latitude of each column (oblique_pages.py rerun_fitted); the cells
# below read by eye
SIGNS12 = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricornus",
           "Aquarius", "Pisces"]
EYE_OB = {(514, 1, 3): ("7", "6"), (514, 5, 0): ("42", "3"), (514, 13, 0): ("127", "0"), (514, 21, 1): ("212", "21"),
          (514, 25, 3): ("267", "32"), (514, 25, 4): ("260", "16"), (515, 20, 6): ("207", "36"), (515, 32, 2): ("335", "56"),
          (515, 34, 1): ("347", "57"), (516, 11, 4): ("94", "2"), (516, 12, 2): ("108", "15"), (516, 25, 4): ("265", "58"),
          (516, 32, 3): ("12", "20"), (516, 33, 3): ("12", "43")}
COLS = {514: ["16° 39′", "20° 28′", "24° 5′", "27° 28′", "30° 40′", "33° 37′"],
        515: ["36° 22′", "38° 54′", "41° 15′", "43° 25′", "45° 22′", "47° 12′", "48° 53′"],
        516: ["Mekkah asc", "Mekkah hour", "Baghdad asc", "Baghdad hour", "Harran asc", "Harran hour"]}
oblique = []
for pdf in (514, 515, 516):
    d = json.load(open(wk.OUT + f"MP{pdf}.json", encoding="utf-8"))
    assert len(d["rows"]) == 36
    for i, r in enumerate(d["rows"]):
        rec = {"pdf": pdf, "ppage": str(pdf - 449), "row": i + 1, "decade": 10 * (i + 1), "sign": SIGNS12[i // 3]}
        checks = []
        for gi, col in enumerate(COLS[pdf]):
            if (pdf, i + 1, gi) in EYE_OB:
                v, cl = EYE_OB[(pdf, i + 1, gi)], "EE"
            else:
                v, cl = cells(r["groups"][gi])
            assert None not in v, (pdf, i, gi)
            classes.update(cl)
            rec[f"c{gi + 1}_d"], rec[f"c{gi + 1}_m"] = v
            checks.append(cl)
        rec["check"] = " ".join(checks)
        oblique.append(rec)
write("oblique_p2.tsv", ["pdf", "ppage", "row", "decade", "sign"] + [f"c{k}_{p}" for k in range(1, 8) for p in "dm"] + ["check"],
      oblique)
write("oblique_columns.tsv", ["pdf", "col", "label"], [{"pdf": p, "col": k + 1, "label": c} for p, cs in COLS.items()
                                                         for k, c in enumerate(cs)])

OBT_AR = "جدول مطالع البروج في الاقاليم بتفاضل ربع ساعة وعشرة اجزاء في العدد"
OBT_LA = "Tabulae ascensionum signorum, per decades graduum, in climatibus intervallo / quadrantis horae descriptis."
pages.append({"pdf": 514, "ppage": "65", "fol": "f. 181,v.", "table": "oblique", "title_ar": OBT_AR, "title_la": OBT_LA,
              "heads": "|".join(["اسماء البروج‖Nomina signorum.", "عدد الاجزاء‖Decades graduum.",
                                 "‖I clima, / lat. 16° 39′. / Horae 13ʰ.‖المطالع‖Gradus / ascensionum.",
                                 "‖Lat. 20° 28′. / Horae 13ʰ 15ᵐ.‖‖Gradus / ascensionum.",
                                 "‖II clima, / lat. 24° 5′. / Horae 13ʰ 30ᵐ.‖‖Gradus / ascensionum.",
                                 "‖Lat. 27° 28′. / Horae 13ʰ 45ᵐ.‖‖Gradus / ascensionum.",
                                 "‖III clima, / lat. 30° 40′. / Horae 14ʰ.‖‖Gradus / ascensionum.",
                                 "‖Lat. 33° 37′. / Horae 14ʰ 15ᵐ.‖‖Gradus / ascensionum."])})
pages.append({"pdf": 515, "ppage": "66", "fol": "f. 182,r.", "table": "oblique", "title_ar": OBT_AR, "title_la": OBT_LA,
              "heads": "|".join(["‖Nomina signorum.", "‖Decades graduum.",
                                 "‖IV clima, / lat. 36° 22′. / Hor. 14ʰ 30ᵐ.‖‖Gradus / ascension.",
                                 "‖Lat. 38° 54′. / Hor. 14ʰ 45ᵐ.‖‖Gradus / ascension",
                                 "‖V clima, / lat. 41° 15′. / Horae 15ʰ.‖‖Gradus / ascension.",
                                 "‖Lat. 43° 25′. / Hor. 15ʰ 15ᵐ.‖‖Gradus / ascension.",
                                 "‖VI clima, / lat. 45° 22′. / Hor. 15ʰ 30ᵐ.‖‖Gradus / ascension.",
                                 "‖Lat. 47° 12′. / Hor. 15ʰ 45ᵐ.‖‖Gradus / ascension.",
                                 "‖VII clima, / lat. 48° 53′. / Horae 16ʰ.‖‖Gradus / ascension."])})
pages.append({"pdf": 516, "ppage": "67", "fol": "f. 182,v.", "table": "cities",
              "title_ar": "جدول مطالع البروج وازمان الساعات بمكة وبغداد وحران",
              "title_la": "Ascensiones signorum et tempora horaria in urbibus Mekkah, Baghdād / et Ḥarrān.",
              "heads": "|".join(["‖Nomina signorum.", "‖Decades graduum.",
                                 "درج المطالع مكة‖Ascensiones / Mekkah, / lat. 21° 40′.", "ازمان الساعات‖Tempora / horaria / 13ʰ 20ᵐ.",
                                 "درج المطالع بغداد‖Ascensiones / Baghdād, / lat. 33° 9′.", "ازمان الساعات‖Tempora / horaria / 14ʰ 12ᵐ 32ˢ.",
                                 "درج المطالع حران‖Ascensiones / Ḥarrān, / lat. 36° 40′.", "ازمان الساعات‖Tempora / horaria / 14ʰ 32ᵐ."])})
write("sph_pages.tsv", ["pdf", "ppage", "fol", "table", "title_ar", "title_la", "heads"], pages)
print(len(sines), "sines;", len(decl), "declinations;", len(ra10), "right ascensions;", len(fig), "figure items;", classes)

"""Write the data of Nallino's Part II pp. 19-23 (mean motions of the Sun, the Moon, the lunar anomaly and the
ascending node in Arab collected years, single years, months, days and hours) to S06/mean_motions/.
Values come from the readings resolved against the linear fit of each column (motion_page.py, MP{pdf}.json):
class A cells (both readers give the value), class B cells (one reader gives it; checked by eye), and the cells in
EYE below, which the fit flagged and which were read by eye. Files: mm_p2.tsv (one row per printed row) and
mm_pages.tsv (titles and heads)."""
import csv, json, os
import wide_kit as wk

AB = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani"
OUT = os.path.join(AB, "S06", "mean_motions")
os.makedirs(OUT, exist_ok=True)
PAGES = {468: ("19", "f. 164,v.", "collected"), 469: ("20", "f. 165,r.", "single"), 470: ("21", "f. 165,v.", "months"),
         471: ("22", "f. 166,r.", "days"), 472: ("23", "f. 166,v.", "hours")}
MONTHS = ["al–muḥarram.", "ṣafar.", "rabī‘ prior.", "rabī‘ posterior.", "ǵumādà prior.", "ǵumādà posterior.", "raǵab.",
          "sha‘bān.", "ramaḍān.", "shawwāl.", "dhū ’l-qa‘dah.", "dhū ’l–ḥiǵǵah / comm.", "bisext."]
GROUPS = ["sun", "moon", "anom", "node"]
# cells the fit flagged, read by eye: (pdf, row, group) -> (d, m, s) as printed
EYE = {(469, 1, "moon"): ("344", "26", "43"),
       (469, 29, "sun"): ("49", "32", "35"),          # the readers gave 34 and 33; read by eye at 2400 dpi
       (469, 26, "node"): ("127", "53", "9"),
       (471, 26, "moon"): ("342", "35", "11"),
       (471, 29, "moon"): ("22", "6", "56")}
DOUBT = {(469, 26, "node"): "printed 127° 53′ 9″; the line through the other rows gives 127° 53′ 20″ (see the ledger)"}

rows = []
for pdf, (pp, fol, table) in PAGES.items():
    d = json.load(open(wk.OUT + f"MP{pdf}.json", encoding="utf-8"))
    for i, r in enumerate(d["rows"]):
        n = i + 1
        rec = {"pdf": pdf, "ppage": pp, "table": table, "row": n,
               "arg": MONTHS[i] if table == "months" else str(r.get("arg_exp") or r["arg"])}
        checks = []
        for gi, g in enumerate(GROUPS):
            cells = r["groups"][gi]
            if (pdf, n, g) in EYE:
                vals = EYE[(pdf, n, g)]; cl = "E" * 3
            else:
                vals = tuple(c["value"] for c in cells); cl = "".join(c["cls"] for c in cells)
                assert None not in vals, (pdf, n, g)
            for k, v in zip(("d", "m", "s"), vals):
                rec[f"{g}_{k}"] = v
            checks.append(cl)
        rec["check"] = " ".join(checks)
        rec["doubt"] = "; ".join(v for (p, rr, g), v in DOUBT.items() if p == pdf and rr == n)
        rows.append(rec)

fields = ["pdf", "ppage", "table", "row", "arg"] + [f"{g}_{k}" for g in GROUPS for k in "dms"] + ["check", "doubt"]
with open(os.path.join(OUT, "mm_p2.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(rows)

T_AR = "جدول {h} الشمس والقمر وحاصة القمر والعقد الشمالي في {w}"
T_LA = "Tabula motuum Solis, Lunae, anomaliae Lunae et nodi borealis / in {w}."
pages = [
    {"pdf": 468, "ppage": "19", "fol": "f. 164,v.", "title_ar": "جدول حركات الشمس والقمر وحاصّة القمر والعقد الشمالي في السنين العربية المجموعة",
     "title_la": T_LA.format(w="annis Arabicis collectis"),
     "heads": "سنو العرب المجموعة/Anni Arabum colle- / cti [ab initio hegirae].|مسير الشمس الاوسط/Solis longitudo media.|"
              "مسير القمر الاوسط/Lunae longitudo media.|حركة حاصّة القمر/Anomalia Lunae.|حركة العقد الشمالي/Longitudo / nodi borealis."},
    {"pdf": 469, "ppage": "20", "fol": "f. 165,r.", "title_ar": T_AR.format(h="حركات", w="السنين العربية المبسوطة"),
     "title_la": T_LA.format(w="singulis Arabum annis"),
     "heads": "سنو العرب المبسوطة/Singuli Arabum / anni.|مسير الشمس الاوسط/Solis iter medium.|مسير القمر الاوسط/Lunae iter medium.|"
              "حركة حاصة القمر/Motus / anomaliae Lunae.|حركة العقد الشمالي/Motus nodi borealis."},
    {"pdf": 470, "ppage": "21", "fol": "f. 165,v.", "title_ar": T_AR.format(h="حركة", w="الشهور العربية"),
     "title_la": T_LA.format(w="mensibus Arabicis"),
     "heads": "اسماء شهور العرب/Nomina / mensium Arabicorum.|مسير الشمس الاوسط/Solis / iter medium.|مسير القمر الاوسط/Lunae / iter medium.|"
              "حركة حاصة القمر/Motus / anomaliae Lunae.|حركة العقد الشمالي/Motus nodi borealis."},
    {"pdf": 471, "ppage": "22", "fol": "f. 166,r.", "title_ar": T_AR.format(h="حركة", w="ايام الشهر القمري"),
     "title_la": T_LA.format(w="diebus mensis lunaris"),
     "heads": "عدد ايام الشهر/Numerus dierum.|مسير الشمس الاوسط/Solis iter medium.|مسير القمر الاوسط/Lunae iter medium.|"
              "حركة حاصة القمر/Motus / anomaliae Lunae.|حركة العقد الشمالي/Motus nodi borealis."},
    {"pdf": 472, "ppage": "23", "fol": "f 166,v.", "title_ar": T_AR.format(h="حركات", w="الساعات المعتدلة"),
     "title_la": T_LA.format(w="horis aequinoctialibus"),
     "heads": "عدد الساعات المعتدلة/Numerus horarum / aequinoctialium.|مسير الشمس الاوسط/Solis iter medium.|مسير القمر الاوسط/Lunae iter medium.|"
              "حركة حاصة القمر/Motus / anomaliae Lunae.|حركة العقد الشمالي/Motus nodi borealis."},
]
with open(os.path.join(OUT, "mm_pages.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pdf", "ppage", "fol", "title_ar", "title_la", "heads"], delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(pages)
from collections import Counter
print(len(rows), "rows;", Counter(c for r in rows for c in r["check"].replace(" ", "")))

# ---------------------------------------------------------------- the five planets, pp. 24-28 (degrees and minutes)
PAGES5 = {473: ("24", "f. 168,r.", "collected"), 474: ("25", "f. 168,v.", "single"), 475: ("26", "f. 169,r.", "months"),
          476: ("27", "f. 169,v.", "days"), 477: ("28", "f. 170,r.", "hours")}
G5 = ["sat", "jup", "mars", "ven", "mer"]
EYE5 = {(473, 27, "mars"): ("349", "17"), (473, 28, "jup"): ("73", "34"), (473, 29, "jup"): ("237", "21"),
        (473, 30, "jup"): ("41", "9"), (474, 1, "jup"): ("29", "26"), (474, 2, "jup"): ("58", "51"),
        (474, 5, "jup"): ("157", "19"), (474, 7, "jup"): ("206", "10"), (474, 10, "jup"): ("294", "33"),
        (474, 2, "ven"): ("76", "30")}
DOUBT5 = {(473, 28, "jup"): "the step from AH 781 is 162° 48′, every other 30-year step 163° 47′–48′ (see the ledger)",
          (473, 29, "jup"): "1° below the line, carried from AH 811",
          (473, 30, "jup"): "1° below the line, carried from AH 811",
          (474, 2, "jup"): "5′ below the line (the leap day of year 2 not counted; see the ledger)",
          (474, 5, "jup"): "157 for 147 (see the ledger)",
          (474, 7, "jup"): "5′ below the line (the leap day of year 7 not counted)",
          (474, 10, "jup"): "5′ below the line (the leap day of year 10 not counted)",
          (474, 2, "ven"): "37′ below the line (the leap day of year 2 not counted)"}
MONTHS12 = ["al–muḥarram.", "ṣafar.", "rabī‘ prior.", "rabī‘ posterior.", "ǵumādà prior.", "ǵumādà posterior.", "raǵab.",
            "sha‘bān.", "ramaḍān.", "shawwāl.", "dhū ’l–qa‘dah.", "dhū ’l–ḥiǵǵah."]      # p. 26 prints the long dash
rows5 = []
for pdf, (pp, fol, table) in PAGES5.items():
    d = json.load(open(wk.OUT + f"MP{pdf}.json", encoding="utf-8"))
    for i, r in enumerate(d["rows"]):
        n = i + 1
        rec = {"pdf": pdf, "ppage": pp, "table": table, "row": n,
               "arg": MONTHS12[i] if table == "months" else str(r.get("arg_exp") or r["arg"])}
        checks = []
        for gi, g in enumerate(G5):
            cells = r["groups"][gi]
            if (pdf, n, g) in EYE5:
                vals = EYE5[(pdf, n, g)]; cl = "EE"
            else:
                vals = tuple(c["value"] for c in cells); cl = "".join(c["cls"] for c in cells)
                assert None not in vals, (pdf, n, g)
            rec[f"{g}_d"], rec[f"{g}_m"] = vals
            checks.append(cl)
        rec["check"] = " ".join(checks)
        rec["doubt"] = "; ".join(v for (p, rr, g), v in DOUBT5.items() if p == pdf and rr == n)
        rows5.append(rec)
fields5 = ["pdf", "ppage", "table", "row", "arg"] + [f"{g}_{k}" for g in G5 for k in "dm"] + ["check", "doubt"]
with open(os.path.join(OUT, "mm5_p2.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields5, delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(rows5)
H5 = "وسط زحل/Saturni / {x}|وسط المشتري/Iovis / {x}|وسط المريخ/Martis / {x}|حاصة الزهرة/{v}|حاصة عطارد/{m}"
pages5 = [
    {"pdf": 473, "ppage": "24", "fol": "f. 168,r.", "title_ar": "جدول حركات الكواكب الخمسة المتحيرة في السنين العربية المجموعة",
     "title_la": "Tabula motuum quinque planetarum in annis Arabicis collectis.",
     "heads": "لسنون العربية المجموعة/Anni Arabum colle- / cti [ab initio hegirae].|" +
              H5.format(x="longitudo media.", v="Anomalia Veneris.", m="Anomalia Mercurii.")},
    {"pdf": 474, "ppage": "25", "fol": "f. 168,v.", "title_ar": "جدول حركات الكواكب الخمسة المتحيرة في السنين العربية المبسوطة",
     "title_la": "Tabula motuum quinque planetarum in singulis Arabum annis.",
     "heads": "سنو العرب المبسوطة/Singuli Arabum / anni.|" +
              H5.format(x="motus medius.", v="Motus anomaliae / Veneris.", m="Motus anomaliae / Mercurii.")},
    {"pdf": 475, "ppage": "26", "fol": "f. 169,r.", "title_ar": "جدول حركات الكواكب الخمسة المتحيرة في الشهور العربية",
     "title_la": "Tabula motuum quinque planetarum in mensibus Arabum.",
     "heads": "اسماء الشهور العربية/Nomina / mensium Arabicorum.|" +
              H5.format(x="motus medius.", v="Motus / anomaliae / Veneris.", m="Motus / anomaliae / Mercurii.")},
    {"pdf": 476, "ppage": "27", "fol": "f. 169,v.", "title_ar": "حركات الكواكب الخمسة المتحيرة في ايام الشهر القمري",
     "title_la": "Motus quinque planetarum in diebus mensis lunaris.",
     "heads": "عدد ايام الشهر/Numerus dierum / mensis.|مسير زحل/Saturni iter.|مسير المشتري/Iovis iter.|مسير المريخ/Martis iter.|"
              "حاصة الزهرة/Motus anomaliae / Veneris.|حاصة عطارد/Motus anomaliae / Mercurii."},
    {"pdf": 477, "ppage": "28", "fol": "f. 170,r.", "title_ar": "جدول حركات الكواكب الخمسة المتحيرة في الساعات المعتدلة",
     "title_la": "Tabula motuum quinque planetarum in horis aequinoctialibus.",
     "heads": "عدد الساعات المعتدلة/Numerus horarum / diei.|مسير زحل/Saturni iter.|مسير المشتري/Iovis iter.|مسير المريخ/Martis iter.|"
              "حركة حاصة الزهرة/Motus anomaliae / Veneris.|حركة حاصة عطارد/Motus anomaliae / Mercurii."},
]
with open(os.path.join(OUT, "mm5_pages.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pdf", "ppage", "fol", "title_ar", "title_la", "heads"], delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(pages5)
print(len(rows5), "rows (planets);", Counter(c for r in rows5 for c in r["check"].replace(" ", "")))

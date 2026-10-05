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

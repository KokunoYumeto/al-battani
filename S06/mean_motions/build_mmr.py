"""Write the data of Nallino's Part II pp. 72-77 (mean motions of the Sun, the Moon, the lunar anomaly and the node in
the Roman calendar) to S06/mean_motions/: mmr_p2.tsv (one row per printed row) and mmr_pages.tsv (titles and heads).
Values come from the readings resolved against the linear fit of each column (mmr_pages.py, MP{pdf}.json); the cells
in EYE were read by eye."""
import csv, json, os
from collections import Counter
import wide_kit as wk

AB = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani"
OUT = os.path.join(AB, "S06", "mean_motions")
G = ["sun", "moon", "anom", "node"]
MONTHS = ["ādhār [Martius].", "nīsān [Aprilis].", "ayyār [Maius].", "ḥazīrān [Iunius].", "tammūz [Iulius].",
          "āb [Augustus].", "aylūl [September].", "tishrīn I [October].", "tishrīn II [November].", "kānūn I [December].",
          "kānūn II [Ianuarius].", "subāṭ [Februarius]. / comm.", "bisext."]
PAGES = {521: ("72", "f. 186,v.", "collected", [str(931 + 20 * k) for k in range(36)]),
         522: ("73", "f. 187,r.", "single", [str(n) for n in range(1, 21)]),
         523: ("74", "f. 187,v.", "months", MONTHS),
         524: ("75", "f. 188,r.", "days", [str(n) for n in range(1, 31)]),
         525: ("76", "f. 188,v.", "hours", [str(n) for n in range(1, 25)]),
         526: ("77", "f. 189,r.", "intervals", [str(n) for n in (20, 40, 60, 80, 100, 200, 300, 400, 500, 600)])}
EYE = {(521, 13, "node"): ("140", "34", "37"), (521, 18, "moon"): ("340", "2", "30"), (521, 36, "sun"): ("346", "54", "34"),
       (523, 13, "sun"): ("360", "44", "54"), (524, 18, "node"): ("0", "57", "12"), (524, 19, "node"): ("1", "0", "23")}
DOUBT = {(521, 13, "node"): "140 for 149 (see the ledger)"}

rows = []
for pdf, (pp, fol, table, args) in PAGES.items():
    d = json.load(open(wk.OUT + f"MP{pdf}.json", encoding="utf-8"))
    assert len(d["rows"]) == len(args), (pdf, len(d["rows"]))
    for i, r in enumerate(d["rows"]):
        n = i + 1
        rec = {"pdf": pdf, "ppage": pp, "table": table, "row": n, "arg": args[i]}
        checks = []
        for gi, g in enumerate(G):
            if (pdf, n, g) in EYE:
                vals, cl = EYE[(pdf, n, g)], "EEE"
            else:
                cells = r["groups"][gi]
                vals = tuple(c["value"] for c in cells); cl = "".join(c["cls"] for c in cells)
                assert None not in vals, (pdf, n, g)
            rec[f"{g}_d"], rec[f"{g}_m"], rec[f"{g}_s"] = vals
            checks.append(cl)
        rec["check"] = " ".join(checks)
        rec["doubt"] = "; ".join(v for (p, rr, g), v in DOUBT.items() if p == pdf and rr == n)
        rows.append(rec)
fields = ["pdf", "ppage", "table", "row", "arg"] + [f"{g}_{k}" for g in G for k in "dms"] + ["check", "doubt"]
with open(os.path.join(OUT, "mmr_p2.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(rows)

W5 = "وسط الشمس‖Solis motus medius.|وسط القمر‖Lunae motus medius.|حاصة القمر‖Motus anomaliae / Lunae.|العقد الشمالي‖Motus nodi borealis."
L4 = "‖Solis motus medius.|‖Lunae motus medius.|‖Motus / anomaliae Lunae.|‖Motus nodi borealis."
pages = [
    {"pdf": 521, "ppage": "72", "fol": "f. 186,v.", "title_ar": "جدول حركة الشمس والقمر وحاصة القمر في السنين الرومية المجموعة",
     "title_la": "Tabula motus Solis, Lunae, anomaliae Lunae [et nodi borealis] in annis / Romanorum collectis [ab aera].",
     "heads": "سنو الروم / المجموعة‖Anni / Romanor. / collecti.|وسط الشمس‖Solis / longitudo media.|وسط القمر‖Lunae / longitudo media.|"
              "حاصة القمر‖Anomalia Lunae.|العقد الشمالي‖Longitudo / nodi borealis."},
    {"pdf": 522, "ppage": "73", "fol": "f. 187,r.",
     "title_ar": "جدول حركات الشمس والقمر وحاصة القمر والعقد الشمالي في السنين الرومية المبسوطة",
     "title_la": "Tabula motuum Solis, Lunae, anomaliae Lunae et nodi borealis in singulis / Romanorum annis.",
     "heads": "سنو الروم / المبسوطة‖Singuli / anni / Romanor.|" + W5},
    {"pdf": 523, "ppage": "74", "fol": "f. 187,v.",
     "title_ar": "جدول حركات الشمس والقمر وحاصة القمر والعقد الشمالي في الشهور الرومية",
     "title_la": "Tabula motuum Solis, Lunae, anomaliae Lunae et nodi borealis / in mensibus Romanis.",
     "heads": "اسماء الشهور الرومية‖Nomina mensium / Romanorum.|‖Solis / motus medius.|‖Lunae / motus medius.|"
              "‖Motus / anomaliae Lunae.|‖Motus / nodi borealis."},
    {"pdf": 524, "ppage": "75", "fol": "f. 188,r.", "title_ar": "حركات الشمس والقمر وحاصة القمر والعقد الشمالي في الايام",
     "title_la": "Motus Solis, Lunae, anomaliae Lunae et nodi borealis in diebus.",
     "heads": "عدد الايام‖Numerus / dierum.|" + L4},
    {"pdf": 525, "ppage": "76", "fol": "f. 188,v.", "title_ar": "جدول حركة الشمس والقمر وحاصة القمر والعقد الشمالي في الساعات",
     "title_la": "Tabula motus Solis, Lunae, anomaliae Lunae et nodi borealis in horis.",
     "heads": "عدد الساعات / المستوية‖Numerus / horarum / aequino- / ctialium.|" + L4},
    {"pdf": 526, "ppage": "77", "fol": "f. 189,r.",
     "title_ar": "جدول حركات الشمس والقمر وحاصة القمر والعقد الشمالي في السنين الرومية المفردة",
     "title_la": "Tabula motuum Solis, Lunae, anomaliae Lunae et nodi borealis / in intervallis annorum Romanorum.",
     "heads": "سنون رومية / مفردة‖Intervalla / annorum / Romanor.|"
              "‖Solis motus medius. / 0° 11′ 10″ 14‴ 35{iv} / 31{v} 30{vi}.|"
              "‖Lunae motus medius. / 133° 35′ 33″ 11‴ 4{iv} / 59{v} 45{vi}.|"
              "‖Motus / anomaliae Lunae. / 39° 41′ 59″ 15‴ 5{iv} / 38{v} 55{vi}|‖Motus nodi borealis."},
]
with open(os.path.join(OUT, "mmr_pages.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pdf", "ppage", "fol", "title_ar", "title_la", "heads"], delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(pages)
print(len(rows), "rows;", Counter(c for r in rows for c in r["check"].replace(" ", "")))

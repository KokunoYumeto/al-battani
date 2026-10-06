"""Write the data of Nallino's Part II pp. 102-106 (mean motions of Saturn, Jupiter and Mars and the anomalies of Venus
and Mercury in the Roman calendar) to S06/mean_motions/: mm5r_p2.tsv (one row per printed row), mm5r_pages.tsv (titles
and heads) and mm5r_extra.tsv (the motions in 20 years printed under the single years of p. 103, to the thirds).
Values come from the readings resolved against the line of each column (mmr5_pages.py, MP{pdf}{tag}.json); the cells
in EYE were read by eye, and every single-reader cell was confirmed by Tesseract as a third reader or by eye."""
import csv, json, os
from collections import Counter
import wide_kit as wk

AB = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani"
OUT = os.path.join(AB, "S06", "mean_motions")
G = ["sat", "jup", "mars", "ven", "mer"]
MONTHS = ["ādhār [Martius].", "nīsān [Aprilis].", "ayyār [Maius].", "ḥazīrān [Iunius].", "tammūz [Iulius].",
          "āb [Augustus].", "aylūl [September].", "tishrīn I [October].", "tishrīn II [November].", "kānūn I [December].",
          "kānūn II [Ianuarius].", "subāṭ [Februarius]. / comm.", "bisext."]
PAGES = [("MP551", 551, "102", "collected", [str(931 + 20 * k) for k in range(34)]),
         ("MP552", 552, "103", "single", [str(n) for n in range(1, 21)]),
         ("MP552s", 552, "103", "intervals", [str(n) for n in (40, 60, 80, 100, 200, 400, 600)]),
         ("MP553", 553, "104", "months", MONTHS),
         ("MP554", 554, "105", "hours", [str(n) for n in range(1, 25)]),
         ("MP555", 555, "106", "days", [str(n) for n in range(1, 31)])]
EYE = {("MP551", 9, "jup"): ("78", "24"), ("MP551", 32, "ven"): ("166", "24"), ("MP551", 34, "sat"): ("212", "45"),
       ("MP551", 34, "mars"): ("94", "10"), ("MP551", 34, "mer"): ("20", "15"),
       ("MP552", 10, "mer"): ("185", "37"), ("MP552", 11, "mer"): ("239", "34"), ("MP552", 12, "mer"): ("296", "37"),
       ("MP552", 13, "mer"): ("350", "34"), ("MP552", 14, "mer"): ("44", "31"), ("MP552", 15, "mer"): ("98", "28"),
       ("MP552", 16, "mer"): ("155", "30"),
       ("MP552s", 7, "sat"): ("141", "23"), ("MP552s", 7, "mars"): ("11", "5"), ("MP553", 7, "jup"): ("17", "45")}
ARG_EYE = {("MP551", 32): "1551"}
DOUBT = {("MP551", 34): "212 for 242 (see the ledger)"}

rows = []
for name, pdf, pp, table, args in PAGES:
    d = json.load(open(wk.OUT + name + ".json", encoding="utf-8"))
    assert len(d["rows"]) == len(args), (name, len(d["rows"]))
    for i, r in enumerate(d["rows"]):
        n = i + 1
        if r.get("arg_exp") is not None:
            assert r["arg_ok"] or ARG_EYE.get((name, n)) == args[i], (name, n, r["arg"], args[i])
        rec = {"pdf": pdf, "ppage": pp, "table": table, "row": n, "arg": args[i]}
        checks = []
        for gi, g in enumerate(G):
            if (name, n, g) in EYE:
                vals, cl = EYE[(name, n, g)], "EE"
            else:
                cells = r["groups"][gi]
                vals = tuple(c["value"] for c in cells); cl = "".join(c["cls"] for c in cells)
                assert None not in vals and "C" not in cl, (name, n, g, vals, cl)
            rec[f"{g}_d"], rec[f"{g}_m"] = vals
            checks.append(cl)
        rec["check"] = " ".join(checks)
        rec["doubt"] = DOUBT.get((name, n), "")
        rows.append(rec)
fields = ["pdf", "ppage", "table", "row", "arg"] + [f"{g}_{k}" for g in G for k in "dm"] + ["check", "doubt"]
with open(os.path.join(OUT, "mm5r_p2.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(rows)

extra = [{"pdf": 552, "ppage": "103", "item": "years20", "sat": "244;42,44,20", "jup": "247;17,34,26",
          "mars": "228;22,10,49", "ven": "183;43,2", "mer": "14;27,43,20"}]
with open(os.path.join(OUT, "mm5r_extra.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pdf", "ppage", "item"] + G, delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(extra)

P5 = "زحل‖[Motus medius] / Saturni.|المشتري‖[Motus medius] / Iovis.|المريخ‖[Motus medius] / Martis.|"
pages = [
    {"pdf": 551, "ppage": "102", "fol": "f. 205,v.", "title_ar": "جداول حركات الخمسة الكواكب المتحيرة في السنين الرومية المجموعة",
     "title_la": "Tabulae motuum quinque planetarum in annis Romanis collectis [ab aera].",
     "heads": "سنو الروم المجموعة‖Anni Romani col- / lecti [ab aera].|وسط زحل‖Longitudo media / Saturni.|"
              "وسط المشتري‖Longitudo media / Iovis.|وسط المريخ‖Longitudo media / Martis.|حاصة الزهرة‖Anomalia / Veneris.|"
              "حاصة عطارد‖Anomalia / Mercurii."},
    {"pdf": 552, "ppage": "103", "fol": "f. 206,r.", "title_ar": "جدول حركات الكواكب الخمسة المتحيرة في السنين الرومية المبسوطة",
     "title_la": "Tabula motuum quinque planetarum in singulis annis Romanis.",
     "heads": "سنو الروم المبسوطة‖Anni Romani / singillatim.|وسط زحل‖Motus medius / Saturni.|وسط المشتري‖Motus medius / Iovis.|"
              "وسط المريخ‖Motus medius / Martis.|حاصة الزهرة‖Motus anomaliae / Veneris.|حاصة عطارد‖Motus anomaliae / Mercurii.",
     "subtitle": "*Summae annorum* (سنون مجموعة)."},
    {"pdf": 553, "ppage": "104", "fol": "f. 206,v.", "title_ar": "جداول حركات الكواكب الخمسة المتحيرة في الشهور الرومية",
     "title_la": "Tabulae motuum quinque planetarum in mensibus Romanis.",
     "heads": "اسماء الشهور الرومية‖Nomina mensium / Romanorum.|" + P5 +
              "الزهرة‖[Motus anoma- / liae] Veneris.|عطارد‖[Motus anoma- / liae] Mercurii."},
    {"pdf": 554, "ppage": "105", "fol": "f. 207,r.", "title_ar": "جداول حركات الكواكب الخمسة المتحيرة في الساعات المعتدلة",
     "title_la": "Tabulae motuum quinque planetarum in horis aequinoctialibus.",
     "heads": "الساعات المستوية‖Horae / aequinoctiales.|" + P5 +
              "حاصة الزهرة‖Motus anomaliae / Veneris.|حاصة عطارد‖Motus anomaliae / Mercurii.", "signature": "14"},
    {"pdf": 555, "ppage": "106", "fol": "f. 207,v.", "title_ar": "جداول حركات الكواكب الخمسة المتحيرة في الايام للشهر الرومي",
     "title_la": "Tabulae motuum quinque planetarum in diebus mensis Romani.",
     "heads": "عدد الايام‖Numerus dierum.|‖[Motus medius] / Saturni.|‖[Motus medius] / Iovis.|‖[Motus medius] / Martis.|"
              "‖Motus anomaliae / Veneris.|‖Motus anomaliae / Mercurii."},
]
with open(os.path.join(OUT, "mm5r_pages.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pdf", "ppage", "fol", "title_ar", "title_la", "heads", "subtitle", "signature"], delimiter="\t",
                       lineterminator="\n", restval="")
    w.writeheader(); w.writerows(pages)
print(len(rows), "rows;", Counter(c for r in rows for c in r["check"].replace(" ", "")))

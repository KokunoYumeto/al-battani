"""Write the data of Nallino's Part II pp. 78-83 (equation of the Sun; simple equation of the Moon, equation of the
anomaly, minutes to be added, least longinquity; latitude of the Moon) to S06/equations/. Values come from the
readings resolved against the empirical curves of lunar_pages.py (run_page3, MP{pdf}c.json); the groups in EYE were
read by eye on the contact sheets (whole group, both readings and the computation shown), as were the B cells in EYE.
Files: equations_p2.tsv (one row per printed row) and equations_pages.tsv (folio lines, titles and heads)."""
import csv, json, os
from collections import Counter
import wide_kit as wk

AB = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani"
OUT = os.path.join(AB, "S06", "equations")
os.makedirs(OUT, exist_ok=True)
G = [("n", 1), ("n_inv", 1), ("sun", 3), ("moon", 3), ("pro", 2), ("min", 1), ("inc", 2), ("lat", 3)]
EYE = {
    (527, 7, 6): "0 17", (527, 19, 3): "1 31 25", (531, 15, 1): "225",
    (528, 5, 3): "2 40 12", (528, 6, 3): "2 45 17", (528, 7, 3): "2 49 42", (528, 11, 3): "3 4 17", (528, 11, 4): "5 59",
    (528, 12, 0): "42", (528, 22, 6): "1 51", (528, 28, 2): "1 39 5", (528, 29, 2): "1 40 9", (528, 30, 2): "1 41 14",
    (529, 1, 2): "1 42 18", (529, 1, 3): "4 11 33", (529, 3, 3): "4 17 8", (529, 3, 7): "4 26 14", (529, 4, 3): "4 19 54",
    (529, 5, 3): "4 22 24", (529, 7, 3): "4 27 7", (529, 8, 3): "4 29 26", (529, 10, 3): "4 33 55", (529, 13, 3): "4 38 52",
    (529, 28, 3): "4 59 0", (529, 30, 3): "5 0 2", (529, 30, 5): "26",
    (530, 1, 3): "5 0 26", (530, 2, 3): "5 0 44", (530, 3, 3): "5 0 55", (530, 4, 3): "5 0 59", (530, 5, 3): "5 1 0",
    (530, 6, 3): "5 0 57", (530, 7, 3): "5 0 45", (530, 8, 3): "5 0 37", (530, 9, 3): "5 0 21", (530, 2, 2): "1 59 10",
    (530, 12, 2): "1 57 20", (530, 13, 2): "1 56 59", (530, 14, 2): "1 56 38", (530, 15, 2): "1 56 0", (530, 16, 2): "1 55 28",
    (530, 17, 2): "1 54 58", (530, 18, 2): "1 54 30", (530, 18, 3): "4 53 30", (530, 19, 2): "1 53 54", (530, 19, 3): "4 52 10",
    (530, 20, 2): "1 53 14", (530, 22, 3): "4 47 32", (530, 23, 3): "4 45 47", (530, 24, 3): "4 44 6", (530, 25, 2): "1 49 33",
    (531, 4, 2): "1 40 43", (531, 5, 2): "1 39 35", (531, 5, 3): "4 18 58", (531, 6, 2): "1 38 23", (531, 8, 3): "4 10 3",
    (531, 13, 3): "3 53 42", (531, 14, 2): "1 27 41", (531, 14, 7): "3 35 51", (531, 15, 2): "1 26 14", (531, 15, 7): "3 32 10",
    (531, 17, 3): "3 38 42", (531, 18, 3): "3 34 50", (531, 19, 7): "3 16 39", (531, 20, 7): "3 12 39", (531, 30, 2): "1 1 24",
    (532, 4, 5): "56", (532, 6, 1): "204", (532, 6, 7): "2 1 56", (532, 7, 3): "2 7 43", (532, 7, 7): "1 57 8",
    (532, 11, 3): "1 46 45",
}
DOUBT = {(528, 5, 3): "Nallino: 52″ for 12″", (528, 6, 3): "Nallino: 2° 44′ 57″ for 2° 45′ 17″",
         (528, 7, 3): "Nallino: 2″ for 42″", (532, 6, 1): "the 4 is printed broken"}

rows, classes = [], Counter()
for pdf in range(527, 533):
    d = json.load(open(wk.OUT + f"MP{pdf}c.json", encoding="utf-8"))
    assert len(d["rows"]) == 30
    for i, r in enumerate(d["rows"]):
        n = 30 * (pdf - 527) + i + 1
        rec = {"pdf": pdf, "ppage": str(pdf - 449), "row": i + 1}
        checks = []
        for gi, (name, places) in enumerate(G):
            if (pdf, i + 1, gi) in EYE:
                vals = EYE[(pdf, i + 1, gi)].split(); cl = "E" * places
            else:
                cells = r["groups"][gi]
                vals = [c["value"] for c in cells]; cl = "".join(c["cls"] for c in cells)
                assert None not in vals and "C" not in cl, (pdf, i + 1, gi, vals, cl)
            assert len(vals) == places, (pdf, i + 1, gi)
            keys = {1: [name], 2: [name + "_d", name + "_m"], 3: [name + "_d", name + "_m", name + "_s"]}[places]
            if name == "min":
                keys = ["min"]
            for k, v in zip(keys, vals):
                rec[k] = v
            checks.append(cl)
            classes.update(cl)
        assert int(rec["n"]) == n and int(rec["n_inv"]) == 360 - n, (pdf, i + 1, rec["n"], rec["n_inv"])
        rec["check"] = " ".join(checks)
        rec["doubt"] = "; ".join(v for (p, rr, g), v in DOUBT.items() if p == pdf and rr == i + 1)
        rows.append(rec)
fields = ["pdf", "ppage", "row", "n", "n_inv", "sun_d", "sun_m", "sun_s", "moon_d", "moon_m", "moon_s", "pro_d", "pro_m",
          "min", "inc_d", "inc_m", "lat_d", "lat_m", "lat_s", "check", "doubt"]
with open(os.path.join(OUT, "equations_p2.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(rows)

TA = "جداول تعديل الشمس وتعديل القمر المجموع الكلي بحصص البعدين وعرضه"
TL = "tabularum aequationis Solis, aequationis Lunae (cui semper adiectae / portiones ambarum longinquitatum){} et latitudinis Lunae."
pages = [{"pdf": 527, "ppage": "78", "fol": "f. 189,v.", "title_ar": "ابتداء " + TA, "title_la": "Initium " + TL.format(",")},
         {"pdf": 528, "ppage": "79", "fol": "f. 190,r.", "title_ar": "من " + TA, "title_la": "Ex tabulis" + TL.format("")[8:]},
         {"pdf": 529, "ppage": "80", "fol": "f. 190,v.", "title_ar": "من " + TA, "title_la": "Ex tabulis" + TL.format("")[8:]},
         {"pdf": 530, "ppage": "81", "fol": "f. 191,r.", "title_ar": "من " + TA, "title_la": "Ex tabulis" + TL.format(",")[8:]},
         {"pdf": 531, "ppage": "82", "fol": "f. 191,v.", "title_ar": "من " + TA, "title_la": "Ex tabulis" + TL.format("")[8:]},
         {"pdf": 532, "ppage": "83", "fol": "f. 192,r.", "title_ar": "تمام " + TA, "title_la": "Finis " + TL.format("")}]
AR_HEADS = "سطور العدد‖Columnae / numerorum.|مستوي‖Ordo / rectus.|منكوس‖Ordo / inversus.|تعديل الشمس‖Aequatio Solis.|" \
           "تعديل القمر المفرد‖Aequatio / simplex Lunae.|تعديل الحاصة‖Aequatio / anomaliae.|حصص البعد‖Portiones / longinquit.|" \
           "دقائق تزيد‖Minuta / addenda.|البعد الاقرب‖In longinquita- / te minima.|عرض القمر‖Latitudo Lunae."
for p in pages:
    heads = AR_HEADS if p["pdf"] == 527 else "|".join("‖" + h.split("‖")[1] for h in AR_HEADS.split("|"))
    p["heads"] = heads
with open(os.path.join(OUT, "equations_pages.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pdf", "ppage", "fol", "title_ar", "title_la", "heads"], delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(pages)
print(len(rows), "rows;", classes)
for p in pages:
    print(p["ppage"], p["title_la"])

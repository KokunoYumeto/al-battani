"""Write the data of Nallino's Part II pp. 108-137 (the equations of the five planets) to S06/planets/:
  planets_p2.tsv       one row per printed row: page, planet, row, n and 360 - n, column III (equation of the centre;
                       degrees, minutes), IV (sixtieths), V, VI, VII (degrees, minutes), how each number was established
                       (`check`), notes (`doubt`)
  planets_pages.tsv    folio line, Arabic and Latin title, heads (Arabic heads on p. 108 only), the line above the
                       first table of each planet (apogee and daily motion in anomaly), the notes «Decrescunt» and
                       «Crescunt» of column IV with the argument above which they stand, and the signature
Values come from the readings resolved by planet_pages.py (MP{pdf}b.json, the second pass against the empirical curves);
the groups in EYE were read by eye (the cells the curves flagged), and every single-reader cell was confirmed by
Tesseract as a third reader or by eye (TR sheets)."""
import csv, json, os
from collections import Counter
import wide_kit as wk

AB = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani"
OUT = os.path.join(AB, "S06", "planets")
os.makedirs(OUT, exist_ok=True)
PLANETS = [("sat", "Saturni", "زحل"), ("jup", "Iovis", "المشتري"), ("mars", "Martis", "المريخ"), ("ven", "Veneris", "الزهرة"),
           ("mer", "Mercurii", "عطارد")]
COLS = [("n2", 1), ("c3", 2), ("c4", 1), ("c5", 2), ("c6", 2), ("c7", 2)]
# (pdf, row, group) -> values read by eye (groups: 0 = II, 1 = III, 2 = IV, 3 = V, 4 = VI, 5 = VII)
EYE = {
    (557, 20, 2): ("55",), (557, 2, 4): ("0", "12"), (557, 3, 4): ("0", "18"), (558, 7, 2): ("47",), (559, 1, 0): ("299",),
    (559, 14, 3): ("0", "18"), (561, 22, 2): ("46",), (562, 1, 0): ("209",), (563, 3, 0): ("357",), (563, 18, 0): ("342",),
    (564, 21, 1): ("3", "58"), (564, 10, 3): ("0", "13"), (564, 19, 4): ("7", "20"), (564, 14, 5): ("0", "16"),
    (565, 16, 1): ("5", "3"), (565, 30, 1): ("5", "14"), (565, 26, 3): ("0", "27"), (565, 14, 4): ("9", "56"),
    (566, 11, 1): ("5", "13"), (566, 23, 2): ("23",), (567, 1, 1): ("4", "35"), (567, 29, 4): ("6", "45"),
    (568, 21, 3): ("0", "7"), (570, 1, 0): ("329",), (571, 30, 1): ("11", "23"), (571, 18, 4): ("29", "32"),
    (572, 21, 0): ("249",), (572, 22, 0): ("248",), (572, 24, 2): ("24",), (572, 2, 3): ("2", "32"), (572, 11, 3): ("2", "54"),
    (572, 25, 3): ("3", "34"), (572, 24, 4): ("39", "24"), (572, 27, 4): ("39", "55"), (572, 30, 4): ("40", "21"),
    (572, 15, 5): ("3", "35"), (572, 18, 5): ("3", "46"), (572, 27, 5): ("4", "22"),
    (574, 1, 0): ("209",), (574, 16, 0): ("194",), (574, 1, 1): ("6", "5"), (574, 16, 1): ("3", "5"), (574, 2, 2): ("52",),
    (574, 4, 2): ("53",), (574, 5, 2): ("54",), (574, 1, 3): ("5", "36"), (574, 6, 3): ("5", "38"), (574, 13, 3): ("5", "10"),
    (574, 24, 3): ("2", "26"), (574, 25, 3): ("2", "3"), (574, 1, 4): ("36", "57"), (574, 13, 4): ("27", "28"),
    (574, 14, 4): ("25", "16"), (574, 15, 4): ("24", "3"), (574, 16, 4): ("23", "45"), (574, 17, 4): ("22", "24"),
    (574, 19, 4): ("19", "0"), (574, 5, 5): ("7", "54"), (574, 6, 5): ("7", "58"),
    (575, 30, 3): ("0", "9"), (575, 12, 0): ("348",), (575, 14, 0): ("346",), (575, 17, 0): ("343",), (575, 21, 3): ("0", "6"), (575, 9, 5): ("0", "3"),
    (577, 23, 2): ("6",), (577, 30, 2): ("2",), (578, 30, 4): ("44", "13"), (579, 6, 1): ("1", "38"), (579, 23, 3): ("1", "23"),
    (580, 24, 0): ("186",), (580, 5, 1): ("0", "52"), (580, 24, 1): ("0", "13"), (580, 8, 2): ("56",), (580, 24, 3): ("0", "56"),
    (580, 25, 3): ("0", "48"), (580, 30, 3): ("0", "0"), (580, 2, 5): ("1", "42"), (580, 4, 5): ("1", "46"),
    (580, 6, 5): ("1", "48"),
    (581, 3, 0): ("357",), (581, 20, 0): ("340",), (581, 18, 2): ("54",), (581, 30, 2): ("44",), (581, 5, 3): ("0", "9"),
    (582, 1, 0): ("329",), (582, 21, 0): ("309",), (582, 1, 3): ("0", "51"), (582, 27, 3): ("1", "34"), (582, 1, 4): ("8", "20"),
    (582, 8, 5): ("0", "36"), (583, 2, 1): ("2", "29"), (583, 22, 1): ("2", "56"), (583, 23, 2): ("34",), (583, 7, 5): ("1", "5"),
    (584, 16, 0): ("254",), (584, 20, 1): ("2", "54"), (584, 9, 3): ("2", "44"), (584, 27, 3): ("3", "6"), (584, 29, 3): ("3", "7"),
    (584, 30, 3): ("3", "8"), (584, 30, 4): ("21", "47"), (584, 12, 5): ("1", "41"), (584, 20, 5): ("1", "48"),
    (585, 28, 2): ("49",), (585, 4, 5): ("1", "59"), (586, 1, 0): ("209",), (586, 4, 2): ("46",),
    # single-reader cells that the third reader (Tesseract) questioned, read by eye with their neighbours
    (557, 15, 3): ("0", "5"), (565, 14, 3): ("0", "25"), (581, 30, 4): ("8", "5"), (582, 2, 4): ("8", "35"),
    (582, 26, 5): ("0", "52"), (586, 9, 2): ("43",),
}
DOUBT = {(557, 1): "the 0 of 0° 6′ (column VI) is printed broken",
         (579, 6): "the 8 of 1° 38′ (column III) is printed damaged", (580, 8): "the 6 of 56 (column IV) is printed damaged",
         (567, 1): "the 5 of 4° 35′ (column III) is printed damaged", (572, 24): "the 4 of 24 (column IV) is printed thin",
         (565, 30): "Nallino, Part II p. 238: 5° 15′ for 5° 14′ (column III)",
         (566, 1): "Nallino, Part II p. 238: 5° 15′ for 5° 14′ (column III)"}


def planet_of(pdf):
    k = (pdf - 557) // 6
    return PLANETS[k], pdf - 557 - 6 * k


rows, classes = [], Counter()
for pdf in range(557, 587):
    (key, la, ar), k = planet_of(pdf)
    d = json.load(open(wk.OUT + f"MP{pdf}b.json", encoding="utf-8"))
    assert len(d["rows"]) == 30, (pdf, len(d["rows"]))
    for i, r in enumerate(d["rows"], 1):
        n = 30 * k + i
        rec = {"pdf": pdf, "ppage": str(pdf - 449), "planet": key, "row": i, "n": str(n)}
        checks = []
        for gi, (name, places) in enumerate(COLS):
            if (pdf, i, gi) in EYE:
                vals, cl = EYE[(pdf, i, gi)], "E" * places
            else:
                cells = r["groups"][gi]
                vals = tuple(c["value"] for c in cells); cl = "".join(c["cls"] for c in cells)
                assert None not in vals and "C" not in cl, (pdf, i, gi, vals, cl)
            assert len(vals) == places, (pdf, i, gi, vals)
            if places == 1:
                rec[name] = vals[0]
            else:
                rec[name + "_d"], rec[name + "_m"] = vals
            checks.append(cl); classes.update(cl)
        assert int(rec["n2"]) == 360 - n, (pdf, i, rec["n2"], n)
        rec["check"] = " ".join(checks)
        rec["doubt"] = DOUBT.get((pdf, i), "")
        rows.append(rec)
fields = ["pdf", "ppage", "planet", "row", "n", "n2", "c3_d", "c3_m", "c4", "c5_d", "c5_m", "c6_d", "c6_m", "c7_d", "c7_m",
          "check", "doubt"]
with open(os.path.join(OUT, "planets_p2.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(rows)
print(len(rows), "rows;", classes)

ABOVE = {
    557: ("بعد زحل الابعد سنة اقضا لذي القرنين رمد كح مسير حاصة زحل ليوم {0} نز",
          "[Longitudo] apogei Saturni anno 1191 a Dhū ’l-Qarnayn 244° 28′; motus diurnus anomaliae Saturni 0° 57′."),
    563: ("بعد المشتري الابعد لسنة اقضا لذي القرنين قصد كح مسير حاصة المشتري ليوم {0} ند",
          "[Longitudo] apogei Iovis anno 1191 a Dhū ’l-qarnayn 164° 28′; motus diurnus anomaliae Iovis 0° 54′."),
    569: ("بعد المريخ الابعد لسنة اقضا لذي القرنين قكو نح مسير حاصة المريخ ليوم {0} كح",
          "[Longitudo] apogei Martis anno 1191 a Dhū ’l-qarnayn 126° 58′; motus diurnus anomaliae Martis 0° 28′."),
    575: ("بعد الزهرة الابعد لسنة اقضا لذي القرنين قب يد",
          "[Longitudo] apogei Veneris anno 1191 a Dhū ’l-Qarnayn 82° 14′; [motus diurnus anomaliae Veneris 0° 37′.]"),
    581: ("بعد عطارد الابعد لسنة اقضا لذي القرنين را كح مسير حاصة عطارد ليوم ج و",
          "[Longitudo] apogei Mercurii anno 1191 a Dhū ’l-qarnayn 201° 28′; motus diurnus anomaliae Mercurii 3° 6′."),
}
NOTES = {k: v for k, v in {
    "sat": [(1, "Decrescunt"), (31, "Decrescunt"), (61, "Decrescunt"), (88, "Crescunt"), (91, "Crescunt"), (121, "Crescunt"),
            (151, "Crescunt")],
    "jup": [(1, "Decrescunt"), (31, "Decrescunt"), (61, "Decrescunt"), (89, "Crescunt"), (91, "Crescunt"), (121, "Crescunt"),
            (151, "Crescunt")],
    "mars": [(1, "Decrescunt"), (31, "Decrescunt"), (61, "Decrescunt"), (88, "Crescunt"), (91, "Crescunt"), (121, "Crescunt"),
             (151, "Crescunt")],
    "ven": [(1, "Decrescunt"), (31, "Decrescunt"), (61, "Decrescunt"), (89, "Crescunt"), (91, "Crescunt"), (121, "Crescunt"),
            (151, "Crescunt")],
    "mer": [(1, "Decrescunt"), (31, "Decrescunt"), (61, "Decrescunt"), (65, "Crescunt"), (91, "Crescunt"), (121, "Decrescunt"),
            (151, "Decrescunt")]}.items()}
SIG = {562: "15", 570: "16", 578: "17", 586: "18"}
HEADS_LA = ["Columnae / numerorum.", "I.", "II.", "III. / Aequatio ano- / maliae et centri.", "IV. / Portiones / duarum longin- / quitatum.",
            "V. / Longinquitas / maxima.", "VI. / Longinquitas / media; aequatio / anomaliae.", "VII. / Longinquitas / minima."]
HEADS_AR = ["سطرا العدد", "الاول", "الثاني", "الثالث / تعديل الحاصة والمركز", "الرابع / حصص البعدين", "الخامس / البعد الابعد",
            "السادس / البعد الاوسط / تعديل الحاصة", "السابع / البعد الاقرب"]
pages = []
for pdf in range(557, 587):
    (key, la, ar), k = planet_of(pdf)
    pp = pdf - 449
    fol = f"f. {(pp + 309) // 2},r." if pp % 2 else f"f. {(pp + 308) // 2},v."
    word_ar = "ابتداء جداول" if k == 0 else "تمام جداول" if k == 5 else "من جداول"
    title_ar = f"{word_ar} تعديل {ar} المجموع الكلي {'بابعادها' if key == 'ven' else 'بابعاده'} الثلثة"
    if k == 0:
        rest = ("semper compositae cum tribus / longinquitatibus eius." if key in ("sat", "ven")
                else "semper cum tribus eius longinquitatibus / compositae.")
        title_la = f"Initium tabularum aequationis {la}, {rest}"
    elif k == 5:
        title_la = f"Finis tabularum aequationis {la}, semper cum tribus eius longinquitatibus / compositae."
    else:
        title_la = f"Ex tabulis aequationis {la}, semper cum tribus eius longinquitatibus / compositae" + ("," if pp == 116 else ".")
    notes = " ".join(f"{n}:{w}" for n, w in NOTES[key] if 30 * k < n <= 30 * k + 30)
    above = ABOVE.get(pdf, ("", ""))
    pages.append({"pdf": pdf, "ppage": str(pp), "planet": key, "fol": fol, "above_ar": above[0], "above_la": above[1],
                  "title_ar": title_ar, "title_la": title_la,
                  "heads": "|".join((a if pdf == 557 else "") + "‖" + l for a, l in zip(HEADS_AR, HEADS_LA)),
                  "notes": notes, "signature": SIG.get(pdf, "")})
with open(os.path.join(OUT, "planets_pages.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(pages[0]), delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(pages)
print(len(pages), "pages")

"""Write the data of Nallino's Part II pp. 140-141 (the latitudes of the planets) to S06/latitudes/:
  latitudes_p2.tsv     one row per printed row and column: page, row, n and 360 - n, the column (sat_n, sat_s, jup_n,
                       jup_s, mars_n, mars_s on p. 140: the latitude at the northern and the southern limit; ven_inc,
                       ven_obl, mer_inc, mer_obl, portio on p. 141: inclination, obliquity, and the portions common to
                       all planets), degrees and minutes, how each number was established (`check`), notes (`doubt`)
  latitudes_pages.tsv  folio line, Arabic and Latin title, the heads, and the inscription in the margin of p. 140
Values: the eye reading of latitude_pages.py (EYE), checked against the glyph reader and the OCR text layer
(MP{pdf}e.json): class A where both give the value, B where one does (every B cell re-read by Tesseract; the 24 where
it gave another number were read by eye at 900 dpi), E where neither does (read by eye at 500 dpi)."""
import csv, json, os
from collections import Counter
import wide_kit as wk
import latitude_pages as lp

AB = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani"
OUT = os.path.join(AB, "S06", "latitudes")
os.makedirs(OUT, exist_ok=True)

rows, classes = [], Counter()
for pdf, cols in lp.COLUMNS.items():
    d = json.load(open(wk.OUT + f"MP{pdf}e.json", encoding="utf-8"))
    assert len(d["rows"]) == 30, (pdf, len(d["rows"]))
    for i, r in enumerate(d["rows"]):
        n = lp.NS[i]
        g0 = r["groups"][0][0]
        assert g0["value"] in (str(360 - n), None), (pdf, i, g0)
        c0 = g0["cls"].replace("C", "E")
        classes.update(c0)
        for gi, col in enumerate(cols, 1):
            u = lp.EYE[col][i]
            cells = r["groups"][gi]
            vals = tuple(c["value"] for c in cells)
            if None not in vals:
                assert vals == (str(u // 60), str(u % 60)), (pdf, i, gi, vals, u)
            cl = "".join(c["cls"] for c in cells).replace("C", "E")
            classes.update(cl)
            rows.append({"pdf": pdf, "ppage": str(pdf - 449), "row": i + 1, "n": str(n), "n2": str(360 - n),
                         "column": col, "d": str(u // 60), "m": str(u % 60), "check": f"{c0} {cl}", "doubt": ""})
fields = ["pdf", "ppage", "row", "n", "n2", "column", "d", "m", "check", "doubt"]
with open(os.path.join(OUT, "latitudes_p2.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(rows)
print(len(rows), "rows;", classes)

ARG = "سطري العدد / متفاضلة و و‖Columnae nume- / rorum, intervallo / sex graduum."
pages = [
    {"pdf": 589, "ppage": "140", "fol": "f. 224,v.",
     "title_ar": "جدول عروض الثلثة الكواكب العلوية", "title_la": "Tabula latitudinum trium planetarum superiorum.",
     "arg_head": ARG,
     "heads": "sat_n sat_s:عرض زحل يزاد على مركزه ن / خمسون‖Latitudo Saturni, cuius / centro 50° addendi."
              "|jup_n jup_s:عرض المشتري ينقص من مركزه ك / عشرون‖Latitudo Iovis, a cuius / centro 20° demendi."
              "|mars_n mars_s:عرض المريخ لا ينقص من مركزه / ولا يزاد عليه‖Latit. Martis, cuius centro ni- / hil "
              "addendum vel demendum.",
     "subheads": "شمال‖Septentrio.|جنوب‖Auster.|‖Septentrio.|‖Auster.|‖Septentrio.|‖Auster.",
     "margin": "افيثخون هو الشمال فرنجيون هو الجنوب‖« ἀπόγειον est septentriones, περίγειον auster ».",
     "signature": ""},
    {"pdf": 590, "ppage": "141", "fol": "f. 225,r.",
     "title_ar": "جدول عروض الكوكبين السفليين", "title_la": "Tabula latitudinum duorum planetarum inferiorum.",
     "arg_head": ARG,
     "heads": "ven_inc ven_obl:عرض الزهرة‖Latitudo Veneris.|mer_inc mer_obl:عرض عطارد‖Latitudo Mercurii,"
              "|portio:حصص العروض / لجميع الكواكب‖Portiones latitu- / dinum communes / omnibus planetis.",
     "subheads": "الميل‖Inclinatio.|الانحراف‖Obliquitas.|‖Inclinatio.|‖Obliquitas.",
     "margin": "", "signature": ""}]
with open(os.path.join(OUT, "latitudes_pages.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(pages[0]), delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(pages)
print(len(pages), "pages")

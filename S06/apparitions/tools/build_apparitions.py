"""Write the data of Nallino's Part II pp. 142-143 (the elongations for the apparitions and occultations of the planets
at latitude 36°) to S06/apparitions/:
  apparitions_p2.tsv     one row per printed row and column: page, row, sign, column, degrees and minutes, how each
                         number was established (`check`), notes (`doubt`). Columns: sat_app, sat_occ, jup_app, jup_occ,
                         mars_app, mars_occ (p. 142); ven_ort_vesp, ven_occ_mat, ven_ort_mat, ven_occ_vesp and the same
                         for mer (p. 143), in the order printed
  apparitions_pages.tsv  folio line, Arabic and Latin title, the head of the column of the signs, the heads of the
                         planets (with the columns they span) and of the single columns
Values: the eye reading of apparition_pages.py (EYE), checked against the glyph reader and the OCR text layer
(MP{pdf}e.json): class A where both give the value, B where one does (every B cell re-read by Tesseract; the 10 where it
gave another number were read by eye at 900 dpi and confirm the value)."""
import csv, json, os
from collections import Counter
import wide_kit as wk
import apparition_pages as ap

AB = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani"
OUT = os.path.join(AB, "S06", "apparitions")
os.makedirs(OUT, exist_ok=True)
NAMES = {"ven_ov": "ven_ort_vesp", "ven_om": "ven_occ_mat", "ven_orm": "ven_ort_mat", "ven_ocv": "ven_occ_vesp",
         "mer_ov": "mer_ort_vesp", "mer_om": "mer_occ_mat", "mer_orm": "mer_ort_mat", "mer_ocv": "mer_occ_vesp"}

rows, classes = [], Counter()
for pdf, cols in ap.COLUMNS.items():
    d = json.load(open(wk.OUT + f"MP{pdf}e.json", encoding="utf-8"))
    assert len(d["rows"]) == 12, (pdf, len(d["rows"]))
    for i, r in enumerate(d["rows"]):
        for gi, col in enumerate(cols):
            u = ap.EYE[col][i]
            cells = r["groups"][gi]
            vals = tuple(c["value"] for c in cells)
            assert vals == (str(u // 60), str(u % 60)), (pdf, i, gi, vals, u)
            cl = "".join(c["cls"] for c in cells)
            assert "C" not in cl, (pdf, i, gi, cl)
            classes.update(cl)
            rows.append({"pdf": pdf, "ppage": str(pdf - 449), "row": i + 1, "sign": ap.SIGNS[i],
                         "column": NAMES.get(col, col), "d": str(u // 60), "m": str(u % 60), "check": cl, "doubt": ""})
fields = ["pdf", "ppage", "row", "sign", "column", "d", "m", "check", "doubt"]
with open(os.path.join(OUT, "apparitions_p2.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(rows)
print(len(rows), "rows;", classes)

SIGNS_HEAD = "اسماء البروج‖Nomina signorum / zodiaci."
pages = [
    {"pdf": 591, "ppage": "142", "fol": "f. 225,v.",
     "title_ar": "جدول ابعاد الكواكب الثلثة العلوية للرؤية والاختفاء في الشرق والغرب لعرض لو",
     "title_la": "Tabula elongationum trium planetarum superiorum ad cognoscendas / apparitiones et occultationes in "
                 "oriente et occidente, ad latitudinem 36° 0′.",
     "signs_head": SIGNS_HEAD,
     "groups": "sat_app:رؤية زحل‖Apparitio / Saturni.|sat_occ:اختفاء زحل‖Occultatio / Saturni."
               "|jup_app:رؤية المشتري‖Apparitio / Iovis.|jup_occ:اختفاء المشتري‖Occultatio / Iovis."
               "|mars_app:رؤية المريخ‖Apparitio / Martis.|mars_occ:اختفاء المريخ‖Occultatio / Martis.",
     "subheads": "التشريق‖Ortus matutinus.|التغريب‖Occasus / vespertinus.|‖Ortus matutinus.|‖Occasus / vespertinus."
                 "|‖Ortus matutinus.|‖Occasus / vespertinus.",
     "signature": ""},
    {"pdf": 592, "ppage": "143", "fol": "f. 226,r.",
     "title_ar": "جدول ابعاد الكوكبين السفليين للروية والاختفاء في الشرق والغرب لعرض لو",
     "title_la": "Tabula elongationum duorum planetarum inferiorum ad cognoscendas appa- / ritiones et occultationes in "
                 "oriente et occidente, ad latitudinem 36° 0′.",
     "signs_head": "اسماء البروج‖Nomina / signorum / zodiaci.",
     "groups": "ven_ort_vesp ven_occ_mat:رؤية الز{rd:س=ه}رة‖Apparitio Veneris."
               "|ven_ort_mat ven_occ_vesp:اختفاء الزهرة‖Occultatio Veneris."
               "|mer_ort_vesp mer_occ_mat:رؤية عطارد‖Apparitio Mercurii."
               "|mer_ort_mat mer_occ_vesp:اختفاء عطارد‖Occultatio Mercurii.",
     "subheads": "طلوع / العشيات من / {0} الى قلز‖Ortus / vespertinus / a 0° ad 137°."
                 "|غروب / الغدوات من / ركج الى سص‖Occasus / matutinus / a 223° ad 360°."
                 "|طلوع / الغدوات من / قف الى ركج‖Ortus / matutinus / a 180° ad 223°."
                 "|غروب / العشيات من / قلز الى قف‖Occasus / vespertinus / a 137° ad 180°."
                 "|طلوع / العشيات من / {0} الى قيب‖Ortus / vespertinus / a 0° ad 112°."
                 "|غروب / الغدوات من / رمح الى سص‖Occasus / matutinus / a 248° ad 360°."
                 "|طلوع / الغدوات من / قف الى رمح‖Ortus / matutinus / a 180° ad 248°."
                 "|غروب / العشيات من / قيب الى قف‖Occasus / vespertinus / a 112° ad 180°.",
     "signature": ""}]
with open(os.path.join(OUT, "apparitions_pages.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(pages[0]), delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(pages)
print(len(pages), "pages")

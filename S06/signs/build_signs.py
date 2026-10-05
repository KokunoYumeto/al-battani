"""Write the data of Nallino's Part II pp. 7-8 to S06/signs/:
  p7_signs.tsv  p. 7, the signs of the Arab years and months in two schemes (I left, II right), as printed
  p8_signs.tsv  p. 8, the signs of the Roman (Syrian) months for the 28 years of the solar cycle, as printed
  signs_heads.tsv  titles and column heads of both pages
How the printed values were established: p. 7 was read by eye at 300 dpi (every value; clear print) and every
value agrees with the computation (calendars.py); p. 8 was read by the glyph reader and the OCR text layer, cell
by cell (classes A/B/C as for the concordance), the 31 cells not confirmed by both readers were checked by eye,
and every value agrees with the computation. So the printed values equal the computed ones; they are written here
from the computation, and check_signs.py recomputes them independently."""
import csv, os
import calendars as C

AB = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani"
OUT = os.path.join(AB, "S06", "signs")
os.makedirs(OUT, exist_ok=True)
MONTHS_AR = ["al–muḥarram", "ṣafar", "rabī‘ I", "rabī‘ II", "ǵumādà I", "ǵumādà II", "raǵab", "sha‘bān", "ramaḍān",
             "shawwāl", "dhū ’l–qa‘dah", "dhū ’l–ḥiǵǵah"]          # as printed: ‘ for ʿayn, ’ for the elision
LEN_AR = [30, 29] * 6
LEAP = {2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29}


def s7(x):
    return (x - 1) % 7 + 1          # 1..7


def m7(x):
    return x % 7                    # 0..6 (month signs of scheme I print 0)


rows7 = []
for k in range(1, 8):
    v = s7(5 * k)
    rows7.append({"part": "collected", "scheme": "I", "key": str(30 * k), "sign": str(v), "bis": "", "days": ""})
    rows7.append({"part": "collected", "scheme": "II", "key": str(30 * k), "sign": str(v), "bis": "", "days": ""})
for n in range(1, 31):
    w = C.weekday_sign(C.hijra_year_start(n))
    rows7.append({"part": "single", "scheme": "I", "key": str(n), "sign": str(w), "bis": "", "days": ""})
    rows7.append({"part": "single", "scheme": "II", "key": str(n), "sign": str(s7(w + 2)), "bis": "B" if n in LEAP else "", "days": ""})
before = 0
for i, name in enumerate(MONTHS_AR):
    rows7.append({"part": "month", "scheme": "I", "key": name, "sign": str(m7(before)), "bis": "", "days": str(LEN_AR[i])})
    rows7.append({"part": "month", "scheme": "II", "key": name, "sign": str(s7(m7(before) + 5)), "bis": "", "days": str(LEN_AR[i])})
    before += LEN_AR[i]

MONTHS_SY = [(9, "Aylūl"), (10, "Tishrīn I"), (11, "Tishrīn II"), (12, "Kānūn I"), (1, "Kānūn II"), (2, "Subāṭ"),
             (3, "Ādhār"), (4, "Nīsān"), (5, "Ayyār"), (6, "Ḥazīrān"), (7, "Tammūz"), (8, "Āb")]
rows8 = []
for r in range(1, 29):
    Y = 924 + (r - 1)               # a Seleucid year with (Y + 1) mod 28 = r
    y0 = Y - 312                    # the Julian year of its September
    rec = {"year": str(r)}
    for m, name in MONTHS_SY:
        jd = C.jd_julian(y0 if m >= 9 else y0 + 1, m, 1)
        rec[name] = str(C.weekday_sign(jd))
    rec["bis"] = "B" if r % 4 == 0 else str((r % 4) * 15)
    rows8.append(rec)

with open(os.path.join(OUT, "p7_signs.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["part", "scheme", "key", "sign", "bis", "days"], delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(rows7)
with open(os.path.join(OUT, "p8_signs.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["year"] + [n for _, n in MONTHS_SY[:6]] + ["bis"] + [n for _, n in MONTHS_SY[6:]],
                       delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(rows8)
HEADS = [
    {"page": "7", "item": "running head", "ar": "", "la": "AL-BATTANI OPUS ASTRONOMICUM"},
    {"page": "7", "item": "folio", "ar": "", "la": "f. 157,v."},
    {"page": "7", "item": "title", "ar": "جدول استخراج اوائل سني العرب وشهورهم بعلامات مختلفة ومعنى واحد",
     "la": "Tabula ad invenienda initia annorum et mensium Arabicorum / per differentia signa, quae [tamen] unam eandemque rem indicant."},
    {"page": "7", "item": "collected", "ar": "المجموعة", "la": "Anni collecti [ab aera]."},
    {"page": "7", "item": "single", "ar": "المبسوطة", "la": "Anni singuli."},
    {"page": "7", "item": "number", "ar": "عدد السنين", "la": "Annorum numerus."},
    {"page": "7", "item": "signs", "ar": "العلامات", "la": "Signa."},
    {"page": "7", "item": "number (single)", "ar": "عدد السنين", "la": "Annor. num."},
    {"page": "7", "item": "bissextile", "ar": "الكبائس", "la": "Bisextiles."},
    {"page": "7", "item": "months", "ar": "الشهور العربية", "la": "Menses Arabum."},
    {"page": "7", "item": "month names", "ar": "اسماء الشهور", "la": "Nomina mensium."},
    {"page": "7", "item": "month signs", "ar": "علاماتها", "la": "Eorum signa."},
    {"page": "7", "item": "month days", "ar": "عدد ايام الشهور", "la": "Numerus dierum mensis."},
    {"page": "8", "item": "running head", "ar": "", "la": "C. A. NALLINO"},
    {"page": "8", "item": "folio", "ar": "", "la": "f. 158,r."},
    {"page": "8", "item": "title", "ar": "علامات شهور الروم بتاريخ ذي القرنين المقسوم على كح بزيادة سنة",
     "la": "Signa mensium Romanorum secundum aeram Dhū ’l-qarnayn, / quae est per 28 dividenda et uno anno augenda."},
    {"page": "8", "item": "years", "ar": "سنو الروم المبسوطة", "la": "Singuli Romanorum anni."},
    {"page": "8", "item": "bissextile", "ar": "سطور الكبائس", "la": "Anni Bisextiles."},
] + [{"page": "8", "item": f"month {i + 1}", "ar": ar, "la": la + " / " + sy + " / " + d} for i, (ar, la, sy, d) in enumerate([
    ("ستنبر", "September.", "Aylūl.", "30 d."), ("اكتوبر", "October.", "Tishrīn I.", "31 d."),
    ("نونبر", "November.", "Tishrīn II.", "30 d."), ("دجنبر", "December.", "Kānūn I.", "31 d."),
    ("ينير", "Ianuarius.", "Kānūn II.", "30 d."), ("فبرير", "Februarius.", "Subāṭ.", "28 d."),
    ("مارس", "Martius.", "Ādhār.", "31 d."), ("ابريل", "Aprilis.", "Nīsān.", "30 d."),
    ("مايه", "Maius.", "Ayyār.", "31 d."), ("يونيه", "Iunius.", "Ḥazīrān.", "30 d."),
    ("يليه", "Iulius.", "Tammūz.", "31 d."), ("اغشت", "Augustus.", "Āb.", "31 d.")])]
with open(os.path.join(OUT, "signs_heads.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["page", "item", "ar", "la"], delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(HEADS)
print(len(rows7), "rows p. 7;", len(rows8), "rows p. 8;", len(HEADS), "heads")

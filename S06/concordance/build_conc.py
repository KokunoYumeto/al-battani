"""Write the data of Nallino's Part II pp. 9-18 (Tabulae I-X, the concordance of the Hijra with the Seleucid era)
to S06/concordance/: conc_p2.tsv (600 rows as printed) and conc_pages.tsv (page heads).
The printed values were established as follows (see the README): every cell was read by the glyph reader and by the
OCR text layer and compared with the computed calendar (calendars.py); cells where both readers gave the computed
value with high confidence are class A; cells where one reader gave it were checked by eye on contact sheets (class B);
the remaining cells (class C) were read by eye in context. The only printed values that differ from the computed
calendar are the eight in PRINTED below; every other cell prints the computed value."""
import csv, json, os
import calendars as C
import wide_kit as wk

AB = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani"
OUTDIR = os.path.join(AB, "S06", "concordance")
os.makedirs(OUTDIR, exist_ok=True)
ORD = ["الاول", "الثاني", "الثالث", "الرابع", "الخامس", "السادس", "السابع", "الثامن", "التاسع", "العاشر"]
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
FOL = ["f. 158,v.", "f. 159,r.", "f. 159,v.", "f. 160,r.", "f. 160,v.", "f. 161,r.", "f. 161,v.", "f. 162,r.",
       "f. 162,v.", "f. 163,r."]
SIG = {9: "2", 17: "3"}
# printed values that differ from the computed calendar: (ah, field) -> printed
PRINTED = {(61, "day"): "31", (145, "wd"): "5", (198, "sy"): "1125", (318, "day"): "3", (377, "sy"): "4298",
           (455, "day"): "4", (459, "sy"): "1278", (534, "day"): "26"}
DOUBT = {(420, "sy"): "the 4 is damaged: its stem and a trace of the crossbar printed, the diagonal did not",
         (414, "sy"): "an ink blot covers part of the 4",
         (600, "sy"): "a short stray rule stands before the number"}
HEADS_AR = "سنو الهجرة|اسم اول يوم من محرم|سنو ذي القرنين|الايام الماضية من الشهر / الرومي الذي بقع اول / المحرم فيه"
# pages where the last Latin head of the right half has no final period
NO_PERIOD_R = {10, 13}


def expected(n):
    jd = C.hijra_year_start(n)
    y, m, d = C.julian_from_jd(jd)
    sy = y + 312 if m >= 9 else y + 311
    return {"ah": n, "wd": C.weekday_sign(jd), "sy": sy, "day": d, "month": C.SYRIAN[m]}


rows, pages = [], []
for k in range(10):
    pdf, ppage = 458 + k, 9 + k
    d = json.load(open(wk.OUT + f"CAL{pdf}.json", encoding="utf-8"))
    cls = {}
    for r in d["rows"]:
        for f, ek in (("ah", "ah"), ("wd", "wd"), ("sy", "sy"), ("dm", "day")):
            exp = str(r["expected"][ek]); rd = r["read"][f]; tl = r["alt"][f]; cf = r["conf"][f] or 0
            c = "A" if (rd == exp and cf >= 0.85 and tl == exp) else "B" if (rd == exp or tl == exp) else "C"
            cls[(r["half"], r["row"], ek)] = c
    pages.append({"pdf": pdf, "ppage": ppage, "fol": d.get("fol", FOL[k]), "tabula": ROMAN[k],
                  "title_ar": f"الجدول {ORD[k]} من استخراج تاريخ العرب من تاريخ الروم وتاريخ الروم من تاريخ العرب",
                  "title_la": f"Tabula {ROMAN[k]} ad inveniendam aeram Arabum per aeram Romanorum / et Romanorum per Arabum.",
                  "heads_ar": HEADS_AR if ppage == 9 else "", "signature": SIG.get(ppage, ""),
                  "note": ("the last head of the right half has no final period" if ppage in NO_PERIOD_R else
                           "Arabic heads over the left half only; «بقع» printed with one dot below (for يقع); the م of «الرومي» "
                           "is a small filled loop with a dot-like mark beside it" if ppage == 9 else "")})
    for half, base in (("L", 1 + 60 * k), ("R", 31 + 60 * k)):
        prev = None                                  # each half starts with a month name, as printed
        for i in range(30):
            n = base + i
            e = expected(n)
            month = e["month"] if e["month"] != prev else "»"
            prev = e["month"]
            vals = {"ah": str(n), "wd": str(e["wd"]), "sy": str(e["sy"]), "day": str(e["day"])}
            doubts, checks = [], []
            for f in ("ah", "wd", "sy", "day"):
                if (n, f) in PRINTED:
                    doubts.append(f"{f}: printed {PRINTED[(n, f)]}, computed {vals[f]} (both readers and the eye)")
                    vals[f] = PRINTED[(n, f)]
                if (n, f) in DOUBT:
                    doubts.append(f"{f}: {DOUBT[(n, f)]}")
                checks.append(cls.get((half, i + 1, f), "?"))
            rows.append({"pdf": pdf, "ppage": ppage, "half": half, "row": i + 1, **vals, "month": month,
                         "check": "".join(checks), "doubt": "; ".join(doubts)})

with open(os.path.join(OUTDIR, "conc_p2.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pdf", "ppage", "half", "row", "ah", "wd", "sy", "day", "month", "check", "doubt"],
                       delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(rows)
with open(os.path.join(OUTDIR, "conc_pages.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pdf", "ppage", "fol", "tabula", "title_ar", "title_la", "heads_ar", "signature", "note"],
                       delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(pages)
from collections import Counter
print(len(rows), "rows;", Counter(c for r in rows for c in r["check"]))

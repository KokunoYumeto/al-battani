"""Write the data of Nallino's Part II pp. 93-94 (parallaxes of the Sun and the Moon in altitude) to S06/parallax/:
  parallax_p2.tsv   one row per printed row: the true zenith distance z (2 ... 90), the Sun's parallax (′ ″), the
                    Moon's parallax in the first term (′ ″), the difference of the second and the first (′ ″), the
                    parallax in the third term (° ′ ″), the difference of the fourth and the third (′ ″), and the
                    sixtieths for the epicycle at the apogee and at the perigee of the eccentre and for the eccentre
Values come from the readings resolved by parallax_pages.py (MP542, MP543); the groups in EYE were read by eye, and every
single-reader cell was confirmed by Tesseract as a third reader or by eye."""
import csv, json, os
from collections import Counter
import wide_kit as wk

AB = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani"
OUT = os.path.join(AB, "S06", "parallax")
os.makedirs(OUT, exist_ok=True)
COLS = [("sun", 2), ("t1", 2), ("d2", 2), ("t3", 3), ("d4", 2), ("epa", 2), ("epp", 2), ("ecc", 2)]
EYE = {(542, 1, 4): ("0", "50"), (542, 1, 5): ("0", "14"), (542, 1, 7): ("0", "15"), (542, 6, 6): ("2", "15"),
       (542, 8, 3): ("0", "21", "40"), (542, 17, 3): ("0", "44", "21"), (542, 18, 3): ("0", "46", "40"),
       (542, 20, 3): ("0", "51", "20"), (542, 21, 7): ("29", "54"), (542, 22, 2): ("7", "20"),
       (542, 22, 3): ("0", "55", "32"), (542, 22, 4): ("17", "20"), (542, 22, 6): ("27", "1"), (542, 22, 7): ("32", "0"),
       (543, 2, 3): ("0", "59", "20"), (543, 4, 5): ("35", "56"), (543, 7, 4): ("21", "10"), (543, 10, 4): ("22", "35"),
       (543, 12, 4): ("23", "20"), (543, 12, 6): ("50", "24"), (543, 15, 5): ("54", "57"), (543, 16, 5): ("56", "6"),
       (543, 17, 6): ("56", "3"), (543, 22, 6): ("59", "45")}
ARG_EYE = {(543, 5): "54"}
DOUBT = {}

rows, classes = [], Counter()
for pdf, pp, zs in ((542, "93", range(2, 45, 2)), (543, "94", range(46, 91, 2))):
    d = json.load(open(wk.OUT + f"MP{pdf}.json", encoding="utf-8"))
    zs = list(zs)
    assert len(d["rows"]) == len(zs), (pdf, len(d["rows"]))
    for i, r in enumerate(d["rows"], 1):
        z = zs[i - 1]
        assert r["arg_ok"] or ARG_EYE.get((pdf, i)) == str(z), (pdf, i, r["arg"], z)
        rec = {"pdf": pdf, "ppage": pp, "row": i, "z": str(z)}
        checks = []
        for gi, (name, n) in enumerate(COLS):
            if (pdf, i, gi) in EYE:
                vals, cl = EYE[(pdf, i, gi)], "E" * n
            else:
                cells = r["groups"][gi]
                vals = tuple(c["value"] for c in cells); cl = "".join(c["cls"] for c in cells)
                assert None not in vals and "C" not in cl, (pdf, i, gi, vals, cl)
            assert len(vals) == n
            for k, v in enumerate(vals, 1):
                rec[f"{name}_{k}"] = v
            checks.append(cl); classes.update(cl)
        rec["check"] = " ".join(checks)
        rec["doubt"] = DOUBT.get((pdf, i), "")
        rows.append(rec)
fields = ["pdf", "ppage", "row", "z"] + [f"{n}_{k}" for n, m in COLS for k in range(1, m + 1)] + ["check", "doubt"]
with open(os.path.join(OUT, "parallax_p2.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n", restval="")
    w.writeheader(); w.writerows(rows)
print(len(rows), "rows;", classes)

HEADS_LA = ["Numeri, intervallo duorum / graduum.", "Parallaxis / Solis.", "Primus / terminus.",
            "Secundus / terminus. / {sm:[Differentia].}", "Tertius / terminus.", "Quartus / terminus. / {sm:[Differentia].}",
            "[In apogeo] / epicycli.", "[In perigeo] / epicycli.", "In excen- / trico."]
HEADS_AR = ["سطر العدد المتفاضل / بجزئين جزئين", "اختلاف / منظر الشمس", "الحد الاول", "الحد الثاني", "الحد الثالث", "الحد الرابع",
            "فلك التدوير", "فلك التدوير", "الفلك الخارج"]
pages = [
    {"pdf": 542, "ppage": "93", "fol": "f. 197,v.",
     "title_ar": "جداول اختلاف منظر القمر في دائرة الارتفاع في حدود الابعاد الاربعة من قبل القسي والزوايا / وهي لبطليموس من كتاب "
                 "المجسطي ان شاء الله",
     "title_la": "Tabulae ad cognoscendas per arcus et angulos parallaxes Lunae in circulo / altitudinis, in quatuor terminis. "
                 "Ex Almagesto Ptolemaei, si Deus vult.",
     "heads": "|".join(a + "‖" + l for a, l in zip(HEADS_AR, HEADS_LA)),
     "groups": "[Parallaxis Lunae.]:3-6|[Sexagesimae partes.]:7-9"},
    {"pdf": 543, "ppage": "94", "fol": "f. 198,r.",
     "title_ar": "بقية جداول بطاميوس ذات التسعة الصفوف المتخذة لاختلاف منظر القمر في دائرة الارتفاع / في حدود الابعاد الاربعة من "
                 "قبل القسي والزوايا التامة ان شاء الله",
     "title_la": "Expliciunt tabulae Ptolemaei, novem columnis praeditae, sumendae ad cogno- / scendas per arcus et angulos "
                 "parallaxes Lunae in circulo altitudinis, in / quatuor terminis distantiarum, si Deus vult.",
     "heads": "|".join("‖" + l for l in HEADS_LA),
     "groups": "[Parallaxis Lunae.]:3-6|[Sexagesimae partes.]:7-9"},
]
with open(os.path.join(OUT, "par_pages.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pdf", "ppage", "fol", "title_ar", "title_la", "heads", "groups"], delimiter="\t",
                       lineterminator="\n")
    w.writeheader(); w.writerows(pages)

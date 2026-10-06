"""Write the data of Nallino's Part II pp. 138-139 (the stations of the planets) to S06/stations/:
  stations_p2.tsv      one row per printed row and planet: page, planet, row, n and 360 - n, Statio I and Statio II
                       (degrees, minutes), how each number was established (`check`), notes (`doubt`)
  stations_pages.tsv   folio line, Arabic and Latin title, the heads of the argument columns, of the planets and of
                       the two stations
Values: the eye reading of station_pages.py (EYE, Statio II = 360 - Statio I), checked against the glyph reader and the
OCR text layer (MP{pdf}e.json): class A where both give the value, B where one does (every B cell re-read by Tesseract;
the 46 where it gave another number were read by eye at 900 dpi), E where neither does (read by eye at 500 dpi)."""
import csv, json, os
from collections import Counter
import wide_kit as wk
import station_pages as sp

AB = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani"
OUT = os.path.join(AB, "S06", "stations")
os.makedirs(OUT, exist_ok=True)

rows, classes = [], Counter()
for pdf, keys in sp.PAGES.items():
    d = json.load(open(wk.OUT + f"MP{pdf}e.json", encoding="utf-8"))
    assert len(d["rows"]) == 30, (pdf, len(d["rows"]))
    for i, r in enumerate(d["rows"]):
        n = sp.NS[i]
        assert r["arg"] in (str(n), None) or r["arg_ok"], (pdf, i, r["arg"])
        g0 = r["groups"][0][0]
        c0 = g0["cls"].replace("C", "E")
        assert g0["value"] in (str(360 - n), None), (pdf, i, g0)
        classes.update(c0)                                   # the argument 360 - n, once per printed row
        for p, key in enumerate(keys):
            u1 = sp.EYE[key][i]; u2 = 21600 - u1
            rec = {"pdf": pdf, "ppage": str(pdf - 449), "planet": key, "row": i + 1, "n": str(n), "n2": str(360 - n),
                   "s1_d": str(u1 // 60), "s1_m": str(u1 % 60), "s2_d": str(u2 // 60), "s2_m": str(u2 % 60)}
            checks = [c0]
            for gi, u in ((1 + 2 * p, u1), (2 + 2 * p, u2)):
                cells = r["groups"][gi]
                vals = tuple(c["value"] for c in cells)
                if None not in vals:                         # resolved: it must be the eye value
                    assert vals == (str(u // 60), str(u % 60)), (pdf, i, gi, vals, u)
                checks.append("".join(c["cls"] for c in cells).replace("C", "E"))
            rec["check"] = " ".join(checks)
            rec["doubt"] = ""
            classes.update("".join(checks[1:]))
            rows.append(rec)
fields = ["pdf", "ppage", "planet", "row", "n", "n2", "s1_d", "s1_m", "s2_d", "s2_m", "check", "doubt"]
with open(os.path.join(OUT, "stations_p2.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(rows)
print(len(rows), "rows;", classes)

ARG_AR = {587: "سطري العدد / المتفاضلة و و", 588: "سطري العدد / متفاضلة و و"}
ARG_LA = "Columnae nume- / rorum, intervallo / sex graduum."
pages = [
    {"pdf": 587, "ppage": "138", "fol": "f. 223,v.",
     "title_ar": "جداول مقامات الكواكب الثلثة العلوية لمعرفة الرجوع والاستقامة",
     "title_la": "Tabulae stationum trium planetarum superiorum ad cognoscendos regressus / et progressus.",
     "arg_head": ARG_AR[587] + "‖" + ARG_LA,
     "planets": "sat:لزحل‖Saturnus.|jup:للمشتري‖Iupiter.|mars:للمريخ‖Mars.",
     "stations": "المقام الاول‖Statio I.|المقام الثاني‖Statio II.|‖Statio I.|‖Statio II.|‖Statio I.|‖Statio II.",
     "signature": ""},
    {"pdf": 588, "ppage": "139", "fol": "f. 224,r.",
     "title_ar": "جداول مقامات الكوكبين السفليين لمعرفة الرجوع والاستقامة",
     "title_la": "Tabulae stationum duorum planetarum inferiorum ad cognoscendos regressus / et progressus.",
     "arg_head": ARG_AR[588] + "‖" + ARG_LA,
     "planets": "ven:للزهرة‖Venus.|mer:لعطارد‖Mercurius.",
     "stations": "‖Statio I.|‖Statio II.|‖Statio I.|‖Statio II.",
     "signature": ""}]
with open(os.path.join(OUT, "stations_pages.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(pages[0]), delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(pages)
print(len(pages), "pages")

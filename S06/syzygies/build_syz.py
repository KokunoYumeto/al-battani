"""Write the data of Nallino's Part II pp. 29-32 (mean syzygies in Egyptian years) to S06/syzygies/.
Values come from the readings resolved against the line of each column (motion_page.py, MP{pdf}{tag}.json): class A
cells (both readers give the value), class B cells (one reader gives it; checked by eye), and the cells in EYE below,
read by eye (the fit flagged them, or a reader failed on the marks of a first row). Files:
  syz_p2.tsv     one row per printed row: page, table, argument, the day of thoth (or the days) in three places, the
                 mean longitude of the luminaries, the lunar anomaly, the argument of latitude (d m s), check, notes
  syz_pages.tsv  folio line, titles and heads of each table, and the units of its day column
  syz_extra.tsv  the line for 25 years under the table of p. 32 and the two eclipse-limit paragraphs"""
import csv, json, os
from collections import Counter
import wide_kit as wk

AB = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani"
OUT = os.path.join(AB, "S06", "syzygies")
os.makedirs(OUT, exist_ok=True)
G = ["day", "lum", "anom", "lat"]
# (json name, pdf, page, table, arguments)
TABLES = [("MP478", 478, "29", "conj", [str(915 + 25 * k) for k in range(32)]),
          ("MP479", 479, "30", "opp", [str(915 + 25 * k) for k in range(32)]),
          ("MP480a", 480, "31", "parts", ["Sexta mensis pars.", "Quarta mensis pars.", "Tertia mensis pars.", "Monsis dimidium."]),
          ("MP480b", 480, "31", "months", [str(n) for n in range(1, 13)]),
          ("MP480c", 480, "31", "intervals", ["50", "100", "200", "300", "400", "500", "600"]),
          ("MP481", 481, "32", "single", [str(n) for n in range(1, 25)])]
# cells read by eye: (table, row, group) -> (a, b, c) as printed
EYE = {("opp", 1, "day"): ("7", "28", "49"),
       ("opp", 12, "anom"): ("155", "55", "7"),
       ("opp", 23, "lum"): ("210", "5", "7"),
       ("opp", 30, "lat"): ("111", "8", "54"),
       ("months", 1, "day"): ("29", "31", "50"),
       ("months", 1, "lum"): ("29", "6", "25"),
       ("intervals", 7, "lum"): ("216", "38", "3"),
       ("single", 1, "lat"): ("38", "43", "3"),
       ("single", 6, "day"): ("24", "47", "50"),
       ("single", 10, "lat"): ("203", "8", "53"),
       ("single", 11, "day"): ("1", "9", "29"),
       ("single", 14, "day"): ("28", "19", "34"),
       ("single", 19, "day"): ("4", "41", "13"),
       ("single", 21, "lat"): ("54", "20", "36")}
DOUBT = {("opp", 12, "anom"): "155 for 153 (see the ledger)",
         ("opp", 23, "lum"): "210 for 240 (see the ledger)",
         ("opp", 30, "lat"): "111 for 211 (see the ledger)",
         ("single", 6, "day"): "Nallino: 40″ for 50″",
         ("single", 11, "day"): "Nallino: 39″ for 29″",
         ("single", 14, "day"): "Nallino: 24″ for 34″",
         ("single", 19, "day"): "Nallino: 23″ for 13″",
         ("parts", 4, "arg"): "«Monsis» for «Mensis» (Nallino, Part II p. 206)"}

rows = []
for name, pdf, pp, table, args in TABLES:
    d = json.load(open(wk.OUT + name + ".json", encoding="utf-8"))
    assert len(d["rows"]) == len(args), (name, len(d["rows"]))
    for i, r in enumerate(d["rows"]):
        n = i + 1
        rec = {"pdf": pdf, "ppage": pp, "table": table, "row": n, "arg": args[i]}
        checks = []
        for gi, g in enumerate(G):
            if (table, n, g) in EYE:
                vals = EYE[(table, n, g)]; cl = "EEE"
            else:
                cells = r["groups"][gi]
                vals = tuple(c["value"] for c in cells); cl = "".join(c["cls"] for c in cells)
                assert None not in vals, (table, n, g)
            rec[f"{g}_1"], rec[f"{g}_2"], rec[f"{g}_3"] = vals
            checks.append(cl)
        rec["check"] = " ".join(checks)
        rec["doubt"] = "; ".join(v for (t, rr, g), v in DOUBT.items() if t == table and rr == n)
        rows.append(rec)
fields = ["pdf", "ppage", "table", "row", "arg"] + [f"{g}_{k}" for g in G for k in "123"] + ["check", "doubt"]
with open(os.path.join(OUT, "syz_p2.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(rows)

LUM = "وسطيِ النيّرين‖Amborum luminarium / motus medii."
pages = [
    {"pdf": 478, "ppage": "29", "fol": "f. 170,v.", "table": "conj",
     "title_ar": "جدول اجتماعات الشمس والقمر الوسطى في السنين المصرية المجموعة",
     "title_la": "Tabula mediarum coniunctionum Solis et Lunae in annis Aegyptiis collectis.",
     "heads": "السنون المجموعة‖Anni collecti / [ab aera].|ايام توت‖Dies mensis Tōt.|وسطَيِ النيّرين‖Amborum luminarium / motus medii.|"
              "حاصة القمر‖Anomalia Lunae.|حركته في العرض‖Lunae motus / latitudinis.", "units": "d ′ ″"},
    {"pdf": 479, "ppage": "30", "fol": "f. 171,r.", "table": "opp",
     "title_ar": "جدول مقابلات الشمس والقمر الوسطى في السنين المصرية المجموعة",
     "title_la": "Tabula mediarum oppositionum Solis et Lunae in annis Aegyptiis collectis.",
     "heads": "السنون المجموعة‖Anni collecti / [ab aera].|ايام توت‖Dies mensis Tōt.|وسط الشمس والقمر قبالته‖Motus medius / Solis, et Lunae / in opposita parte.|"
              "حاصة القمر‖Anomalia Lunae.|حركته في العرض‖Lunae motus / latitudinis.", "units": "d ′ ″"},
    {"pdf": 480, "ppage": "31", "fol": "f. 171,v.", "table": "parts",
     "title_ar": "جدول تجزئة ايام الشهور وشهور القبط وجملة سنين مفردة للزيادة او النقصان",
     "title_la": "Tabula divisionis dierum et mensium Coptorum, et intervalla annorum / addenda aut demenda.",
     "subtitle_ar": "جدول ما يحتاج اليه من تجزئة ايام الشهر القبطي",
     "subtitle_la": "Tabula divisionis dierum Coptici mensis qua opus est uti.", "heads": "", "units": "d ′ ″"},
    {"pdf": 480, "ppage": "31", "fol": "", "table": "months",
     "title_ar": "", "title_la": "",
     "subtitle_ar": "جدول الاجتماعات والمقابلات في الشهور القبطية",
     "subtitle_la": "Tabula coniunctionum et oppositionum in mensibus Coptorum.",
     "heads": "عدد الشهور‖Numerus mensium.|الايام القمرية‖Dies lunares.|وسطيِ النيّرين‖Amborum lumina- / rium motus medii.|"
              "حاصة القمر‖Anomalia Lunae.|حركة العرض‖Lunae motus / latitudinis.", "units": "d ′ ″"},
    {"pdf": 480, "ppage": "31", "fol": "", "table": "intervals",
     "title_ar": "", "title_la": "", "subtitle_ar": "", "subtitle_la": "",
     "heads": "جملة سنين مفردة تزاد او / تنقص‖Intervalla annorum / quae adduntur aut de- / trahuntur.|"
              "تنقص مما يستانف وتزاد / على ما تقدم‖Demitur de eo / quod futurum est, / et additur ei quod / praecessit.|"
              + "|".join(["تزاد على ما يستانف / وتنقص مما تقدم‖Additur ei quod / futurum est, et de- / mitur de eo quod / praecessit."] * 3),
     "units": "′ ″ ‴"},
    {"pdf": 481, "ppage": "32", "fol": "f. 172,r.", "table": "single",
     "title_ar": "جدول الاجتماعات والاستقبالات الوسطى في السنين المصرية المبسوطة",
     "title_la": "Tabula mediarum coniunctionum et oppositionum in singulis annis Aegyptiis.",
     "heads": "السنون المبسوطة‖Singuli anni.|زيادات الايام‖Incrementa dierum.|" + LUM + "|حاصة القمر‖Anomalia Lunae.|"
              "حركة العرض‖Motus / latitudinis Lunae.", "units": "d ′ ″"},
]
pfields = ["pdf", "ppage", "fol", "table", "title_ar", "title_la", "subtitle_ar", "subtitle_la", "heads", "units"]
with open(os.path.join(OUT, "syz_pages.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=pfields, delimiter="\t", lineterminator="\n", restval="")
    w.writeheader(); w.writerows(pages)

extra = [
    {"pdf": 481, "ppage": "32", "item": "period25",
     "text": "25|0{d} 57′ 13″ 5{iii} 0{iv}|354° 1′ 35″ 6{iii} 26{iv}|57° 21′ 44″ 0{iii}|117° 12′ 5″ 51{iii}",
     "value": "25|0;57,13,5,0|354;1,35,6,26|57;21,44,0|117;12,5,51"},
    {"pdf": 481, "ppage": "32", "item": "eclipse_sun",
     "text": "*Termini eclipsis Solis* (حدود كسوف الشمس). — Si latitudinis motus medius a 159° 44′ ad 191° 16′ fuerit, "
             "a 0° ad 20° 16′, et a 348° 44′ ad 360°, poterit Sol deficere; alioquin nequibit.",
     "value": "159;44-191;16|0;0-20;16|348;44-360;0"},
    {"pdf": 481, "ppage": "32", "item": "eclipse_moon",
     "text": "*Termini eclipsis Lunae* (وحدود كسوف القمر). — Si medius latitudinis motus a 165° 13′ ad 194° 47′, "
             "a 0° ad 14° 47′, et a 345° 13′ ad 360° fuerit, poterit Luna deficere; alioquin nequibit.",
     "value": "165;13-194;47|0;0-14;47|345;13-360;0"},
]
with open(os.path.join(OUT, "syz_extra.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pdf", "ppage", "item", "text", "value"], delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(extra)
print(len(rows), "rows;", Counter(c for r in rows for c in r["check"].replace(" ", "")))

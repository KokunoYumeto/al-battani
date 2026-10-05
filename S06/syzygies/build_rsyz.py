"""Write the data of Nallino's Part II pp. 84-87 (mean syzygies in Roman years) to S06/syzygies/: rsyz_p2.tsv (one row
per printed row) and rsyz_pages.tsv (folio lines, titles, heads). Values come from the readings resolved by
roman_syz_pages.py (MP533, MP534, MP535b, MP536a/m/i); the groups in EYE were read by eye; every single-reader cell was
confirmed by Tesseract as a third reader or by eye."""
import csv, json, os
from collections import Counter
import wide_kit as wk

AB = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani"
OUT = os.path.join(AB, "S06", "syzygies")
G = ["day", "lum", "anom", "lat"]
MONTHS = ["ādhār.", "nīsān.", "ayyār.", "ḥazīrān.", "tammūz.", "āb.", "aylūl.", "tishrīn I.", "tishrīn II.", "kānūn I.",
          "kānūn II.", "subāṭ."]
SUMDAYS = ["31", "61", "92", "122", "153", "184", "214", "245", "275", "306", "337", "365"]
TABLES = [("MP533", 533, "84", "conj", [str(879 + 24 * k) for k in range(32)], 0),
          ("MP534", 534, "85", "opp", [str(879 + 24 * k) for k in range(32)], 0),
          ("MP535b", 535, "86", "single", [str(n) for n in range(1, 25)], 0),
          ("MP536a", 536, "87", "parts", ["Dimidium mensis.", "Tertia pars mensis.", "Quarta pars mensis.", "Sexta pars mensis."], 0),
          ("MP536m", 536, "87", "months", MONTHS, 1),
          ("MP536i", 536, "87", "intervals", [str(24 * m) for m in (2, 3, 4, 8, 12, 16, 20)], 0)]
EYE = {("conj", 32, "lat"): ("247", "3", "0"), ("opp", 1, "day"): ("28", "43", "59"), ("opp", 32, "day"): ("22", "15", "35"),
       ("single", 1, "anom"): ("335", "37", "2"), ("single", 12, "lum"): ("16", "55", "38"),
       ("parts", 1, "day"): ("14", "45", "55"), ("intervals", 1, "lum"): ("9", "29", "16"),
       ("intervals", 4, "lat"): ("153", "14", "18"), ("intervals", 5, "anom"): ("189", "55", "36"),
       ("intervals", 5, "lat"): ("229", "56", "27"), ("intervals", 6, "lat"): ("306", "28", "36"),
       ("intervals", 7, "lum"): ("7", "33", "26"), ("intervals", 7, "lat"): ("23", "5", "45")}
DOUBT = {("conj", 32, "lat"): "0″ for 51″ (see the ledger)",
         ("opp", 32, "day"): "22 for 23 (see the ledger)",
         ("single", 6, "day"): "Nallino: 50″ for 40″; the computation supports 40″ (see the ledger)",
         ("single", 11, "day"): "Schiaparelli (Nallino, Part II p. 230): the codex has 28ᵈ 9′ 39″, 358° 32′ 6″, 271° 4′ 19″, 211° 11′ 43″, "
                                "taken by an interpolator from p. 32",
         ("single", 22, "day"): "Schiaparelli (Nallino, Part II p. 230): the codex has 26ᵈ 19′ 18″, 357° 4′ 18″, 182° 8′ 39″, 62° 23′ 27″, "
                                "taken by an interpolator from p. 32",
         ("intervals", 2, "lat"): "Nallino (Schiaparelli): 52″ for 54″; codex 6″",
         ("intervals", 4, "lat"): "not reduced by the lunation that the day drops (see the ledger)",
         ("intervals", 5, "anom"): "Nallino (Schiaparelli): 184° for 189°",
         ("intervals", 5, "lat"): "Nallino (Schiaparelli): 51′ for 56′; codex 18′",
         ("intervals", 6, "lat"): "Nallino (Schiaparelli): 275° 48′ 22″ for 306° 28′ 36″; codex 275° 4′ 10″",
         ("intervals", 7, "lat"): "Nallino (Schiaparelli): 321° 45′ 17″ for 23° 5′ 45″; codex 291° 0′ 40″"}

rows, classes = [], Counter()
for name, pdf, pp, table, args, skip in TABLES:
    d = json.load(open(wk.OUT + name + ".json", encoding="utf-8"))
    assert len(d["rows"]) == len(args), (name, len(d["rows"]))
    for i, r in enumerate(d["rows"]):
        n = i + 1
        if r.get("arg_exp") is not None:
            assert r["arg_ok"] is not False or (table, n) in {}, (name, n, r["arg"], r["arg_exp"])
        rec = {"pdf": pdf, "ppage": pp, "table": table, "row": n, "arg": args[i]}
        if table == "months":
            g0 = r["groups"][0][0]
            assert g0["value"] == SUMDAYS[i], (name, n, g0["value"])
            rec["sumdays"] = SUMDAYS[i]
        checks = []
        for gi, g in enumerate(G):
            if (table, n, g) in EYE:
                vals, cl = EYE[(table, n, g)], "EEE"
            else:
                cells = r["groups"][gi + skip]
                vals = tuple(c["value"] for c in cells); cl = "".join(c["cls"] for c in cells)
                assert None not in vals and "C" not in cl, (table, n, g, vals, cl)
            rec[f"{g}_1"], rec[f"{g}_2"], rec[f"{g}_3"] = vals
            checks.append(cl); classes.update(cl)
        rec["check"] = " ".join(checks)
        rec["doubt"] = "; ".join(v for (t, rr, g), v in DOUBT.items() if t == table and rr == n)
        rows.append(rec)
fields = ["pdf", "ppage", "table", "row", "arg", "sumdays"] + [f"{g}_{k}" for g in G for k in "123"] + ["check", "doubt"]
with open(os.path.join(OUT, "rsyz_p2.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n", restval="")
    w.writeheader(); w.writerows(rows)

pages = [
    {"pdf": 533, "ppage": "84", "fol": "f. 192,v.", "table": "conj",
     "title_ar": "جداول اجتماعات الشمس والقمر الوسطى في السنين الرومية المجموعة",
     "title_la": "Tabulae mediarum coniunctionum Solis et Lunae in annis Romanis / collectis [ab aera].",
     "heads": "سنو الروم المجموعة‖Anni Romanorum / collecti [ab aera].|ايام اذار للاجتماعات‖Dies mensis ādhār / [Martii] usque ad / "
              "coniunctiones.|وسطي النيرين‖Amborum luminarium / motus medius.|حاصة القمر‖Anomalia Lunae.|حركة العرض‖Motus latitudinis / Lunae.",
     "units": "d ′ ″"},
    {"pdf": 534, "ppage": "85", "fol": "f. 193,r.", "table": "opp",
     "title_ar": "جداول مقابلات الشمس والقمر الوسطى في السنين الرومية المجموعة",
     "title_la": "Tabulae mediarum oppositionum Solis et Lunae in annis Romanis / collectis [ab aera].",
     "heads": "‖Anni Romanorum / collecti [ab aera].|ايام اذار لمعرفة الاستقبالات‖Dies mensis ādhār / ad cognoscendas / oppositiones.|"
              "وسط الشمس قبالة القمر‖Solis motus medius / in parte opposita / Lunae.|حاصة القمر‖Anomalia Lunae.|حركته في العرض‖Motus latitudinis / Lunae.",
     "units": "d ′ ″"},
    {"pdf": 535, "ppage": "86", "fol": "f. 193,v.", "table": "single",
     "title_ar": "جداول الاجتماعات والاستقبالات في السنين الرومية المبسوطة",
     "title_la": "Tabulae coniunctionum et oppositionum in singulis Romanorum annis.",
     "heads": "سنو الروم المبسوطة‖Anni Romanorum / singillatim.|ايام اذار للاجتماعات / والاستقبالات‖Dies mensis ādhār / ad syzygias.|"
              "وسطي الشمس والقمر‖Solis et Lunae / motus medius.|حاصة القمر‖Anomalia Lunae.|حركته في العرض‖Lunae motus / in latitudine.",
     "units": "d ′ ″"},
    {"pdf": 536, "ppage": "87", "fol": "f. 194,r.", "table": "parts",
     "title_ar": "جداول تجزئة ايام الشهر للاجتماعات والاستقبالات الاوسطين",
     "title_la": "Tabulae divisionis mensis ad [inveniendas] coniunctiones et oppositiones medias.", "heads": "", "units": "d ′ ″"},
    {"pdf": 536, "ppage": "87", "fol": "", "table": "months",
     "title_ar": "جداول الشهور الرومية للاجتماعات والاستقبالات الاوسطين",
     "title_la": "Tabulae mensium Romanorum ad [inveniendas] coniunctiones / et oppositiones medias.",
     "heads": "شهور الروم‖Menses / Romanorum.|جملة ايام مدة الشهور‖Summa dierum / mensium.|ايام الشهور القمرية‖Dies mensium / lunarium.|"
              "وسطي النيرين‖Amborum lumina- / rium motus medius.|حاصة القمر‖Anomalia Lunae.|حركته في العرض‖Motus Lunae / in latitudine.",
     "units": "d ′ ″"},
    {"pdf": 536, "ppage": "87", "fol": "", "table": "intervals", "title_ar": "سنون مفردة", "title_la": "Intervalla annorum",
     "heads": "", "units": "d ′ ″"},
]
with open(os.path.join(OUT, "rsyz_pages.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pdf", "ppage", "fol", "table", "title_ar", "title_la", "heads", "units"],
                       delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(pages)
print(len(rows), "rows;", classes)

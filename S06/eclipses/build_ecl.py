"""Write the data of Nallino's Part II pp. 88-91 (the tables for computing eclipses) to S06/eclipses/:
  motions_p2.tsv      p. 88: the true hourly motions of the Sun and the Moon (n, 360 - n, Sun ′ ″, Moon ′ ″), and the
                      small table of increments (degrees of mean elongation; ′ ″)
  correction_p2.tsv   p. 89: the table of correction (n, 360 - n, portions ′ ″, epicycle ′, eccentre ′)
  digits_p2.tsv       p. 89: the eclipsed areas (digits 1-12; Sun and Moon in digits and minutes) and the inclinations
                      (digits 0-21 and «compl.»; degrees)
  eclipses_p2.tsv     pp. 90-91: lunar and solar eclipses at the greatest and the least distance (latitude ′ ″,
                      incidence ′ ″, half duration ′ ″ for the Moon; digits)
  ecl_pages.tsv       folio lines, titles, heads and the lines under the tables
  ecl_text.tsv        the eclipse limits on p. 88 (Arabic and Latin)
Values come from the readings resolved by eclipse_pages.py (MP537, MP537s, MP538, MP538a, MP538i, MP539L/R,
MP540L/R); the cells in EYE were read by eye (the marks of a first row, the last rows of pp. 90-91); every
single-reader cell was confirmed by Tesseract as a third reader or by eye."""
import csv, json, os
from collections import Counter
import wide_kit as wk

AB = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani"
OUT = os.path.join(AB, "S06", "eclipses")
os.makedirs(OUT, exist_ok=True)
EYE = {("MP538a", 1, 0): ("0", "20"), ("MP538a", 1, 1): ("0", "30"),
       ("MP539L", 23, 3): ("21", "31", "30"), ("MP539R", 23, 3): ("21", "36"),
       ("MP540L", 13, 1): ("11", "23", "30"), ("MP540R", 14, 1): ("12", "33"),
       # flagged by the computation and read by eye (both readers agree)
       ("MP539L", 4, 1): ("26", "7"), ("MP539L", 5, 1): ("29", "45"), ("MP539L", 6, 1): ("33", "16"),
       ("MP539L", 13, 1): ("47", "7"), ("MP539L", 15, 1): ("35", "19"),
       ("MP539R", 20, 2): ("27", "42"), ("MP539R", 21, 2): ("28", "12"), ("MP539R", 22, 2): ("28", "53"),
       ("MP539R", 23, 2): ("28", "56"),
       ("MP540L", 6, 2): ("25", "47"), ("MP540L", 11, 2): ("30", "49"), ("MP540R", 5, 2): ("24", "50")}
DOUBT = {("eclipses", "solar_min", 14): "the ᵈ of 12ᵈ 33′ is printed damaged"}
classes = Counter()


def load(name):
    d = json.load(open(wk.OUT + name + ".json", encoding="utf-8"))
    return d["rows"]


def cell(name, i, gi, row):
    """the values of group gi of row i (1-based) and their classes"""
    if (name, i, gi) in EYE:
        vals = EYE[(name, i, gi)]
        classes.update("E" * len(vals))
        return list(vals), "E" * len(vals)
    cells = row["groups"][gi]
    vals = [c["value"] for c in cells]
    cl = "".join(c["cls"] for c in cells)
    assert None not in vals and "C" not in cl, (name, i, gi, vals, cl)
    classes.update(cl)
    return vals, cl


def write(name, fields, rows):
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n", restval="")
        w.writeheader(); w.writerows(rows)


# p. 88
rows = []
NS = list(range(0, 181, 6))
for i, r in enumerate(load("MP537"), 1):
    n2, c0 = cell("MP537", i, 0, r)
    assert r["arg_ok"] and int(n2[0]) == 360 - NS[i - 1], (i, r["arg"], n2)
    sun, c1 = cell("MP537", i, 1, r); moon, c2 = cell("MP537", i, 2, r)
    rows.append({"pdf": 537, "ppage": "88", "table": "hourly", "row": i, "arg": str(NS[i - 1]), "arg2": n2[0],
                 "sun_1": sun[0], "sun_2": sun[1], "moon_1": moon[0], "moon_2": moon[1], "check": f"{c1} {c2}"})
for i, r in enumerate(load("MP537s"), 1):
    v, c = cell("MP537s", i, 0, r)
    rows.append({"pdf": 537, "ppage": "88", "table": "increments", "row": i, "arg": str(i), "inc_1": v[0], "inc_2": v[1],
                 "check": c})
assert len(rows) == 31 + 7
write("motions_p2.tsv", ["pdf", "ppage", "table", "row", "arg", "arg2", "sun_1", "sun_2", "moon_1", "moon_2", "inc_1", "inc_2",
                         "check", "doubt"], rows)

# p. 89: correction
rows = []
for i, r in enumerate(load("MP538"), 1):
    n = 6 * i
    n2, c0 = cell("MP538", i, 0, r)
    assert r["arg_ok"] and int(n2[0]) == 360 - n, (i, r["arg"], n2)
    por, c1 = cell("MP538", i, 1, r); epi, c2 = cell("MP538", i, 2, r); ecc, c3 = cell("MP538", i, 3, r)
    rows.append({"pdf": 538, "ppage": "89", "table": "correction", "row": i, "arg": str(n), "arg2": n2[0],
                 "portion_1": por[0], "portion_2": por[1], "epicycle": epi[0], "eccentre": ecc[0],
                 "check": f"{c1} {c2} {c3}"})
assert len(rows) == 30
write("correction_p2.tsv", ["pdf", "ppage", "table", "row", "arg", "arg2", "portion_1", "portion_2", "epicycle", "eccentre",
                            "check", "doubt"], rows)

# p. 89: areas and inclinations
rows = []
for i, r in enumerate(load("MP538a"), 1):
    s, c1 = cell("MP538a", i, 0, r); m, c2 = cell("MP538a", i, 1, r)
    rows.append({"pdf": 538, "ppage": "89", "table": "areas", "row": i, "arg": str(i), "sun_1": s[0], "sun_2": s[1],
                 "moon_1": m[0], "moon_2": m[1], "check": f"{c1} {c2}"})
assert len(rows) == 12
inc = load("MP538i")
assert len(inc) == 23
for i, r in enumerate(inc, 1):
    vals = [cell("MP538i", i, g, r) for g in range(3)]
    rows.append({"pdf": 538, "ppage": "89", "table": "inclinations", "row": i, "arg": str(i - 1) if i < 23 else "compl.",
                 "sun_incl": vals[0][0][0], "moon_begin": vals[1][0][0], "moon_end": vals[2][0][0],
                 "check": " ".join(v[1] for v in vals)})
write("digits_p2.tsv", ["pdf", "ppage", "table", "row", "arg", "sun_1", "sun_2", "moon_1", "moon_2", "sun_incl", "moon_begin",
                        "moon_end", "check", "doubt"], rows)

# pp. 90-91
rows = []
for name, pdf, pp, table, kind in (("MP539L", 539, "90", "lunar_max", "lunar"), ("MP539R", 539, "90", "lunar_min", "lunar"),
                                   ("MP540L", 540, "91", "solar_max", "solar"), ("MP540R", 540, "91", "solar_min", "solar")):
    R = load(name)
    for i, r in enumerate(R, 1):
        rec = {"pdf": pdf, "ppage": pp, "table": table, "row": i}
        if kind == "lunar":
            lat, c1 = cell(name, i, 0, r); inc_, c2 = cell(name, i, 1, r); mora, c3 = cell(name, i, 2, r)
            dig, c4 = cell(name, i, 3, r)
            rec.update({"lat_1": lat[0], "lat_2": lat[1], "inc_1": inc_[0], "inc_2": inc_[1], "mora_1": mora[0],
                        "mora_2": mora[1], "check": f"{c1} {c2} {c3} {c4}"})
        else:
            lat, c1 = cell(name, i, 0, r); dig, c4 = cell(name, i, 1, r); inc_, c2 = cell(name, i, 2, r)
            rec.update({"lat_1": lat[0], "lat_2": lat[1], "inc_1": inc_[0], "inc_2": inc_[1], "check": f"{c1} {c4} {c2}"})
        if i < len(R):
            assert dig == [str(i - 1)], (name, i, dig)
        rec["digits"] = " ".join(dig)
        rec["doubt"] = DOUBT.get(("eclipses", table, i), "")
        rows.append(rec)
    assert len(R) == {"lunar_max": 23, "lunar_min": 23, "solar_max": 13, "solar_min": 14}[table], (table, len(R))
write("eclipses_p2.tsv", ["pdf", "ppage", "table", "row", "digits", "lat_1", "lat_2", "inc_1", "inc_2", "mora_1", "mora_2",
                          "check", "doubt"], rows)

pages = [
    {"pdf": 537, "ppage": "88", "fol": "f. 194,v.", "table": "hourly",
     "title_ar": "جدول حركتي الشمس والقمر المختلفة في الساعة المعتدلة في اوقات الاجتماعات والمقابلات",
     "title_la": "Tabula inaequalium motuum Solis et Lunae in hora aequinoctiali / temporibus coniunctionum et oppositionum.",
     "heads": "سطري العدد / المتفاضلين و و‖Columnae nume- / rorum intervallo / 6 graduum.|حركة الشمس / المختلفة في الساعة‖"
              "Motus inaequalis / horarius Solis.|حركة القمر المختلفة / في الساعة‖Motus inaequalis / horarius Lunae.",
     "footer_ar": "", "footer_la": ""},
    {"pdf": 537, "ppage": "88", "fol": "", "table": "increments", "title_ar": "", "title_la": "",
     "heads": "فضل ما بين الشمس / والقمر الاوسط‖Media differentia / [longitudinis] inter / Solem et Lunam.|الزيادة والنقصان في / "
              "حركة الشمس والقمر / في الساعة‖Incrementum et / diminutio motuum / horariorum Solis / et Lunae.",
     "footer_ar": "", "footer_la": ""},
    {"pdf": 538, "ppage": "89", "fol": "f. 195,r.", "table": "correction", "title_ar": "جدول لتقويم",
     "title_la": "Tabula correctionis.",
     "heads": "سطرا العدد / المتفاضلان ستة / اجزاء‖Columnae / numerorum / intervallo 6°.|حصص ابعاد / القمر‖Portiones / longinqui- / "
              "tatum Lu- / nae.|فلك التدوير‖Epicyclus.|الفلك الخارج‖Excentricus.",
     "footer_ar": "", "footer_la": ""},
    {"pdf": 538, "ppage": "89", "fol": "", "table": "areas",
     "title_ar": "وقدر اصابع الكسوف وانحراف القمر في الظلم في البدء والانجلا",
     "title_la": "Et [tabula] quantitatis digitorum eclipsis atque / inclinationis Lunae in obscuritate in initio / "
                 "[immersionis] et [fine] emersionis.",
     "heads": "عدد اصابع الكسوف من قطري النيرين‖Digiti diametrorum Solis et Lunae qui eclipsantur.|قدر ما ينكسف من دائرة الشمس "
              "بالمقدار / الذي به يكون تكسير دائرتها اثنتي عشرة اصبعا‖Quantitas disci solaris quae eclipsatur, cum sit / area "
              "disci in duodecim digitos divisa.|قدر ما ينكسف من دائرة القمر بالمقدار / الذي به يكون تكسير دائرته اثني عشر جزءا‖"
              "Quantitas disci lunaris quae eclipsatur, cum sit / area disci in duodecim partes divisa.",
     "footer_ar": "", "footer_la": ""},
    {"pdf": 538, "ppage": "89", "fol": "", "table": "inclinations", "title_ar": "", "title_la": "",
     "heads": "عدد اصابع الكسوف من اقطار النيرين‖Digiti ex diametris Solis et Lunae qui eclipsantur.|اول كسوف الشمس واخر "
              "انجلائها‖Initium eclipsis Solis et finis emersionis.|اول كسوف القمر واخر انجلائه‖Initium immersionis Lunae et "
              "finis emersionis.|اخر كسوف القمر واول انجلائه‖Finis immersionis Lunae et initium emersionis.",
     "footer_ar": "", "footer_la": "12"},
    {"pdf": 539, "ppage": "90", "fol": "f. 195,v.", "table": "lunar_max", "title_ar": "الكسوفات القمرية في البعد الابعد",
     "title_la": "Eclipses Lunae in maxima / longinquitate.",
     "heads": "عرض القمر / الحقيقي‖Latitudo / vera Lunae.|مقادير السقوط‖Quantitates / incidentiae.|مقدار المكث‖Quantitas / "
              "[dimidiae] / morae.|عدد الاصابع / المنكسفة من قطر / القمر‖Digiti diame- / tri lunaris / qui / eclipsantur.",
     "footer_ar": "تفاضله {0} ب كز ل", "footer_la": "Eius [i. e. latitudinis] intervallum 0° 2′ 27″ 30‴"},
    {"pdf": 539, "ppage": "90", "fol": "", "table": "lunar_min", "title_ar": "الكسوفات القمرية في البعد الاقرب",
     "title_la": "Eclipses Lunae in minima / longinquitate.",
     "heads": "‖Latitudo / vera Lunae.|‖Quantitates / incidentiae.|‖Quantitas / [dimidiae] / morae.|‖Digiti diame- / tri lunaris / "
              "qui / eclipsantur.",
     "footer_ar": "تفاضله {0} ب نو ل", "footer_la": "Eius [i. e. latitudinis] intervallum 0° 2′ 56″ 30‴"},
    {"pdf": 540, "ppage": "91", "fol": "f. 196,r.", "table": "solar_max", "title_ar": "اقدار كسوف الشمس في بعد / القمر الابعد",
     "title_la": "Eclipses Solis in maxima / longinquitate Lunae.",
     "heads": "عرض القمر / المرئي‖Latitudo / apparens / Lunae.|الاصابع / المنكسفة من / قطر الشمس‖Digiti diame- / tri solaris / qui / "
              "eclipsantur.|مقادير السقوط‖Quantitates / incidentiae.",
     "footer_ar": "تفاضله {0} ب مب ل", "footer_la": "Eius [i. e. latitudinis] intervallum / 0° 2′ 42″ 30‴"},
    {"pdf": 540, "ppage": "91", "fol": "", "table": "solar_min", "title_ar": "اقدار كسوف الشمس في بعد / القمر الاقرب",
     "title_la": "Eclipses Solis in minima / longinquitate Lunae.",
     "heads": "‖Latitudo / apparens / Lunae.|‖Digiti diame- / tri solaris / qui / eclipsantur.|‖Quantitates / incidentiae.",
     "footer_ar": "تفاضله {0} ب مب ل", "footer_la": "Eius [i. e. latitudinis] intervallum / 0° 2′ 42″ 30‴"},
]
write("ecl_pages.tsv", ["pdf", "ppage", "fol", "table", "title_ar", "title_la", "heads", "footer_ar", "footer_la"], pages)

text = [
    {"pdf": 537, "ppage": "88", "item": "limits_ar_sun",
     "text": "اما حدود كسوف الشمس اذا كانت حركة العرض الوسطى من قنط مد الى قضا يو ومن {0} الى ك يو ومن سمح مد الى تمام سص فانه "
             "يمكن ان تنكسف الشمس والا فلا تنكسف"},
    {"pdf": 537, "ppage": "88", "item": "limits_ar_moon",
     "text": "واما حدود كسوف القمر اذا كانت حركة العرض الوسطى من قصه يج الى قضد مز ومن {0} الى يد مز ومن سمه يج الى تمام سص فانه "
             "يمكن ان ينكسف القمر والا فلا تنكسف"},
    {"pdf": 537, "ppage": "88", "item": "limits_la_sun",
     "text": "*Termini eclipsis Solis.* — Si latitudinis motus medius a 159° 44′ ad 191° 16′ fuerit, et a 0° ad 20° 16′, et a "
             "348° 44′ ad 360°, poterit Sol deficere; alioquin nequibit."},
    {"pdf": 537, "ppage": "88", "item": "limits_la_moon",
     "text": "*Termini eclipsis Lunae.* — Si latitudinis motus medius a 165° 13′ ad 194° 47′ fuerit, et a 0° ad 14° 47′, et a "
             "345° 13′ ad 360°, poterit Luna deficere, alioquin nequibit."},
]
write("ecl_text.tsv", ["pdf", "ppage", "item", "text"], text)
print("classes", classes)

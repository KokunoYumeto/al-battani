"""Write the data of Nallino's Part II pp. 300-307 (the spurious tables) to S06/spurious/:
  spurious_p2.tsv      one row per printed number: page, table, row, argument, column, value, how it was established
                       (`check`), notes. Tables and columns:
                       p. 300  decades (arg 0 ... 210; columns decade, 1 ... 9), months (arg the month; days, sign)
                       p. 301  years (arg the collected years; collected_sign, single, single_sign), arab_months (sign),
                               persian (arg the Persian month; columns 1 ... 7)
                       p. 302  grid (arg the year 1 ... 28; oct, nov, dec, inter, jan ... sep), multiples (arg 28k; value)
                       p. 303  grid (arg the year 1 ... 28; the twelve Coptic months, bisext)
                       p. 304  conversion (arg 30 ... 660; R_anni R_menses R_dies R_fract C_... P_anni P_menses P_dies)
                       p. 305  years (arg 1 ... 30; bisext, S_anni S_menses S_dies S_fract P_anni P_menses P_dies),
                               months (arg the month; menses, dies)
                       p. 306  conjunctions, p. 307 oppositions (arg 1, 31 ... 631; I_dies I_horae I_min, II_s II_d
                               II_m II_sec, and the same for III and IV)
  spurious_heads.tsv   the titles and heads of every page (page, key, Arabic, Latin), and the folio lines
Values: the readings of spurious_pages.py (MP{pdf}e*.json), where the computation of each table gave the expected
value and the glyph reader and the OCR text layer classify each number: A both give it, B one, E neither (read by eye
at 450-600 dpi). Every B and E cell was read by eye on contact sheets (eye_sheet.py). The month blocks, the heads and
the cells in EYE were read by eye."""
import csv, json, os
from collections import Counter
import wide_kit as wk
import spurious_pages as sp

AB = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani"
OUT = os.path.join(AB, "S06", "spurious")
os.makedirs(OUT, exist_ok=True)
rows, classes = [], Counter()
# cells that neither reader gives and where the eye reading differs from the computation: (json, row, group) -> values
EYE = {("749e", 1, 0): ("0",),                          # p. 300: the sign of the decade 0 is printed 0 (computed 7)
       ("755eg", 9, 3): ("30", "25", "44"),             # p. 306, line 241, II: 2s 30° 25′ 44″ as printed
       ("749e", 10, 1): ("5",),                         # p. 300, year 91: the glyph reader alone read 4
       ("751eg", 27, 9): ("5",)}                        # p. 302, year 27, June: the glyph reader alone read 4
ARG_EYE = {("751em", 10): "280",                        # p. 302: the 8 of 280 is printed broken
           ("755eg", 17): "481", ("755eg", 19): "541"}  # p. 306: clearly printed; the text layer misreads them
DOUBT = {("302", "multiples", "280"): "the 8 of 280 is printed broken",
         ("302", "multiples", "616"): "the 2 of 1428 is printed broken",
         ("302", "grid", "6", "jun"): "a stray mark after the 6",
         ("302", "grid", "7", "sep"): "a dot after the 2",
         ("303", "grid", "11", "bawunah"): "a dot after the 2",
         ("304", "conversion", "210", "R_menses"): "a dot after the 6",
         ("306", "conjunctions", "241", "II_d"): "30° with the sign 2: 2s 30° for 3s 0°"}


def add(pdf, table, i, arg, col, value, cls, ppage=None):
    pp = ppage or str(pdf - 449)
    key = (pp, table, str(arg), col)
    doubt = DOUBT.get(key, DOUBT.get(key[:3], "") if col in ("value",) else "")
    rows.append({"pdf": pdf, "ppage": pp, "table": table, "row": i + 1, "arg": str(arg), "column": col,
                 "value": str(value), "check": cls, "doubt": doubt})
    classes.update(cls)


def take(name, cols, args, table, places=None, expected=None):
    """the values of MP{name}.json: one row per group (places > 1: one TSV row per place, column name + suffix)"""
    d = json.load(open(wk.OUT + f"MP{name}.json", encoding="utf-8"))
    assert len(d["rows"]) == len(args), (name, len(d["rows"]), len(args))
    for i, r in enumerate(d["rows"]):
        if r.get("arg_ok") is False:
            assert ARG_EYE.get((name, i + 1)) == str(args[i]), (name, i + 1, r["arg"], args[i])
        for gi, col in enumerate(cols):
            if col is None:
                continue
            cells = r["groups"][gi]
            vals = [c["value"] for c in cells]
            cls = [c["cls"] for c in cells]
            if (name, i + 1, gi) in EYE:
                vals, cls = list(EYE[(name, i + 1, gi)]), ["E"] * len(cells)
            elif None in vals:                           # read by eye: the eye reading is the computation
                exp = expected(i, gi)
                assert len(exp) == len(cells), (name, i, gi, exp)
                vals, cls = [str(x) for x in exp], ["E"] * len(cells)
            cols_ = [col] if len(cells) == 1 else [f"{col}_{s}" for s in places[gi]]
            for c, v, k in zip(cols_, vals, cls):
                add(d["pdf"], table, i, args[i], c, v, k.replace("C", "E"))


# p. 300
exp300 = sp.p300_expected()
take("749e", ["decade"] + [str(j) for j in range(1, 10)], list(range(0, 211, 10)), "decades",
     expected=lambda i, gi: [exp300[i][gi]])
MONTHS = ["al-muḥarram", "ṣafar", "rabīʿ I", "rabīʿ II", "ǵumādà I", "ǵumādà II", "raǵab", "shaʿbān", "ramaḍān",
          "shawwāl", "dhū ’l-qaʿdah", "dhū ’l-ḥiǵǵah"]
DAYS300 = ["30", "29", "30", "29", "30", "29", "30", "29", "30", "29", "30", "29 et {sfrac:11/30}"]
SIGNS = [1, 3, 4, 6, 7, 2, 3, 5, 6, 1, 2, 4]
for i, m in enumerate(MONTHS):
    add(749, "months", i, m, "days", DAYS300[i], "E")
    add(749, "months", i, m, "sign", SIGNS[i], "E")
# p. 301
years, persian, _ = sp.p301_expected()
take("750ey", ["collected_sign", "single", "single_sign"], list(range(30, 901, 30)), "years",
     expected=lambda i, gi: [years[i][gi]])
for i, m in enumerate(MONTHS):
    add(750, "arab_months", i, m, "sign", SIGNS[i], "E")
PMONTHS = ["farwardīn-māh", "ardibihisht-māh", "khurdādh-māh", "tīr-māh", "murdādh-māh", "shahrīwar-māh", "mihr-māh",
           "ābān-māh", "ādhar-māh", "day-māh", "bahman-māh", "isfandārmadh-māh"]
take("750ep", [str(c) for c in range(1, 8)], PMONTHS, "persian", expected=lambda i, gi: [persian[i][gi]])
# p. 302
g302, inter, mult = sp.p302_expected()
COLS302 = ["oct", "nov", "dec", "inter", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep"]


def exp302(i, gi):
    if gi == 3:
        return [inter[i]] if inter[i] != "B" else ["Bisext." if i == 2 else "B"]
    return [g302[i][gi if gi < 3 else gi - 1]]


take("751eg", COLS302, list(range(1, 29)), "grid", expected=exp302)
take("751em", ["value"], [a for a, b in mult], "multiples", expected=lambda i, gi: [mult[i][1]])
# p. 303
g303, bis = sp.p303_expected()
COLS303 = ["tut", "babah", "hatur", "kiyahk", "tubah", "amshir", "barmahut", "barmudhah", "bashans", "bawunah", "abib",
           "misri", "bisext"]
take("752eg", COLS303, list(range(1, 29)), "grid",
     expected=lambda i, gi: [g303[i][gi]] if gi < 12 else [bis[i] if bis[i] != "B" else ("Bisext." if i == 1 else "B")])
# p. 304
c304 = sp.p304_expected()
COLS304 = ["R_anni", "R_menses", "R_dies", "R_fract", "C_anni", "C_menses", "C_dies", "C_fract", "P_anni", "P_menses",
           "P_dies"]
take("753eg", COLS304, list(range(30, 661, 30)), "conversion", expected=lambda i, gi: [c304[i][gi]])
# p. 305: the B column from the computation, confirmed on the text layer and the scan (B in the 11 leap years)
y305, m305 = sp.p305_expected()
tlB = {(w[1] + w[3]) / 2 for w in wk.doc[754 - 1].get_text("words") if w[4].strip() == "B" and 95 < w[0] < 125}
d = json.load(open(wk.OUT + "MP754ey.json", encoding="utf-8"))
nB = sum(1 for r in d["rows"] if any(abs(r["y"] - y) < 5 for y in tlB))
assert nB == len(sp.LEAP_ARAB), nB
COLS305 = [None, "S_anni", "S_menses", "S_dies", "S_fract", "P_anni", "P_menses", "P_dies"]
take("754ey", COLS305, list(range(1, 31)), "years", expected=lambda i, gi: [y305[i][gi]])
for i in range(30):
    if (i + 1) in sp.LEAP_ARAB:
        r = d["rows"][i]
        add(754, "years", i, i + 1, "bisext", "B", "A" if any(abs(r["y"] - y) < 5 for y in tlB) else "E")
take("754em", ["menses", "dies"], MONTHS, "months", expected=lambda i, gi: [m305[i][gi]])
# pp. 306-307
for pdf, table in ((755, "conjunctions"), (756, "oppositions")):
    ex = sp.syz_expected(pdf)

    def exp_syz(i, gi, ex=ex):
        r = ex[i]
        if gi == 0:
            return [r[0]]
        if gi == 1:
            return list(r[1])
        c = r[2 + (gi - 2) // 2]
        return [c[0]] if gi % 2 == 0 else list(c[1:])
    take(f"{pdf}eg", ["I_dies", "I", "II_s", "II", "III_s", "III", "IV_s", "IV"], [1 + 30 * k for k in range(22)],
         table, places={1: ["horae", "min"], 3: ["d", "m", "sec"], 5: ["d", "m", "sec"], 7: ["d", "m", "sec"]},
         expected=exp_syz)
fields = ["pdf", "ppage", "table", "row", "arg", "column", "value", "check", "doubt"]
with open(os.path.join(OUT, "spurious_p2.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(rows)
print(len(rows), "numbers;", classes)
print(Counter((r["ppage"], r["table"]) for r in rows))

# titles and heads: (page, key, Arabic, Latin); ' / ' a line break
H = [
    ("297", "halftitle", "", "TABULAE SPURIAE"), ("297", "signature", "", "38"),
    ("300", "fol", "", "f. 240,v."),
    ("300", "title", "جدول استخراج علامات رؤس سني العرب ورؤس شهورهم – من زيج مسلمة",
     "Tabula ad invenienda signa initiorum annorum et mensium Arabum. / Ex opere astronomico Maslamae."),
    ("300", "decades_arg", "سنو العرب المجموعة المتفاضلة / ي ي", "Anni Arabum collecti / [ab aera] per decades."),
    ("300", "decade", "علامات مجموعة العشرات", "Signa decadum."),
    ("300", "singles", "سنو العرب المبسوطة", "Singuli Arabum anni."),
    ("300", "days", "عدد الايام من الشهور", "Numerus dierum / [singulorum] mensium."),
    ("300", "names", "اسماء الشهور", "Nomina mensium."),
    ("300", "sign", "علاماتها", "Eorum signa."),
    ("301", "fol", "", "f. 241,r."),
    ("301", "title_arab", "جدول علامات العرب", "Tabula signorum Arabum."),
    ("301", "title_pers", "جدول علامات الفرس", "Tabula signorum Persarum."),
    ("301", "collected", "المبسوطة", "[Anni] collecti."), ("301", "single", "المجموعة", "[Anni] singuli."),
    ("301", "numerus", "عدد", "Numerus / [annorum]."), ("301", "signa", "علامات", "Signa."),
    ("301", "menses", "الشهور", "Menses."),
    ("301", "maslamah", "من زيج مسلمة", "Ex opere astronomico Maslamae."),
    ("301", "pnames", "اسماء الشهور الفارسية", "Nomina mensium / Persicorum."),
    ("302", "fol", "", "f. 241,v."),
    ("302", "title", "جدول علامات السريان على ان الكبس في دجنبر وهو مذهب الروم",
     "Tabula signorum Syrorum, intercalatione mense Decembri posita / secundum methodum Romanorum."),
    ("302", "arg", "سطر العدد", "Numerus annorum."),
    ("302", "oct", "اكتوبر", "October.|31 dies"), ("302", "nov", "نونبر", "November.|30"),
    ("302", "dec", "دجنبر", "December.|31"), ("302", "inter", "سطر الكبس", "Columna intercalationis."),
    ("302", "jan", "ينير", "Ianuarius.|31"), ("302", "feb", "فبرير", "Februarius.|28"),
    ("302", "mar", "مارس", "Martius.|31"), ("302", "apr", "ابريل", "Aprilis.|30"), ("302", "may", "مايه", "Maius.|31"),
    ("302", "jun", "يونيه", "Iunius.|30"), ("302", "jul", "يليه", "Iulius.|31"), ("302", "aug", "اغشت", "Augustus.|31"),
    ("302", "sep", "شتنبر", "September.|30"),
    ("302", "multiples", "سطري المطرح كح كح", "Columnae [nume- / rorum] subtra- / hendorum, [qu / sunt] multipli 28"),
    ("303", "fol", "", "f. 242,r."),
    ("303", "title", "جدول لمعرفة رؤس سني القبط ورؤس شهورهم والكبس في اخر السنة",
     "Tabula ad cognoscenda initia annorum et mensium Coptorum; / et est intercalatio in fine anni."),
    ("303", "arg", "سطر العدد", "Numeri [annorum]."),
    ("303", "tut", "توت", "Tūt.|30"), ("303", "babah", "بابه", "Bābah.|30"), ("303", "hatur", "هتور", "Hatūr.|30"),
    ("303", "kiyahk", "كيهك", "Kiyahk.|30"), ("303", "tubah", "طوبه", "Ṭūbah.|30"),
    ("303", "amshir", "امشير", "Amshīr.|30"), ("303", "barmahut", "برمهوت", "Barmahūt.|30"),
    ("303", "barmudhah", "برموذه", "Barmūdhah.|30"), ("303", "bashans", "بشانس", "Bashāns.|30"),
    ("303", "bawunah", "بوونه", "Bawūnah.|30"), ("303", "abib", "ابيب", "Abīb.|30"),
    ("303", "misri", "مسري", "Misrī.|35"), ("303", "bisext", "الكبائس", "Bisextiles."),
    ("304", "fol", "", "f. 242,v."),
    ("304", "title", "جدول تحويل التواريخ بعضها الى بعض في مجموعة العرب",
     "Tabula conversionis aerarum in alias, secundum annos Arabicos collectos."),
    ("304", "arg", "سنو العرب المجموعة", "Anni Arabum collecti [ab aera]."),
    ("304", "R", "سنو الروم مكبسة محولة لسني الهجرة / – الاصل الرومي قبل الهجرة غلب ط / يز {0}",
     "Anni Romanorum, intercala- / tionem habentes, secundum an- / nos hegirae conversi. Aerae ini- / tium, ante "
     "hegiram, 932 an., / 9 m., 17 d., 0 fract."),
    ("304", "C", "سنو القبط المكبسة محولة لسني الهجرة / – الاصل القبطي قبل الهجرة سلز / ي يط مه",
     "Anni Coptorum, intercalatio- / nem habentes, secundum annos / hegirae conversi. Aerae initium, / ante hegiram, "
     "337 an., 10 m., / 19 d., 45 fract."),
    ("304", "P", "سنو الفرس مطلقة محولة / لسني الهجرة – الاصل / الفارسي بعد الهجرة ط يا ط",
     "Anni Persarum, sine / intercalatione, secun- / dum annos heg. con- / versi. Aerae initium, / p. heg., 9 a., "
     "11 m., 9 d."),
    ("304", "anni", "سنون", "Anni."), ("304", "menses", "شهور", "Menses."), ("304", "dies", "ايام", "Dies."),
    ("304", "fract", "كسور", "Fraction."),
    ("305", "fol", "", "f. 243,r."), ("305", "signature", "", "39"),
    ("305", "title", "جدول تحويل التواريخ بعضها الى بعض على مبسوطة العرب وشهورهم",
     "Tabula conversionis aerarum in alias, secundum singulos Arabum annos / et menses."),
    ("305", "arg", "سنو العرب المبسوطة", "Anni Arabum singuli."), ("305", "bisext", "كبائس العرب", "Bisextiles Arabum."),
    ("305", "S", "مبسوطة السريان وهي مكبسة", "Anni singuli Syrorum / cum intercalatione."),
    ("305", "P", "مبسوطة الفرس وهي مطلقة / غير مكبسة", "Anni singuli Persarum / sine intercalatione."),
    ("305", "sub", "", "Anni.|Menses.|Dies.|Fract."),
    ("305", "mhead", "شهور العرب تستعمل / في جميع التواريخ",
     "Menses Arabum, / qui [conversioni- / bus] omnium ha- / rum aerarum in- / serviunt."),
    ("305", "menses", "شهور", "Menses [harum aerarum]."), ("305", "dies", "ايام", "Dies."),
    ("306", "fol", "", "f. 243,v."),
    ("306", "title", "جدول اجتماعات الشمس والقمر في السنين العربية المجموعة",
     "Tabula coniunctionum Solis et Lunae in annis Arabicis collectis."),
    ("306", "arg", "السنون العربية المجموعة", "Anni Arabici collecti / [ab aera]."),
    ("306", "I", "الاول / ايام الزيادة على التاريخ", "I. / Dies incrementi / supra aeram."),
    ("306", "II", "الثاني / وسطي النيرين", "II. / Amborum luminarium / motus medius."),
    ("306", "III", "الثالث / حاصة القمر", "III. / Anomalia Lunae."),
    ("306", "IV", "الرابع / حركة العرض", "IV. / Motus latitudinis."),
    ("306", "sub", "", "Dies.|Horae.|Minuta.|Signa / zodiaci.|Gradus.|Min.|Sec."),
    ("307", "fol", "", "f. 244,r."),
    ("307", "title", "جدول استقبالات الشمس والقمر في السنين العربية المجموعة",
     "Tabula oppositionum Solis et Lunae in annis Arabicis collectis."),
    ("307", "arg", "", "Anni Arabum collecti / [ab aera]."),
    ("307", "I", "", "I. / Dies incrementi / supra aeram."), ("307", "II", "", "II. / Amborum luminarium / motus medius."),
    ("307", "III", "", "III. / Anomalia Lunae."), ("307", "IV", "", "IV. / Motus latitudinis."),
    ("307", "sub", "", "Dies.|Horae.|Minuta.|Signa / zodiaci.|Gradus.|Min.|Sec."),
]
with open(os.path.join(OUT, "spurious_heads.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["ppage", "key", "ar", "la"])
    w.writerows(H)
print(len(H), "heads")

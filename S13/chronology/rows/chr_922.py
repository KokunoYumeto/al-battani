# Chronology: Part III p. 230 (PDF 922), read 2026-10-05 (Part II pp. 2-3 are already entered with pp. 1-6).
# Footnote 8: f. 155,v. begins at Zeno (R16); on that folio the copyist kept the Eastern hundreds ض = 800, ظ = 900
# (check_chr.EAST_ROWS); a ض after the hundreds keeps the Maghribi 90 (ظضب = 992). Totals over 1000 are written as
# a separate ا (the thousand), a gap, and the rest: «ا ح» = 1008 (entered with a space).
TARGETS = {"P3": "chr_p3.tsv", "P3FN": "chr_p3_footnotes.tsv", "P3PAGE": "chr_p3_pages.tsv"}
E = ""


def k3(line, key, text, reg, total, doubt=E):
    return (922, 230, line, "row", "K", key, text, reg, E, E, total, E, E, doubt)


def h3(line, text, doubt=E):
    return (922, 230, line, "heading", "K", E, text, E, E, E, E, E, E, doubt)


P3 = [
    (922, 230, "H01", "colhead", "K", E, "اسماء الملوك|عدد ما ملكوا|مجموع السنين", E, E, E, E, E, E,
     "the same heads over both panels; a round speck before اسماء الملوك of the right panel in the master copy only"),
    k3("R01", "K66", "قلوذيوس", "ا", "ثضب"),
    k3("R02", "K67", "اوريلينوس{fn1}", "و", "ثضح"),
    k3("R03", "K68", "فربوس{fn2}", "ز", "خه", "ف with one dot (the codex has قربوس, fn2)"),
    k3("R04", "K69", "قاروس وقارينوس{fn3}", "ب", "خز"),
    k3("R05", "K70", "دقلطيانوس", "كا", "خكح"),
    h3("Rh1", "وبعد هذا ملوك النَّصْرانيّة"),
    k3("R06", "K71", "قوسطنطينس", "لب", "خص"),
    k3("R07", "K72", "قوسطوس", "كد", "خفد"),
    k3("R08", "K73", "يوليانس الحَنِيف", "ب", "خفو", "kasra under ن and two dots under ي, both copies"),
    k3("R09", "K74", "يوبيانس{fn4}", "ا", "خفز"),
    k3("R10", "K75", "ثاذوسيوس{fn5}", "يد", "ذا"),
    k3("R11", "K76", "وليس{fn6}", "يز", "ذيح"),
    k3("R12", "K77", "ارقاذيوس", "يج", "ذلا"),
    k3("R13", "K78", "ثاوذسيوس{fn7}", "مب", "ذعج"),
    k3("R14", "K79", "مارقيانس", "و", "ذعط"),
    k3("R15", "K80", "لأون", "يح", "ذضز"),
    k3("R16", "K81", "زينون{fn8}", "يز", "ضد", "total ضد in both copies: 804 with the Eastern ض of f. 155,v. (fn8); Part II 814"),
    k3("L01", "K82", "انسطاسيوس{fn9}", "كز", "ضما"),
    k3("L02", "K83", "يوسطينس الاوّل", "ط", "ضن"),
    k3("L03", "K84", "يوسطينينوس{fn10}", "لز", "ضفز"),
    k3("L04", "K85", "يوسطينس الثاني", "يد", "ظا"),
    k3("L05", "K86", "طيبريوس{fn11}", "د", "ظه"),
    k3("L06", "K87", "ماورقيوس{fn12}", "ك", "ظكه"),
    k3("L07", "K88", "فوقاس", "ح", "ظلج"),
    k3("L08", "K89", "هرقلس صاحب العرب", "لا", "ظصد"),
    k3("L09", "K90", "قسطنطنس", "ا", "ظصه"),
    k3("L10", "K91", "قوسطنطيوس{fn13}", "كز", "ظضب"),
    k3("L11", "K92", "لسطبوس{fn14}", "يو", "ا ح"),
    k3("L12", "K93", "طيبريوس{fn15} الثاني", "ى", "ا يح"),
    k3("L13", "K94", "يوسطينس", "ج", "ا كا", "printed يوسطينس (as for Iustinus in L02 and L04); Part II translates Iustinianus"),
    k3("L14", "K95", "ڡيقوس{fn16}", "ز", "ا كح", "no dot over the first letter in the master copy; the IA copy has only a faint small ring beside it"),
    k3("L15", "K96", "يوسطينينس{fn17}", "و", "ا لد", "Nallino's emendation of the codex قوسطنس (fn17); Part II translates Constantinus"),
    k3("L16", "K97", "فيلفقوس{fn18}", "ج", "ا لز"),
    k3("L17", "K98", "انسطاس{fn19}", "ب", "ا لط"),
    k3("L18", "K99", "ثاوذسيوس{fn20}", "ا", "ا م"),
]
P3FN = [
    (922, 1, "Cod. اقوتلينوس"),
    (922, 2, "Cod. قربوس"),
    (922, 3, "Cod. قارسوس"),
    (922, 4, "Cod. بوسانس"),
    (922, 5, "Cod. نادرسوس"),
    (922, 6, "Cod. ووليس"),
    (922, 7, "Cod. ناوذسيوس"),
    (922, 8, "Incipit f. 155,v., cui titulus: بقية جداول تاريخ ملوك النصرانية. In hac pag. amanuensis oblitus est litteras numerales orientales archetypi in maghrebinicas convertere; ergo hic ض = 800, ظ = 900."),
    (922, 9, "Cod. اسطاثبوس"),
    (922, 10, "Cod. بوقݐطݐوس"),
    (922, 11, "Cod. طنيربوس"),
    (922, 12, "Cod. ناورنقوس"),
    (922, 13, "Cod. قوسطنطينوس"),
    (922, 14, "Sic."),
    (922, 15, "Cod. طنيربوس"),
    (922, 16, "Sic."),
    (922, 17, "Cod. قوسطنس"),
    (922, 18, "Cod. قيقوس"),
    (922, 19, "Cod. السطاس"),
    (922, 20, "Cod. تاودسبونس"),
]
P3PAGE = [(922, 230, E, E)]

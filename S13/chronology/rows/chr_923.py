# Chronology: Part III p. 229 (PDF 923), read 2026-10-05 (Part II pp. 2-3 are already entered with pp. 1-6).
# Footnote words checked in both copies with pairs.py and dots.py (dot counts by size: footnote dots 1.1-1.6 pt,
# a pair 2.0-2.5 pt); table rows located from the ink bands of the names columns.
TARGETS = {"P3": "chr_p3.tsv", "P3FN": "chr_p3_footnotes.tsv", "P3PAGE": "chr_p3_pages.tsv"}
E = ""


def k3(line, key, text, reg, total, doubt=E):
    return (923, 229, line, "row", "K", key, text, reg, E, E, total, E, E, doubt)


def h3(line, text, doubt=E):
    return (923, 229, line, "heading", "K", E, text, E, E, E, E, E, E, doubt)


P3 = [
    (923, 229, "H01", "colhead", "K", E, "اسماء الملوك|عدد ما ملكوا|مجموع السنين", E, E, E, E, E, E, "the same heads over both panels, as on p. 228"),
    h3("Rh1", "وبعد هذا ملوك اتور{fn1}", "اتور: two dots over the tooth (ت), merged into a dumbbell, in both copies; Part II p. 2 prints اثور"),
    k3("R01", "K32", "فيافوس{fn2} ابو ذي القَرْنَيْن", "ز", "ز", "the letter after في is an alif, not a lām"),
    k3("R02", "K33", "الاسكندر البَنَّاء", "يب", "يط"),
    k3("R03", "K34", "بطلميوس أَرْنَب{fn3}", "ك", "لط", "the round mark over ر is a sukun; أرنب is Nallino's emendation of the codex اربيا (fn3), which his note in Part II p. 194 regrets (ارنبا, as in the Escorial codex, would have been better)"),
    k3("R04", "K35", "بطلميوس فيلاذلفوس", "لح", "عز"),
    k3("R05", "K36", "بطلميوس اورغطس الاوّل", "كه", "قب"),
    k3("R06", "K37", "بطلميوس فيليفطور", "يز", "قيط"),
    k3("R07", "K38", "بطلميوس افيفنيس", "كد", "قمج"),
    k3("R08", "K39", "بطلميوس فيليميطور", "له", "قعح"),
    k3("R09", "K40", "بطلميوس اورغطس الثاني", "كط", "رز"),
    k3("R10", "K41", "بطلميوس سوطر", "لو", "رمج"),
    k3("R11", "K42", "بطلميوس{fn4} ديونسيوس", "كط", "رعب"),
    k3("R12", "K43", "بطلميوس قلوبطرا", "كب", "رضد"),
    h3("Rh2", "وبعد هذا ملوك الروم"),
    k3("R13", "K44", "اغسطس", "مج", "سلز"),
    k3("R14", "K45", "طيبريوس", "كب", "سنط"),
    k3("R15", "K46", "غائيوس{fn5}", "د", "سصج"),
    k3("R16", "K47", "قلوذيوس", "يد", "سعز"),
    k3("L01", "K48", "نارون", "يد", "سضا"),
    k3("L02", "K49", "ويسفسيانوس{fn6}", "ى", "تا"),
    k3("L03", "K50", "طيطوس{fn7}", "ج", "تد"),
    k3("L04", "K51", "دومطيانوس{fn8}", "يه", "تيط"),
    k3("L05", "K52", "ناروس{fn9}", "ا", "تك"),
    k3("L06", "K53", "طرايانوس{fn10}", "يط", "تلط"),
    k3("L07", "K54", "اذريانس", "كا", "تص"),
    k3("L08", "K55", "انطونينس{fn11}", "كج", "تفج"),
    k3("L09", "K56", "قومذوس", "لب", "ثيه"),
    k3("L10", "K57", "ساوىرس{fn12}", "كه", "ثم", "the tooth after و has no dots in both copies"),
    k3("L11", "K58", "انطونينوس وَحْدَه{fn13}", "د", "ثمد"),
    k3("L12", "K59", "الكسندرس برغما{fn14}", "يج", "ثنز", "the dot of ب touches the stroke of ر"),
    k3("L13", "K60", "مكسميانوس{fn15}", "ج", "ثص"),
    k3("L14", "K61", "غورديانوس", "و", "ثصو"),
    k3("L15", "K62", "فيلفس", "و", "ثعب"),
    k3("L16", "K63", "ذاقيانس", "ا", "ثعج"),
    k3("L17", "K64", "غالس", "ج", "ثعو"),
    k3("L18", "K65", "والرينس{fn16}", "يه", "ثضا"),
]
P3FN = [
    (923, 1, "Error amanuensis; in titulo f. 155,r. recte legitur الملوك اليونانية"),
    (923, 2, "Cod. قيلقوس"),
    (923, 3, "Cod. اربيا. Cognomina sequentium Ptolemaeorum hoc modo in cod. deformata leguntur: قيذايقش, اوعسطس, قيلنقطوس, افيقينس, قنليقطور, اوعسطوس, سرسوطر, ديولسلير"),
    (923, 4, "Incipit f. 155,r., cui titulus جدول تاريخ الملوك اليونانية والرومية من لدن قيلقوس"),
    (923, 5, "Cod. غالبوس; cf. {sp:al-Bīr.} ٩٢ et {sp:al-Mas‘ūdī}, *Tanbīh* ١٢٢, adn."),
    (923, 6, "Cod. ويسقيسرموس"),
    (923, 7, "Cod. طنطوس"),
    (923, 8, "Cod. ذومطيناوس"),
    (923, 9, "Cod. ثادوس"),
    (923, 10, "Cod. طوايانوس"),
    (923, 11, "Cod. انطوينيش"),
    (923, 12, "Cod. ساوطيلس"),
    (923, 13, "Cod. انطوبلبوس وجده"),
    (923, 14, "Sic; pro بن ماميا. Codd. {sp:al-Bīr.} ٩٤ بزيما; {sp:Al-Mas‘ūdī}, *Prairies* II, 306 الاسكندر مامياس; *Tanbīh* ١٣٣ الاسكندرس يلقَّب مامياس; {sp:Abū ’l-farag}, ed. Ṣālḥānī ١٢٦ الكسندروس بن ماما etc."),
    (923, 15, "Cod. مكسابوس"),
    (923, 16, "Cod. وارثيس"),
]
P3PAGE = [(923, 229, E, E)]

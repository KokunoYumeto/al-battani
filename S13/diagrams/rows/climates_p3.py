"""Part III p. 243 (master PDF 909, codex fol. 196,v.): the circular diagram of the seven climes, as printed.
Read 2026-10-05 at 300-2600 dpi from polar unwraps and radial strips of both copies (master and Internet Archive,
IA page 44); every value and every difference from Part II was read in both copies.

Angles t: degrees counterclockwise from the right-hand horizontal of the page. The page has south at the top
(t = 90) and east on the left (t = 180). Nallino's azimuth in his note (Part II p. 234), from south through east, is
t - 90. Rings 1-7 from the innermost; radii in master pt from the centre (328.7, 453.6)."""

# The ring cells: line angle -> (degrees, minutes) for rings 1..7. At every line the degrees stand on the side of the
# line toward the horizontal axis, the minutes on the side toward the vertical axis (checked at each line).
CELLS = {
    22.5: ["يب|ج", "يب|يط", "يج|كز", "يد|كج", "يه|كو", "يو|لج", "يز|مج"],
    45: ["كا|يا", "كب|يح", "كج|كه", "كه|كط", "كز|كو", "كط|لج", "لا|مو"],
    67.5: ["كد|لط", "كو|{0}", "كز|نب", "كط|مح", "لب|لح", "لو|لز", "لز|كح"],
    112.5: ["كد|لط", "كو|{0}", "كز|مب", "كط|مح", "لب|ح", "لد|نز", "لز|كح"],
    135: ["كا|يا", "كب|لح", "كج|مه", "كه|مط", "كز|كو", "كط|لج", "لا|مو"],
    157.5: ["يب|ج", "يب|لط", "ىج|كز", "يد|كج", "يه|كو", "يو|لج", "يز|مج"],
    202.5: ["يب|ج", "يب|لط", "تج|كز", "يد|كج", "يه|كو", "يو|لج", "يز|مج"],
    225: ["كا|يا", "كب|يح", "كج|مه", "كه|مط", "كز|كو", "كط|لج", "لا|مو"],
    247.5: ["كد|يط", "كو|{0}", "كز|ىب", "كط|مح", "لب|ح", "لد|يز", "لز|كح"],
    292.5: ["كد|لط", "كو|{0}", "كز|يب", "كط|يح", "لب|ح", "لد|نز", "لز|كح"],
    315: ["كا|يا", "كب|يح", "كج|كه", "كه|كط", "كز|كو", "كط|لج", "لا|يو"],
    337.5: ["يب|ج", "يب|يط", "يج|كز", "يد|كج", "يه|كو", "يو|لج", "يز|كج"],
}
CELL_DOUBT = {
    (45, 3, "deg"): "a small ه-like loop stands beside كج in the cell, both copies",
    (135, 6, "deg"): "the ط of كط is oddly formed (an extra stroke), both copies; read ط",
    (157.5, 3, "deg"): "the first letter is a tooth without dots (ى), both copies",
    (202.5, 3, "deg"): "printed ت: a tooth with two dots above, both copies",
    (247.5, 3, "min"): "the first letter is a tooth without dots (ى), both copies",
}

# The axes: line angle -> (counterclockwise side, clockwise side) for rings 1..7.
AXES = {
    0: [("{0}", "{0}")] * 7,
    180: [("{0}", "{0}")] * 7,
    # top, azimuth of the south: the climes; clockwise (right) side الاقليم or the number of the clime, counterclockwise
    # (left) side the ordinal or the latitude
    90: [("الاول", "الاقليم"), ("كه", "ب"), ("ل", "ج"), ("الرابع", "الاقليم"), ("ما", "ه"), ("مه", "و"),
         ("السابع", "الاقليم")],
    # bottom, azimuth of the north: the longest day of each clime; counterclockwise (right) side the hours,
    # clockwise (left) side «its hours»
    270: [("يج", "ساعاته"), ("يج ل", "ساعاته"), ("يد", "ساعاته"), ("يد ل", "ساعاته"), ("يه", "ساعاته"),
          ("يه ل", "ساعاته"), ("يو", "ساعاته")],
}
AXIS_DOUBT = {
    (270, 1, "cw"): "written ساعا with ته above it (narrow cell), both copies",
}

# Labels outside the outer circle: measured centre angle, radius (pt; the start of a radial label, the middle of a
# tangential one), orientation, text, note.
# radial: the word starts at the rim and runs outward, its top toward the clockwise side;
# tangential: along the circle, top outward; upright: as normal text on the page.
LABELS = [
    ("azimuth", 91.5, 284, "tangential", "سمت الجنوب {ov:ض}", "ض = 90 in Maghribi abjad, overlined as a numeral"),
    ("azimuth", 271.0, 282, "upright", "سمت الشمال {ov:ض}", "ض = 90, overlined; set upright on the page"),
    ("sign", 42.6, 274, "radial", "الدلو", ""),
    ("sign", 47.4, 274, "radial", "القوس", ""),
    ("sign", 67.7, 274, "radial", "الجدي", ""),
    ("sign", 112.8, 275, "radial", "الجدي", ""),
    ("sign", 133.1, 276, "radial", "الدلو", ""),
    ("sign", 137.7, 276, "radial", "القوس", ""),
    ("sign", 155.3, 275, "radial", "العقرب", ""),
    ("sign", 160.7, 274, "radial", "الحوت", ""),
    ("sign", 175.9, 280, "tangential", "الحمل", "above the horizontal axis"),
    ("sign", 184.4, 279, "tangential", "الميزان", "below the horizontal axis"),
    ("sign", 201.1, 275, "radial", "السنبلة", ""),
    ("sign", 205.4, 274, "radial", "الثور", ""),
    ("sign", 223.5, 276, "radial", "الجوزاه", "the last letter is a closed loop (ه), both copies"),
    ("sign", 227.3, 276, "radial", "الاسد", ""),
    ("sign", 247.1, 276, "radial", "السرطان", ""),
    ("sign", 292.4, 276, "radial", "السرطان", ""),
    ("sign", 313.7, 274, "radial", "الجوزاه", "the last letter is a closed loop (ه), both copies"),
    ("sign", 317.2, 275, "radial", "الاسد", ""),
    ("colhead", 60.3, 278, "tangential", "درج", "over the degrees of the 67.5 line"),
    ("colhead", 73.4, 280, "tangential", "دقائق", "over the minutes of the 67.5 line"),
    ("colhead", 106.9, 277, "tangential", "درج", "over the minutes of the 112.5 line (the degrees are on its other side)"),
    ("colhead", 117.7, 280, "tangential", "دقائق", "over the degrees of the 112.5 line"),
    ("colhead", 240.5, 277, "tangential", "درج", "over the degrees of the 247.5 line"),
    ("colhead", 251.4, 280, "tangential", "دقائق", "over the minutes of the 247.5 line"),
    ("colhead", 286.5, 276, "tangential", "درج", "over the minutes of the 292.5 line (the degrees are on its other side)"),
    ("colhead", 296.8, 278, "tangential", "دقائق", "over the degrees of the 292.5 line"),
]

# The names inside the innermost circle, one on each of the 16 directions; written along the radius, starting at
# the circle and running inward, top toward the counterclockwise side.
WINDS = {
    0: ("رهفرس", "the ف has its dot, both copies; Part II p. 234 prints the codex form رهڡرس"),
    22.5: ("لبعوس", "a tooth with a dot below between ل and ع, both copies; Part II p. 234 prints لعوس"),
    45: ("ليبونطس", ""),
    67.5: ("بونطس", ""),
    90: ("ىوطس", "the first tooth has no dot, both copies"),
    112.5: ("بوبوطس", ""),
    135: ("هوىعس", "the fourth letter is a closed loop with a pointed top; read ع, as Part II p. 234"),
    157.5: ("صدوس", ""),
    180: ("اڡلىطس", "dotless ف and a small dotless tooth before the ط, both copies"),
    202.5: ("سعانس", "the ن has its dot, both copies; Part II p. 234 prints the codex form سعاىس"),
    225: ("بورىوٮ", "the last letter is a shallow bowl without teeth or dot (ٮ)"),
    247.5: ("افر{stroke}ىطس", "a short free stroke stands between ر and ى, both copies; Part II p. 234: افر...ىطس"),
    270: ("بعدىاس", "the master shows a dot high above the tooth with a speck beside it, the IA copy none: "
                     "a mark in one copy only, entered without dot (Part II p. 234: بعدىاس)"),
    292.5: ("افريقس", ""),
    315: ("برقسىس", "after the ق two low teeth, a taller tooth, then three teeth and the bowl"),
    337.5: ("اىاقونس", "the second letter is a tooth joined to the following alif"),
}

CORNERS = {
    "TL": ["المشارق الشِّتَوِيَّة", "اورى نطس"],
    "TR": ["المغارب الشِّتَوِيَّة", "قاطرغربا"],
    "BL": ["اريقنفوس", "المشارق الصيْفيّة"],
    "BR": ["ارقطوس", "المغارب الصيْفيّة"],
}

TITLE = [
    "مَدار الاقاليم السبعة الممَثَّلة بدَوَاىِر الآفاق واجزاء سَمْت مطالع ومغارب البروج من أُفْق كلّ إقْليم",
    "وهو مقدار بُعْده عن مَطْلَع الاعتدال ومَغْرِبه في الشَّمال والجَنوب",
]
TITLE_DOUBT = [
    "الممَثَّلة: the first م is the small loop at the foot of the ل (as in المشارق), the fatha stands over the second; "
    "بدَوَاىِر: the tooth before the ر has no dots and a kasra below",
    "",
]
HEADER = {"page": "243", "fol": "Fol. 196,v."}

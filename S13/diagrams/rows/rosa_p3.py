"""Part III p. 244 (master PDF 908, codex fol. 197,r.): the astrological figure (Nallino's «rosa astrologica»), as
printed. Read 2026-10-05 at 500-2600 dpi from radial strips and unrolled rings of both copies (master and Internet
Archive, IA page 43).

Geometry (master pt): centre (292.0, 407.0); circles at 77.4, 115.9, 153.9, 182.0, 209.1, 263.9; twelve sector
lines at 30k - 1 degrees (the scan is turned about 1 degree). Angles t: degrees counterclockwise from the right-hand
horizontal of the page. The signs run counterclockwise from Aries (89-119) at the top; within a sign the order of the
terms and faces runs counterclockwise too. Rings from the inside: 1 houses and exaltations (merged in the codex),
2 faces, 3 and 4 the triplicities (Nallino: the outer part gives the lords by day, the inner by night), 5 terms.
Orientation: terms and faces are written along the radius, starting at the inner circle, the tops of the letters
toward the clockwise side; triplicities, ring 1 and the sign names are written along the circles, tops outward,
starting at the clockwise end."""

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn",
         "Aquarius", "Pisces"]
SECTOR_START = {s: (89 + 30 * i) % 360 for i, s in enumerate(SIGNS)}     # the clockwise line of each sign
RADII = [77.4, 115.9, 153.9, 182.0, 209.1, 263.9]

# Ring 5, the terms: per sign, five (angle, planet, degrees) from the beginning of the sign.
TERMS = {
    "Aries": [(92.5, "مشتري", "ه"), (98.1, "زهرة", "ح"), (103.7, "عطارد", "و"), (109.5, "مريخ", "ه"), (115.2, "زحل", "ه")],
    "Taurus": [(122.6, "زهرة", "ح"), (128.0, "عطارد", "ز"), (133.9, "مشتري", "و"), (140.2, "زحل", "ج"), (145.2, "مريخ", "و")],
    "Gemini": [(152.8, "عطارد", "ح"), (158.0, "مشتري", "و"), (163.7, "زهرة", "ز"), (169.2, "مريخ", "ج"), (174.6, "زحل", "د")],
    "Cancer": [(182.9, "مريخ", "ز"), (188.2, "مشتري", "و"), (193.1, "زهرة", "ز"), (198.8, "عطارد", "ز"), (205.1, "زحل", "ج")],
    "Leo": [(212.4, "عطارد", "و"), (217.4, "زهرة", "ز"), (223.1, "مشتري", "و"), (229.5, "زحل", "ز"), (234.8, "مريخ", "د")],
    "Virgo": [(242.3, "عطارد", "ز"), (247.6, "زهرة", "ه"), (253.9, "مشتري", "و"), (260.1, "مريخ", "و"), (265.6, "زحل", "ه")],
    "Libra": [(273.2, "زحل", "و"), (278.6, "زهرة", "ه"), (284.2, "مشتري", "ح"), (290.0, "عطارد", "و"), (296.0, "مريخ", "ه")],
    "Scorpio": [(303.0, "مريخ", "و"), (308.5, "مشتري", "ح"), (314.6, "زهرة", "ز"), (320.4, "عطارد", "ز"), (326.3, "زحل", "و")],
    "Sagittarius": [(332.4, "مشتري", "ح"), (337.1, "زهرة", "و"), (342.3, "عطارد", "ه"), (348.5, "زحل", "و"), (354.2, "مريخ", "ه")],
    "Capricorn": [(2.6, "زهرة", "و"), (8.3, "عطارد", "ح"), (14.4, "مشتري", "ز"), (20.5, "مريخ", "ج"), (26.3, "زحل", "و")],
    "Aquarius": [(32.0, "زحل", "و"), (36.6, "عطارد", "و"), (41.9, "زهرة", "ح"), (47.3, "مشتري", "ه"), (53.1, "مريخ", "ه")],
    "Pisces": [(62.1, "زهرة", "ح"), (66.8, "مشتري", "و"), (72.0, "عطارد", "ز"), (77.7, "مريخ", "ه"), (84.1, "زحل", "د")],
}
TERM_DOUBT = {
    ("Aries", 2): "a speck above the ح in the master only; not a dot",
    ("Leo", 4): "the dot of the ز stands well above the stroke (both copies)",
}

# Rings 4 (outer, by day) and 3 (inner, by night): the three lords of each sign, in reading order.
TRIPLICITIES = {
    "Aries": ("شمس مشتري زحل", "مشتري شمس زحل"),
    "Taurus": ("زهرة قمر مريخ", "قمر زهرة مريخ"),
    "Gemini": ("زحل عطارد مشتري", "عطارد زحل مشتري"),
    "Cancer": ("زهرة مريخ قمر", "مريخ زهرة قمر"),
    "Leo": ("شمس مشتري زحل", "مشتري شمس زحل"),
    "Virgo": ("زهرة قمر مريخ", "قمر زهرة مريخ"),
    "Libra": ("زحل عطارد مشتري", "عطارد زحل مشتري"),
    "Scorpio": ("زهرة مريخ قمر", "مريخ زهرة قمر"),
    "Sagittarius": ("شمس مشتري زحل", "مشتري شمس زحل"),
    "Capricorn": ("زهرة قمر مريخ", "قمر زهرة مريخ"),
    "Aquarius": ("زحل عطارد مشتري", "عطارد زحل مشتري"),
    "Pisces": ("زهرة مريخ قمر", "مريخ زهرة قمر"),
}

# Ring 2, the faces: three (angle, planet) per sign from the beginning of the sign.
FACES = {
    "Aries": [(93.6, "مريخ"), (104.8, "شمس"), (113.0, "زهرة")],
    "Taurus": [(123.9, "عطارد"), (134.6, "قمر"), (143.3, "زحل")],
    "Gemini": [(154.1, "مشتري"), (163.8, "مريخ"), (173.7, "شمس")],
    "Cancer": [(183.8, "زهرة"), (193.6, "عطارد"), (204.2, "قمر")],
    "Leo": [(213.6, "زحل"), (223.6, "مشتري"), (232.9, "مريخ")],
    "Virgo": [(244.9, "شمس"), (253.2, "زهرة"), (262.9, "عطارد")],
    "Libra": [(276.3, "قمر"), (287.9, "زحل"), (294.7, "مشترب")],
    "Scorpio": [(305.6, "مريخ"), (315.5, "شمس"), (323.2, "زهرة")],
    "Sagittarius": [(335.4, "عطارد"), (344.4, "قمر"), (352.7, "زحل")],
    "Capricorn": [(4.0, "مشتري"), (13.5, "مريخ"), (22.6, "شمس")],
    "Aquarius": [(34.8, "زهرة"), (44.6, "عطارد"), (54.1, "قمر")],
    "Pisces": [(64.3, "زحل"), (74.0, "مشتري"), (83.1, "مريخ")],
}
FACE_DOUBT = {
    ("Libra", 3): "one dot under the final bowl in both copies (a speck beside it in the master): printed مشترب for مشتري",
    ("Leo", 3): "the two dots of the ي are merged into a short stroke (both copies)",
}

# Ring 1, houses and exaltations merged: the cell as printed (lines from the outside, « / »), then the house, the
# planet of the exaltation and its degrees.
RING1 = {
    "Aries": ("بهرام / شمس ىط", "بهرام", "شمس", "ىط"),
    "Taurus": ("زهرة / ج / قمر", "زهرة", "قمر", "ج"),
    "Gemini": ("عطارد / ج / رأس", "عطارد", "رأس", "ج"),
    "Cancer": ("قمر يد / مشتري", "قمر", "مشتري", "يد"),
    "Leo": ("شمس / {0}", "شمس", "", "{0}"),
    "Virgo": ("عطارد / يه / عطارد", "عطارد", "عطارد", "يه"),
    "Libra": ("زهرة / كا / زحل", "زهرة", "زحل", "كا"),
    "Scorpio": ("مريخ / {0}", "مريخ", "", "{0}"),
    "Sagittarius": ("مشتري / ج / ذنب", "مشتري", "ذنب", "ج"),
    "Capricorn": ("زحل كح / مريخ", "زحل", "مريخ", "كح"),
    "Aquarius": ("زحل / {0}", "زحل", "", "{0}"),
    "Pisces": ("مشتري / زهرة كز", "مشتري", "زهرة", "كز"),
}
RING1_DOUBT = {
    "Aries": "بهرام, the Persian name of Mars (Nallino, Part II p. 308, n. 2); the degrees ىط have a dotless tooth (both copies)",
    "Gemini": "رأس with a hamza over the alif",
    "Leo": "no exaltation: the codex's zero sign (a bar with a ring below)",
    "Scorpio": "no exaltation: the zero sign",
    "Aquarius": "no exaltation: the zero sign",
}

# The sign names outside the outer circle: measured angle, text (along the circle, tops outward).
SIGN_LABELS = [(102.6, "حمل"), (133.6, "ثور"), (162.2, "جوزاه"), (193.2, "سرطان"), (221.4, "اسد"), (252.3, "سنبلة"),
               (285.1, "ميزان"), (310.6, "عقرب"), (342.1, "قوس"), (12.9, "جدي"), (41.8, "دلو"), (72.3, "حوت")]
SIGN_DOUBT = {"جوزاه": "the last letter is a closed loop (ه), as الجوزاه on p. 243"}

HEADER = {"page": "244", "fol": "Fol. 197,r."}
TITLE = ("وهذه الدائرة حَوَتْ على ارباب حُدود البروج الاثنَيْ عَشَرَ وارباب مُثَلَّثاتها في النهار والليل{fn1} "
         "وارباب الوُجوه وارباب البُيُوت{fn2} وارباب الأشراف إن شاء اللّٰه.")
TITLE_DOUBT = ("الاثنَيْ: a fatha over the ن and a sukun over the ي, the ث without a mark; الأشراف: a bare hamza "
               "(2.9 pt high); اللّٰه: shadda and a vertical alif over the lam; the footnote mark 2 follows البيوت")
CLOSING = ("الدائرة الأُولَى للحُدُود والتي تَلِيها للمُثلَّثات والتي تليهما للوُجُوه والتي تليها بعد الثلٰثة "
           "للبيوت{fn3} والتي تليها كلَّها وهي داخِلَها للأشْراف{fn4} وليْسَتْ من الأُمّ.")
CLOSING_DOUBT = ("الأُولى and الأُمّ: hamza and ḍamma touching (6.3-6.5 pt high); الثلٰثة: a vertical alif over the "
                 "lam; للمُثلَّثات: no fatha over the ث here (the title has one)")
FOOTNOTES = [("1", "Cod. في الليل والنهار"), ("2", "Cod. البروج"), ("3", "Cod. للشرف"),
             ("4", "Cod. للبيوت. Codicis errores etiam in circulorum descriptione servavi.")]

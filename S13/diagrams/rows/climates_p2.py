"""Part II p. 92 (master PDF 541): Nallino's Latin version of the diagram of the seven climes, as printed.
Read 2026-10-05 at 330-500 dpi (one copy; the Internet Archive copy covers Part III only).

Angles t as in climates_p3.py: degrees counterclockwise from the right-hand horizontal of the page; south at the top
(t = 90), east (sunrise) on the left (t = 180). The figure repeats the same three columns of values in every
quadrant."""

PISCES = ["12°|3′", "12°|39′", "13°|27′", "14°|23′", "15°|26′", "16°|33′", "17°|43′"]
AQUARIUS = ["21°|11′", "22°|18′", "23°|45′", "25°|29′", "27°|26′", "29°|33′", "31°|46′"]
CAPRICORN = ["24°|41′", "26°|0′", "27°|42′", "29°|48′", "32°|8′", "34°|43′", "37°|28′"]
CELLS = {22.5: PISCES, 157.5: PISCES, 202.5: PISCES, 337.5: PISCES,
         45: AQUARIUS, 135: AQUARIUS, 225: AQUARIUS, 315: AQUARIUS,
         67.5: CAPRICORN, 112.5: CAPRICORN, 247.5: CAPRICORN, 292.5: CAPRICORN}

AXES = {
    0: [("0", "0")] * 7,
    180: [("0", "0")] * 7,
    # top: counterclockwise (left) side the clime, clockwise (right) side «clima» or the latitude
    90: [("I", "clima"), ("2", "25"), ("3", "30"), ("IV", "clima"), ("5", "41"), ("6", "45"), ("VII", "clima")],
    # bottom: counterclockwise (right) side the hours, clockwise (left) side «horae eius»
    270: [("13h", "horae / eius"), ("13h / 30m", "horae / eius"), ("14h", "horae / eius"), ("14h / 30m", "horae / eius"),
          ("15h", "horae / eius"), ("15h / 30m", "horae / eius"), ("16h", "horae / eius")],
}

# Labels outside the figure: line angle, text (« / » = line break), placement.
LABELS = [
    ("azimuth", 90, "Azimuth / meridiei, 90°.", "set along the vertical axis above the figure, rotated"),
    ("azimuth", 270, "Azimuth / septentrionis, 90°", "set along the vertical axis below the figure, rotated"),
    ("side", 180, "[Solis ortus aequinoctialis.]", "bold, set vertically at the left edge; Nallino's brackets"),
    ("side", 0, "[Solis occasus aequinoctialis.]", "bold, set vertically at the right edge; Nallino's brackets"),
    ("sign", 0, "Libra / Aries", ""),
    ("sign", 22.5, "Scorpio / Pisces", ""),
    ("sign", 45, "Sagittarius / Aquarius", ""),
    ("sign", 67.5, "Capricornus", ""),
    ("sign", 112.5, "Capricornus", ""),
    ("sign", 135, "Aquarius / Sagittarius", ""),
    ("sign", 157.5, "Pisces / Scorpio", ""),
    ("sign", 180, "Aries / Libra", ""),
    ("sign", 202.5, "Taurus / Virgo", ""),
    ("sign", 225, "Gemini / Leo", ""),
    ("sign", 247.5, "Cancer", ""),
    ("sign", 292.5, "Cancer", ""),
    ("sign", 315, "Leo / Gemini", ""),
    ("sign", 337.5, "Virgo / Taurus", ""),
]

WINDS = {0: "Zephyrus", 22.5: "Lips", 45: "Libonotus", 67.5: "Leuconotus ?", 90: "Notus", 112.5: "Euronotus",
         135: "Phoenicias ?", 157.5: "Eurus", 180: "Apeliotes", 202.5: "Thebanas", 225: "Boreas",
         247.5: "Aparctias ?", 270: "Ornithias ?", 292.5: "Cercias ?", 315: "Thrascias", 337.5: "Iapyx"}

CORNERS = {
    "TL": ["Solis ortus hiemalis.", "Euronotus."],
    "TR": ["Occasus hiemalis.", "Carbas [?]."],
    "BL": ["Solis ortus aestivus.", "Ornithias [?]"],
    "BR": ["Occasus aestivus.", "Argestes [?]"],
}

TITLE = [
    "Circuli septem climatum, cum circulis horizontum concentrici,",
    "item gradus azimuth ascensionum et occasuum signorum in singulis climatibus,",
    "i. e. eorum elongationes ab ortu et occasu aequinoctiali",
    "versus septentriones et austrum.",
]
HEADER = {"page": "92", "head": "C. A. NALLINO", "fol": "f. 196,v."}

# Nallino's table of the wind names (Part II p. 234, «Ad pag. 92»): azimuth in the figure (from south through
# east), direction, the name in the Almagest, the name in the codex, Nallino's probable restoration (Arabic, Greek).
NAMES_TABLE = [
    ("0", "S", "νότος", "ىوطس", "نوطس νότος"),
    ("22 1/2", "SSE", "ortus hiemalis", "بوبوطس", "اورونوطس εὐρόνοτος (= φοινικίας)"),
    ("45", "SE", "εὐρόνοτος", "هوىعس", "فونقيس φοινικίας"),
    ("67 1/2", "ESE", "εὖρος", "صدوس", "اوروس εὖρος"),
    ("90", "E", "ἀπηλιώτης", "اڡلىطس", "افليوطس ἀπηλιώτης"),
    ("112 1/2", "ENE", "καικίας", "سعاىس", "ثيبانس θηβάνας (= καικίας)"),
    ("135", "NE", "βορέας", "بورىوٮ", "بورياس βορέας"),
    ("157 1/2", "NNE", "ortus aestivus", "افر...ىطس", "افرقطيس ἀπαρκτίας (= ὀρνιθίας)"),
    ("180", "N", "ἀπαρκτίας", "بعدىاس", "ارنثياس ὀρνιθίας"),
    ("202 1/2", "NNW", "occasus aestivus", "افريقس", "قرقيس κερκίας (= θρασκίας)"),
    ("225", "NW", "θρασκίας", "برقسىس", "ثرسقيس θρασκίας"),
    ("247 1/2", "WNW", "ἰάπυξ", "اىاقونس", "يافوقس ἰάπυξ"),
    ("270", "W", "ζέφυρος", "رهڡرس", "زهفرس ζέφυρος"),
    ("292 1/2", "WSW", "λίψ", "لعوس", "ليبوس λίψ (ex genit. λιβός)"),
    ("315", "SW", "λιβόνοτος", "ليبونطس", "ليبونطس λιβόνοτος"),
    ("337 1/2", "SSW", "occasus hiemalis", "بونطس", "لوقونطس λευκόνοτος (= λιβόνοτος)."),
]

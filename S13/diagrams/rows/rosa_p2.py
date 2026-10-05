"""Part II p. 299 (master PDF 748): Nallino's Latin version of the astrological figure, as printed. Read 2026-10-05 at
450-1800 dpi (one copy; the Internet Archive copy covers Part III only).

Geometry (master pt): centre (267.0, 457.0); circles at 40.5, 56.0, 71.5, 109.0, 147.0, 193.5, and a dashed circle
inside the triplicity ring. Sector lines at 30k degrees, counterclockwise from the right-hand horizontal; Aries at
90-120 as in the codex figure. Rings from the inside: exaltations, houses, faces, triplicities (outer half by day,
inner half by night, as Nallino says on p. 310), terms. Terms and faces are written along the radius from the outer
end, the tops of the letters toward the clockwise side; everything else is written along the circles, tops outward.
The planets of the triplicities and exaltations are printed as symbols; Nallino gives the key on p. 309."""

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn",
         "Aquarius", "Pisces"]
RADII = [40.5, 56.0, 71.5, 109.0, 147.0, 193.5]
DASHED = 128.0

TERMS = {
    "Aries": [(94.5, "Iupiter", "6°"), (99.4, "Venus", "8°"), (104.5, "Mercurius", "7°"), (109.6, "Mars", "5°"), (114.8, "Saturnus", "4°")],
    "Taurus": [(124.5, "Venus", "8°"), (129.4, "Mercurius", "7°"), (134.2, "Iupiter", "7°"), (139.1, "Saturnus", "4°"), (144.3, "Mars", "4°")],
    "Gemini": [(154.2, "Mercurius", "7°"), (160.0, "Iupiter", "7°"), (164.4, "Venus", "7°"), (169.0, "Mars", "5°"), (174.2, "Saturnus", "4°")],
    "Cancer": [(184.2, "Mars", "6°"), (189.3, "Iupiter", "7°"), (194.3, "Venus", "7°"), (199.7, "Mercurius", "7°"), (204.9, "Saturnus", "3°")],
    "Leo": [(214.4, "Mercurius", "7°"), (219.7, "Venus", "6°"), (224.8, "Iupiter", "6°"), (229.7, "Saturnus", "6°"), (235.1, "Mars", "5°")],
    "Virgo": [(244.4, "Mercurius", "7°"), (249.7, "Verus", "6°"), (254.8, "Iupiter", "5°"), (259.3, "Mars", "6°"), (264.7, "Saturnus", "6°")],
    "Libra": [(274.0, "Saturnus", "6°"), (279.2, "Venus", "5°"), (284.9, "Iupiter", "8°"), (289.5, "Mercurius", "5°"), (294.4, "Mars", "6°")],
    "Scorpio": [(303.9, "Mars", "6°"), (309.0, "Iupiter", "8°"), (314.4, "Venus", "7°"), (319.4, "Mercurius", "6°"), (324.9, "Saturnus", "3°")],
    "Sagittarius": [(333.7, "Iupiter", "8°"), (339.0, "Venus", "6°"), (344.2, "Mercurius", "5°"), (349.1, "Saturnus", "6°"), (354.6, "Mars", "5°")],
    "Capricorn": [(4.0, "Venus", "6°"), (9.6, "Mercurius", "6°"), (14.5, "Iupiter", "7°"), (19.4, "Mars", "6°"), (24.9, "Saturnus", "5°")],
    "Aquarius": [(33.7, "Saturnus", "6°"), (39.1, "Mercurius", "6°"), (44.5, "Venus", "8°"), (49.5, "Iupiter", "5°"), (54.5, "Mars", "5°")],
    "Pisces": [(63.9, "Venns", "8°"), (69.4, "Iupiter", "6°"), (74.0, "Mercurius", "6°"), (78.9, "Mars", "6°"), (84.5, "Saturnus", "4°")],
}
TERM_DOUBT = {
    ("Virgo", 2): "printed Verus (an r for the n)",
    ("Pisces", 1): "printed Venns (a turned n for the u)",
    ("Capricorn", 2): "the u of Mercurius is broken in print",
}

TRIPLICITIES = {                                    # (by day, outer; by night, inner), symbols in reading order
    "Aries": ("☉ ♃ ♄", "♃ ☉ ♄"), "Taurus": ("♀ ☽ ♂", "☽ ♀ ♂"), "Gemini": ("♄ ☿ ♃", "☿ ♄ ♃"),
    "Cancer": ("♀ ♂ ☽", "♂ ♀ ☽"), "Leo": ("☉ ♃ ♄", "♃ ☉ ♄"), "Virgo": ("♀ ☽ ♂", "☽ ♀ ♂"),
    "Libra": ("♄ ☿ ♃", "☿ ♄ ♃"), "Scorpio": ("♀ ♂ ☽", "♂ ♀ ☽"), "Sagittarius": ("☉ ♃ ♄", "♃ ☉ ♄"),
    "Capricorn": ("♀ ☽ ♂", "☽ ♀ ♂"), "Aquarius": ("♄ ☿ ♃", "☿ ♄ ♃"), "Pisces": ("♀ ♂ ☽", "♂ ♀ ☽"),
}

FACES = {
    "Aries": [(97.4, "Mars"), (103.2, "Sol"), (111.9, "Venus")],
    "Taurus": [(126.2, "Mercurius"), (133.9, "Luna"), (141.7, "Saturnus")],
    "Gemini": [(157.0, "Iupiter"), (164.6, "Mars"), (172.2, "Sol")],
    "Cancer": [(186.8, "Venus"), (194.2, "Mercurius"), (203.7, "Luna")],
    "Leo": [(217.7, "Saturnus"), (225.6, "Iupiter"), (232.6, "Mars")],
    "Virgo": [(248.1, "Sol"), (253.8, "Venus"), (262.7, "Mercurius")],
    "Libra": [(276.3, "Luna"), (283.0, "Saturnus"), (292.5, "Iupiter")],
    "Scorpio": [(306.7, "Mars"), (314.6, "Sol"), (321.2, "Venus")],
    "Sagittarius": [(335.9, "Mercurius"), (344.5, "Luna"), (350.2, "Saturnus")],
    "Capricorn": [(6.8, "Iupiter"), (14.6, "Mars"), (22.2, "Sol")],
    "Aquarius": [(35.9, "Venus"), (43.7, "Mercurius"), (52.5, "Luna")],
    "Pisces": [(66.8, "Saturnus"), (74.4, "Iupiter"), (82.5, "Mars")],
}
FACE_DOUBT = {("Taurus", 3): "the t and n of Saturnus are broken in print"}

HOUSES = {"Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercurius", "Cancer": "Luna", "Leo": "Sol",
          "Virgo": "Mercurius", "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Iupiter", "Capricorn": "Saturnus",
          "Aquarius": "Saturnus", "Pisces": "Iupiter"}
EXALTATIONS = {"Aries": ("☉", "19°"), "Taurus": ("☽", "3°"), "Gemini": ("☊", "3°"), "Cancer": ("♃", "15°"),
               "Leo": ("", "0°"), "Virgo": ("☿", "15°"), "Libra": ("♄", "21°"), "Scorpio": ("", "0°"),
               "Sagittarius": ("☋", "3°"), "Capricorn": ("♂", "28°"), "Aquarius": ("", "0°"), "Pisces": ("♀", "27°")}
EXALT_DOUBT = {"Capricorn": "the degree sign after 28 is not visible"}

SIGN_LABELS = [(105, "Aries"), (135, "Taurus"), (165, "Gemini"), (195, "Cancer"), (225, "Leo"), (255, "Virgo"),
               (285, "Libra"), (315, "Scorpius"), (345, "Sagittarius"), (15, "Capricornus"), (45, "Aquarius"),
               (75, "Pisces")]

HEADER = {"page": "", "fol": "Fol. 197,r."}
HEADER_DOUBT = ("no page number is printed (a double rule heads the page); Nallino cites the figure as p. 299 "
                "(Part II p. 308)")
TITLE = ("Circulus hic complectitur dominos terminorum duodecim signorum, dominos eorum triplicitatum die et nocte (1), "
         "dominos facierum (2), dominos domiciliorum, et dominos exaltationum, si Deus vult.")
CLOSING = ("Primus circulus *terminis* [inservit]; qui eum sequitur *triplicitatibus*; qui ambos sequitur *faciebus*; "
           "qui tres illos sequitur *domiciliis* (3); qui omnes eos sequitur, ac intimus est, *exaltationibus* (4). "
           "Nec est [imago haec] ex archetypo.")
FOOTNOTES = [("1", "Cod. « nocte et die »."), ("2", "Cod. « signorum »."), ("3", "Cod. « exaltationi »."),
             ("4", "Cod. « domiciliis ». Emendationes figurae illatas in commentario recensebo.")]

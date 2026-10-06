"""Write the data of Nallino's Part II pp. 95-101 (the parallaxes of the Moon in longitude and latitude in the seven
climes) to S06/parallax/:
  clime_p2.tsv      one row per printed row: page, folio, sign, row, the hour from culmination as printed (the
                    half-day arc in the first and last rows), the parallax in longitude and in latitude (minutes), «+»
                    where the latitude is northern, the mark «bor.» or «austr.» printed over the value, the class of
                    each number (A both readers, M one reader and the mirror table, E by eye), notes
  clime_pages.tsv   folio lines, titles and heads
Values come from clime_resolve.py (p3_kit/CLR.json); every value resolved with the help of the mirror table was also
read by eye (CLM sheets)."""
import csv, json, os, re
import fitz
import wide_kit as wk
import clime_pages as cp
import clime_resolve as cr

AB = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani"
OUT = os.path.join(AB, "S06", "parallax")
PP = {544: "95", 545: "96", 546: "97", 547: "98", 548: "99", 549: "100", 550: "101"}
FOL = {544: ("f. 198,v.", "f. 199,r."), 545: ("f. 199,v.", "f. 200,r."), 546: ("f. 200,v.", "f. 201,r."),
       547: ("f. 201,v.", "f. 202,r."), 548: ("f. 202,v.", "f. 203,r."), 549: ("f. 203,v.", "f. 204,r."),
       550: ("f. 204,v.", "f. 205,r.")}
# half-day arcs as printed: Cancer, Leo (= Gemini), Virgo (= Taurus), Scorpio (= Pisces), Sagittarius (= Aquarius),
# Capricorn; Libra and Aries 6h
HALF = {544: [(6, 30), (6, 25), (6, 15), (5, 45), (5, 35), (5, 30)], 545: [(6, 45), (6, 38), (6, 21), (5, 39), (5, 22), (5, 15)],
        546: [(7, 0), (6, 51), (6, 28), (5, 32), (5, 9), (5, 0)], 547: [(7, 15), (7, 4), (6, 35), (5, 25), (4, 56), (4, 45)],
        548: [(7, 30), (7, 16), (6, 42), (5, 18), (4, 45), (4, 30)], 549: [(7, 45), (7, 28), (6, 48), (5, 12), (4, 32), (4, 15)],
        550: [(8, 0), (7, 40), (6, 54), (5, 6), (4, 20), (4, 0)]}
WHICH = {"Cancer": 0, "Leo": 1, "Gemini": 1, "Virgo": 2, "Taurus": 2, "Scorpio": 3, "Pisces": 3, "Sagittarius": 4,
         "Aquarius": 4, "Capricorn": 5}
DOUBT = {}


def half_day(pdf, sign):
    return (6, 0) if sign in ("Libra", "Aries") else HALF[pdf][WHICH[sign]]


def hours(pdf, sign, n):
    h, m = half_day(pdf, sign)
    before = h + (1 if m else 0)
    assert n == 2 * before + 1, (pdf, sign, n, h, m)
    first = f"{h}ʰ {m}′" if m else f"{h}ʰ"
    last = first if m else str(h)
    labels = [first] + [str(k) for k in range(before - 1, 0, -1)] + ["culm."] + [str(k) for k in range(1, before)] + [last]
    return labels


data, res, eye = cr.resolve()
assert not eye
# the marks «bor.» / «austr.» from the text layer: the first data row below each mark, in its column
marks = {}
for pdf in PP:
    page = wk.doc[pdf - 1]
    words = [w for w in page.get_text("words") if re.match(r"^(bor|austr)", w[4])]
    for w in words:
        xc, yb = (w[0] + w[2]) / 2, w[3]
        for (p, sign), s in data.items():
            if p != pdf or not (s["rules"][1] <= xc <= s["rules"][2]):
                continue
            below = [(r["y"] - yb, i) for i, r in enumerate(s["rows"]) if 0 < r["y"] - yb < 14]
            if below:
                marks[(pdf, sign, min(below)[1])] = "bor." if w[4].startswith("bor") else "austr."

rows = []
for (pdf, sign), s in data.items():
    n = len(s["rows"])
    labels = hours(pdf, sign, n)
    prev = None
    for i in range(n):
        v = res[(pdf, sign, i)]
        north = bool(v["north"]) and v["lat"] != "0"
        side = "N" if north else "S"
        rule_mark = ("bor." if north else "austr.") if (i == 0 or side != prev) else ""
        prev = side
        mark = marks.get((pdf, sign, i), "")
        rows.append({"pdf": pdf, "ppage": PP[pdf], "fol": FOL[pdf][0 if s["half"] == "top" else 1], "sign": sign, "row": i + 1,
                     "hour": labels[i], "long": v["long"], "lat": v["lat"], "north": "+" if north else "", "mark": mark,
                     "check": v["cls"], "doubt": DOUBT.get((pdf, sign, i), ""), "_rule": rule_mark})
# every mark stands over the first row and wherever the direction changes; the text layer finds all but three, which
# were read by eye
MARK_EYE = {(544, "Leo", 3): "bor.", (549, "Sagittarius", 1): "austr.", (550, "Leo", 1): "austr."}
for r in rows:
    found = r["mark"] or MARK_EYE.get((r["pdf"], r["sign"], r["row"]), "")
    assert found == r["_rule"], (r["pdf"], r["sign"], r["row"], found, r["_rule"])
    r["mark"] = found
print("marks", sum(1 for r in rows if r["mark"]), "(3 read by eye)")
order = {s: k for k, s in enumerate(cp.SIGNS["top"] + cp.SIGNS["bot"])}
rows.sort(key=lambda r: (r["pdf"], order[r["sign"]], r["row"]))
# the line of each row in the grid of its half (the lines of the longest column), and the lines after a wider space
GRID, GAPS = {}, {}
for pdf in PP:
    for half in ("top", "bot"):
        cols = [(len(s["rows"]), s) for (p, sign), s in data.items() if p == pdf and s["half"] == half]
        ref = max(cols, key=lambda t: t[0])[1]
        ys = [r["y"] for r in ref["rows"]]
        GRID[(pdf, half)] = ys
        step = sorted(b - a for a, b in zip(ys, ys[1:]))[len(ys) // 3]
        GAPS[(pdf, half)] = [k + 1 for k in range(1, len(ys)) if ys[k] - ys[k - 1] > step * 1.3]
for r in rows:
    s = data[(r["pdf"], r["sign"])]
    ys = GRID[(r["pdf"], s["half"])]
    y = s["rows"][r["row"] - 1]["y"]
    line = min(range(len(ys)), key=lambda k: abs(ys[k] - y))
    assert abs(ys[line] - y) < 4, (r["pdf"], r["sign"], r["row"], y)
    r["line"] = line + 1
fields = ["pdf", "ppage", "fol", "sign", "row", "line", "hour", "long", "lat", "north", "mark", "check", "doubt"]
with open(os.path.join(OUT, "clime_p2.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n", extrasaction="ignore")
    w.writeheader(); w.writerows(rows)
print(len(rows), "rows")

ORD = ["primo", "secundo", "tertio", "quarto", "quinto", "sexto", "septimo"]
AR_ORD = ["الاول", "الثاني", "الثالث", "الرابع", "الخامس", "السادس", "السابع"]
LAT = {544: ("يو لب", "16° 32′", "يج", "13ʰ"), 545: ("كد", "24°", "يج ل", "13ʰ 30ᵐ"), 546: ("ل م", "30° 40′", "يد", "14ʰ"),
       547: ("لو كب", "36° 22′", "يد ل", "14ʰ 30ᵐ"), 548: ("ما يه", "41° 15′", "يه", "15ʰ"), 549: ("مه كب", "45° 22′", "يه ل", "15ʰ 30ᵐ"),
       550: ("مح يج", "48° 13′", "يو", "16ʰ")}
HOURS_AR = {"Cancer": "ساعات السرطان", "Leo": "ساعات الاسد", "Virgo": "ساعات السنبلة", "Libra": "ساعات الميزان",
            "Scorpio": "ساعات العقرب", "Sagittarius": "ساعات القوس", "Capricorn": "ساعات الجدي", "Aquarius": "ساعات الدلو",
            "Pisces": "ساعات الحوت", "Aries": "ساعات الحمل", "Taurus": "ساعات الثور", "Gemini": "ساعات الجوزاء"}
HOURS_LA = {"Cancer": "Horae Cancri.", "Leo": "Horae Leonis.", "Virgo": "Horae Virginis.", "Libra": "Horae Librae.",
            "Scorpio": "Horae Scorpii.", "Sagittarius": "Horae Sagittarii.", "Capricorn": "Horae Capricorni.",
            "Aquarius": "Horae Aquarii.", "Pisces": "Horae Piscium.", "Aries": "Horae Arietis.", "Taurus": "Horae Tauri.",
            "Gemini": "Hor. Geminorum."}
pages = []
for k, pdf in enumerate(sorted(PP)):
    ar_lat, la_lat, ar_h, la_h = LAT[pdf]
    title_ar = (f"جداول اختلاف منظر القمر في الاقليم {AR_ORD[k]} وعرضه {ar_lat} وساعاته {ar_h}" if pdf == 544 else
                f"جداول اختلاف منظر القمر في الطول والعرض للاقليم {AR_ORD[k]} وعرضه {ar_lat} وساعاته {ar_h}")
    tab = "Tabula" if pdf in (547, 548) else "Tabulae"
    title_la = (f"{tab} parallaxium Lunae in longitudine et latitudine, in {ORD[k]} climate / cuius latitudo {la_lat} et "
                f"horae {la_h}.")
    for half in ("top", "bot"):
        signs = cp.SIGNS[half]
        heads = []
        for j, sign in enumerate(signs):
            la = HOURS_LA[sign] if not (pdf == 544 and sign == "Gemini") else "Horae Geminorum."
            ar = HOURS_AR[sign] if pdf == 544 else ""
            heads.append(ar + "‖" + la)
            par_ar = "اختلاف / منظر القمر" if (pdf == 544 and half == "top" and j == 0) else ""
            heads.append(par_ar + "‖Parallaxis / Lunae.")
        pages.append({"pdf": pdf, "ppage": PP[pdf], "half": half, "fol": FOL[pdf][0 if half == "top" else 1],
                      "title_ar": title_ar if half == "top" else "", "title_la": title_la if half == "top" else "",
                      "heads": "|".join(heads), "lines": len(GRID[(pdf, half)]),
                      "space_before": " ".join(str(k) for k in GAPS[(pdf, half)]),
                      "signature": "13" if (pdf == 546 and half == "bot") else ""})
with open(os.path.join(OUT, "clime_pages.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pdf", "ppage", "half", "fol", "title_ar", "title_la", "heads", "lines", "space_before",
                                      "signature"], delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(pages)

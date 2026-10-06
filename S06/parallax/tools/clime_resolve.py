"""Resolve the readings of Part II pp. 95-101 (CL{pdf}{half}.json from clime_pages.py).
Each row of a sign holds the parallax in longitude and in latitude (minutes); a «+» marks a northern latitude. A value
is taken where the glyph reader (its «+» removed) and the text layer give the same digits and the two «+» tests agree
(class A); the table of the mirror sign (Leo-Gemini, Virgo-Taurus, Libra-Aries, Scorpio-Pisces, Sagittarius-Aquarius;
Cancer and Capricorn with themselves), read backwards in time, prints the same values and decides between two readings
(class M); everything else goes to a sheet for reading by eye (EYE in this file, class E).
Output: p3_kit/CLR.json {key: {"long", "lat", "north", "cls"}} and sheets CLE_{k}.png."""
import json, os
import fitz
from PIL import Image, ImageDraw, ImageFont
import wide_kit as wk

PDFS = list(range(544, 551))
MIRROR = {"Leo": "Gemini", "Gemini": "Leo", "Virgo": "Taurus", "Taurus": "Virgo", "Libra": "Aries", "Aries": "Libra",
          "Scorpio": "Pisces", "Pisces": "Scorpio", "Sagittarius": "Aquarius", "Aquarius": "Sagittarius",
          "Cancer": "Cancer", "Capricorn": "Capricorn"}
EYE = {      # (pdf, sign, row index): (long, lat, north), read by eye on CLE_0.png
    (544, "Virgo", 0): ("51", "4", True), (544, "Virgo", 4): ("34", "6", True), (544, "Virgo", 11): ("36", "24", False),
    (544, "Scorpio", 1): ("49", "4", True), (544, "Pisces", 11): ("49", "4", True), (544, "Aries", 10): ("45", "4", True),
    (544, "Taurus", 3): ("36", "24", False), (544, "Taurus", 10): ("34", "6", True), (544, "Taurus", 14): ("51", "4", True),
    (545, "Libra", 0): ("51", "0", False), (545, "Aries", 12): ("51", "0", False), (546, "Cancer", 9): ("21", "8", False),
    (546, "Sagittarius", 8): ("14", "42", False), (546, "Aquarius", 4): ("14", "42", False),
    (547, "Libra", 2): ("45", "13", False), (547, "Capricorn", 5): ("0", "44", False), (547, "Aries", 1): ("25", "44", False),
    (547, "Aries", 10): ("45", "13", False), (548, "Leo", 1): ("44", "26", False), (548, "Virgo", 10): ("16", "36", False),
    (548, "Capricorn", 5): ("0", "46", False), (548, "Taurus", 4): ("16", "36", False), (548, "Gemini", 15): ("44", "26", False),
    (549, "Leo", 15): ("26", "44", False), (549, "Sagittarius", 6): ("1", "46", False), (549, "Capricorn", 5): ("0", "48", False),
    (549, "Aquarius", 4): ("1", "46", False), (549, "Taurus", 2): ("20", "44", False), (549, "Gemini", 1): ("26", "44", False),
    (550, "Cancer", 0): ("30", "42", False), (550, "Capricorn", 4): ("0", "49", False)}


def load():
    data = {}
    for pdf in PDFS:
        for half in ("top", "bot"):
            d = json.load(open(wk.OUT + f"CL{pdf}{half}.json", encoding="utf-8"))
            for s in d["signs"]:
                data[(pdf, s["sign"])] = {"half": half, "rules": s["rules"], "rows": s["rows"]}
    return data


def digits(t):
    return "".join(ch for ch in (t or "") if ch.isdigit())


def readings(row):
    lo, la = row["long"], row["lat"]
    north_tl, north_img = row["plus_tl"], row["plus_img"]
    g_lat = digits(la["text"])
    if (north_tl or north_img) and len(g_lat) >= 2:
        g_lat = g_lat[1:]                                     # the «+» read as a digit
    return {"long_g": digits(lo["text"]), "long_t": digits(lo.get("tl")), "conf_long": lo["conf"],
            "lat_g": g_lat, "lat_t": digits(la.get("tl")), "north_tl": north_tl, "north_img": north_img}


def first_pass(data):
    out = {}
    for (pdf, sign), s in data.items():
        for i, row in enumerate(s["rows"]):
            r = readings(row)
            lon = r["long_g"] if r["long_g"] == r["long_t"] and r["long_g"] else None
            lat = r["lat_g"] if r["lat_g"] == r["lat_t"] and r["lat_g"] else None
            north = r["north_tl"] if r["north_tl"] == r["north_img"] else None
            out[(pdf, sign, i)] = {"long": lon, "lat": lat, "north": north, "r": r}
    return out


def resolve():
    data = load()
    fp = first_pass(data)
    res, eye = {}, []
    for (pdf, sign, i), v in fp.items():
        n = len(data[(pdf, sign)]["rows"])
        m = (pdf, MIRROR[sign], n - 1 - i)
        mv = fp.get(m)
        if (pdf, sign, i) in EYE:
            lo, la, no = EYE[(pdf, sign, i)]
            res[(pdf, sign, i)] = {"long": lo, "lat": la, "north": no, "cls": "E"}
            continue
        rec, cls = {}, ""
        for f, cands in (("long", [v["r"]["long_g"], v["r"]["long_t"]]), ("lat", [v["r"]["lat_g"], v["r"]["lat_t"]])):
            if v[f] is not None:
                rec[f], c = v[f], "A"
            elif mv and mv[f] is not None and mv[f] in cands:
                rec[f], c = mv[f], "M"
            else:
                rec[f], c = None, "C"
            cls += c
        if v["north"] is not None:
            rec["north"], c = v["north"], "A"
        elif mv and mv["north"] is not None:
            rec["north"], c = mv["north"], "M"
        else:
            rec["north"], c = None, "C"
        rec["cls"] = cls + c
        if rec["lat"] == "0":
            rec["north"] = False
        # the mirror must agree with an agreed value
        if mv and all(mv[f] is not None for f in ("long", "lat")) and rec["long"] is not None and rec["lat"] is not None:
            if (mv["long"], mv["lat"]) != (rec["long"], rec["lat"]) or (mv["north"] is not None and rec["north"] is not None
                                                                      and mv["north"] != rec["north"] and rec["lat"] != "0"):
                rec["cls"] = rec["cls"].replace("A", "X")
        if "C" in rec["cls"] or "X" in rec["cls"]:
            eye.append(((pdf, sign, i), m))
        res[(pdf, sign, i)] = rec
    return data, res, eye


def sheet(data, eye, per=40):
    font = ImageFont.truetype("arial.ttf", 26)
    items = []
    for (pdf, sign, i), m in eye:
        page = wk.doc[pdf - 1]
        s = data[(pdf, sign)]
        row = s["rows"][i]
        x0, x1 = s["rules"][1] + 0.5, s["rules"][2] - 0.5
        im = wk.gray(page, 400, fitz.Rect(x0, row["y"] - 8, x1, row["y"] + 6))
        r = readings(row)
        lab = (f"{pdf} {sign} r{i}  glyph {r['long_g']} {('+' if r['north_tl'] or r['north_img'] else '')}{r['lat_g']}  "
               f"tl {r['long_t']} {r['lat_t']}  +tl {int(r['north_tl'])} +img {int(r['north_img'])}")
        items.append((lab, im))
    files = []
    for k in range(0, len(items), per):
        part = items[k:k + per]
        W = 1500; H = sum(max(im.height, 40) + 12 for _, im in part)
        out = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(out); y = 0
        for lab, im in part:
            d.text((5, y + 5), lab, fill="black", font=font)
            out.paste(im, (1000, y)); y += max(im.height, 40) + 12
        f = wk.OUT + f"CLE_{k // per}.png"; out.save(f); files.append(f)
    return files


if __name__ == "__main__":
    data, res, eye = resolve()
    from collections import Counter
    print("cells", len(res), Counter(v["cls"] for v in res.values()).most_common(12))
    print("eye", len(eye))
    json.dump({f"{k[0]}|{k[1]}|{k[2]}": v for k, v in res.items()}, open(wk.OUT + "CLR.json", "w", encoding="utf-8"),
              ensure_ascii=False)
    print(sheet(data, eye))

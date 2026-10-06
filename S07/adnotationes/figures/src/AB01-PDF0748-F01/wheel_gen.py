"""Generate the TikZ redraw of the astrological wheel of Nallino Part II p. 299 (master PDF page 748) from the reading
of its labels (below) and their positions measured on the print (wheel_items.json, from wheel_items.py). Font sizes
are calibrated on the measured ink widths of the words. Writes figures/AB01-PDF0748-F01.tex."""
import json, math
from pathlib import Path
from fontTools.ttLib import TTFont

LIB = r"C:/Users/Floris/AppData/Local/Programs/MiKTeX/fonts/opentype/public/libertine/"
OUT = Path(__file__).resolve().parents[2] / "AB01-PDF0748-F01.tex"

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpius", "Sagittarius", "Capricornus",
         "Aquarius", "Pisces"]
TERMS = [  # each sector from its clockwise edge: name, degrees
    [("Iupiter", "6°"), ("Venus", "8°"), ("Mercurius", "7°"), ("Mars", "5°"), ("Saturnus", "4°")],
    [("Venus", "8°"), ("Mercurius", "7°"), ("Iupiter", "7°"), ("Saturnus", "4°"), ("Mars", "4°")],
    [("Mercurius", "7°"), ("Inpiter", "7°"), ("Venus", "7°"), ("Mars", "5°"), ("Saturnus", "4°")],
    [("Mars", "6°"), ("Iupitor", "7°"), ("Venus", "7°"), ("Mercurius", "7°"), ("Saturnus", "3°")],
    [("Mercurius", "7°"), ("Venus", "6°"), ("Iupiter", "6°"), ("Saturnus", "6°"), ("Mars", "5°")],
    [("Mercurius", "7°"), ("Venus", "6°"), ("Iupiter", "5°"), ("Mars", "6°"), ("Saturnus", "6°")],
    [("Saturnus", "6°"), ("Venus", "5°"), ("Iupiter", "8°"), ("Mercurius", "5°"), ("Mars", "6°")],
    [("Mars", "6°"), ("Iupiter", "8°"), ("Venus", "7°"), ("Mercurius", "6°"), ("Saturnus", "3°")],
    [("Iupiter", "8°"), ("Venus", "6°"), ("Mercurius", "5°"), ("Saturnus", "6°"), ("Mars", "5°")],
    [("Venus", "6°"), ("Mercurius", "6°"), ("Iupiter", "7°"), ("Mars", "6°"), ("Saturnus", "5°")],
    [("Saturnus", "6°"), ("Mercurius", "6°"), ("Venus", "8°"), ("Iupiter", "5°"), ("Mars", "5°")],
    [("Venns", "8°"), ("Iupiter", "6°"), ("Mercurius", "6°"), ("Mars", "6°"), ("Saturnus", "4°")],
]
TRIP = {"fire": (["☉", "♃", "♄"], ["♃", "☉", "♄"]), "earth": (["♀", "☾", "♂"], ["☾", "♀", "♂"]),
        "air": (["♄", "☿", "♃"], ["☿", "♄", "♃"]), "water": (["♀", "♂", "☾"], ["♂", "♀", "☾"])}
ELEMENT = ["fire", "earth", "air", "water"] * 3
FACES = [["Mars", "Sol", "Venus"], ["Mercurius", "Luna", "Saturnus"], ["Iupiter", "Mars", "Sol"],
         ["Venus", "Mercurius", "Luna"], ["Saturnus", "Iupiter", "Mars"], ["Sol", "Venus", "Mercurius"],
         ["Luna", "Saturnus", "Iupiter"], ["Mars", "Sol", "Venus"], ["Mercurius", "Luna", "Saturnus"],
         ["Iupiter", "Mars", "Sol"], ["Venus", "Mercurius", "Luna"], ["Saturnus", "Iupiter", "Mars"]]
DOMIC = ["Mars", "Venus", "Mercurius", "Luna", "Sol", "Mercurius", "Venus", "Mars", "Iupiter", "Saturnus", "Saturnus",
         "Iupiter"]
EXALT = [("☉", "19°"), ("☾", "3°"), ("☊", "3°"), ("♃", "15°"), (None, "0°"), ("☿", "15°"), ("♄", "21°"), (None, "0°"),
         ("☋", "3°"), ("♂", "28"), (None, "0°"), ("♀", "27°")]
TERM_RAYS = [-10.2, -5.3, -0.2, 4.9, 9.9]  # deg, the regular template where a measurement failed
R = {"inner": 40.3, "exalt": 55.85, "domic": 71.5, "faces": 109.25, "dash": 127.7, "trip": 146.95, "outer": 193.5}


def width(font, text, size):
    f = TTFont(LIB + font)
    cmap = f.getBestCmap()
    hm = f["hmtx"].metrics
    upm = f["head"].unitsPerEm
    glyphs = [cmap[ord(c)] for c in text]
    return sum(hm[g][0] for g in glyphs) / upm * size


items = json.load(open(Path(__file__).with_name("wheel_items.json"), encoding="utf-8"))


def words(sec, ring):
    return [i for i in items if i["sector"] == sec and i["ring"] == ring]


def pol(r, a):
    return f"({a:.2f}:{r:.2f})"


nodes = []
ratios = {"sign": [], "names": [], "deg": [], "faces": [], "domic": []}
for sec in range(12):
    th = 105 + 30 * sec
    # signs
    ws = [w for w in words(sec, "sign") if w["w"] > 8]
    w = max(ws, key=lambda w: w["w"])
    u = w["start_r"] * math.cos(math.radians(w["start_ang"]))
    v = w["start_r"] * math.sin(math.radians(w["start_ang"])) - w["w"] / 2
    phi, rr = math.degrees(math.atan2(v, u)), math.hypot(u, v)
    nodes.append(("sign", SIGNS[sec], th + phi, rr, "base", th + phi - 90))
    ratios["sign"].append(w["w"] / width("LinLibertine_RB.otf", SIGNS[sec], 1))
    # domicile
    ws = [w for w in words(sec, "domic") if w["w"] > 5]
    w = max(ws, key=lambda w: w["w"])
    u = w["start_r"] * math.cos(math.radians(w["start_ang"]))
    v = w["start_r"] * math.sin(math.radians(w["start_ang"])) - w["w"] / 2
    phi, rr = math.degrees(math.atan2(v, u)), math.hypot(u, v)
    nodes.append(("domic", DOMIC[sec], th + phi, rr, "base", th + phi - 90))
    ratios["domic"].append(w["w"] / width("LinLibertine_R.otf", DOMIC[sec], 1))
    # terms
    names = sorted([w for w in words(sec, "terms") if w["start_r"] > 160 and 8 < w["w"] < 40 and w["h"] < 12],
                   key=lambda w: w["cen_ang"])
    degs = sorted([w for w in words(sec, "terms") if w["start_r"] < 160 and 4 < w["w"] < 8],
                  key=lambda w: w["cen_ang"])
    assert len(degs) == 5, (sec, len(degs))
    for k, (name, deg) in enumerate(TERMS[sec]):
        d = degs[k]
        phid = d["cen_ang"] + 137.5 / d["cen_r"]
        nodes.append(("deg", deg, th + phid, d["start_r"], "base west", th + phid + 180))
        ratios["deg"].append(d["w"] / width("LinLibertine_R.otf", deg, 1))
        cand = [w for w in names if abs(w["cen_ang"] + 137.5 / w["cen_r"] - phid) < 2.0]
        if len(cand) == 1:
            w = cand[0]
            phin = w["cen_ang"] + 137.5 / w["cen_r"]
            nodes.append(("names", name, th + phin, w["start_r"], "base west", th + phin + 180))
            ratios["names"].append(w["w"] / width("LinLibertine_RB.otf", name, 1))
        else:  # the template: on the ray of its degrees, from 190.6 pt
            nodes.append(("names", name, th + phid, 190.6, "base west", th + phid + 180))
            print(f"sector {sec} term {k} {name}: template ({len(cand)} candidates)")
    # faces
    fs = sorted([w for w in words(sec, "faces") if w["w"] > 5], key=lambda w: w["cen_ang"])
    assert len(fs) == 3, (sec, len(fs))
    for k, name in enumerate(FACES[sec]):
        w = fs[k]
        phif = w["cen_ang"] + 137.5 / w["cen_r"]
        nodes.append(("faces", name, th + phif, w["start_r"], "base west", th + phif + 180))
        ratios["faces"].append(w["w"] / width("LinLibertine_R.otf", name, 1))
    # triplicities: outer row (day), inner row (night), each read from the left (counterclockwise side)
    ws = [w for w in words(sec, "trip") if w["w"] > 3.5 and w["h"] > 6]
    outer = sorted([w for w in ws if w["cen_r"] > 127.7], key=lambda w: -w["cen_ang"])
    inner = sorted([w for w in ws if w["cen_r"] < 127.7], key=lambda w: -w["cen_ang"])
    assert len(outer) == 3 and len(inner) == 3, (sec, len(outer), len(inner))
    day, night = TRIP[ELEMENT[sec]]
    for row, syms in ((outer, day), (inner, night)):
        for w, sym in zip(row, syms):
            nodes.append(("trip", sym, th + w["cen_ang"], w["cen_r"], "center", th + w["cen_ang"] - 90))
    # exaltation
    ws = sorted([w for w in words(sec, "exalt") if w["w"] > 3 and w["h"] > 5], key=lambda w: -w["cen_ang"])
    sym, deg = EXALT[sec]
    if sym and len(ws) == 1:  # the sign and the number printed close together (Capricornus): split the word
        w = ws[0]
        us = w["start_r"] * math.cos(math.radians(w["start_ang"]))
        vs = w["start_r"] * math.sin(math.radians(w["start_ang"]))
        cu = w["cen_r"] * math.cos(math.radians(w["cen_ang"]))
        a1, r1 = math.degrees(math.atan2(vs - 3.6, cu)), math.hypot(cu, vs - 3.6)
        nodes.append(("esym", sym, th + a1, r1, "center", th + a1 - 90))
        a2, r2 = math.degrees(math.atan2(vs - 8.2, us)), math.hypot(us, vs - 8.2)
        nodes.append(("edeg", deg, th + a2, r2, "base west", th + a2 - 90))
        continue
    if sym:
        assert len(ws) == 2, (sec, len(ws))
        w = ws[0]
        nodes.append(("esym", sym, th + w["cen_ang"], w["cen_r"], "center", th + w["cen_ang"] - 90))
        w = ws[1]
    else:
        assert len(ws) == 1, (sec, len(ws))
        w = ws[0]
    nodes.append(("edeg", deg, th + w["start_ang"], w["start_r"], "base west", th + w["start_ang"] - 90))

for k, v in ratios.items():
    v = sorted(v)
    print(k, "font size (ink width / advance width at 1 pt): median", round(v[len(v) // 2], 2))

FONT = {"sign": r"\fontsize{8.5}{10}\selectfont\bfseries ", "names": r"\fontsize{7.4}{9}\selectfont\bfseries ",
        "deg": r"\fontsize{8.5}{10}\selectfont ", "faces": r"\fontsize{7.7}{9}\selectfont ",
        "domic": r"\fontsize{7.6}{9}\selectfont ", "trip": r"\MoonFont\fontsize{13}{15}\selectfont ",
        "esym": r"\MoonFont\fontsize{11}{13}\selectfont ", "edeg": r"\fontsize{9.5}{11}\selectfont\itshape "}
out = [r"% Nallino, Part II p. 299: the wheel of the terms, triplicities (by day, outer, and by night, inner, of the",
       r"% dashed circle), faces, domiciles and exaltations of the twelve signs, redrawn from the print at the size of the",
       r"% print. Generated by figures/src/AB01-PDF0748-F01/wheel_gen.py: the circles were fitted to the print (one centre), the sector lines stand at",
       r"% multiples of 30 degrees, and every label stands where its ink stands on the print (measured upright, sector by",
       r"% sector); the labels along the radius read from the rim inwards, the others along the circle. Coordinates in",
       r"% pt from the centre, angles counterclockwise from the right.",
       r"\begin{tikzpicture}[x=1pt,y=1pt,every node/.style={inner sep=0pt,outer sep=0pt}]",
       r"\path (-215,-214.75) rectangle (215,215.01);"]
for name in ("inner", "exalt", "domic", "faces", "trip", "outer"):
    out.append(rf"\draw[line width=1pt] (0,0) circle[radius={R[name]}];")
out.append(rf"\draw[line width=0.9pt,dash pattern=on 2.8pt off 2.4pt] (0,0) circle[radius={R['dash']}];")
out.append(r"\foreach \a in {0,30,...,330} \draw[line width=1pt] (\a:" + f"{R['inner']}" + r") -- (\a:" + f"{R['outer']}" + ");")
for kind, text, ang, r, anchor, rot in nodes:
    out.append(rf"\node[anchor={anchor},rotate={rot % 360:.2f}] at {pol(r, ang % 360)} {{{FONT[kind]}{text}}};")
out.append(r"\end{tikzpicture}")
open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("wrote", OUT, len(nodes), "labels")

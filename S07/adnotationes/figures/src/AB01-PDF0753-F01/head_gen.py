"""Generate the head of the table of Nallino, Part II p. 304 (master PDF page 753; the conversion of the eras by the
collected Arab years) as a TikZ picture drawn to the columns of the body of the table, and print the @cols line of
the page file. Positions were measured on the print (PDF points, 1/72 in). The body has rules only between the four
groups of columns; the rules between the columns of a group stand only in the head. The head stands 0.6 pt to the
left of the body on the print (the page is slightly skewed): its measured x positions are moved by SKEW. The group
heads are set as printed: the Arabic as a right-to-left paragraph (the first line indented at the right, the lines
justified, the last line flush right), the Latin justified with the first line indented. Sizes were calibrated on the
lengths of the texts. Writes ../../AB01-PDF0753-F01.tex."""
from pathlib import Path

BP = 25.4 / 72  # mm per PDF point
X0 = 117.76  # the outer edge of the left frame rule in the body (pt)
Y0 = 136.36  # the top of the heavy rule over the table (pt)
SKEW = 0.6  # pt, added to the x positions measured in the head
TEXPT = 25.4 / 72.27  # mm per TeX point
WIDTH = {"|": 0.4 * TEXPT, "<||": 2.0 * TEXPT, "||>": 2.0 * TEXPT, "": 0.0}

# the boundaries of the columns in the body (pt): the group rules (|) and the rules that stand only in the head ("")
RULES = [("|", 148.16), ("", 190.14 + SKEW), ("", 222.12 + SKEW), ("", 254.22 + SKEW), ("|", 289.34),
         ("", 331.14 + SKEW), ("", 363.84 + SKEW), ("", 395.70 + SKEW), ("|", 430.22),
         ("", 473.16 + SKEW), ("", 505.62 + SKEW)]
RIGHT = 542.88  # the outer edge of the right frame rule in the body
TEXT_EDGE = [141.5, 181.2, 210.8, 242.7, 274.8, 319.6, 352.0, 383.9, 416.1, 461.2, 493.6, 526.8]  # right ends (pt)

AR_GROUPS = [  # each group's Arabic: lines with (text, left ink, right ink, baseline); the last line flush right
    [("سنو الروم مكبسة محولة لسني الهجرة", 158.14, 269.98, 237.5),
     ("— الاصل الرومي قبل الهجرة غلب ط", 157.66, 279.10, 254.8),
     (r"يز \AbjadZero{}", 261.76, 278.68, 268.8)],
    [("سنو القبط المكبسة محولة لسني الهجرة", 299.26, 411.70, 237.5),
     ("— الاصل القبطي قبل الهجرة سلز", 298.06, 420.46, 254.8),
     ("ى يط مه", 391.00, 419.92, 267.72)],
    [("سنو الفرس مطلقة محولة", 440.98, 521.26, 237.8),
     ("لسني الهجرة — الاصل", 440.20, 528.52, 253.38),
     ("الفارسي بعد الهجرة ط يا ط", 440.44, 529.12, 267.96)],
]
LAT_GROUPS = [  # each group's Latin: lines with (text, left ink, right ink, baseline, justified)
    [("Anni Romanorum, intercala-", 166.06, 279.34, 281.6, True),
     ("tionem habentes, secundum an-", 157.90, 279.10, 290.2, True),
     ("nos hegirae conversi. Aerae ini-", 157.54, 278.98, 298.7, True),
     ("tium, ante hegiram, 932 an.,", 157.90, 279.22, 307.3, True),
     ("9 m., 17 d., 0 fract.", 157.30, 236.26, 316.0, False)],
    [("Anni Coptorum, intercalatio-", 307.54, 420.22, 281.6, True),
     ("nem habentes, secundum annos", 298.66, 419.98, 290.2, True),
     ("hegirae conversi. Aerae initium,", 298.54, 420.10, 298.7, True),
     ("ante hegiram, 337 an., 10 m.,", 298.42, 420.34, 307.3, True),
     ("19 d., 45 fract.", 299.02, 356.98, 316.0, False)],
    [("Anni Persarum, sine", 448.42, 529.78, 281.6, True),
     ("intercalatione, secun-", 440.14, 529.42, 290.2, True),
     ("dum annos heg. con-", 439.66, 529.78, 298.9, True),
     ("versi. Aerae initium,", 440.14, 530.14, 307.3, True),
     ("p. heg., 9 a., 11 m., 9 d.", 440.14, 529.90, 316.1, True)],
]
SUBHEADS = [  # Arabic and its ink centre, Latin and the centre of its ink
    ("سنون", (168.68, 341.86), "Anni.", 168.70), ("شهور", (205.34, 342.70), "Menses.", 206.42),
    ("ايام", (238.90, 341.86), "Dies.", 238.00), ("كسور", (271.98, 339.70), "Fraction.", 271.56),
    ("سنون", (309.70, 341.74), "Anni.", 310.00), ("شهور", (347.18, 342.82), "Menses.", 347.78),
    ("ايام", (380.22, 341.86), "Dies.", 379.56), ("كسور", (413.64, 339.70), "Fraction.", 413.10),
    ("سنون", (451.54, 341.90), "Anni.", 451.42), ("شهور", (488.52, 341.80), "Menses.", 489.78),
    ("ايام", (522.94, 342.04), "Dies.", 522.88)]


def mm(x):
    return (x - X0) * BP


def ymm(y):
    return -(y - Y0) * BP


def layout():
    edges, widths, pos = [], [], WIDTH["<||"]
    for kind, xc in RULES + [("||>", None)]:
        target = (mm(xc) - WIDTH[kind] / 2) if xc else mm(RIGHT) - WIDTH["||>"]
        w = round(target - pos, 2)
        widths.append(w)
        edges.append((pos, pos + w))
        pos += w + WIDTH[kind]
    return widths, edges


def cols_line(widths, edges):
    toks = ["<||"]
    for k, w in enumerate(widths):
        toks.append(f"{w:.2f}r<{edges[k][1] - mm(TEXT_EDGE[k]):.2f}")
        sep = RULES[k][0] if k < len(RULES) else "||>"
        if sep:
            toks.append(sep)
    return "@cols 0 " + " ".join(toks)


def rect(x0, y0, x1, y1):
    return rf"\fill ({x0:.3f},{y0:.3f}) rectangle ({x1:.3f},{y1:.3f});"


def font(size, bold=False):
    return rf"\fontsize{{{size}}}{{{size * 1.2:.1f}}}\selectfont" + (r"\bfseries" if bold else "")


def main():
    widths, edges = layout()
    print(cols_line(widths, edges))
    right = edges[-1][1] + WIDTH["||>"]
    t = 0.4 * TEXPT
    heavy = 1.3 * TEXPT
    y_title, y_groups, y_head = ymm(219.52), ymm(325.36), ymm(363.28)
    bottom = -y_head + heavy
    L = [r"% Nallino, Part II p. 304: the head of the table of the conversion of the eras by the collected Arab years,",
         r"% drawn to the columns of the body of the table (generated by figures/src/AB01-PDF0753-F01/head_gen.py;",
         r"% coordinates in mm from the outer edge of the frame and from its top, y upwards)",
         r"\begin{tikzpicture}[x=1mm,y=1mm,every node/.style={inner sep=0pt,outer sep=0pt}]",
         rf"\path (0,0) rectangle ({right:.3f},{-bottom:.3f});",
         rect(0, 0, right, -1.2 * TEXPT), rect(0, -2.2 * TEXPT, right, -2.6 * TEXPT)]
    for x in (0, WIDTH["<||"] - t, right - WIDTH["||>"], right - t):
        L.append(rect(x, 0, x + t, -bottom))
    L.append(rect(0, y_title, right, y_title - t))
    L.append(rect(0, y_head, right, y_head - heavy))
    L.append(rect(edges[0][1], y_groups, right - WIDTH["||>"], y_groups - t))  # under the group heads
    for k, (kind, xc) in enumerate(RULES):
        x = edges[k][1]
        if kind == "|":  # the group rules, from the title rule down
            L.append(rect(x, y_title - t, x + WIDTH["|"], y_head))
        else:  # the rules between the columns of a group, under the group heads only
            xm = mm(xc) - WIDTH["|"] / 2
            L.append(rect(xm, y_groups - t, xm + WIDTH["|"], y_head))
    # the title and the head of the first column
    L.append(rf"\node[anchor=center] at ({mm(329.36 + SKEW):.3f},{ymm(167.58):.3f}) "
             rf"{{{font(13.9)} \textarabic{{جدول تحويل التواريخ بعضها الى بعض في مجموعة العرب}}}};")
    L.append(rf"\node[anchor=base] at ({mm(329.00 + SKEW):.3f},{ymm(197.16):.3f}) "
             rf"{{{font(12.7, True)} Tabula conversionis aerarum in alias, secundum annos Arabicos collectos.}};")
    L.append(rf"\node[anchor=center,rotate=90] at ({mm(128.78 + SKEW):.3f},{ymm(293.04):.3f}) "
             rf"{{{font(11.1)} \textarabic{{سنو العرب المجموعة}}}};")
    L.append(rf"\node[anchor=center,rotate=90] at ({mm(139.98 + SKEW):.3f},{ymm(292.44):.3f}) "
             rf"{{{font(10.0)} Anni Arabum collecti [ab aera].}};")
    # the group heads
    for lines in AR_GROUPS:
        for k, (text, a, b, base) in enumerate(lines):
            if k < len(lines) - 1:  # justified to its printed length
                L.append(rf"\node[anchor=base west] at ({mm(a + SKEW):.3f},{ymm(base):.3f}) "
                         rf"{{{font(9.9)}\makebox[{(b - a) * BP:.3f}mm][s]{{\textarabic{{{text}}}}}}};")
            else:  # the last line, flush right
                L.append(rf"\node[anchor=base east] at ({mm(b + SKEW):.3f},{ymm(base):.3f}) "
                         rf"{{{font(9.9)}\textarabic{{{text}}}}};")
    for lines in LAT_GROUPS:  # in the type of the head of the last columns on p. 302, at its size there (the lines
        # set at the size of their printed last lines would not fit the justified lines)
        for text, a, b, base, just in lines:
            box = rf"\makebox[{(b - a) * BP:.3f}mm][s]{{{text}}}" if just else text
            L.append(rf"\node[anchor=base west] at ({mm(a + SKEW):.3f},{ymm(base):.3f}) {{{font(9.1, True)}{box}}};")
    for ar, (ax, ay), lat, lx in SUBHEADS:
        L.append(rf"\node[anchor=center] at ({mm(ax + SKEW):.3f},{ymm(ay):.3f}) {{{font(10.8)} \textarabic{{{ar}}}}};")
        L.append(rf"\node[anchor=base] at ({mm(lx + SKEW):.3f},{ymm(355.2):.3f}) {{{font(7.2, True)} {lat}}};")
    L.append(r"\end{tikzpicture}")
    out = Path(__file__).resolve().parents[2] / "AB01-PDF0753-F01.tex"
    out.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("wrote", out, f"(height {bottom:.3f} mm)")


if __name__ == "__main__":
    main()

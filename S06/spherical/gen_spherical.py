"""Generate the edition of Nallino's Part II pp. 55-58 from the TSV files of this folder: the sines (pp. 55-56,
three sections per page), the declination of the Sun with the four arcs of equal declination (pp. 57-58), and on
p. 58 the figure of the orders of declination (redrawn in TikZ from fig58.tsv) and the right ascensions of the
decades with their sines (printed in bold, as in the print). Output: p2_spherical.tex"""
import math
from pathlib import Path

from gen_stars import PREAMBLE, read
from gen_stars import markup as _markup


def markup(s):
    """the modifier letters of hours, minutes and seconds (13ʰ 15ᵐ 32ˢ) as superscripts, which every face has"""
    out = _markup(s)
    for ch, t in (("ʰ", "h"), ("ᵐ", "m"), ("ˢ", "s")):
        out = out.replace(ch, r"\textsuperscript{" + t + "}")
    return out


HERE = Path(__file__).resolve().parent
WIDTHS = r"\newlength{\Dw}\newlength{\Mw}\settowidth{\Dw}{000}\settowidth{\Mw}{00}"
SIGNCOL = r">{\centering\arraybackslash}p{9mm}"          # the four arcs of equal declination


def nl(s):
    return markup(s).replace(" / ", r"\\").replace(r"\\[", r"\\{}[")


def ar(s):
    return r"\\".join(r"\textarabic{" + x + "}" for x in s.split(" / ")) if s else ""


def box(v, w=r"\Mw"):
    return r"\makebox[" + w + "][r]{" + v + "}"


def num(vals, marks=None, gap="2.2mm"):
    vals = [v + (r"\rlap{" + m + "}" if m else "") for v, m in zip(vals, marks or [""] * len(vals))]
    return (r"\hspace{" + gap + "}").join(box(v, r"\Dw" if k == 0 else r"\Mw") for k, v in enumerate(vals))


def head(h, w):
    a, l = h.split("‖")
    inner = (ar(a) + r"\\" if a else "") + nl(l)
    return r"\parbox[c]{" + w + r"}{\centering\scriptsize " + inner + r"\par\vspace{0.7mm}}"


def vhead(h):
    a, l = h.split("‖")
    inner = (ar(a) + r"\\" if a else "") + nl(l)
    return r"\rotatebox{90}{\scriptsize\begin{tabular}{@{}c@{}}" + inner + r"\end{tabular}}"


def running(pp, fol):
    rh = (r"\noindent\makebox[\textwidth]{\hfill{\scriptsize AL-BATTANI OPUS ASTRONOMICUM}\hfill\llap{" + str(pp) + "}}"
          if pp % 2 else r"\noindent\makebox[\textwidth]{\rlap{" + str(pp) + r"}\hfill{\scriptsize C. A. NALLINO}\hfill}")
    return [r"\clearpage", rh, r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{1mm}",
            r"\begin{center}{\small " + fol + r"}\end{center}\vspace{-3mm}"]


def title(p, ncol, w="165mm"):
    la = "".join(r"\\\textbf{" + markup(x) + "}" for x in p["title_la"].split(" / "))
    return (r"\multicolumn{" + str(ncol) + r"}{||c||}{\parbox{" + w + r"}{\centering\vspace{1mm}{\large " + ar(p["title_ar"]) +
            "}" + la + r"\vspace{1mm}}} \\ \hline")


def sines_page(p, rows):
    out = running(int(p["ppage"]), p["fol"])
    spec = "||" + "||".join([r">{\centering\arraybackslash}p{27mm}|>{\centering\arraybackslash}p{19mm}"] * 3) + "||"
    out.append(r"\begin{center}\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.02}\begin{tabular}{" + spec + r"}\hline")
    out.append(title(p, 6))
    hs = p["heads"].split("|")
    out.append(" & ".join(head(h, "27mm" if k % 2 == 0 else "19mm") for k, h in enumerate(hs)) + r" \\ \hline\hline")
    by = {(int(r["section"]), int(r["row"])): r for r in rows}
    for i in range(1, 31):
        line = []
        for k in (1, 2, 3):
            r = by[(k, i)]
            m1 = ["°", "′"] if i == 1 else None
            arc = num([r["arc_d"], r["arc_m"]], m1, "1.2mm") + r"\hspace{2.6mm}" + num([r["supp_d"], r["supp_m"]], m1, "1.2mm")
            sn = num([r["sin_p"], r["sin_m"], r["sin_s"]], [r"\textsuperscript{p}", "′", "″"] if i == 1 else None, "1.6mm")
            line += [arc, sn]
        out.append(" & ".join(line) + r" \\" + (r"[1.2mm]" if i % 5 == 0 and i < 30 else ""))
    out.append(r"\hline\end{tabular}\end{center}")
    return "\n".join(out)


def decl_block(p, rows, heads, with_arabic_span=True):
    """one half: declination and the four arcs"""
    hs = heads
    first = head(hs[0], "26mm")
    span = head(hs[1], "42mm")
    signs = [vhead(h) for h in hs[2:6]]
    rows_tex = []
    for i, r in enumerate(rows):
        m = ["°", "′", "″"] if i == 0 else None
        cells = [num([r["decl_d"], r["decl_m"], r["decl_s"]], m)] + \
                [r["arc_" + k] + (r"\rlap{°}" if i == 0 else "") for k in "abcd"]
        rows_tex.append(" & ".join(cells) + r" \\" + (r"[1.2mm]" if i % 5 == 4 and i < len(rows) - 1 else ""))
    return first, span, signs, rows_tex


def page57(p, rows):
    out = running(57, p["fol"])
    spec = "||" + r">{\centering\arraybackslash}p{26mm}|" + "|".join([SIGNCOL] * 4) + "||" + \
           r">{\centering\arraybackslash}p{26mm}|" + "|".join([SIGNCOL] * 4) + "||"
    hs = p["heads"].split("|")
    L = [r for r in rows if r["half"] == "L"]; R = [r for r in rows if r["half"] == "R"]
    f1, s1, g1, r1 = decl_block(p, L, hs[:6]); f2, s2, g2, r2 = decl_block(p, R, hs[6:])
    out.append(r"\begin{center}\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.02}\begin{tabular}{" + spec + r"}\hline")
    out.append(title(p, 10))
    out.append(r"\multirow{2}{*}{" + f1 + r"} & \multicolumn{4}{c||}{" + s1 + r"} & \multirow{2}{*}{" + f2 + r"} & \multicolumn{4}{c||}{" + s2 + r"} \\ \cline{2-5}\cline{7-10}")
    out.append(" & " + " & ".join(g1) + " & & " + " & ".join(g2) + r" \\ \hline\hline")
    for a, b in zip(r1, r2):
        out.append(a.rsplit(r" \\", 1)[0] + " & " + b)
    out.append(r"\hline\end{tabular}\end{center}")
    return "\n".join(out)


def figure58(p, items):
    """the orders of declination: circle, square band of 24 cells, labels"""
    R, W = 34.0, 6.0                   # mm: radius of the circle (= half-diagonal of the outer square), band width
    r_in = R - W * math.sqrt(2)        # half-diagonal of the inner square
    T = [r"\begin{tikzpicture}[x=1mm,y=1mm,font=\itshape\scriptsize]",
         rf"\draw (0,0) circle ({R});",
         rf"\draw (-{R},0)--(0,{R})--({R},0)--(0,-{R})--cycle;",
         rf"\draw (-{r_in:.3f},0)--(0,{r_in:.3f})--({r_in:.3f},0)--(0,-{r_in:.3f})--cycle;"]
    # cross lines: 6 per side, perpendicular to the side, at k/7 of its length
    corners = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    for c in range(4):
        (ax, ay), (bx, by) = corners[c], corners[(c + 1) % 4]
        for k in range(1, 7):
            t = k / 7
            ox, oy = R * (ax + t * (bx - ax)), R * (ay + t * (by - ay))
            ix, iy = r_in * (ax + t * (bx - ax)), r_in * (ay + t * (by - ay))
            T.append(rf"\draw ({ox:.3f},{oy:.3f})--({ix:.3f},{iy:.3f});")
    rm = (R + r_in) / 2                # the middle line of the band
    sides = {"upper-left": (corners[0], corners[1], 45), "upper-right": (corners[1], corners[2], -45),
             "lower-right": (corners[2], corners[3], 45), "lower-left": (corners[3], corners[0], -45)}
    for it in items:
        k, pos, a, l, rot = it["kind"], it["position"], it["text_ar"], it["text_la"], it["rot"]
        if k == "cell":
            if pos.startswith("corner"):
                c = {"left": (-1, 0), "top": (0, 1), "right": (1, 0), "bottom": (0, -1)}[pos.split()[1]]
                x, y = rm * c[0] * 0.93, rm * c[1] * 0.93
                ang = 0
            else:
                side, j = pos.rsplit(" ", 1)
                (ax, ay), (bx, by), ang = sides[side]
                t = (int(j) + 0.5) / 7
                x, y = rm * (ax + t * (bx - ax)), rm * (ay + t * (by - ay))
            T.append(rf"\node[rotate={ang},font=\itshape\footnotesize] at ({x:.2f},{y:.2f}) {{{l}}};")
        elif k == "dir":
            arx = (r"\textarabic{" + a + "}") if a else ""
            if pos == "top":
                T.append(rf"\node[align=center] at (0,{R + 5}) {{{arx}\\{l}}};")
            elif pos == "bottom":
                T.append(rf"\node[align=center] at (0,-{R + 5}) {{{l}\\{arx}}};")
            elif pos == "left":
                T.append(rf"\node[rotate=90,align=center] at (-{R + 5},0) {{{arx}\\{l}}};")
            else:
                T.append(rf"\node[rotate=-90,align=center] at ({R + 4},0) {{{l}}};")
        elif k == "sign":
            arx = r"\textarabic{" + a + "}"
            xy = {"top": (0, r_in * 0.45), "bottom": (0, -r_in * 0.45), "left": (-r_in * 0.5, 0), "right": (r_in * 0.5, 0)}[pos]
            T.append(rf"\node[rotate={rot},align=center] at ({xy[0]:.2f},{xy[1]:.2f}) {{{l}\\{arx}}};")
        elif k == "order":
            c = {"upper-left": (-1, 1), "upper-right": (1, 1), "lower-left": (-1, -1), "lower-right": (1, -1)}[pos]
            d = (R / math.sqrt(2) + R) / 2 * 1.01          # midway between the side of the square and the circle
            x, y = c[0] * d / math.sqrt(2), c[1] * d / math.sqrt(2)
            txt = r"\\".join(l.split(" / ")) + r"\\\textarabic{" + a + "}"
            T.append(rf"\node[rotate={rot},align=center,font=\itshape\tiny] at ({x:.2f},{y:.2f}) {{{txt}}};")
    T.append(r"\end{tikzpicture}")
    return "\n".join(T)


def ra_table(p, rows):
    hs = p["heads"].split("|")
    out = [r"\setlength{\tabcolsep}{4pt}\begin{tabular}{||c|>{\centering\arraybackslash}p{27mm}|>{\centering\arraybackslash}p{24mm}||}\hline\hline",
           vhead(hs[0]) + " & " + head(hs[1], "27mm") + " & " + head(hs[2], "24mm") + r" \\ \hline\hline"]
    for i, r in enumerate(rows):
        m = ["°", "′", "″"] if i == 0 else None
        out.append(r["decade"] + (r"\rlap{°}" if i == 0 else "") + " & " + num([r["ra_d"], r["ra_m"], r["ra_s"]], m) +
                   r" & \bfseries " + num([r["sin_p"], r["sin_m"], r["sin_s"]], m) + r" \\")
    out.append(r"\hline\hline\end{tabular}")
    return "\n".join(out)


def page58(pd, pr, pf, rows, ra_rows, items):
    out = running(58, pd["fol"])
    hs = pd["heads"].split("|")
    f1, s1, g1, r1 = decl_block(pd, rows, hs)
    left = [r"\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.02}\begin{tabular}{||>{\centering\arraybackslash}p{26mm}|" +
            "|".join([SIGNCOL] * 4) + "||}\\hline",
            title(pd, 5, "75mm"),
            r"\multirow{2}{*}{" + f1 + r"} & \multicolumn{4}{c||}{" + s1 + r"} \\ \cline{2-5}",
            " & " + " & ".join(g1) + r" \\ \hline\hline"] + r1 + [r"\hline\end{tabular}"]
    la = r"\\".join(r"\textbf{" + markup(x) + "}" for x in pf["title_la"].split(" / "))
    right = [r"\begin{center}{\large\textarabic{" + pf["title_ar"] + r"}}\\" + la + r"\end{center}\vspace{-2mm}",
             r"\begin{center}" + figure58(pf, items) + r"\end{center}\vspace{2mm}",
             r"\begin{center}" + ra_table(pr, ra_rows) + r"\end{center}"]
    out.append(r"\noindent\begin{minipage}[t]{0.52\textwidth}\vspace{0pt}" + "\n".join(left) + r"\end{minipage}\hfill" +
               r"\begin{minipage}[t]{0.46\textwidth}\vspace{0pt}" + "\n".join(right) + r"\end{minipage}")
    return "\n".join(out)


def three_sections(p, rows, arg, val, argw, valw, group=5):
    """pp. 59-60: three sections side by side, each an argument column and a value column"""
    out = running(int(p["ppage"]), p["fol"])
    col = r">{\centering\arraybackslash}p{" + argw + r"}|>{\centering\arraybackslash}p{" + valw + "}"
    out.append(r"\begin{center}\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.02}\begin{tabular}{||" + "||".join([col] * 3) +
               r"||}\hline")
    la = "".join(r"\\\textbf{" + markup(x) + "}" for x in p["title_la"].split(" / "))
    out.append(r"\multicolumn{6}{||c||}{\parbox{170mm}{\centering\vspace{1mm}{\large " + ar(p["title_ar"]) + "}" + la +
               r"\vspace{1mm}}} \\ \hline")
    hs = p["heads"].split("|")
    out.append(" & ".join(head(h, argw if k % 2 == 0 else valw) for k, h in enumerate(hs)) + r" \\ \hline\hline")
    by = {(int(r["section"]), int(r["row"])): r for r in rows}
    n = max(int(r["row"]) for r in rows)
    for i in range(1, n + 1):
        line = []
        for k in (1, 2, 3):
            r = by[(k, i)]
            line += [arg(r, i == 1), val(r, i == 1)]
        out.append(" & ".join(line) + r" \\" + (r"[1.2mm]" if i % group == 0 and i < n else ""))
    out.append(r"\hline\end{tabular}\end{center}")
    return "\n".join(out)


def raeq_page(p, rows, second=("eq_d", "eq_m")):
    """pp. 61-64: the common numbers 1-30, and for three signs the degrees of ascension and the equation of days"""
    out = running(int(p["ppage"]), p["fol"])
    col = r">{\centering\arraybackslash}p{27mm}|>{\centering\arraybackslash}p{25mm}"
    out.append(r"\begin{center}\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.02}\begin{tabular}{||c|" +
               "||".join([col] * 3) + r"||}\hline")
    out.append(title(p, 7, "170mm"))
    hs = p["heads"].split("|")
    out.append(" & ".join([vhead(hs[0])] + [head(h, "27mm" if k % 2 == 0 else "25mm") for k, h in enumerate(hs[1:])]) +
               r" \\ \hline\hline")
    signs = []
    for r in rows:
        if r["sign"] not in signs:
            signs.append(r["sign"])
    by = {(r["sign"], int(r["row"])): r for r in rows}
    for i in range(1, 31):
        line = [str(i)]
        for s in signs:
            r = by[(s, i)]
            m = ["°", "′"] if i == 1 else None
            line += [num([r["asc_d"], r["asc_m"]], m, "2mm"), num([r[second[0]], r[second[1]]], m, "2mm")]
        out.append(" & ".join(line) + r" \\" + (r"[1.2mm]" if i % 5 == 0 and i < 30 else ""))
    out.append(r"\hline\end{tabular}\end{center}")
    return "\n".join(out)


def oblique_page(p, rows, ncols, colw):
    """pp. 65-67: sign names (vertical, three rows each), the decades, and the columns of ascensions (and hours)"""
    out = running(int(p["ppage"]), p["fol"])
    out.append(r"\begin{center}\setlength{\tabcolsep}{2.5pt}\renewcommand{\arraystretch}{1.0}\begin{tabular}{||c|c|" +
               "|".join([r">{\centering\arraybackslash}p{" + colw + "}"] * ncols) + r"||}\hline")
    out.append(title(p, ncols + 2, "175mm"))
    hs = p["heads"].split("|")
    cells = [vhead(hs[0]), vhead(hs[1])]
    for h in hs[2:]:
        parts = h.split("‖")
        if len(parts) == 4:                        # clime and latitude above, «Gradus ascensionum» below
            _, upper, a, lower = parts
            inner = nl(upper) + r"\\[-0.6ex]\rule{0.8\linewidth}{0.3pt}\\" + (ar(a) + r"\\" if a else "") + nl(lower)
            cells.append(r"\parbox[c]{" + colw + r"}{\centering\scriptsize " + inner + r"\par\vspace{0.7mm}}")
        else:
            cells.append(head(h, colw))
    out.append(" & ".join(cells) + r" \\ \hline\hline")
    for i, r in enumerate(rows):
        sign = (r"\multirow{3}{*}{\rotatebox{90}{\tiny " + r["sign"] + ".}}") if i % 3 == 0 else ""
        line = [sign, r["decade"]]
        for k in range(1, ncols + 1):
            line.append(num([r[f"c{k}_d"], r[f"c{k}_m"]], ["°", "′"] if i == 0 else None, "2mm"))
        out.append(" & ".join(line) + r" \\" + (r" \hline" if i % 3 == 2 and i < len(rows) - 1 else ""))
    out.append(r"\hline\end{tabular}\end{center}")
    return "\n".join(out)


def document():
    pages = read("sph_pages.tsv"); sines = read("sines_p2.tsv"); decl = read("decl_p2.tsv")
    ra10 = read("ra10_p2.tsv"); items = read("fig58.tsv")
    P = {(p["ppage"], p["table"]): p for p in pages}
    out = [PREAMBLE.replace("margin=16mm", "margin=12mm").replace(r"\usepackage{fontspec,amsmath,array,multirow,graphicx}",
                                                                   r"\usepackage{fontspec,amsmath,array,multirow,graphicx,tikz}"),
           WIDTHS, r"\begin{document}"]
    out.append(sines_page(P[("55", "sines")], [r for r in sines if r["ppage"] == "55"]))
    out.append(sines_page(P[("56", "sines")], [r for r in sines if r["ppage"] == "56"]))
    out.append(page57(P[("57", "decl")], [r for r in decl if r["ppage"] == "57"]))
    out.append(page58(P[("58", "decl")], P[("58", "ra10")], P[("58", "figure")], [r for r in decl if r["ppage"] == "58"], ra10, items))
    out.append(three_sections(P[("59", "days")], read("days59_p2.tsv"),
                              lambda r, f: num([str(r["phi_d"]), str(r["phi_m"])], ["°", "′"] if f else None, "1.6mm"),
                              lambda r, f: num([r["inc_d"], r["inc_m"]], ["°", "′"] if f else None, "1.6mm"), "22mm", "30mm", 5))
    out.append(three_sections(P[("60", "shadows")], read("shadows60_p2.tsv"),
                              lambda r, f: str(r["alt"]),
                              lambda r, f: num([r["dig"], r["min"]], [r"\textsuperscript{\,dig.}", "′"] if f else None, "7mm"),
                              "22mm", "30mm", 5))
    raeq = read("raeq_p2.tsv")
    for pp in ("61", "62", "63", "64"):
        out.append(raeq_page(P[(pp, "raeq")], [r for r in raeq if r["ppage"] == pp]))
    raq = read("raqqah_p2.tsv")
    obl = read("oblique_p2.tsv")
    out.append(oblique_page(P[("65", "oblique")], [r for r in obl if r["ppage"] == "65"], 6, "23mm"))
    out.append(oblique_page(P[("66", "oblique")], [r for r in obl if r["ppage"] == "66"], 7, "20mm"))
    out.append(oblique_page(P[("67", "cities")], [r for r in obl if r["ppage"] == "67"], 6, "23mm"))
    for pp in ("68", "69", "70", "71"):
        out.append(raeq_page(P[(pp, "raqqah")], [r for r in raq if r["ppage"] == pp], ("hr_d", "hr_m")))
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p2_spherical.tex").write_text(document(), encoding="utf-8")
    print("wrote p2_spherical.tex")

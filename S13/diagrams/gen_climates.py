"""Generate the two editions of the diagram of the seven climes from the checked TSV data:
  p3_climates.tex - Part III p. 243 (the codex figure), Arabic, as printed
  p2_climates.tex - Part II p. 92 (Nallino's Latin figure), as printed
The figures are drawn with TikZ on the measured geometry of the master scan (radii in pt, scaled), with every text at
its printed position and orientation:
  Part III: ring cells along the circles, top outward, the degrees on the side of the line toward the horizontal axis;
  the names of the inner circle along the radius, starting at the circle; the sign names outside the outer circle along
  the radius, starting at the circle; درج, دقائق, الحمل, الميزان along the circle, top outward.
  Part II: the values upright on the page as far as the circle allows (top outward above the horizontal axis, inward
  below), degrees before minutes in reading order."""
import re
from pathlib import Path

from gen_stars import PREAMBLE, AR_DIGITS, markup, read

HERE = Path(__file__).resolve().parent
P3_RADII = [77.0, 106.0, 132.6, 159.0, 186.2, 213.1, 241.8, 271.2]       # master PDF 909
P2_RADII = [71.8, 90.7, 111.9, 131.2, 151.9, 171.6, 189.1, 205.0]        # master PDF 541
LINES = [i * 22.5 for i in range(16)]
SCALE = 0.78


def ar(s):
    s = s.replace("{stroke}", "‌ـ‌")             # the free stroke of the 247.5 name: an unjoined tatweel
    return r"\textarabic{" + markup(s, False) + "}"


def lat(s):
    s = re.sub(r"(\d+)([hm])\b", r"\1\\textsuperscript{\2}", s)      # 13h 30m: the h and m raised, as printed
    return markup(s).replace(" / ", r"\\")


def node(x, y, rot, anchor, text, size=r"\footnotesize", align=None):
    opts = [f"rotate={rot:.2f}", f"anchor={anchor}", "inner sep=0.6pt", "font={" + size + "}"]   # font= keeps the size
    if align:                                                                                       # after a line break
        opts.append(f"align={align}")
    return rf"\node[{','.join(opts)}] at ({x:.2f},{y:.2f}) {{{text}}};"


def polar(t, r):
    import math
    return r * math.cos(math.radians(t)), r * math.sin(math.radians(t))


def frame(radii):
    out = [rf"\draw[line width=0.5pt] (0,0) circle ({r});" for r in radii]
    out += [rf"\draw[line width=0.5pt] ({t}:{radii[0]}) -- ({t}:{radii[-1]});" for t in LINES]
    return out


def mids(radii):
    return [(radii[k - 1] + radii[k]) / 2 for k in range(1, len(radii))]


def toward_axis_ccw(t):
    """True when the counterclockwise side of the line at t is the side toward the horizontal axis."""
    return (t % 180) > 90


def cell_nodes(rows, radii, arabic):
    out, M = [], mids(radii)
    for r in rows:
        if r["kind"] not in ("cell", "axis"):
            continue
        t, k = float(r["t"]), int(r["ring"]); rm = M[k - 1]
        if r["kind"] == "cell":
            ccw = (r["side"] == "deg") == toward_axis_ccw(t) if arabic else None
            if not arabic:                                  # Latin: degrees first in reading order
                ccw = (r["side"] == "deg") == (t < 180)
        else:
            ccw = r["side"] == "ccw"
        text = ar(r["text"]) if arabic else lat(r["text"])
        size = r"\footnotesize" if k > 1 else r"\scriptsize"                 # the innermost ring is narrow
        if r["kind"] == "axis" and (len(r["text"]) > 3 or "/" in r["text"]):
            size = r"\tiny" if r["text"] == "horae / eius" or k <= 2 else r"\scriptsize"
        if t in (0, 180):                                   # the zeros of the horizontal axis, upright
            d = 9.0 / rm * 57.2958
            x, y = polar(t + (d if ccw else -d), rm)
            out.append(node(x, y, 0, "center", text, size))
            continue
        gap = 2.2 / rm * 57.2958                            # a small gap between the text and the line
        phi = t + (gap if ccw else -gap)
        x, y = polar(phi, rm)
        if arabic or t < 180:                               # top outward: +x of the text runs clockwise
            rot, anchor = phi - 90, ("east" if ccw else "west")
        else:                                               # Part II below the axis: top inward, +x counterclockwise
            rot, anchor = phi + 90, ("west" if ccw else "east")
        out.append(node(x, y, rot, anchor, text, size, align="center" if "/" in r["text"] else None))
    return out


def p3_figure(rows):
    out = [r"\begin{tikzpicture}[x=" + f"{SCALE}pt,y={SCALE}pt" + "]"] + frame(P3_RADII) + cell_nodes(rows, P3_RADII, True)
    for r in rows:
        k = r["kind"]
        if k == "wind":
            t = float(r["t"]); x, y = polar(t, P3_RADII[0] - 3)
            out.append(node(x, y, t, "east", ar(r["text"]), r"\small"))
        elif k in ("sign", "colhead", "azimuth"):
            t, rr = float(r["t"]), float(r["r"])
            if r["orient"] == "radial":
                x, y = polar(t, rr + 1)
                out.append(node(x, y, t + 180, "east", ar(r["text"]), r"\small"))
            elif r["orient"] == "tangential":
                x, y = polar(t, rr + 3)
                out.append(node(x, y, t - 90, "center", ar(r["text"]), r"\small"))
            else:
                x, y = polar(t, rr + 3)
                out.append(node(x, y, 0, "center", ar(r["text"]), r"\small"))
    corners = {"TL": (-233, 254), "TR": (216, 258), "BL": (-234, -278), "BR": (216, -277)}
    for pos, (x, y) in corners.items():
        lines = [r["text"] for r in rows if r["kind"] == "corner" and r["side"] == pos]
        out.append(node(x, y, 0, "center", r"\begin{tabular}{c}" + r"\\".join(ar(s) for s in lines) + r"\end{tabular}", r"\normalsize"))
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def p2_figure(rows):
    out = [r"\begin{tikzpicture}[x=" + f"{SCALE * 1.24:.3f}pt,y={SCALE * 1.24:.3f}pt" + "]"] + frame(P2_RADII) + cell_nodes(rows, P2_RADII, False)
    R = P2_RADII[-1]
    for r in rows:
        k = r["kind"]
        if k == "wind":
            t = float(r["t"]); x, y = polar(t, P2_RADII[0] - 2.5)
            out.append(node(x, y, t, "east", lat(r["text"]), r"\scriptsize"))
        elif k == "sign":
            t = float(r["t"]); x, y = polar(t, R + 3)
            left = 90 < t <= 270
            out.append(node(x, y, t + 180 if left else t, "east" if left else "west", lat(r["text"]), r"\scriptsize",
                            align="left" if not left else "right"))
        elif k == "azimuth":
            t = float(r["t"]); x, y = polar(t, R + 4)      # set downward along the vertical axis, outside the circle
            out.append(node(x, y, -90, "east" if t == 90 else "west", lat(r["text"]), r"\scriptsize\bfseries", align="left"))
        elif k == "side":
            t = float(r["t"]); x, y = polar(t, R + 52)
            out.append(node(x, y, 90 if t == 180 else -90, "center", lat(r["text"]), r"\small\bfseries"))
    corners = {"TL": (-175, 256), "TR": (207, 245), "BL": (-195, -228), "BR": (198, -239)}
    for pos, (x, y) in corners.items():
        lines = [r["text"] for r in rows if r["kind"] == "corner" and r["side"] == pos]
        out.append(node(x, y, 0, "center", r"\begin{tabular}{c}\bfseries " + r"\\\bfseries ".join(lat(s) for s in lines) + r"\end{tabular}", r"\small"))
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


PRE = PREAMBLE.replace("margin=16mm", "margin=11mm").replace(r"\usepackage{polyglossia}", r"\usepackage{tikz}" "\n" r"\usepackage{polyglossia}")


def p3_document():
    rows = read("climates_p3.tsv")
    head = {r["side"]: r["text"] for r in rows if r["kind"] == "header"}
    title = [r["text"] for r in rows if r["kind"] == "title"]
    out = [PRE, r"\begin{document}",
           r"\noindent{\large\textarabic{" + head["page"].translate(AR_DIGITS) + r"}}\hfill " + head["fol"] + r"\hfill\mbox{}\par\vspace{2mm}",
           r"\begin{center}\large " + r"\\".join(ar(s) for s in title) + r"\end{center}\vspace{-2mm}",
           r"\begin{center}" + p3_figure(rows) + r"\end{center}", r"\end{document}"]
    return "\n".join(out) + "\n"


def p2_document():
    rows = read("climates_p2.tsv")
    head = {r["side"]: r["text"] for r in rows if r["kind"] == "header"}
    title = [r["text"] for r in rows if r["kind"] == "title"]
    out = [PRE, r"\begin{document}",
           r"\noindent " + head["page"] + r"\hfill{\small " + head["head"] + r"}\hfill\mbox{}\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par",
           r"\begin{center}{\small " + head["fol"] + r"}\\[2mm]\textbf{" + r"\\".join(lat(s) for s in title) + r"}\end{center}\vspace{-3mm}",
           r"\begin{center}" + p2_figure(rows) + r"\end{center}", r"\end{document}"]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p3_climates.tex").write_text(p3_document(), encoding="utf-8")
    (HERE / "p2_climates.tex").write_text(p2_document(), encoding="utf-8")
    print("wrote p3_climates.tex, p2_climates.tex")

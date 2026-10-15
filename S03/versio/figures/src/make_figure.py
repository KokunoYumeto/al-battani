"""Write the TikZ file of a redrawn figure of the Latin translation from its measurements.

python make_figure.py NAME      reads NAME.json beside this script, writes ../NAME.tex

NAME.json holds the measurements in PDF points of the master page (y downward): "circles" (cx, cy, r and the
width w of the stroke), "segments" (x0, y0, x1, y1, w) and "labels" (the letter t and the box x0, y0, x1, y1 of its
printed ink); "origin" [X0, Y0] is the point of the page that becomes the upper left corner of the picture (the left
edge of the text block and the top of the first printed line beside the figure), "scale" the factor that brings the
printed line spacing to that of the edition, "size" [W, H] the box of the picture in points of the page, and
"label_pt" the size of the bold italic letters. The circles and the lines are least-squares fits to the printed
ink (_intake/latin/tools/fig_measure2.py). Optional:
  "hatch"  [{"circle": i, "segment": j, "away": [x, y], "step": S, "w": W}]: the part of circle i on the side of
           segment j away from the point [x, y], filled with horizontal lines S pt apart, W pt thick
  "arcs"   [{"cx", "cy", "r", "a0", "a1", "w", "dots": D}]: an arc from angle a0 to a1 (degrees, measured from the
           right toward the bottom of the page), dotted with dots D pt apart if "dots" is given
  "rings"  [{"cx", "cy", "r", "w", "dot": R}]: a small circle with a filled dot of radius R at its centre
  "words"  [{"t", "cx", "cy", "font", "rot"}]: a word set in the TeX font commands "font", turned through "rot"
           degrees, centred at (cx, cy)
  "groups" [{"w", "segs": [[x0, y0, x1, y1], ...], "cap", "comment"}]: many short strokes of one width (the ticks
           of a graduation, the dashes of a broken line), drawn eight to a command
  "fills"  [{"pts": [[x, y], ...], "name"}]: a small printed shape filled through its traced outline (a smooth
           closed curve through the points), for marks that are not lines, circles or letters
  "arcbraces" [{"cx", "cy", "r", "a0", "a1", "amp", "w", "name"}]: a curly brace along the arc of radius r from
           the angle a0 to a1 (degrees, as for "arcs"), its ends on the arc and its point "amp" pt outside it (a
           negative amp puts the point inside); drawn as a curve through computed points
  "ellipses" [{"cx", "cy", "rx", "ry", "w", "name"}]: an ellipse with axes parallel to the page (a circle printed
           a little wider than high)
  "braces" [{"x0", "y0", "x1", "y1", "amp", "w", "name"}]: a curly brace along the line from (x0, y0) to (x1, y1),
           its ends there and its point "amp" pt away, on the left of the direction of travel as seen on the page
           (from left to right: the point upward; from top to bottom: the point to the right)
  labels may give their centre as "cx", "cy" instead of the box, a turn "rot" (degrees), a "font" of their own and an
  "anchor" (base: the point is on the baseline of the letter, as for the letters of a word set along a curve)"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    name = sys.argv[1]
    d = json.loads((HERE / f"{name}.json").read_text(encoding="utf-8"))
    X0, Y0 = d["origin"]
    s = d["scale"]
    W, H = d["size"]

    def X(x):
        return f"{x - X0:.2f}"

    def Y(y):
        return f"{y - Y0:.2f}"

    out = ["% " + ln for ln in d["comment"]]
    out.append(r"\begin{tikzpicture}[x=" + f"{s:.4f}" + "pt,y=-" + f"{s:.4f}" + r"pt,line cap=butt,"
               r"every node/.style={font=\fontsize{" + f"{d['label_pt']}" + "}{" + f"{d['label_pt']}"
               + r"}\bfseries\itshape\selectfont,inner sep=0pt}]")
    out.append(r"\useasboundingbox (0,0) rectangle (" + f"{W:.2f},{H:.2f});")
    for h in d.get("hatch", []):
        c, g = d["circles"][h["circle"]], d["segments"][h["segment"]]
        ux, uy = g["x1"] - g["x0"], g["y1"] - g["y0"]
        L = math.hypot(ux, uy)
        ux, uy = ux / L, uy / L
        nx, ny = -uy, ux  # a normal of the segment, turned away from the point
        if (h["away"][0] - g["x0"]) * nx + (h["away"][1] - g["y0"]) * ny > 0:
            nx, ny = -nx, -ny
        e = c["r"] + 2
        a = (g["x0"] - e * ux, g["y0"] - e * uy)
        b = (g["x1"] + e * ux, g["y1"] + e * uy)
        f = 2 * c["r"] + 4
        out.append(r"\begin{scope}\clip (" + X(c["cx"]) + "," + Y(c["cy"]) + ") circle[radius="
                   + f"{c['r']:.2f}" + "];")
        out.append(r"\clip (" + X(a[0]) + "," + Y(a[1]) + ") -- (" + X(b[0]) + "," + Y(b[1]) + ") -- ("
                   + X(b[0] + f * nx) + "," + Y(b[1] + f * ny) + ") -- (" + X(a[0] + f * nx) + ","
                   + Y(a[1] + f * ny) + ") -- cycle;")
        y = c["cy"] - c["r"] + h["step"] / 2
        while y < c["cy"] + c["r"]:
            out.append(r"\draw[line width=" + f"{h['w'] * s:.2f}" + "pt] (" + X(c["cx"] - c["r"] - 1) + "," + Y(y)
                       + ") -- (" + X(c["cx"] + c["r"] + 1) + "," + Y(y) + ");")
            y += h["step"]
        out.append(r"\end{scope}")
    for c in d["circles"]:
        out.append(r"\draw[line width=" + f"{c['w'] * s:.2f}" + "pt] (" + X(c["cx"]) + "," + Y(c["cy"])
                   + ") circle[radius=" + f"{c['r']:.2f}" + "];  % " + c["name"])
    for e in d.get("ellipses", []):
        out.append(r"\draw[line width=" + f"{e['w'] * s:.2f}" + "pt] (" + X(e["cx"]) + "," + Y(e["cy"])
                   + ") ellipse[x radius=" + f"{e['rx']:.2f}" + ",y radius=" + f"{e['ry']:.2f}" + "];  % " + e["name"])
    for g in d["segments"]:
        out.append(r"\draw[line width=" + f"{g['w'] * s:.2f}" + "pt] (" + X(g["x0"]) + "," + Y(g["y0"]) + ") -- ("
                   + X(g["x1"]) + "," + Y(g["y1"]) + ");  % " + g["name"])
    for a in d.get("arcs", []):
        style = r"line width=" + f"{a['w'] * s:.2f}" + "pt"
        if a.get("dots"):
            style += r",line cap=round,dash pattern=on 0pt off " + f"{a['dots'] * s:.2f}" + "pt"
        x = a["cx"] + a["r"] * math.cos(math.radians(a["a0"]))
        y = a["cy"] + a["r"] * math.sin(math.radians(a["a0"]))
        out.append(r"\draw[" + style + "] (" + X(x) + "," + Y(y) + ") arc[start angle=" + f"{a['a0']:.2f}"
                   + ",end angle=" + f"{a['a1']:.2f}" + ",radius=" + f"{a['r']:.2f}" + "];")
    for r in d.get("rings", []):
        out.append(r"\draw[line width=" + f"{r['w'] * s:.2f}" + "pt] (" + X(r["cx"]) + "," + Y(r["cy"])
                   + ") circle[radius=" + f"{r['r']:.2f}" + "];")
        if r.get("dot"):
            out.append(r"\fill (" + X(r["cx"]) + "," + Y(r["cy"]) + ") circle[radius=" + f"{r['dot']:.2f}" + "];")
    for fl in d.get("fills", []):
        out.append(r"\fill plot[smooth cycle,tension=0.5] coordinates {" + " ".join(
            "(" + X(x) + "," + Y(y) + ")" for x, y in fl["pts"]) + "};  % " + fl["name"])
    for gr in d.get("groups", []):
        if gr.get("comment"):
            out.append("% " + gr["comment"])
        style = r"line width=" + f"{gr['w'] * s:.2f}" + "pt" + (",line cap=" + gr["cap"] if gr.get("cap") else "")
        segs = gr["segs"]
        for k in range(0, len(segs), 8):
            out.append(r"\draw[" + style + "] " + " ".join("(" + X(x0) + "," + Y(y0) + ")--(" + X(x1) + "," + Y(y1)
                                                          + ")" for x0, y0, x1, y1 in segs[k:k + 8]) + ";")
    for br in d.get("arcbraces", []):
        # the profile of a brace across its length t (0..1): the ends curl out to half the amplitude, the middle
        # rises to the point (as the brace decoration, but following the arc)
        L = abs(math.radians(br["a1"] - br["a0"])) * br["r"]
        c = min(0.22, 2.4 / max(L, 1e-6))
        amp = br["amp"]

        def prof(t):
            u = min(t, 1 - t)
            if u < c:
                return amp / 2 * math.sin(math.pi / 2 * u / c)
            if u < 0.5 - c:
                return amp / 2
            return amp / 2 + amp / 2 * (1 - math.cos(math.pi / 2 * (u - (0.5 - c)) / c))
        pts = []
        for k in range(121):
            t = k / 120
            a_ = math.radians(br["a0"] + (br["a1"] - br["a0"]) * t)
            rr = br["r"] + prof(t)
            pts.append((br["cx"] + rr * math.cos(a_), br["cy"] + rr * math.sin(a_)))
        out.append(r"\draw[line width=" + f"{br['w'] * s:.2f}" + "pt,line cap=round,line join=round] "
                   + " -- ".join("(" + X(x) + "," + Y(y) + ")" for x, y in pts) + ";  % " + br["name"])
    for br in d.get("braces", []):
        out.append(r"\draw[decorate,decoration={brace,amplitude=" + f"{br['amp'] * s:.2f}" + "pt},line width="
                   + f"{br['w'] * s:.2f}" + "pt] (" + X(br["x0"]) + "," + Y(br["y0"]) + ") -- (" + X(br["x1"]) + ","
                   + Y(br["y1"]) + ");  % " + br["name"])
    for lb in d["labels"]:
        if "cx" in lb:
            cx, cy = lb["cx"], lb["cy"]
        else:
            cx, cy = (lb["x0"] + lb["x1"]) / 2, (lb["y0"] + lb["y1"]) / 2
        opts = ([f"rotate={lb['rot']}"] if lb.get("rot") else []) + ([f"anchor={lb['anchor']}"] if lb.get("anchor") else [])
        rot = "[" + ",".join(opts) + "]" if opts else ""
        text = (r"\normalfont" + lb["font"] + " " + lb["t"]) if lb.get("font") else lb["t"]
        out.append(r"\node" + rot + " at (" + X(cx) + "," + Y(cy) + ") {" + text + "};")
    for wd in d.get("words", []):
        rot = f"[rotate={wd['rot']}]" if wd.get("rot") else ""
        out.append(r"\node" + rot + " at (" + X(wd["cx"]) + "," + Y(wd["cy"]) + r") {\normalfont" + wd["font"]
                   + " " + wd["t"] + "};")
    out.append(r"\end{tikzpicture}")
    (HERE.parent / f"{name}.tex").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {name}.tex: {len(d['circles'])} circles, {len(d['segments'])} lines, "
          f"{sum(len(g['segs']) for g in d.get('groups', []))} strokes in groups, {len(d['labels'])} letters, "
          f"{len(d.get('hatch', []))} hatched parts, {len(d.get('fills', []))} filled shapes, "
          f"{len(d.get('words', []))} words, {len(d.get('braces', [])) + len(d.get('arcbraces', []))} braces")


if __name__ == "__main__":
    main()

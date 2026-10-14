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
           degrees, centred at (cx, cy)"""
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
    for lb in d["labels"]:
        out.append(r"\node at (" + X((lb["x0"] + lb["x1"]) / 2) + "," + Y((lb["y0"] + lb["y1"]) / 2) + ") {"
                   + lb["t"] + "};")
    for wd in d.get("words", []):
        rot = f"[rotate={wd['rot']}]" if wd.get("rot") else ""
        out.append(r"\node" + rot + " at (" + X(wd["cx"]) + "," + Y(wd["cy"]) + r") {\normalfont" + wd["font"]
                   + " " + wd["t"] + "};")
    out.append(r"\end{tikzpicture}")
    (HERE.parent / f"{name}.tex").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {name}.tex: {len(d['circles'])} circles, {len(d['segments'])} lines, {len(d['labels'])} letters, "
          f"{len(d.get('hatch', []))} hatched parts, {len(d.get('words', []))} words")


if __name__ == "__main__":
    main()

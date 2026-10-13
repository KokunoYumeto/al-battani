"""Write the TikZ file of a redrawn figure of the Latin translation from its measurements.

python make_figure.py NAME      reads NAME.json beside this script, writes ../NAME.tex

NAME.json holds the measurements in PDF points of the master page (y downward): "circles" (cx, cy, r and the
width w of the stroke), "segments" (x0, y0, x1, y1, w) and "labels" (the letter t and the box x0, y0, x1, y1 of its
printed ink); "origin" [X0, Y0] is the point of the page that becomes the upper left corner of the picture (the left
edge of the text block and the top of the first printed line beside the figure), "scale" the factor that brings the
printed line spacing to that of the edition, "size" [W, H] the box of the picture in points of the page, and
"label_pt" the size of the bold italic letters. The circles and the lines are least-squares fits to the printed
ink (_intake/latin/tools/fig_measure2.py)."""
import json
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
    for c in d["circles"]:
        out.append(r"\draw[line width=" + f"{c['w'] * s:.2f}" + "pt] (" + X(c["cx"]) + "," + Y(c["cy"])
                   + ") circle[radius=" + f"{c['r']:.2f}" + "];  % " + c["name"])
    for g in d["segments"]:
        out.append(r"\draw[line width=" + f"{g['w'] * s:.2f}" + "pt] (" + X(g["x0"]) + "," + Y(g["y0"]) + ") -- ("
                   + X(g["x1"]) + "," + Y(g["y1"]) + ");  % " + g["name"])
    for lb in d["labels"]:
        out.append(r"\node at (" + X((lb["x0"] + lb["x1"]) / 2) + "," + Y((lb["y0"] + lb["y1"]) / 2) + ") {"
                   + lb["t"] + "};")
    out.append(r"\end{tikzpicture}")
    (HERE.parent / f"{name}.tex").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {name}.tex: {len(d['circles'])} circles, {len(d['segments'])} lines, {len(d['labels'])} letters")


if __name__ == "__main__":
    main()

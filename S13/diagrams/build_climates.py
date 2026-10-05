"""Write the TSV data of the diagram of the seven climes from the reading files in rows/:
  climates_p3.tsv        Part III p. 243 (the codex figure, Arabic)
  climates_p2.tsv        Part II p. 92 (Nallino's Latin figure)
  climates_names_p2.tsv  Nallino's table of the wind names, Part II p. 234
Columns of the two figure files: kind, t (line or label angle, degrees counterclockwise from the right-hand horizontal
of the page), r (radius in master pt, labels only), ring (1-7 from the inside; the line number for title and corner
texts), side (deg / min for cells, ccw / cw for the axes, TL TR BL BR for corners, page / head / fol for the header),
orient (labels), text, doubt."""
import csv, importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLS = ["kind", "t", "r", "ring", "side", "orient", "text", "doubt"]


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / "rows" / f"{name}.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def fmt(t):
    return f"{t:g}"


def figure_rows(m, arabic):
    out = []
    for side, text in m.HEADER.items():
        out.append({"kind": "header", "side": side, "text": text})
    for i, line in enumerate(m.TITLE, 1):
        out.append({"kind": "title", "ring": i, "text": line, "doubt": (getattr(m, "TITLE_DOUBT", None) or [""] * 9)[i - 1]})
    for pos, lines in m.CORNERS.items():
        for i, line in enumerate(lines, 1):
            out.append({"kind": "corner", "side": pos, "ring": i, "text": line})
    for lab in m.LABELS:
        if arabic:
            kind, t, r, orient, text, doubt = lab
            out.append({"kind": kind, "t": fmt(t), "r": r, "orient": orient, "text": text, "doubt": doubt})
        else:
            kind, t, text, doubt = lab
            out.append({"kind": kind, "t": fmt(t), "text": text, "doubt": doubt})
    for t in sorted(m.CELLS):
        for k, cell in enumerate(m.CELLS[t], 1):
            deg, mins = cell.split("|")
            doubts = getattr(m, "CELL_DOUBT", {})
            out.append({"kind": "cell", "t": fmt(t), "ring": k, "side": "deg", "text": deg, "doubt": doubts.get((t, k, "deg"), "")})
            out.append({"kind": "cell", "t": fmt(t), "ring": k, "side": "min", "text": mins, "doubt": doubts.get((t, k, "min"), "")})
    for t in sorted(m.AXES):
        for k, (ccw, cw) in enumerate(m.AXES[t], 1):
            doubts = getattr(m, "AXIS_DOUBT", {})
            out.append({"kind": "axis", "t": fmt(t), "ring": k, "side": "ccw", "text": ccw, "doubt": doubts.get((t, k, "ccw"), "")})
            out.append({"kind": "axis", "t": fmt(t), "ring": k, "side": "cw", "text": cw, "doubt": doubts.get((t, k, "cw"), "")})
    for t in sorted(m.WINDS):
        w = m.WINDS[t]
        text, doubt = w if isinstance(w, tuple) else (w, "")
        out.append({"kind": "wind", "t": fmt(t), "orient": "radial", "text": text, "doubt": doubt})
    return out


def write(name, rows, cols):
    with open(HERE / name, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})
    print(name, len(rows))


if __name__ == "__main__":
    p3, p2 = load("climates_p3"), load("climates_p2")
    write("climates_p3.tsv", figure_rows(p3, True), COLS)
    write("climates_p2.tsv", figure_rows(p2, False), COLS)
    write("climates_names_p2.tsv", [dict(zip(["az", "dir", "almagest", "codex", "restitution"], r)) for r in p2.NAMES_TABLE],
          ["az", "dir", "almagest", "codex", "restitution"])

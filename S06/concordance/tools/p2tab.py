"""Grid extraction for the numeric tables of Part II: tokens from p2num.read_region, arranged into rows (text lines)
and columns (clusters of token x-centres), with the OCR text layer of the same cell as a second reading.
grid(pdf, rect, ncols=None) -> {"cols": [x-centres], "rows": [{"y": .., "cells": [token or None per column]}]}
  token = {"text", "conf", "tl" (text-layer digits at that place or ""), "x0", "x1"}
Columns: x-centres of all tokens are clustered with a gap threshold; ncols, if given, must match.
CLI: python p2tab.py PDF x0 y0 x1 y1 [ncols]  prints the grid (low-confidence cells marked with *)."""
import sys
import numpy as np
import fitz
import p2num
import wide_kit as wk


def textlayer(page, rect):
    out = []
    for w in page.get_text("words"):
        x0, y0, x1, y1, t = w[:5]
        if fitz.Rect(x0, y0, x1, y1).intersects(rect):
            d = "".join(ch for ch in t if ch.isdigit())
            if d:
                out.append((x0, y0, x1, y1, d))
    return out


def grid(pdf, rect, ncols=None, gap=3.0, labels=None, vecs=None):
    page = wk.doc[pdf - 1]
    lines = [L for L in p2num.read_region(pdf, rect, labels, vecs) if L]
    xs = sorted((t["x0"] + t["x1"]) / 2 for L in lines for t in L)
    cols, cur = [], []
    for x in xs:
        if cur and x - cur[-1] > gap:
            cols.append(cur); cur = []
        cur.append(x)
    if cur:
        cols.append(cur)
    # keep clusters that occur in a good share of the lines
    centres = [float(np.median(c)) for c in cols if len(c) >= max(2, 0.25 * len(lines))]
    if ncols and len(centres) != ncols:
        print(f"warning: {len(centres)} columns found, {ncols} expected", file=sys.stderr)
    tl = textlayer(page, rect)
    rows = []
    for L in lines:
        cells = [None] * len(centres)
        for t in L:
            xc = (t["x0"] + t["x1"]) / 2
            j = int(np.argmin([abs(xc - c) for c in centres]))
            if abs(xc - centres[j]) > 6:
                continue
            tt = ""
            for (x0, y0, x1, y1, d) in tl:
                if x0 - 2 <= xc <= x1 + 2 and y0 - 3 <= t["y"] <= y1 + 3:
                    tt = d; break
            t = dict(t); t["tl"] = tt
            if cells[j] is None:
                cells[j] = t
            else:                                   # two tokens in one column: join them
                cells[j]["text"] += t["text"]; cells[j]["conf"] = min(cells[j]["conf"], t["conf"])
        rows.append({"y": L[0]["y"], "cells": cells})
    return {"cols": centres, "rows": rows}


def show(g, thr=0.75):
    print("columns:", [round(c, 1) for c in g["cols"]])
    for r in g["rows"]:
        out = []
        for c in r["cells"]:
            if c is None:
                out.append("-")
            else:
                flag = "*" if c["conf"] < thr or (c["tl"] and c["tl"] != c["text"]) else ""
                out.append(c["text"] + flag + (f"[{c['tl']}]" if flag and c["tl"] != c["text"] else ""))
        print(f"{r['y']:6.1f} " + " ".join(out))


if __name__ == "__main__":
    pdf = int(sys.argv[1]); x0, y0, x1, y1 = map(float, sys.argv[2:6])
    n = int(sys.argv[6]) if len(sys.argv) > 6 else None
    show(grid(pdf, fitz.Rect(x0, y0, x1, y1), n))

"""Column-wise reading of a Part II table page.
rules(pdf, y0, y1): x positions (pt) of the vertical rules crossing the band y0-y1 (long vertical ink runs).
read_cols(pdf, cols, y0, y1): cols = list of (name, x0, x1); each column strip is read with p2num.read_region;
  rows are aligned across columns by y (the first column with most lines gives the row grid).
  -> list of rows: {"y": .., name: token or None}; token = {"text", "conf", "x0", "x1", "masks", "ink"}
  where "ink" is the width (pt) of all ink in the strip at that row outside the digit token (for words or ditto marks).
CLI: python p2cols.py PDF y0 y1   prints the vertical rules."""
import sys
import numpy as np
import fitz
import p2num
import wide_kit as wk


def rules(pdf, y0, y1, dpi=300, minrun=40.0, maxw=3.2):
    """Vertical rules: pixel columns whose longest ink run (small gaps closed) is at least minrun pt, grouped into
    lines at most maxw pt wide; returns their x (pt)."""
    from scipy.ndimage import binary_closing
    page = wk.doc[pdf - 1]
    s = 72.0 / dpi
    a = np.array(wk.gray(page, dpi, fitz.Rect(0, y0, page.rect.width, y1))) < 170
    a = binary_closing(a, structure=np.ones((5, 1), bool))
    best = np.zeros(a.shape[1])
    for x in range(a.shape[1]):
        col = a[:, x]
        if not col.any():
            continue
        d = np.diff(np.r_[0, col.astype(int), 0])
        st, en = np.where(d == 1)[0], np.where(d == -1)[0]
        best[x] = (en - st).max() * s
    xs = np.where(best >= minrun)[0]
    out, cur = [], []
    for x in xs:
        if cur and x - cur[-1] > 1:
            out.append(cur); cur = []
        cur.append(x)
    if cur:
        out.append(cur)
    return [round(float(np.mean(c)) * s, 1) for c in out if len(c) * s <= maxw]


def rules_banded(pdf, y0, y1, band=110.0, need=0.5):
    """Skew-tolerant rules: detect in sub-bands of about `band` pt (minimum run 0.6 of the band) and keep the x
    positions found in at least `need` of the sub-bands (clustered within 2.5 pt)."""
    nb = max(1, int(round((y1 - y0) / band)))
    edges = np.linspace(y0, y1, nb + 1)
    found = []
    for a, b in zip(edges[:-1], edges[1:]):
        found.append(rules(pdf, a, b, minrun=0.6 * (b - a)))
    xs = sorted(x for f in found for x in f)
    groups, cur = [], []
    for x in xs:
        if cur and x - cur[-1] > 2.5:
            groups.append(cur); cur = []
        cur.append(x)
    if cur:
        groups.append(cur)
    return [round(float(np.mean(g)), 1) for g in groups if len(g) >= need * nb]


def read_cols(pdf, cols, y0, y1, labels=None, vecs=None):
    if labels is None:
        labels, vecs = p2num.load_templates()
    per = {}
    for name, x0, x1 in cols:
        lines = p2num.read_region(pdf, fitz.Rect(x0, y0, x1, y1), labels, vecs)
        per[name] = [L for L in lines if L]
    # row grid: the union of line y positions, merged within 3 pt
    ys = sorted(L[0]["y"] for v in per.values() for L in v)
    grid = []
    for y in ys:
        if grid and y - grid[-1][-1] < 3.0:
            grid[-1].append(y)
        else:
            grid.append([y])
    rows = [{"y": float(np.mean(g))} for g in grid]
    for name, lines in per.items():
        for L in lines:
            r = min(rows, key=lambda r: abs(r["y"] - L[0]["y"]))
            toks = sorted(L, key=lambda t: t["x0"])
            # the digit token: the first token (numbers stand at the left of a name column)
            r[name] = toks[0]
            r[name + "_rest"] = toks[1:]
    return rows


if __name__ == "__main__":
    pdf = int(sys.argv[1]); y0, y1 = float(sys.argv[2]), float(sys.argv[3])
    print(rules(pdf, y0, y1))

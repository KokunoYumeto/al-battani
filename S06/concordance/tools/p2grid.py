"""Read a ruled numeric table of Part II column by column: the column strips between the detected rules are read
with the glyph reader (p2num) and the OCR text layer; rows are formed by clustering the line positions of all
columns. Returns rows of cells {text, conf, tl, x0, x1, masks} (None where a column has nothing on that row).
grid(pdf, y0, y1, rules=None, inset=1.5) -> (rules, rows)  rows = [{"y": .., "cells": [cell|None per column]}]"""
import numpy as np
import fitz
import p2num, p2cols
import wide_kit as wk


def textlayer(page):
    out = []
    for w in page.get_text("words"):
        d = "".join(ch for ch in w[4] if ch.isdigit())
        if d:
            out.append((w[0], w[1], w[2], w[3], d))
    return out


def grid(pdf, y0, y1, rules=None, inset=1.5, labels=None, vecs=None, merge=3.0):
    page = wk.doc[pdf - 1]
    if rules is None:
        rules = p2cols.rules_banded(pdf, y0, y1)
    if labels is None:
        labels, vecs = p2num.load_templates()
    tl = textlayer(page)
    cols = []
    for a, b in zip(rules[:-1], rules[1:]):
        lines = [L for L in p2num.read_region(pdf, fitz.Rect(a + inset, y0, b - inset, y1), labels, vecs) if L]
        cols.append(lines)
    ys = sorted(L[0]["y"] for c in cols for L in c)
    groups = []
    for y in ys:
        if groups and y - groups[-1][-1] < merge:
            groups[-1].append(y)
        else:
            groups.append([y])
    rows = [{"y": float(np.mean(g)), "cells": [None] * len(cols)} for g in groups]
    for j, lines in enumerate(cols):
        for L in lines:
            r = min(rows, key=lambda r: abs(r["y"] - L[0]["y"]))
            toks = sorted(L, key=lambda t: t["x0"])
            cell = dict(toks[0])
            for t in toks[1:]:
                cell["text"] += t["text"]; cell["conf"] = min(cell["conf"], t["conf"]); cell["x1"] = t["x1"]
                cell["masks"] = cell.get("masks", []) + t.get("masks", [])
            xc = (cell["x0"] + cell["x1"]) / 2
            cell["tl"] = ""
            for (a0, b0, a1, b1, d) in tl:
                if a0 - 2 <= xc <= a1 + 2 and b0 - 3 <= cell["y"] <= b1 + 3:
                    cell["tl"] = d; break
            r["cells"][j] = cell
    return rules, rows

"""Read and check a Hijra-Seleucid conversion page of Part II (Tabulae I-X, pp. 9-18): two halves of 30 rows,
columns: Hijra year, weekday sign of 1 Muharram, Seleucid (Dhu 'l-qarnayn) year, day of the Syrian month in which
1 Muharram falls and the month name (printed when it changes, otherwise a ditto mark »).
Expected values from calendars.py: arithmetical Hijra calendar with the astronomical epoch (Thursday 15 July 622),
weekday signs 1 = Sunday, the Seleucid year changing at Aylul (September), as the column order of p. 8 shows.
Usage: python p2cal.py PDF FIRST_AH y0 y1   -> prints mismatches; writes p3_kit/CAL{PDF}.json with the rows."""
import sys, json
import fitz
import numpy as np
import p2cols, p2num, calendars as C
import wide_kit as wk


def expected(n):
    jd = C.hijra_year_start(n)
    y, m, d = C.julian_from_jd(jd)
    sy = y + 312 if m >= 9 else y + 311
    return {"ah": n, "wd": C.weekday_sign(jd), "sy": sy, "day": d, "month": C.SYRIAN[m]}


def run(pdf, first, y0, y1, xmid=None, x0=None, x1=None, train=False):
    """Each half of the table is read as one region; a line's tokens in x order are: Hijra year, weekday sign,
    Seleucid year, day, then the glyphs of a month name if one is printed (a ditto mark is too small to be a token)."""
    page = wk.doc[pdf - 1]
    r = p2cols.rules_banded(pdf, y0, y1)
    # the middle rule has the wide day-and-month column (about 86 pt) on its left and a narrow one on its right
    mi = next(i for i in range(4, len(r) - 4) if 70 < r[i] - r[i - 1] < 100 and 30 < r[i + 1] - r[i] < 55)
    x0 = r[mi - 4] + 1.5 if x0 is None else x0
    x1 = r[mi + 4] - 1.5 if x1 is None else x1
    xmid = r[mi] if xmid is None else xmid
    labels, vecs = p2num.load_templates()
    tl = []
    for w in page.get_text("words"):
        d = "".join(ch for ch in w[4] if ch.isdigit())
        if d:
            tl.append((w[0], w[1], w[2], w[3], d))

    def tlayer(t):
        xc = (t["x0"] + t["x1"]) / 2
        for (a0, b0, a1, b1, d) in tl:
            if a0 - 2 <= xc <= a1 + 2 and b0 - 3 <= t["y"] <= b1 + 3:
                return d
        return ""
    out, bad = [], []
    for half, a, b, base in (("L", x0, xmid - 2, first), ("R", xmid + 2, x1, first + 30)):
        lines = [L for L in p2num.read_region(pdf, fitz.Rect(a, y0, b, y1), labels, vecs) if L]
        lines = [L for L in lines if len(L) >= 3]           # data lines have at least year, sign, year
        # column centres from lines with exactly four tokens (no month name, no split)
        four = [sorted(L, key=lambda t: t["x0"]) for L in lines if len(L) == 4]
        centres = [float(np.median([(T[j]["x0"] + T[j]["x1"]) / 2 for T in four])) for j in range(4)]
        prev_month = None
        for i, L in enumerate(lines):
            cells = {k: None for k in ("ah", "wd", "sy", "dm")}
            name_ink = 0.0
            for t in sorted(L, key=lambda t: t["x0"]):
                xc = (t["x0"] + t["x1"]) / 2
                j = int(np.argmin([abs(xc - c) for c in centres]))
                k = ("ah", "wd", "sy", "dm")[j]
                if k == "dm" and t["x0"] > centres[3] + 6:   # right of the day number: month name glyphs
                    name_ink += t["x1"] - t["x0"]; continue
                if abs(xc - centres[j]) > 9:
                    name_ink += t["x1"] - t["x0"]; continue
                if cells[k] is None:
                    cells[k] = dict(t)
                else:                                          # a number split into two tokens
                    cells[k]["text"] += t["text"]; cells[k]["conf"] = min(cells[k]["conf"], t["conf"])
                    cells[k]["x1"] = t["x1"]
            e = expected(base + i)
            show_name = e["month"] != prev_month
            prev_month = e["month"]
            got = {k: (c["text"] if c else None) for k, c in cells.items()}
            alt = {k: (tlayer(c) if c else "") for k, c in cells.items()}
            conf = {k: (c["conf"] if c else None) for k, c in cells.items()}
            name_printed = name_ink > 8.0
            masks = {k: (c.get("masks") if c else None) for k, c in cells.items()}
            out.append({"half": half, "row": i + 1, "y": L[0]["y"], "read": got, "alt": alt, "conf": conf, "masks": masks,
                        "name_printed": name_printed, "name_ink": round(name_ink, 1), "expected": e,
                        "show_name": show_name, "cells": {k: (c["x0"], c["x1"]) if c else None for k, c in cells.items()}})
            for k, ek in (("ah", "ah"), ("wd", "wd"), ("sy", "sy"), ("dm", "day")):
                if got[k] != str(e[ek]) and alt[k] != str(e[ek]):
                    bad.append((half, i + 1, k, got[k], e[ek], conf[k], alt[k]))
            if name_printed != show_name:
                bad.append((half, i + 1, "name", f"ink {name_ink:.1f}", e["month"] if show_name else "»", None, ""))
        if len(lines) != 30:
            bad.append((half, None, "rows", len(lines), 30, None, ""))
    if train:
        pairs = []
        for r in out:
            for k, ek in (("ah", "ah"), ("wd", "wd"), ("sy", "sy"), ("dm", "day")):
                exp = str(r["expected"][ek])
                if r["masks"][k] and (r["read"][k] == exp or r["alt"][k] == exp):
                    pairs.append(({"text": r["read"][k], "conf": r["conf"][k], "masks": r["masks"][k]}, exp))
        n = p2num.learn_from(pairs, labels, vecs, per_digit=150)
        p2num.save_templates(labels, vecs)
        print("templates added:", n)
    for r in out:
        r.pop("masks", None)
    json.dump({"pdf": pdf, "xmid": xmid, "x0": x0, "x1": x1, "rows": out, "bad": bad}, open(wk.OUT + f"CAL{pdf}.json", "w", encoding="utf-8"),
              ensure_ascii=False, default=str)
    return out, bad


if __name__ == "__main__":
    pdf, first = int(sys.argv[1]), int(sys.argv[2])
    y0, y1 = float(sys.argv[3]), float(sys.argv[4])
    out, bad = run(pdf, first, y0, y1, train="--train" in sys.argv)
    print(f"rows {len(out)}, mismatches {len(bad)}")
    for b in bad:
        print("  ", b)

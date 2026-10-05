"""Digit reader for the numeric tables of Nallino's Part II (Western numerals in one typeface).
Pipeline for a page region:
  1. render at DPI, binarize, drop rules (long thin components) and specks;
  2. glyph components -> text lines (by vertical overlap) -> tokens (by horizontal gaps);
  3. classify each digit glyph by nearest template (normalized correlation on a 24x32 grid, aspect ratio kept);
     templates are bootstrapped from the page's own OCR text layer (tokens whose glyph count equals the length of
     the text-layer number at the same place) and stored in p2num_templates.npz for later pages;
  4. marks: a small raised glyph after a number is ° ′ or ″ (kept as a flag, not classified further).
Usage as a module: read_region(pdf, rect_pt) -> list of lines, each a list of tokens
  {x0, x1, y, text, conf, glyphs}; conf = lowest digit score in the token.
CLI: python p2num.py PDF x0 y0 x1 y1 [--learn] prints the lines."""
import sys, os, json
import numpy as np
import fitz
from scipy import ndimage
import wide_kit as wk

DPI = 400
S = 72.0 / DPI
HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, "p2num_templates.npz")
GW, GH = 24, 32


def norm_glyph(m):
    """Binary glyph -> GHxGW float image, scaled to the glyph height, centred, aspect kept."""
    ys, xs = np.nonzero(m)
    m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1].astype(float)
    h, w = m.shape
    sc = GH / h
    nw = max(1, min(GW, int(round(w * sc))))
    zy = np.linspace(0, h - 1, GH); zx = np.linspace(0, w - 1, nw)
    g = ndimage.map_coordinates(m, np.meshgrid(zy, zx, indexing="ij"), order=1)
    out = np.zeros((GH, GW)); off = (GW - nw) // 2
    out[:, off:off + nw] = g
    v = out - out.mean()
    n = np.linalg.norm(v)
    return v / n if n else v


def components(page, rect):
    im = np.array(wk.gray(page, DPI, rect), dtype=np.uint8)
    a = im < 150
    lab, k = ndimage.label(a)
    objs = ndimage.find_objects(lab)
    comps = []
    for i, sl in enumerate(objs, 1):
        if sl is None:
            continue
        h = (sl[0].stop - sl[0].start) * S; w = (sl[1].stop - sl[1].start) * S
        m = lab[sl] == i
        area = m.sum() * S * S
        if area < 0.25:                      # specks
            continue
        if (w > 25 and h < 2.5) or (h > 12 and w < 2.5) or w < 0.45:   # rules and their edge fragments
            continue
        comps.append({"x0": rect.x0 + sl[1].start * S, "x1": rect.x0 + sl[1].stop * S,
                      "y0": rect.y0 + sl[0].start * S, "y1": rect.y0 + sl[0].stop * S, "m": m, "area": area})
    return comps


def merge_pieces(comps, frac=0.45):
    """Broken type: pieces of one digit (the hook and the bowl of a 6 or a 9) overlap horizontally; two adjacent
    digits do not. Merge components whose x-overlap is at least frac of the narrower one and whose vertical spans
    lie within one digit height (both pieces between the line's top and bottom)."""
    comps = sorted(comps, key=lambda c: c["x0"])
    out = []
    for c in comps:
        merged = False
        for o in out[-3:]:
            ov = min(o["x1"], c["x1"]) - max(o["x0"], c["x0"])
            if ov <= 0 or ov < frac * min(o["x1"] - o["x0"], c["x1"] - c["x0"]):
                continue
            top, bot = min(o["y0"], c["y0"]), max(o["y1"], c["y1"])
            if bot - top > 9.0 or abs((o["y0"] + o["y1"]) / 2 - (c["y0"] + c["y1"]) / 2) > 6.0:
                continue
            x0, x1 = min(o["x0"], c["x0"]), max(o["x1"], c["x1"])
            H = int(round((bot - top) / S)) + 1; W = int(round((x1 - x0) / S)) + 1
            m = np.zeros((H, W), bool)
            for q in (o, c):
                oy = int(round((q["y0"] - top) / S)); ox = int(round((q["x0"] - x0) / S))
                h, w = q["m"].shape
                m[oy:oy + h, ox:ox + w] |= q["m"][:H - oy, :W - ox]
            o.update({"x0": x0, "x1": x1, "y0": top, "y1": bot, "m": m, "area": o["area"] + c["area"]})
            merged = True
            break
        if not merged:
            out.append(dict(c))
    return out


def split_wide(comps, wd):
    """A digit-height component wider than 1.6 digit widths is two or more touching digits: cut it at the lowest
    column sums into round(width / wd) parts."""
    out = []
    for c in comps:
        w = c["x1"] - c["x0"]; h = c["y1"] - c["y0"]
        if h >= 4.0 and w > 1.6 * wd:
            k = max(2, int(round(w / wd)))
            col = c["m"].sum(axis=0).astype(float)
            cuts, n = [], c["m"].shape[1]
            for j in range(1, k):
                centre = int(j * n / k); lo = max(1, centre - n // (3 * k)); hi = min(n - 1, centre + n // (3 * k))
                cuts.append(lo + int(np.argmin(col[lo:hi])) if hi > lo else centre)
            edges = [0] + cuts + [n]
            for a, b in zip(edges[:-1], edges[1:]):
                part = c["m"][:, a:b]
                if part.sum() == 0:
                    continue
                ys = np.nonzero(part.any(axis=1))[0]
                out.append({"x0": c["x0"] + a * S, "x1": c["x0"] + b * S, "y0": c["y0"] + ys.min() * S,
                            "y1": c["y0"] + (ys.max() + 1) * S, "m": part[ys.min():ys.max() + 1], "area": part.sum() * S * S,
                            "split": True})
        else:
            out.append(c)
    return out


def digit_width(comps):
    """Typical width of a single digit: the 80th percentile of digit-height glyphs narrower than 7 pt (the median
    is pulled down by the narrow 1)."""
    ws = [c["x1"] - c["x0"] for c in comps if c["y1"] - c["y0"] >= 4.0 and c["x1"] - c["x0"] < 7.0]
    return float(np.percentile(ws, 80)) if ws else 4.5


def lines_of(comps, hmin=4.0):
    """Digit-sized glyphs define the lines; smaller glyphs (marks) attach to the nearest line."""
    big = [c for c in comps if c["y1"] - c["y0"] >= hmin]
    big.sort(key=lambda c: (c["y0"] + c["y1"]) / 2)
    lines = []
    for c in big:
        yc = (c["y0"] + c["y1"]) / 2
        if lines and abs(yc - lines[-1]["yc"]) < 3.0:
            L = lines[-1]; L["g"].append(c); L["yc"] = np.mean([(g["y0"] + g["y1"]) / 2 for g in L["g"]])
        else:
            lines.append({"yc": yc, "g": [c]})
    for c in comps:
        if c["y1"] - c["y0"] >= hmin or not lines:
            continue
        L = min(lines, key=lambda L: abs((c["y0"] + c["y1"]) / 2 - L["yc"]))
        if abs((c["y0"] + c["y1"]) / 2 - L["yc"]) < 6:
            L.setdefault("marks", []).append(c)
    return lines


def tokens_of(line, gap=2.2):
    g = sorted(line["g"], key=lambda c: c["x0"])
    toks = []
    for c in g:
        if toks and c["x0"] - toks[-1][-1]["x1"] < gap:
            toks[-1].append(c)
        else:
            toks.append([c])
    return toks


def load_templates():
    if os.path.exists(TPL):
        d = np.load(TPL)
        return list(d["labels"]), list(d["vecs"])
    return [], []


def save_templates(labels, vecs):
    np.savez(TPL, labels=np.array(labels), vecs=np.array(vecs))


def classify(m, labels, vecs):
    v = norm_glyph(m).ravel()
    if not vecs:
        return "?", 0.0
    sims = np.array(vecs).reshape(len(vecs), -1) @ v
    i = int(np.argmax(sims))
    return labels[i], float(sims[i])


def textlayer_tokens(page, rect):
    out = []
    for w in page.get_text("words"):
        x0, y0, x1, y1, t = w[:5]
        if fitz.Rect(x0, y0, x1, y1).intersects(rect):
            t2 = "".join(ch for ch in t if ch.isdigit())
            if t2:
                out.append((x0, y0, x1, y1, t2))
    return out


def learn(page, rect, labels, vecs, per_digit=12):
    """Bootstrap: a glyph token whose box overlaps a text-layer number with the same digit count gets those labels."""
    comps = components(page, rect)
    tl = textlayer_tokens(page, rect)
    count = {d: labels.count(d) for d in "0123456789"}
    added = 0
    comps = split_wide(comps, digit_width(comps))
    for L in lines_of(comps):
        for tok in tokens_of(L):
            tx0, tx1 = tok[0]["x0"], tok[-1]["x1"]; ty = L["yc"]
            best = None
            for (x0, y0, x1, y1, t) in tl:
                if x0 - 1.5 <= tx0 and tx1 <= x1 + 1.5 + 6 and y0 - 2 <= ty <= y1 + 2:
                    best = t; break
            if best is None:
                continue
            digits = [c for c in tok if c["y1"] - c["y0"] >= 4.0]
            if len(digits) != len(best):
                continue
            for c, d in zip(digits, best):
                if count.get(d, 0) < per_digit:
                    labels.append(d); vecs.append(norm_glyph(c["m"]).ravel()); count[d] = count.get(d, 0) + 1; added += 1
    return added


def learn_from(cells_truth, labels, vecs, per_digit=60):
    """Self-training: (token, true digit string) pairs from checked cells; a token whose glyph count equals the length
    of the true string adds its glyphs as templates where the reader was wrong or unsure, up to per_digit each."""
    count = {d: labels.count(d) for d in "0123456789"}
    added = 0
    for tok, truth in cells_truth:
        if tok is None or len(tok.get("masks", [])) != len(truth):
            continue
        if tok["text"] == truth and tok["conf"] >= 0.85:
            continue
        for m, d in zip(tok["masks"], truth):
            if count.get(d, 0) < per_digit:
                labels.append(d); vecs.append(norm_glyph(m).ravel()); count[d] = count.get(d, 0) + 1; added += 1
    return added


def read_region(pdf, rect, labels=None, vecs=None):
    page = wk.doc[pdf - 1]
    if labels is None:
        labels, vecs = load_templates()
    out = []
    comps = components(page, rect)                       # merge_pieces() is not used: it merged kerned digits
    comps = split_wide(comps, digit_width(comps))
    for L in lines_of(comps):
        line = []
        for tok in tokens_of(L):
            txt, conf, masks = "", 1.0, []
            for c in tok:
                if c["y1"] - c["y0"] < 4.0:
                    continue                                  # marks inside a token (a degree sign) are not digits
                d, s = classify(c["m"], labels, vecs)
                txt += d; conf = min(conf, s); masks.append(c["m"])
            line.append({"x0": round(tok[0]["x0"], 1), "x1": round(tok[-1]["x1"], 1), "y": round(L["yc"], 1),
                         "text": txt, "conf": round(conf, 3), "masks": masks})
        out.append(line)
    return out


if __name__ == "__main__":
    pdf = int(sys.argv[1]); x0, y0, x1, y1 = map(float, sys.argv[2:6])
    rect = fitz.Rect(x0, y0, x1, y1)
    labels, vecs = load_templates()
    if "--learn" in sys.argv:
        n = learn(wk.doc[pdf - 1], rect, labels, vecs)
        save_templates(labels, vecs)
        print("templates added", n, "| per digit", {d: labels.count(d) for d in "0123456789"})
    for line in read_region(pdf, rect, labels, vecs):
        print(line[0]["y"] if line else "", " ".join(f"{t['text']}({t['conf']:.2f})" for t in line))

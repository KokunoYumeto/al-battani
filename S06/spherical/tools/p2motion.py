"""Read and check a mean-motion page of Part II: an argument column and motion columns, each motion column holding
degrees, minutes, seconds (or more places) as separate numbers.
read(pdf, y0, y1, rules, nsub=3) -> rows (nsub: places per column, or a list per column) [{"y", "arg": cell, "groups": [[cell per place] per motion column]}]
  cell = {"text", "conf", "tl", "x0", "x1", "y"} or None
fit(rows, tvals, gi, places, mod) -> (values, flags, (a, b)): for motion column gi, the reading of each row closest
  to the line a + b*t (mod `mod` in the smallest unit) among the candidates of the two readers; the line is fitted on
  the rows where both readers agree with high confidence (unwrapped about the median step); a row whose best
  candidate is more than TOL units from the line is flagged."""
import itertools
import numpy as np
import fitz
import p2num
import wide_kit as wk

TOL = 2


def textlayer(page):
    out = []
    for w in page.get_text("words"):
        d = "".join(ch for ch in w[4] if ch.isdigit())
        if d:
            out.append((w[0], w[1], w[2], w[3], d))
    return out


def attach_tl(cell, tl):
    xc = (cell["x0"] + cell["x1"]) / 2
    cell["tl"] = ""
    for (a0, b0, a1, b1, d) in tl:
        if a0 - 1.5 <= xc <= a1 + 1.5 and b0 - 3 <= cell["y"] <= b1 + 3:
            cell["tl"] = d
            break
    return cell


def read(pdf, y0, y1, rules, nsub=3, inset=1.5, merge=3.0, labels=None, vecs=None):
    page = wk.doc[pdf - 1]
    if labels is None:
        labels, vecs = p2num.load_templates()
    tl = textlayer(page)
    cols = []
    for k, (a, b) in enumerate(zip(rules[:-1], rules[1:])):
        lines = [L for L in p2num.read_region(pdf, fitz.Rect(a + inset, y0, b - inset, y1), labels, vecs) if L]
        cols.append(lines)
    ys = sorted(L[0]["y"] for c in cols for L in c)
    groups = []
    for y in ys:
        if groups and y - groups[-1][-1] < merge:
            groups[-1].append(y)
        else:
            groups.append([y])
    ns = [nsub[k] if isinstance(nsub, (list, tuple)) else nsub for k in range(len(cols) - 1)]   # places per column
    rows = [{"y": float(np.mean(g)), "arg": None, "groups": [[None] * ns[k] for k in range(len(cols) - 1)]} for g in groups]
    # argument column: the joined tokens of a line
    for L in cols[0]:
        r = min(rows, key=lambda r: abs(r["y"] - L[0]["y"]))
        toks = sorted(L, key=lambda t: t["x0"])
        c = dict(toks[0])
        for t in toks[1:]:
            c["text"] += t["text"]; c["conf"] = min(c["conf"], t["conf"]); c["x1"] = t["x1"]
        r["arg"] = attach_tl(c, tl)
    # motion columns: place centres from lines with exactly nsub tokens
    for gi, lines in enumerate(cols[1:]):
        full = [sorted(L, key=lambda t: t["x0"]) for L in lines if len(L) == ns[gi]]
        if not full:
            continue
        centres = [float(np.median([(T[j]["x0"] + T[j]["x1"]) / 2 for T in full])) for j in range(ns[gi])]
        for L in lines:
            r = min(rows, key=lambda r: abs(r["y"] - L[0]["y"]))
            for t in sorted(L, key=lambda t: t["x0"]):
                xc = (t["x0"] + t["x1"]) / 2
                j = int(np.argmin([abs(xc - c) for c in centres]))
                cell = r["groups"][gi][j]
                if cell is None:
                    r["groups"][gi][j] = attach_tl(dict(t), tl)
                else:
                    cell["text"] += t["text"]; cell["conf"] = min(cell["conf"], t["conf"]); cell["x1"] = t["x1"]
    return rows


def cands(cell):
    out = []
    if cell is None:
        return out
    for t in (cell["text"], cell.get("tl", "")):
        if t and t.isdigit() and int(t) not in out:
            out.append(int(t))
    return out


def sure(cell, thr=0.85):
    return cell is not None and cell["conf"] >= thr and (not cell.get("tl") or cell["tl"] == cell["text"])


def units(vals):
    u = 0
    for v in vals:
        u = u * 60 + v
    return u


def fit(rows, tvals, gi, places=3, mod_deg=360, rate=None, fixed=None):
    """fixed=(a, b): use the line a + b*t as given (for short tables whose line is known exactly)."""
    MOD = mod_deg * 60 ** (places - 1)
    if fixed is not None:
        return match(rows, tvals, gi, MOD, mod_deg, *fixed)
    pts = [(i, units([int(c["text"]) for c in r["groups"][gi]])) for i, r in enumerate(rows)
           if all(sure(c) for c in r["groups"][gi])]
    if len(pts) < 3:
        return None, [("fit", gi, "too few sure rows")], None
    # rough rate: the given one, or the median of the steps between consecutive sure points
    steps = []
    for (ia, ua), (ib, ub) in zip(pts[:-1], pts[1:]):
        dt = tvals[ib] - tvals[ia]
        if dt:
            steps.append(((ub - ua) % MOD) / dt)
    b = rate if rate is not None else float(np.median(steps))
    # robust intercept: circular median of the residuals; then least squares on the inliers (within 30 units)
    res = np.array([((u - b * tvals[i]) % MOD) for i, u in pts], float)
    ref = res[0]
    centred = ((res - ref + MOD / 2) % MOD) - MOD / 2
    a = ref + float(np.median(centred))
    for _ in range(2):
        xs, ys = [], []
        for i, u in pts:
            pred = a + b * tvals[i]
            d = ((u - pred + MOD / 2) % MOD) - MOD / 2
            if abs(d) <= 30:
                xs.append(tvals[i]); ys.append(pred + d)
        if len(xs) >= 3 and len(set(xs)) >= 2:
            b, a = np.polyfit(xs, ys, 1)
    return match(rows, tvals, gi, MOD, mod_deg, a, b)


def match(rows, tvals, gi, MOD, mod_deg, a, b):
    values, flags = [], []
    for i, r in enumerate(rows):
        pred = (a + b * tvals[i]) % MOD
        cs = [cands(c) for c in r["groups"][gi]]
        best = None
        for combo in itertools.product(*[c or [None] for c in cs]):
            if None in combo or combo[0] >= mod_deg or any(v >= 60 for v in combo[1:]):
                continue
            u = units(list(combo))
            e = abs(((u - pred + MOD / 2) % MOD) - MOD / 2)
            if best is None or e < best[0]:
                best = (e, combo)
        if best is not None and best[0] <= TOL:
            values.append(best[1])
        else:
            values.append(None)
            flags.append((i, gi, f"predicted {pred:.1f}; read {cs}"))
    return values, flags, (a, b)

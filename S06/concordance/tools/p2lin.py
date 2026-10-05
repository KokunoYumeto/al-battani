"""Resolve and check a linear (mean-motion) table of Part II read by p2tab.grid.
Each motion column group (degrees, minutes, seconds[, thirds]) grows by a constant step per row, modulo 360 degrees.
For every row and group the candidate readings (glyph reader and OCR text layer, per cell) are combined; the
combination closest to the fitted line is taken if it lies within TOL seconds, otherwise the cell group is flagged.
The fit uses rows where both readers agree with high confidence: the step is the median of their first
differences (mod 360 degrees), the offset the median residual.
resolve(g, groups, arg_col=None, arg=None) -> (values, flags)
  groups: list of column-index tuples, e.g. [(1,2,3),(4,5,6)]; arg_col/arg: the argument column and a function
  row_index -> expected argument (checked exactly).
  values[r][gi] = (d, m, s[, t]) or None; flags = list of (row, group or 'arg', reason)."""
import itertools
import numpy as np

TOL = 2          # seconds (or thirds for four-place groups)
FULL = 360 * 3600


def cand(cell):
    if cell is None:
        return []
    c = []
    for t in (cell["text"], cell.get("tl", "")):
        if t and t.isdigit() and int(t) not in c:
            c.append(int(t))
    return c


def good(cell, thr=0.85):
    return cell is not None and cell["conf"] >= thr and (not cell.get("tl") or cell["tl"] == cell["text"])


def to_units(vals, places):
    d, m, s = vals[0], vals[1], vals[2]
    u = (d * 60 + m) * 60 + s
    if places == 4:
        u = u * 60 + vals[3]
    return u


def resolve(g, groups, arg_col=None, arg=None, tol=TOL):
    rows = [r for r in g["rows"] if any(c is not None for c in r["cells"])]
    values = [[None] * len(groups) for _ in rows]
    flags = []
    if arg_col is not None and arg is not None:
        for i, r in enumerate(rows):
            if arg(i) not in cand(r["cells"][arg_col]):
                flags.append((i, "arg", f"expected {arg(i)}, read {cand(r['cells'][arg_col])}"))
    for gi, cols in enumerate(groups):
        places = len(cols)
        full = FULL * (60 if places == 4 else 1)
        # sure rows: both readers agree with high confidence in every cell of the group
        sure = {}
        for i, r in enumerate(rows):
            cells = [r["cells"][j] for j in cols]
            if all(good(c) for c in cells):
                sure[i] = to_units([int(c["text"]) for c in cells], places)
        idx = sorted(sure)
        adj = [((sure[b] - sure[a]) % full) for a, b in zip(idx[:-1], idx[1:]) if b - a == 1]
        if not adj:
            flags.append((None, gi, "no adjacent sure rows")); continue
        step0 = float(np.median(adj))
        # unwrap the sure values around the rough line, then fit the line by least squares
        base = sure[idx[0]]
        xs, ys = [], []
        for i in idx:
            approx = base + step0 * (i - idx[0])
            n = round((approx - sure[i]) / full)
            xs.append(i); ys.append(sure[i] + n * full)
        if len(xs) >= 2:
            step, off = np.polyfit(xs, ys, 1)
        else:
            step, off = step0, base - step0 * idx[0]
        for i, r in enumerate(rows):
            pred = (off + step * i) % full
            cs = [cand(r["cells"][j]) for j in cols]
            best = None
            for combo in itertools.product(*[c or [None] for c in cs]):
                if None in combo:
                    continue
                if combo[1] >= 60 or combo[2] >= 60 or (places == 4 and combo[3] >= 60) or combo[0] >= 360:
                    continue
                u = to_units(list(combo), places)
                e = abs(((u - pred + full / 2) % full) - full / 2)
                if best is None or e < best[0]:
                    best = (e, combo)
            if best is not None and best[0] <= tol:
                values[i][gi] = best[1]
            else:
                flags.append((i, gi, f"predicted {fmt(pred, places)}; read {cs}"))
    return rows, values, flags


def fmt(u, places):
    u = int(round(u))
    if places == 4:
        t = u % 60; u //= 60
    s = u % 60; u //= 60
    m = u % 60; d = u // 60
    return f"{d}°{m}'{s}\"" + (f"{t}'''" if places == 4 else "")

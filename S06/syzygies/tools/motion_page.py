"""Read, fit and classify one mean-motion page of Part II (see p2motion.py).
run(pdf, y0, y1, rules, tvals, args=None, nsub=3, tag="", keep=None, rates=None, mods=None) -> dict saved as
  p3_kit/MP{pdf}{tag}.json (mods: the modulus of each motion column in its first place, default 360):
  rows with the argument text and, per motion column, the resolved values (None where the fit flags the row),
  per-cell classes A (both readers give the resolved value, glyph reader confident), B (one reader gives it),
  C (unresolved: neither reader gives a value on the line), and the fitted line (a, b) of each column.
sheet(pdf, tag) -> p3_kit/MS{pdf}{tag}_k.png contact sheets of the B and C cells (crop + resolved value)."""
import json
import fitz
from PIL import Image, ImageDraw
import p2motion
import wide_kit as wk


def run(pdf, y0, y1, rules, tvals, args=None, nsub=3, tag="", keep=None, rates=None, mods=None, fixed=None):
    rows = p2motion.read(pdf, y0, y1, rules, nsub)
    rows = [r for r in rows if keep is None or keep(r)]
    n_exp = len(tvals[0]) if isinstance(tvals[0], (list, tuple)) else len(tvals)
    if len(rows) != n_exp:
        print(f"warning: {len(rows)} rows read, {n_exp} expected")
    out = {"pdf": pdf, "rules": rules, "rows": [], "lines": [], "flags": []}
    vals = []
    for gi in range(len(rules) - 2):
        ns = nsub[gi] if isinstance(nsub, (list, tuple)) else nsub
        tv = tvals[gi] if isinstance(tvals[0], (list, tuple)) else tvals        # per-column times (or expected values)
        v, flags, ab = p2motion.fit(rows, tv[:len(rows)], gi, ns, mod_deg=(mods[gi] if mods else 360),
                                    rate=(rates[gi] if rates else None), fixed=(fixed[gi] if fixed else None))
        vals.append(v); out["flags"] += [list(map(str, f)) for f in flags]
        out["lines"].append(list(ab) if ab else None)
    cls_count = {"A": 0, "B": 0, "C": 0}
    for i, r in enumerate(rows):
        rec = {"y": r["y"], "arg": r["arg"]["text"] if r["arg"] else None, "arg_tl": r["arg"]["tl"] if r["arg"] else "",
               "arg_ok": None, "groups": []}
        if args is not None and i < len(args):
            rec["arg_ok"] = (r["arg"] is not None and (r["arg"]["text"] == str(args[i]) or r["arg"]["tl"] == str(args[i])))
            rec["arg_exp"] = str(args[i])
        for gi, g in enumerate(r["groups"]):
            v = vals[gi][i] if vals[gi] else None
            cells = []
            for j, c in enumerate(g):
                exp = str(v[j]) if v else None
                rd = c["text"] if c else None; tl = c.get("tl", "") if c else ""; cf = c["conf"] if c else 0
                if exp is None:
                    k = "C"
                elif rd == exp and cf >= 0.85 and (not tl or tl == exp):
                    k = "A"
                elif rd == exp or tl == exp:
                    k = "B"
                else:
                    k = "C"
                cls_count[k] += 1
                cells.append({"value": exp, "read": rd, "tl": tl, "conf": cf, "cls": k,
                              "box": [c["x0"], c["x1"]] if c else None})
            rec["groups"].append(cells)
        out["rows"].append(rec)
    out["classes"] = cls_count
    json.dump(out, open(wk.OUT + f"MP{pdf}{tag}.json", "w", encoding="utf-8"), ensure_ascii=False, default=str)
    return out


def sheet(pdf, tag="", per=60):
    d = json.load(open(wk.OUT + f"MP{pdf}{tag}.json", encoding="utf-8"))
    page = wk.doc[pdf - 1]
    items = []
    for i, r in enumerate(d["rows"]):
        for gi, cells in enumerate(r["groups"]):
            for j, c in enumerate(cells):
                if c["cls"] == "A":
                    continue
                if c["box"]:
                    x0, x1 = c["box"]
                else:                                   # no token: show the whole motion column
                    x0, x1 = d["rules"][gi + 1] + 1, d["rules"][gi + 2] - 1
                im = wk.gray(page, 450, fitz.Rect(x0 - 3, r["y"] - 7, x1 + 3, r["y"] + 7))
                items.append((f"{c['cls']} r{i + 1} g{gi} p{j} = {c['value']}", im))
        if r.get("arg_ok") is False:
            x0, x1 = d["rules"][0] + 1, d["rules"][1] - 1
            items.append((f"C r{i + 1} arg = {r['arg_exp']}", wk.gray(page, 450, fitz.Rect(x0, r["y"] - 7, x1, r["y"] + 7))))
    files = []
    for s in range(0, len(items), per):
        part = [(lab, im.resize((max(1, int(im.width * 0.6)), max(1, int(im.height * 0.6))))) for lab, im in items[s:s + per]]
        cw = max(im.width for _, im in part) + 8; ch = max(im.height for _, im in part) + 8
        ncol = 5; nrow = (len(part) + ncol - 1) // ncol; LW = 150
        out = Image.new("L", (ncol * (cw + LW), nrow * ch), 255); dr = ImageDraw.Draw(out)
        for k, (lab, im) in enumerate(part):
            x = (k % ncol) * (cw + LW); y = (k // ncol) * ch
            dr.text((x + 2, y + ch // 2 - 6), lab, fill=0); out.paste(im, (x + LW, y + 4))
        f = wk.OUT + f"MS{pdf}{tag}_{s // per}.png"; out.save(f); files.append(f)
    return len(items), files


def agreed_units(name):
    """{(row index, group): units} for the cells of MP{name}.json where both readers give the same numbers"""
    d = json.load(open(wk.OUT + f"MP{name}.json", encoding="utf-8"))
    out = {}
    for i, r in enumerate(d["rows"]):
        for gi, g in enumerate(r["groups"]):
            if all(c and c["read"] and c["read"] == c.get("tl") and c["conf"] >= 0.85 for c in g):
                u = 0
                for c in g:
                    u = u * 60 + int(c["read"])
                out[(i, gi)] = u
    return out


def empirical_tv(name, tv, mods, places, half=3):
    """second pass: each column's expected values plus the running median (window 2 half + 1) of the residuals of the
    agreed cells of MP{name}.json against them; for tables whose values depart smoothly from the exact computation"""
    import statistics
    ag = agreed_units(name)
    out = []
    for gi, col in enumerate(tv):
        MOD = mods[gi] * 60 ** (places[gi] - 1)
        res = {i: ((ag[(i, gi)] - col[i] + MOD / 2) % MOD) - MOD / 2 for i in range(len(col)) if (i, gi) in ag}
        new = []
        for i in range(len(col)):
            near = [res[k] for k in range(i - half, i + half + 1) if k in res]
            new.append(round(col[i] + (statistics.median(near) if near else 0)))
        out.append(new)
    return out

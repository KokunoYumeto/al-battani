"""Write the data of Nallino's Part II pp. 187-188 to S06/revolutions/:
  revolutions_p2.tsv     one row per printed value: page, table, row, argument, column, degrees, minutes (and seconds),
                         the quarter printed in brackets (directions), how the number was established (`check`), notes.
                         Tables: increments (p. 187; columns moon, moon_anom, node, sat, jup, mars, ven_anom, mer_anom),
                         years (p. 188; columns collected, single: the «tempora ascensionum»), altitude (columns cap,
                         can), direction (columns can, cap)
  revolutions_pages.tsv  folio lines, titles and heads
p. 187: the eye reading of revolution_pages.py (EYE187), checked with the glyph reader and the OCR text layer
(MP636e.json): A both give the value, B one (the B cells re-read by Tesseract; those it read otherwise confirmed by eye
at 900 dpi), E neither (read again by eye at 500 dpi). p. 188: the eye reading compared, row by row, with the numbers
of the OCR text layer: A they agree, E they differ and a 700 dpi zoom confirms the eye."""
import csv, json, os, re
from collections import Counter
import wide_kit as wk
import revolution_pages as rp

AB = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani"
OUT = os.path.join(AB, "S06", "revolutions")
os.makedirs(OUT, exist_ok=True)
rows, classes = [], Counter()

# p. 187
d = json.load(open(wk.OUT + "MP636e.json", encoding="utf-8"))
assert len(d["rows"]) == 12
for i, r in enumerate(d["rows"]):
    assert r["arg_ok"], (i, r["arg"])
    for gi, col in enumerate(rp.P187):
        u = rp.EYE187[col][i]
        cells = r["groups"][gi]
        vals = tuple(c["value"] for c in cells)
        assert vals in ((str(u // 60), str(u % 60)), (None, None)), (i, col, vals)    # None: read by eye (E)
        cl = "".join(c["cls"] for c in cells).replace("C", "E")
        classes.update(cl)
        rows.append({"pdf": 636, "ppage": "187", "table": "increments", "row": i + 1, "arg": str(i + 1), "column": col,
                     "d": str(u // 60), "m": str(u % 60), "s": "", "quarter": "", "check": cl, "doubt": ""})


def tl_rows(x0, x1, y0, y1, tol=6.0):
    ws = [w for w in wk.doc[637 - 1].get_text("words") if x0 < (w[0] + w[2]) / 2 < x1 and y0 < w[1] < y1
          and re.search(r"\d", w[4])]
    ws.sort(key=lambda w: w[1])
    out = []
    for w in ws:
        if out and abs(w[1] - out[-1][-1][1]) < tol:
            out[-1].append(w)
        else:
            out.append([w])
    return [[t for w in sorted(r, key=lambda w: w[0]) for t in re.findall(r"\d+", w[4])] for r in out]


def classify(expected, tl):
    """per value (tuple of numbers): A if the text-layer row has the same numbers in the same places, else E"""
    flat = [str(x) for v in expected for x in v]
    if len(tl) == len(flat) - len(expected[0]):          # the text layer misses the argument: compare the values
        tl = [str(x) for x in expected[0]] + tl
    if len(tl) != len(flat):
        return ["E"] * len(expected)
    out, k = [], 0
    for v in expected:
        n = len(v)
        out.append("A" if tl[k:k + n] == [str(x) for x in v] else "E")
        k += n
    return out


blocks = [("years", "collected", (120, 200, 300, 640 + 75), [((20 * (i + 1),), v) for i, v in
                                                                  enumerate(rp.COLLECTED[k] for k in sorted(rp.COLLECTED))]),
          ("years", "single", (205, 285, 300, 730), [((k,), rp.SINGLE[k]) for k in sorted(rp.SINGLE)])]
for table, col, (x0, x1, y0, y1), items in blocks:
    tl = tl_rows(x0, x1, y0, y1, tol=6.0 if col == "collected" else 4.0)
    assert len(tl) == len(items), (col, len(tl))
    for i, ((arg,), val) in enumerate(items):
        cl = classify([(arg,), val], tl[i])[1]
        classes.update(cl)
        rows.append({"pdf": 637, "ppage": "188", "table": table, "row": i + 1, "arg": str(arg), "column": col,
                     "d": str(val[0]), "m": str(val[1]), "s": "", "quarter": "", "check": cl, "doubt": ""})
tl = tl_rows(290, 520, 298, 460, tol=4.0)
assert len(tl) == 12, len(tl)
for h in range(12):
    cap, can = rp.ALTITUDE["cap"][h], rp.ALTITUDE["can"][h]
    cls = classify([(h + 1,), cap, can], tl[h])
    for col, val, cl in (("cap", cap, cls[1]), ("can", can, cls[2])):
        classes.update(cl)
        rows.append({"pdf": 637, "ppage": "188", "table": "altitude", "row": h + 1, "arg": str(h + 1), "column": col,
                     "d": str(val[0]), "m": str(val[1]), "s": "", "quarter": "", "check": cl, "doubt": ""})
tl = tl_rows(290, 520, 650, 735, tol=6.0)
assert len(tl) == 6, len(tl)
for h in range(6):
    (can, qn), (cap, qp) = rp.DIRECTION["can"][h], rp.DIRECTION["cap"][h]
    cls = classify([(h + 1,), can, cap], tl[h])
    for col, val, q, cl in (("can", can, qn, cls[1]), ("cap", cap, qp, cls[2])):
        classes.update(cl)
        rows.append({"pdf": 637, "ppage": "188", "table": "direction", "row": h + 1, "arg": str(h + 1), "column": col,
                     "d": str(val[0]), "m": str(val[1]), "s": str(val[2]), "quarter": q, "check": cl, "doubt": ""})
fields = ["pdf", "ppage", "table", "row", "arg", "column", "d", "m", "s", "quarter", "check", "doubt"]
with open(os.path.join(OUT, "revolutions_p2.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(rows)
print(len(rows), "rows;", classes)
print("E cells:", [(r["table"], r["column"], r["arg"]) for r in rows if "E" in r["check"]])

pages = [
    {"pdf": 636, "ppage": "187", "fol": "f. 239,v.",
     "title_ar": "جدول زيادات الكواكب التي يزاد اوساطها في الاصل للتحاويل",
     "title_la": "Tabula incrementorum quibus planetarum loci medii in origine augendi sunt / ad revolutiones "
                 "[annorum supputandas].",
     "heads": "‖Numerus annorum / Romanorum integrorum."
              "|زيادة وسط القمر‖Incrementum / loci medii Lunae.|زيادة حاصة القمر‖Incrementum / anomaliae Lunae."
              "|زيادة العقد الشمالي‖Incrementum / nodi borealis."
              "|زيادة وسط زحل ونقصان حاصته‖Incrementum loci medii / et deminutio anomaliae / Saturni."
              "|زيادة وسط المشتري ونقصان حاصته‖Incrementum loci medii / et deminutio anomaliae / Iovis."
              "|زيادة وسط المريخ ونقصان حاصته‖Incrementum loci medii / et deminutio anomaliae / Martis."
              "|زيادة حاصة الزهرة‖Incrementum / anomaliae Veneris.|زيادة حاصة عطارد‖Incrementum / anomaliae Mercurii.",
     "signature": ""},
    {"pdf": 637, "ppage": "188", "fol": "f. 240,r.",
     "title_ar": "جدول تحاويل السنين الرومية‖جداول الساعات‖جدول سموت الساعات",
     "title_la": "Tabula revolutionum annorum / Romanorum [tropicorum].‖Tabulae horarum.‖Tabula directionum horarum.",
     "heads": "السنون المجموعة للتحاويل‖Anni collecti / ad revolutiones.|ازمان المطالع‖Tempora / ascensionum."
              "|السنون المبسوطة للتحاويل‖Anni singuli / ad revolutiones.|ازمان المطالع‖Tempora / ascensionum."
              "|الساعات‖Horae.|الارتفاع / ساعات الجدي‖Altitudo. / Horae Capricorni."
              "|الارتفاع / ساعات السرطان‖Altitudo. / Horae Cancri."
              "|عدد الساعات‖Numerus horarum.|ساعات راس السرطان / سمت الساعات‖Horae initii Cancri. / Directio horarum."
              "|ساعات راس الجدي / سمت الساعات‖Horae initii Capricorni. / Directio horarum.",
     "signature": ""}]
with open(os.path.join(OUT, "revolutions_pages.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(pages[0]), delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(pages)
print(len(pages), "pages")

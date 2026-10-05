"""Generate the two diplomatic editions of al-Battani's status tables for the year 1211 of Dhu 'l-qarnayn:
  p3_status_1211.tex - Nallino Part III (Arabic, codex numerals in Maghribi abjad), one page per source page
  p2_status_1211.tex - Nallino Part II (Latin, Western numerals, notes), one page per source page
Data: st_p3.tsv, st_p3_footnotes.tsv, st_p3_pages.tsv, st_p2.tsv, st_p2_notes.tsv, st_p2_pages.tsv.
Markup as in gen_stars.py; a vnote row is a note printed vertically over the rows named in its p2 field (e.g. 17-24):
its text is split at ' || ' into the part over the half-arc columns and the part over the rising/setting columns."""
import re
from pathlib import Path

from gen_stars import PREAMBLE, AR_DIGITS, markup, read

HERE = Path(__file__).resolve().parent
NUMS = ("dec_d", "dec_m", "dir", "alt_d", "alt_m", "half_d", "half_m", "cul_d", "cul_m", "ris_d", "ris_m", "set_d", "set_m")
NCOL = 2 + len(NUMS)                                  # magnitude, name, 13 numeric columns

NO_MAG = {"M3"}                                       # the third table has no magnitude column (Nallino, Pars II p. 183, n. 1)


def p3_head(text, has_mag):
    off = 1 if has_mag else 0
    mag = r"\multirow{2}{*}{\rotatebox[origin=c]{90}{\scriptsize مراتب العظم}} & " if has_mag else ""
    return (mag + r"\multirow{2}{*}{\parbox{36mm}{\centering %s}} & " % text +
            r"\multicolumn{2}{c|}{\parbox{15mm}{\centering ابعادها عن معدّل النهار}} & \multirow{2}{*}{\rotatebox[origin=c]{90}{\scriptsize علامات الجهة}} & "
            r"\multicolumn{2}{c|}{\parbox{15mm}{\centering ارتفاعها في وسط السماء}} & \multicolumn{2}{c|}{\parbox{15mm}{\centering نصف مكثها فوق الارض}} & "
            r"\multicolumn{2}{c|}{\parbox{15mm}{\centering الاجزاء التي تتوسط السماء معها}} & \multicolumn{2}{c|}{\parbox{15mm}{\centering الاجزاء التي معها تطلع}} & "
            r"\multicolumn{2}{c|}{\parbox{15mm}{\centering الاجزاء التي معها تغيب}} \\ " + r"\cline{%d-%d}\cline{%d-%d}" % (2 + off, 3 + off, 5 + off, 14 + off) +
            "\n" + (" & " if has_mag else "") + r" & درج & دقائق & & درج & دقائق & درج & دقائق & درج & دقائق & درج & دقائق & درج & دقائق \\ \hline")


def p3_tab(has_mag):
    return (r"\begin{Arabic}\footnotesize\begin{tabular}{" + ("|c" if has_mag else "") + "|p{36mm}|" +
            "|".join([">{\\centering\\arraybackslash}p{6.3mm}"] * 13) + "|}\\hline")


def vnote_spans(rows):
    """For each vnote, the p2 numbers it covers -> (first row index, number of rows, text parts)."""
    spans = {}
    for r in rows:
        if r["kind"] in ("vnote", "hnote"):
            a, b = (int(x) for x in r["p2"].split("-"))
            spans[r["pdf"]] = (a, b, r["text"].split(" || "), r["kind"])
    return spans


def p3_document():
    rows = read("st_p3.tsv"); notes = read("st_p3_footnotes.tsv")
    pages = {p["pdf"]: p for p in read("st_p3_pages.tsv")}
    out = [PREAMBLE, r"\usepackage{rotating}", r"\begin{document}"]
    for pdf in sorted({r["pdf"] for r in rows}, key=int, reverse=True):
        R = [r for r in rows if r["pdf"] == pdf]
        out.append(r"\clearpage")
        out.append(r"{\large \textarabic{" + R[0]["ppage"].translate(AR_DIGITS) + r"}}\par\vspace{1mm}")
        folio = (pages.get(pdf) or {}).get("above")
        if folio:
            out.append(r"\begin{center}" + folio + r"\end{center}")
        spans = vnote_spans(R)
        open_tab = False
        for r in R:
            k = r["kind"]
            if k == "folio":
                if open_tab:
                    out.append(r"\end{tabular}\end{Arabic}"); open_tab = False
                out.append(r"\par\vspace{3mm}\begin{center}" + r["text"] + r"\end{center}\vspace{-1mm}")
                continue
            if not open_tab:
                has_mag = r["section"] not in NO_MAG
                out.append(p3_tab(has_mag)); open_tab = True
            if k == "title":
                out.append(r"\multicolumn{%d}{|c|}{\rule{0pt}{6mm}\large %s} \\ \hline" % (NCOL if has_mag else NCOL - 1, markup(r["text"], False)))
            elif k == "colhead":
                out.append(p3_head(markup(r["text"], False).replace(" / ", r"\\"), has_mag))
            elif k == "star":
                cells = ([markup(r["mag"], False)] if has_mag else []) + [markup(r["text"], False).replace(" / ", r"\newline ")]
                vals = [markup(r[f], False) for f in NUMS]
                n = int(r["p2"]) if r["p2"].isdigit() else None
                sp = spans.get(pdf)
                if sp and sp[3] == "hnote" and n is not None and sp[0] <= n <= sp[1]:
                    # a text printed in the row itself, across the altitude/half-arc and the rising/setting columns
                    part = lambda t: r"\multicolumn{4}{c|}{\parbox{24mm}{\centering\scriptsize %s}}" % markup(t, False).replace(" / ", r"\\")
                    vals = vals[:3] + [part(sp[2][0])] + vals[7:9] + [part(sp[2][1])]
                    sp = None
                if sp and n is not None and sp[0] <= n <= sp[1]:
                    rowsn = sp[1] - sp[0] + 1
                    if n == sp[0]:
                        p_part = r"\multicolumn{2}{c|}{\multirow{%d}{*}{\rotatebox[origin=c]{-90}{\parbox{%dmm}{\centering\scriptsize %s}}}}" % (rowsn, 4 * rowsn, markup(sp[2][0], False).replace(" / ", r"\\"))
                        bc_part = r"\multicolumn{4}{c|}{\multirow{%d}{*}{\rotatebox[origin=c]{-90}{\parbox{%dmm}{\centering\scriptsize %s}}}}" % (rowsn, 4 * rowsn, markup(sp[2][1], False).replace(" / ", r"\\"))
                    else:
                        p_part, bc_part = r"\multicolumn{2}{c|}{}", r"\multicolumn{4}{c|}{}"
                    vals = vals[:5] + [p_part] + vals[7:9] + [bc_part]
                extra = r["text"].count(" / ")
                if extra:
                    vals = [r"\raisebox{-%d\normalbaselineskip}[0pt][0pt]{%s}" % (extra, v) if v and not v.startswith(r"\multicolumn") else v for v in vals]
                    if has_mag:
                        cells[0] = r"\raisebox{-%d\normalbaselineskip}[0pt][0pt]{%s}" % (extra, cells[0]) if cells[0] else ""
                out.append(" & ".join(cells + vals) + r" \\")
                nxt = R[R.index(r) + 1] if R.index(r) + 1 < len(R) else None
                if nxt is None or nxt["kind"] not in ("star", "vnote"):
                    out.append(r"\hline")
            elif k in ("vnote", "hnote"):
                continue
        if open_tab:
            out.append(r"\end{tabular}\end{Arabic}")
        F = [n for n in notes if n["pdf"] == pdf]
        if F:
            out.append(r"\par\vspace{3mm}\noindent\rule{40mm}{.4pt}\par\vspace{1mm}{\small " +
                       " --- ".join(f"{n['n']}) " + markup(n["text"]) for n in F) + r"}")
        sig = (pages.get(pdf) or {}).get("signature")
        if sig:
            out.append(r"\par\vfill\hfill " + sig)
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


P2_HEADS = ("Declinatio.", "Plaga Caeli.", "Altitudo meridiana.", "Dimidium commorationis supra Terram.",
            "Gradus cum quibus culminant.", "Gradus cum quibus oriuntur.", "Gradus cum quibus occidunt.")


def rot(t, w=24):
    return r"\rotatebox{90}{\parbox{%dmm}{\centering\scriptsize %s}}" % (w, t)


def p2_document():
    rows = read("st_p2.tsv"); notes = read("st_p2_notes.tsv"); pages = {p["pdf"]: p for p in read("st_p2_pages.tsv")}
    out = [PREAMBLE, r"\usepackage{rotating}", r"\begin{document}"]
    head = (r" & \centering Stellarum nomina. & \multicolumn{2}{c|}{" + rot(P2_HEADS[0], 14) + r"} & " + rot(P2_HEADS[1], 14) + " & " +
            " & ".join(r"\multicolumn{2}{c|}{" + rot(h) + "}" for h in P2_HEADS[2:]) + r" & " + rot("Ordines magnitudinis.", 14) + r" \\ \hline")
    tab = r"\begin{center}\footnotesize\begin{tabular}{r|p{30mm}|r@{\hspace{1.5mm}}r|c|" + "|".join(["r@{\\hspace{1.5mm}}r"] * 5) + "||c|}\\cline{2-16}"
    for pdf in sorted({r["pdf"] for r in rows}, key=int):
        R = [r for r in rows if r["pdf"] == pdf]; P = pages.get(pdf, {})
        out.append(r"\clearpage")
        if P.get("head"):
            l, c, rr = (P["head"].split("|") + ["", "", ""])[:3]
            out.append(r"\noindent\makebox[\textwidth]{\textbf{" + l + r"}\hfill{\small " + c + r"}\hfill\textbf{" + rr + r"}}\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{2mm}")
        for part in filter(None, (P.get("above") or "").split("}//{")):
            kind, _, txt = part.strip("{}").partition(":")
            out.append(r"\begin{center}{\small " + markup(txt) + r"}\end{center}")
        out.append(tab)
        if pdf == "627":
            out.append(r" & \multicolumn{15}{c|}{\rule{0pt}{6mm}\textbf{Status praecipuarum stellarum fixarum anno 1211 a Dhū ’l-qarnayn.}} \\ \cline{2-16}")
        out.append(head)
        vn = [r for r in R if r["kind"] == "vnote"]
        span = None
        if vn:
            a, b = (int(x) for x in vn[0]["no"].split("-")); span = (a, b, vn[0]["name"].split(" // "))
        hn = {int(r["no"].split("-")[0]): r["name"].split(" // ") for r in R if r["kind"] == "hnote"}
        for r in R:
            if r["kind"] != "star":
                continue
            desc = markup(r["name"]).replace(" / ", r"\newline\hspace*{3mm}")
            vals = [markup(r[f]) for f in ("dec_d", "dec_m", "plaga", "alt_d", "alt_m", "half_d", "half_m", "cul_d", "cul_m", "ris_d", "ris_m", "set_d", "set_m")]
            n = int(r["no"]) if r["no"].isdigit() else None
            if n in hn:                                  # a text printed in the row itself (nr. 69)
                part = lambda t: r"\multicolumn{4}{c|}{\parbox{30mm}{\centering\scriptsize %s}}" % markup(t).replace(" / ", r"\\")
                vals = vals[:3] + [part(hn[n][0])] + vals[7:9] + [part(hn[n][1])]
            if span and span[0] <= n <= span[1]:
                rowsn = span[1] - span[0] + 1
                if n == span[0]:
                    vals[5:7] = [r"\multicolumn{2}{c|}{\multirow{%d}{*}{\rotatebox{90}{\parbox{%dmm}{\centering\scriptsize %s}}}}" % (rowsn, 6 * rowsn, markup(span[2][0]).replace(" / ", r"\\"))]
                    vals[8:12] = [r"\multicolumn{4}{c|}{\multirow{%d}{*}{\rotatebox{90}{\parbox{%dmm}{\centering\scriptsize %s}}}}" % (rowsn, 6 * rowsn, markup(span[2][1]).replace(" / ", r"\\"))]
                else:
                    vals[5:7] = [r"\multicolumn{2}{c|}{}"]
                    vals[8:12] = [r"\multicolumn{4}{c|}{}"]
            extra = r["name"].count(" / ")
            if extra:
                vals = [r"\raisebox{-%d\normalbaselineskip}[0pt][0pt]{%s}" % (extra, v) if v and not v.startswith(r"\multicolumn") else v for v in vals]
            mag = markup(r["mag"])
            if extra:
                mag = r"\raisebox{-%d\normalbaselineskip}[0pt][0pt]{%s}" % (extra, mag)
            out.append(" & ".join([r["no"], desc] + vals + [mag]) + r" \\")
        out.append(r"\cline{2-16}\end{tabular}\end{center}")
        N = [n for n in notes if n["pdf"] == pdf and n["no"] != "*" and n["text"]]
        if N:
            out.append(r"{\small")
            for n in N:
                num = "" if n["no"] == "cont" else n["no"] + ". "
                out.append(r"\par\hangindent=12mm\hangafter=1 " + num + markup(n["text"]))
            out.append(r"\par}")
        for n in notes:
            if n["pdf"] == pdf and n["no"] == "*":
                out.append(r"\par\vspace{2mm}\begin{center}\rule{40mm}{.4pt}\end{center}{\small " + markup(n["text"]) + r"}")
        if P.get("signature"):
            out.append(r"\par\vfill\hfill " + P["signature"])
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p3_status_1211.tex").write_text(p3_document(), encoding="utf-8", newline="\n")
    (HERE / "p2_status_1211.tex").write_text(p2_document(), encoding="utf-8", newline="\n")
    print("wrote p3_status_1211.tex, p2_status_1211.tex")

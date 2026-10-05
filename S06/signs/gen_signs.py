"""Generate the edition of Nallino's Part II pp. 7-8 from p7_signs.tsv, p8_signs.tsv and signs_heads.tsv:
p. 7 (the signs of the Arab years and months, two schemes side by side, with the number of days of each month
between them) and p. 8 (the signs of the Syrian months for the 28 years of the solar cycle). Output: p2_signs.tex"""
from pathlib import Path

from gen_stars import PREAMBLE, markup, read

HERE = Path(__file__).resolve().parent


def nl(s):
    return markup(s).replace(" / ", r"\\")


def ar(s):
    return r"\textarabic{" + s + "}"


def rot(*lines, size=r"\scriptsize"):
    return r"\rotatebox{90}{" + size + r"\begin{tabular}{@{}c@{}}" + r"\\".join(lines) + r"\end{tabular}}"


def page7(rows, H):
    get = lambda part, sch: [r for r in rows if r["part"] == part and r["scheme"] == sch]
    coll = {s: get("collected", s) for s in ("I", "II")}
    sing = {s: get("single", s) for s in ("I", "II")}
    mon = {s: get("month", s) for s in ("I", "II")}
    t = H["title"]["la"].split(" / ")
    out = [r"\clearpage\noindent\makebox[\textwidth]{\hfill{\scriptsize AL-BATTANI OPUS ASTRONOMICUM}\hfill\llap{7}}",
           r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{1mm}",
           r"\begin{center}{\small " + H["folio"]["la"] + r"}\end{center}\vspace{-3mm}",
           r"\begin{center}\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.02}"]
    C = r">{\centering\arraybackslash}"
    spec = ("|" + C + "p{27mm}|" + C + "p{6mm}||" + C + "p{7mm}|" + C + "p{6mm}||" + C + "p{13mm}||" +
            C + "p{27mm}|" + C + "p{6mm}||" + C + "p{7mm}|" + C + "p{6mm}|" + C + "p{6mm}|")
    out.append(r"\begin{tabular}{" + spec + r"}\hline\hline")
    out.append(r"\multicolumn{10}{||c||}{\parbox{150mm}{\centering\vspace{1mm}{\large " + ar(H["title"]["ar"]) + r"}\\\textbf{" +
               markup(t[0]) + r"}\\\textbf{" + markup(t[1]) + r"}\vspace{1mm}}} \\ \hline")
    blk = lambda: [r"\multicolumn{2}{c||}{\small\begin{tabular}{@{}c@{}}" + ar(H["collected"]["ar"]) + r"\\" + nl(H["collected"]["la"]) + r"\end{tabular}}",
                   r"\multicolumn{2}{c||}{\small\begin{tabular}{@{}c@{}}" + ar(H["single"]["ar"]) + r"\\" + nl(H["single"]["la"]) + r"\end{tabular}}"]
    out.append(" & ".join(blk() + [""] + [blk()[0], r"\multicolumn{3}{c|}{\small\begin{tabular}{@{}c@{}}" + ar(H["single"]["ar"]) +
               r"\\" + nl(H["single"]["la"]) + r"\end{tabular}}"]) + r" \\ \cline{1-4}\cline{6-10}")
    num = r"\small\begin{tabular}{@{}c@{}}" + ar(H["number"]["ar"]) + r"\\" + nl(H["number"]["la"]) + r"\end{tabular}"
    sg = rot(ar(H["signs"]["ar"]), nl(H["signs"]["la"]))
    ns = rot(ar(H["number (single)"]["ar"]), nl(H["number (single)"]["la"]))
    bs = rot(ar(H["bissextile"]["ar"]), nl(H["bissextile"]["la"]))
    out.append(" & ".join([num, sg, ns, sg, "", num, sg, ns, sg, bs]) + r" \\ \hline\hline")
    days_head = r"\multirow{-9}{*}{" + rot(ar(H["month days"]["ar"]), nl(H["month days"]["la"])) + "}"   # spans upward
    for i in range(30):
        cells = []
        for s in ("I", "II"):
            if i < 7:
                cells += [coll[s][i]["key"], coll[s][i]["sign"]]
            elif i == 7:
                cells += ["", ""]
            elif i == 10:
                cells += [r"\multicolumn{2}{c||}{\small\begin{tabular}{@{}c@{}}" + ar(H["months"]["ar"]) + r"\\" + nl(H["months"]["la"]) + r"\end{tabular}}"]
            elif i in (8, 9, 11, 12):
                cells += [r"\multicolumn{2}{c||}{}"]
            elif i == 15:
                cells += [r"\small\begin{tabular}{@{}c@{}}" + ar(H["month names"]["ar"]) + r"\\" + nl(H["month names"]["la"]) + r"\end{tabular}",
                          r"\multirow{-3}{*}{" + rot(ar(H["month signs"]["ar"]), nl(H["month signs"]["la"])) + "}"]
            elif i < 18:
                cells += ["", ""]
            else:
                m = mon[s][i - 18]
                cells += [r"\raggedright " + markup(m["key"]), m["sign"]]
            r = sing[s][i]
            cells += [r["key"], r["sign"]] + ([r["bis"]] if s == "II" else [])
            if s == "I":
                cells.append(days_head if i == 17 else (mon["I"][i - 18]["days"] if i >= 18 else ""))
        line = " & ".join(cells) + r" \\"
        if i == 6:
            line += r" \cline{1-2}\cline{6-7}"
        if i == 12:
            line += r" \cline{1-2}\cline{6-7}"
        if i == 17:
            line += r" \cline{1-2}\cline{6-7}"
        out.append(line)
    out.append(r"\hline\hline\end{tabular}\end{center}")
    return "\n".join(out)


def page8(rows, H):
    t = H["title"]["la"].split(" / ")
    months = [H[f"month {i}"] for i in range(1, 13)]
    out = [r"\clearpage\noindent\makebox[\textwidth]{\rlap{8}\hfill{\scriptsize C. A. NALLINO}\hfill}",
           r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{1mm}",
           r"\begin{center}{\small " + H["folio"]["la"] + r"}\end{center}\vspace{-3mm}",
           r"\begin{center}\setlength{\tabcolsep}{2pt}\renewcommand{\arraystretch}{1.05}"]
    C = r">{\centering\arraybackslash}"
    spec = "|" + C + "p{13mm}|" + "|".join([C + "p{8.5mm}"] * 6) + "||" + C + "p{11mm}||" + "|".join([C + "p{8.5mm}"] * 6) + "|"
    out.append(r"\begin{tabular}{" + spec + r"}\hline\hline")
    out.append(r"\multicolumn{14}{||c||}{\parbox{150mm}{\centering\vspace{1mm}{\large " + ar(H["title"]["ar"]) + r"}\\\textbf{" +
               markup(t[0]) + r"}\\\textbf{" + markup(t[1]) + r"}\vspace{1mm}}} \\ \hline")

    def mhead(h):
        la, sy, d = h["la"].split(" / ")
        return rot(ar(h["ar"]), markup(la), markup(sy), markup(d), size=r"\tiny")
    heads = [rot(ar(H["years"]["ar"]), markup(H["years"]["la"]), size=r"\scriptsize")] + [mhead(h) for h in months[:6]] + \
            [rot(ar(H["bissextile"]["ar"]), markup(H["bissextile"]["la"]), size=r"\scriptsize")] + [mhead(h) for h in months[6:]]
    out.append(" & ".join(heads) + r" \\ \hline\hline")
    keys = ["year", "Aylūl", "Tishrīn I", "Tishrīn II", "Kānūn I", "Kānūn II", "Subāṭ", "bis", "Ādhār", "Nīsān", "Ayyār",
            "Ḥazīrān", "Tammūz", "Āb"]
    for r in rows:
        out.append(" & ".join(r[k] for k in keys) + r" \\")
    out.append(r"\hline\hline\end{tabular}\end{center}")
    return "\n".join(out)


def document():
    heads = read("signs_heads.tsv")
    H7 = {h["item"]: h for h in heads if h["page"] == "7"}
    H8 = {h["item"]: h for h in heads if h["page"] == "8"}
    pre = PREAMBLE.replace("margin=16mm", "margin=12mm").replace(r"\usepackage{polyglossia}", r"\usepackage{multirow}" "\n" r"\usepackage{polyglossia}")
    out = [pre, r"\begin{document}", page7(read("p7_signs.tsv"), H7), page8(read("p8_signs.tsv"), H8), r"\end{document}"]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p2_signs.tex").write_text(document(), encoding="utf-8", newline="\n")
    print("wrote p2_signs.tex")

"""Generate the edition of Nallino's Part II pp. 29-32 (mean syzygies in Egyptian years) from syz_p2.tsv,
syz_pages.tsv and syz_extra.tsv: one page per printed page, with the running head, the folio line and the framed
tables (titles, heads, rows in groups of four; each column a centred group of three fixed-width numbers; the first row
of a table carries the marks as printed). p. 31 holds three tables in one frame; under the table of p. 32 stand the
line for 25 years and the eclipse limits. Output: p2_syzygies.tex"""
import re
from pathlib import Path

from gen_stars import PREAMBLE, markup, read

HERE = Path(__file__).resolve().parent
G = ["day", "lum", "anom", "lat"]
WIDTHS = r"\newlength{\Dw}\newlength{\Mw}\settowidth{\Dw}{000}\settowidth{\Mw}{00}"
COLW = "30mm"


def nl(s):
    return markup(s).replace(" / ", r"\\").replace(r"\\[", r"\\{}[")       # a bracket after \\ is not its argument


def ar(s):
    return r"\\".join(r"\textarabic{" + x + "}" for x in s.split(" / "))


def sup(s):
    """{d}, {iii}, {iv} -> superscripts as printed."""
    s = s.replace("{d}", r"\textsuperscript{d}")
    return re.sub(r"\{(iii|iv)\}", lambda m: r"\textsuperscript{\textsc{" + m.group(1) + "}}", s)


def numbers(vals):
    return r"\hspace{2.6mm}".join(r"\makebox[" + (r"\Dw" if k == 0 else r"\Mw") + "][r]{" + v + "}" for k, v in enumerate(vals))


def marks(table, g):
    if table == "parts":
        return ["", "", ""]
    if g == "day":
        return ["′", "″", "‴"] if table == "intervals" else [r"\textsuperscript{d}", "′", "″"]
    return ["°", "′", "″"]


def head_cells(page, argw, rotate):
    heads = [h.split("‖") for h in page["heads"].split("|")]
    a, l = heads[0]
    if rotate:
        c0 = r"\rotatebox{90}{\scriptsize\begin{tabular}{@{}c@{}}" + ar(a) + r"\\" + nl(l) + r"\end{tabular}}"
    else:
        c0 = r"\parbox[c]{" + argw + r"}{\centering\scriptsize " + ar(a) + r"\\" + nl(l) + r"\par\vspace{0.7mm}}"
    return [c0] + [r"\parbox[c]{" + COLW + r"}{\centering\scriptsize " + ar(a) + r"\\" + nl(l) + r"\par\vspace{0.7mm}}"
                   for a, l in heads[1:]]


def body(rows, table, group=4):
    out = []
    for i, r in enumerate(rows):
        arg = nl(r["arg"])
        line = [arg if table != "parts" else r"\raggedright " + arg]
        for g in G:
            vals = [r[g + "_1"], r[g + "_2"], r[g + "_3"]]
            if i == 0:
                vals = [v + (r"\rlap{" + m + "}" if m else "") for v, m in zip(vals, marks(table, g))]
            line.append(numbers(vals))
        gap = r"[1.2mm]" if group and i % group == group - 1 and i < len(rows) - 1 else ""
        out.append(" & ".join(line) + r" \\" + gap)
    return out


def title_cell(ar_text, la_text, size=r"\large", bold=True):
    la = "".join(r"\\" + (r"\textbf{" if bold else "{") + markup(x) + "}" for x in la_text.split(" / "))
    return r"\multicolumn{5}{||c||}{\parbox{160mm}{\centering\vspace{1mm}{" + size + " " + ar(ar_text) + "}" + la + r"\vspace{1mm}}} \\"


def running_head(pp):
    return (r"\noindent\makebox[\textwidth]{\hfill{\scriptsize AL-BATTANI OPUS ASTRONOMICUM}\hfill\llap{" + str(pp) + "}}"
            if pp % 2 else r"\noindent\makebox[\textwidth]{\rlap{" + str(pp) + r"}\hfill{\scriptsize C. A. NALLINO}\hfill}")


def page_start(pp, fol):
    return [r"\clearpage", running_head(pp), r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{1mm}",
            r"\begin{center}{\small " + fol + r"}\end{center}\vspace{-3mm}"]


def spec(argw, centred=True):
    a = (r">{\centering\arraybackslash}p{" if centred else r">{\raggedright\arraybackslash}p{") + argw + "}"
    return "|" + a + "|" + "|".join([r">{\centering\arraybackslash}p{" + COLW + "}"] * 4) + "|"


def simple_page(page, rows, extra):
    """pp. 29, 30, 32: one table."""
    out = page_start(int(page["ppage"]), page["fol"])
    out.append(r"\begin{center}\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.05}\begin{tabular}{" + spec("13mm") + r"}\hline\hline")
    out.append(title_cell(page["title_ar"], page["title_la"]) + r" \hline")
    out.append(" & ".join(head_cells(page, "13mm", True)) + r" \\ \hline\hline")
    out += body(rows, page["table"])
    out.append(r"\hline\hline\end{tabular}\end{center}")
    if page["table"] == "single":
        p25 = sup(extra["period25"]["text"]).split("|")
        out.append(r"\vspace{-1mm}\begin{center}\setlength{\tabcolsep}{4pt}\begin{tabular}{" + spec("13mm").replace("|", "") + "}")
        out.append(" & ".join(p25) + r" \\")
        out.append(r"\end{tabular}\end{center}\vspace{2mm}")
        for item in ("eclipse_sun", "eclipse_moon"):
            out.append(r"\noindent\hspace*{6mm}\parbox{\dimexpr\textwidth-12mm}{\setlength{\parindent}{6mm}\indent "
                       + markup(extra[item]["text"]) + r"}\par\vspace{1mm}")
    return "\n".join(out)


def page31(pages, rows):
    pa, pb, pc = (next(p for p in pages if p["table"] == t) for t in ("parts", "months", "intervals"))
    R = {t: [r for r in rows if r["table"] == t] for t in ("parts", "months", "intervals")}
    out = page_start(31, pa["fol"])
    out.append(r"\begin{center}\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.05}\begin{tabular}{" + spec("32mm") + r"}\hline\hline")
    out.append(title_cell(pa["title_ar"], pa["title_la"]) + r" \hline")
    out.append(title_cell(pa["subtitle_ar"], pa["subtitle_la"], r"\normalsize", bold=False) + r" \hline")
    out += body(R["parts"], "parts", group=0)
    out.append(r"\hline")
    out.append(title_cell(pb["subtitle_ar"], pb["subtitle_la"]) + r" \hline")
    out.append(" & ".join(head_cells(pb, "32mm", False)) + r" \\ \hline\hline")
    out += body(R["months"], "months")
    out.append(r"\hline\hline")
    out.append(" & ".join(head_cells(pc, "32mm", False)) + r" \\ \hline\hline")
    out += body(R["intervals"], "intervals", group=0)
    out.append(r"\hline\hline\end{tabular}\end{center}")
    return "\n".join(out)


def document():
    pages = read("syz_pages.tsv"); rows = read("syz_p2.tsv")
    extra = {r["item"]: r for r in read("syz_extra.tsv")}
    out = [PREAMBLE.replace("margin=16mm", "margin=14mm"), WIDTHS, r"\begin{document}"]
    for page in pages:
        t = page["table"]
        if t in ("conj", "opp", "single"):
            out.append(simple_page(page, [r for r in rows if r["table"] == t], extra))
        elif t == "parts":
            out.append(page31(pages, rows))
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p2_syzygies.tex").write_text(document(), encoding="utf-8", newline="\n")
    print("wrote p2_syzygies.tex")

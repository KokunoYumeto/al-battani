"""Generate the edition of Nallino's Part II pp. 29-32 (mean syzygies in Egyptian years) and pp. 84-87 (in Roman
years) from syz_p2.tsv, syz_pages.tsv, syz_extra.tsv, rsyz_p2.tsv and rsyz_pages.tsv: one page per printed page, with
the running head, the folio line and the framed tables (titles, heads, rows in groups of four; each column a centred
group of three fixed-width numbers; the first row of a table carries the marks as printed). pp. 31 and 87 hold three
tables in one frame; under the table of p. 32 stand the line for 25 years and the eclipse limits. Output:
p2_syzygies.tex"""
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


def numbers(vals, gap="2.6mm"):
    return (r"\hspace{" + gap + "}").join(r"\makebox[" + (r"\Dw" if k == 0 else r"\Mw") + "][r]{" + v + "}" for k, v in enumerate(vals))


def marks(table, g, roman=False):
    """the marks of the first row: p. 31 prints none on the parts of a month; pp. 84-87 mark the days «dies» (the
    intervals of p. 87 «d»)"""
    if table == "parts" and not roman:
        return ["", "", ""]
    if g == "day":
        if roman:
            return [r"\textsuperscript{d}" if table == "intervals"
                    else r"\raisebox{0.75ex}{\fontsize{5.5}{6}\selectfont\itshape dies}", "′", "″"]
        return ["′", "″", "‴"] if table == "intervals" else [r"\textsuperscript{d}", "′", "″"]
    return ["°", "′", "″"]


def head_text(a, l):
    return (ar(a) + r"\\" if a else "") + nl(l)


def head_cells(page, argw, rotate):
    heads = [h.split("‖") for h in page["heads"].split("|")]
    a, l = heads[0]
    if rotate:
        c0 = r"\rotatebox{90}{\scriptsize\begin{tabular}{@{}c@{}}" + head_text(a, l) + r"\end{tabular}}"
    else:
        c0 = r"\parbox[c]{" + argw + r"}{\centering\scriptsize " + head_text(a, l) + r"\par\vspace{0.7mm}}"
    return [c0] + [r"\parbox[c]{" + COLW + r"}{\centering\scriptsize " + head_text(a, l) + r"\par\vspace{0.7mm}}"
                   for a, l in heads[1:]]


def body(rows, table, group=4, roman=False, lead=None):
    """lead(r): the cells before the four columns (default: the argument)"""
    out = []
    for i, r in enumerate(rows):
        if lead:
            line = lead(r)
        else:
            arg = nl(r["arg"])
            line = [arg if table != "parts" else r"\raggedright " + arg]
        for g in G:
            vals = [r[g + "_1"], r[g + "_2"], r[g + "_3"]]
            if i == 0:
                vals = [v + (r"\rlap{" + m + "}" if m else "") for v, m in zip(vals, marks(table, g, roman))]
            wide = roman and g == "day" and table != "intervals"      # room for the mark «dies»
            line.append(numbers(vals, "4.6mm" if wide else "2.6mm"))
        gap = r"[1.2mm]" if group and i % group == group - 1 and i < len(rows) - 1 else ""
        out.append(" & ".join(line) + r" \\" + gap)
    return out


def title_cell(ar_text, la_text, size=r"\large", bold=True, ncols=5):
    la = "".join(r"\\" + (r"\textbf{" if bold else "{") + markup(x) + "}" for x in la_text.split(" / "))
    return (r"\multicolumn{" + str(ncols) + r"}{||c||}{\parbox{160mm}{\centering\vspace{1mm}{" + size + " "
            + ar(ar_text) + "}" + la + r"\vspace{1mm}}} \\")


def running_head(pp):
    return (r"\noindent\makebox[\textwidth]{\hfill{\scriptsize AL-BATTANI OPUS ASTRONOMICUM}\hfill\llap{" + str(pp) + "}}"
            if pp % 2 else r"\noindent\makebox[\textwidth]{\rlap{" + str(pp) + r"}\hfill{\scriptsize C. A. NALLINO}\hfill}")


def page_start(pp, fol):
    return [r"\clearpage", running_head(pp), r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{1mm}",
            r"\begin{center}{\small " + fol + r"}\end{center}\vspace{-3mm}"]


def spec(argw, centred=True):
    a = (r">{\centering\arraybackslash}p{" if centred else r">{\raggedright\arraybackslash}p{") + argw + "}"
    return "|" + a + "|" + "|".join([r">{\centering\arraybackslash}p{" + COLW + "}"] * 4) + "|"


def simple_page(page, rows, extra, roman=False):
    """pp. 29, 30, 32, 84, 85, 86: one table."""
    out = page_start(int(page["ppage"]), page["fol"])
    out.append(r"\begin{center}\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.05}\begin{tabular}{" + spec("13mm") + r"}\hline\hline")
    out.append(title_cell(page["title_ar"], page["title_la"]) + r" \hline")
    out.append(" & ".join(head_cells(page, "13mm", True)) + r" \\ \hline\hline")
    out += body(rows, page["table"], roman=roman)
    out.append(r"\hline\hline\end{tabular}\end{center}")
    if page["ppage"] == "32":
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


def page87(pages, rows):
    """p. 87: the parts of a month, the Roman months (with the sums of their days) and the intervals of years in one
    frame of six columns; the parts and the intervals take the first two columns for their arguments."""
    pa, pb, pc = (next(p for p in pages if p["table"] == t) for t in ("parts", "months", "intervals"))
    R = {t: [r for r in rows if r["table"] == t] for t in ("parts", "months", "intervals")}
    out = page_start(87, pa["fol"])
    colspec = ("|" + r">{\raggedright\arraybackslash}p{21mm}|" + r">{\centering\arraybackslash}p{11mm}|"
               + "|".join([r">{\centering\arraybackslash}p{" + COLW + "}"] * 4) + "|")
    out.append(r"\begin{center}\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.05}\begin{tabular}{" + colspec + r"}\hline\hline")
    out.append(title_cell(pa["title_ar"], pa["title_la"], ncols=6) + r" \hline")
    out += body(R["parts"], "parts", group=0, roman=True, lead=lambda r: [r"\multicolumn{2}{|l|}{" + nl(r["arg"]) + "}"])
    out.append(r"\hline\hline")
    out.append(title_cell(pb["title_ar"], pb["title_la"], ncols=6) + r" \hline")
    heads = [h.split("‖") for h in pb["heads"].split("|")]
    cells = [r"\parbox[c]{21mm}{\centering\scriptsize " + head_text(*heads[0]) + r"\par\vspace{0.7mm}}",
             r"\rotatebox{90}{\scriptsize\begin{tabular}{@{}c@{}}" + head_text(*heads[1]) + r"\end{tabular}}"]
    cells += [r"\parbox[c]{" + COLW + r"}{\centering\scriptsize " + head_text(a, l) + r"\par\vspace{0.7mm}}" for a, l in heads[2:]]
    out.append(" & ".join(cells) + r" \\ \hline\hline")
    out += body(R["months"], "months", roman=True, lead=lambda r: [nl(r["arg"]), r["sumdays"]])
    out.append(r"\hline\hline")
    out.append(r"\multicolumn{6}{||c||}{\rule{0pt}{5mm}\textbf{" + markup(pc["title_la"]) + r"} (\textarabic{"
               + pc["title_ar"] + r"}).} \\[1mm] \hline")
    out += body(R["intervals"], "intervals", group=0, roman=True,
                lead=lambda r: [r"\multicolumn{2}{|c|}{" + r["arg"] + "}"])
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
    rpages = read("rsyz_pages.tsv"); rrows = read("rsyz_p2.tsv")
    for page in rpages:
        t = page["table"]
        if t in ("conj", "opp", "single"):
            out.append(simple_page(page, [r for r in rrows if r["table"] == t], extra, roman=True))
        elif t == "parts":
            out.append(page87(rpages, rrows))
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p2_syzygies.tex").write_text(document(), encoding="utf-8", newline="\n")
    print("wrote p2_syzygies.tex")

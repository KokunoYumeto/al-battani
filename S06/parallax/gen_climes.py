"""The pages of Nallino's Part II pp. 95-101 (the parallaxes of the Moon in longitude and latitude in the seven climes)
for p2_parallax.tex, from clime_p2.tsv and clime_pages.tsv: one page per printed page, the two halves in one frame with
the folio line of the lower half between them; for each sign a column of hours and the parallaxes in longitude and
latitude, the rows on the lines of the print (blank lines kept), the marks «bor.» and «austr.» over their values."""
import re
from gen_stars import markup, read

SIGNS = {"top": ["Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius"],
         "bot": ["Capricorn", "Aquarius", "Pisces", "Aries", "Taurus", "Gemini"]}


def ar(s):
    return r"\\".join(r"\textarabic{" + markup(x, False) + "}" for x in s.split(" / "))


def nl(s):
    return markup(s).replace(" / ", r"\\")


def hour(h):
    m = re.match(r"(\d+)ʰ(?: (\d+)′)?$", h)
    if not m:
        return h
    return m.group(1) + r"\textsuperscript{h}" + (r"\,\makebox[\Mw][r]{" + m.group(2) + r"}′" if m.group(2) else "")


def lat_cell(r, first):
    v = (r["north"] or "") + r["lat"] + ("′" if first else "")
    if r["mark"]:
        v = r"\smash{\rlap{\raisebox{1.75ex}{\tiny\hspace{-1.2mm}" + r["mark"] + "}}}" + v
    return v


def half_rows(page, rows):
    signs = SIGNS[page["half"]]
    n = int(page["lines"])
    space = {int(x) for x in page["space_before"].split()}
    by = {(r["sign"], int(r["line"])): r for r in rows}
    out = []
    for line in range(1, n + 1):
        cells = []
        for sign in signs:
            r = by.get((sign, line))
            if r is None:
                cells += ["", "", ""]
                continue
            first = r["row"] == "1"
            cells += [hour(r["hour"]), r["long"] + ("′" if first else ""), lat_cell(r, first)]
        gap = "[1.6mm]" if (line + 1) in space else ""
        out.append(" & ".join(cells) + r" \\" + gap)
    return out


def heads(page):
    hs = [h.split("‖") for h in page["heads"].split("|")]
    top, sub = [], []
    for k in range(0, 12, 2):
        a, l = hs[k]
        text = (ar(a) + r"\\" if a else "") + nl(l)
        top.append(r"\rotatebox{90}{\parbox{17mm}{\centering\tiny " + text + "}}")
        a, l = hs[k + 1]
        text = (ar(a) + r"\\" if a else "") + nl(l)
        top.append(r"\multicolumn{2}{c|}{\parbox[c]{14mm}{\centering\tiny " + text + "}}")
    for k in range(6):
        sub += ["", r"{\scriptsize Long.}", r"{\scriptsize Lat.}"]
    return " & ".join(top) + r" \\ " + "".join(r"\cline{" + f"{3 * k + 2}-{3 * k + 3}" + "}" for k in range(6)) + "\n" + \
        " & ".join(sub) + r" \\ \hline\hline"


def page(pp, pages, rows, running_head):
    top = next(p for p in pages if p["ppage"] == pp and p["half"] == "top")
    bot = next(p for p in pages if p["ppage"] == pp and p["half"] == "bot")
    out = [r"\clearpage", running_head(int(pp)), r"\par\vspace{-1mm}\noindent\rule{\textwidth}{.4pt}\par\vspace{1mm}",
           r"\begin{center}{\small " + top["fol"] + r"}\end{center}\vspace{-3mm}"]
    spec = "||" + "||".join(r">{\centering\arraybackslash}p{9mm}|>{\raggedleft\arraybackslash}p{6mm}"
                            r">{\raggedright\arraybackslash}p{9mm}" for _ in range(6)) + "||"
    out.append(r"\begin{center}\small\setlength{\tabcolsep}{1.6pt}\renewcommand{\arraystretch}{1.0}\begin{tabular}{" + spec
               + r"}\hline\hline")
    la = "".join(r"\\\textbf{" + markup(x) + "}" for x in top["title_la"].split(" / "))
    out.append(r"\multicolumn{18}{||c||}{\parbox{160mm}{\centering\vspace{1mm}{\large " + ar(top["title_ar"]) + "}" + la
               + r"\vspace{1mm}}} \\ \hline")
    out.append(heads(top))
    R = [r for r in rows if r["ppage"] == pp]
    out += half_rows(top, [r for r in R if r["sign"] in SIGNS["top"]])
    out.append(r"\hline\hline\multicolumn{18}{||c||}{\rule{0pt}{4mm}\small " + bot["fol"] + r"} \\ \hline\hline")
    out.append(heads(bot))
    out += half_rows(bot, [r for r in R if r["sign"] in SIGNS["bot"]])
    out.append(r"\hline\hline\end{tabular}\end{center}")
    if bot.get("signature"):
        out.append(r"\vspace{-2mm}\noindent\hfill{\small " + bot["signature"] + r"}\hspace*{10mm}")
    return "\n".join(out)


def pages_tex(running_head):
    pages = read("clime_pages.tsv"); rows = read("clime_p2.tsv")
    return [page(pp, pages, rows, running_head) for pp in ("95", "96", "97", "98", "99", "100", "101")]

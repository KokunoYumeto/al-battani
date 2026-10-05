"""Generate the two editions of the astrological figure («rosa astrologica») from the checked TSV data:
  p3_rosa.tex - Part III p. 244 (the codex figure, Arabic, codex errors kept), as printed
  p2_rosa.tex - Part II p. 299 (Nallino's emended Latin figure), as printed
Drawn with TikZ on the measured geometry of the master scan (radii in pt, scaled), every text at its printed place:
  Part III: terms and faces along the radius, starting at the inner circle, letter tops toward the clockwise side;
  triplicities, ring 1 and the sign names along the circles, tops outward.
  Part II: terms (name at the outer end, degrees at the inner end) and faces along the radius, from the outer end;
  triplicity and exaltation symbols, houses and sign names along the circles, tops outward."""
from pathlib import Path

from gen_stars import AR_DIGITS, markup, read
from gen_climates import PRE, ar, lat, node, polar

HERE = Path(__file__).resolve().parent
P3 = [77.4, 115.9, 153.9, 182.0, 209.1, 263.9]
P2 = [40.5, 56.0, 71.5, 109.0, 147.0, 193.5]
P2_DASHED = 128.0
SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn",
         "Aquarius", "Pisces"]
SYMBOLS = set("☉☽☿♀♂♃♄☊☋")
PRE_R = PRE.replace(r"\newcommand{\AbjadZero}", r"\newfontfamily\astrofont{DejaVu Sans}" "\n" r"\newcommand{\AbjadZero}")


def astro(s):
    """Latin text with the planet symbols in a font that has them."""
    return "".join(r"{\astrofont " + c + "}" if c in SYMBOLS else c for c in s)


def frame(radii, lines0, dashed=None):
    out = [rf"\draw[line width=0.5pt] (0,0) circle ({r});" for r in radii]
    if dashed:
        out.append(rf"\draw[line width=0.4pt,dash pattern=on 2pt off 1.5pt] (0,0) circle ({dashed});")
    out += [rf"\draw[line width=0.5pt] ({t}:{radii[0]}) -- ({t}:{radii[-1]});" for t in lines0]
    return out


def by_sign(rows, kind):
    return {(r["sign"], r["idx"]): r for r in rows if r["kind"] == kind}


def p3_figure(rows, scale):
    start = {s: (89 + 30 * i) % 360 for i, s in enumerate(SIGNS)}
    out = [rf"\begin{{tikzpicture}}[x={scale}pt,y={scale}pt]"] + frame(P3, [(89 + 30 * k) % 360 for k in range(12)])
    for r in rows:
        k = r["kind"]
        if k == "term":
            t = float(r["t"])
            x, y = polar(t, P3[4] + 3); out.append(node(x, y, t + 180, "east", ar(r["planet"]), r"\footnotesize"))
            x, y = polar(t, P3[5] - 7); out.append(node(x, y, t + 180, "center", ar(r["value"]), r"\footnotesize"))
        elif k == "face":
            t = float(r["t"]); x, y = polar(t, (P3[1] + P3[2]) / 2)
            out.append(node(x, y, t + 180, "center", ar(r["planet"]), r"\footnotesize"))
        elif k == "trip":
            t = start[r["sign"]] + 15; rr = (P3[3] + P3[4]) / 2 if r["idx"] == "1" else (P3[2] + P3[3]) / 2
            x, y = polar(t, rr); out.append(node(x, y, t - 90, "center", ar(r["text"]), r"\footnotesize"))
        elif k == "ring1":
            t = start[r["sign"]] + 15; x, y = polar(t, (P3[0] + P3[1]) / 2)
            lines = r"\\".join(ar(s) for s in r["text"].split(" / "))
            out.append(node(x, y, t - 90, "center", lines, r"\scriptsize", align="center"))
        elif k == "sign":
            t = float(r["t"]); x, y = polar(t, P3[5] + 10)
            out.append(node(x, y, t - 90, "center", ar(r["text"]), r"\normalsize"))
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def p2_figure(rows, scale):
    start = {s: (90 + 30 * i) % 360 for i, s in enumerate(SIGNS)}
    out = [rf"\begin{{tikzpicture}}[x={scale}pt,y={scale}pt]"] + frame(P2, [30 * k for k in range(12)], P2_DASHED)
    for r in rows:
        k = r["kind"]
        if k == "term":
            t = float(r["t"])
            x, y = polar(t, P2[5] - 3); out.append(node(x, y, t + 180, "west", lat(r["planet"]), r"\scriptsize\bfseries"))
            x, y = polar(t, P2[4] + 6); out.append(node(x, y, t + 180, "center", lat(r["value"]), r"\scriptsize\bfseries"))
        elif k == "face":
            t = float(r["t"]); x, y = polar(t, (P2[2] + P2[3]) / 2)
            out.append(node(x, y, t + 180, "center", lat(r["planet"]), r"\scriptsize\bfseries"))
        elif k == "trip":
            t = start[r["sign"]] + 15; rr = (P2_DASHED + P2[4]) / 2 if r["idx"] == "1" else (P2[3] + P2_DASHED) / 2
            x, y = polar(t, rr); out.append(node(x, y, t - 90, "center", astro(r["text"].replace(" ", r"\ \ ")), r"\small"))
        elif k == "house":
            t = start[r["sign"]] + 15; x, y = polar(t, (P2[1] + P2[2]) / 2)
            out.append(node(x, y, t - 90, "center", lat(r["planet"]), r"\tiny"))
        elif k == "exalt":
            t = start[r["sign"]] + 15; x, y = polar(t, (P2[0] + P2[1]) / 2)
            text = (astro(r["planet"]) + " " if r["planet"] else "") + lat(r["value"])
            out.append(node(x, y, t - 90, "center", text, r"\scriptsize"))
        elif k == "sign":
            t = float(r["t"]); x, y = polar(t, P2[5] + 6)
            out.append(node(x, y, t - 90, "center", lat(r["text"]), r"\scriptsize\bfseries"))
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def notes(rows, arabic):
    F = [r for r in rows if r["kind"] == "footnote"]
    if arabic:
        return " --- ".join(f"{r['idx']}) " + markup(r["text"]) for r in F)
    return r"\par ".join(f"({r['idx']}) " + markup(r["text"]) for r in F)


def p3_document():
    rows = read("rosa_p3.tsv")
    head = {r["idx"]: r["text"] for r in rows if r["kind"] == "header"}
    title = next(r["text"] for r in rows if r["kind"] == "title")
    closing = next(r["text"] for r in rows if r["kind"] == "closing")
    out = [PRE_R, r"\begin{document}",
           r"\noindent\mbox{}\hfill " + head["fol"] + r"\hfill{\large\textarabic{" + head["page"].translate(AR_DIGITS) + r"}}\par\vspace{2mm}",
           r"\begin{Arabic}\noindent " + markup(title, False).replace(r"\textsuperscript", r"\textsuperscript") + r"\end{Arabic}\vspace{-2mm}",
           r"\begin{center}" + p3_figure(rows, 0.86) + r"\end{center}\vspace{-3mm}",
           r"\begin{Arabic}\noindent " + markup(closing, False) + r"\end{Arabic}",
           r"\par\vspace{2mm}\noindent\rule{40mm}{.4pt}\par\vspace{1mm}{\small " + notes(rows, True) + "}",
           r"\end{document}"]
    return "\n".join(out) + "\n"


def p2_document():
    rows = read("rosa_p2.tsv")
    head = {r["idx"]: r["text"] for r in rows if r["kind"] == "header"}
    title = next(r["text"] for r in rows if r["kind"] == "title")
    closing = next(r["text"] for r in rows if r["kind"] == "closing")
    F = [r for r in rows if r["kind"] == "footnote"]
    left = r"\\".join(f"({r['idx']}) " + markup(r["text"]) for r in F[:3])
    right = f"({F[3]['idx']}) " + markup(F[3]["text"])
    out = [PRE_R, r"\begin{document}",
           r"\noindent\rule{\textwidth}{1.2pt}\\[-2.6mm]\rule{\textwidth}{.4pt}\par\vspace{6mm}",
           r"\begin{center}{\small " + head["fol"] + r"}\end{center}\vspace{-1mm}",
           r"\noindent " + markup(title) + r"\par\vspace{-1mm}",
           r"\begin{center}" + p2_figure(rows, 1.12) + r"\end{center}\vspace{-2mm}",
           r"\noindent " + markup(closing) + r"\par\vspace{2mm}",
           r"\begin{center}\rule{40mm}{.4pt}\end{center}\vspace{-2mm}",
           r"{\small\noindent\begin{minipage}[t]{0.45\textwidth}" + left + r"\end{minipage}\hfill\vrule\hfill"
           r"\begin{minipage}[t]{0.5\textwidth}" + right + r"\end{minipage}}",
           r"\end{document}"]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    (HERE / "p3_rosa.tex").write_text(p3_document(), encoding="utf-8")
    (HERE / "p2_rosa.tex").write_text(p2_document(), encoding="utf-8")
    print("wrote p3_rosa.tex, p2_rosa.tex")

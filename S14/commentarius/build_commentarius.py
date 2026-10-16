"""S14 - al-Battani's commentary on Ptolemy's Tetrabiblos (Escorial, RBMSL, ar. 969, ff. 20r-80v), converted from
the transcription by Nadine Loehr in Ptolemaeus Arabus et Latinus (PAL), CC BY 4.0, exact commit
762614d992ac588389f10309cb180e0a34b3459c (source/, unchanged).

The edition keeps PAL's transcription as committed: one line of the edition for each line of the manuscript (PAL's
«||»), anchored AB03-F020r-L01 ...; PAL's editorial signs as PAL sets them ({} uncertain or conjectural, [] to be
deleted, [[ ]] deleted by the scribe, 〈〉 added by the editor, 〈〈 〉〉 added in the margin or between the lines);
PAL's notes (the apparatus, numbered as PAL numbers them); the folio correspondences of the Berlin manuscript
(/B1r/ ...); the chapter headings (I.1-I.40); and the two tables of ff. 80r-80v. Nothing is normalized beyond what
PAL states in its conventions (source/1.xml); the letters are kept as committed (among them the Persian ی and ک).

Writes commentarius.tex, records/AB03-F###x.json, anchors.tsv, apparatus.tsv, berlin.tsv, chapters.tsv,
signs.tsv, tables/*.tsv, source_manifest.tsv and page_disposition.tsv.  python build_commentarius.py"""
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "source"
COMMIT = "762614d992ac588389f10309cb180e0a34b3459c"
ZIP_PREFIX = ("pal-texts-762614d992ac588389f10309cb180e0a34b3459c-762614d992ac588389f10309cb180e0a34b3459c-ms-Escorial, "
              "RBMSL, ár. 969 #689-#1016-text/ms/Escorial, RBMSL, ár. 969 #689/#1016/text/")
LA, RA = "〈", "〉"
ANGLES = {LA: RA, RA: LA, "〈": "〉", "〉": "〈"}
FOLIO = re.compile(r"/B?\d+[rv]/")


class Node:
    def __init__(self, tag, attrs):
        self.tag, self.attrs, self.children = tag, dict(attrs), []


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {})
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs)
        self.stack[-1].children.append(n)
        self.stack.append(n)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def parse(path):
    t = Tree()
    t.feed(path.read_text(encoding="utf-8"))
    return t.root


def text_of(node):
    out = []
    for ch in node.children:
        if isinstance(ch, str):
            out.append(ch)
        elif ch.tag == "span" and "data-prae" in ch.attrs and not ch.children:
            out.append(ch.attrs["data-prae"])
        else:
            out.append(text_of(ch))
    return "".join(out)


# ---------------------------------------------------------------- TeX helpers
def esc(s):
    return (s.replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%").replace("$", r"\$")
            .replace("#", r"\#").replace("_", r"\_").replace("~", r"\textasciitilde{}").replace("^", r"\^{}"))


def esc_rl(s):
    """an Arabic run: TeX specials escaped. The round, square and curly brackets are left as they are written: in a
    right-to-left run Amiri shows them mirrored, as PAL shows them. The angle brackets (U+2329, U+232A) are in a font
    that does not mirror them; each is set as its mirror image in a left-to-right box"""
    out = []
    for ch in s:
        if ch in ANGLES:
            out.append(r"\LR{\Sg{" + ANGLES[ch] + "}}")
        elif ch in "{}":
            out.append("\\" + ch)
        else:
            out.append(esc(ch))
    return "".join(out)


def esc_lr(s):
    out = []
    for ch in s:
        if ch in ANGLES:
            out.append(r"\Sg{" + ch + "}")
        elif ch in "{}":
            out.append("\\" + ch)
        else:
            out.append(esc(ch))
    return "".join(out)


PAL_FIELDS = {"work-siglum": "C.2.2", "work-author": "al-Battānī",
              "work-title": "Sharḥ Kitāb al-Arbaʿ maqālāt fī aḥkām ʿilm al-nujūm", "witness-name": "Escorial, RBMSL, ár. 969"}


def note_tex(node):
    """a note of PAL: Latin (left to right) with Arabic runs (span dir=rtl); the fields that PAL's website fills from
    its catalogue (empty in the files) are filled from PAL's page of the work (source/evidence)"""
    out = []
    for ch in node.children:
        if not isinstance(ch, str) and ch.tag in PAL_FIELDS and not ch.children:
            out.append(r"	extit{" + esc_lr(PAL_FIELDS[ch.tag]) + "}")
            continue
        if isinstance(ch, str):
            out.append(esc_lr(ch))
        elif ch.tag == "span" and "data-prae" in ch.attrs and not ch.children:
            out.append(esc_lr(ch.attrs["data-prae"]))
        elif ch.tag == "span" and ch.attrs.get("dir") == "rtl":
            out.append(r"\RL{\ArN " + esc_rl(text_of(ch)) + "}")
        else:
            out.append(note_tex(ch))
    return "".join(out)


# ---------------------------------------------------------------- the page sides
def walk(node, ctx, out):
    for ch in node.children:
        if isinstance(ch, str):
            out.append(("t", ch, dict(ctx)))
            continue
        tag, a = ch.tag, ch.attrs
        if tag == "span" and "data-prae" in a and not ch.children and a.get("class") != "note":
            v = a["data-prae"]
            if v == "||":
                out.append(("lb",))
            elif FOLIO.fullmatch(v.strip()):
                out.append(("fol", v.strip().strip("/")))
            else:
                out.append(("t", v, dict(ctx)))
            continue
        if tag == "span" and a.get("class") == "note":
            small = next(c for c in ch.children if not isinstance(c, str) and c.tag == "small")
            out.append(("note", small.attrs["data-prae"], small, dict(ctx)))
            continue
        if tag in ("h2", "h3"):
            out.append(("sep",))
            walk(ch, {**ctx, "head": a.get("id"), "dir": a.get("dir", "rtl")}, out)
            out.append(("sep",))
            continue
        if tag == "p":
            out.append(("sep",))
            walk(ch, {**ctx, "dir": a.get("dir", "rtl"), "center": "center" in a.get("style", "")}, out)
            out.append(("sep",))
            continue
        if tag == "table":
            out.append(("table", ch))
            continue
        if tag == "span":
            c = dict(ctx)
            if a.get("data-by") == "hg":
                c["ed"] = True
            if "dir" in a:
                c["dir"] = a["dir"]
            walk(ch, c, out)
            continue
        walk(ch, ctx, out)


def lines_of(tokens):
    """split at the line breaks of the manuscript; the paragraphs and headings of PAL are kept as spaces"""
    lines, cur, tables = [], [], []
    for tk in tokens:
        if tk[0] == "lb":
            lines.append(cur)
            cur = []
        elif tk[0] == "sep":
            cur.append(("t", " ", {}))
        elif tk[0] == "table":
            tables.append(tk[1])
        else:
            cur.append(tk)
    if any(tk[0] != "t" or tk[1].strip() for tk in cur):
        lines.append(cur)
    return lines, tables


def runs(line):
    """merge the text pieces of a line into runs of the same direction, editorial status and heading"""
    out = []
    for tk in line:
        if tk[0] == "t":
            c = tk[2]
            key = (c.get("dir", "rtl"), bool(c.get("ed")), c.get("head"))
            if out and out[-1][0] == "t" and out[-1][2] == key:
                out[-1] = ("t", out[-1][1] + tk[1], key)
            else:
                out.append(("t", tk[1], key))
        else:
            out.append(tk)
    # collapse spaces across the line
    res, prev_space = [], True
    for r in out:
        if r[0] == "t":
            s = re.sub(r"\s+", " ", r[1])
            if prev_space:
                s = s.lstrip(" ")
            if not s:
                continue
            prev_space = s.endswith(" ")
            res.append(("t", s, r[2]))
        else:
            res.append(r)
    while res and res[-1][0] == "t" and res[-1][1].endswith(" "):
        s = res[-1][1].rstrip(" ")
        res[-1] = ("t", s, res[-1][2])
        if not s:
            res.pop()
    return res


def line_tex(rs):
    out = []
    for r in rs:
        if r[0] == "t":
            s, (d, ed, head) = r[1], r[2]
            t = r"\LR{\LatinF " + esc_lr(s) + "}" if d == "ltr" else esc_rl(s)
            if head:
                t = r"\Hd{" + t + "}"
            out.append(t)
        elif r[0] == "note":
            out.append(r"\PN{" + r[1] + "}")
        elif r[0] == "fol":
            out.append(r"\BF{" + r[1] + "}")
    return "".join(out)


def line_plain(rs):
    out = []
    for r in rs:
        if r[0] == "t":
            out.append(r[1])
        elif r[0] == "fol":
            out.append("/" + r[1] + "/")
    return "".join(out).strip()


SIGN = [("[[", "]]", "deleted by the scribe"), (LA + LA, RA + RA, "added in the margin or between the lines"),
        ("{", "}", "uncertain or conjectural reading"), ("[", "]", "in the text but to be deleted (additions, eulogies)"),
        (LA, RA, "added by the editor")]


def signs_of(plain):
    """the editorial signs of a line, outermost first, with what they enclose"""
    found, i = [], 0
    while i < len(plain):
        for op, cl, kind in SIGN:
            if plain.startswith(op, i):
                j = plain.find(cl, i + len(op))
                if j >= 0:
                    found.append((op + cl, kind, plain[i + len(op):j]))
                    i = j + len(cl) - 1
                else:
                    found.append((op + cl, kind + " (opened, closed on a later line)", plain[i + len(op):]))
                    i = len(plain)
                break
        i += 1
    return found


def table_grid(tbl):
    """the cells of an HTML table on a grid: (row, col, rowspan, colspan, node)"""
    rows = [c for c in tbl.children if not isinstance(c, str) and c.tag == "tr"]
    occ, cells = {}, []
    for r, tr in enumerate(rows):
        c = 0
        for td in (x for x in tr.children if not isinstance(x, str) and x.tag == "td"):
            while (r, c) in occ:
                c += 1
            rs, cs = int(td.attrs.get("rowspan", 1)), int(td.attrs.get("colspan", 1))
            for dr in range(rs):
                for dc in range(cs):
                    occ[(r + dr, c + dc)] = True
            cells.append((r, c, rs, cs, td))
            c += cs
    ncol = max(c + cs for r, c, rs, cs, td in cells)
    return len(rows), ncol, cells


def cell_tex(td):
    parts = []
    for div in (x for x in td.children if not isinstance(x, str)):
        bits = []
        for ch in div.children:
            if isinstance(ch, str):
                if ch.strip():
                    bits.append(esc_rl(ch.strip()))
            elif ch.tag == "span" and ch.attrs.get("class") == "note":
                small = next(c for c in ch.children if not isinstance(c, str) and c.tag == "small")
                bits.append(r"\PN{" + small.attrs["data-prae"] + "}")
            else:
                inner = []
                for g in ch.children:
                    if isinstance(g, str):
                        inner.append(esc_rl(g))
                    elif g.attrs.get("class") == "note":
                        small = next(c for c in g.children if not isinstance(c, str) and c.tag == "small")
                        inner.append(r"\PN{" + small.attrs["data-prae"] + "}")
                    else:
                        inner.append(esc_rl(text_of(g)))
                bits.append("".join(inner).strip())
        t = " ".join(b for b in bits if b)
        if t:
            parts.append(r"\RL{\ArT " + t + "}")
    return r"\shortstack{" + r"\\".join(parts) + "}" if len(parts) > 1 else (parts[0] if parts else "")


def table_tex(tbl):
    nrow, ncol, cells = table_grid(tbl)
    at = {(r, c): (rs, cs, td) for r, c, rs, cs, td in cells}
    cover = {}
    for r, c, rs, cs, td in cells:
        for dr in range(rs):
            for dc in range(cs):
                cover[(r + dr, c + dc)] = (r, c)
    out = [r"\begin{tabular}{|" + "c|" * ncol + "}", r"\hline"]
    for r in range(nrow):
        row, c = [], 0
        while c < ncol:
            o = cover.get((r, c))
            if o is None:
                row.append("")
                c += 1
                continue
            r0, c0 = o
            rs, cs, td = at[o]
            body = cell_tex(td) if r0 == r else ""
            if rs > 1 and r0 == r:
                body = r"\multirow{" + str(rs) + "}{*}{" + body + "}"
            row.append(r"\multicolumn{" + str(cs) + "}{|c|}{" + body + "}" if cs > 1 else body)
            c += cs
        out.append(" & ".join(row) + r" \\")
        # the rule under the row, except under the cells that continue in the next row
        segs, c = [], 0
        while c < ncol:
            o = cover.get((r, c))
            cont = o is not None and r + 1 < nrow and cover.get((r + 1, c)) == o
            if not cont:
                segs.append(c + 1)
            c += 1
        if len(segs) == ncol:
            out.append(r"\hline")
        else:
            spans, start = [], None
            for k in range(1, ncol + 2):
                if k in segs and start is None:
                    start = k
                if (k not in segs or k == ncol + 1) and start is not None:
                    end = k - 1 if k not in segs else k
                    spans.append((start, min(end, ncol)))
                    start = None
            out.append("".join(r"\cline{" + f"{a}-{b}" + "}" for a, b in spans))
    out.append(r"\end{tabular}")
    return "\n".join(out), nrow, ncol, cells


def text_no_notes(node):
    out = []
    for ch in node.children:
        if isinstance(ch, str):
            out.append(ch)
        elif ch.attrs.get("class") == "note":
            continue
        elif ch.tag == "span" and "data-prae" in ch.attrs and not ch.children:
            out.append(ch.attrs["data-prae"])
        else:
            out.append(text_no_notes(ch))
    return "".join(out)


def notes_in(node):
    out = []
    for ch in node.children:
        if isinstance(ch, str):
            continue
        if ch.attrs.get("class") == "note":
            small = next(c for c in ch.children if not isinstance(c, str) and c.tag == "small")
            out.append(small.attrs["data-prae"])
        else:
            out += notes_in(ch)
    return out


def table_rows(tbl):
    """the cells of a table for its TSV: the lines of a cell joined with « / », its notes by their numbers"""
    nrow, ncol, cells = table_grid(tbl)
    out = []
    for r, c, rs, cs, td in cells:
        txt = " / ".join(re.sub(r"\s+", " ", text_no_notes(div)).strip() for div in td.children if not isinstance(div, str))
        out.append((r + 1, c + 1, rs, cs, txt, " ".join(notes_in(td))))
    return out


PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[a4paper,left=24mm,right=30mm,top=22mm,bottom=22mm,headheight=14pt]{geometry}
\usepackage{fontspec,multirow,array,graphicx}
\usepackage[unicode,hidelinks]{hyperref}
\usepackage{polyglossia}
\setmainlanguage{english}
\setotherlanguages{arabic}
\setmainfont{Linux Libertine O}[Ligatures=TeX]
\newfontfamily\arabicfont{Amiri}[Script=Arabic]
\newfontfamily\ArBody{Amiri}[Script=Arabic,Scale=1.08]
\newfontfamily\ArN{Amiri}[Script=Arabic,Scale=0.95]
\newfontfamily\ArT{Amiri}[Script=Arabic,Scale=0.9]
\newfontfamily\SgFont{Yu Gothic}
\newfontfamily\LatinF{Linux Libertine O}
\newcommand{\Sg}[1]{{\SgFont #1}}
\hypersetup{pdftitle={al-Battani, Commentary on Ptolemy's Tetrabiblos (Escorial, RBMSL, ar. 969, ff. 20r-80v). After the PAL transcription by Nadine Loehr. S14},pdfauthor={al-Battani; transcription: Nadine Loehr, Ptolemaeus Arabus et Latinus (CC BY 4.0)}}
\setlength{\parindent}{0pt}\setlength{\parskip}{0pt}
\tracinglostchars=2
\makeatletter
\def\ps@ms{\def\@oddhead{\hbox to\textwidth{\footnotesize AL-BATTĀNĪ — COMMENTARY ON THE TETRABIBLOS (ESCORIAL ÁR. 969)\hfil\leftmark}}%
\let\@evenhead\@oddhead\def\@oddfoot{\hbox to\textwidth{\footnotesize\rightmark\hfil\thepage}}\let\@evenfoot\@oddfoot}
\makeatother
\pagestyle{ms}
\newcommand{\Folio}[2]{\par\bigskip\penalty-200\markboth{f. #2}{AB03-F#1}\pdfbookmark[1]{f. #2}{f-#1}%
 \hypertarget{AB03-F#1}{}{\large\bfseries f.\,#2}\par\smallskip}
\newcommand{\Chap}[2]{\pdfbookmark[2]{#2}{ch-#1}}
\newsavebox{\LBox}
% one line of the manuscript, right to left, its number in the right margin; a line longer than the measure (a
% marginal addition set in the line) runs on, right-aligned, to the next line of the page
\newcommand{\MsL}[3]{\par\noindent\hypertarget{#2}{}\hbox to\linewidth{\parbox[t]{\linewidth}{\setRTL\ArBody\raggedleft #3\par}\rlap{\hspace{3mm}\footnotesize #1}}\par}
\newcommand{\MsLc}[3]{\par\noindent\hypertarget{#2}{}\hbox to\linewidth{\parbox[t]{\linewidth}{\setRTL\ArBody\centering #3\par}\rlap{\hspace{3mm}\footnotesize #1}}\par}
\newcommand{\Hd}[1]{{\bfseries #1}}
\newcommand{\PN}[1]{\LR{\textsuperscript{\fontsize{7}{7}\selectfont #1}}}
\newcommand{\BF}[1]{\LR{\fontsize{8}{8}\selectfont\,/#1/\,}}
\newenvironment{PNotes}{\par\smallskip\noindent\rule{40mm}{0.4pt}\par\footnotesize}{\par}
\newcommand{\PNote}[3]{\par\hangindent=6mm\hypertarget{#2}{}\textbf{#1}\enspace #3}
\begin{document}
"""


def front_matter(work):
    """the title page and PAL's introduction, conventions and sigla, as PAL gives them (source/1.xml)"""
    art = next(n for n in work.children if not isinstance(n, str) and n.tag == "main")
    intro = []
    def pick(node):
        for ch in node.children:
            if isinstance(ch, str):
                continue
            if ch.tag == "p" and not ch.attrs.get("class") and ch.attrs.get("dir") != "rtl":
                intro.append(("p", ch))
            elif ch.tag == "li":
                intro.append(("li", ch))
            elif ch.tag in ("nav",):
                continue
            else:
                pick(ch)
    pick(art)
    out = [r"\thispagestyle{empty}",
           r"\begin{center}\Large AL-BATTĀNĪ\par\vspace{4mm}\LARGE Commentary on Ptolemy’s \textit{Tetrabiblos}\par"
           r"\vspace{3mm}\large\RL{\ArBody شرح أبي عبد الله محمّد بن جابر بن سنان الحرّانيّ المعروف بالبتّانيّ على كتاب الأربع مقالات لبطلميوس}\par"
           r"\vspace{5mm}\large Escorial, Real Biblioteca de San Lorenzo, árabe 969, ff.\,20r–80v\par\vspace{6mm}"
           r"\normalsize After the transcription by Nadine Löhr, \textit{Ptolemaeus Arabus et Latinus. Texts}\\"
           r"(https://ptolemaeus.badw.de/text/M1016), CC BY 4.0, commit \texttt{" + COMMIT[:12] + r"}\par"
           r"\vspace{4mm}\large S14 --- edition of the source, line by line\end{center}\vspace{6mm}",
           r"\noindent Every line of this edition is one line of the manuscript as Nadine Löhr’s transcription "
           r"divides it (her «||»), numbered in the right margin and anchored \texttt{AB03-F020r-L01} and so on. "
           r"The text, the editorial signs, the notes, the folio correspondences of the Berlin manuscript "
           r"(\texttt{/B1r/}) and the chapter headings are hers, unchanged; the notes stand after each page of the "
           r"manuscript, with her numbers. This conversion was made by an AI (Claude) without the images of the "
           r"manuscript; no person has reviewed it. The transcription is licensed CC BY 4.0, and so is this edition "
           r"of it. Her introduction follows; the fields that PAL’s website fills from its catalogue (the siglum, author and title of the work and the name of the witness), empty in the files, are filled from PAL’s page of the work, C.2.2 (in italics).\par\medskip\sloppy"]
    for kind, node in intro:
        t = note_tex(node).strip()
        if not t:
            continue
        out.append((r"\par\hangindent=4mm\noindent\textbullet\ " if kind == "li" else r"\par\smallskip\noindent ") + t)
    out.append(r"\par\clearpage")
    return "\n".join(out)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def folio_key(p):
    m = re.search(r"#(\d+)([rv])", p.name)
    return int(m.group(1)), m.group(2)


def main():
    pages = sorted((SRC / "pages").glob("1#*.xml"), key=folio_key)
    work = parse(SRC / "1.xml")
    tex = [PREAMBLE, front_matter(work)]
    anchors, appar, berlin, chapters, signs, manifest, disp = [], [], [], [], [], [], []
    manifest.append(("1.xml", ZIP_PREFIX + "1.xml", sha(SRC / "1.xml")))
    (HERE / "records").mkdir(exist_ok=True)
    (HERE / "tables").mkdir(exist_ok=True)
    seen_heads = set()
    for p in pages:
        n, side = folio_key(p)
        fol = f"{n:03d}{side}"
        manifest.append((f"pages/{p.name}", ZIP_PREFIX + "pages/" + p.name, sha(p)))
        root = parse(p)
        toks = []
        walk(root, {"dir": "rtl"}, toks)
        lines, tables = lines_of(toks)
        tex.append(r"\Folio{" + fol + "}{" + f"{n}{side}" + "}")
        rec = {"anchor": f"AB03-F{fol}", "folio": f"{n}{side}", "source_file": f"source/pages/{p.name}",
               "source_sha256": sha(p), "pal_commit": COMMIT, "lines": [], "notes": [], "tables": []}
        notes_here = []
        for k, ln in enumerate(lines, 1):
            rs = runs(ln)
            aid = f"AB03-F{fol}-L{k:02d}"
            plain = line_plain(rs)
            center = any(tk[0] == "t" and tk[2].get("center") for tk in ln)
            for r in rs:
                if r[0] == "t" and r[2][2]:
                    hid = r[2][2]
                    if not chapters or chapters[-1][0] != hid:
                        chapters.append([hid, aid, r[1].strip()])
                    else:
                        chapters[-1][2] += r[1]
            for tk in ln:
                if tk[0] == "note":
                    notes_here.append((tk[1], aid, tk[2]))
                if tk[0] == "fol":
                    berlin.append((tk[1], aid))
            for kind_sign, kind, inner in signs_of(plain):
                signs.append((aid, kind_sign, kind, inner))
            body = line_tex(rs)
            for r in rs:
                if r[0] == "t" and r[2][2] and r[2][2] not in seen_heads:
                    seen_heads.add(r[2][2])
                    head_text = " ".join(x[1].strip() for x in rs if x[0] == "t" and x[2][2] == r[2][2])
                    tex.append(r"\Chap{" + r[2][2] + "}{" + re.sub(r"\s+", " ", head_text).replace("〈", "<")
                               .replace("〉", ">") + "}")
            tex.append((r"\MsLc{" if center else r"\MsL{") + str(k) + "}{" + aid + "}{" + body + "}")
            anchors.append((aid, f"{n}{side}", str(k), plain))
            rec["lines"].append({"id": aid, "n": k, "text": plain, "tex": body, "centred": center,
                                 "notes": [tk[1] for tk in ln if tk[0] == "note"],
                                 "berlin": [tk[1] for tk in ln if tk[0] == "fol"]})
        for t, tbl in enumerate(tables, 1):
            tid = f"AB03-F{fol}-T{t:02d}"
            ttex, nrow, ncol, cells = table_tex(tbl)
            tex.append(r"\par\medskip\hypertarget{" + tid + r"}{}\begin{center}\footnotesize\setlength{\tabcolsep}{2.5pt}"
                       r"\renewcommand{\arraystretch}{1.05}\resizebox{\ifdim\width>\linewidth\linewidth\else\width\fi}{!}{"
                       + ttex + r"}\end{center}")
            rows = table_rows(tbl)
            with open(HERE / "tables" / f"{tid}.tsv", "w", encoding="utf-8", newline="\n") as fh:
                fh.write("row\tcol\trowspan\tcolspan\ttext\tnotes\n")
                for r_ in rows:
                    fh.write("\t".join(str(x) for x in r_) + "\n")
            rec["tables"].append({"id": tid, "rows": nrow, "columns": ncol, "cells": len(cells),
                                  "file": f"tables/{tid}.tsv"})
            for cell in cells:
                for d in cell[4].children:
                    if isinstance(d, str):
                        continue
                    for sp in d.children:
                        if isinstance(sp, str):
                            continue
                        for g in sp.children:
                            if not isinstance(g, str) and g.attrs.get("class") == "note":
                                small = next(c for c in g.children if not isinstance(c, str) and c.tag == "small")
                                notes_here.append((small.attrs["data-prae"], tid, small))
        if notes_here:
            tex.append(r"\begin{PNotes}")
            for num, aid, small in notes_here:
                nt = note_tex(small).strip()
                tex.append(r"\PNote{" + num + "}{" + f"AB03-n{int(num):03d}" + "}{" + nt + "}")
                plain_note = re.sub(r"\s+", " ", text_of(small)).strip()
                appar.append((f"AB03-n{int(num):03d}", num, aid, plain_note))
                rec["notes"].append({"id": f"AB03-n{int(num):03d}", "n": int(num), "line": aid, "text": plain_note})
            tex.append(r"\end{PNotes}")
        (HERE / "records" / f"AB03-F{fol}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1) + "\n",
                                                           encoding="utf-8", newline="\n")
        kind = ("table" if tables and not lines else "title page" if fol == "020r" else
                "blank page (PAL: «a blank page»)" if not lines or (len(lines) == 1 and "سهو" in anchors[-1][3]) else "text")
        disp.append((f"AB03-F{fol}", f"{n}{side}", kind, str(len(lines)), str(len(tables)), f"source/pages/{p.name}"))
    tex.append(r"\end{document}")
    (HERE / "commentarius.tex").write_text("\n".join(tex) + "\n", encoding="utf-8", newline="\n")

    def tsv(name, head, rows):
        with open(HERE / name, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\t".join(head) + "\n")
            for r in rows:
                fh.write("\t".join(str(x).replace("\t", " ").replace("\n", " ") for x in r) + "\n")
    tsv("anchors.tsv", ["anchor", "folio", "line", "text"], anchors)
    tsv("apparatus.tsv", ["note", "pal_number", "anchor", "text"], appar)
    tsv("berlin.tsv", ["berlin_folio", "escorial_anchor"], berlin)
    tsv("chapters.tsv", ["pal_id", "anchor", "heading"], [(a, b, re.sub(r"\s+", " ", c).strip()) for a, b, c in chapters])
    tsv("signs.tsv", ["anchor", "sign", "kind", "enclosed"], signs)
    tsv("source_manifest.tsv", ["file", "zip_member", "sha256"], manifest)
    tsv("page_disposition.tsv", ["anchor", "folio", "content", "lines", "tables", "source"], disp)
    print(f"{len(pages)} page sides, {len(anchors)} lines, {len(appar)} notes, {len(berlin)} Berlin folios, "
          f"{len(chapters)} headings, {len(signs)} editorial signs")


if __name__ == "__main__":
    main()

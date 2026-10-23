"""The English of the tables of Part III: Nallino's notice, the chronological and the geographical tables, the
star catalogue and the tables of the stars for the year 1211. The Arabic and its numbers come from S13, where every
printed row is transcribed and joined with Nallino's Latin version (Part II) and with the readings of the codex that
his notes report. tables/*.tsv give the English of every row of the Arabic that has text:

  KEY <tab> ENGLISH [<tab> NALLINO'S READING]

KEY is the master PDF page and the printed row of S13 (for example 924:R02). A row of column heads gives its heads
separated by |, as the Arabic does; «^» marks a line translated together with the line above it. The numbers are
decoded from the abjad of Part III (Maghribi values). Where Nallino corrects the codex in Part II, his value is given
and marked *, with the codex reading in the notes; where Part II differs from Part III without a note of his, Part III
is given and marked †, with Part II's value in the notes.

python build_tables.py   (writes tables_en.tex; build_en.py calls it, and any coverage error stops the build)"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S13 = HERE.parent / "S13"


def read_tsv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE))


def read_en(name):
    path = HERE / "tables" / f"{name}.tsv"
    if not path.exists():
        return None
    out = {}
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip() or raw.startswith("#"):
            continue
        parts = raw.split("\t")
        if parts[0] in out:
            raise SystemExit(f"tables/{name}.tsv line {n}: {parts[0]} twice")
        out[parts[0]] = parts[1:] + [""] * (3 - len(parts[1:]))
    return out


def tex(s):
    s = (s.replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%").replace("$", r"\$")
         .replace("#", r"\#").replace("_", r"\_").replace("{", r"\{").replace("}", r"\}"))
    s = re.sub(r"\*([^*]+)\*", r"\\emph{\1}", s)
    return re.sub(r"([؀-ۿ][؀-ۿ\s]*[؀-ۿ]|[؀-ۿ])", r"\\RL{\\ArNote \1}", s)


def statuses(row):
    """field -> status, from the joined status column (for example «lon_d:codex note; lon_m:codex note»)"""
    out = {}
    for part in row.get("status", "").split(";"):
        if ":" in part:
            f, st = part.split(":", 1)
            out[f.strip()] = st.strip()
    return out


def value(row, f, notes, label, show=str):
    """the number of field f as the English gives it, marked; its note goes to notes. show turns a stored value
    (for example «b» or «4 magna») into its English form"""
    st = statuses(row).get(f, "")
    v, p2, codex = row.get(f, ""), row.get(f"p2_{f}", ""), row.get(f"codex_{f}", "")
    if st == "codex note":
        notes.append(f"{label}: codex {show(codex or v)}")
        return f"{show(p2)}*"
    if st == "ledgered":
        notes.append(f"{label}: Part II {show(p2) if p2 else '–'}")
        return f"{show(v)}†"
    return show(v if v != "" else p2)


def coverage(name, rows, en, keyf):
    """every row with text has its English once, and the English has no other keys"""
    need = {keyf(r) for r in rows}
    missing = sorted(need - set(en))
    extra = sorted(set(en) - need)
    errors = []
    if missing:
        errors.append(f"tables/{name}.tsv: not translated: {', '.join(missing[:8])}"
                      f"{' …' if len(missing) > 8 else ''} ({len(missing)})")
    if extra:
        errors.append(f"tables/{name}.tsv: no such row: {', '.join(extra[:8])}")
    return errors


def head(title, ident, page=""):
    mark = r"\ArPage{" + page + "}" if page else ""
    return (r"\par\needspace{8\baselineskip}\bigskip\pdfbookmark[1]{" + title + "}{tab-" + ident + "}" +
            r"{\large\bfseries " + tex(title) + r"\par}" + mark + r"\nobreak\medskip" + "\n")


def pagerow(ncols, page):
    return r"\multicolumn{" + str(ncols) + r"}{l}{\footnotesize\color{gray}Ar.\,p.\," + page + r"}\\"


def notice(en, errors):
    rows = read_tsv(S13 / "notice" / "note227.tsv")
    errors += coverage("notice", rows, en, lambda r: f"925:{r['line']}")
    if errors:
        return ""
    body = " ".join(en[f"925:{r['line']}"][0] for r in rows if r["kind"] == "line" and en[f"925:{r['line']}"][0] != "^")
    ends = "".join(r"\par{\centering " + tex(en[f"925:{r['line']}"][0]) + r"\par}" for r in rows if r["kind"] == "end")
    return head(en["925:T01"][0], "notice", "227") + tex(body) + ends


def chronology(en, errors):
    p3 = read_tsv(S13 / "chronology" / "chr_p3.tsv")
    joined = {(r["pdf"], r["row"]): r for r in read_tsv(S13 / "chronology" / "chronology_joined.tsv")}
    errors += coverage("chronology", p3, en, lambda r: f"{r['pdf']}:{r['line']}")
    if errors:
        return ""
    ncols = {"K": 5, "I": 3, "C": 8}
    specs = {"K": "L{38mm}L{38mm}R{13mm}R{13mm}L{32mm}", "I": "L{96mm}R{12mm}L{30mm}",
             "C": "L{46mm}R{10mm}R{10mm}R{10mm}R{10mm}R{10mm}R{10mm}L{26mm}"}
    wide = r">{\raggedright\arraybackslash}p{140mm}"
    out, section, page, pending = [head("The chronological tables", "chronology")], None, None, None

    def close():
        if section:
            out.append(r"\end{longtable}}")

    for r in p3:
        e = en[f"{r['pdf']}:{r['line']}"]
        if r["ppage"] != page:
            page, pending = r["ppage"], r["ppage"]
        if r["kind"] in ("above", "title"):
            close()
            section = None
            out.append(r"\par\needspace{6\baselineskip}\smallskip{\centering\bfseries " + tex(e[0]) +
                       r"\par}\nopagebreak" + (r"\ArPage{" + pending + "}" if pending else ""))
            pending = None
            continue
        if r["kind"] == "colhead":
            if section == r["section"]:
                continue
            close()
            section = r["section"]
            h = [tex(x) for x in e[0].split("|")]
            out.append(r"{\small\setlength{\tabcolsep}{3pt}\begin{longtable}{" + specs[section] + "}")
            if section == "K":
                out.append(r"\textbf{" + h[0] + r"} & \textbf{Nallino's reading} & \textbf{" + h[1] + r"} & \textbf{" +
                           h[2] + r"} & \textbf{Notes}\\\hline\endhead")
            else:
                three = r"\multicolumn{3}{>{\centering\arraybackslash}p{33mm}}"   # a «c» span would widen the table
                out.append(r"\textbf{" + h[0] + r"} & " + three + r"{\textbf{" + h[1] + r"}} & " + three +
                           r"{\textbf{" + h[2] + r"}} & \textbf{Notes}\\")
                out.append(" & " + " & ".join(r"{\footnotesize\bfseries " + x + "}" for x in h[3:9]) +
                           r" & \\\hline\endhead")
            continue
        if section is None:
            section = r["section"]
            out.append(r"{\small\setlength{\tabcolsep}{3pt}\begin{longtable}{" + specs[section] + "}")
            out.append(r" & \textbf{Years} & \textbf{Notes}\\\hline\endhead")
        if pending:
            out.append(pagerow(ncols[section], pending))
            pending = None
        if r["kind"] == "heading":
            out.append(r"\multicolumn{" + str(ncols[section]) + "}{" + wide + r"}{\emph{" + tex(e[0]) + r"}}\\")
            continue
        j = joined[(r["pdf"], r["line"])]
        notes = []
        if section == "C":
            nums = [value(j, f, notes, lab) for f, lab in (("reg_y", "years"), ("reg_m", "months"), ("reg_d", "days"),
                    ("sum_y", "total years"), ("sum_m", "total months"), ("sum_d", "total days"))]
            cells = [tex(e[0])] + nums
        elif section == "I":
            cells = [tex(e[0]), value(j, "reg_y", notes, "years")]
        else:
            cells = [tex(e[0]), tex(e[1]), value(j, "reg_y", notes, "years"), value(j, "sum_y", notes, "total")]
        out.append(" & ".join(cells + [tex("; ".join(notes))]) + r"\\")
    close()
    return "\n".join(out)


def geography(en, errors):
    p3 = read_tsv(S13 / "geography" / "geo_p3.tsv")
    joined = {(r["pdf"], r["row"]): r for r in read_tsv(S13 / "geography" / "geography_joined.tsv")}
    errors += coverage("geography", p3, en, lambda r: f"{r['pdf']}:{r['line']}")
    if errors:
        return ""
    spec = "R{8mm}L{42mm}L{34mm}R{7mm}R{6mm}R{6mm}R{6mm}L{24mm}"
    out, opened, section, page, pending = [head("The geographical tables", "geography")], False, None, None, None

    def close():
        if opened:
            out.append(r"\end{longtable}}")

    for r in p3:
        e = en[f"{r['pdf']}:{r['line']}"]
        if r["ppage"] != page:
            page, pending = r["ppage"], r["ppage"]
        if r["kind"] in ("title", "fol"):
            close()
            opened = False
            size = r"\footnotesize" if r["kind"] == "fol" else r"\bfseries"
            out.append(r"\par\needspace{6\baselineskip}\smallskip{\centering" + size + " " + tex(e[0]) +
                       r"\par}\nopagebreak" + (r"\ArPage{" + pending + "}" if pending else ""))
            pending = None
            continue
        if r["kind"] == "colhead":
            if opened:
                continue
            opened = True
            out.append(r"{\small\setlength{\tabcolsep}{3pt}\begin{longtable}{" + spec + "}")
            out.append(r"\textbf{No.} & \textbf{" + tex(e[0]) + r"} & \textbf{The place} & "
                       r"\multicolumn{2}{c}{\footnotesize\bfseries Longitude} & "
                       r"\multicolumn{2}{c}{\footnotesize\bfseries Latitude} & "
                       r"\textbf{Notes}\\")
            out.append(r" & & & ° & ′ & ° & ′ & \\\hline\endhead")
            continue
        if pending:
            out.append(pagerow(8, pending))
            pending = None
        if section and r["section"] != section:
            out.append(r"\hline")
        section = r["section"]
        j = joined[(r["pdf"], r["line"])]
        notes = []
        nums = [value(j, f, notes, lab) for f, lab in (("lon_d", "longitude °"), ("lon_m", "longitude ′"),
                                                         ("lat_d", "latitude °"), ("lat_m", "latitude ′"))]
        out.append(" & ".join([j.get("no", ""), tex(e[0]), tex(e[1])] + nums + [tex("; ".join(notes))]) + r"\\")
    close()
    return "\n".join(out)


SIDE = {"b": "N", "a": "S", "0": "–"}
MAG = {"magna": "greater", "parva": "lesser", "obscura": "faint", "nebulosa": "nebulous", "conspicua": "conspicuous"}
IDENT = {"10 Leo. M.": "10 LMi", "12 Canum": "12 CVn", "2 Ceti.": "2 Cet", "6 Ceti.": "6 Cet", "7 Ceti.": "7 Cet",
         "21 Comae": "21 Com", "4 Comae": "4 Com", "31 Lync.": "31 Lyn", "40 Lync.": "40 Lyn", "40 Ophi": "40 Oph",
         "71 Leo.": "71 Leo", "α Andr.": "α And", "α Columbae.": "α Col", "β Columbae.": "β Col",
         "α Piscis Austr.": "α PsA"}


def ident(raw, abbr):
    """Nallino's identification in the usual modern form: a letter of his takes the constellation it stands under"""
    raw = raw.replace("ϰ", "κ")
    if not raw:
        return ""
    if raw in IDENT:
        return IDENT[raw]
    m = re.fullmatch(r"Fl\. (\d+)\.", raw)
    if m:
        return f"{m.group(1)} {abbr}"
    if not re.fullmatch(r"(\*[a-z]\*|[A-Za-zα-ω])[¹²³⁴⁵⁶⁷⁸⁹]*", raw):
        raise SystemExit(f"identification {raw!r}: no rule")
    return f"{raw} {abbr}"


def stars(en, errors):
    sc = S13 / "star_catalogue"
    p3 = read_tsv(sc / "p3_stars.tsv")
    joined = {(r["pdf"], r["row"]): r for r in read_tsv(sc / "star_catalogue_joined.tsv")}
    idents = {f"{r['section']} {r['no']}": r["ident"] or "" for r in read_tsv(sc / "p2_stars.tsv") if r["kind"] == "star"}
    errors += coverage("stars", p3, en, lambda r: f"{r['pdf']}:{r['line']}")
    if errors:
        return ""
    # the Part III section in which each constellation of Part II stands
    seen = {}
    for r in p3:
        if r["kind"] == "star" and r["p2"]:
            seen.setdefault(r["p2"].rsplit(" ", 1)[0], {}).setdefault(r["section"], 0)
            seen[r["p2"].rsplit(" ", 1)[0]][r["section"]] += 1
    home = {k: max(v, key=v.get) for k, v in seen.items()}
    # a star whose numbers belong to the constellation before a heading is shown before that heading
    rows = []
    for r in p3:
        cons = r["p2"].rsplit(" ", 1)[0] if r["p2"] else ""
        if r["kind"] == "star" and cons in home and home[cons] != r["section"]:
            at = max(i for i, x in enumerate(rows) if x["kind"] == "heading")
            if any(x["kind"] == "star" for x in rows[at:]):
                raise SystemExit(f"stars: {r['pdf']}:{r['line']} cannot be moved")
            rows.insert(at, r)
        else:
            rows.append(r)
    spec = "L{44mm}L{12mm}R{7mm}R{5mm}R{6mm}R{5mm}L{3mm}L{15mm}L{34mm}"
    span = r"\multicolumn{8}{>{\raggedright\arraybackslash}p{98mm}}"
    out = [head("The star catalogue", "stars")]
    state = {"open": False, "colhead": None, "page": None, "pending": None}

    def open_table():
        if not state["open"]:
            state["open"] = True
            out.append(r"{\small\setlength{\tabcolsep}{3pt}\begin{longtable}{" + spec + "}")
            out.append(r"\textbf{Description} & \textbf{Star} & \multicolumn{2}{c}{\footnotesize\bfseries Longitude} & "
                       r"\multicolumn{3}{c}{\footnotesize\bfseries Latitude} & {\footnotesize\bfseries Magnitude} & "
                       r"\textbf{Notes}\\")
            out.append(r" & & ° & ′ & ° & ′ & & & \\\hline\endhead")

    def close_table():
        if state["open"]:
            out.append(r"\end{longtable}}")
            state["open"] = False

    def page_mark():
        if state["pending"]:
            out.append(pagerow(9, state["pending"]) + "*")      # «\\*»: no page break after the row
            state["pending"] = None

    for r in rows:
        e = en[f"{r['pdf']}:{r['line']}"]
        if r["ppage"] and r["ppage"] != state["page"]:
            state["page"] = state["pending"] = r["ppage"]
        if r["kind"] in ("above", "title"):
            close_table()
            size = r"\footnotesize" if r["kind"] == "above" else r"\bfseries"
            note = r"\par{\normalfont\footnotesize\itshape " + tex(e[1]) + r"\par}" if e[1] else ""
            out.append(r"\par\needspace{6\baselineskip}\smallskip{\centering" + size + " " + tex(e[0]) + note +
                       r"\par}\nopagebreak" +
                       (r"\ArPage{" + state["pending"] + "}" if state["pending"] else ""))
            state["pending"] = None
            state["titled"] = r["kind"] == "title"
            continue
        open_table()
        if r["kind"] == "colhead":
            # the running head of the Arabic pages, shown where it changes, unless a title has just named the part
            if e[0] != state["colhead"]:
                shown, state["colhead"] = state["colhead"], e[0]
                titled, state["titled"] = state.get("titled"), False
                if shown is not None and titled:
                    continue
                page_mark()
                out.append(r"\multicolumn{9}{>{\raggedright\arraybackslash}p{140mm}}{\bfseries " + tex(e[0]) + r"}\\*")
            continue
        page_mark()
        if r["kind"] in ("heading", "centerline"):
            out.append(span + r"{\emph{" + tex(e[0]) + r"}} & " + tex(e[1]) + r"\\*")
            continue
        j = joined[(r["pdf"], r["line"])]
        cons = j["part2_star"].rsplit(" ", 1)[0]
        notes = []
        nums = [value(j, f, notes, lab) for f, lab in (("lon_d", "longitude °"), ("lon_m", "longitude ′"),
                                                         ("lat_d", "latitude °"), ("lat_m", "latitude ′"))]
        side = value(j, "dir", notes, "side", lambda x: SIDE.get(x, x))
        mag = value(j, "mag", notes, "magnitude", lambda x: " ".join(MAG.get(w, w) for w in x.split()))
        star = ident(idents.get(j["part2_star"], ""), home.get(cons, r["section"]))
        note = "; ".join(([e[1]] if e[1] else []) + notes)
        line = " & ".join([tex(e[0]), tex(star)] + nums + [side, tex(mag), tex(note)]) + r"\\"
        out.append(("{}" if line.startswith("[") else "") + line)       # «\\[» would read the bracket as a skip
    close_table()
    return "\n".join(out)


def folio_en(label):
    """Nallino's folio label, for example «F. 238,v.», in English"""
    m = re.fullmatch(r"F\. (\d+),(r|v)\.", label.strip())
    if not m:
        raise SystemExit(f"folio label {label!r}: no rule")
    return f"Folio {m.group(1)} {'recto' if m.group(2) == 'r' else 'verso'} of the codex"


def status_1211(en, errors):
    sd = S13 / "status_1211"
    p3 = read_tsv(sd / "st_p3.tsv")
    joined = {(r["pdf"], r["row"]): r for r in read_tsv(sd / "status_1211_joined.tsv")}
    above = {r["pdf"]: r["above"] for r in read_tsv(sd / "st_p3_pages.tsv") if r["above"]}
    # Part II's «neb.» and «obsc.», which the joined table leaves blank
    words = {r["no"]: {"neb.": "nebulosa", "obsc.": "obscura"}.get(r["mag"], "")
             for r in read_tsv(sd / "st_p2.tsv") if r["kind"] == "star"}
    errors += coverage("status_1211", p3, en, lambda r: f"{r['pdf']}:{r['line']}")
    if errors:
        return ""
    spec = ("R{5mm}L{40mm}L{12mm}" + "R{6.5mm}R{5.5mm}" + "L{3.5mm}" + "R{6.5mm}R{5.5mm}" * 5 + "L{13mm}L{55mm}")
    heads = ("Their distances from the equator", "Their altitude in the middle of the sky",
             "Half their stay above the earth", "The degrees that culminate with them",
             "The degrees with which they rise", "The degrees with which they set")
    pair = r"\multicolumn{2}{>{\centering\arraybackslash}p{14mm}}"
    fields = (("dec", "distance"), ("alt", "altitude"), ("half", "half stay"), ("cul", "culminating"),
              ("ris", "rising"), ("set", "setting"))
    out = [r"\begin{landscape}", head("The tables of the stars for the year 1211", "status1211")]
    state = {"open": False, "section": None, "page": None, "pending": None}

    def close_table():
        if state["open"]:
            out.append(r"\end{longtable}}")
            state["open"] = False

    def centred(text, size, note=""):
        close_table()
        note = r"\par{\normalfont\footnotesize\itshape " + tex(note) + r"\par}" if note else ""
        out.append(r"\par\needspace{6\baselineskip}\smallskip{\centering" + size + " " + tex(text) + note +
                   r"\par}\nopagebreak" + (r"\ArPage{" + state["pending"] + "}" if state["pending"] else ""))
        state["pending"] = None

    def page_mark():
        if state["pending"]:
            out.append(pagerow(18, state["pending"]) + "*")
            state["pending"] = None

    for r in p3:
        e = en[f"{r['pdf']}:{r['line']}"]
        if r["ppage"] != state["page"]:
            state["page"] = state["pending"] = r["ppage"]
            if r["pdf"] in above:
                centred(folio_en(above[r["pdf"]]), r"\footnotesize")
        if r["kind"] == "title":
            centred(e[0], r"\bfseries", e[2])
            continue
        if r["kind"] == "folio":
            centred(e[0], r"\footnotesize")
            continue
        if r["kind"] == "colhead":
            if r["section"] == state["section"] and state["open"]:
                continue
            close_table()
            state["section"], state["open"] = r["section"], True
            out.append(r"{\footnotesize\setlength{\tabcolsep}{3pt}\begin{longtable}{" + spec + "}")
            out.append(r"\textbf{No.} & \textbf{" + tex(e[0]) + r"} & \textbf{Star} & " + pair + "{\\scriptsize\\bfseries " +
                       heads[0] + r"} & \rotatebox{90}{\scriptsize\bfseries Direction} & " +
                       " & ".join(pair + "{\\scriptsize\\bfseries " + h + "}" for h in heads[1:]) +
                       r" & {\scriptsize\bfseries Ranks of magnitude} & \textbf{Notes}\\")
            out.append(r" & & & ° & ′ & & " + " & ".join(["° & ′"] * 5) + r" & & \\\hline\endhead")
            continue
        page_mark()
        if r["kind"] in ("vnote", "hnote"):
            out.append(r"\multicolumn{17}{>{\raggedright\arraybackslash}p{185mm}}{\emph{" + tex(e[0]) + r"}} & " +
                       tex(e[2]) + r"\\")
            continue
        j = joined[(r["pdf"], r["line"])]
        if not j["p2_mag"] and words.get(j["no"]):
            j = dict(j, p2_mag=words[j["no"]])
        notes = []
        cells = []
        for f, lab in fields:
            cells += [value(j, f"{f}_d", notes, f"{lab} °"), value(j, f"{f}_m", notes, f"{lab} ′")]
            if f == "dec":
                cells.append(value(j, "dir", notes, "direction", lambda x: SIDE.get(x, x)))
        if j["table"] == "M3":                     # the third table has no column of magnitudes
            mag = ""
        else:
            mag = value(j, "mag", notes, "magnitude", lambda x: " ".join(MAG.get(w, w) for w in x.split()))
        note = "; ".join(([e[2]] if e[2] else []) + notes)
        out.append(" & ".join([j["no"], tex(e[0]), tex(e[1])] + cells + [tex(mag), tex(note)]) + r"\\")
    close_table()
    out.append(r"\end{landscape}")
    return "\n".join(out)


ABJAD = {"ا": 1, "ب": 2, "ج": 3, "د": 4, "ه": 5, "و": 6, "ز": 7, "ح": 8, "ط": 9, "ى": 10, "ي": 10, "ك": 20, "ل": 30,
         "م": 40, "ن": 50, "ص": 60, "ع": 70, "ف": 80, "ض": 90, "ق": 100, "ر": 200, "س": 300, "ت": 400, "ث": 500,
         "خ": 600, "ذ": 700, "ظ": 800, "غ": 900, "ش": 1000}
SIGNS = {"حمل": "Aries", "ثور": "Taurus", "جوزاه": "Gemini", "سرطان": "Cancer", "اسد": "Leo", "سنبلة": "Virgo",
         "ميزان": "Libra", "عقرب": "Scorpio", "قوس": "Sagittarius", "جدي": "Capricorn", "دلو": "Aquarius", "حوت": "Pisces"}
PLANETS = {"شمس": "Sun", "قمر": "Moon", "زحل": "Saturn", "مشتري": "Jupiter", "مريخ": "Mars", "بهرام": "Bahrām (Mars)",
           "زهرة": "Venus", "عطارد": "Mercury", "رأس": "the Head", "ذنب": "the Tail",
           "مشترب": "Jupiter"}                                  # printed with one dot under the last letter


def abjad(raw):
    """the value of a cell in Maghribi abjad; {0} is the zero sign"""
    raw = raw.strip()
    return 0 if raw == "{0}" else sum(ABJAD[c] for c in raw)


def figures(en, errors):
    """the two figures of pp. 243 and 244, set out as tables: the lines of the circle of the climes as rows, the
    signs of the astrological figure as columns"""
    dd = S13 / "diagrams"
    cl, cl2 = read_tsv(dd / "climates_p3.tsv"), read_tsv(dd / "climates_p2.tsv")
    names = {r["az"]: r for r in read_tsv(dd / "climates_names_p2.tsv")}
    ro, ro2 = read_tsv(dd / "rosa_p3.tsv"), read_tsv(dd / "rosa_p2.tsv")
    keys = {"title": lambda r: f"243:title:{r['ring']}", "corner": lambda r: f"243:corner:{r['side']}:{r['ring']}",
            "azimuth": lambda r: f"243:azimuth:{r['t']}", "wind": lambda r: f"243:wind:{r['t']}"}
    need = [r for r in cl if r["kind"] in keys]
    errors += coverage("figures", need + [{"k": "244:title"}, {"k": "244:closing"}], en,
                       lambda r: r["k"] if "k" in r else keys[r["kind"]](r))
    if errors:
        return ""
    E = lambda k: en[k][0]                                                    # noqa: E731
    lat = {(r["kind"], r["t"], r["ring"], r["side"]): r["text"] for r in cl2}
    cell = {(r["t"], r["ring"], r["side"]): r["text"] for r in cl if r["kind"] in ("cell", "axis")}

    def latin_num(v):
        return int(re.sub(r"[^0-9]", "", v)) if re.sub(r"[^0-9]", "", v) else None

    out = [r"\begin{landscape}", head("The figure of the seven climes", "climes", "243"),
           r"{\centering\footnotesize " + folio_en("F. 196,v.") + r"\par}\smallskip",
           r"{\centering\bfseries " + tex(E("243:title:1")) + " " + tex(E("243:title:2")) + r"\par}\medskip"]
    # the lines of the circle, grouped by the signs whose beginnings they give: (rising line, setting line)
    groups = (("180", "0"), ("157.5", "22.5"), ("135", "45"), ("112.5", "67.5"), ("202.5", "337.5"),
              ("225", "315"), ("247.5", "292.5"))
    printed = {}
    for r in cl:
        if r["kind"] == "sign":
            line = min((float(t) for g in groups for t in g), key=lambda t: abs(t - float(r["t"])))
            printed.setdefault(f"{line:g}", []).append(SIGNS[r["text"].removeprefix("ال")])
    p2signs = {r["t"]: r["text"].replace(" / ", ", ") for r in cl2 if r["kind"] == "sign"}
    spec = "L{34mm}L{24mm}" + "R{6mm}R{6mm}" * 7 + "L{48mm}"
    out.append(r"{\footnotesize\setlength{\tabcolsep}{3pt}\begin{longtable}{" + spec + "}")
    span = r"\multicolumn{2}{>{\centering\arraybackslash}p{15mm}}"
    south, north = [], []
    for k in range(1, 8):
        a, b = cell[("90", str(k), "cw")], cell[("90", str(k), "ccw")]
        ordinal = {"الاول": "first", "الرابع": "fourth", "السابع": "seventh"}
        south.append(f"The {ordinal[b]} clime" if a == "الاقليم" else f"{abjad(a)}, {abjad(b)}")
        h = cell[("270", str(k), "ccw")].split()
        north.append(f"{abjad(h[0])} h" + (f" {abjad(h[1])} m" if len(h) > 1 else ""))
    out.append(r"\multicolumn{2}{l}{\bfseries " + tex(E("243:azimuth:91.5")) + "} & " +
               " & ".join(span + "{" + s + "}" for s in south) + r" & \\")
    out.append(r"\multicolumn{2}{l}{\bfseries " + tex(E("243:azimuth:271")) + r", its hours} & " +
               " & ".join(span + "{" + s + "}" for s in north) + r" & \\")
    out.append(r"\textbf{Signs} & \textbf{Line} & " + " & ".join(["° & ′"] * 7) + r" & \textbf{Notes}\\\hline\endhead")
    for rise, sett in groups:
        for t, side in ((rise, "rising"), (sett, "setting")):
            where = "" if t in ("0", "180") else (", south" if 0 < float(t) < 180 else ", north")
            signs = ", ".join(printed[t]) if t in printed else "[" + p2signs[t] + "]"
            nums, notes = [], []
            for k in range(1, 8):
                for part, word in (("deg", "degrees"), ("min", "minutes")):
                    if t in ("0", "180"):
                        v, p2 = abjad(cell[(t, str(k), "ccw")]), 0
                    else:
                        v, p2 = abjad(cell[(t, str(k), part)]), latin_num(lat[("cell", t, str(k), part)])
                    if v != p2:
                        notes.append(f"clime {k}, {word}: Part II {p2}")
                        nums.append(f"{v}†")
                    else:
                        nums.append(str(v))
            out.append("{}" + " & ".join([tex(signs), f"{side}{where}"] + nums + [tex("; ".join(notes))]) + r"\\")
    out.append(r"\end{longtable}}")
    # the names in the corners and inside the circle
    out.append(r"\par\needspace{8\baselineskip}\medskip{\footnotesize\setlength{\tabcolsep}{3pt}"
               r"\begin{longtable}{L{62mm}L{30mm}L{60mm}L{35mm}}")
    out.append(r"\textbf{Place in the figure} & \textbf{Name as written} & \textbf{Nallino's reading} & "
               r"\textbf{Name}\\\hline\endhead")
    for side, place in (("TL", "upper left corner"), ("TR", "upper right corner"), ("BL", "lower left corner"),
                        ("BR", "lower right corner")):
        rows = {r["ring"]: r["text"] for r in cl if r["kind"] == "corner" and r["side"] == side}
        greek = "2" if side in ("TL", "TR") else "1"
        label = "1" if greek == "2" else "2"
        out.append(" & ".join([place + ": " + tex(E(f"243:corner:{side}:{label}")), tex(rows[greek]), "",
                               tex(E(f"243:corner:{side}:{greek}"))]) + r"\\")
    for r in sorted((r for r in cl if r["kind"] == "wind"), key=lambda r: (float(r["t"]) - 90) % 360):
        az = (float(r["t"]) - 90) % 360
        n = names[f"{az:g}".replace(".5", " 1/2")]
        place = f"inner circle, {az:g}° from the south ({n['dir']})".replace(".5°", "½°")
        reading = n["restitution"].rstrip(".").replace("ex genit.", "from the genitive")
        out.append(" & ".join([place, tex(r["text"].replace("{stroke}", "…")), tex(reading),
                               tex(E(f"243:wind:{r['t']}"))]) + r"\\")
    out.append(r"\end{longtable}}")
    # the astrological figure
    order = list(SIGNS.values())
    by = {}
    for r in ro:
        by.setdefault((r["kind"], r["sign"]), []).append(r)
    out.append(r"\clearpage" + head("The astrological figure", "astrological", "244"))
    out.append(r"{\centering\footnotesize " + folio_en("F. 197,r.") + r"\par}\smallskip")
    out.append(r"{\centering\bfseries " + tex(E("244:title")) + r"\par}\medskip")
    spec = "L{30mm}" + "L{15.5mm}" * 12
    out.append(r"{\footnotesize\setlength{\tabcolsep}{2.5pt}\begin{longtable}{" + spec + "}")
    out.append(r"& " + " & ".join(r"\textbf{" + s + "}" for s in order) + r"\\\hline\endhead")

    def planet(x):
        return PLANETS[x]
    p2t, p2x = {}, {}
    for r in ro2:
        if r["kind"] == "term":
            p2t.setdefault(r["sign"], []).append((int(r["idx"]), latin_num(r["value"])))
        if r["kind"] == "exalt":
            p2x[r["sign"]] = latin_num(r["value"])
    for i in range(5):
        cells = []
        for s in order:
            t = sorted(by[("term", s)], key=lambda r: int(r["idx"]))[i]
            v = abjad(t["value"])
            cells.append(f"{planet(t['planet'])} {v}" + ("†" if v != sorted(p2t[s])[i][1] else ""))
        out.append(("Terms" if i == 0 else "") + " & " + " & ".join(tex(c) for c in cells) + r"\\")
    out.append(r"\emph{Nallino's degrees} & " + " & ".join(
        r"\emph{" + " ".join(str(v) for _, v in sorted(p2t[s])) + "}" for s in order) + r"\\")
    for i, label in ((1, "Triplicities, outer circle"), (2, "Triplicities, inner circle")):
        cells = [", ".join(planet(p) for p in next(r for r in by[("trip", s)] if r["idx"] == str(i))["text"].split())
                 for s in order]
        out.append(label + " & " + " & ".join(tex(c) for c in cells) + r"\\")
    for i in range(3):
        cells = [planet(sorted(by[("face", s)], key=lambda r: int(r["idx"]))[i]["planet"]) for s in order]
        out.append(("Faces" if i == 0 else "") + " & " + " & ".join(tex(c) for c in cells) + r"\\")
    out.append("Houses & " + " & ".join(tex(planet(by[("house", s)][0]["planet"])) for s in order) + r"\\")
    ex = []
    for s in order:
        x = by[("exalt", s)][0]
        v = abjad(x["value"])
        ex.append((planet(x["planet"]) + " " if x["planet"] else "") + str(v) + ("†" if v != p2x[s] else ""))
    out.append("Exaltations & " + " & ".join(tex(c) for c in ex) + r"\\")
    out.append(r"\end{longtable}}")
    out.append(r"{\centering " + tex(E("244:closing")) + r"\par}\smallskip")
    sums = {s: sum(abjad(t["value"]) for t in by[("term", s)]) for s in order}
    off = [f"{s} {v}" for s, v in sums.items() if v != 30]
    notes = [en["244:closing"][1] + ".",
             r"In the codex the circles of the houses and of the exaltations are drawn as one, and the circle of the "
             r"triplicities is split in two (Nallino); its outer half names the lord by day first, its inner half the "
             r"lord by night.",
             f"In {len(off)} signs the codex's terms do not add up to 30 degrees: " + ", ".join(off) + ". "
             "Nallino's figure gives Ptolemy's terms, after the Frankfurt version of the Tetrabiblos; the row "
             "«Nallino's degrees» lists them, planet by planet.",
             "0 is the codex's zero sign: these signs have no exaltation. Nallino reads 15 for the 14 of Jupiter "
             "in Cancer.",
             "Nallino holds that the figure is not al-Battānī's: al-Battānī never mentions it, and it concerns "
             "judicial astrology only (Part II pp. 308–313)."]
    out.append(r"{\scriptsize " + r"\par ".join(tex(x) for x in notes) + r"\par}")
    out.append(r"\end{landscape}")
    return "\n".join(out)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    errors, parts, built = [], [], []
    for name, fn in (("notice", notice), ("chronology", chronology), ("geography", geography), ("figures", figures),
                     ("stars", stars), ("status_1211", status_1211)):
        en = read_en(name)
        if en is not None:
            parts.append(fn(en, errors))
            built.append(name)
    if errors:
        for e in errors:
            print("ERROR", e)
        raise SystemExit(1)
    target = HERE / "tables_en.tex"
    if not parts:
        target.unlink(missing_ok=True)
        return built
    intro = tex((HERE / "tables" / "intro.txt").read_text(encoding="utf-8").strip())
    top = (r"\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}"
           r"\newcolumntype{R}[1]{>{\raggedleft\arraybackslash}p{#1}}" + "\n" +
           r"\clearpage\pdfbookmark[0]{The tables of Part III}{tables}{\Large\bfseries The tables of Part III\par}"
           r"\medskip" + "\n" + intro + "\n")
    target.write_text(top + "\n\n".join(parts) + "\n", encoding="utf-8", newline="\n")
    print(f"tables_en.tex: {len(parts)} sections")
    return built


if __name__ == "__main__":
    main()

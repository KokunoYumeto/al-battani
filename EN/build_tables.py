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


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    errors, parts, built = [], [], []
    for name, fn in (("notice", notice), ("chronology", chronology), ("geography", geography), ("stars", stars),
                     ("status_1211", status_1211)):
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

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
        out[parts[0]] = parts[1:] + [""] * (2 - len(parts[1:]))
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


def value(row, f, notes, label):
    """the number of field f as the English gives it, marked; its note goes to notes"""
    st = statuses(row).get(f, "")
    v, p2, codex = row.get(f, ""), row.get(f"p2_{f}", ""), row.get(f"codex_{f}", "")
    if st == "codex note":
        notes.append(f"{label}: codex {codex or v}")
        return f"{p2}*"
    if st == "ledgered":
        notes.append(f"{label}: Part II {p2 or '–'}")
        return f"{v}†"
    return v if v != "" else p2


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
             "C": "L{48mm}R{8mm}R{8mm}R{8mm}R{8mm}R{8mm}R{8mm}L{24mm}"}
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
            out.append(r"\par\smallskip{\centering\bfseries " + tex(e[0]) + r"\par}\nopagebreak" +
                       (r"\ArPage{" + pending + "}" if pending else ""))
            pending = None
            continue
        if r["kind"] == "colhead":
            if section == r["section"]:
                continue
            close()
            section = r["section"]
            h = [tex(x) for x in e[0].split("|")]
            out.append(r"{\small\setlength{\tabcolsep}{4pt}\begin{longtable}{" + specs[section] + "}")
            if section == "K":
                out.append(r"\textbf{" + h[0] + r"} & \textbf{Nallino's reading} & \textbf{" + h[1] + r"} & \textbf{" +
                           h[2] + r"} & \textbf{Notes}\\\hline\endhead")
            else:
                out.append(r"\textbf{" + h[0] + r"} & \multicolumn{3}{c}{\textbf{" + h[1] + r"}} & "
                           r"\multicolumn{3}{c}{\textbf{" + h[2] + r"}} & \textbf{Notes}\\")
                out.append(" & " + " & ".join(r"\textbf{" + x + "}" for x in h[3:9]) + r" & \\\hline\endhead")
            continue
        if section is None:
            section = r["section"]
            out.append(r"{\small\setlength{\tabcolsep}{4pt}\begin{longtable}{" + specs[section] + "}")
            out.append(r" & \textbf{Years} & \textbf{Notes}\\\hline\endhead")
        if pending:
            out.append(pagerow(ncols[section], pending))
            pending = None
        if r["kind"] == "heading":
            out.append(r"\multicolumn{" + str(ncols[section]) + r"}{l}{\emph{" + tex(e[0]) + r"}}\\")
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


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    errors, parts = [], []
    for name, fn in (("notice", notice), ("chronology", chronology)):
        en = read_en(name)
        if en is not None:
            parts.append(fn(en, errors))
    if errors:
        for e in errors:
            print("ERROR", e)
        raise SystemExit(1)
    target = HERE / "tables_en.tex"
    if not parts:
        target.unlink(missing_ok=True)
        return
    intro = tex((HERE / "tables" / "intro.txt").read_text(encoding="utf-8").strip())
    top = (r"\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}"
           r"\newcolumntype{R}[1]{>{\raggedleft\arraybackslash}p{#1}}" + "\n" +
           r"\clearpage\pdfbookmark[0]{The tables of Part III}{tables}{\Large\bfseries The tables of Part III\par}"
           r"\medskip" + "\n" + intro + "\n")
    target.write_text(top + "\n\n".join(parts) + "\n", encoding="utf-8", newline="\n")
    print(f"tables_en.tex: {len(parts)} sections")


if __name__ == "__main__":
    main()

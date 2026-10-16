"""S16 - the assembled monolingual editions of AB01, from the sessions' own PDFs (no page is re-typeset):
  AB01_Latin_Nallino_edition.pdf   Nallino's Latin edition: Part I (front matter, translation and notes, commentary)
                                   and Part II (front matter, the tables in his Latin version, notes, glossary, indexes)
  AB01_Arabic_edition.pdf          the Arabic edition: Part III (its title pages and corrigenda, the Arabic title,
                                   the list of chapters, the text of the 57 chapters, Nallino's notice, the tables)
Each opens with a cover and a contents page (XeLaTeX) and has bookmarks to every part and page record. The modern
critical apparatus of S01 (in English) is not bound into either: it is a separate artifact. AB02 (S15) and AB03 (S14)
are monolingual Arabic editions of their own and keep their own licences; they are not bound with AB01.
The build is deterministic (SOURCE_DATE_EPOCH for the covers, fixed metadata): run twice, the files are the same.
python assemble.py [--check]   --check: build into a temporary folder and compare with the files here"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import fitz

AB = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
EPOCH = "1792022400"          # 2026-10-16 00:00 UTC: the date written into the covers' PDF metadata
DATE = "16 October 2026"

LATIN = {
    "file": "AB01_Latin_Nallino_edition.pdf",
    "title": "Nallino’s Latin edition",
    "subtitle": "Part I, Pars prima: front matter, translation of the 57 chapters with notes, commentary; "
                "Part II, Pars secunda: front matter, the tables in Nallino’s Latin version, notes, glossary, "
                "indexes",
    "about": (r"This volume binds, in the order of Nallino\textquoteright s Parts I and II, the line-anchored editions "
              r"of every page of those two volumes: his front matter, his Latin translation of the 57 chapters of "
              r"the \emph{Z\={\i}j} with his footnotes and his commentary (Part I), and the front matter of Part II, "
              r"the tables in his Latin version, his notes on the tables, his glossary and his indexes (Part II). "
              r"A family of tables that Nallino prints in several places is bound once, at the place of its first "
              r"page; the contents give all its pages. "
              r"It is Nallino\textquoteright s historical Latin layer; the Arabic text and tables of Part III are a "
              r"separate volume, and no page of either is set beside the other."),
    "parts": [
        ("I", "Part I — Pars prima", [
            ("Front matter: frontispiece, title, dedication, preface, bibliography, addenda (S01)", "[I]–LXXX",
             "S01/pdf/S01_NALLINO_SOURCE_v003.pdf"),
            ("Translation and notes, pp. 1–53 (S02, v009)", "1–53",
             "S02/candidate_v009_print001-053/pdf/S02_NALLINO_SOURCE_v009.pdf"),
            ("Translation and notes, pp. 54–109 (S02)", "54–109", "S02/versio/p1_versio.pdf"),
            ("The end of the translation and the commentary on chapters 1–28, pp. 110–218 (S03)",
             "110–218", "S03/versio/p1_versio.pdf"),
            ("The commentary on chapters 28–57 and on the appendices, pp. 219–327 (S04)", "219–327",
             "S04/versio/p1_versio.pdf"),
        ]),
        ("II", "Part II — Pars secunda", [
            ("Front matter: half-title, title, preface, conspectus, addenda et emendanda (S05)", "[I]–[XXXII]",
             "S05/versio/p1_versio.pdf"),
            ("Chronological tables (S13)", "1–6", "S13/chronology/p2_chronology.pdf"),
            ("Weekday signs (S06)", "7–8", "S06/signs/p2_signs.pdf"),
            ("Concordance of the Hijra with the era of Dhū ’l-qarnayn (S06)", "9–18",
             "S06/concordance/p2_concordance.pdf"),
            ("Mean motions; motion of the fixed stars (S06)", "19–28, 72–77, 102–107",
             "S06/mean_motions/p2_mean_motions.pdf"),
            ("Mean syzygies (S06)", "29–32, 84–87", "S06/syzygies/p2_syzygies.pdf"),
            ("Geographical tables (S13)", "33–54, 219–220", "S13/geography/p2_geography.pdf"),
            ("Sines, declination, ascensions, shadows, equation of days (S06)", "55–71",
             "S06/spherical/p2_spherical.pdf"),
            ("Equations of the Sun and the Moon (S06)", "78–83", "S06/equations/p2_equations.pdf"),
            ("Eclipses (S06)", "88–91", "S06/eclipses/p2_eclipses.pdf"),
            ("Diagram of the seven climes (S13)", "92", "S13/diagrams/p2_climates.pdf"),
            ("Parallaxes (S06)", "93–101", "S06/parallax/p2_parallax.pdf"),
            ("Equations of the five planets (S06)", "108–137", "S06/planets/p2_planets.pdf"),
            ("Stations (S06)", "138–139", "S06/stations/p2_stations.pdf"),
            ("Latitudes of the planets (S06)", "140–141", "S06/latitudes/p2_latitudes.pdf"),
            ("Apparitions and occultations (S06)", "142–143", "S06/apparitions/p2_apparitions.pdf"),
            ("Star catalogue (S13)", "144–177", "S13/star_catalogue/p2_star_catalogue.pdf"),
            ("Status tables of the bright stars for 1211 (S13)", "178–186", "S13/status_1211/p2_status_1211.pdf"),
            ("Revolutions of the years; the hours (S06)", "187–188", "S06/revolutions/p2_revolutions.pdf"),
            ("Nallino’s notes on the tables (S07)", "189–318", "S07/adnotationes/p2_adnotationes.pdf"),
            ("The spurious tables (S06)", "297, 300–307", "S06/spurious/p2_spurious.pdf"),
            ("The astrological figure (S13)", "299", "S13/diagrams/p2_rosa.pdf"),
            ("Glossary (S09)", "319–358", "S09/glossarium/p2_glossarium.pdf"),
            ("Indexes (S09)", "359–413", "S09/indices/p2_indices.pdf"),
        ]),
    ],
    "twice": (r"Nallino prints the Andalusian geographical table (Part II pp.~219\textendash 220), the spurious tables "
              r"(pp.~297, 300\textendash 307) and the astrological figure (p.~299) among his notes; they are given "
              r"with the notes and again in their checked table editions, whose numbers agree with the notes\textquoteright\ "
              r"transcription (S16, \texttt{duplicates\_compared.tsv})."),
}
ARABIC = {
    "file": "AB01_Arabic_edition.pdf",
    "title": "The Arabic edition",
    "subtitle": "Part III, Pars tertia: the Arabic text of the 57 chapters and the tables of the Escorial codex, "
                "after Nallino",
    "about": (r"This volume binds, in the reading order of the Arabic text, the line-anchored editions of every page "
              r"of Nallino\textquoteright s Part III: its title pages and corrigenda, the Arabic title, the "
              r"codex\textquoteright s list of the 57 chapters, the text of the chapters with Nallino\textquoteright s "
              r"footnotes, his notice before the tables, and the tables and figures of the codex. It is the Arabic "
              r"source layer of the \emph{Z\={\i}j}; Nallino\textquoteright s Latin version is a separate volume, and "
              r"no page of either is set beside the other."),
    "parts": [
        ("III", "Part III — Pars tertia", [
            ("Title pages, corrigenda, Arabic title, list of chapters, text pp. 1–79: chapters 1–30 (S10)",
             "1–79", "S10/textus/p3_textus.pdf"),
            ("Text pp. 80–153: chapters 30–43 (S11)", "80–153", "S11/textus/p3_textus.pdf"),
            ("Text pp. 154–226: chapters 43–57 (S12)", "154–226", "S12/textus/p3_textus.pdf"),
            ("Nallino’s notice before the tables (S13)", "227", "S13/notice/p3_note227.pdf"),
            ("Chronological tables (S13)", "228–234", "S13/chronology/p3_chronology.pdf"),
            ("Geographical tables (S13)", "234–242", "S13/geography/p3_geography.pdf"),
            ("Diagram of the seven climes (S13)", "243", "S13/diagrams/p3_climates.pdf"),
            ("Astrological figure (S13)", "244", "S13/diagrams/p3_rosa.pdf"),
            ("Star catalogue (S13)", "245–274", "S13/star_catalogue/p3_star_catalogue.pdf"),
            ("Status tables of the bright stars for 1211 (S13)", "275–279", "S13/status_1211/p3_status_1211.pdf"),
        ]),
    ],
    "twice": "",
}


def esc(s):
    return s.replace("&", "\\&").replace("%", "\\%").replace("#", "\\#")


def cover_tex(vol, starts, total, commit):
    rows = []
    k = 0
    for part, ptitle, secs in vol["parts"]:
        rows.append("\\multicolumn{3}{@{}l}{\\rule{0pt}{14pt}\\textbf{" + esc(ptitle) + "}}\\\\[2pt]")
        for title, pages, f in secs:
            n = len(fitz.open(AB / f))
            s = starts[k]
            k += 1
            rows.append(f"{esc(pages)} & {esc(title)} & {s if n == 1 else f'{s}' + chr(8211) + f'{s + n - 1}'}\\\\")
    twice = ("\n\n\\textbf{Pages that stand twice.} " + vol["twice"]) if vol["twice"] else ""
    return r"""\documentclass[10pt]{article}
\usepackage[paperwidth=220mm,paperheight=320mm,margin=24mm,top=26mm]{geometry}
\usepackage{fontspec}
\setmainfont{Linux Libertine O}
\usepackage{array}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{6pt}
\begin{document}
\begin{center}
{\fontsize{30}{36}\selectfont al-Batt\={a}n\={\i}\par}
\vspace{6pt}
{\fontsize{17}{22}\selectfont al-Z\={\i}j al-\d{S}\={a}bi\textquoteright\ (Opus astronomicum)\par}
\vspace{10pt}
{\large after the edition of C.\,A. Nallino, \emph{Al-Batt\={a}n\={\i} sive Albatenii opus astronomicum}\\(Milan, 1899\textendash 1907)\par}
\vspace{22pt}
{\fontsize{17}{22}\selectfont @@TITLE@@\par}
\vspace{4pt}
{\normalsize @@SUBTITLE@@\par}
\vspace{6pt}
{\large @@DATE@@ \textperiodcentered\ sources at repository commit @@COMMIT@@\par}
\end{center}
\vspace{16pt}
@@ABOUT@@ It has @@TOTAL@@ pages. The transcriptions are diplomatic and line-anchored: every printed line is one line of the edition, with the anchor AB01-PDF\#\#\#\# of its page in the master scan of Nallino\textquoteright s three volumes (1,162 pages: Part I, printed page + 89; Part II, printed page + 449; Part III, 1,152 $-$ printed page). Readings that depart from what one expects are kept as printed and described in the page records. The contents on the next page give each part\textquoteright s pages in Nallino and in this volume.@@TWICE@@

The transcriptions, markup and checks are AI-integrated work (Claude); no person has reviewed them. Nallino\textquoteright s edition is in the public domain; this edition is released under CC0 1.0. The maintained source, with the page files, records, ledgers, TeX and scripts of every part, is \texttt{github.com/KokunoYumeto/al-battani}; S16 there records the integration and the independent audit.
\newpage
{\Large Contents\par}
\vspace{6pt}
{\small
\begin{tabular}{@{}>{\raggedright\arraybackslash}p{34mm}>{\raggedright\arraybackslash}p{100mm}>{\raggedleft\arraybackslash}p{24mm}@{}}
\textit{Nallino, pp.} & \textit{Part of the edition} & \textit{This volume}\\
@@CONTENTS@@
\end{tabular}}
\end{document}
""".replace("@@SUBTITLE@@", esc(vol["subtitle"])).replace("@@TITLE@@", esc(vol["title"])) \
        .replace("@@DATE@@", DATE).replace("@@COMMIT@@", commit).replace("@@ABOUT@@", vol["about"]) \
        .replace("@@TOTAL@@", f"{total:,}").replace("@@TWICE@@", twice).replace("@@CONTENTS@@", "\n".join(rows))


def build(vol, outdir, commit):
    secs = [s for _, _, ss in vol["parts"] for s in ss]
    counts = [len(fitz.open(AB / f)) for _, _, f in secs]
    starts, p = [], 3
    for n in counts:
        starts.append(p)
        p += n
    total = p - 1
    work = Path(tempfile.mkdtemp(prefix="s16cover_"))
    (work / "cover.tex").write_text(cover_tex(vol, starts, total, commit), encoding="utf-8", newline="\n")
    env = dict(os.environ, SOURCE_DATE_EPOCH=EPOCH, FORCE_SOURCE_DATE="1")
    r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", "cover.tex"], cwd=work, env=env,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    cover = fitz.open(work / "cover.pdf")
    if r.returncode != 0 or len(cover) != 2:
        sys.exit(f"cover failed ({len(cover)} pages):\n" + r.stdout[-2000:])
    out = fitz.open()
    out.insert_pdf(cover)
    toc = [[1, "About this volume", 1], [1, "Contents", 2]]
    k = 0
    for part, ptitle, ss in vol["parts"]:
        toc.append([1, ptitle, starts[k]])
        for title, pages, f in ss:
            src = fitz.open(AB / f)
            out.insert_pdf(src)
            toc.append([2, f"{title} — Nallino pp. {pages}", starts[k]])
            for lvl, t, pg in src.get_toc(simple=True):
                if pg >= 1:
                    toc.append([min(lvl + 2, 6), t, starts[k] + pg - 1])
            k += 1
    fixed, prev = [], 0
    for lvl, t, pg in toc:
        lvl = min(lvl, prev + 1)
        fixed.append([lvl, t, pg])
        prev = lvl
    out.set_toc(fixed)
    out.set_metadata({"title": f"al-Battānī, al-Zīj al-Ṣābi’ — {vol['title']} "
                               f"(after Nallino), {DATE}",
                      "author": "al-Battānī; C. A. Nallino (ed., 1899–1907); source edition: "
                                "github.com/KokunoYumeto/al-battani",
                      "subject": vol["subtitle"], "keywords": "al-Battani, Nallino, zij, source edition, S16",
                      "creator": "S16/assembly/assemble.py (PyMuPDF), XeLaTeX", "producer": "PyMuPDF",
                      "creationDate": "D:20261016000000Z", "modDate": "D:20261016000000Z"})
    dest = outdir / vol["file"]
    out.save(dest, garbage=4, deflate=True, no_new_id=True)
    shutil.rmtree(work, ignore_errors=True)
    return dest, total, len(fixed), list(zip([s[0] for s in secs], starts, counts))


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    # the commit of the last change to any bound file: the covers name the state of their sources, and a later
    # commit that does not touch them leaves the build unchanged
    files = [f for vol in (LATIN, ARABIC) for _, _, ss in vol["parts"] for _, _, f in ss]
    commit = subprocess.run(["git", "-C", str(AB), "log", "-1", "--format=%h", "--"] + files, capture_output=True,
                            text=True).stdout.strip()
    check = "--check" in sys.argv
    outdir = Path(tempfile.mkdtemp(prefix="s16asm_")) if check else HERE
    rows = []
    for vol in (LATIN, ARABIC):
        dest, total, nb, secs = build(vol, outdir, commit)
        h = sha256(dest)
        rows.append((vol["file"], total, nb, h, secs))
        print(f"{vol['file']}: {total} pages, {nb} bookmarks, {dest.stat().st_size / 1e6:.2f} MB, sha256 {h}")
        if check:
            mine = HERE / vol["file"]
            print("   same as the file here:", mine.exists() and sha256(mine) == h)
    if not check:
        with open(HERE / "assembly_receipt.tsv", "w", encoding="utf-8", newline="\n") as fh:
            fh.write("volume\tsection\tfirst_page\tpages\n")
            for f, total, nb, h, secs in rows:
                for title, start, n in secs:
                    fh.write(f"{f}\t{title}\t{start}\t{n}\n")
        with open(HERE / "volumes.tsv", "w", encoding="utf-8", newline="\n") as fh:
            fh.write("volume\tpages\tbookmarks\tsha256\tcommit_on_cover\n")
            for f, total, nb, h, secs in rows:
                fh.write(f"{f}\t{total}\t{nb}\t{h}\t{commit}\n")


if __name__ == "__main__":
    main()

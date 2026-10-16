# S16 cold audit — visual inspection and reviewed reports

The rendered evidence of the cold audit was looked at by the same AI (Claude) that produced the edition and wrote the
audit program, in the same session. This is a record of what was looked at and what was found; it is not an
independent or a human review.

## Contact sheets: master scan beside the edition (S16/audit/samples)

| Master page | Why | Looked at | Finding |
|---|---|---|---|
| PDF 210 (Part I p. 121) | the page with the most formula lines (23) | whole page at 45 dpi; lines 1–17 of the master at 110 dpi beside the edition at 130 dpi | the same lines, notes and margin locators; every number and fraction of lines 1–17 agrees: 1/15 (1), 7ᵖ 2/3, 5 1/2, 1108 (3), 201 1/2 (4), 7 2/3, 1 ad 26 1/4 (5), [scilicet 2ᵖ], 1° 57′ (6), 0° 4′ 1/2 + 1/6 [= 0° 4′ 2/3], 1/18087 (7), 2/13 (8), 166 (9), 6 1/2, 1070 (10), 618, 1/10, 61 4/5, 201 1/2, 1/4 + 1/10×2 [= 3/10], (11), 0° 32′ 27″; the locator «p. 183.» |
| PDF 365, 292, 279 | dense formula pages (19 lines each) | whole page at 45 dpi | the same lines, notes and figures in the same places |
| PDF 566 (Part II p. 117) | dense table: the equation of Jupiter | the heads at 110 dpi; rows 95–100 at 100 dpi | the folio line, the Arabic and Latin titles and the column heads agree; rows 95–100 agree in every cell (95 265 5 15 6 0 28 11 1 0 31 … 100 260 5 13 11 0 29 11 3 0 32) |
| PDF 620 (Part II p. 171), 895 (Part III p. 257) | dense tables: the star catalogue | whole page at 45 dpi | the same rows, sections, numerals and footnotes |
| PDF 1146 (Part III p. 6) | the beginning of the Arabic text | the head of the page at 100 dpi | «الباب الاوّل», «في صدر الكتاب» and the first line with its vowel signs and the line number 5 agree |
| PDF 1071 (Part III p. 81) | an Arabic page with a figure | whole page at 45 dpi | the same lines, figure (circles, lines and letters in their places) and footnotes |
| PDF 909 (Part III p. 243), 748 (Part II p. 299) | the circular figures | whole page at 45 dpi | redrawn with the same rings, lines and texts in their places and orientations |
| PDF 2 | the frontispiece | whole page | the raster panel of the scan, as S01 keeps it |
| PDF 90, 416, 418, 450, 862, 926, 873, 1153 | first and last pages of the parts | whole page at 45 dpi | the same lines and page structure; first and last lines agree |

## The seams of the assembled volumes (S16/assembly/inspection)

All six sheets were looked at: the covers, the contents pages, every boundary between two bound parts and the last
pages of both volumes. The order of the parts, their first and last pages and the page numbers of the contents
agree. During this inspection, before the audit ran, a fault of the assembler was found and corrected in production:
the covers printed «SUB» before their subtitle (a placeholder was replaced inside another). The covers were rebuilt and
looked at again. Before the final audit run the last sentence of the covers was corrected: it called the audit
independent; it now says that the cold audit is read-only and run by the same AI. The covers and contents
(inspection/cover_*.png, contents_*.png) were rendered again and read.

## The pages transcribed twice, compared word by word

Before the final audit run, S16's comparison of the twelve master pages that two sessions transcribed
(S16/integration/compare_duplicates.py) was extended from the numbers to every word of the astrological figure on
Part II p. 299 (master PDF 748). It found three labels of the terms that the two transcriptions read differently. Each
was read on the scan, the label beside the other labels of its planet (S16/integration/evidence), and corrected in the
session that had it wrong (S16/integration/repairs.tsv): Gemini term 2 is printed «Inpiter» and Cancer term 2
«Iupitor» (S13 had «Iupiter» for both); Virgo term 2 is printed «Verus» (S07's redrawn figure had «Venus»). The
labels were then looked at in both editions: S13/diagrams/p2_rosa.pdf and S07/adnotationes/p2_adnotationes.pdf
p. 112 show «Inpiter», «Iupitor», «Verus» and «Venns» at their places. After the correction all twelve pages agree:
every item of the canonical transcription stands in S07's, and S07's further items are footnote marks and the note
that begins on p. 220.

## Reports of the sessions' own checks, reviewed

The observation checkers of S07 and S09 (glossary) report 5 and 6 observations whose quoted words stand on a line
other than the one the observation names. Each was read:

| Page | Report | Reading |
|---|---|---|
| S07 PDF 705 | L28 quotes «5° 2/3» (L27) | context: the observation contrasts the 8 of L28 with the 3 of «5° 2/3» before it |
| S07 PDF 721 | notes_left L22 quotes «tiones» | context: the word continues «tiones» at the head of the right column |
| S07 PDF 734 | notes_left L12, L15 quote «to» | context: «tho» is printed for «to» |
| S07 PDF 736 | body L34 quotes «ea» | context: «ca» is printed for «ea» |
| S07 PDF 741 | body L41 quotes «18′.29» (L42) | context: the rule at the height of L41 runs to the end of «18′.29» |
| S09 PDF 796 | L5 quotes «gittarii» (L6) | context: the kasra over «gittarii» of L6 |
| S09 PDF 796 | L7, L9 quote «ἀπηλιώτης» (L10), «ὀψινὸς» (L20) | context: the observation names L10 and L20 itself |
| S09 PDF 796 | L16 quotes «II» (L17) | context: the kasra above «II» of L17 |
| S09 PDF 796 | notes_right L5 quotes «العَوَّاء» (body L31) | context: the observation names body L31 itself |
| S09 PDF 798 | body L7, L21 quote «ἀκρόνυκτος» (notes_right L1) | context: the observation names notes_right L1 itself |

None is a wrong line number; nothing is open.

## S01's own technical audit

S01's read-only technical audit (S01/scripts/audit_v003_readonly.py) was replayed on the complete S01 v003 package
(_intake/AB01_S01_v003.zip, 1,015 files; the repository holds 563 of them, all byte-identical to the package's):
47 checks, 0 failures (s01_technical_audit_replay.json). That audit is technical; S01's own status records that its
independent philological reading audit has not been performed.

## What the audit does not do

It does not re-read the transcriptions line by line against the scans: the reading of every page is the work of the
sessions, recorded in their page files and observations. The contact sheets compare page structure, and for three
pages the readings of formula, table and text lines.

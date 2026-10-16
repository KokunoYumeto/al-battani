"""The routing of Nallino's Addenda et emendanda of Part II (pp. XVI-XXXI) to the places of the edition that they
concern: one row per correction or addition, with the lines of S05 that print it, the anchors of the place concerned
(a line of a Latin or Arabic page record, or a row of a table), where it is recorded there, and what was checked.
No correction is applied to the transcribed text: every place keeps its printed form (REGISTERED_NOT_APPLIED), as in
S01/ledgers/printed_corrigenda_routing.tsv. Writes corrigenda_routing.tsv and corrigenda_routing.json.
python write_routing.py"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
P1 = "Part I"
OBS = "observation in the page record: "


def a(spec):
    """'447:L029-L031' -> the S05 body anchors of those lines"""
    pdf, rng = spec.split(":")
    m = re.match(r"L(\d+)(?:-L(\d+))?$", rng)
    lo, hi = int(m.group(1)), int(m.group(2) or m.group(1))
    return [f"AB01-PDF{int(pdf):04d}-body-L{k:03d}" for k in range(lo, hi + 1)]


HEAD = re.compile(r"^(Pag\. )?(\{sc:[ivxlc]+\}|\{b:\d+[^}]*\}|\{ar:[٠-٩]+\})")


def entries():
    """the entries of the addenda, PDF 433-448, in order: the anchors of their body lines, from the page files (an
    entry begins at a line headed by a page of the volume concerned) and the records (the anchors of the lines)"""
    out, vol = [], None
    for pdf in range(433, 449):
        rec = json.loads((HERE / "records" / f"AB01-PDF{pdf:04d}.json").read_text(encoding="utf-8"))
        ids = [ln["id"] for sec in rec["sections"] for ln in sec["lines"]]
        raw, part = [], "body"
        for ln in (HERE / "pages" / f"AB01-PDF{pdf:04d}.txt").read_text(encoding="utf-8").splitlines():
            if ln.startswith("@notes"):
                part = "notes"
            elif ln.startswith("%") or not ln.strip() or (ln.startswith("@") and not ln.startswith(("@pos", "@lc", "@center", "@wrapr"))):
                continue
            else:
                raw.append((part, ln))
        assert len(raw) == len(ids), (pdf, len(raw), len(ids))
        for aid, (part, ln) in zip(ids, raw):
            if part != "body" or ln.startswith("@wrapr"):
                continue
            if ln.startswith("@lc"):
                vol = "I" if "PRIMUM" in ln else "II" if "SECUNDUM" in ln else "III"
                continue
            t = re.sub(r"^>?\^? ?", "", ln) if ln.startswith((">", "^")) else ln
            if vol and not ln.startswith(">") and HEAD.match(t):
                out.append([aid])
            elif out:
                out[-1].append(aid)
    return out


def resolve(src, ents, text):
    """an entry (its index), a part of one ((index, first words, words of the line after the part)), or anchors"""
    if isinstance(src, int):
        return ents[src]
    if isinstance(src, tuple):
        k, start, stop = src
        ids = ents[k]
        i = 0 if start is None else next(j for j, x in enumerate(ids) if text[x].startswith(start))
        e = len(ids) if stop is None else next(j for j, x in enumerate(ids) if text[x].startswith(stop))
        return ids[i:e]
    return [x for spec in src.split("; ") for x in a(spec)]


# (printed target, layer, target anchors, recorded in, check, S05 lines, segment of the S05 text or None)
ROWS = [
    # ---- to the first volume (Part I): its preface, in S01 v003
    ("t. I, p. xi, lin. 17", "Part I preface (S01 v003)", "AB01-PDF0020-body-L017", "this ledger",
     "the line reads «muliere malis moribus praedita»; the addenda prefer «muliere natura aspera» (Glossarium to aṭ-Ṭabarī, p. CCXXXI)",
     0, None),
    ("t. I, p. xvii, n. 1, lin. 3 a f.", "Part I preface (S01 v003)", "AB01-PDF0026-notes_left-L019", "this ledger",
     "the third line from the foot of the left column of notes, in note 1, reads «R. Astronomical Society, t. XIV, London 1843»: XIII for XIV",
     1, None),
    ("t. I, p. xvii, n. 3", "Part I preface (S01 v003)", "AB01-PDF0026-notes_right-L020", "this ledger",
     "the note reads «hodie ad Yale University in Princeton»: New Haven for Princeton", 2, None),
    ("t. I, pp. xxv et xlix", "Part I preface (S01 v003)", "AB01-PDF0034-body-L006; AB01-PDF0058-body-L031; AB01-PDF0058-notes_left-L003",
     "this ledger", "the author of the preface of the Latin Planisphaerium is its translator, Hermann of Dalmatia (Secundus), and the year of the version 1143 (Björnbo, Bibl. Math. 3. F., 4, 1903, pp. 130-133)",
     3, None),
    ("t. I, p. xxvi", "Part I preface (S01 v003)", "AB01-PDF0035-body-L007-L019", "this ledger",
     "additions on the book of Shādhān ibn Baḥr: Latin copies at Munich (Clm. 826) and Brussels (1464) after Boll; the London book that names Abū Ma‘shar's colloquy with Shādhān ibn Baḥr (Rieu, p. 624 a, nr. 1348); Ibn Khaldūn, Beirut 1879, p. 293",
     4, None),
    ("t. I, p. xxx, lin. 8-10", "Part I preface (S01 v003)", "AB01-PDF0040-body-L008-L010", "this ledger; S05 observation on AB01-PDF0433-body-L018",
     "misprint in the addenda: the passage on Bethem, Bethen, Bereni and Apollonius of Tyana is p. XXXI, lines 8-10; Suter's identification with Apollonius, which Nallino still doubts",
     5, None),
    ("t. I, p. xxxi, lin. 1", "Part I preface (S01 v003)", "AB01-PDF0040-body-L001", "this ledger",
     "the line reads «[ad-darīǵan]»: ad-darīǵān", 6, None),
    ("t. I, p. xxxiii, lin. 13-14", "Part I preface (S01 v003)", "AB01-PDF0042-body-L013-L014", "this ledger",
     "the unknown author of tasṭīḥ aṣ-ṣuwar is al-Bīrūnī, who lists it among his books (Suter)", 7, None),
    ("t. I, p. xxxvi, n. 1", "Part I preface (S01 v003)", "AB01-PDF0045-notes_left-L002-L003", "this ledger",
     "the libellus de motu octave spere (Bologna 1480) is an excerpt of the last chapter of Purbach's Theoricae novae planetarum",
     8, None),
    ("t. I, p. xlviii, lin. 3-4", "Part I preface (S01 v003)", "AB01-PDF0057-body-L003-L004", "this ledger",
     "delete 194 and «et formulam α ...» (Suter): the lines read «p. 181, 194, 258, 259, et formulam α pag. 183»",
     9, None),
    ("t. I, p. lx, lin. 18-21", "Part I preface (S01 v003)", "AB01-PDF0069-body-L018-L021", "this ledger",
     "on the origin of the Spanish version see Part II, p. VII", 10, None),
    ("t. I, p. lxvi, lin. 26-27", "Part I preface (S01 v003)", "AB01-PDF0075-body-L026-L027", "this ledger",
     "the lines are to be read «editus, titulo Arabico omisso ... 16 pro reliquis»", 11, None),
    ("t. I, p. lxxii et pp. 163-164", "Part I addenda (S01 v003); Part I commentary (S03)",
     "AB01-PDF0081-body-L032-L035; AB01-PDF0253-body-L013-L014", OBS + "S03/versio/records/AB01-PDF0253.json",
     "Theon's tables also count the right ascensions from the beginning of Capricorn", 12, None),
    ("t. I, p. lxxv et p. 266", "Part I addenda (S01 v003); Part I commentary (S04)",
     "AB01-PDF0084-body-L007; AB01-PDF0355-notes_right-L001-L012", OBS + "S04/versio/records/AB01-PDF0355.json",
     "further examples of the uncertainty about the new moon (Ibn Ǵubayr; Abū Nuwās on the day of doubt)", 13, None),
    ("t. I, p. lxxv et p. 272 (mir’āh)", "Part I addenda (S01 v003); Part I commentary (S04)",
     "AB01-PDF0084-body-L024-L025; AB01-PDF0361-body-L009-L017", OBS + "S04/versio/records/AB01-PDF0361.json",
     "the mir’āh of Abū ’l-‘Alā’ is the astrolabe (Luzūm; his second letter; Ḥāǵǵī Khalīfah; Kushāǵim)", (14, None, 'Monet'), None),
    ("t. I, p. 272 (Walafrid)", "Part I commentary (S04)", "AB01-PDF0361-body-L027", OBS + "S04/versio/records/AB01-PDF0361.json",
     "Suter: the diary of Walafrid Strabo is a forgery of P. Marty; the monk with the tube in codex 18 of St. Gall", (14, 'Monet', None), None),
    ("t. I, p. lxxvii, n. 1", "Part I addenda (S01 v003)", "AB01-PDF0086-notes_left-L001-L008; AB01-PDF0086-notes_right-L001-L004",
     "this ledger", "the booklet of Sahl ibn Bishr is in the British Museum, anonymous and wrongly entitled nawādir al-qaḍā’",
     15, None),
    ("t. I, p. lxxviii et p. 297", "Part I addenda (S01 v003); Part I commentary (S04)",
     "AB01-PDF0087-body-L021-L031; AB01-PDF0386-body-L026-L033", OBS + "S04/versio/records/AB01-PDF0386.json",
     "examples of mumāzaǵah and mizāǵ in Arabic astrology, σύγκρασις and μῖξις in Greek, mixtura, mūzāgā", 16, None),
    ("t. I, p. lxxviii et p. 301", "Part I addenda (S01 v003); Part I commentary (S04)",
     "AB01-PDF0087-body-L036; AB01-PDF0390-body-L016-L018", OBS + "S04/versio/records/AB01-PDF0390.json",
     "the Introductorium Ptolemaei ad artem sphaericam is the Arabic Geminus; وحَكَى for وحُكي in al-Bīrūnī", 17, None),
    ("t. I, p. lxxix et p. 309, n. 2", "Part I addenda (S01 v003); Part I commentary (S04)",
     "AB01-PDF0088-body-L018-L019; AB01-PDF0398-notes_left-L009-L015", OBS + "S04/versio/records/AB01-PDF0398.json",
     "the book of Hermes in Dr. Griffini's codex; dates checked: dhū ’l-qa‘dah 125 H. = 26 August-23 September 743; 17 rabī‘ I 1071 H. = Saturday 20 November 1660 by the civil reckoning",
     18, None),
    # ---- to the first volume: the text and commentary
    ("t. I, p. 3, lin. 7-8 (et n. 1)", "Part I translation (S02 v009 candidate)",
     "AB01-PDF0092-body-L007-L008; AB01-PDF0092-notes_left-L001", "this ledger (the v009 candidate is frozen)",
     "the title of chapter 28 in the list of chapters", 19, None),
    ("t. I, p. 27, lin. 14-15", "Part I translation (S02 v009 candidate)", "AB01-PDF0116-body-L010-L011",
     "this ledger (the v009 candidate is frozen)",
     "lines 14-15 by the margin numbers (the page begins with the head of chapter 13); the printed «maxima ... minima» for «amplius quam ... tantodem minus»",
     20, None),
    ("t. I, p. 43, titulo et lin. 9-10", "Part I translation (S02 v009 candidate)",
     "AB01-PDF0132-body-L001-L003; AB01-PDF0132-body-L005-L006", "this ledger (the v009 candidate is frozen)",
     "the title of chapter 28 and lines 9-10 by the margin numbers; see Part II, p. 358, s. v. وضع", 21, None),
    ("t. I, p. 64, lin. 4", "Part I translation (S02)", "AB01-PDF0153-body-L004", OBS + "S02/versio/records/AB01-PDF0153.json",
     "«est ipsa quantitas [sinus] mediae aequationis planetae»", 22, None),
    ("t. I, p. 67, lin. 13", "Part I translation (S02)", "AB01-PDF0156-body-L013", OBS + "S02/versio/records/AB01-PDF0156.json",
     "printed «isfandarmadh–māh»", 23, None),
    ("t. I, pp. 92-93", "Part I translation (S02)", "AB01-PDF0181-notes_right-L004-L006; AB01-PDF0182-body",
     OBS + "S02/versio/records/AB01-PDF0181.json, AB01-PDF0182.json", "note 4 of p. 92 takes the era for that of Augustus",
     24, None),
    ("t. I, p. 115, lin. 18", "Part I translation (S03)", "AB01-PDF0204-body-L014", OBS + "S03/versio/records/AB01-PDF0204.json",
     "line 18 by the margin numbers is L14, which prints 360° for 270°", 25, None),
    ("t. I, p. 125, n. 1", "Part I translation (S03)", "AB01-PDF0214-notes_left-L003", OBS + "S03/versio/records/AB01-PDF0214.json",
     "printed «ἡ πλόκαμος»", 26, None),
    ("t. I, p. 125, n. 7 et seqq.", "Part I translation (S03)",
     "AB01-PDF0214-notes_left-L012-L023; AB01-PDF0214-notes_right-L020-L026", OBS + "S03/versio/records/AB01-PDF0214.json",
     "the stars of five lunar mansions after aṣ-Ṣūfī and al-Bīrūnī", 27, None),
    ("t. I, p. 143, lin. 4, 5", "Part I translation (S03)", "AB01-PDF0232-body-L004-L005", OBS + "S03/versio/records/AB01-PDF0232.json",
     "B for the C of «alterum in C» and «extremum stilum C»", 28, None),
    ("t. I, p. 149, titulus adp. F", "Part I translation (S03)", "AB01-PDF0238-body-L004", OBS + "S03/versio/records/AB01-PDF0238.json",
     "directione for «profectione», as Part I, p. 325 says", 29, None),
    ("t. I, p. 153, n. 1", "Part I commentary (S03)", "AB01-PDF0242-notes_right-L001-L002", OBS + "S03/versio/records/AB01-PDF0242.json",
     "+ for − in the numerator: crd (p + q) = [crd p crd (180° − q) + crd q crd (180° − p)] : 2R, checked", 30, None),
    ("t. I, p. 157, lin. 24", "Part I commentary (S03)", "AB01-PDF0246-body-L024", OBS + "S03/versio/records/AB01-PDF0246.json",
     "printed «‘Alī ibn Mūsà»", 31, None),
    ("t. I, p. 160, n. 3", "Part I commentary (S03)", "AB01-PDF0249-notes_left-L012-L013", OBS + "S03/versio/records/AB01-PDF0249.json",
     "printed «(cfr. p. 6, adn. 3)»", 32, None),
    ("t. I, p. 161, n. 3", "Part I commentary (S03)", "AB01-PDF0250-notes_right-L008-L011", OBS + "S03/versio/records/AB01-PDF0250.json",
     "the story of Euclid and the obliquity traced to Heron, Proclus, Eudemus and Theon of Smyrna", 33, None),
    ("t. I, pp. 167-175", "Part I commentary (S03)",
     "AB01-PDF0256-body-L032; AB01-PDF0258-body-L033; AB01-PDF0259-notes_left-L005-L011; AB01-PDF0260-notes_right-L010-L013",
     OBS + "S03/versio/records/AB01-PDF0256.json, 0258, 0259, 0260", "an-Naysābūrī's and Fakhr ad-dīn ar-Rāzī's descriptions of the seas",
     34, None),
    ("t. I, pp. 175-177", "Part I commentary (S03)",
     "AB01-PDF0265-body-L005-L007; AB01-PDF0265-body-L010; AB01-PDF0265-body-L028; AB01-PDF0266-body-L012-L025",
     OBS + "S03/versio/records/AB01-PDF0265.json, 0266", "de Goeje's letter on the Green Sea", 35, None),
    ("t. I, p. 189, lin. 3", "Part I commentary (S03)", "AB01-PDF0278-body-L003", OBS + "S03/versio/records/AB01-PDF0278.json",
     "sin m = tg φ tg δ : R for the printed R tg φ tg δ, checked", 36, "189,3: Formula Ḥabash est sin m = tg φ tg δ : R."),
    ("t. I, p. 163, lin. 24", "Part I commentary (S03)", "AB01-PDF0252-body-L024", OBS + "S03/versio/records/AB01-PDF0252.json",
     "sin α = tg δ cotg ε : R for the printed R tg δ cotg ε, checked", 36, "Item 163,24: sin α = tg δ cotg ε : R."),
    ("t. I, p. 217, lin. 21", "Part I commentary (S03)", "AB01-PDF0306-body-L021", OBS + "S03/versio/records/AB01-PDF0306.json",
     "3600″ : 299 = 12″ 12/299, checked; printed 11″ 12/299", 37, "217,21: pro 11″ 12/299 l. 12″ 12/299."),
    ("t. I, p. 217, n. 5", "Part I commentary (S03)", "AB01-PDF0306-notes_right-L017-L018", OBS + "S03/versio/records/AB01-PDF0306.json",
     "printed «fuit X Chr. saeculo»", 37, "Ibid., n. 5: pro X l. XI."),
    ("t. I, p. 222, lin. 30-37", "Part I commentary (S04)", "AB01-PDF0311-body-L030-L037", OBS + "S04/versio/records/AB01-PDF0311.json",
     "the fifth method of the equation of time (al-Fārisī after Steinschneider); dates and numbers checked in the records of pp. XXIV-XXV",
     38, None),
    ("t. I, pp. 284-285", "Part I commentary (S04)", "AB01-PDF0373-body-L023", OBS + "S04/versio/records/AB01-PDF0373.json",
     "Ptolemy, Tetrabiblos II, 7", 39, None),
    ("t. I, p. 287", "Part I commentary (S04)", "AB01-PDF0376-body-L019-L022", OBS + "S04/versio/records/AB01-PDF0376.json",
     "the twelfth, not the second, book of Euclid: عشرة fallen out after المقالة الثانية", 40, None),
    ("t. I, pp. 288 et 289", "Part I commentary (S04)", "AB01-PDF0377-body-L018; AB01-PDF0378-body-L029-L033",
     OBS + "S04/versio/records/AB01-PDF0377.json, 0378", "the Kitāb al-manshūrāt in Barhebraeus; Abū Ma‘shar's distance of the Moon; computations checked in the records of pp. XXV-XXVII",
     41, None),
    ("t. I, p. 305, n. 1", "Part I commentary (S04)", "AB01-PDF0394-notes_left-L001-L002", OBS + "S04/versio/records/AB01-PDF0394.json",
     "printed «Adnotator Schaton»", 42, None),
    ("t. I, p. 318 (demonstratio)", "Part I commentary (S04)", "AB01-PDF0407-body-L004-L009; AB01-PDF0407-body-L016-L017",
     OBS + "S04/versio/records/AB01-PDF0407.json", "cos azimuth = sin (λ − λ′) cos φ : sin distantiae, with φ for the printed φ′; checked",
     (43, None, 'Error ex'), None),
    ("t. I, p. 318 (error)", "Part I commentary (S04)", "AB01-PDF0407-body-L033", OBS + "S04/versio/records/AB01-PDF0407.json",
     "1°-2° for the printed «3° vel 4°»; recomputed with al-Battānī's coordinates: 0.1°-1.3°", (43, 'Error ex', None), None),
    # ---- to the second volume (Part II): the tables
    ("t. II, p. 5, ult. lin.", "Part II tables (S13 chronology)", "S13/chronology/chr_p2.tsv: p. 5, C50 (al-Mu‘tamid), reign 28 years",
     "S13/chronology/chr_p2.tsv, doubt column (Part II p. 198)", "255 y 6 m 17 d + 23 y 0 m 3 d = 278 y 6 m 20 d, the printed sum", 44, None),
    ("t. II, p. 22, col. Solis, nr. 10", "Part II tables (S06 mean motions)", "S06/mean_motions/mm_p2.tsv: p. 22, days 10, Sun 9° 51′ 25″",
     "S06/mean_motions/mm_discrepancies.tsv (Nallino, Part II p. 204)", "computed 24″ (the line through the table 23.4″)", 45, None),
    ("t. II, p. 22, col. nodi, nr. 21", "Part II tables (S06 mean motions)", "S06/mean_motions/mm_p2.tsv: p. 22, days 21, node 1° 6′ 45″",
     "S06/mean_motions/mm_discrepancies.tsv (Nallino, Part II p. 204)", "computed 44″ (44.0″)", 46, None),
    ("t. II, p. 23, col. Solis, nr. 3", "Part II tables (S06 mean motions)", "S06/mean_motions/mm_p2.tsv: p. 23, hours 3, Sun 0° 7′ 25″",
     "S06/mean_motions/mm_discrepancies.tsv (Nallino, Part II p. 204)", "computed 24″ (23.7″); p. 76 has 24″", 47, None),
    ("t. II, p. 23, col. anom., paenult. lin.", "Part II tables (S06 mean motions)", "S06/mean_motions/mm_p2.tsv: p. 23, hours 23, anomaly 12° 31′ 13″",
     "S06/mean_motions/mm_discrepancies.tsv (Nallino, Part II p. 204)", "computed 14″ (14.2″); p. 76 has 14″", 48, None),
    ("t. II, p. 31, lin. 10", "Part II tables (S06 syzygies)", "S06/syzygies/syz_p2.tsv: p. 31, parts, «Monsis dimidium»",
     "S06/syzygies/README.md (Nallino's note)", "printed «Monsis»", 49, None),
    ("t. II, p. 32, col. dierum, ad nr. 4", "Part II tables (S06 syzygies)", "S06/syzygies/syz_p2.tsv: p. 32, single year 6, days 24ᵈ 47′ 50″",
     "S06/syzygies/syz_discrepancies.tsv (Nallino, Part II p. 207); S05 observation on AB01-PDF0444-body-L036",
     "misprint in the addenda: the 50″ stands under year 6 (year 4 has 47″); 75 lunations − 6 × 365 days = 24;47,40.4", 50,
     "32, col. dierum, ad nr. 4 pro 50″ l. 40″"),
    ("t. II, p. 32, col. dierum, ad nr. 11", "Part II tables (S06 syzygies)", "S06/syzygies/syz_p2.tsv: p. 32, single year 11, days 1ᵈ 9′ 29″",
     "S06/syzygies/syz_discrepancies.tsv (Nallino, Part II p. 207)", "136 lunations − 11 × 365 days = 1;9,38.9", 50,
     "ad nr. 11 pro 29″ l. 39″"),
    ("t. II, p. 32, col. dierum, ad nr. 19", "Part II tables (S06 syzygies)", "S06/syzygies/syz_p2.tsv: p. 32, single year 19, days 4ᵈ 41′ 13″",
     "S06/syzygies/syz_discrepancies.tsv (Nallino, Part II p. 207)", "235 lunations − 19 × 365 days = 4;41,22.6; the addenda leave out year 14 (34″ for 24″), which the notes give",
     50, "ad nr. 19 pro 13″ l. 23″"),
    ("t. II, p. 32, lin. 3 a fine", "Part II tables (S06 syzygies)", "S06/syzygies/syz_extra.tsv: p. 32, the solar limits 191° 16′ and 348° 44′",
     "S06/syzygies/syz_discrepancies.tsv (Nallino, Part II p. 209)", "the addenda print ″ for ′ in three of the four numbers (S05 record of p. XXVIII)",
     51, None),
    ("t. II, p. 35, nr. 72, latit.", "Part II tables (S13 geography)", "S13/geography/geo_p2.tsv: p. 35, nr. 72 (Iṣfahān), latitude 37° 0′",
     "this ledger", "36° for the codex's 37° (cfr. Part II, p. 215)", 52, None),
    ("t. II, p. 35, n. ad nr. 77", "Part II tables (S13 geography)", "S13/geography/geo_p2_notes.tsv: nr. 77 (Marw ar-rūdh)",
     "this ledger", "addition: the site of Marw ar-rūdh", 53, None),
    ("t. II, p. 35, n. ad nr. 80", "Part II tables (S13 geography)", "S13/geography/geo_p2_notes.tsv: nr. 80 (Binkat)",
     "this ledger", "addition: Binkat (Tashkent) and the Stone Tower", 54, None),
    ("t. II, pp. 38-53", "Part II tables (S13 geography)", "S13/geography/geo_p2.tsv: pp. 38-53",
     "this ledger", "small emendations from the Spanish version, given in Part II, pp. 216-217", 55, None),
    ("t. II, p. 39, lin. 3 notae 114", "Part II tables (S13 geography)", "S13/geography/geo_p2_notes.tsv: nr. 114",
     "this ledger", "the note reads «Sud suspicor»: Sed", 56, None),
    ("t. II, p. 40, n. ad nr. 137", "Part II tables (S13 geography)", "S13/geography/geo_p2_notes.tsv: nr. 137",
     "this ledger", "the note reads «al-Matkh»", 57, None),
    ("t. II, p. 41, n. ad nr. 150", "Part II tables (S13 geography)", "S13/geography/geo_p2_notes.tsv: nr. 150",
     "this ledger", "the note reads «anno 1835 Chesney»", 58, None),
    ("t. II, p. 41, n. ad nr. 152", "Part II tables (S13 geography)", "S13/geography/geo_p2_notes.tsv: nr. 152",
     "this ledger", "the note reads «39° 8′ E Gr., 37° 53′ N» (Kiepert)", 59, None),
    ("t. II, p. 41, n. ad nr. 155", "Part II tables (S13 geography)", "S13/geography/geo_p2_notes.tsv: nr. 155",
     "this ledger", "the note reads «Urbem, Mawzan quoque appellata»", 60, None),
    ("t. II, p. 44, n. ad nr. 189", "Part II tables (S13 geography)", "S13/geography/geo_p2_notes.tsv: nr. 189 (ad-Daybul)",
     "this ledger", "addition: the site of ad-Daybul", 61, None),
    ("t. II, p. 45, n. ad nr. 199", "Part II tables (S13 geography)", "S13/geography/geo_p2_notes.tsv: nr. 199 (Ctesiphon)",
     "this ledger", "addition: the forms of the name of Ctesiphon", 62, None),
    ("t. II, p. 47, n. ad nr. 213", "Part II tables (S13 geography)", "S13/geography/geo_p2_notes.tsv: nr. 213 (Asdūd)",
     "this ledger", "addition: another example of the form Asdūd", 63, None),
    ("t. II, p. 48, n. ad nr. 219", "Part II tables (S13 geography)", "S13/geography/geo_p2_notes.tsv: nr. 219",
     "this ledger", "the note reads «(V, 15, 1)»", 64, None),
    ("t. II, p. 49, n. ad nr. 230", "Part II tables (S13 geography)", "S13/geography/geo_p2_notes.tsv: nr. 230",
     "this ledger", "the note reads «(VI, 7, 4)»", 65, None),
    ("t. II, p. 49, n. ad nr. 231", "Part II tables (S13 geography)", "S13/geography/geo_p2_notes.tsv: nr. 231 (Sera metropolis)",
     "this ledger", "addition: the site of Sera metropolis", 66, None),
    ("t. II, p. 50, nr. 238", "Part II tables (S13 geography)", "S13/geography/geo_p2.tsv: p. 50, nr. 238 (Madīnat aṭ-Ṭīb), longitude 81° 0′",
     "this ledger", "82° for 81°", 67, None),
    ("t. II, p. 51, n. ad nr. 239", "Part II tables (S13 geography)", "S13/geography/geo_p2_notes.tsv: nr. 239",
     "this ledger", "addition: de Goeje on the Gypsies", 68, None),
    ("t. II, p. 52, n. ad nr. 248", "Part II tables (S13 geography)", "S13/geography/geo_p2_notes.tsv: nr. 248 (an-Nīrūn)",
     "this ledger", "addition: an-Nīrūn is Ḥaydarābād of Sindh", 69, None),
    ("t. II, p. 60, in titulo", "Part II tables (S06 spherical astronomy)", "S06/spherical/sph_pages.tsv: p. 60, the Arabic title",
     "this ledger", "the title is transcribed «... يب جزء ... وعرف احدهما ...»; the addenda read جزءًا and يعرف", 70, None),
    ("t. II, p. 71, lin. ult., col. V", "Part II tables (S06 spherical astronomy)", "S06/spherical/sph_p2.tsv: p. 71, Aquarius 30, hours 13° 33′",
     "S06/spherical/spherical_discrepancies.tsv (Nallino, Part II p. 222)", "computed for 36° 0′: 13° 34.7′", 71, None),
    ("t. II, p. 79, ad nr. 35", "Part II tables (S06 equations)", "S06/equations/equations_p2.tsv: p. 79, Moon 35°, 2° 40′ 12″",
     "S06/equations/equations_discrepancies.tsv (Nallino, Part II p. 226)", "computed 2° 40′ 52.6″", 72,
     "79, ad nr. 35: 2° 40′ 52″ (نب pro يب 12″)"),
    ("t. II, p. 79, ad nr. 36", "Part II tables (S06 equations)", "S06/equations/equations_p2.tsv: p. 79, Moon 36°, 2° 45′ 17″",
     "S06/equations/equations_discrepancies.tsv (Nallino, Part II p. 226)", "computed 2° 44′ 59.5″", 72,
     "ad nr. 36: 2° 44′ 57″ (مد نز pro 45′ 17″ مه يز)"),
    ("t. II, p. 79, ad nr. 37", "Part II tables (S06 equations)", "S06/equations/equations_p2.tsv: p. 79, Moon 37°, 2° 49′ 42″",
     "S06/equations/equations_discrepancies.tsv (Nallino, Part II p. 226); S05 observation on AB01-PDF0446-body-L008",
     "the addenda print 22″ where Nallino's note restores 2″ (ب for مب); computed 2° 49′ 4″", 72,
     "ad nr. 37: 2° 49′ 22″ (pro 42″)"),
    ("t. II, p. 87", "Part II tables (S06 syzygies, Roman)", "S06/syzygies/rsyz_p2.tsv: p. 87, the third table",
     "S06/syzygies/README.md (Nallino, Part II p. 230)", "corrections of the third (lower) table as given on Part II, p. 230", 73, None),
    ("t. II, p. 88", "Part II tables (S06 eclipses)", "S06/eclipses/eclipses_p2.tsv: p. 88, the solar limits 191° 16′ and 348° 44′",
     "S06/eclipses/ecl_discrepancies.tsv (Nallino, Part II pp. 209 and 231)", "in the western values of the letters", 74, None),
    ("t. II, p. 89, ad nr. 18", "Part II tables (S06 eclipses)", "S06/eclipses/eclipses_p2.tsv: p. 89, correction 18, portion 1′ 22″",
     "S06/eclipses/ecl_discrepancies.tsv (Nallino, Part II p. 231)", "1′ 42″, the mean of 12° and 24°", 75,
     "89, ad nr. 18: in port. longinq. pro 1′ 22″ l. 1′ 42″."),
    ("t. II, p. 89, in titulo", "Part II tables (S06 eclipses)", "S06/eclipses/ecl_pages.tsv: p. 89, title «جدول لتقويم»",
     "this ledger", "جدول التقويم for the printed جدول لتقويم", 75, "In titulo l. جدول التقويم."),
    ("t. II, p. 95, in titulo", "Part II tables (S06 parallaxes)", "S06/parallax: p. 95, title, latitude 16° 32′",
     "S06/parallax/par_discrepancies.tsv (Nallino, Part II p. 237)", "computed 16° 38′ 48″ for 13ʰ", 76, None),
    ("t. II, p. 96, in titulo", "Part II tables (S06 parallaxes)", "S06/parallax: p. 96, title, latitude 24°",
     "S06/parallax/par_discrepancies.tsv (Nallino, Part II p. 237)", "computed 24° 4′ 47″ for 13ʰ 30ᵐ", 77, None),
    ("t. II, p. 97", "Part II tables (S06 parallaxes)", "S06/parallax: p. 97, Cancer, 2 hours after culmination, longitude 21′",
     "S06/parallax/par_discrepancies.tsv (Nallino, Part II p. 237)", "the hour before culmination has 22′", 78, None),
    ("t. II, p. 101, in titulo", "Part II tables (S06 parallaxes)", "S06/parallax: p. 101, title, latitude 48° 13′",
     "S06/parallax/par_discrepancies.tsv (Nallino, Part II p. 237)", "computed 48° 52′ 46″ for 16ʰ", 79, None),
    ("t. II, p. 116, ult. lin.", "Part II tables (S06 planets)", "S06/planets: p. 116, Jupiter 90°, third column 5° 14′",
     "S06/planets/planets_discrepancies.tsv (Nallino, Part II p. 238)", "computed 5° 14.6′", 80, None),
    ("t. II, p. 117, lin. 1", "Part II tables (S06 planets)", "S06/planets: p. 117, Jupiter 91°, third column 5° 14′",
     "S06/planets/planets_discrepancies.tsv (Nallino, Part II p. 238)", "computed 5° 14.8′", 81, None),
    ("t. II, pp. 142-143", "Part II tables (S06 apparitions)", "S06/apparitions/apparitions_p2.tsv: pp. 142-143",
     "S06/apparitions/apparitions_discrepancies.tsv (Nallino, Part II p. 269)", "the readings of Theon and of the Latin Almagest that Nallino adopts", 82, None),
    ("t. II, pp. 144-177", "Part II tables (S13 star catalogue)", "S13/star_catalogue/p2_stars.tsv, p2_notes.tsv: pp. 144-177",
     "this ledger", "the supplements stand in Part II, pp. 278-283 (AB01-PDF0727 to AB01-PDF0732), with the emendations of the notes at Ursa minor 3, Sagittarius 15 and 16, Orion 2, Centaurus 22 (20 in the notes of p. 174) and Piscis australis 4 (3 in the notes of p. 176)",
     83, None),
    ("t. II, p. 182, n. ad nr. 40", "Part II tables (S13 status tables)", "S13/status_1211/st_p2_notes.tsv: nr. 40",
     "S13/status_1211/st_discrepancies.tsv (degree/minute sign in Nallino's note)", "the note reads «in B cod. نط 59′ pro لط 39′»", 84, None),
    # ---- to the second volume: Nallino's notes and glossary
    ("t. II, p. 194", "Part II notes (S07)", "AB01-PDF0643-body-L028-L030", OBS + "S07/adnotationes/records/AB01-PDF0643.json",
     "addition: Ptolemy Lagus in Ibn al-Athīr and Abū ’l-fidā’", 85, None),
    ("t. II, pp. 194-195", "Part II notes (S07)", "AB01-PDF0643-body-L039-L042; AB01-PDF0644-body-L001-L002",
     OBS + "S07/adnotationes/records/AB01-PDF0643.json, 0644", "addition: the vowels of Māmā", 86, None),
    ("t. II, p. 195", "Part II notes (S07)", "AB01-PDF0644-body-L007-L008", OBS + "S07/adnotationes/records/AB01-PDF0644.json",
     "addition: Daqyūs in north-western Africa", 87, None),
    ("t. II, pp. 195-197", "Part II notes (S07)", "AB01-PDF0644-body-L033-L035; AB01-PDF0645-body-L007-L010; AB01-PDF0645-body-L016-L017; AB01-PDF0645-body-L025-L028",
     OBS + "S07/adnotationes/records/AB01-PDF0644.json, 0645", "addition: Heraclius confused with Hercules", 88, None),
    ("t. II, pp. 201-202", "Part II notes (S07)", "AB01-PDF0650-body-L029-L030", OBS + "S07/adnotationes/records/AB01-PDF0650.json",
     "addition: the Latin month names in Ibn Ǵubayr", 89, None),
    ("t. II, p. 218, n. 2", "Part II notes (S07)", "AB01-PDF0667-notes_left-L003-L009", OBS + "S07/adnotationes/records/AB01-PDF0667.json",
     "addition: Marçais on Qal‘at Banī Ḥammād", 90, None),
    ("t. II, p. 234, lin. 6", "Part II notes (S07)", "AB01-PDF0684-body-L006", OBS + "S07/adnotationes/records/AB01-PDF0684.json; S05 observation on AB01-PDF0447-body-L022",
     "misprint in the addenda: the words stand on p. 235, line 6", 91, "234,6: deleantur verba nomina intra minimum circulum omittens. Insunt enim, licet haud paucum depravata."),
    ("t. II, p. 234, lin. 8 (= p. 235, lin. 8)", "Part II notes (S07)", "AB01-PDF0684-body-L008", OBS + "S07/adnotationes/records/AB01-PDF0684.json",
     "printed «ڡاطاعرڡا»", 91, "Lin. 8 l. قاطاعرقا."),
    ("t. II, p. 235, n. 1, lin. 3", "Part II notes (S07)", "AB01-PDF0684-notes_left-L003", OBS + "S07/adnotationes/records/AB01-PDF0684.json",
     "printed «sapienti»", 92, None),
    ("t. II, p. 291, lin. 14", "Part II notes (S07)", "AB01-PDF0740-body-L014", OBS + "S07/adnotationes/records/AB01-PDF0740.json",
     "printed «haec quantitates»", 93, None),
    ("t. II, p. 312, lin. 24", "Part II notes (S07)", "AB01-PDF0761-body-L024", OBS + "S07/adnotationes/records/AB01-PDF0761.json",
     "printed «ζοδιακῷ»", 94, None),
    ("t. II, p. 338, lin. 6", "Part II glossary (S09)", "AB01-PDF0787-body-L006", OBS + "S09/glossarium/records/AB01-PDF0787.json",
     "printed «und» in Lane's English", 95, None),
    # ---- to the third volume (Part III): the Arabic text
    ("t. III, p. ٢١, lin. 22", "Part III Arabic text (S10)", "AB01-PDF1131-L19", OBS + "S10/textus/records/AB01-PDF1131.json",
     "printed السَّنْويّ", "447:L029", "Pag. ٢١, lin. 22, forte l. السّٰنَوِيّ = السَّانَوِيّ."),
    ("t. III, p. ٢٦, lin. 18", "Part III Arabic text (S10)", "AB01-PDF1126-L18", OBS + "S10/textus/records/AB01-PDF1126.json",
     "printed الأَنْذَلُس", "447:L029", "٢٦,18, l. الأَنْدَلُس."),
    ("t. III, p. ٢٨, lin. 12", "Part III Arabic text (S10)", "AB01-PDF1124-L12", OBS + "S10/textus/records/AB01-PDF1124.json",
     "printed ارقيانس", "447:L029", "٢٨,12, l. اوقيانس."),
    ("t. III, p. ٣٥, n. 3", "Part III Arabic text (S10)", "AB01-PDF1117 (note 3)", OBS + "S10/textus/records/AB01-PDF1117.json",
     "printed «Addidi, Platonem sequens.»", "447:L029-L030", "٣٥, n. 3, l. addidi ex coniectura."),
    ("t. III, p. ٤٢, lin. 15", "Part III Arabic text (S10)", "AB01-PDF1110-L15", OBS + "S10/textus/records/AB01-PDF1110.json",
     "printed المُعوَّجة", "447:L030", "٤٢,15, l. المُعْوَجَّة."),
    ("t. III, p. ٧٣, lin. 12", "Part III Arabic text (S10)", "AB01-PDF1079-L12", OBS + "S10/textus/records/AB01-PDF1079.json",
     "printed لط كه كب (39;25,22); Part I, p. 48 has 39p 27′ 22″", "447:L030", "٧٣,12, l. كب (cod. كه) لط كز (cfr. t. I, 48)."),
    ("t. III, p. ٨٣, lin. 7", "Part III Arabic text (S11)", "AB01-PDF1069-L07", OBS + "S11/textus/records/AB01-PDF1069.json",
     "printed صار مركزه في فلك البروج", "447:L031", "٨٣,7, l. صار [مركزُه] مركزَ فلك البروج (cfr. I, 54, n. 11)."),
    ("t. III, p. ٩٥, lin. 16", "Part III Arabic text (S11)", "AB01-PDF1057-L13", OBS + "S11/textus/records/AB01-PDF1057.json",
     "line 16 by the margin numbers is L13: printed يكون بقدر تعديله الأوْسَط", "447:L031; 448:L001",
     "٩٥,16, l. يكون بقدر [وتر] تعديله الاوسط (cfr. II, p. xx)."),
    ("t. III, p. ١١٢, lin. 4", "Part III Arabic text (S11)", "AB01-PDF1040-L04", OBS + "S11/textus/records/AB01-PDF1040.json",
     "printed على حَدَّته", "448:L001", "١١٢,4, l. حِدَته."),
    ("t. III, p. ١٣٧, lin. 1", "Part III Arabic text (S11)", "AB01-PDF1015-L01", OBS + "S11/textus/records/AB01-PDF1015.json",
     "the line begins with القمر", "448:L001", "١٣٧,1, pro القمر l. سمت القمر."),
    ("t. III, p. ١٦١, lin. 3", "Part III Arabic text (S12)", "AB01-PDF0991-L03", OBS + "S12/textus/records/AB01-PDF0991.json",
     "printed فخُذْ حاصَّة الشمس", "448:L001-L002", "١٦١,3, pro الشمس l. القمر (cfr. I, 106, n. 5)."),
    ("t. III, p. ١٨١, lin. 18", "Part III Arabic text (S12)", "AB01-PDF0971-L15", OBS + "S12/textus/records/AB01-PDF0971.json",
     "line 18 by the margin numbers is L15: printed المتأَخِّرْون", "448:L002", "١٨١,18, l. المتأَخرون."),
    ("t. III, p. ١٨٩, lin. 7", "Part III Arabic text (S12)", "AB01-PDF0963-L07", OBS + "S12/textus/records/AB01-PDF0963.json",
     "والرشاء, the twenty-eighth mansion, is missing after الفرغ المؤخر", "448:L002", "١٨٩,7 post الفرغ المؤَخَّر inserendum والرِّشَاء."),
    ("t. III, p. ١٩١, lin. 3", "Part III Arabic text (S12)", "AB01-PDF0961-L03", OBS + "S12/textus/records/AB01-PDF0961.json",
     "printed ونَحْوَه", "448:L003", "١٩١,3, l. او نحوه (cfr. I, 127, n. 3)."),
    ("t. III, p. ١٩٨, lin. 5", "Part III Arabic text (S12)", "AB01-PDF0954-L05", OBS + "S12/textus/records/AB01-PDF0954.json",
     "the fifth printed line of the page (margin number 8): printed في الأقاليم", "448:L003", "١٩٨,5, l. وفي الاقاليم (cfr. I, 132, n. 3)."),
    ("t. III, p. ٢٠٢, lin. 4", "Part III Arabic text (S12)", "AB01-PDF0950-L03-L04", OBS + "S12/textus/records/AB01-PDF0950.json",
     "words lost after الذي وصفت لك, restored by conjecture", "448:L003-L005",
     "٢٠٢,4 ut monui t. I, p. 316, n. 3, procul dubio post الذي وصفت لك nonnulla in cod. et Plat. exciderunt, hoc modo circiter restituenda: فما كان ٱضربه في ازمان ساعات الجزء التالي."),
    ("t. III, p. ٢١٠, lin. 2", "Part III Arabic text (S12)", "AB01-PDF0942-L02", OBS + "S12/textus/records/AB01-PDF0942.json",
     "printed فوصَفْنا", "448:L005-L007",
     "٢١٠,2 pro فوصفنا ponendum, ut cod. habet, واتينا على كلّ ما يحتاج ان يقدَّم ذكرُهُ بقدر الطاقة فنرى ان نختم في هذا الموضع بوصفنا (cfr. t. I, p. 321)."),
    ("t. III, p. ٢١٢, lin. 13", "Part III Arabic text (S12)", "AB01-PDF0940-L13", OBS + "S12/textus/records/AB01-PDF0940.json",
     "printed نحيِّز ... حِيزًا; L20 and p. ٢١٣, line 10 have نحُزّ", "448:L007",
     "٢١٢, 13 pro نحيز . . . حيزًا codicis, l. نحُزّ . . . حَزًّا (ut recte ٢١٢,20 et ٢١٣,10)."),
    ("t. III, p. ٢١٧, lin. 10", "Part III Arabic text (S12)", "AB01-PDF0935-L10", OBS + "S12/textus/records/AB01-PDF0935.json",
     "printed خطّ الشَّاقول", "448:L008", "٢١٧,10 l. خيط الشاقول (cfr. ٢١٥,12)."),
    ("t. III, p. ٢٢٤, lin. 11", "Part III Arabic text (S12)", "AB01-PDF0928-L09", OBS + "S12/textus/records/AB01-PDF0928.json",
     "line 11 by the margin numbers is L09: printed تسيُّر", "448:L008", "٢٢٤,11, l. تسيير (cod. تسير)."),
    # ---- to the third volume: the tables
    ("t. III, p. ٢٢٨, in titulo", "Part III tables (S13 chronology)", "S13/chronology/chr_p3.tsv: p. 228, T01, «ومنه بتأْريخ المِجِسْطِي»",
     "this ledger", "تاريخ for بتاريخ, as Nallino's note in Part II, p. 191 says", "448:L008-L009", "٢٢٨, in titulo probabiliter l. تاريخ (cfr. II, 191)."),
    ("t. III, p. ٢٢٩, lin. 4, col. I", "Part III tables (S13 chronology)", "S13/chronology/chr_p3.tsv: p. 229, R03, «بطلميوس أَرْنَب»",
     "S13/chronology/chr_p3.tsv, doubt column (Part II p. 194)", "ارنبا for Nallino's printed أرنب (the codex اربيا)", "448:L009", "٢٢٩,4 col. I, l. ارنبا (cfr. II, 194)."),
    ("t. III, p. ٢٣٠, lin. 8, col. II", "Part III tables (S13 chronology)", "S13/chronology/chr_p3.tsv: p. 230, L08, «هرقلس صاحب العرب»",
     "this ledger; S07 observation on AB01-PDF0644-body-L033-L035", "صاحب العرف, Nallino's conjecture in Part II, p. 195", "448:L009-L010",
     "٢٣٠,8 col. II, probabiliter l. صاحب العرف (cfr. II, 195-197 et xxx)."),
    ("t. III, p. ٢٣١, lin. 6", "Part III tables (S13 chronology)", "S13/chronology/chr_p3.tsv: p. 231, R06, «... هرقل صاحب العرب»",
     "this ledger", "صاحب العرف, as on p. ٢٣٠", "448:L009-L010", "et ٢٣١,6, probabiliter l. صاحب العرف."),
    ("t. III, p. ٢٣١, lin. 3 a fine", "Part III tables (S13 chronology)", "S13/chronology/chr_p3.tsv: p. 231, 2R05, «وكانت الشَّوْرَى»",
     "this ledger", "الشُّورَى for the printed الشَّوْرَى", "448:L010", "٢٣١,3 a fine, l. الشُّورَى."),
    ("t. III, p. ٢٥١, Aurigae 2", "Part III tables (S13 star catalogue)", "S13/star_catalogue/p3_stars.tsv: p. 251, R04, Auriga 2, «وهو ﴿العَيُّوق﴾»",
     "this ledger", "العنز for العيوق", "448:L010-L011", "٢٥١, in secunda stella Aurigae, pro العيوق l. العنز."),
    ("t. III, p. ٢٦٤, n. 2", "Part III tables (S13 star catalogue)", "S13/star_catalogue/p3_footnotes.tsv: p. 263 (AB01-PDF0889), note 2, «Error pro ذراع الساقي»",
     "this ledger; S05 observation on AB01-PDF0448-body-L011", "misprint in the addenda: the note is note 2 of p. ٢٦٣ (Aquarius 8); note 2 of p. ٢٦٤ reads «Cod. الحوت»",
     "448:L011", "٢٦٤, n. 2, pro ذراع l. عضد."),
]


def s05_lines():
    out = {}
    for f in sorted((HERE / "records").glob("AB01-PDF04*.json")):
        rec = json.loads(f.read_text(encoding="utf-8"))
        for sec in rec["sections"]:
            for ln in sec["lines"]:
                out[ln["id"]] = ln["transcription"]
    return out


def main():
    text = s05_lines()
    ents = entries()
    assert len(ents) == 99, len(ents)
    rows = []
    for n, (printed, layer, targets, recorded, check, src, seg) in enumerate(ROWS, 1):
        ids = resolve(src, ents, text)
        missing = [x for x in ids if x not in text]
        if missing:
            raise SystemExit(f"S05-A{n:03d}: no such S05 line {missing}")
        entry = seg if seg else " / ".join(text[x] for x in ids)
        rows.append({"corrigendum_id": f"S05-A{n:03d}", "printed_target": printed, "target_layer": layer,
                     "target_anchors": targets, "source_line_ids": ", ".join(ids), "source_entry": entry,
                     "routing_status": "REGISTERED_NOT_APPLIED", "recorded_in": recorded, "check": check})
    cols = list(rows[0])
    with open(HERE / "corrigenda_routing.tsv", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in rows:
            fh.write("\t".join(r[c].replace("\t", " ").replace("\n", " ") for c in cols) + "\n")
    (HERE / "corrigenda_routing.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n",
                                                   encoding="utf-8", newline="\n")
    by = {}
    for r in rows:
        k = r["target_layer"].split(" (")[0]
        by[k] = by.get(k, 0) + 1
    print(len(rows), "rows;", ", ".join(f"{k}: {v}" for k, v in by.items()))


if __name__ == "__main__":
    main()

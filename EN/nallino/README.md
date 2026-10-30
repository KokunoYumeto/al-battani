# English translation of Nallino's notes on al-Battānī's *Zīj*

C. A. Nallino's *Al-Battānī sive Albatenii opus astronomicum* (Milan, 1899–1907) gives the Arabic text of the *Zīj* (Part III), a Latin translation of the canons with a commentary on them (Part I) and the tables in Latin with notes on them, a glossary and indexes (Part II). The canons are translated into English from the Arabic in [../](../). This folder translates Nallino's own writing, which is in Latin. No English translation of it has been published.

**Done:** the whole commentary of Part I, on chapters 3–57 and on the appendices A–H (pp. 151–327); the notes on the tables of pp. 1–83 (Part II, pp. 189–227). Read [nallino_en.pdf](nallino_en.pdf).

**Still to translate:** the rest of the notes on the tables (Part II, pp. 227–317), the prefaces and the addenda of Parts I and II, Nallino's footnotes to his Latin translation (Part I, pp. 1–150), the glossary and the indexes.

## How it is made

- The source is the line-by-line transcription of Nallino's Latin in this repository ([S03](../../S03/versio/), [S04](../../S04/versio/), [S07](../../S07/adnotationes/)). Every printed line is translated, in Nallino's order; nothing is summarised or left out. Each block of the English names the lines it translates; `build_nallino.py` checks that every line of a unit belongs to a block, that every one of Nallino's footnotes is called once, and that every redrawn figure of a translated page is set.
- Modern English, not the phrasing of a Latin crib. Technical terms follow the English *Zīj* ([../glossary.tsv](../glossary.tsv) gives Nallino's Latin equivalents). Proper names are given in a modern transliteration (al-Khwārizmī, Ibn Yūnus, Abū l-Wafāʾ). Bibliographical references keep their titles in the original languages.
- Nallino's quotations in Arabic, Greek, Hebrew and Syriac stand in their scripts, as he prints them, with his own translations of them in English. His quotations in Latin, Spanish, French, Italian and German keep the original words, followed by an English translation in parentheses.
- In the headings of the commentary, «p.» and «l.» are the pages and lines of Nallino's Latin translation of the canons (Part I, pp. 1–150).
- Nallino's footnotes are numbered as footnotes. The translator's notes are lettered; they record where the translation follows Nallino's own corrections in the *Addenda et emendanda* (Part I, pp. LXXI–LXXII; Part II, pp. XVI–XXVII), and where it sets a formula that the print gets wrong in the form the argument needs.
- The pages of Nallino's volumes stand in the margin (I 153 is Part I, p. 153).

## Files

| File | Content |
|---|---|
| `units.tsv` | the units of the translation, in the order of the edition, with the lines of the Latin that each covers |
| `text/*.txt` | one file per unit: each block of English with the lines it translates, Nallino's footnotes and the translator's notes; the format is described at the head of `build_nallino.py` |
| `build_nallino.py`, `make_pdf.py` | check the coverage of the Latin lines, the footnotes and the figures, and build the PDF deterministically |
| `tools/latin.py` | the Latin of a unit in reading order, with the observations of the page records |
| `figures/`, `tools/figures_en.py` | the redrawn figures whose labels have words, with the words in English |
| `alignment.tsv` | every block of the English with its lines and pages |
| `checkpoint.json` | the units done and a checksum over their files |

## Credits

- C. A. Nallino: the Latin translation, the commentary and the apparatus (1899–1907), in the public domain.
- The translation: AI-translated (Claude), 2026. No person has proofread it. Dedicated to the public domain (CC0 1.0).

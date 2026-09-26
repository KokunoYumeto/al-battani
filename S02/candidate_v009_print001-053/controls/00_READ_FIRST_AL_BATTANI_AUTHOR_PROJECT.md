# Al-Battani — one-author source Project

This is an additive, source-gated Project for the securely attributed and reader-relevant corpus of Abū ʿAbd Allāh Muḥammad ibn Jābir al-Battānī. It supersedes no source, packet, edition, or output. It performs no transcription by being uploaded.

## Start here

1. Read files `00` through `11` before choosing a session.
2. Paste exactly one dormant `12_SESSION_*.txt` through `27_SESSION_*.txt` prompt. Do not run every session at once.
3. Work only on the ranges and roles assigned to that session. Return a cumulative checkpoint and the required evidence ledgers.
4. Never produce a bilingual or facing-page reader. Produce a separate Arabic source edition, a separate historical Latin/Nallino edition where that layer is being preserved, and one separate monolingual edition for each target language.

## Corpus boundary

Tier A is the complete extant *al-Zīj al-Ṣābiʾ*: 57 chapters and tables. The controlling local witness is Nallino’s three-part 1,162-page edition. It contains distinct authorship layers: al-Battānī’s Arabic text and tables; Nallino’s Latin translation, notes, prefaces, indices, and edition apparatus; and copy-specific scan matter. Never collapse these roles.

Tier B maps five smaller works reported by the primary bibliography. Two have complete usable payloads here: the astrological-history work in a 136-page Arabic/English critical publication, and the 40-chapter commentary on Ptolemy’s *Tetrabiblos* as a 122-page-side CC BY transcription. The trigonometric *Tajrīd* remains source-unacquired and attribution-questioned. Two other titles are probably the material already present as Zīj chapters 54 and 55; do not create duplicate works without evidence.

## Controlling sources

- `30_NALLINO_PARS_I_II_III_MASTER_1162P.pdf`: complete 600/604-ppi master; SHA-256 and topology are in `03_SOURCE_WITNESS_GATE.tsv`.
- `31_NALLINO_PARS_III_RGB_COMPARATOR_292P.pdf`: 400-ppi RGB Part III comparator.
- `35_KENNEDY_ET_AL_ASTROLOGICAL_HISTORY_136P.pdf`: full article, Arabic edition, English translation, diagrams, recomputation, and commentary. Its CC BY-NC-ND license permits use as a source/reference but does not authorize a derivative republication of the editors’ article.
- `36_PAL_TETRABIBLOS_COMMENTARY_CC_BY_XML.zip`: exact-commit CC BY 4.0 transcription, Escorial árabe 969 fols.20r–80v.
- `32`, `33`, and `34`: prior component, working state, and page-map evidence. They are continuity/recovery material, never authority over the scans.

## Non-negotiable production rules

- Immutable diplomatic/source-language layer, separate faithful translation, separate restrained critical apparatus.
- Direct source replay; OCR and prior TeX are witnesses only.
- Never silently modernize, correct, complete, or reattribute.
- Every formula, table cell, diagram, title, corrigendum, blank, and excluded page receives a disposition.
- If a figure or table cannot be faithfully reconstructed in editable form, use a highest-resolution authoritative crop plus a separate conservative presentation derivative and record hashes and operations.
- Remove “Digitized by Google,” library plates, barcodes, call numbers, bindings, and provider UI from the scholarly body, but preserve them in provenance/topology.
- No human review gate. Build, render, inspect, hash, disclose unresolved items, and use independent cold audit.

The first old component, T01, is already owned at master PDF450–455 / Part II printed pp.1–6. It must be replayed before reuse; the first untouched Tier-A source unit is Part I frontispiece/master PDF2 for complete-edition production, and Part II printed p.7/master PDF456 for continuation of the old table lane.

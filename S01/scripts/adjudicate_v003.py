from pathlib import Path
import json
from revision_helpers import change,read_rows,write_rows
R=Path(__file__).resolve().parents[1]
repl=[
('0037-body-L017','100–102','0037-G01','S01-U013'),
('0040-notes_left-L020','<ar>زِگ</ar>','0040-G01','S01-U004'),
('0070-body-L021','<ar>جزوأً</ar>','0070-G02','S01-U008'),
('0070-body-L021','<ar>تَهَيَّأَ</ar>','0070-G03','S01-U008'),
('0070-body-L025','<ar>تِلْقَاء</ar>','0070-G04','S01-U008'),
('0070-body-L026','<ar>تَلِهِ</ar>','0070-G05','S01-U008'),
('0070-body-L025','<ar>تَلَقَّى</ar>','0070-G06','S01-U008'),
('0070-body-L026','<ar>سَمِّ</ar>','0070-G07','S01-U008'),
('0079-body-L021','<ar>الصَّباء</ar>','0079-G01','S01-U009'),
('0079-body-L021','<ar>الصُّبَّاء</ar>','0079-G02','S01-U009'),
('0080-body-L026','pro <i>terrestrium</i>','0080-G01','S01-U010'),
('0084-body-L028','<ar>خُذِ المرآةَ واختبِرْ نُجُومًا</ar>     <ar>تُمِرُّ بِمَطْعَمِ الأَرْيِ المَشُورِ</ar>','0084-G01','S01-U012'),
('0084-body-L029','<ar>تَدُلُّ على الحِمام بلا ارتيابِ</ar>     <ar>ولكن لا تَدُلَّ على النُّشُورِ</ar>','0084-G02','S01-U012'),
('0086-body-L013','precipua','0086-G01','S01-U014')]
for line,old,g,u in repl:
 new=f'<glyph>AB01-PDF{g}</glyph>'
 if g=='0080-G01':new='pro '+new
 change('AB01-PDF'+line,old,new,'source/raw/AB01-PDF'+g+'-raw.png',f'{u}: withdraw the uncertain character-level representation in favor of an exact native source-image object. Earlier proposed text remains in immutable history and this change ledger; no historical correction is silently supplied.','source_image_fallback','high for pixel preservation; character-level interpretation remains unresolved')
notes=read_rows('critical_findings');assets={x['object_id']:x for x in read_rows('figure_provenance')}
configs={
'S01-U002':('RESOLVED_RETAINED','The native reread confirms the two unvocalized words المثبتة and المبينة. Retain the existing unvocalized transcription; no shaddah or other vowel mark is supplied.','history/interrupted_reread/qa/u002a_native.png',[]),
'S01-U003':('DISPOSED_IMAGE_FALLBACK','The Syriac place-name is preserved in its existing exact image. Its Unicode transcription is not promoted.','source/raw/AB01-PDF0022-G01-raw.png',['AB01-PDF0022-G01']),
'S01-U004':('DISPOSED_IMAGE_FALLBACK','The original Persian cluster includes more visible signs than the earlier زِگ encoding represented. Replace that provisional encoding with the entire native cluster; do not guess a normalized Persian spelling.','source/raw/AB01-PDF0040-G01-raw.png',['AB01-PDF0040-G01']),
'S01-U005':('RESOLVED_RETAINED','Native reread supports unaccented βιβλιον in this quotation. Preserve that printed form, rather than adding the expected Greek accent.','history/interrupted_reread/qa/u005_native.png',[]),
'S01-U006':('RESOLVED_RETAINED','The damaged initial letter is read as i in i. e.; comparison with the clean i. e. on the same mathematical page supports retaining the existing reading. Formula content is unchanged.','history/interrupted_reread/qa/u006a_native.png; history/interrupted_reread/qa/u006b_native.png',[]),
'S01-U007':('DISPOSED_IMAGE_FALLBACK','Retain the existing exact sign image. Identification as alif with waslah remains an interpretation, not a substituted code point.','source/raw/AB01-PDF0070-G01-raw.png',['AB01-PDF0070-G01']),
'S01-U008':('DISPOSED_IMAGE_FALLBACK','Six unusually vocalized examples are now preserved as exact native clusters, including the two additional examples on the same lines. The placement of vowels and lower marks is no longer silently approximated by modern Unicode vowel sequences.','qa/v003/p70_glyph_region.png',[f'AB01-PDF0070-G{x:02}' for x in range(2,8)]),
'S01-U009':('DISPOSED_IMAGE_FALLBACK','Preserve the original and corrected Arabic lemmas independently as exact images. Subbī/Ṣubbī remains typed. This records Nallino’s historical erratum; it does not apply the correction to printed p. XV.','qa/v003/p79_correction_region.png',['AB01-PDF0079-G01','AB01-PDF0079-G02']),
'S01-U010':('DISPOSED_IMAGE_FALLBACK','The left lemma visibly contains an intervening point or ink mark. It is now preserved as an image, so the two printed lemmas are no longer represented as visually identical words. Whether that point was intended is not decided.','qa/v003/p80_lemma_region.png',['AB01-PDF0080-G01']),
'S01-U011':('DISPOSED_IMAGE_FALLBACK','Retain both existing exact lemma images, separately and in their original order. No character-level expansion is asserted.','source/raw/AB01-PDF0082-G01-raw.png; source/raw/AB01-PDF0082-G02-raw.png',['AB01-PDF0082-G01','AB01-PDF0082-G02']),
'S01-U012':('DISPOSED_IMAGE_FALLBACK','Replace the uncertain fully vocalized transcription with two full native verse-line objects. Each preserves its original right-hand first hemistich and left-hand second hemistich. Earlier proposed text is retained only in version history and the change ledger, not certified as the reading.','qa/v003/p84_verse_region.png',['AB01-PDF0084-G01','AB01-PDF0084-G02'])}
for x in notes:
 x['previous_v002_status']=x['status'];x['review_responsibility']='Current producing assistant; not an independent cold auditor'
 if x['apparatus_id'] in configs:
  status,reason,evidence,oids=configs[x['apparatus_id']]
  x.update(status=status,reason=reason,witness_evidence=evidence,object_ids=oids,confidence=('source-image preservation exact; character interpretation not settled' if oids else 'source reread supports retained text'),proposed_critical_reading='No conjectural historical emendation adopted.')
  if oids:
   x['diplomatic_reading']='Exact source image object(s): '+', '.join(oids)
   x['source_rect_pt']=assets[oids[0]].get('source_rect_pt',assets[oids[0]].get('pdf_rect_pt'))
   x['coordinate_granularity']='native crop rectangles individually recorded in figure_provenance.json'
for u,lid,oid,reading,alts,reason in [
('S01-U013','AB01-PDF0037-body-L017','AB01-PDF0037-G01','100–102 / 106–102','100–102 / 106–102; the terminal digit is damaged','The source terminal digit in the first page number has a broken stroke. Exact pixels replace a confidently encoded 100; neither a numerical correction nor a conjecture is applied.'),
('S01-U014','AB01-PDF0086-body-L013','AB01-PDF0086-G01','precipua / previpua','precipua / previpua; the medial printed letter is unclear','The printed title word is difficult to encode faithfully at the damaged medial letter. Preserve the exact source word rather than regularizing the Latin title.')]:
 a=assets[oid]
 notes.append({'apparatus_id':u,'issue_class':'reading','source_anchor':lid.split('-body')[0],'line_id':lid,'source_rect_pt':a['source_rect_pt'],'coordinate_granularity':'native crop; see figure_provenance.json','diplomatic_reading':f'Exact image {oid} ({reading} not adjudicated)','faithful_translation':'No new target-language translation requested.','proposed_critical_reading':'No conjectural historical emendation adopted.','bounded_alternatives':alts,'required_hypotheses':'None; no calculation or expected grammar is used to replace the source.','witness_evidence':a['raw_path'],'reason':reason,'confidence':'exact image preservation; character-level interpretation unresolved','propagation_impact':'Nallino source layer only; Arabic authorial canon unchanged','prior_notice_result':'Identified by the recovered proof material and reread for v003; no exhaustive claim about earlier scholarship.','citation':f"Nallino (1903), SRC01 physical PDF{a['master_pdf_page']}; pinned source hash in source_evidence.json.",'status':'DISPOSED_IMAGE_FALLBACK','object_ids':[oid],'review_responsibility':'Current producing assistant; not an independent cold auditor','previous_v002_status':'NOT_PREVIOUSLY_FLAGGED'})
write_rows('critical_findings',notes)
# Retain character-interpretation limitations even though their image-preservation disposition is complete.
write_rows('unresolved_readings',[x for x in notes if x['status']!='RESOLVED_RETAINED'])
write_rows('v003_adjudications',notes)
print('Notes',len(notes),'image-disposed',sum(x['status']=='DISPOSED_IMAGE_FALLBACK' for x in notes))

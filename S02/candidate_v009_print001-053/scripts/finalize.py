"""Create provenance, run real builds, and package the bounded S02 successor.
All status fields are computed or explicitly attributed, not inferred from file names.
"""
from pathlib import Path
import csv,json,hashlib,subprocess,os,shutil,re,zipfile,sys,datetime
import fitz
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT.parent
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def js(path,obj):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def tsv(path,rows,fields):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',extrasaction='ignore');w.writeheader();w.writerows(rows)
if not (ROOT/'tex/S02_P041_043_checked.tex').is_file():raise RuntimeError('Corrected source not generated; no release.')
pages=[json.loads(p.read_text()) for p in sorted((ROOT/'transcription/pages').glob('*.json'))]
last=max(q['master_pdf_page'] for q in pages);assert last>=137
assert [q['master_pdf_page'] for q in pages]==list(range(90,last+1))
# Attribute the review accurately. The user supplied definitive source readings;
# restored subsequent drafts must not inherit a final source-verification claim.
for q in pages:
 n=q['master_pdf_page']
 if 130<=n<=132:
  q['review_responsibility']='User: explicit scan-checked correction message; assistant: encoding and line-form integration.'
  q['status']='USER_SCAN_CHECKED_READINGS_ACCEPTED_LINE_FORM_INTEGRATED'
 elif n>=133:
  q['status']='RESTORED_LINE_ANCHORED_SOURCE_CANDIDATE'
  q['review_responsibility']='Assistant continuation inherited from prior work and supplied source context; final image-to-render review is not certified in this export.'
 if n>=130:(ROOT/f'transcription/pages/{q["anchor"]}.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
# User's corrections are a precise and sufficient review input even when the
# separately named checked file is absent.
corrections=[
 ('U01','0130-body-L019','287','285','Damaged 5; embedded-text misreading, not a historical emendation.'),
 ('U02','0130-body-L019','fraction unresolved','1/20','Confirmed by user from scan.'),
 ('U03','0130-body-L025','Greek accent unresolved','[ἄρχων]','Brackets and accent retained.'),
 ('U04','0130-N04','untranscribed formula',r'\dfrac{1+1/5}{360}=\dfrac{6/5}{360}=\dfrac{6}{1800}=\dfrac{1}{300}.','Exact four-member printed chain; no inferred arrangement.'),
 ('U05','0131-body-L011;0131-body-L013','fraction unresolved','2/5 in both occurrences','Confirmed independently of arithmetic.'),
 ('U06','0131-P03;0131-N06;0131-N09;0131-N10','lowercase iv/v/vi','upright uppercase IV/V/VI superscripts','Seven numerical strings retained; order signs corrected.'),
 ('U07','0131-N09','30 and42 with unknown orders',r'Codex male 30^{IV} et 42^{VI}','Exact orders accepted.'),
 ('U08','0132-P05','PKLRMY uncertain','PKLRMY','Literal printed sequence preserved; semantic P05 anchor is stable.'),
 ('U09','0132-N02','unclosed citation flagged','no closing parenthesis','Printed omission retained, not silently repaired.'),
 ('E01','0130-body-L020','superantis, ad','superantis, --- ad','Second dash restored.'),
 ('E02','0130-N02;0131-N02;0131-N03','al-Battāni','al-Battānī','Final macron restored; source initial capital retained in p41n2.'),
 ('E03','0131-body-L008','Pachon','Pachōn','Printed macron restored.'),
 ('E04','0131-body-L020','efficiant','efficiunt','OCR misreading corrected.'),
 ('E05','0131-body-L017;0131-N05','365 degrees',r'365^d14′26″;365^d14′48″','Day superscripts, not degrees.'),
 ('E06','0131-N02','XXXII. Hunc','XXXII. --- Hunc','Dash restored.'),
 ('E07','0131-N05','24s. Ptolemaeus','24s. --- Ptolemaeus','Dash restored.'),
 ('E08','0131-N06','p.916.)','p.916.','Printed absence of closing parenthesis retained.'),
 ('E09','0131-N07','164 recto','fol.164,v.--166,v., et186,v.--189,r.','Verso locator; line break retained in source form.'),
 ('T01','0130-0132','roman Almag.','italic Almag.','All abbreviation occurrences in reviewed range.'),
 ('T02','0130-0132','roman or whole italic parentheses','italic a-d letters inside roman parentheses','Historical apparatus calls, not new notes.'),
 ('T03','0131-body-L024','roman medium Solis','italic medium Solis','Defined term.'),
 ('T04','0132-N04','quotation type incomplete','source italic phrase and repeated line-initial «','The quoted quae...nant phrase, not the entire first line, is italic.'),
 ('T05','0131-N04;0131-N05;0131-N08','upright d h m s','italic d h m s','Mathematical time units retain italic letters.'),
 ('T06','0131-N02;0131-N05;0131-N06;0131-N09;0131-N10;0132-N03','ordinary spacing','letter-spaced proper names','Ibn Yūnus, Caussin, Halley, specified Ptolemaeus occurrences, Schiaparelli.'),
 ('L01','0130-body-L006','missing locator','p.62 right at printed l6','Line-form integration; user supplied position.'),
 ('L02','0130-body-L030','missing locator','p.63 right at printed l30','Line-form integration; user supplied position.'),
 ('L03','0131-body-L017','missing locator','p.64 left at printed l17','Line-form integration; user supplied position.'),
 ('L04','0132-P02','missing locator','p.65 right at printed l15','Source-line number, not sequential L anchor.'),
 ('L05','0132-P05','missing locator','p.66 right at printed last line39','Seam locator retained.'),
 ('L06','0130-0132','line numbers absent','visible 5-line source numbering','Heading/blank positions are included in printed-source line-number sequence.'),
 ('S01','0132-P05;0133-P01','seam at p43/44','denique arcum PKLRMY excentrici eam excentrici / partem quam Sol medio suo itinere','No supplied word, punctuation or new paragraph substituted at source seam.')]
rows=[dict(id=i,source_anchor='AB01-PDF'+a,before=b,after=c,disposition='ACCEPTED',responsibility='User scan-check; assistant integration',comment=d) for i,a,b,c,d in corrections]
tsv('ledgers/accepted_user_corrections.tsv',rows,['id','source_anchor','before','after','disposition','responsibility','comment'])
# Retain a machine-readable exact user report, separated from a checked-file claim.
js('receipts/user_review_acceptance.json',{'reviewed_printed_pages':[41,43],'reviewed_master_pages':[130,132],'resolved_flag_ids':[f'U{i:02}' for i in range(1,10)],'accepted_correction_rows':len(rows),'checked_file_received':False,'basis':'Detailed user scan-check message, not an acquired copy of the separately mentioned checked TeX file.','reading_status':'ALL_NINE_FLAGS_RESOLVED_BY_USER_SCAN_REVIEW','line_form_status':'LOCATORS_LINE_NUMBERS_AND_QUOTE_CONTINUATIONS_INTEGRATED','full_session_closed':False})
# Ledgers and human-readable transcription, without modifying inherited JSON.
line_rows=[];margins=[];formula=[];plain=[];new_counts={}
for q in pages:
 n=q['master_pdf_page'];plain.append('\n## AB01-PDF%04d | printed %d\n'%(n,n-89));seq=0
 if n>=130:
  for sec in q['sections']:
   plain.append('['+sec['authorship']+' / '+sec['role']+']')
   for l in sec['lines']:
    plain.append(l['id']+'\t'+l['tex']);line_rows.append({'id':l['id'],'master_pdf_page':n,'printed_page':n-89,'source_line_no':l['source_line_no'],'role':l['source_role'],'semantic_anchor':l['semantic_anchor'] or '', 'tex':l['tex']})
    for m in re.finditer(r'(?<!\\)\$(.*?)(?<!\\)\$',l['tex']):
     seq+=1;formula.append({'id':f'AB01-PDF{n:04}-M{seq:03}','line_anchor':l['id'],'tex':m.group(1),'role':l['source_role'],'status':'Literal source/candidate expression; not silently normalized'})
  margins.extend(dict(master_pdf_page=n,printed_page=n-89,**a) for a in q.get('margin_locators',[]))
  new_counts[n]=sum(len(s['lines']) for s in q['sections'])
 else:plain.append('[Inherited page record retained byte-for-byte in transcription/pages; see prior formatted text.]')
(ROOT/'transcription/S02_NEW_P041_LAST_LINE_ANCHORED.txt').write_text('\n'.join(plain[plain.index(next(v for v in plain if '## AB01-PDF0130' in v)):])+'\n')
tsv('ledgers/new_line_alignment.tsv',line_rows,['id','master_pdf_page','printed_page','source_line_no','role','semantic_anchor','tex'])
tsv('ledgers/new_margin_locators.tsv',margins,['master_pdf_page','printed_page','line','text','side','line_anchor'])
tsv('ledgers/new_formula_objects.tsv',formula,['id','line_anchor','tex','role','status'])
# Page-disposition ledger covers the entire assigned range, not only saved pages.
dispositions=[]
for n in range(90,199):
 status=('INHERITED_PP1_40_UNCHANGED' if n<130 else 'USER_SCAN_CHECKED_READINGS_INTEGRATED' if n<=132 else 'CONTINUATION_CANDIDATE' if n<=last else 'NOT_TRANSCRIBED')
 dispositions.append({'source_anchor':f'AB01-PDF{n:04}','printed_page':n-89,'status':status,'provider_matter':'Excluded from historical reader; retained only in source evidence','source_roles':'NALLINO_TRANSLATION;NALLINO_APPARATUS'})
tsv('ledgers/page_disposition.tsv',dispositions,['source_anchor','printed_page','status','provider_matter','source_roles'])
open_rows=[{'id':'S02-v009-U001','anchor':'AB01-PDF0140-body-L001','category':'reading','reading':'.n / in','status':'Exact damaged source crop retained; the missing part of the first character is not supplied.'},{'id':'S02-v009-VISUAL','anchor':f'AB01-PDF0133–AB01-PDF{last:04}','category':'verification','reading':'Source-to-render comparison','status':'Final visual/philological checking is not certified by this package. Render files and build outcomes are supplied for replay.'}]
tsv('ledgers/unresolved_readings.tsv',open_rows,['id','anchor','category','reading','status'])
ts=[{'id':'H01','anchor':'AB01-PDF0134-body-L010','category':'printed discrepancy','detail':'secet Planeta: no full stop supplied.'},{'id':'H02','anchor':'AB01-PDF0136-body-L015;AB01-PDF0136-N02','category':'formula','detail':'Body 1p33′ retained separately from note verbal reading thirty-three seconds.'},{'id':'H03','anchor':'AB01-PDF0135-P03;AB01-PDF0136-P02','category':'formula','detail':'58p12′34″ versus58p12′32″ retained; passages are not made identical.'},{'id':'H04','anchor':'AB01-PDF0140-body-L020;AB01-PDF0140-body-L021','category':'reading','detail':'Repeated in at source line seam retained in candidate.'},{'id':'H05','anchor':'AB01-PDF0141-N01','category':'reference','detail':'Candidate citation293–206 retained rather than normalized; final checking outstanding.'}]
tsv('ledgers/historical_discrepancies.tsv',ts,['id','anchor','category','detail'])
js('receipts/canonical_synchronization.json',{'canonical_arabic_checkpoint':None,'canonical_arabic_modified':False,'new_target_language_translations':[],'historical_latin_checkpoint':'S02_v009','accepted_changes_apply_to':'Historical Nallino transcription only','S01_modified':False,'S03_started':False,'human_review_required_to_continue':False})
tsv('ledgers/proposed_canonical_corrections.tsv',[],['id','canonical_anchor','proposal','source_evidence','status'])
# Derive an original-pixel-preserving excerpt directly from the controlling master.
master=BASE/'30_NALLINO_PARS_I_II_III_MASTER_1162P.pdf';doc=fitz.open(master);ex=fitz.open();ex.insert_pdf(doc,from_page=89,to_page=last-1)
evidence=ROOT/f'source/SRC01_PDF0090_{last:04}_EVIDENCE.pdf';ex.save(evidence,garbage=4,deflate=True,no_new_id=True);ex.close()
with fitz.open(evidence) as ed:
 identical=[]
 for i in range(len(ed)):
  a=ed[i].get_pixmap(dpi=72);b=doc[i+89].get_pixmap(dpi=72);identical.append((a.width,a.height,a.samples)==(b.width,b.height,b.samples))
 assert all(identical)
js('receipts/source_excerpt_identity.json',{'source_master_sha256':H(master),'excerpt_file':evidence.relative_to(ROOT).as_posix(),'excerpt_sha256':H(evidence),'physical_master_range':[90,last],'excerpt_pages':last-89,'render_comparison_dpi':72,'all_page_pixels_match':all(identical)})
# Build outputs are asserted only from actual exit codes and logs.
env=os.environ.copy();env.update(SOURCE_DATE_EPOCH='1790467200',FORCE_SOURCE_DATE='1',TZ='UTC')
texfiles=[ROOT/'tex/S02_NALLINO_SOURCE_v009.tex',ROOT/'tex/S02_P041_043_checked.tex',ROOT/f'tex/S02_P044_{last-89:03}_source_replayed.tex']
builds=[]
for tex in texfiles:
 runs=[]
 for label in ['A','B']:
  out=ROOT/f'qa/clean_build_{label}'/tex.stem;out.mkdir(parents=True,exist_ok=True);codes=[]
  for passno in [1,2]:
   try:
    r=subprocess.run(['xelatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error',f'-output-directory={out}',tex.name],cwd=ROOT/'tex',env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60)
    (out/f'pass{passno}.txt').write_bytes(r.stdout);codes.append(r.returncode)
    if r.returncode:break
   except Exception as e:codes.append(-1);(out/f'pass{passno}.txt').write_text(str(e));break
  pdf=out/(tex.stem+'.pdf');log=(out/(tex.stem+'.log')).read_text(errors='replace') if (out/(tex.stem+'.log')).exists() else ''
  ok=codes==[0,0] and pdf.is_file();pagesn=None
  if ok:
   with fitz.open(pdf) as f:pagesn=len(f)
  runs.append({'run':label,'returncodes':codes,'success':ok,'pdf_sha256':H(pdf) if ok else None,'pages':pagesn,'missing_character_lines':[l for l in log.splitlines() if 'Missing character' in l],'overfull_lines':[l for l in log.splitlines() if 'Overfull' in l],'diplomatic_width_lines':[l for l in log.splitlines() if 'DIPLOMATICWIDTH' in l]})
  if ok and label=='A':shutil.copy2(pdf,ROOT/'pdf'/pdf.name)
  # Keep complete logs, not incidental font caches or auxiliary outputs.
  logs=ROOT/'receipts/build_logs'/tex.stem/label;logs.mkdir(parents=True,exist_ok=True)
  for pp in out.glob('*'):
   if pp.suffix in ['.log','.txt']:shutil.copy2(pp,logs/pp.name)
 rec={'document':tex.name,'runs':runs,'two_clean_builds_pass':all(x['success'] for x in runs),'byte_identical':all(x['success'] for x in runs) and runs[0]['pdf_sha256']==runs[1]['pdf_sha256']}
 builds.append(rec)
js('receipts/build_receipt.json',{'engine':'XeLaTeX','shell_escape':False,'clean_builds_per_document':2,'passes_per_build':2,'source_date_epoch':1790467200,'documents':builds,'visual_inspection_is_separate':True})
# Render the checked block and continuation at readable resolution; rendering is
# not recorded as inspection.
for name in [p.stem for p in texfiles[1:]]:
 pdf=ROOT/'pdf'/f'{name}.pdf'
 if not pdf.exists():continue
 with fitz.open(pdf) as f:
  target=ROOT/'qa/render'/name;target.mkdir(exist_ok=True,parents=True)
  for i in range(len(f)):f[i].get_pixmap(dpi=130).save(target/f'page_{i+1:03}.png')
# Unchanged historical first40 page records are checked byte-for-byte.
old=ROOT/'history/S02_PRINT001_040_CHECKPOINT/transcription/pages';inherited=[]
for n in range(90,130):
 p=Path(f'AB01-PDF{n:04}.json');inherited.append({'page':n,'equal':(old/p).read_bytes()==(ROOT/'transcription/pages'/p).read_bytes(),'sha256':H(ROOT/'transcription/pages'/p)})
assert all(x['equal'] for x in inherited)
js('receipts/inherited_pages_unchanged.json',{'count':40,'all_byte_identical':True,'records':inherited})
# User-request semantic regression checks on the checked single-file TeX.
checked=(ROOT/'tex/S02_P041_043_checked.tex').read_text()
newsource='\n'.join(l['tex'] for q in pages if 130<=q['master_pdf_page']<=132 for s in q['sections'] for l in s['lines'])
checks={
 'all_nine_flags_accepted':len([r for r in rows if r['id'].startswith('U')])==9,
 '285_not_287':'287' not in newsource and '285 annis colligi' in newsource,
 'fraction_chain_complete':r'\dfrac{1+1/5}{360}=\dfrac{6/5}{360}=\dfrac{6}{1800}=\dfrac{1}{300}' in newsource,
 'Pachon_macron':'Pachōn' in newsource,
 'efficiunt_not_efficiant':'efficiant' not in newsource and 'efficiunt' in newsource,
 'dies_not_degree':r'365^d14\'26' in newsource if False else ("365^d14'26''" in newsource and "365^d14'48''" in newsource),
 'U07_orders':r'30^{\mathrm{IV}}$ et $42^{\mathrm{VI}}' in newsource,
 '164_verso':'fol. 164,v.--166,v.' in newsource,
 'second_dash':'superantis, --- ad 285 annos' in newsource,
 'source_parentheses_omissions':('p. 916.\n' in newsource and 'p. 184--185.\n' in newsource),
 'quote_continuation_signs':sum(l['tex'].startswith('«') for q in pages if q['master_pdf_page']==132 for s in q['sections'] for l in s['lines'])==2,
 'all_five_reviewed_margin_locators':len([m for m in margins if m['master_pdf_page']<=132])==5,
 'no_lowercase_order_signs':not any('\\mathrm{'+s+'}' in newsource for s in ['iv','v','vi']),
 'source_excerpts_pixel_match':all(identical),
 'inherited40_byte_identical':all(x['equal'] for x in inherited),
 'source_page_range_contiguous':[q['master_pdf_page'] for q in pages]==list(range(90,last+1)),
 'no_new_translation':True,
 'two_clean_builds_each':all(b['two_clean_builds_pass'] for b in builds),
 'byte_identical_each':all(b['byte_identical'] for b in builds),
 'no_missing_characters':all(not r['missing_character_lines'] for b in builds for r in b['runs'])}
js('receipts/technical_audit.json',{'auditor':'Producing assistant-run read-only technical checks; not an independent human or philological reviewer','checks':checks,'passed':sum(checks.values()),'total':len(checks),'status':'PASS' if all(checks.values()) else 'FAIL','candidate_patched_by_auditor':False,'full_visual_reading_audit':False})
state={'schema_version':2,'session':'S02','version':'v009','status':'USER_CORRECTIONS_INTEGRATED_CONTINUATION_CANDIDATE','assigned_master_pages':[90,198],'assigned_printed_pages':[1,109],'cumulative_candidate_master_pages':[90,last],'cumulative_candidate_printed_pages':[1,last-89],'candidate_pages':last-89,'remaining_pages':198-last,'last_saved_transcription_candidate':f'AB01-PDF{last:04}','last_fully_transcribed_source_unit':f'AB01-PDF{last:04}','transcription_boundary_definition':'Saved editable candidate coverage; not an assertion of exhaustive source or final render verification.','first_untouched_source_unit':f'AB01-PDF{last+1:04}','last_fully_verified_source_unit':None,'verified_ranges':[{'master_pages':[130,132],'printed_pages':[41,43],'scope':'Readings and specified typography','responsibility':'User scan-check; assistant integration'}],'line_form_integrated_ranges':[[130,last]],'new_line_anchors':len(line_rows),'new_math_spans':len(formula),'new_margin_locators':len(margins),'resolved_U01_U09':True,'source_review_vs_current_output':'User verified41–43. Later lines are candidates reconstructed from prior source-linked work. Current rendered output is generated but final visual inspection is not asserted.','all_builds_pass':all(b['two_clean_builds_pass'] for b in builds),'all_builds_byte_identical':all(b['byte_identical'] for b in builds),'S01_modified':False,'S03_started':False,'canonical_arabic_modified':False,'new_target_language_translations':[],'human_review_required_to_continue':False,'next_action':f'Continue at master PDF{last+1}, printed p.{last-88}; check the current candidate against source/render without reopening the nine resolved user readings.'}
js('receipts/cumulative_checkpoint.json',state)
readme=f'''# S02 v009 — accepted scan corrections and cumulative continuation

## What this successor changes
The user’s scan-checked readings for printed pages41–43 (physical PDF130–132)
are accepted. All nine U-flags are closed. The additional macrons, punctuation,
time units, small-capital sexagesimal order signs, italics, spaced names and164-verso
locator are incorporated. The five outstanding margin locators, printed line
numbers and repeated line-initial quotation signs are encoded in the line form.
The source seam43/44 is preserved exactly; no word is supplied or dropped.

The named checked TeX file was not found. This successor implements the complete
correction message; it does not claim to have imported that separately named file.

## Contents
- `tex/S02_P041_043_checked.tex`: self-contained checked block; inputs no page files.
- `pdf/S02_P041_043_checked.pdf`: built only when the recorded build succeeded.
- `tex/S02_NALLINO_SOURCE_v009.tex`: cumulative historical reader, pp.1–{last-89}.
- `tex/S02_P044_{last-89:03}_source_replayed.tex`: separate continuation candidate.
- `transcription/pages`: contiguous page records1–{last-89}; first40 byte-unchanged.
- `ledgers/accepted_user_corrections.tsv`: every accepted reading/style/line-form edit.
- `ledgers/page_disposition.tsv`: all109 assigned pages; untouched pages are explicit.
- `source`: original-image evidence and documented native-pixel crops.
- `receipts`: actual build logs, source-excerpt pixel checks and exact checkpoint.

## Status and responsibility
This is not completion of S02. User scan verification is credited as such;
restored line-anchored continuation pages are candidates, not newly certified
philological readings. A successful technical build is not a visual reading audit.
The current export does not assert that the newly generated render has received
final visual inspection. One damaged glyph at PDF140l1 is preserved as an image;
the hidden part is not guessed. Printed mathematical/reference discrepancies stay
in the text and are documented separately.

No Arabic canonical change, new target-language translation, S01 modification,
or S03 production is included. Human certification is not required to continue.

## Rebuild
Install XeLaTeX with the fonts named in the TeX preamble (font binaries are not
included). From `tex/`, run XeLaTeX twice on the named document. Relative paths to
`source/presentation` and the restored historical table dependencies are retained.
`python scripts/build_edition.py` regenerates the TeX from page records and the
unchanged historical first40 TeX held under `history/`.
`new_pages.py` is the construction record; do not rerun it as a review operation:
it precedes the responsibility/status updates recorded by `finalize.py`.

Continue at physical PDF{last+1} / printed page{last-88}. See
`receipts/cumulative_checkpoint.json` for granular verification, not merely a
single inherited last-verified value.
'''
(ROOT/'README.md').write_text(readme)
# Core acceptance must pass before any export. Builds may fail but are explicitly
# represented, with no success label on an unsuccessful document.
assert all(v for k,v in checks.items() if k not in ['two_clean_builds_each','byte_identical_each','no_missing_characters']), checks
# History keeps editable prior sources and receipts; avoid redundant scan copies.
for hist in (ROOT/'history').iterdir():
 for child in ['source','tables']:
  p=hist/child
  if p.exists():shutil.rmtree(p)
# Historical master PDF remains outside the deliverable; the bounded excerpt is in.
for p in [ROOT/'qa/build_test',ROOT/'qa/clean_build_A',ROOT/'qa/clean_build_B']:
 if p.exists():shutil.rmtree(p)
# Deterministic self-excluding manifest and archive.
for p in ROOT.rglob('*'):
 if p.is_file() and p.suffix.lower() in {'.ttf','.otf','.ttc','.woff','.woff2','.pfb','.pfa','.dfont'}:raise RuntimeError('Font binary unexpectedly in export: '+str(p))
manifest=ROOT/'MANIFEST_SHA256.tsv';files=sorted(p for p in ROOT.rglob('*') if p.is_file() and p!=manifest and '__pycache__' not in p.parts)
manifest.write_text('sha256\tbytes\tpath\n'+''.join(f'{H(p)}\t{p.stat().st_size}\t{p.relative_to(ROOT).as_posix()}\n' for p in files))
archive=BASE/'AB01_S02_v009.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files+[manifest]:
  info=zipfile.ZipInfo(ROOT.name+'/'+p.relative_to(ROOT).as_posix(),date_time=(2026,9,26,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,p.read_bytes())
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for p in files:assert hashlib.sha256(z.read(ROOT.name+'/'+p.relative_to(ROOT).as_posix())).hexdigest()==H(p)
validation={'archive':archive.name,'sha256':H(archive),'bytes':archive.stat().st_size,'manifest_files':len(files),'zip_integrity':'PASS','all_manifest_members_match':True,'session_complete':False,'all_builds_pass':state['all_builds_pass']}
(BASE/'AB01_S02_v009_ZIP_VALIDATION.json').write_text(json.dumps(validation,indent=2)+'\n')
print(json.dumps({'zip':validation,'checkpoint':state,'audit':checks},ensure_ascii=False,indent=2))

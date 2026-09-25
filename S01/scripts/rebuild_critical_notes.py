"""Build a separate English critical apparatus, never a parallel translation."""
from pathlib import Path
import hashlib,json,os,re,shutil,subprocess,tempfile
import fitz
R=Path(__file__).resolve().parents[1];name='S01_CRITICAL_NOTES_v002'
notes=json.loads((R/'ledgers/critical_findings.json').read_text())
ESC={'\\':r'\textbackslash{}','{':r'\{','}':r'\}','%':r'\%','&':r'\&','#':r'\#','_':r'\_','$':r'\$','^':r'\textasciicircum{}','~':r'\textasciitilde{}'}
def esc(s):return ''.join(ESC.get(c,c) for c in str(s))
def text(s):
    # Script runs are quotations in an English apparatus, not a translated reader.
    out=[];pos=0
    for m in re.finditer(r'[\u0600-\u06ff\u0750-\u077f\u08a0-\u08ff]+|[\u0700-\u074f]+|[\u0370-\u03ff\u1f00-\u1fff]+',str(s)):
        out.append(esc(str(s)[pos:m.start()]));v=m.group()
        if '\u0700'<=v[0]<='\u074f':out.append(r'\RL{{\syriacfont '+esc(v)+'}}')
        elif ('\u0370'<=v[0]<='\u03ff') or ('\u1f00'<=v[0]<='\u1fff'):out.append(r'\textgreek{'+esc(v)+'}')
        else:out.append(r'\textarabic{'+esc(v)+'}')
        pos=m.end()
    out.append(esc(str(s)[pos:]));return ''.join(out)
out=[r'''\documentclass[11pt]{article}
\usepackage[a4paper,margin=23mm,headheight=14pt]{geometry}
\usepackage{fontspec,graphicx}
\usepackage{polyglossia}
\setmainlanguage{english}
\setotherlanguages{arabic,greek}
\setmainfont{Linux Libertine O}
\newfontfamily\arabicfont{Amiri}[Script=Arabic]
\newfontfamily\greekfont{FreeSerif}[Script=Greek]
\newfontfamily\syriacfont{Noto Sans Syriac}[Script=Syriac]
\usepackage{fancyhdr}
\usepackage[unicode,hidelinks]{hyperref}
\hypersetup{pdftitle={S01 v002 - Critical notes and source limitations},pdfauthor={Digital editorial apparatus; AI-assisted production}}
\graphicspath{{../source/presentation/}}
\pagestyle{fancy}\fancyhf{}\fancyhead[L]{S01 v002 — Critical notes}\fancyhead[R]{Modern editorial apparatus}\fancyfoot[C]{\thepage}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\emergencystretch=2em
\begin{document}
\begin{center}{\Large Critical notes and source limitations}\par
{\large Nallino, Part I: front matter and apparatus}\par
S01 v002 — 25 September 2026\end{center}
These notes belong to the new digital production, not to Nallino's historical prose. The historical reader is a separate artifact. No parallel translation is supplied here.

The complete S01 range has received first-pass transcription or an explicit image/blank disposition. Eleven reading entries remain open. One additional entry documents truncation already present in the frontispiece source. Four inline source-image glyphs avoid asserting unsupported Unicode readings. These qualifications remain attached to the candidate.

Source identifiers are physical pages of the pinned Nallino master, SRC01. Source-line identifiers and exact evidence paths are in the machine-readable ledgers. The reader begins with one modern notice; its page numbering is not the original Roman foliation. Nallino's printed addenda are transcribed and routed, not silently inserted into earlier text.
''']
for x in notes:
    n=int(x['source_anchor'].split('PDF')[1]);reader=2 if n==2 else n-9
    out += [r'\par\noindent\begin{minipage}{\linewidth}',r'\subsection*{'+esc(x['apparatus_id']+' — '+x['source_anchor'])+'}',
            r'\textit{'+esc(x['issue_class'].replace('_',' ')+'; '+x['status'].replace('_',' ').lower()+f'; reader p. {reader}')+'}',
            r'\textbf{Reading retained.} '+text(x['diplomatic_reading'])+'.',
            text(x['reason']),
            r'\textbf{Bounded alternatives.} '+text(x['bounded_alternatives']),
            r'\textbf{Source location.} '+r'{\small\texttt{'+esc(x['line_id'])+'}}. '+esc('Rectangle '+'['+', '.join(f'{v:.2f}' for v in x['source_rect_pt'])+']'+' PDF points (display rounded); '+x['coordinate_granularity'].replace('whole source page; exact page anchor, not a fabricated line box','whole-page region; line-specific coordinates not verified')+'.'),
            r'\textbf{Disposition.} '+text(x['confidence'])+'. No critical emendation is adopted. The Arabic authorial canon is unchanged.']
    if n==22:out.append(r'\par\includegraphics[height=8mm]{AB01-PDF0022-G01.png}')
    elif n==70 and 'orthographic sign' in x['diplomatic_reading']:out.append(r'\par\includegraphics[height=8mm]{AB01-PDF0070-G01.png}')
    elif n==82:out.append(r'\par\includegraphics[height=8mm]{AB01-PDF0082-G01.png}\qquad\includegraphics[height=8mm]{AB01-PDF0082-G02.png}')
    out.append(r'\end{minipage}\par\smallskip')
out += [r'''\section*{Repairs, historical corrections and verification}
The 28 recorded proof-repair or encoding decisions affect 25 distinct source lines relative to the preserved first-pass snapshot. They correct the digital transcription, not Nallino's historical claims. Every changed line has a repair identifier and a before/after record. Transient image fallbacks later resolved remain in the history.

The 86 printed addenda/corrigenda entries have the status \texttt{REGISTERED\_NOT\_APPLIED}. References into later sessions are routing records only. No later-session text has been transcribed or changed here.

Two clean two-pass builds of the historical reader are byte-identical. A separate read-only executable checks source identity, coverage, assets and builds. It was authored in the production session and is not an independent philologist. The producing assistant inspected source and reader proofs; an independent cold source/reading audit has not been performed. No human-only certification requirement is introduced. S01 remains a candidate, not a closed session.

The line-alignment ledger distinguishes page/section anchors from rectangles estimated using embedded-text similarity. Such rectangles are locator candidates, not certified measurements of every historical line. Native image-crop coordinates and pixel-equality tests are recorded separately.

\section*{Source citation}
Nallino, C. A. (1903). [Front matter, preface, bibliography, and addenda]. In \textit{Al-Battānī sive Albatenii opus astronomicum} (Pars prima: \textit{Versio capitum cum animadversionibus}, pp. VII–LXXX). Ulrich Hoepli. Controlling digital witness: SRC01, physical PDF2, PDF10 and PDF12–89.

{\small\raggedright Source SHA-256:\par\texttt{544c16b6355c9b74e281aded657d6572}\par\texttt{24bff738366d5260e1a610d31b0d6297}\par}
\end{document}''']
(R/'tex'/f'{name}.tex').write_text('\n'.join(out)+'\n')
env=dict(os.environ,SOURCE_DATE_EPOCH='1790294400',FORCE_SOURCE_DATE='1',TZ='UTC');receipts=[]
for label in ['A','B']:
    with tempfile.TemporaryDirectory(prefix='.notes_build_'+label+'_',dir=R) as td:
        wd=Path(td);shutil.copyfile(R/'tex'/f'{name}.tex',wd/f'{name}.tex')
        for run in [1,2]:
            cp=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',f'{name}.tex'],cwd=wd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=True)
            (R/'receipts'/f'critical_build_{label}_pass{run}.txt').write_bytes(cp.stdout)
        data=(wd/f'{name}.pdf').read_bytes();log=(wd/f'{name}.log').read_text()
        (R/'receipts'/f'critical_build_{label}.log').write_text(log)
        d=fitz.open(stream=data,filetype='pdf')
        receipts.append({'build':label,'clean_directory':True,'passes':2,'pages':len(d),'bytes':len(data),'pdf_sha256':hashlib.sha256(data).hexdigest(),'missing_characters':log.count('Missing character'),'overfull_boxes':log.count('Overfull'),'font_warnings':log.count('Font Warning')})
        if label=='B':(R/'pdf'/f'{name}.pdf').write_bytes(data)
result={'artifact':f'pdf/{name}.pdf','role':'MODERN_EDITORIAL','language':'English critical apparatus with cited source readings; not a target-language translation','builds':receipts,'byte_identical':receipts[0]['pdf_sha256']==receipts[1]['pdf_sha256'],'source_date_epoch':1790294400}
(R/'receipts/critical_notes_builds.json').write_text(json.dumps(result,indent=2)+'\n')
assert result['byte_identical'] and not any(x[k] for x in receipts for k in ['missing_characters','overfull_boxes','font_warnings']),result
print('Critical apparatus:',receipts[1]['pages'],'pages, byte-identical clean builds.')

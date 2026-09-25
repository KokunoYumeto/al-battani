from pathlib import Path
import json,re,collections
root=Path('/mnt/data/AB01_S01_v002')
counts=collections.Counter(); errs=[]; weird=[]; text=''
for p in sorted((root/'transcription/pages').glob('*.json')):
 d=json.loads(p.read_text());
 for s in d['sections']:
  st=[]
  for l in s['lines']:
   v=l['text']; text+=v+'\n'
   for m in re.finditer(r'</?(i|n|ar|gr|sy|small|sup|m|glyph|b)>',v):
    t=m.group(1); counts[t]+=1
    if m.group().startswith('</'):
     if not st or st[-1]!=t: errs.append((l['id'],'close',t,st.copy()))
     else: st.pop()
    else: st.append(t)
   for c in v:
    if ord(c)<32: errs.append((l['id'],'control',repr(c)))
   # known-looking malformed tags
   for x in re.findall(r'<[^>\n]*(?:>|$)',v):
    if not re.fullmatch(r'</?(i|n|ar|gr|sy|small|sup|m|glyph|b)>',x): weird.append((l['id'],x))
  if st: errs.append((p.name,s['role'],'remaining',st))
print('pages',len(list((root/'transcription/pages').glob('*.json'))),'words',len(re.sub(r'<[^>]*>','',text).split()))
print('errors',errs)
print('otherangle',weird)
print('tags',counts)

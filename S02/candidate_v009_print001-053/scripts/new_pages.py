from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
def section(raw,role,p):
 lines=[]
 for s in raw.strip().splitlines():
  if not s.strip():continue
  n,t=s.split('|',1);m=re.match(r'\[(N\d+|P\d+|H\d+)\]',t);extra=m.group(1) if m else None
  if m:t=t[m.end():]
  lines.append({'id':f'AB01-PDF{p:04}-{role}-L{len(lines)+1:03}','source_line_no':int(n) if n else None,'tex':t.rstrip(),'semantic_anchor':f'AB01-PDF{p:04}-{extra}' if extra else None,'source_role':'NALLINO_TRANSLATION' if role=='body' else 'NALLINO_APPARATUS'})
 return {'role':role,'authorship':'NALLINO_TRANSLATION' if role=='body' else 'NALLINO_APPARATUS','lines':lines}
def page(p,body,left,right,margins=None,figures=None,review='ASSISTANT_SOURCE_REPLAYED_FIRST_PASS',signature=None):
 q={'anchor':f'AB01-PDF{p:04}','master_pdf_page':p,'printed_page':p-89,'source':'SRC01','status':review,'sections':[section(body,'body',p),section(left,'notes_left',p),section(right,'notes_right',p)],'margin_locators':margins or [],'figures':figures or [],'signature':signature,'source_authority':'Controlling master page image. Embedded text is not the authority for a reading.','transcription_convention':'Source line breaks, hyphenation, repeated quotation signs, word-level type distinctions and mathematical units retained. Stable L numbers count text-bearing lines; source_line_no follows visible numbering, including implied blanks/headings.'}
 for loc in q['margin_locators']:
  loc['line_anchor']=next(l['id'] for l in q['sections'][0]['lines'] if l['source_line_no']==loc['line'])
 (ROOT/f'transcription/pages/AB01-PDF{p:04}.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
 return q

page(130,r"""
1|[P01]diei quae 365 diebus addebatur. Qua re de motu Solis non dubitavit, ita ut Solem aliam
2|sphaeram habere cuius centrum a centris duarum sphaerarum differret, supponeret ({\itshape b}).
3|[P02]\Indent Veteres plerumque haec ex observationibus aestivis, quae fiunt cum Sol per punctum
4|solstitiale aestivum transit, deprehenderunt; sed non ita verae videntur ut observationes factae
5|cum Sol per alterutrum punctum aequinoctiale transit, et praesertim per punctum aequinoctii
6|autumni; hoc enim tempore aer clarior et purior est quam tempore aequinoctii vernalis. Et
7|quia Solis motus in declinatione, quando per punctum solstitiale transit, tardus est, at quando
8|per puncta aequinoctialia iter facit, velocissimus, Ptolemaeus nonnisi observationibus autumnis
9|confisus est, et iuxta eas calculos instituit. Una ex observationibus Hipparchi qua usus est et
10|de cuius veritate non dubitavit, ea est, qua, ut narrat (1), Solem per punctum aequinoctii
11|autumni transiisse comperit anno 178 ab Alexandro mortuo, die tertia ex quinque diebus epa-
12|gomenis, hora mediae noctis cuius crastinum fuit quarta epagomenorum dies, Alexandria in
13|urbe (2). Post hoc Ptolemaeus, 285 annis Aegyptiis transactis, iterum observavit, quam obser-
14|vationem ipse in libro suo accuratissimam fuisse dicit; et Solis transitum per punctum aequi-
15|noctii autumni comperit anno tertio Antonini regis, id est anno 463 (3) ab Alexandro mor-
16|tuo, die nona mensis Coptici Athyr, una hora circiter post Solis ortum, Alexandria in urbe.
17|Intervallum inter duas observationes illas invenit esse veraciter 285 annorum Aegyptiorum,
18|70 dierum, et $\qfrac{1}{4}+\qfrac{1}{20}$ [$=\qfrac{3}{10}$] diei, pro 71 diebus $\qfrac{1}{4}$, qui ex quartis partibus integris in iis
19|285 annis colligi debebant. Ratio igitur huius unius diei minus $\qfrac{1}{20}$ diei, --- quo tempus ob-
20|servationis praecessit tempus quartae partis diei 365 dies superantis, --- ad 285 annos inter
21|duas illas observationes transactos, est ut ratio unius diei ad 300 annos; qua re tempus unius
22|anni per has duas observationes inventum, complectitur 365 dies $\qfrac{1}{4}$, detracto $\qfrac{1}{300}$ diei, quod
23|est una pars et quinta e 360 partibus (4).
24|[P03]\Indent Narrat etiam Ptolemaeus, se observationes antiquas aestivas, quae factae sint ante Hip-
25|parchum, accepisse, e quibus observationem esse tempore Apseudis, regis [\textgreek{ἄρχων}] Athenarum,
26|factam, cum Sol per punctum solstitiale aestivum transivisset anno 108 (5) ante Alexandrum
27|mortuum, matutino XXI diei mensis Coptici Pharmouthi (6); deinde seipsum Solis transitum per
28|punctum solstitii aestivi observasse anno 463 (7) post Alexandrum mortuum, XI die mensis
29|Coptici Mesori, duabus horis circiter post mediam noctem cuius crastinum dies XII fuit (8).
30|Inter has duas observationes intercesserunt fere 571 anni Aegyptii, 140 dies et $\qfrac{1}{2}+\qfrac{1}{3}$
31|[$=\qfrac{5}{6}$] diei, pro 142 diebus $\qfrac{1}{2}+\qfrac{1}{4}$ [$=\qfrac{3}{4}$], qui ex quartis partibus in iis annis collecti
32|essent si in annis quartae partes integrae fuissent. Invenit igitur tempus solstitii aestivi tempus
33|quartae integrae partis diei uno die et $\qfrac{2}{3}+\qfrac{1}{4}$ [$=\qfrac{11}{12}$] praecessisse, quorum ratio ad 571
34|annos memoratos est ut ratio duorum integrorum dierum ad 600 (9) annos; idque cum eo
35|iuxta quod calculos fecit convenit, scilicet singulis 300 annis tempus observationis tempus
36|quartae partis integrae diei uno die praecedere, licet ob causam memoratam hae observationes
37|aestivae non adeo sint bonae ut autumnae. Manifestum est inter primam illam observationem
""",r"""
|[N01]\Indent (1) {\itshape Almag.} III, 2 (ed. Halma, t. I, p. 161).
|[N02]\Indent (2) Al-Battānī coniectura; minime Ptolemaeus
|dicit Hipparchum id Alexandriae observasse. Et re
|vera nunc certum habetur Hipparchum Rhodi tan-
|tum observationes suas perfecisse, quam perperam
|sub eodem meridiano quo Alexandria iacere putabat.
|[N03]\Indent (3) Codex perperam 563.
|[N04]\Indent (4) $\dfrac{1+1/5}{360}=\dfrac{6/5}{360}=\dfrac{6}{1800}=\dfrac{1}{300}$.
""",r"""
|[N05]\Indent (5) Codex perperam 168.
|[N06]\Indent (6) Est observatio Metonis et Euctemonis (27
|Iun. 432 ante Chr. n.); {\itshape Almag.} III, 2 (ed. Halma,
|t. I, p. 162).
|[N07]\Indent (7) Male Plato 36.
|[N08]\Indent (8) {\itshape Almag.} l. l.
|[N09]\Indent (9) Plato perperam 60.
""",margins=[{'line':6,'text':'p. 62.','side':'right'},{'line':30,'text':'p. 63.','side':'right'}],review='USER_SCAN_REVIEW_ACCEPTED_AND_ASSISTANT_SOURCE_REPLAYED',signature='6')

page(131,r"""
1|[P01]et observationem Hipparchi idem fere tempus intercessisse quod inter Hipparchi et Ptolemaei;
2|fuit enim observatio 286 (1) annis ante Hipparchum.
3|[P02]\Indent Nos ipsi in urbe ar-Raqqah observavimus; et una nostrarum observationum autumna-
4|rum, qua confidimus et de cuius veritate, ut ex instrumentis apparuit, haud dubitamus, est
5|observatio quae 743 annis fuit post observationem autumnam Ptolemaei iam memoratam. Ea
6|invenimus Solem per punctum aequinoctii autumni transivisse, anno 1194 aerae Dhū ’l-qar-
7|nayn, idest 1206 post Alexandrum mortuum, ante Solis ortum diei XIX mensis Romani Aylūl (2),
8|scilicet VIII diei mensis Coptici Pachōn, quatuor circiter horis et $\qfrac{1}{2}+\qfrac{1}{4}$ ({\itshape c}). Et quia circulus
9|meridianus Alexandriae circulum meridianum urbis ar-Raqqah $\qfrac{2}{3}$ horae aequinoctialis circiter
10|praecedit (3), inter observationem nostram et observationem autumnam Ptolemaei 743 anni
11|Aegyptii, 178 dies, et $\qfrac{1}{2}+\qfrac{1}{4}$ diei, detractis $\qfrac{2}{5}$ horae circiter (4), intercesserunt, loco 185
12|dierum $\qfrac{1}{2}+\qfrac{1}{4}$ qui debuissent in his annis colligi si quartae partes diei integrae fuissent. Si
13|hos 7 dies et $\qfrac{2}{5}$ horae, quibus tempus observationis tempus quartae partis diei 365 dies supe-
14|rantis praecessit, per 743 annos qui inter duas observationes illas fuerunt dividimus, invenimus
15|portionem unius anni esse $3^\circ24'$ ex iis $360^\circ$ qui revolutionem diei et noctis perficiunt. Quam
16|portionem si de tempore quartae partis diei, scilicet de $90^\circ$ detrahimus, quantitas augmenti
17|super 365 dies integros remanet $86^\circ36'$; est igitur verum anni tempus $365^d14'26''$ (5) fere.
18|[P03]\Indent Si $360^\circ$ circumferentiae caelestis sphaerae per tempus anni nuper inventum dividimus,
19|motum medium Solis in nychthemero reperimus $0^\circ59'8''20'''46^{\mathrm{IV}}56^{\mathrm{V}}14^{\mathrm{VI}}$ esse, motum au-
20|tem in 30 diebus, qui mensem Aegyptium efficiunt, $29^\circ34'10''23'''28^{\mathrm{IV}}6^{\mathrm{V}}47^{\mathrm{VI}}$, et in 365
21|diebus anni Aegyptii $359^\circ45'46''25'''32^{\mathrm{IV}}2^{\mathrm{V}}31^{\mathrm{VI}}$ (6) circiter ({\itshape d}). Hos motus multiplicavimus
22|et in tabulis ad annos collectos et singulos, et ad menses, dies, horas, iuxta aeram Arabum
23|aeramque Romanorum descripsimus (7), ut facile quocumque harum aerarum tempore locus
24|Solis, secundum eius motum medium qui {\itshape medium Solis} appellatur, inveniri possit. Tempus
25|anni a nobis inventum patet $2^\circ\qfrac{1}{5}$ minus esse quam tempus a Ptolemaeo memorato (8); qua
26|re motus Solis, iuxta calculum nostrum, motum a Ptolemaeo inventum in die $0^\circ0'0''3'''$
27|$33^{\mathrm{IV}}43^{\mathrm{V}}43^{\mathrm{VI}}$ (9) superat, et in anno Aegyptio, Deo volente, $0^\circ0'21''40'''10^{\mathrm{IV}}53^{\mathrm{V}}56^{\mathrm{VI}}$ fere (10).
""",r"""
|[N01]\Indent (1) Codex 280, Plato 186.
|[N02]\Indent (2) I. e. ante Solis ortum diei 19 Sept. 882;
|nam al-Battānī prima die mensis Septembris annos
|huius aerae incipere vult, cfr. cap. XXXII. --- Hunc
|locum laudat \Name{Ibn Yūnus} apud \Name{Caussin}, {\itshape Le li-}
|{\itshape vre de la grande table Hakémite} (Notices et ex-
|traits des mss. de la Bibl. Nation., t. VII, Paris 1804,
|p. 149).
|[N03]\Indent (3) In suis tabulis geographicis, e communi
|Arabica traditione depromptis, al-Battānī urbi ar-
|-Raqqah $73^\circ15'$ long. tribuit, Alexandriae, Ptole-
|maeum sequens, $60^\circ30'$. Hinc differentia longitudi-
|nalis $12^\circ45'$ sequeretur, non $10^\circ$.
|[N04]\Indent (4) I. e. 743 anni, $178^d\,17^h\,36^m$.
|[N05]\Indent (5) I. e. $365^d\,5^h\,46^m\,24^s$. --- \Name{Ptolemaeus}, {\itshape Al-}
|{\itshape mag.} III, 2 (Halma t. I, p. 165), seu potius Hippar-
""",r"""
|chus, invenerat $365^d14'48''=365^d\,5^h\,55^m\,12^s$; astro-
|nomi nostri temporis $365^d\,5^h\,48^m\,47^s{,}33$ ponunt.
|[N06]\Indent (6) Male quartae in cod. et Plat. $31^{\mathrm{IV}}$. Iam cor-
|rexit Ed. \Name{Halley}, {\itshape Emendationes ac notae in ve-}
|{\itshape tustas Albatênii observationes} (Philosophical Tran-
|sactions of the Royal Society, 1693, vol. XVII, nr. 204,
|p. 916.
|[N07]\Indent (7) Vide tabulas in fol. 164,v.--166,v., et 186,v.-
|-189,r.
|[N08]\Indent (8) Nam $8^m\,48^s\times15=528^s\times15=7920''=$
|$2^\circ12'=2^\circ\qfrac{1}{5}$.
|[N09]\Indent (9) Codex male $30^{\mathrm{IV}}$ et $42^{\mathrm{VI}}$; \Name{Ptolemaeus} III,
|2 (ed. Halma, t. I, p. 166) enim habet $0^\circ59'8''17'''$
|$13^{\mathrm{IV}}12^{\mathrm{V}}31^{\mathrm{VI}}$.
|[N10]\Indent (10) Male quintae apud Platonem $55^{\mathrm{V}}$ et in co-
|dice $50^{\mathrm{V}}$; \Name{Ptolemaeus} $359^\circ45'24''45'''21^{\mathrm{IV}}8^{\mathrm{V}}35^{\mathrm{VI}}$.
""",margins=[{'line':17,'text':'p. 64.','side':'left'}],review='USER_SCAN_REVIEW_ACCEPTED_AND_ASSISTANT_SOURCE_REPLAYED')

page(132,r"""
3|[H01]\CenterLine{CAPUT XXVIII.}
5|\CenterLine{De inaequalitate motus [sive anomalia] Solis et de eo quod}
6|\CenterLine{ab eius apogei loco cum illa apparet (1).}
8|[P01]\Indent Dicit [auctor]: Dissertatione de tempore anni et de motu medio Solis absoluta, ad expli-
9|candum pergamus quae et quanta sit inaequalitas in motu Solis, et qualis appareat [cum Sol
10|motu suo medio recesserit] a loco sui apogei in ecliptica.
11|[P02]\Indent Rationem qua Ptolemaeus in libro suo (2) usus est sequentes, nos quo modo Sol quadran-
12|tes eclipticae percurrat, per plurimas diligentissimas observationes multis subsequentibus annis
13|factas studuimus, invenimusque Solem eclipticam a puncto aequinoctii autumni ad aequinoctii
14|vernalis 178 diebus, 14 horis $\qfrac{1}{2}$ circiter percurrere; a puncto autem aequinoctii vernalis ad
15|aequinoctii autumni tempus eo longius occupare, quod ex nostris diligentissimis observationibus
16|patuit 186 dierum, 14 horarum aequinoctialium et $\qfrac{1}{4}+\qfrac{1}{2}$ horae circiter esse. Et ex iis
17|quae memoravimus (3) apparuit eius apogeum in hac dimidia parte haberi.
18|[P03]\Indent Deinde observavimus et invenimus Solem spatium ab initio Arietis ad initium Cancri,
19|idest inter punctum aequinoctii vernalis et punctum solstitii aestivi, 93 diebus et 14 fere horis
20|aequinoctialibus percurrere ({\itshape a}), quae parum ad deminutionem inclinant; unde manifestum est
21|cursui Solis a puncto aequinoctii vernalis ad solstitii aestivi tempus longius necessarium esse
22|quam a puncto solstitii aestivi ad aequinoctii autumni. Scimus igitur punctum apogei et cen-
23|trum excentrici, super quem punctum apogei simul ac super eclipticam incidit, ea quarta parte
24|contineri, quae tardioris temporis est quam reliquus quadrans. Motum medium Solis in iis
25|186 diebus, 14 horis et $\qfrac{1}{2}+\qfrac{1}{4}$ horae invenimus $183^\circ56'12''$ esse, et in iis 93 diebus et
26|14 horis $92^\circ14'10''$ fere (4).
27|[P04]\Indent Quae cum ita sint, circulum eclipticae ABCD circa centrum E describamus. Duae dia-
28|metri AC, BD se invicem ad angulos rectos abscindant, sitque A punctum aequinoctii vernalis;
29|erit B punctum solstitii aestivi, C aequinoctii autumni, D solstitii hiemalis. In quadrante AB,
30|ob ea quae supra diximus, punctum F centrum ponamus, et, intra primum circulum, circu-
31|lum KLMN sphaerae excentricae Solis describamus, cuius diametri KM, LN se invicem in
32|centro F ad angulos rectos abscindant. Punctum lineis BD, KM commune littera S signemus;
33|punctum quo diametrus AC circulum KLMN versus A secat, littera P; punctum quo diame-
34|trus BD circulum KLMN versus B abscindit, littera R. In arcu PK, perpendicularem a P ad
35|punctum Q diametri KM ducamus; item perpendicularem RG, et lineam EF quae per duo
36|centra transit, eamque usque ad punctum H eclipticae ABCD protrahamus, littera T signantes
37|locum quo ea circulum KLMN secat.
38|[P05]\Indent Manifestum est arcum AB esse $90^\circ$, ut arcum KL excentrici; punctum P excentrici esse
39|initium Arietis; R locum initii Cancri; denique arcum PKLRMY excentrici eam excentrici
""",r"""
|[N01]\Indent (1) I. e. de supputanda anomalia ad singulos
|gradus medii motus Solis ab apogeo.
|[N02]\Indent (2) {\itshape Almag.} III, 4 (ed. Halma t. I, p. 184--185.
|[N03]\Indent (3) Sed antea, ut me \Name{Schiaparelli} monet,
|nihil de his rebus dixit. Forte aliquid excidit ubi
|demonstrabatur apogeum reperiendum esse in parte
|cui maius temporis intervallum respondet.
""",r"""
|[N04]\Indent (4) Ita etiam in calculis infra, qua re corri-
|gere non audeo; e tabulis $92^\circ14'26''$ deducuntur.
|Sed antea dixerat « 93 diebus et 14 horis aequino-
|« ctialibus, {\itshape quae parum ad deminutionem incli-}
|« {\itshape nant} »; forte huic « parum minus » respondent
|hae 16 secundae, quae in auctoris calculo deficere
|videntur.
""",margins=[{'line':15,'text':'p. 65.','side':'right'},{'line':39,'text':'p. 66.','side':'right'}],review='USER_SCAN_REVIEW_ACCEPTED_AND_ASSISTANT_SOURCE_REPLAYED')

page(133,r"""
1|[P01]partem quam Sol medio suo itinere ab initio Arietis ad initium Librae percurrit, scilicet, ut
2|supra vidimus, $183^\circ56'12''$. Arcus KLRM, semicircumferentia excentrici, $180^\circ$ continet; quis-
3|que igitur arcuum PK, YM est dimidia pars eorum $3^\circ56'12''$, quibus Sol medio suo itinere
4|$180^\circ$ superat, idest $1^\circ58'6''$. --- Manifestum etiam est arcum PKLR (1) excentrici id esse quod
5|Sol, medio suo itinere, ab initio Arietis ad initium Cancri percurrit; igitur $92^\circ14'10''$ erit;
6|et quia arcus PKL, ob ea quae nuper diximus, $91^\circ58'6''$ complectitur, arcus LR $0^\circ16'4''$
7|continebit. Item manifestum est perpendicularem PQ sinum esse arcus PK, et perpendicula-
8|rem RG sinum arcus LR; igitur PQ fere $2^p3'39''$, et RG fere $0^p16'45''$ erit. Quoniam
9|linea KM parallela est lineae AC, erit linea ES aequalis PQ; et similiter, quia LN parallela
10|est lineae BD, erit FS aequalis RG. Est itaque etiam latus EF trianguli rectanguli ESF no-
11|tum; quadratum lateris ES est fere $4^p14'48''$, quadratum lateris FS fere $0^p4'41''$, summa
12|igitur $4^p19'29''$ (2) efficit quadratum lateris EF, cuius radix $2^p4'\,\qfrac{3}{4}$ est quantitas lineae EF
13|ambo centra coniungentis. Ea ratione autem, qua quadrans circuli triangulum rectangulum
14|ESF circumdantis $90^\circ$ complectitur, et semidiametrus $60^p$, erit arcus EF circiter $1^\circ59'$ (3); et
15|haec est maxima anomalia motus Solis per has observationes manifesta ({\itshape b}).
16|[P02]\Indent Nunc in quantitatem arcus BH eclipticae inquiramus; qua cognita, etiam arcus HA reli-
17|quus notus erit. Punctum T est locus apogei in circulo Solis excentrico; nam, si lineam EF,
18|ambo centra coniungentem, usque ad eclipticam producimus, ipsa circulum KLMN in T, et
19|circulum eclipticae in H secat. Necesse est ut rationem lineae EF ad semidiametrum EH co-
20|gnoscamus, nec non quantitatem arcus BH eclipticae. Iam vidimus lineam EF $2^p4'\,\qfrac{3}{4}$ com-
21|plecti ea ratione qua semidiametrus $60^p$ continet; eadem ratione igitur linea EH, quae, ut EB,
22|semidiametrus est, lineam EF 28 vicibus et $\qfrac{5}{6}$ fere continebit. Quoniam linea FS, ut dixi-
23|mus, [$0^p16'45''$] est, si linea EF $60^p$ ponatur, erit iuxta hanc rationem linea FS circiter $8^p4'$;
24|hoc enim invenitur si $28\,\qfrac{5}{6}$ vicibus [$0^p16'45''$]
25|multiplicantur. --- Aut, si mavis, lineam FS in
26|semidiametrum EH multiplica; invenies $16^p45'$,
27|quae, per lineam EF scilicet per $2^p4'\,\qfrac{3}{4}$ divisa,
28|dabunt $8^p4'$, quod est [sinus] anguli BEH; ar-
29|cus igitur BH $7^\circ43'$ circiter continet. Itaque
30|manifestum est punctum T apogei in excentrico,
31|a puncto solstitii aestivi versus partem anterio-
32|rem signorum $7^\circ43'$ distare, scilicet $82^\circ17'$ ab
33|initio Arietis esse. Hoc invenire volebamus. Ob-
34|servatio iuxta quam hunc calculum fecimus,
35|anno 1194 aerae Dhū ’l-qarnayn (4) fuit, quo
36|iter Solis ab initio Arietis ad initium Cancri et
37|ad initium Librae observavimus ({\itshape c}).
38|[P03]\Indent Restat nunc nobis ut hanc anomaliam ad
39|gradus eclipticae distribuamus, et portiones eius quae ad singulos gradus pertinent in tabulis
""",r"""
|[N01]\Indent (1) Male codex PKL.
|[N02]\Indent (2) Male secundae apud Platonem $59''$.
|[N03]\Indent (3) Plato male $1^\circ58'$; \Name{Ibn Yūnus} (apud \Name{Caus-}
|\Name{sin}, {\itshape Le livre de la grande table Hakémite}, in
|Notices et extraits des mss. de la Bibl. Nation., t. VII,
|Paris 1804, p. 155) scribit: « al-Battānī aequationem
|« totam Solis calculavit, invenitque $1^\circ59'10''$ esse ».
""",r"""
|\Name{Halley} p. 917, et \Name{Delambre}, {\itshape Astr. moyen âge},
|p. 36, qui hodiernis tabulis trigonometricis usi sunt,
|invenere quoque $1^\circ59'10''$. Codicis lectio igitur bona
|est; in tabulis aequationis Solis (fol. 191,r.) re vera
|maxima aequatio est $1^\circ59'10''$.
|[N04]\Indent (4) Incipit, iuxta usum auctoris nostri, die 1 Se-
|ptembris 882 post Chr. n.
""",margins=[{'line':17,'text':'p. 67.','side':'left'}],figures=[{'id':'AB01-PDF0133-F01','start_line':24,'end_line':38,'side':'left','image_width_fraction':.46,'text_width_fraction':.50}])

page(134,r"""
1|[P01]describamus, ut facile possit aequatio motus Solis inveniri. Ostendit Ptolemaeus (1) motus va-
2|rios duobus modis effingi posse; quorum alter est ut ponatur planetam habere circulum eclip-
3|ticae concentricum, super quem alius circulus sit, cuius centrum circumferentiam primi per-
4|currat. Hic secundus circulus est circulus minor, Terram non ambiens, cuius centrum circulus
5|maior rotare facit versus partem successionis signorum iuxta quantitatem motus longitudinalis
6|planetae versus partem in quam signa succedunt. Sidus ipsum in epicyclo, qui est circulus
7|minor, versus praecedentem aut versus subsequentem partem movetur; aut circulus minor
8|planetam versus alterutram partem rotare facit. Hic est motus anomaliae quae ad planetam
9|pertinet. --- Alter explicandi modus est ut ponatur sidus habere circulum concentricum ecli-
10|pticae, et alterum excentricum sed illi aequalem, qui eum duobus locis secet Planeta est in
11|excentrico, sive hic eum movet, sive ipse in excentrico movetur. --- Utraque ratio anomaliam
12|pariter explicat; nos a prima incipiemus.
13|[P02]\Indent Circulum ABCD eclipticae circa centrum E describamus; sit A, initio, centrum epicycli
14|HF (2). Diametrum AC usque ad H producamus, quod est punctum apogei in epicyclo; sit F
15|locus Solis in epicyclo, et ab eo perpendicularem supra lineam AH usque ad punctum M du-
16|camus; denique lineam AF signemus, lineae AH aequalem, nam ambae sunt semidiametri
17|epicycli. Ob ea quae in hoc ipso capite iam diximus, patet eam $2^p4'\,\qfrac{3}{4}$ complecti, ut semi-
18|diametrum EF epicycli in figura praecedenti. Quo cognito, motum Solis in epicyclo versus
19|partem contrariam successioni signorum observa, vel quantitatem qua epicyclus motu medio
20|diurno Solem versus illam partem movet, iuxta rationem qua circumferentia epicycli in $360^\circ$
21|dividitur. Motus medius Solis, qui observationibus invenitur, est motus centri epicycli versus
22|partem successionis signorum; et hic motus quoque ea ratione ponitur qua circulus ABCD
23|$360^\circ$ complectitur.
24|[P03]\Indent Arcus HF, qui est arcus epicycli inter locum Solis et punctum apogei, $30^\circ$ contineat e
25|gradibus quorum epicyclus 360 continet. Lineam EF in hac figura ducamus; et in arcum
26|lineae FM, qui est variatio motus Solis eo loco, inquiramus. Linea EA, semidiametrus circuli
27|concentrici eclipticae, 60 partes habet ex iis quarum diametrus AC 120 continet; linea igitur
28|EH, quae centrum circuli parecliptici (3) cum apogeo epicycli coniungit, $62^p4'45''$ erit. Et
29|quia triangulum FMA est rectangulum, quadratum lineae AF erit ut summa quadratorum
30|AM, FM; angulus autem MAF (4) notus est, ergo etiam linea FM est nota, a qua deinde co-
""",r"""
|[N01]\Indent (1) {\itshape Almag.} III, 3, 4 et 5 (ed. Halma, t. I, p. 170-
|-183, 183--190, 190--199); quoad Solem tamen hypo-
|thesim excentrici commodiorem censet.
|[N02]\Indent (2) Cod. et Plato HFT; in eorum figura enim
|punctum T ponitur loco intersectionis epicycli et
|circuli magni, inter A et D. Sed ex iis quae sequun-
|tur patet T esse punctum circuli magni indicans di-
|rectionem apogei.
|[N03]\Indent (3) Scilicet paralleli seu concentrici eclipticae.
|Cum nullum habeat nomen apud scriptores nostra-
|tes, ita verto Arabicum {\itshape al-mumaththal bi falak}
|{\itshape al-burūǵ} « similem factum eclipticae » seu {\itshape al-mu-}
|{\itshape maththal} tantum, qui apud Ptolemaeum interdum
|\textgreek{ὁ ὁμόκεντρος τῷ κόσμῳ κύκλος} « circulus mundo con-
|« centricus » vel \textgreek{ὁ ὁμόκεντρος τῷ διὰ μέσων τῶν ζω-}
|\textgreek{δίων κύκλος} « circulus concentricus circulo per me-
""",r"""
|dium signorum transeunti » (i. e. eclipticae) vocatur.
|In astronomia Syriaca Barhebraei vertenda, \Name{Nau}
|eum {\itshape intersphère de la similitude} appellat; \Name{Golius},
|in versione al-Farghānī, et \Name{Sédillot}, in versione
|Ulugh Beg, {\itshape sphaeram} vel {\itshape circulum homocentri-}
|{\itshape cum}. --- Est circulus concentricus eclipticae in cuius
|plano iacet; descriptus est in superficie sphaerae
|Solis vel planetarum, {\itshape al-mumaththal} quoque vo-
|cata, quae est corpus solidum, concentricum eclip-
|ticae, duabus superficiebus parallelis contentum, qua-
|rum exterior superficiem exteriorem sphaerae circuli
|excentrici (deferentis) in puncto apogeo excentrici
|tangit; interior superficiem interiorem sphaerae ex-
|centrici in perigeo. --- Movetur ut signa zodiaci ob
|praecessionem moventur, ab ortu ad occasum.
|[N04]\Indent (4) Cod. HEF.
""",margins=[{'line':2,'text':'p. 68.','side':'right'},{'line':22,'text':'p. 69.','side':'right'}])

page(135,r"""
1|[P01]gnoscitur reliquum latus AM trianguli, quod est [cosinus] arcus FH et anguli FAH (1). Igi-
2|tur est etiam linea EM nota. Cum triangulum FME rectangulum sit, eius hypotenusa EF
3|cognoscitur, ex qua linea FM deprehenditur; arcus autem super FM est arcus anomaliae.
4|[P02]\Indent Si, ut posuimus, arcus FH $30^\circ$ complectitur, eius sinus erit 30 partium, e partibus qua-
5|rum semidiametrus AF 60 continet; sed ea ratione qua linea AF $2^p4'45''$ complectitur, erit
6|linea FM $1^p2'22''\,\qfrac{1}{2}$ (2), reliqua igitur AM $1^p48'2''$, et linea EM (3) $61^p48'2''$ (4); unde
7|patet [lineam EF] $61^p48'35''$ circiter esse ({\itshape d}). Sed ex partibus quarum linea EF 60 tantum
8|habet, linea FM $1^p0'33''$ (5) continebit, et arcus super eam positus $0^\circ57'49''$ circiter; et
9|haec est quantitas anomaliae motus Solis, scilicet arcus HF. Est igitur arcus TA eclipticae
10|$29^\circ2'11''$, qui antea $30^\circ$ erat; nam epicycli centrum a T ad A motum est ut Sol in epicyclo
11|a H ad F.
12|[P03]\Indent Nunc epicyclum GQP consideremus, cuius centrum est B; locum Solis G ponamus, sit-
13|que arcus QG (6), quem Sol a puncto Q apogei percurrit, $150^\circ$ (7); remanent igitur $30^\circ$ arcui
14|PG, qui a loco Solis ad punctum perigei porrigitur. Lineam EG et perpendicularem GK du-
15|camus; patet triangula BKG et GKE rectangula esse, et latera BG, BE haud ignota; nam
16|BG est semidiametrus epicycli (8), et BE semidiametrus circuli eclipticae. Angulus et arcus
17|GP dati sunt; perpendicularis GK et reliqua linea BK notae; [ergo etiam lineae KE et EG
18|cognoscuntur] (9). Cum arcus GP, ut posui-
19|mus, $30^\circ$ contineat, eius sinus quoque $30^p$
20|erit; arcus autem complementaris, qui su-
21|per KB est, sinum habebit $51^p57'41''$ (10).
22|--- At ex partibus quarum linea BG $2^p4'\,\qfrac{3}{4}$
23|habet, perpendicularis KG $1^p2'22''\,\qfrac{1}{2}$ (11)
24|continebit; remanet linea KB $1^p48'2''$, qua
25|re EK fere $58^p11'58''$, et EG fere $58^p12'$
26|$34''$ (12) continebit ({\itshape e}). Sed ex partibus qua-
27|rum EG 60 habet, cathetus KG $1^p4'17''$ (13)
28|complectetur, et arcus super eam positus
29|$1^\circ1'24''$ (14), iuxta rationem qua circulus
30|triangulum rectangulum BKG circumdans
31|in $360^\circ$ dividitur. Et hic est arcus anoma-
32|liae, scilicet arcus PG. Qua re arcus NB (15)
33|eclipticae, quem cognoscere volebamus, $31^\circ$
34|$1'24''$ (16) complectetur.
""",r"""
|[N01]\Indent (1) Cod.: « quod est quod angulo FAH et arcui
|« FH deest ad quadrantem perficiendum ».
|[N02]\Indent (2) Pro $22''$ Plato habet $55''$. Persaepe in Pla-
|tonis editione pro 2 legitur 5, qui error codicibus
|Latinis vel editoris incuriae tribuendus est.
|[N03]\Indent (3) Codex EF.
|[N04]\Indent (4) Plato verba seqq. omittit et pro $2''$ habet $35''$.
|[N05]\Indent (5) Plato $1^\circ33'$.
|[N06]\Indent (6) Cod. QM.
|[N07]\Indent (7) Male Plato 120.
|[N08]\Indent (8) Cod.: eclipticae.
|[N09]\Indent (9) Addidi, Platonem sequens; sed additio non
|est necessaria.
""",r"""
|[N10]\Indent (10) Partes apud Plat. $59^p$.
|[N11]\Indent (11) Deest $\qfrac{1}{2}$ in cod.; Plato pro $22''$ habet $55''$
|(cfr. adnot. 2).
|[N12]\Indent (12) Plato $58^p7'34''$.
|[N13]\Indent (13) Secundae apud Platonem $13''$.
|[N14]\Indent (14) Plato $1^p4'54''$.
|[N15]\Indent (15) Cod. IB (\textarabic{ى} I pro \textarabic{ن} N); Plato GB. In figura
|codicis et Platonis punctum N lineaque NT desunt;
|punctum T vero, ut supra notavi, perperam prope
|locum intersectionis epicycli HF et eclipticae collo-
|catum.
|[N16]\Indent (16) Minuta in cod. $4'$; Plat. $1^\circ4'54''$.
""",margins=[{'line':13,'text':'p. 70.','side':'left'}],figures=[{'id':'AB01-PDF0135-F01','start_line':18,'end_line':33,'side':'left','image_width_fraction':.49,'text_width_fraction':.465}])

page(136,r"""
1|[P01]\Indent Dicit [auctor]: Nunc aliter haec explicabimus. Circa centrum E et diametrum AC, sit
2|circulus eclipticae ABC; circa centrum H, excentricus FMG; et diametrus AC per ambo
3|centra transeat. Erit F punctum apogei in circulo parecliptico, G perigei. Initio locum Solis
4|in excentrico in M esse ponamus, et arcum FM excentrici, quem Sol iam percurrit, $30^\circ$ com-
5|plecti; angulus FHM erit quoque $30^\circ$. Lineam EH, ambo centra coniungentem, iam vidimus
6|$2^p4'\,\qfrac{3}{4}$ esse. Semidiametrum HM excentrici et lineam EM ducamus, HM usque ad punctum
7|L quo cum perpendiculari LE convenit protrahentes. Triangulum HLE rectangulum est; eius
8|angulus LHE aequat angulum datum FHM; arcus super EL, ex circulo triangulum HLE
9|circumdanti, si circumferentia $360^\circ$ continet, $30^\circ$ complectetur, eiusque sinus $30^p$ quoque ex
10|partibus quarum linea HE inter ambo centra 60 habet. Remanebit linea LH, quadrantem per-
11|ficiens, $51^p57'41''$, nam arcus complementaris LH $60^\circ$ continet. Sed ea ratione qua linea HE
12|inter ambo centra $2^p4'\,\qfrac{3}{4}$ complectitur, linea EL $1^p2'22''\,\qfrac{1}{2}$ (1) erit, et linea LH, quadran-
13|tem perficiens, $1^p48'2''$; itaque linea tota LM $61^p48'2''$. Triangulum MLE rectangulum est;
14|eius hypotenusam EM $61^p48'35''$ esse vidimus. Sed ratione qua lineae EM $60^p$ tribuuntur,
15|EL est $1^p33'$ (2), et arcus super eam $0^\circ57'49''$, cum circulus triangulum HLE circumdans
16|$360^\circ$ sit. Arcus igitur AB eclipticae $29^\circ2'11''$ fere remanebit.
17|[P02]\Indent Item Solem in puncto D excentrici esse ponamus, arcumque FD (3) $150^\circ$ complecti; reli-
18|quus arcus DG, inter locum Solis et perigeum, $30^\circ$ erit. Lineas EK et HD, quarum utraque
19|est sui circuli semidiametrus, ducamus; item perpendicularem ES. Triangulum HSE rectan-
20|gulum est; latus EH, ambo centra coniungens, latus ES, angulus DHG (4) nota sunt; erunt
21|ergo nota latus HS et angulus HES (5). Cognoscuntur igitur quoque linea DG et hypotenusa
22|ED trianguli rectanguli ESD. Cum vero datus arcus DG et datus angulus GHD $30^\circ$ sint ut
23|diximus, eorumque sinus $30^p$ pariter, arcus quoque ES circuli triangulum rectangulum ESH
24|circumdantis complectetur $30^\circ$ ex partibus quarum totus ille circulus $360^\circ$ habet, et eius sinus,
25|nempe cathetus ES, $30^p$ quoque e partibus quarum linea EH, semidiametrus huius circuli, $60^p$
26|complectitur. Sed ratione qua lineae EH $2^p4'\,\qfrac{3}{4}$ tribuuntur, cathetus ES erit $1^p2'22''\,\qfrac{1}{2}$ (6);
27|qua re latus SH $1^p48'2''$ remanebit.
28|Semidiametrus HD excentrici $60^p$ conti-
29|net, de quibus si SH dematur, remanent
30|lineae SD $58^p11'58''$; igitur hypote-
31|nusa ED trianguli rectanguli ESD erit
32|circiter $58^p12'32''$ (7). Sed ex partibus
33|quarum linea ED 60 habet, cathetus ES
34|$1^p4'17''$ complectetur, et arcus super
35|eam, qui est quantitas anomaliae, $1^\circ1'$
36|$24''$ (8): arcus igitur KC eclipticae, $31^\circ$
37|$1'24''$ (9) circiter erit. Haec de anomalia
38|sufficiunt, quam explicare volebamus.
39|[P03]\Indent Dicit [auctor]: Hunc motum ita ad
40|singulos gradus in tabulis a puncto apogei posuimus; similiter reperiuntur aequatio simplex
""",r"""
|[N01]\Indent (1) Secundae apud Platonem $55''$.
|[N02]\Indent (2) Cod. « unius partis et trium ac triginta se-
|« cundarum ».
|[N03]\Indent (3) Cod. AD. Postea Plato 120.
|[N04]\Indent (4) Cod. HDG.
""",r"""
|[N05]\Indent (5) Cod. HS.
|[N06]\Indent (6) Secundae apud Platonem $55''$.
|[N07]\Indent (7) Plato $58^p15'34''$. Cfr. adnot. {\itshape e} huius capitis.
|[N08]\Indent (8) Cod. $1^\circ4'24''$; Plato $1^\circ4'54''$.
|[N09]\Indent (9) Cod. $1^\circ1'24''$; Plato $31^\circ4'54''$.
""",margins=[{'line':3,'text':'p. 71.','side':'right'},{'line':25,'text':'p. 72.','side':'right'}],figures=[{'id':'AB01-PDF0136-F01','start_line':27,'end_line':39,'side':'left','image_width_fraction':.54,'text_width_fraction':.43}])

page(137,r"""
0|[P01]Lunae et aequatio media quinque planetarum, quae est semidiametrus eorum epicycli, cum
1|eius sinus sumatur et eo modo dividatur.
2|[P02]\Indent Si id calculo reperire vis, gradus epicycli quos ab apogeo Sol, vel Luna, vel planeta
3|percurrerit, scilicet anomaliam, observa; si gradus minus quam $180^\circ$ sunt, iis utere, sed si
4|$180^\circ$ superant, eos de $360^\circ$ deme et residuum adhibe. Graduum alterutra via repertorum, si
5|minus quam $90^\circ$ sunt, sinum atque cosinum multiplica in semidiametrum epicycli sideris qui
6|est totius aequationis sinus; ambo producta per semidiametrum divide, et quod ex divisione
7|cosinus provenerit adde $60^p$ scilicet semidiametro. Quadratum huius summae adde quadrato
8|eius quod e divisione sinus exierit; huius summae radicem inveni. Deinde quod e divisione
9|sinus provenerat, in semidiametrum multiplica, et productum per inventam radicem divide. ---
10|Si contra gradus adhibendi superant $90^\circ$, de iis $90^\circ$ deme; sinum et cosinum residui in semi-
11|diametrum epicycli multiplica et per semidiametrum divide; quod e sinu provenerit de $60^p$
12|deme; quadratum residui adde quadrato eius quod e cosinu exierit, et huius summae radi-
13|cem inveni. Postea quod e divisione cosinus provenerat in semidiametrum multiplica, et pro-
14|ductum per radicem inventam divide. --- Quod ex alterutra operatione tibi provenerit, in
15|arcum converte; arcus erit portio graduum ad anomaliam qua usus es pertinens, scilicet ae-
16|quatio stellae ({\itshape f}).
17|[P03]\Indent Semidiametrus epicycli Solis est $2^p4'45''$ (1); semidiametrus epicycli Lunae $5^p15'$ (2);
18|Saturni $6^p29'50''$ (3); Iovis $11^p30'0''$ (4); Martis $39^p27'22''$ (5); Veneris $43^p9'0''$ (6); Mer-
19|curii $22^p30'30''$ (7). Hoc ex observationibus patuit et cum calculis congruit; idque, volente
20|Deo, est sinus aequationis mediae ({\itshape g}).
23|[H01]\CenterLine{CAPUT XXIX.}
25|\CenterLine{De inaequalitate nychthemerōn et de aliorum in alia conversione.}
27|[P04]\Indent Dicit [auctor]: Plurimi homines et vulgus nychthemera existimant aequalia esse, et eo-
28|rum quodque 24 horas amplecti; sed hoc haud verum est, nam nychthemerum medium est
29|ortus omnium 360 temporum aequatoris ab horizonte vel a circulo meridiano, eo addito quod
30|ex aequatoris temporibus ascendit cum 59 minutis quae Sol, motu suo medio, in nychthemero
31|percurrit. Nychthemerum autem inaequale est ortus 360 temporum aequatoris, addito motu
32|inaequali Solis in nychthemero, qui necessarie minor aut maior est quam $59'$.
33|[P05]\Indent Quoniam omni loco initium a circulo horizontis variat prout in illo variant ascensiones
34|signorum, initium autem ab hora meridiana immobile est neque mutatur, ob aequalitatem
35|ascensionum signorum in circulo meridiano quolibet loco, in calculo stellarum earumque lo-
36|corum initium diei non ponitur ab ortu vel occasu Solis, sed a tempore meridiei aut mediae
37|noctis (8) ({\itshape a}).
38|[P06]\Indent Item quoniam omnes motus stellarum in tabulis nonnisi ad aequales dies supputantur,
39|differentia inter nychthemera inaequalia et nychthemera media negligitur. In motu Solis et
40|reliquarum stellarum differentia tanta non est ut errorem sensibilem gignat; sed error mani-
""",r"""
|[N01]\Indent (1) Cod. $5'$ pro $4'$.
|[N02]\Indent (2) Gradus in cod. $6^\circ$.
|[N03]\Indent (3) Secundae apud Plat. $7''$.
|[N04]\Indent (4) Secundae apud Plat. $5''$.
""",r"""
|[N05]\Indent (5) Cod. $19^\circ25'22''$; minuta apud Plat. $55'$.
|[N06]\Indent (6) Plat. $44^\circ9'5''$.
|[N07]\Indent (7) Gradus in cod. $29^\circ$.
|[N08]\Indent (8) {\itshape Almag.} III, 8 (ed. Halma, t. I, p. 208).
""",margins=[{'line':7,'text':'p. 73.','side':'left'},{'line':29,'text':'p. 74.','side':'left'}])

page(138,r"""
1|[P01]festus est in Luna, ob eius festinum cursum, ita ut fere dimidiae horae sit; nam interdum
2|Lunae motus eo temporis spatio 18 minuta complectitur, cuius duplum est differentia inter
3|maxima et minima nychthemera.
4|[P02]\Indent Haec differentia e duobus elementis constat, quorum alterum est inaequalitas motus Solis,
5|sive aequatio, alterum differentia transitus signorum per medium Caelum, quia non omnia illic
6|eadem quantitate ascendunt. Quod maximi ex anomalia motus Solis provenit est fere $3^\circ\qfrac{1}{4}+$
7|$\qfrac{1}{10}$ (1) [$=3^\circ21'$], quod e culminatione signorum $4^\circ\qfrac{1}{4}+\qfrac{1}{5}$ (2) [$=4^\circ27'$] circiter; summa
8|igitur est $7^\circ48'$ (3), quae $\qfrac{1}{2}+\qfrac{1}{50}$ horae aequinoctialis [$=0^h\,31^m\,12^s$] circiter efficiunt. Locus
9|deminutionis fere a $\qfrac{2}{3}$ (4) Aquarii ad initium circiter Scorpionis porrigitur; locus augmenti
10|ab initio Scorpionis ad $\qfrac{2}{3}$ (5) fere Aquarii. --- In tabulis huius nostri libri nos motus medios
11|descripsimus, ponentes locum Solis, iuxta eius motum medium, in $18^\circ19'$ [Aquarii], at secun-
12|dum veracem motum apparentem in $20^\circ$ Aquarii. Et iuxta hoc nychthemerum reliqua nych-
13|themera anni in hoc libro supputa ({\itshape b}).
14|[P03]\Indent Dicit [auctor]: Si vis dies inaequales convertere in dies medios, ad quos in tabulis sunt
15|motus medii descripti, sume gradus inter medium locum Solis datum et locum alterum ad
16|quem Sol motu medio pervenerit ({\itshape c}); item, per tempora ascensionum rectarum signorum,
17|gradus inter primum locum verum et locum ad quem Sol motu vero pervenerit. Si numerus
18|horum temporum numerum graduum motus medii superat, quanta pars unius horae aequino-
19|ctialis differentia sit, vide, et eam partem diebus inaequalibus datis adde. Si contra numerus
20|temporum minor est, eam partem de iis diebus deme. Exibunt dies medii, in quos dies inaequa-
21|les dati convertendi erant, sive a meridie sive a media nocte calculus diei inchoatus est. ---
22|Rem contrariam fac, si dies medios tabularum in dies inaequales convertere vis; idest partem
23|illam diebus mediis adde vel de iis deme, prout numerus temporum minor vel maior fuerit.
24|Invenies dies inaequales quaesitos.
25|[P04]\Indent Iuxta hoc principium, in hoc nostro libro constitutum, numerus temporum semper minor
26|erit a loco Solis dato usque ad terminum longi spatii temporis, in quo variatio apogei Solis,
27|quod in ecliptica invenimus, crescet; qua re mutabitur quod ex inaequalitate motus Solis pro-
28|venit. Et cum res ita sint ut diximus, loco medio Lunae in initio calculi 18 (6) minuta addidi-
29|mus; portionem autem variationis nychthemerōn, quae ad singulos gradus signorum pertinet,
30|in tabulis ascensionum rectarum (7) descripsimus in columna quae ascensiones singulorum gra-
31|duum sequitur. Si igitur quod vero gradui Solis respondet sumpserimus, et partem propor-
32|tionalem unius horae aequinoctialis de diebus inaequalibus detraxerimus, remanebunt dies
33|medii, ad quos in tabulis motus reperiuntur; si vero eam diebus mediis addiderimus, exibunt
34|dies inaequales qui calculo deducuntur ({\itshape d}).
""",r"""
|[N01]\Indent (1) Male Plato $3^\circ\qfrac{1}{5}+\qfrac{1}{10}$, quod $3^\circ18'$ effice-
|ret. --- In {\itshape Almag.} III, 8 (ed. Halma t. I, 209) est $3^\circ\qfrac{2}{3}$;
|ibi enim excentricitas orbis solaris maior est quam
|apud al-Battānī.
|[N02]\Indent (2) {\itshape Almag.} $4^\circ\qfrac{2}{3}$; differentia e diversa eclipti-
|cae obliquitate provenit.
""",r"""
|[N03]\Indent (3) {\itshape Almag.} $8^\circ\qfrac{1}{3}$ scilicet $\qfrac{1}{2}+\qfrac{1}{18}$ horae.
|[N04]\Indent (4) {\itshape Almag.} $\qfrac{1}{2}$.
|[N05]\Indent (5) {\itshape Almag.} $\qfrac{1}{2}$.
|[N06]\Indent (6) Plato 58. --- Cur id fecerit explicatur in
|adnot. {\itshape b} ad hoc caput.
|[N07]\Indent (7) Fol. 179,r.--181,v.
""",margins=[{'line':13,'text':'p. 75.','side':'right'}],signature='7')

page(139,r"""
3|[H01]\CenterLine{CAPUT XXX.}
5|\CenterLine{De sphaeris Lunae, de inaequalitate eius motus, de accretione et demi-}
6|\CenterLine{nutione eius luminis, de causis eclipsium, atque de distantiis geo-}
7|\CenterLine{centricis, diametris et magnitudinibus amborum luminarium cum}
8|\CenterLine{Terra comparatorum.}
10|[P01]\Indent Dicit [auctor]: In motibus Lunae duae inaequalitates repertae sunt. Altera, per se simplex,
11|temporibus syzygiarum, quae ob medium Solis et Lunae iter iuxta locum Lunae in epicyclo
12|fiunt, apparet. Altera per elongationes Lunae a Sole deprehenditur, et primae inaequalitati ita
13|adiungitur ut simul unam rem efficiant, sicut demonstrationibus geometricis cognoscitur.
14|[P02]\Indent Luna quatuor sphaeras [seu circulos] habere cogitetur; quorum primus concentricus et
15|similis sit eclipticae, eodemque motu sub ea absque ulla deviatione moveatur (1) --- Secundus ab
16|eo in septentriones et meridiem versus deflectat, sed eandem magnitudinem idemque centrum
17|ac ille habeat; maxima eius declinatio in utramque plagam versus sit fere $5^\circ$, quae est maxima
18|distantia latitudinalis Lunae ab ecliptica. Motus huius circuli deflectentis [i. e. obliqui] quotidie
19|sit 3 minutorum fere in partem contrariam successionis signorum; et hic est motus duorum
20|nodorum, quorum alter, a quo Luna in latitudine ad septentriones transit, {\itshape Caput} vocatur, alter
21|vero, a quo Luna ad meridiem transit, {\itshape Cauda}. Hi nodi sunt loca ubi circulus deflectens cir-
22|culum pareclipticum secat. --- Intra circulum deflectentem [seu obliquum] tertius reperiatur,
23|qui excentricus sit, a deflectente pendat, eumque in puncto omnium altissimo, {\itshape apogeo} appel-
24|lato, contingat; ipse quotidie intra circulum deflectentem versus partem contrariam successioni
25|signorum $11^\circ12'$ circiter (2) moveatur. --- Quartus circulus sit epicyclus Lunae, cuius cen-
26|trum in circumferentia excentrici quotidie $24^\circ23'$ fere (3) ad successionem signorum mo-
27|veatur, ut sit initium motus a puncto apogei excentrici dato cum loco medio Solis. Centrum
28|igitur epicycli bis in mense lunari in punctum apogei incidit; altera vice tempore mediae
29|coniunctionis, altera tempore oppositionis; Luna autem quotidie in circumferentia epicycli
30|fere $13^\circ4'$ (4) versus partem contrariam successionis signorum movetur, incipiens a puncto
31|apogei quod respectu centri excentrici consideratur. Et cum centrum epicycli super circum-
32|ferentiam circuli deflectentis duobus memoratis temporibus incidat, nihil obstat quin epicycli
33|centrum quotidie super circumferentiam deflectentis $13^\circ14'$ fere moveatur; et hic est motus
34|Lunae in latitudine. Sed nodus eum versus partem contrariam successionis signorum minuit
35|tribus minutis memoratis, quae sunt motus circuli deflectentis; qua re motus Lunae in lon-
36|gitudine ad successionem signorum remanet $13^\circ11'$ fere in die. Motus in epicyclo est primus
37|quem memoravimus.
38|[P03]\Indent Ex iis quae diximus patet motui Lunae nullam variationem ob excentricum his duobus tem-
39|poribus contingere, nam in iis Luna a loco Solis medio vel huic opposito non recedit, et inae-
40|qualitas simplex cum altera non commiscetur eo usque quo Luna a Sole non recesserit; et
""",r"""
|[N01]\Indent (1) Eum infra {\itshape pareclipticum} voco; cfr. p. 45,
|adn. 3.
|[N02]\Indent (2) Nam motus apogei = duplus motus syno-
|dicus $-$ motus in latit. $+$ motus nodorum $=24^\circ$
|$23'-13^\circ14'+0^\circ3'=11^\circ12'$.
""",r"""
|[N03]\Indent (3) Est duplus motus synodicus (vel relativus
|sive dupla elongatio.
|[N04]\Indent (4) Est motus diurnus anomaliae, quem \Name{Pto-}
|\Name{lemaeus} IV, 3 (ed. Halma t. I, p. 223) invenit esse
|$13^\circ3'53''56'''29^{\mathrm{IV}}38^{\mathrm{V}}38^{\mathrm{VI}}$.
""",margins=[{'line':3,'text':'p. 76.','side':'left'},{'line':27,'text':'p. 77.','side':'left'}])

page(140,r"""
1|[P01]\raisebox{-0.15pt}{\includegraphics[height=6.1pt]{AB01-PDF0140-G01.png}} his distantiis ei altera tantum inaequalitas additur, quae ab excentrico iuxta Lunae a Sole
2|elongationem oritur.
3|[P02]\Indent Haec est imago quatuor sphaerarum Lunae, ad demonstrationem geometricam inserviens.
4|[P03]\Indent Dicit [auctor]: Circa centrum E sit
5|circulus pareclipticus (1) ABCD, qui eodem
6|tempore sit etiam circulus deflectens [i. e.
7|obliquus]; similiter sphaerae continget quae
8|circa eius polos revolvitur. Diametrum AS
9|ducamus, in cuius puncto F sit centrum ex-
10|centrici AMP, radio FA descripti. Arcus AM
11|sit motus epicycli a puncto A, apogeo et
12|loco Solis, usque ad M, quod centrum epi-
13|cycli GHRK ponamus. [Punctum F′ in dia-
14|metro ita signetur ut sit EF′ = EF]. Li-
15|neas EMG, F′MH (2) ducamus; erit G (3)
16|locus apogei in epicyclo, ut centro E Ter-
17|rae et eclipticae apparet; H (4) locus veri
18|apogei qui ex puncto F′ (5) conspicitur. Pa-
19|tet arcum HG esse differentiam [i. e. ae-
20|quationem] motus anomalistici Lunae in
21|in epicyclo, quae in tertia columna tabularum aequationis Lunae (6) describitur. In epicyclo
22|Luna a G ad H, postea ad R moveatur, denique ad K perveniat. Lineam [E]KN, epicyclum
23|tangentem, ducamus; item MK [perpendicularem], quae erit semidiametrus epicycli [a Sole]
24|declivis quantitate qua centrum epicycli a puncto A excentrici deflectit. Quoniam Luna est
25|in linea epicyclum tangente, haec semidiametrus epicycli [vel angulus MEK ab eadem sub-
26|tensus] est summa inaequalitatis simplicis et alterius inaequalitatis, quae iuxta elongationem
27|Lunae a puncto A Solis determinantur ({\itshape a}). --- Ut ex hac figura patet, Luna stante in prima
28|medietate GHR epicycli, locus verus Lunae in ecliptica, qui a centro E videtur, minor est
29|loco medio eius in longitudine, qui est centrum epicycli; aequatio igitur de medio motu
30|Lunae demitur, si anomalia minor quam $180^\circ$ est. Cum autem Luna in altera medietate RKG
31|sit, eius locus verus locum medium in ecliptica superat; qua re, anomalia $180^\circ$ excedente,
32|aequatio, si Deus vult, motui medio Lunae est addenda.
33|[P04]\Indent Aequatio simplex, quae temporibus syzygiarum apparet et in hoc nostro libro in secunda
34|columna tabularum aequationis (7) describitur, iam diximus quo modo numeris supputetur,
35|eadem via quam secuti sumus in calculanda et in tabulis describenda aequatione Solis (8).
36|Maxima quantitas, quam haec simplex inaequalitas Lunae attingere potest, est $5^\circ1'$ (9), cuius
37|sinus, qui tunc erit semidiametrus epicycli, $5^p\qfrac{1}{4}$ fere complectitur; talis enim est ratio 60 par-
38|tium semidiametrum efficientium ad $5^p\qfrac{1}{4}$. Id Ptolemaeus (10) declaravit et probavit eclipsibus
""",r"""
|[N01]\Indent (1) Vide supra pag. 50, adn. 1.
|[N02]\Indent (2) Cod. et Plato: EMH, FMG.
|[N03]\Indent (3) Cod. et Plato H.
|[N04]\Indent (4) Cod. et Plato G.
|[N05]\Indent (5) Cod. et Plato: « ex centro F scilicet ex cen-
|tro excentrici ». Punctum F′ apud eos deest.
|[N06]\Indent (6) Fol. 189,v. et sqq; sed est tertia columna
|tantum si columna aequationis Solis non computetur.
""",r"""
|[N07]\Indent (7) Fol. 189,v. et seqq.; sed est secunda colu-
|mna tantum si columna aequationis Solis vel colu-
|mna numerorum non computetur.
|[N08]\Indent (8) Cap. XXVIII.
|[N09]\Indent (9) Sunt numeri Ptolemaei.
|[N10]\Indent (10) {\itshape Almag.} IV, 5 (ed. Halma, t. I, pag. 244-
|-260).
""",margins=[{'line':11,'text':'p. 78.','side':'right'}],figures=[{'id':'AB01-PDF0140-F01','start_line':4,'end_line':20,'side':'left','image_width_fraction':.48,'text_width_fraction':.48}])

page(141,r"""
1|[P01]lunaribus, in quibus necessarie locus verus Lunae loco vero Solis in ecliptica opponitur; qua
2|re elongatio inter locum Lunae iuxta eius motum medium, et gradum gradui vero Solis oppo-
3|situm, erit inaequalitas simplex motus Lunae iuxta eius locum in epicyclo. --- Nos quoque
4|multas eclipses lunares observavimus, earum tempora et medium diligentissime investigavimus,
5|et quantitatem huius simplicis inaequalitatis ut diximus reperimus ({\itshape b}).
6|[P02]\Indent Maximam quantitatem alterius inaequalitatis, contingentis ob elongationem Lunae a Sole,
7|fere $2^\circ\qfrac{2}{3}$ attingere invenerunt (1), quibus si $5^\circ1'$ simplicis inaequalitatis addantur, $7^\circ40'$ cir-
8|citer proveniunt. Hoc evenit cum epicycli centrum sit in P, quod ab A quantitate [dimidii]
9|excentrici distat (2); tunc semidiametrus epicycli [a loco Solis] declivis, erit fere $8^p$, quae
10|sunt sinus iis $7^\circ\qfrac{2}{3}$ respondens.
11|[P03]\Indent Ex iis quae diximus consequitur lineam EF, ambo centra coniungentem, $10^p19'$ (3) esse;
12|idque hoc modo demonstratur. Circa centrum A, apogeum excentrici, epicyclum HG descri-
13|bamus; lineam tangentem EH, et lineam AH ducamus. Quoniam Luna in linea tangente est,
14|inaequalitas simplex tota perficitur, quam $5^\circ1'$ esse vidimus e partibus quarum quatuor an-
15|guli recti 360 continent; eius sinus igitur $5^p15'$ (4) iuxta rationem qua semidiametrus in 60
16|partes dividitur, ut semidiametrus circuli qui in hac figura excentricum repraesentat. --- Circa
17|centrum P, perigeum excentrici, epicyclum HG describamus, et lineam tangentem EH atque
18|lineam PH ducamus. Quoniam Luna in puncto H, scilicet in linea tangente, est, ambae inae-
19|qualitates perficiuntur, quarum summa $7^\circ40'$ complectitur, et sinus summae $8^p$ fere continebit,
20|iuxta rationem qua quatuor anguli recti $360^\circ$ efficiunt, et semidiametrus, idest EA, in 60 par-
21|tes dividitur. --- Linea PH aequalis est lineae AH. quam $5^p\qfrac{1}{4}$ esse vidimus, si $60^p$ semidia-
22|metro EA tribuantur; sed quia centrum epicycli in locum venit quo, ob proximitatem puncti E,
23|--- quod est centrum Terrae et locus veri aspectus, --- dimensio mutari debet, id quod ex
24|observatione apparet fiet $8^p$ circiter secundum rationem qua EA $60^p$ complectitur; sed iuxta
25|rationem qua $8^p$ in $60^p$ convertuntur, $5^p\qfrac{1}{4}$ fient $39^p22'$. Et haec est quantitas lineae EP,
26|centrum Terrae cum perigeo excentrici coniungentis. Similiter ut $8^p$ in $5^p\qfrac{1}{4}$ convertuntur,
27|$60^p$ fiunt $39^p22'$. Si linea EP, quam $39^p22'$ esse vidimus, lineae EA, $60^p$ complectenti, addatur,
28|summa $99^p22'$ erit diametrus tota excentrici, cuius dimidia pars $49^p41'$ attinget. [Qua re
29|excentricitas $10^p19'$ complectitur ex partibus quarum AE $60^p$ continet] (5).
30|[P04]\Indent Cognita semidiametro epicycli iuxta eius declivitatem (6) respectu Solis, et cognita etiam
31|excentricitate atque semidiametro excentrici, restat nobis ut arcum HG, in tertia (7) columna
32|descriptum, supputemus et exponamus quanta fiat summa aequationis simplicis et alterius in
33|locis inter duas longinquitates, eo modo qui in tabulis descriptus est in quarta et quinta (8)
34|columna; et, quod ad quartam columnam attinet, cum hi $2^\circ40'$ fient $60'$ quae in quinta co-
35|lumna notantur, videamus quantum ex iis coadunetur, et quae sit eius ratio ad 60 (9). Haec
36|omnia, ut nunc docebimus, cognoscuntur.
""",r"""
|[N01]\Indent (1) Ita {\itshape Almag.} V, 3 (ed. Halma t. I, p. 293--206).
|[N02]\Indent (2) Plato: « punctum P, quod est egressi circuli
|longitudinis propior », i. e. perigeum excentrici. Sen-
|sus cum verbis codicis optime convenit.
|[N03]\Indent (3) Plato $10^\circ18'$; demonstratio et numeri se-
|quentes reperiuntur in {\itshape Almag.} V, 4 (ed. Halma, t. I,
|p. 296--297).
|[N04]\Indent (4) Minuta in cod. $25'$.
|[N05]\Indent (5) Addidi, Platonem et Ptolemaeum sequens.
""",r"""
|[N06]\Indent (6) I. e. iuxta elongationem centri epicycli a
|Solis loco.
|[N07]\Indent (7) Si columna numerorum singulorum, vel co-
|lumna Solis non computetur.
|[N08]\Indent (8) Quinta et sexta.
|[N09]\Indent (9) \Name{Schiaparelli} duce, interpretandum vi-
|detur: « et quoad quartam columnam, exhibetur in
|« ea pars proportionalis ad 60 sumenda de numeris
|« qui in quinta columna notantur ».
""",margins=[{'line':2,'text':'p. 79.','side':'left'},{'line':25,'text':'p. 80.','side':'left'}])

page(142,r"""
1|[P01]\Indent Lineam ME (1) usque ad L producamus, et L cum F coniungamus (2); in triangulo MLF
2|latera proportionalia (3), anguli noti sunt. Arcum AM, ut Ptolemaeus statuit, $120^\circ$ ponamus (4),
3|quae est dupla elongatio Lunae a Sole. Quoniam rationem sinuum ad semidiametrum (5) re-
4|ferimus, angulus EFL (6) $30^\circ$, eiusque complementum FEL $60^\circ$ continebit, iuxta rationem qua
5|circulus triangulum FEL circumdans $360^\circ$ complectitur. Sinus anguli EFL (7) $30^p$ quoque erit,
6|et sinus anguli FEL circiter $51^p58'$ (8) ex partibus quarum linea EF 60 continet; sed si huic
7|lineae $10^p19'$ tantum (9) tribuantur, linea EL $5^p10'$, linea FL $9^p16'$ (10) circiter fiet. Cum
8|in figura linea EKN epicyclum tetigerit, et locus Lunae in epicyclo fuerit punctum K, erit
9|id maximum quod attingit summa primae inaequalitatis et secundae. Cum autem semidia-
10|trus MK epicycli et semidiametrus FM excentrici notae sint, ex ratione FM et FL ratio li-
11|neae ML deprehendetur, eritque tota ML $48^p53'$; de qua, linea EL scilicet $5^p10'$ demptis,
12|remanet linea EM a centro [Terrae sive zodiaci] progrediens $43^p43'$. Semidiametrum MK
13|epicycli vidimus $5^p15'$ esse: sed si lineae EM a centro [Terrae vel zodiaci] progredienti $60^p$
14|tribuantur, semidiametrus MK epicycli declivis [ab apogeo excentrici] $7^p12'$ circiter fiet,
15|et arcus MK super eam insistens $6^\circ54'$ (11) fere continebit. De quo, si tota simplex inaequali-
16|tas, idest $5^\circ1'$, dematur, altera inaequalitas ei adiecta remanebit $1^\circ53'$; et si illi $2^\circ\qfrac{2}{3}$ (12) fiant
17|$60'$, hi $1^\circ53'$ in partes sexagesimas $0^\circ42'38''$ (13) convertentur, quae sub numero 120 in
18|quarta (14) columna reperiuntur. {\itshape Hoc secundum rationem minutorum ad gradum, quae}
19|{\itshape est ratio $0^\circ42'38''$ ad $60'$. Si haec $0^\circ42'38''$ usque ad $60'$ crescunt, ea $1^\circ53'$ fiunt}
20|{\itshape $2^\circ39'$, quae in quinta} (15) {\itshape columna sub numero 120} (16) {\itshape leguntur} ({\itshape c}).
21|[P02]\Indent Nunc differentiam inter apogeum verum et apo-
22|geum medium (17), idest arcum HG, cognoscamus.
23|Elongatio Lunae a Sole, iuxta motum medium du-
24|plicatum, sit $90^\circ30'$, ut Ptolemaeus (18) in figura
25|ex qua id deprehenditur posuit; et motus Lunae in
26|epicyclo a puncto A sit $333^\circ12'$. Ad haec explicanda
27|hunc circulum ponamus.
28|[P03]\Indent Dicit [auctor]: Circa centrum D diametrumque
29|AC sit excentricus ABC; E ponamus centrum ecli-
30|pticae, B centrum epicycli MGH. Lineas BM, EBG
31|ducamus, BE usque ad K protrahentes, et K cum
32|D coniungamus, ita ut angulus KDE sit dimidius
33|gradus qui $90^\circ$ excedit; et arcus EK dimidium gra-
""",r"""
|[N01]\Indent (1) Vide figuram pag. 51. --- Iisdem numeris
|demonstratio legitur in {\itshape Almag.} V, 7 (= ed. Halma,
|t. I, p. 313--314).
|[N02]\Indent (2) FL est perpendicularis ad KL.
|[N03]\Indent (3) Interpretandum videtur: « proportiones la-
|terum sunt notae ».
|[N04]\Indent (4) Non arcum AM, sed angulum AEM Ptole-
|maeus $120^\circ$ complecti statuit; arcus AM subtendit
|angulum AFM maiorem quam AEM (\Name{Schiapa-}
|\Name{relli}).
|[N05]\Indent (5) Plato addit: « et ad quadrantem circuli ».
|[N06]\Indent (6) Cod. et Plato, ut parum infra, AEM.
|[N07]\Indent (7) Cod. et Plato, ut supra, AEM.
""",r"""
|[N08]\Indent (8) Codex $11^p18'$.
|[N09]\Indent (9) Est excentricitas paulo antea reperta.
|[N10]\Indent (10) Plato $18^p56'$.
|[N11]\Indent (11) Gradus in cod. $5^\circ$.
|[N12]\Indent (12) Maximae secundae inaequalitatis, cf. su-
|pra p. 52.
|[N13]\Indent (13) Pro $42'$ Plato semper 45.
|[N14]\Indent (14) Vel potius quinta, cfr. supra p. 51, adn. 6
|et 7; p. 52, adn. 7 et 8.
|[N15]\Indent (15) Vel potius sexta.
|[N16]\Indent (16) Sed in tabulis sub numero 110 reperiuntur.
|[N17]\Indent (17) In tabulis {\itshape aequatio anomaliae} appellatur.
|[N18]\Indent (18) {\itshape Almag.} V, 6 (ed. Halma t. I, p. 308--311).
""",margins=[{'line':12,'text':'p. 81.','side':'right'}],figures=[{'id':'AB01-PDF0142-F01','start_line':21,'end_line':33,'side':'left','image_width_fraction':.43,'text_width_fraction':.55}])

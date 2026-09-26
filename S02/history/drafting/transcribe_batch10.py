from work_helpers import *
# Source-based name repairs to the unreleased working JSON, retaining a change ledger.
repairs=[]
for n in (103,105):
 path=R/f'transcription/pages/AB01-PDF{n:04}.json';d=json.loads(path.read_text())
 for sec in d['sections']:
  for line in sec['lines']:
   if 'al-Ġaġmīnī' in line['text']:
    old=line['text'];line['text']=old.replace('al-Ġaġmīnī','al-Ġaghmīnī')
    repairs.append({'anchor':line['id'],'before':old,'after':line['text'],'evidence':f'AB01-PDF{n:04}-NAME-proof','reason':'The source visibly has gh, not a second ġ; restore the printed transliteration.'})
 path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
ledger=R/'ledgers/working_repairs.json';existing=json.loads(ledger.read_text()) if ledger.exists() else [];ledger.write_text(json.dumps(existing+repairs,ensure_ascii=False,indent=2)+'\n')
save_page(117,r'''[body]
partis unius horae aequinoctialis posuimus, ut ascensiones quae nobis opus sunt melius et ve-
rius cognoscantur quam ex ascensionibus cum intervallo dimidiae horae descriptis (1).
Si in tabulis ascensiones cuiuslibet gradus reperire vis, gradum illum in columna nume-
rorum singulorum in tabula ascensionum dati climatis quaere, aut in tabula ascensionum re-
ctarum; quod ei respondet in columna temporum ascensionalium, indicat ascensiones ab initio
Arietis ad gradum datum, si ascensiones climatis adhibuisti, aut ascensiones ab initio Capri-
corni ad eum gradum, si ascensionibus rectis usus es (2). Si una cum gradibus etiam minuta
habes, quanta pars e 60 sint, si numeri cum intervallo unius gradus sunt descripti, vide;
partem proportionalem e differentia inter ascensiones illas et ascensiones in tabula proxime
superiores sume, et ascensionibus gradus integrorum adde. Si gradus autem per decades distri-
buti sunt, quanta pars unius decadis sint gradus minutaque redundantia vide; partem pro-
portionalem e differentia inter ascensiones decadum datarum et decadis statim superioris sume,
atque ascensionibus decadum integrarum adde.
Si ab ascensionibus cupis gradus signorum cognoscere, — idque appellatur ascensionum
arcuatio et conversio ad gradus aequalitatis (3), qui sunt ipsi gradus signorum, — in tabula
ascensionum rectarum aut obliquarum tempora ascensionalia data, vel tempora iis quam
maxime proxima sed minora quaere, et gradus iis in columna numerorum respondentes sume.
Postea tempora in tabula reperta de temporibus datis deme; residuum in 60 minuta mul-
tiplica, si numeri graduum cum intervallo unius gradus sunt descripti, aut in 600 minuta, si
numeri sunt ad decades; productum per differentiam inter ascensiones inventas et ascensiones
in tabula eas statim sequentes divide; gradus et minuta quae exibunt gradibus iam inventis
adde; et iuxta id per quod operatus eris habebis tunc quantitatem illius signi ascendentem
aut culminantem. — Vel, si mavis, residuum inventum vide quanta pars ex differentia ascen-
sionum sit; partem proportionalem ex intervallo numerorum sume, atque gradibus iam
repertis adde.
Si per tabulas scire vis arcum diurnum et nocturnum, scilicet quantitatem circuli aequi-
noctialis ab ortu ad occasum Solis vel ab occasu ad crastinum ortum ascendentem, die data
gradum Solis inveni; tempora ascensionum ei respondentia sume in climate, quod latitudini
tuae urbis aequale vel saltem quam maxime vicinum est; ea tempora de ascensionibus illius
climatis, gradui respondentibus qui gradui Solis oppositus est, deme; residuum est arcus diur-
nus. Si ascensiones gradus Solis maiores sunt ascensionibus gradus oppositi, 360° adde ascen-
sionibus nadir, et de summa ascensiones Solis deme; residuum erit arcus diurnus. Arcum
nocturnum habebis de 360° arcum diurnum demendo.
Si aliter arcum diurnum cognoscere vis, tempora ascensionum obliquarum et ascensionum
rectarum gradus Solis accipe, postquam de iis 90 gradus detracti sunt, ut ab Arietis initio
incipiant; differentiam inter ea inveni, quam, si tempora ascensionalia climatis maiora [ascen-
sionibus rectis] sunt, de 90° deme, at si minora, 90 gradibus adde. Exibit arcus semidiurnus,
qui duplicatus arcum diurnum efficit. Hanc differentiam ascensionalem scias portionem esse
diversitatis diei quae ad gradum Solis pertinet; eam, si gradus Solis in signis borealibus est,
[notes_left]
(1) Tabulae sunt in fol. 181,v. et seqq.
(2) Ascensionum rectarum initium in primo
puncto Capricorni auctor ponit; cfr. cap. V, pag. 14.
(3) Si circulus declinationis eclipticam et aequa-
torem secat, gradus eclipticae ab aequinoctio ad
circulum appellantur <i>gradus aequalitatis</i> respectu
[notes_right]
arcus aequinoctialis inter initium Arietis et circu-
lum declinationis, scilicet respectu ascensionis rectae.
Vide <n>al-Ġaghmīnī</n>, p. 238; <n>Aboul Hhassan</n>,
cap. XXXII, p. 218. In Tabulis Alphonsinis vocantur
<i>gradus aequales</i>.
[margins]
p. 41.
p. 42.
5; 10; 15; 20; 25; 30; 35
''')
save_page(118,r'''[body]
adde 90 gradibus; si in signis australibus, de 90° deme; exibit arcus semidiurnus, scilicet pars
circuli aequinoctialis ab ortu ad culminationem Solis tempore meridiano. Eius duplum est ar-
cus diurnus.
Si numerum horarum aequinoctialium diei vel noctis scire vis, arcum diurnum vel arcum
nocturnum per 15 divide; exibunt horae arcus delecti. Quibus de 24 detractis, remanent ho-
rae alterius arcus.
Si tempora horarum temporalium diei vel noctis scire cupis, quae semper 12 sunt et
horae obliquae etiam appellantur, arcum diurnum vel nocturnum per 12 divide; exeunt tem-
pora horarum. Si tempora horaria alterius arcus de 30° demis, invenis alterius tempora ho-
raria; nam haec 30 sunt tempora duarum horarum aequinoctialium, et quod e temporibus
unius horae noctis vel diei deficit, alteri additur.
Si tempora horaria aliter scire cupis, accipe sextam partem residui diversitatis diei, quod
iam in hoc capite memoravimus; si Sol vel gradus datus in hemisphaerio boreali est, 15° adde
sextae parti illi; si in hemisphaerio australi, eam partem de 15° deme. Exibunt tempora ho-
raria diei.
Si per tabulam tempora horarum diei scire vis, in tabulam ascensionum climatis tuae urbis,
in columnam numerorum singulorum intra cum gradu Solis vel eclipticae, et horarum tempora
ei respondentia in tabula illius signi in quo datus gradus habetur, sume; haec sunt tempora
horaria diei. — Si tempora horaria noctis cupis, tempora quae nadir gradus Solis respondent
in tabula eodem modo sume, et habebis tempora horaria noctis. — Alia etiam ab aliis depre-
hendi possunt, nam alia e 30° detracta, alia efficiunt.
Si a temporibus horariis arcum diurnum aut nocturnum discere vis, tempora illius quem
vis in 6 (1) multiplica; habebis arcum semidiurnum aut seminocturnum, iuxta id quod
supputaveris. Arcum inventum duplicans, arcum totum diei aut noctis habebis. Si gradus (2)
temporum in 12 multiplicas, exit arcus diurnus aut nocturnus gradus dati.
Si horas aequinoctiales in temporales convertere vis, horas aequinoctiales in 15 multiplica
et per tempora horaria diei aut noctis divide; exibunt horae temporales diei vel noctis, prout
fuerint illae aequinoctiales diurnae aut nocturnae. Si vis horas temporales in aequinoctiales
convertere, horas diurnas in tempora horaria diei, nocturnas in tempora horaria noctis mul-
tiplica; productum per 15 divide; provenient horae aequinoctiales una cum fractionibus, si,
Deo volente, fractiones remanserint.
<center>CAPUT XIV.</center>
<center>De cognoscenda per observationes latitudine locorum terrestrium</center>
Dicit [auctor]: Si cuiuslibet loci latitudinem, quae idem est ac eius longinquitas ab aequa-
tore vel etiam altitudo poli borealis eo loco, scire vis, altitudinem meridianam Solis, idest eo
tempore quo Sol per lineam meridianam transit, quadrante vel cognitione umbrae inveni, et de-
clinationem gradus Solis eodem tempore deprehende, quam, si borealis est, de altitudine demes,
at si australis altitudini addes; exibit altitudo initii Arietis vel initii Librae eo loco. Eam de
[notes_left]
(1) Plato: 60.
(2) Parva Arabicarum litterarum mutatione,
[notes_right]
pro <ar>اجزا</ar> Plato legit <ar>احد</ar> « unum ». Ambae lectiones
bonae sunt.
[margins]
p. 43.
p. 44.
5; 10; 15; 20; 25; 30; 35; 40
''')
save_page(119,r'''[body]
90° deme, et habebis latitudinem loci <i>(a)</i>. — Latitudo loci quae e tabula latitudinum ur-
bium (1) deprehenditur, veritati tantum est propinqua, nec ita certa ut latitudo observationibus
cognita (2).
<center>CAPUT XV.</center>
<center>De cognoscenda altitudine meridiana Solis quacumque die.</center>
Dicit [auctor]: Si qualibet die altitudinem meridianam Solis cognoscere vis, declinationem
gradus Solis, cum borealis sit, de latitudine loci deme, aut, si australis, latitudini adde; quod
exibit de 90° detrahe, et residuum erit altitudo Solis tempore meridiano. Si autem declinatio
maior est latitudine loci, Solem a septentrionibus zenith loci esse scias; qua re declinationem
deme de latitudine 90 gradibus aucta; habebis altitudinem super horizontem borealem.
Aliter etiam altitudinem meridianam Solis cognoscere potes. Latitudinem loci de 90° deme
ut altitudinem initii Arietis habeas; postea declinationem, si borealis est, altitudini illi adde,
vel, si australis, de ea deme; exibit altitudo meridiana Solis. Quae, si 90° superaverit de 180°
dematur; residuum erit altitudo super horizontem borealem <i>(a)</i>.
<center>CAPUT XVI.</center>
<center>De cognoscendis horis diei transactis per observationem Solis,</center>
<center>et de inveniendo ascendente.</center>
Dicit [auctor]: Si dimetiendo Sole horas praeteritas diei scire cupis, Solis altitudinem me-
ridianam et arcum semidiurnum ea die cognosce; sinum versum huius arcus, ut in capite de
chordis [cap. III] explicavimus, inveni; denique vel quadrante vel umbra altitudinem Solis me-
tire. Sinum altitudinis Solis eo tempore in sinum versum arcus semidiurni multiplica, et quod
exierit per sinum altitudinis meridianae divide: quod ex divisione prodibit, a sinu verso arcus
semidiurni deme; residui autem arcum versum, iuxta ea quae de sinibus versis arcuandis
[cap. III] diximus, inveni. Si observatio horis antemeridianis facta est, hunc arcum versum de
arcu semidiurno deme; si horis pomeridianis, arcui semidiurno adde; exibit arcus revolutio-
nis sphaerae ab ortu Solis ad tempus observationis <i>(a)</i>. Quem si per tempora horaria diei, a
gradu Solis cognoscenda, diviseris, habebis horas temporales diei praeteritas; si vero per 15°
diviseris, habebis horas aequinoctiales.
Si ascendens per id quod spherae [ab initio diei] revolutum est scire vis, arcum revolu-
tionis adde temporibus ascensionum quae gradui Solis in eo climate respondent; ex hac summa,
eo modo quem in anteriore libri parte [cap. XIII] docuimus, ascendens cognosces.
Si vis (3) potes arcum versum [supra] inventum, scilicet distantiam Solis a linea medii
Caeli, per tempora horaria diei dividere; quod exibit, de sex horis deme, si observatio ante
meridiem fuerit, vel sex horis adde, si post meridiem; exibunt horae temporales transactae,
quas in horas aequinoctiales convertere poteris.
[notes_left]
(1) Vide tabulas in fol. 172,v.–175,v.
(2) Plato addit: « Est iterum alius modus id
« addiscendi per stellas scilicet fixas, quod veritati
[notes_right]
« fere appropinquat, si Deus voluerit ». Sed forte
est interpolatio.
(3) Scilicet horas temporales cognoscere.
[margins]
p. 45.
5; 10; 15; 20; 25; 30; 35; 40
''')

"""Write S06/apparitions/apparitions_discrepancies.tsv: Nallino's corrections of pp. 142-143 (kind «noted», generated
from apparitions_readings.tsv and the data), and the differences found by check_apparitions.py, each confirmed on the
scan of the table and compared with the readings that Nallino lists (Part II pp. 262-268)."""
import csv, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.argv = sys.argv[:1]
import check_apparitions as ca

OUT = HERE / "apparitions_discrepancies.tsv"
dm = ca.dm


def reading(x):
    parts = []
    for f, unit in (("deg", "°"), ("min", "′")):
        if x[f]:
            t = x[f] + unit
            parts.append(f"({t})" if x[f + "_mark"] == "false" else f"{t} [uncertain]" if x[f + "_mark"] else t)
    return " ".join(parts)


def comp(col, i):
    return ca.COMP[col][i]


def off(col, i, value=None):
    v = ca.CORRECTED[col][i] if value is None else value
    return f"{abs(v - comp(col, i)):.0f}′"


L = []
for (col, i), (p, c, rd) in sorted(ca.CORRECTIONS.items(), key=lambda kv: (list(ca.PRINTED).index(kv[0][0]), kv[0][1])):
    src = "; ".join(f"{ca.SOURCE[x['source']]}: {reading(x)}" for x in rd if not x["source"].startswith("Nallino"))
    note = (f"{src}. Nallino (p. 269) adopts the readings of Theon and of the Latin Almagest that he marks neither false "
            f"(in brackets) nor uncertain")
    if any(x["source"].startswith("Nallino") for x in rd):
        note += ", and restores the degrees 2° of the evening setting of Venus"
    note += "."
    if col in ca.COMP:
        note += (f" The computation gives {dm(comp(col, i))}: the reading lies {off(col, i)} from it, the printed value "
                 f"{off(col, i, p)}.")
    else:
        note += " The column is not computed (see the README)."
    L.append((ca.key(col, i), dm(p), dm(c), "noted", note))

ma, mo = ca.CORRECTED["mars_app"], ca.CORRECTED["mars_occ"]
L += [
    ("identity mars app Libra = occ Aries", f"{dm(ma[6])}, {dm(mo[0])}", "equal", "identity",
     f"with Nallino's readings, the apparition of Mars at the beginning of Libra is Theon's {dm(ma[6])} and the "
     f"occultation at the beginning of Aries Theon's {dm(mo[0])}; the other 31 identities of the table hold. The printed "
     f"table has {dm(ca.PRINTED['mars_app'][6])} and {dm(ca.PRINTED['mars_occ'][0])}; the computation gives "
     f"{dm(comp('mars_app', 6))} for both"),
    ("p. 143 ven_occ_mat Virgo", dm(ca.PRINTED["ven_occ_mat"][5]), dm(comp("ven_occ_mat", 5)), "value",
     f"the column of Venus headed «occasus matutinus» follows the western horizon with an arcus visionis of 7°; "
     f"Leo {dm(ca.CORRECTED['ven_occ_mat'][4])} and Libra {dm(ca.CORRECTED['ven_occ_mat'][6])} (Theon's readings) lie "
     f"{off('ven_occ_mat', 4)} and {off('ven_occ_mat', 6)} from their computation. Of the witnesses Nallino compares "
     f"(pp. 264, 267-268) only Ḥabash differs, with 47′"),
    ("p. 143 ven_occ_mat Sagittarius (reading)", dm(ca.CORRECTED["ven_occ_mat"][8]), dm(comp("ven_occ_mat", 8)), "value",
     f"Theon, the Latin Almagest, the codex and Ḥabash have 12° 27′, the Spanish version 12° 24′ and the Alphonsine "
     f"tables 12° 77′, which Nallino takes for a misprint of 27′ (pp. 264, 266-268). The printed number, "
     f"{dm(ca.PRINTED['ven_occ_mat'][8])}, lies {off('ven_occ_mat', 8, ca.PRINTED['ven_occ_mat'][8])} from the "
     f"computation, the reading {off('ven_occ_mat', 8)}"),
    ("p. 143 mer_ort_vesp Pisces", dm(ca.PRINTED["mer_ort_vesp"][11]), dm(comp("mer_ort_vesp", 11)), "value",
     f"the column of Mercury headed «ortus vespertinus» follows the eastern horizon with an arcus visionis of 12°; "
     f"Aries {dm(ca.CORRECTED['mer_ort_vesp'][0])} and Aquarius {dm(ca.CORRECTED['mer_ort_vesp'][10])} (Theon's "
     f"reading) lie {off('mer_ort_vesp', 0)} and {off('mer_ort_vesp', 10)} from their computation. The codex, the "
     f"Spanish version, Ḥabash and the Alphonsine tables have the printed number; Theon has 35′, which Nallino marks "
     f"uncertain, and the Latin Almagest 18′, which he marks false (pp. 265, 267-268)"),
    ("p. 143 mer_ort_mat Taurus", dm(ca.PRINTED["mer_ort_mat"][1]), dm(comp("mer_ort_mat", 1)), "value",
     f"the codex and the Spanish version have the printed number; Ḥabash has 24°, the Alphonsine tables 24° 32′ and "
     f"the Latin Almagest 24°, which Nallino marks uncertain, while "
     f"he marks Theon's 21° false (pp. 265, 267-268); 24° 23′ would lie "
     f"{off('mer_ort_mat', 1, 24 * 60 + 23)} from the computation. Aries {dm(ca.CORRECTED['mer_ort_mat'][0])} and "
     f"Gemini {dm(ca.CORRECTED['mer_ort_mat'][2])} lie {off('mer_ort_mat', 0)} and {off('mer_ort_mat', 2)} from theirs"),
    ("p. 143 mer_occ_vesp Cancer", dm(ca.PRINTED["mer_occ_vesp"][3]), dm(comp("mer_occ_vesp", 3)), "value",
     f"all the witnesses Nallino compares have the printed number (pp. 265, 267-268). Gemini "
     f"{dm(ca.CORRECTED['mer_occ_vesp'][2])} and Leo {dm(ca.CORRECTED['mer_occ_vesp'][4])} lie "
     f"{off('mer_occ_vesp', 2)} and {off('mer_occ_vesp', 4)} from their computation"),
    ("p. 143 mer_occ_vesp Sagittarius (reading)", dm(ca.CORRECTED["mer_occ_vesp"][8]), dm(comp("mer_occ_vesp", 8)), "value",
     f"Theon, the Latin Almagest, the codex, the Spanish version, Ḥabash and the Alphonsine tables all have 17° "
     f"(pp. 265, 267-268). The printed {dm(ca.PRINTED['mer_occ_vesp'][8])} lies "
     f"{off('mer_occ_vesp', 8, ca.PRINTED['mer_occ_vesp'][8])} from the computation, the reading "
     f"{off('mer_occ_vesp', 8)}; Scorpius {dm(ca.CORRECTED['mer_occ_vesp'][7])} and Capricornus "
     f"{dm(ca.CORRECTED['mer_occ_vesp'][9])} lie {off('mer_occ_vesp', 7)} and {off('mer_occ_vesp', 9)} from theirs"),
]
with open(OUT, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["where", "printed", "computed", "kind", "note"])
    w.writerows(L)
print(len(L), "ledger rows")

"""Write S06/revolutions/revolutions_discrepancies.tsv: the differences found by check_revolutions.py, each confirmed on
the scan, and the numbers on which Nallino's notes give the reading of the codex (Part II pp. 295-296): his
emendation of the last numbers of Jupiter on p. 187, and the codex's numbers for the directions of the hours, which
Schiaparelli recomputed for p. 188."""
import csv, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.argv = sys.argv[:1]
import check_revolutions as cr

OUT = HERE / "revolutions_discrepancies.tsv"
inc_jup = cr.stats["jup"][0]


def line(col, n):
    return cr.dms((n * cr.stats[col][0] % 21600) / 60)


JUP = {6: ("182° 51′", "نا for يا, 51′ for 11′"), 8: ("142° 15′", "قمب يه for قفب يا, 182° 11′"),
       9: ("217° 33′", "ريز for ريب, 212°; the Spanish version 214°"), 10: ("242° 55′", "the Spanish version 15′ (يه for نه)"),
       11: ("273° 17′", "the Spanish version 40′"), 12: ("63° 38′", "صج for سج, 303°")}
L = []
for n, (codex, how) in JUP.items():
    L.append((f"p. 187 jup {n}", cr.printed[f"p. 187 jup {n}"], line("jup", n), "noted",
              f"Nallino, Part II p. 295, emends the last numbers of Jupiter: after the correct 212° 33′ of year 7 the "
              f"copyist wrote 182° 11′ again and the numbers that follow it, and left out the last two, 334° 0′ and "
              f"4° 22′. The codex and the Spanish version have {codex} here ({how}). The printed number is the "
              f"emendation; the line through the column gives {line('jup', n)}"))
L.append(("p. 187 mer_anom 6", cr.printed["p. 187 mer_anom 6"], line("mer_anom", 6), "value",
          "327 for 328: the steps from year 5 (273° 27′) and to year 7 (22° 50′) are 53° 41′ and 55° 42′; every other "
          "step of the column is 54° 41′ or 54° 42′"))
L += [(f"p. 188 altitude can {k}", cr.printed[f"p. 188 altitude can {k}"], cr.dms(cr.COMP[("can", k)][0]), "value",
       f"the altitude at the end of the {'second' if k == 2 else 'tenth'} hour of the summer solstice: hours 2 and 10 "
       f"both have 27° 1′, where the computation gives 27° 24.2′; the other ten altitudes of the day lie within 0.6′ "
       f"of it, those of the winter solstice within 2.2′") for k in (2, 10)]
CODEX = {("can", 1): "19° 36′ 32″", ("can", 2): "10° 5′ 11″", ("can", 3): "1° 18′ 35″ (the Spanish version 38′)",
         ("can", 4): "11° 21′ 31″", ("can", 5): "32° 58′ 30″ (the Spanish version 35″)", ("can", 6): "79° 36′ 4″",
         ("cap", 1): "36° 35′ 24″ (the Spanish version 37°)", ("cap", 2): "46° 28′ 35″", ("cap", 3): "54° 3′ 50″",
         ("cap", 4): "65° 29′ 57″", ("cap", 5): "77° 24′ 57″", ("cap", 6): "85° 1′ 0″"}
for (c, k), codex in CODEX.items():
    w = f"p. 188 direction {c} {k}"
    L.append((w, cr.printed[w], cr.dms(abs(cr.COMP[(c, k)][1]), True), "noted",
              f"Nallino, Part II p. 296: the codex has {codex}. The numbers of the codex are so far from the truth "
              f"that they seem supplied by another hand from other elements; the printed numbers are Schiaparelli's, "
              f"and Delambre's agree with them. Neither the codex nor the Spanish version names the quarter, which "
              f"Nallino adds in brackets"))
for c, k in (("cap", 3), ("can", 4), ("cap", 4), ("can", 5)):
    w = f"p. 188 direction {c} {k}"
    dev = cr.dev_dir[(c, k)]
    L.append((w, cr.printed[w], cr.dms(abs(cr.COMP[(c, k)][1]), True), "value",
              f"Schiaparelli's number lies {abs(dev):.0f}″ {'above' if dev > 0 else 'below'} the computation for "
              f"latitude 36° and obliquity 23° 35′, the elements of the altitudes; the other six directions of the first "
              f"five hours lie within 26″ of it"))
with open(OUT, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["where", "printed", "computed", "kind", "note"])
    w.writerows(L)
print(len(L), "ledger rows")

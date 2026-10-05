"""Write S06/syzygies/syz_discrepancies.tsv: the differences found by check_syzygies.py (pp. 29-32), each confirmed
on the scan, and the cells that Nallino emends in his notes (Part II pp. 206-209)."""
import csv

OUT = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani/S06/syzygies/syz_discrepancies.tsv"
L = [
    ("p. 30 opp 1190 anom", "155° 55′ 7″", "153° 55′ 7″", "value",
     "155 for 153: the line of the column gives 153° 55′ 7″, and so does the anomaly of p. 29 (346° 49′ 37″) less that "
     "of half a lunation (192° 54′ 30″, p. 31)"),
    ("p. 30 opp 1465 lum", "210° 5′ 7″", "240° 5′ 7″", "value",
     "210 for 240: the line of the column gives 240° 5′ 7″, and so does the longitude of p. 29 (254° 38′ 19″) less the "
     "motion in half a lunation (14° 33′ 12″, p. 31)"),
    ("p. 30 opp 1640 lat", "111° 8′ 54″", "211° 8′ 54″", "value",
     "111 for 211: the line of the column gives 211° 8′ 54.2″; the argument of latitude of p. 29 (46° 29′ 2″) less "
     "that of half a lunation (195° 20′ 7″, p. 31) gives 211° 8′ 55″"),
    ("p. 32 period25 day", "0ᵈ 57′ 13″ 5‴ 0ⁱᵛ", "0ᵈ 57′ 12″ 55‴ 0ⁱᵛ", "value",
     "309 lunations of 29;31,50,8,20 days are 9124;57,12,55,0 days, and 9125 days exceed them by 0;2,47,5, the step "
     "of the day columns of pp. 29-30 (22;14,44 at year 915, 20;48,24 at year 1690) and of the intervals of p. 31 "
     "(0;5,34,10 for 50 years); the printed value corresponds to an excess of 0;2,46,55"),
    ("p. 32 single 6 day", "24ᵈ 47′ 50″", "24ᵈ 47′ 40″", "noted",
     "Nallino, Part II p. 207: 40″ for 50″. Year 6 holds 75 lunations, and 75 × 29;31,50,8,20 - 6 × 365 = 24;47,40.4 days"),
    ("p. 32 single 11 day", "1ᵈ 9′ 29″", "1ᵈ 9′ 39″", "noted",
     "Nallino, Part II p. 207: 39″ for 29″. 136 lunations - 11 × 365 days = 1;9,38.9 days"),
    ("p. 32 single 14 day", "28ᵈ 19′ 34″", "28ᵈ 19′ 24″", "noted",
     "Nallino, Part II p. 207: 24″ for 34″. 174 lunations - 14 × 365 days = 28;19,24.2 days"),
    ("p. 32 single 19 day", "4ᵈ 41′ 13″", "4ᵈ 41′ 23″", "noted",
     "Nallino, Part II p. 207: 23″ for 13″. 235 lunations - 19 × 365 days = 4;41,22.6 days"),
    ("p. 32 eclipse_sun 191° 16′", "191° 16′", "190° 56′", "noted",
     "Nallino, Part II p. 209, asks that the solar limits here and on p. 88 be read 159° 44′-190° 56′, 0°-20° 16′ and "
     "349° 4′-360°; the printed numbers are his earlier emendation of the codex (pp. 207-209)"),
    ("p. 32 eclipse_sun 348° 44′", "348° 44′", "349° 4′", "noted",
     "Nallino, Part II p. 209 (see the entry for 191° 16′)"),
]
with open(OUT, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["where", "printed", "computed", "kind", "note"])
    w.writerows(L)
print(len(L), "ledger rows")

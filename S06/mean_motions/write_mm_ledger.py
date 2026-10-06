"""Write S06/mean_motions/mm_discrepancies.tsv: the differences found by check_mean_motions.py (pp. 19-28), each
confirmed on the scan, and the four cells that Nallino emends in his notes (Part II, p. 204)."""
import csv, os

OUT = r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani/S06/mean_motions/mm_discrepancies.tsv"
ONE_DAY = "one day's motion"
L = [
    # pp. 19-23
    ("p. 20 single 26 node", "127° 53′ 9″", "127° 53′ 21″", "value",
     "the line through the other 29 rows gives 127° 53′ 20.9″; the steps to the neighbouring rows, 18° 47′ 41″ and "
     "18° 44′ 53″, are 10″ shorter and 12″ longer than the motions in a 355- and a 354-day year (18° 47′ 51″ and "
     "18° 44′ 41″)"),
    ("identity single year 1 = dhu 'l-hijjah comm. (anom)", "305° 0′ 13″ (p. 21)", "305° 0′ 14″ (p. 20)", "identity",
     "the motion of the anomaly in one common year of 354 days is printed as 305° 0′ 14″ on p. 20 (single year 1) and "
     "305° 0′ 13″ on p. 21 (dhū ’l-ḥiǵǵah, comm.); both lie within the rounding of their own tables"),
    ("p. 22 days 10 sun", "9° 51′ 25″", "9° 51′ 24″", "noted",
     "Nallino, Part II p. 204: an error of the codex, noticed after printing; codex and translation have 25″ for 24″. "
     "The line through the table gives 9° 51′ 23.4″"),
    ("p. 22 days 21 node", "1° 6′ 45″", "1° 6′ 44″", "noted",
     "Nallino, Part II p. 204: an error of the codex, noticed after printing, 45″ for 44″. The line through the table "
     "gives 1° 6′ 44.0″"),
    ("p. 23 hours 3 sun", "0° 7′ 25″", "0° 7′ 24″", "noted",
     "Nallino, Part II p. 204: an error of the codex that passed into the translation, 25″ for 24″. The line through "
     "the table gives 0° 7′ 23.7″"),
    ("p. 23 hours 23 anom", "12° 31′ 13″", "12° 31′ 14″", "noted",
     "Nallino, Part II p. 204: an error of the codex that passed into the translation; the codex has 33″, the "
     "translation 13″, for 14″. The line through the table gives 12° 31′ 14.2″"),
    # pp. 24-28
    ("p. 24 collected 811 jup", "73° 34′", "74° 33.6′", "value",
     "the step from AH 781 (270° 46′) is 162° 48′; every other 30-year step of the column is 163° 47′ or 163° 48′"),
    ("p. 24 collected 841 jup", "237° 21′", "238° 21.4′", "value",
     "the step from AH 811 is the regular 163° 47′, so the degree missing at AH 811 carries on"),
    ("p. 24 collected 871 jup", "41° 9′", "42° 9.2′", "value",
     "the step from AH 841 is the regular 163° 48′, so the degree missing at AH 811 carries on"),
    ("p. 25 single 2 jup", "58° 51′", "58° 56.5′", "value",
     f"{ONE_DAY} (4′ 59″) less than the line: 708 days, one fewer than the 709 of the row, give 58° 51.5′; "
     "the rows after it count the day again"),
    ("p. 25 single 5 jup", "157° 19′", "147° 18.8′", "value",
     "157 for 147: the steps from year 4 (117° 48′) and to year 6 (176° 45′) are 39° 31′ and 19° 26′, for the motions "
     "in a 355- and a 354-day year, 29° 31′ and 29° 26′"),
    ("p. 25 single 7 jup", "206° 10′", "206° 15.3′", "value",
     f"{ONE_DAY} (4′ 59″) less than the line: 2,480 days, one fewer than the 2,481 of the row, give 206° 10.3′; "
     "the rows after it count the day again"),
    ("p. 25 single 10 jup", "294° 33′", "294° 37.6′", "value",
     f"{ONE_DAY} (4′ 59″) less than the line: 3,543 days, one fewer than the 3,544 of the row, give 294° 32.6′; "
     "the rows after it count the day again"),
    ("p. 25 single 2 ven", "76° 30′", "77° 6.9′", "value",
     f"{ONE_DAY} (36′ 59″) less than the line: 708 days, one fewer than the 709 of the row, give 76° 29.9′; "
     "the rows after it count the day again"),
]
IDENT = [("sat", "11° 51′", "11° 52′", "11° 51.5′", "0.5′"), ("jup", "29° 25′", "29° 26′", "29° 25.8′", "0.8′"),
         ("mars", "185° 30′", "185° 31′", "185° 31.3′", "1.3′"), ("ven", "218° 14′", "218° 15′", "218° 15.0′", "1.0′"),
         ("mer", "19° 45′", "19° 46′", "19° 46.4′", "1.4′")]
for g, p26, p25, rate354, behind in IDENT:
    L.append((f"identity single year 1 = dhu 'l-hijjah ({g})", f"{p26} (p. 26)", f"{p25} (p. 25)", "identity",
              f"the motion in one common year of 354 days; the daily motion implied by the 30-year steps of p. 24 gives "
              f"{rate354}, which p. 25 rounds to the minute, while the months of p. 26 fall progressively below it and "
              f"end {behind} lower"))
# pp. 72-77: the Roman calendar
AL = "Nallino, Part II p. 204, names this difference between the two tables and takes it to come from al-Battānī himself"
L += [
    ("p. 72 collected 1171 node", "140° 34′ 37″", "149° 34′ 36.6″", "value",
     "140 for 149: the node advances by 26° 48′ 23″ or 24″ every 20 years; the neighbouring rows are 122° 46′ 13″ (1151) "
     "and 176° 23′ 0″ (1191)"),
    ("identity p. 75 days 9 sun = p. 22", "8° 52′ 15″", "8° 52′ 16″ on p. 22", "identity", AL),
    ("identity p. 75 days 10 sun = p. 22", "9° 51′ 23″", "9° 51′ 25″ on p. 22", "identity",
     AL + "; on p. 22 Nallino corrects 25″ to 24″"),
    ("identity p. 75 days 10 anom = p. 22", "130° 38′ 59″", "130° 39′ 0″ on p. 22", "identity", AL),
    ("identity p. 75 days 21 node = p. 22", "1° 6′ 44″", "1° 6′ 45″ on p. 22", "identity",
     "p. 75 has the 44″ to which Nallino corrects the 45″ of p. 22"),
    ("identity p. 75 days 24 anom = p. 22", "313° 33′ 35″", "313° 33′ 34″ on p. 22", "identity",
     "24 days of the anomaly are 313° 33′ 34.6″; p. 75 rounds, p. 22 has 1″ less"),
    ("identity p. 76 hours 3 sun = p. 23", "0° 7′ 24″", "0° 7′ 25″ on p. 23", "identity",
     "p. 76 has the 24″ to which Nallino corrects the 25″ of p. 23"),
    ("identity p. 76 hours 10 anom = p. 23", "5° 26′ 37″", "5° 26′ 38″ on p. 23", "identity",
     AL + " (exactly 5° 26′ 37″ 28‴ 17⁗)"),
    ("identity p. 76 hours 14 moon = p. 23", "7° 41′ 11″", "7° 41′ 10″ on p. 23", "identity", AL),
    ("identity p. 76 hours 23 anom = p. 23", "12° 31′ 14″", "12° 31′ 13″ on p. 23", "identity",
     "p. 76 has the 14″ to which Nallino corrects the 13″ of p. 23"),
    # pp. 102-106
    ("p. 102 collected 1591 sat", "212° 45′", "242° 44.5′", "value",
     "212 for 242: Saturn at 1571 (358° 2′) plus the motion in 20 years under p. 103 (244° 42′ 44″ 20‴) gives "
     "242° 44′ 44″; every 20-year step of the column is 244° 42′ or 244° 43′"),
    ("identity p. 106 days 11 mer = p. 27", "34° 11′", "34° 10′ on p. 27", "identity",
     "11 days of Mercury's anomaly are 34° 10′ 25″ (3;6,24,7,… a day); p. 27 has the rounded value"),
    ("identity p. 105 hours 5 mars = p. 28", "0° 7′", "0° 6′ on p. 28", "identity",
     "5 hours of Mars are 6′ 33″; p. 105 rounds, p. 28 drops the seconds"),
    ("identity p. 105 hours 7 sat = p. 28", "0° 0′", "0° 1′ on p. 28", "identity",
     "7 hours of Saturn are 35″; p. 28 rounds, p. 105 drops the seconds"),
    ("identity p. 105 hours 12 jup = p. 28", "0° 3′", "0° 2′ on p. 28", "identity",
     "12 hours of Jupiter are 2′ 30″ (2′ 29.6″); p. 28 drops the half minute, p. 105 rounds it up"),
    ("identity p. 105 hours 18 sat = p. 28", "0° 2′", "0° 1′ on p. 28", "identity",
     "18 hours of Saturn are 1′ 30″ (1′ 30.4″); p. 105 rounds, p. 28 drops the half minute"),
]
with open(OUT, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["where", "printed", "computed", "kind", "note"])
    w.writerows(L)
print(len(L), "ledger rows")

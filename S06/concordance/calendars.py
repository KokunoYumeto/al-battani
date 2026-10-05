"""Calendar arithmetic for checking al-Battani's chronological tables (Part II pp. 7-18).
Julian day numbers (JD at noon, integer), the Julian calendar, the arithmetical Hijra calendar (30-year cycle, leap
years 2 5 7 10 13 16 18 21 24 26 29) with the astronomical epoch Thursday 15 July 622 (JD 1948439), the Seleucid
(Dhu 'l-qarnayn) year beginning on 1 October, and the Syrian month names Nallino uses.
Weekday signs: 1 = Sunday ... 7 = Saturday (al-Battani's «signa»)."""

SYRIAN = {10: "tishrīn I", 11: "tishrīn II", 12: "kānūn I", 1: "kānūn II", 2: "subāṭ", 3: "ādhār", 4: "nīsān",
          5: "ayyār", 6: "ḥazīrān", 7: "tammūz", 8: "āb", 9: "aylūl"}
HIJRA_LEAP = {2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29}
EPOCH_ASTRO = 1948439           # JD of Thursday 15 July 622 (Julian)


def jd_julian(y, m, d):
    a = (14 - m) // 12
    yy = y + 4800 - a
    mm = m + 12 * a - 3
    return d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - 32083


def julian_from_jd(jd):
    c = jd + 32082
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = d - 4800 + m // 10
    return year, month, day


def weekday_sign(jd):
    """1 = Sunday ... 7 = Saturday."""
    return (jd + 1) % 7 + 1


def hijra_year_start(n, epoch=EPOCH_ASTRO):
    """JD of the first of Muharram of Hijra year n (arithmetical calendar)."""
    k = n - 1
    cycles, rest = divmod(k, 30)
    days = cycles * 10631 + rest * 354 + sum(1 for y in range(1, rest + 1) if y in HIJRA_LEAP)
    return epoch + days


def hijra_leap(n):
    return ((n - 1) % 30) + 1 in HIJRA_LEAP


def seleucid_year(y, m):
    """Seleucid (Dhu 'l-qarnayn) year of a Julian year and month, the year beginning on 1 October."""
    return y + 312 if m >= 10 else y + 311


if __name__ == "__main__":
    for n in (1, 2, 31, 566, 567, 568, 600):
        jd = hijra_year_start(n)
        y, m, d = julian_from_jd(jd)
        print(n, weekday_sign(jd), seleucid_year(y, m), d, SYRIAN[m], (y, m, d))

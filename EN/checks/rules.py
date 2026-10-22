"""Numerical checks of the claims made in the notes of the English translation.

Each check computes the exact value with modern spherical astronomy and compares it with al-Battani's rule as the
notes state it. Run: python rules.py   (prints every case and fails on any disagreement)."""
import math

R, D = math.radians, math.degrees
EPS = R(23 + 35 / 60)  # al-Battani's inclination, 23;35


def ecl_to_eq(lon, lat):
    """right ascension and declination of the point of ecliptic longitude lon and latitude lat"""
    x = math.cos(lat) * math.cos(lon)
    y = math.cos(lat) * math.sin(lon)
    z = math.sin(lat)
    y2 = y * math.cos(EPS) - z * math.sin(EPS)
    z2 = y * math.sin(EPS) + z * math.cos(EPS)
    return math.atan2(y2, x) % (2 * math.pi), math.asin(z2)


def chapter_12():
    """the altitude of the sun on the prime vertical at latitude 36;22, the sun at the beginning of Cancer"""
    phi, delta = R(36 + 22 / 60), EPS
    exact = D(math.asin(math.sin(delta) / math.sin(phi)))
    sin_a = math.sin(delta) / math.cos(phi)              # sine of the amplitude
    h0 = R(90) - phi + delta                             # noon altitude
    rule = D(math.asin(sin_a * math.sin(h0) / (sin_a + math.cos(h0))))
    text = D(math.asin(30 * 58.5166667 / (30 + 13 + 17 / 60) / 60))  # HG = 30, KZ = 58;31, KH = 13;17
    print(f"ch. 12: HG = {60 * sin_a:.4f} parts; exact {exact:.4f}°, rule {rule:.4f}°, text's numbers {text:.4f}°")
    assert abs(exact - rule) < 1e-9 and abs(60 * sin_a - (29 + 49 / 60)) < 0.01 and abs(text - (42 + 32 / 60)) < 0.02


def chapter_18():
    """the declination of a star (second declination) and the difference of its passage through the meridian"""
    for lon_d, lat_d in [(60, 10), (30, 5), (120, -8), (200, 12), (300, -15), (80, 30)]:
        lon, lat = R(lon_d), R(lat_d)
        ra, dec = ecl_to_eq(lon, lat)
        ra_h, dec_h = ecl_to_eq(lon, 0.0)
        beta2 = math.atan(math.sin(lon) * math.tan(EPS))  # second declination of the degree
        rule_dec = math.asin(math.sin(lat + beta2) * math.cos(EPS) / math.cos(beta2))
        diff = abs(D((ra - ra_h + math.pi) % (2 * math.pi) - math.pi))
        codex = D(math.asin(math.sin(abs(lat)) * math.sin(EPS) * abs(math.cos(ra_h)) / math.cos(dec)))
        emended = D(math.asin(min(1.0, math.sin(abs(lat)) * math.sin(EPS) * abs(math.cos(ra_h))
                                   / (math.cos(dec) * math.cos(dec_h)))))
        print(f"ch. 18: L {lon_d:3}° b {lat_d:4}°: declination {D(dec):8.4f}° rule {D(rule_dec):8.4f}°;"
              f" difference {diff:.4f}° codex {codex:.4f}° emended {emended:.4f}°")
        assert abs(D(dec) - D(rule_dec)) < 1e-9 and abs(diff - codex) < 1e-9 and emended > codex


def ascension(lon, phi):
    """the ascension at latitude phi of the ecliptic point of longitude lon (right ascension less the ascensional
    difference), counted from the beginning of Aries"""
    ra, dec = ecl_to_eq(lon, 0.0)
    return (ra - math.asin(math.tan(phi) * math.tan(dec))) % (2 * math.pi)


def ascendant(lst, phi):
    """the longitude of the ecliptic point rising when the sidereal time is lst"""
    return math.atan2(math.cos(lst), -(math.sin(lst) * math.cos(EPS) + math.tan(phi) * math.sin(EPS))) % (2 * math.pi)


def chapter_24():
    """the degree culminating with a star from the degree rising or setting with it: rising, ascension + half arc;
    setting, the ascension of the counterpart of the setting degree − half arc, not that of the setting degree"""
    phi = R(36)
    for ra_d, dec_d in [(50, 20), (200, -10), (300, 15), (120, 5)]:
        ra, dec = R(ra_d), R(dec_d)
        half = math.pi / 2 + math.asin(math.tan(phi) * math.tan(dec))  # half the arc of the day of the star
        target = (ra + math.pi / 2) % (2 * math.pi)                        # right ascension counted from Capricorn
        rising = ascendant(ra - half, phi)                                 # the degree rising with the star
        setting = (ascendant(ra + half, phi) + math.pi) % (2 * math.pi)    # the degree setting with the star
        by_rising = (ascension(rising, phi) + half) % (2 * math.pi)
        by_counterpart = (ascension(setting + math.pi, phi) - half) % (2 * math.pi)
        by_setting = (ascension(setting, phi) - half) % (2 * math.pi)
        print(f"ch. 24: star {ra_d:3}° {dec_d:3}°: from Capricorn {D(target):7.3f}°; rising rule {D(by_rising):7.3f}°;"
              f" setting with the counterpart {D(by_counterpart):7.3f}°, with the setting degree {D(by_setting):7.3f}°")
        for x in (by_rising, by_counterpart):
            assert abs((x - target + math.pi) % (2 * math.pi) - math.pi) < 1e-9
        assert abs((by_setting - target + math.pi) % (2 * math.pi) - math.pi) > R(10)


def chapter_25():
    """the longitude of a star from its declination and the degree culminating with it (the variation of the star):
    the rule for the same side of the equator is close but not exact, the rule for opposite sides is far off; the
    latitude rule with the second declination is exact"""
    for lon_d, lat_d in [(60, 10), (150, 25), (300, -15), (200, 12), (45, -20)]:
        lon, lat = R(lon_d), R(lat_d)
        ra, dec = ecl_to_eq(lon, lat)
        ra_h, _ = ecl_to_eq(lon, 0.0)
        true = abs(D((ra - ra_h + math.pi) % (2 * math.pi) - math.pi))
        m_lon = math.atan2(math.sin(ra), math.cos(ra) * math.cos(EPS)) % (2 * math.pi)  # the culminating degree
        ra_m, dec_m = ecl_to_eq(m_lon, 0.0)
        sin_dist = abs(math.cos(ra_m))  # sine of its distance from the solstice, in right ascension
        longest, exceeding = 2 - math.cos(EPS), 2 - math.cos(dec_m)
        if (dec >= 0) == (dec_m >= 0):
            adj = abs(abs(dec) - abs(dec_m))
            sin_m = math.sin(EPS) / math.cos(dec_m)
            s = (sin_m * math.tan(adj) * exceeding / longest * math.cos(EPS) / math.cos(math.asin(sin_m))
                 * sin_dist)
            case = "same side"
        else:
            adj = abs(dec) + abs(dec_m)
            sin_m = math.sin(EPS) * math.sin(abs(dec)) / math.cos(adj) * math.cos(dec_m)
            dividend = sin_m * math.tan(abs(dec)) * exceeding / longest
            s = math.cos(math.asin(sin_m)) * dividend / math.cos(EPS) * sin_dist
            case = "opposite sides"
        rule = D(math.asin(min(1.0, abs(s))))
        beta2 = math.atan(math.sin(lon) * math.tan(EPS))
        lat_rule = D(math.asin(math.sin(dec) * math.cos(beta2) / math.cos(EPS)) - beta2)
        print(f"ch. 25: L {lon_d:3}° b {lat_d:4}° ({case}): variation {true:.4f}°, rule {rule:.4f}°;"
              f" latitude rule {lat_rule:.4f}°")
        assert abs(lat_rule - lat_d) < 1e-9
        if case == "same side":
            assert 0 < abs(rule - true) < 0.03 * true
        else:
            assert abs(rule - true) > 0.5 * true


def sexa(x, places=3):
    """x as degrees (or parts), minutes, seconds ..., rounded in the last place"""
    v = round(x * 60 ** (places - 1))
    out = []
    for _ in range(places - 1):
        v, r = divmod(v, 60)
        out.append(r)
    return [v] + out[::-1]


def chapter_28():
    """the equation of the sun with the radius 2;4,45: 30° from the apogee and 30° from the perigee; and the mean
    motion in 186 days 14 3/4 hours"""
    r = 2 + 4 / 60 + 45 / 3600
    near = r * math.sin(R(30))                     # 1;2,22,30
    far = 60 + r * math.cos(R(30))                 # 61;48,2
    dist = math.hypot(far, near)                   # 61;48,35
    scaled = near * 60 / dist
    arc = D(math.asin(scaled / 60))
    print(f"ch. 28: apogee side: distance {sexa(dist)}, line {sexa(scaled)}, arc {sexa(arc)}")
    assert sexa(scaled) == [1, 0, 33] and sexa(arc) == [0, 57, 49]
    far2 = 60 - r * math.cos(R(30))                # 58;11,58
    dist2 = math.hypot(far2, near)
    scaled2 = near * 60 / dist2
    arc2 = D(math.asin(scaled2 / 60))
    print(f"ch. 28: perigee side: distance {sexa(dist2)}, line {sexa(scaled2)}, arc {sexa(arc2)}")
    # the text has 1;4,17 for the line (from its rounded distance 58;12,34); the arc is the same
    assert sexa(scaled2)[:2] == [1, 4] and abs(sexa(scaled2)[2] - 17) <= 1 and sexa(arc2) == [1, 1, 24]
    year = 365 + 14 / 60 + 26 / 3600
    mean = 360 / year * (186 + 14.75 / 24)
    print(f"ch. 28: mean motion in 186 days 14 3/4 hours {sexa(mean)}")
    assert sexa(mean)[:2] == [183, 56] and abs(sexa(mean)[2] - 12) < abs(sexa(mean)[2] - 2)


def chapter_30():
    """the moon: the eccentricity, the second anomaly at the doubled elongation of 120 and the arc of the prosneusis
    at 90;30 (Ptolemy's numbers), Ptolemy's and al-Battani's distances of the sun, and the sun's parallax"""
    def sx(*v):
        return sum(x / 60 ** i for i, x in enumerate(v))
    # the eccentricity: the epicycle 5;15 seen as 8 at the nearest distance
    hf = 5.25 * 60 / 8
    print(f"ch. 30: HF {sexa(hf)}, diameter {sexa(60 + hf)}, radius {sexa((60 + hf) / 2)}, centres {sexa(60 - (60 + hf) / 2)}")
    assert sexa(hf, 2) == [39, 22] and sexa((60 + hf) / 2, 2) == [49, 41] and sexa(60 - (60 + hf) / 2, 2) == [10, 19]
    # the doubled elongation of 120: the angle ZHL of 60 on the base HZ = 10;19
    e, rad, r = sx(10, 19), sx(49, 41), sx(5, 15)
    zl = e * sx(51, 58) / 60
    ml = math.sqrt(rad ** 2 - zl ** 2)
    ml_text = math.sqrt(rad ** 2 - sx(9, 16) ** 2)
    hm = sx(48, 53) - sx(5, 10)
    mk = r * 60 / hm
    arc = D(math.asin(mk / 60))
    print(f"ch. 30: ZL {sexa(zl)}; ML {sexa(ml)} (with the text's 9;16: {sexa(ml_text)}); HM {sexa(hm)}; MK {sexa(mk)};"
          f" arc {sexa(arc)}")
    assert sexa(zl, 2) == [8, 56] and sexa(ml, 2) == [48, 52] and sexa(ml_text, 2) == [48, 49]
    assert sexa(hm, 2) == [43, 43] and sexa(mk, 2) == [7, 12] and sexa(arc, 2) == [6, 54]
    sixty_239, sixty_240 = 60 * sx(1, 53) / sx(2, 39), 60 * sx(1, 53) / sx(2, 40)
    print(f"ch. 30: 60 x 1;53 / 2;39 = {sexa(sixty_239)}, / 2;40 = {sexa(sixty_240)}; 7;40 - 5;1 = {sexa(sx(7, 40) - sx(5, 1))}")
    assert sexa(sixty_239, 2) == [42, 38] and sexa(sixty_240) == [42, 22, 30] and sexa(sx(7, 40) - sx(5, 1), 2) == [2, 39]
    # the doubled elongation of 90;30: the arc between the true and the mean farthest distance of the epicycle
    hk = e * math.sin(R(0.5))
    bk = math.sqrt(rad ** 2 - (e * math.cos(R(0.5))) ** 2)
    sb = bk - 2 * hk
    bz = math.hypot(sb, e * math.cos(R(0.5)))
    sz = e * math.cos(R(0.5)) * 60 / bz
    print(f"ch. 30: HK {sexa(hk)}, BK {sexa(bk)}, SB {sexa(sb)}, BZ {sexa(bz)}, SZ {sexa(sz)}, arc {sexa(D(math.asin(sz / 60)))};"
          f" arc of 12;32 {sexa(D(math.asin(sx(12, 32) / 60)))}")
    assert sexa(hk, 2) == [0, 5] and sexa(bk, 2) == [48, 36] and sexa(bz, 2) == [49, 30] and sexa(sz, 2) == [12, 30]
    sz_text = sx(10, 19) * 60 / sx(49, 31)  # with the text's rounded BZ
    assert sexa(sz_text, 2) == [12, 30] and sexa(D(math.asin(sx(12, 30) / 60)), 2) == [12, 1]
    assert sexa(D(math.asin(sx(12, 32) / 60)), 2) == [12, 3]
    assert 333 + 12 / 60 + 12 + 1 / 60 == 345 + 13 / 60
    # Ptolemy's distances (Almagest V 15-16)
    moon, shadow = 60 * math.sin(R(sx(0, 15, 40))), 60 * math.sin(R(sx(0, 40, 40)))
    print(f"ch. 30: sines {sexa(moon)}, {sexa(shadow)}; 1 / 0;3,11 = {1 / sx(0, 3, 11):.3f}; 64;10 / 0;3,11 ="
          f" {sx(64, 10) / sx(0, 3, 11):.1f}; cubes {5.5 ** 3}, {18.8 ** 3:.2f}, {3.4 ** 3:.2f}; 6644.5 / 39.25 ="
          f" {6644.5 / 39.25:.1f}")
    assert sexa(moon) == [0, 16, 24] and sexa(shadow) == [0, 42, 35]
    assert abs(sx(64, 10) / sx(0, 3, 11) - 1210) < 2 and abs(6644.5 / 39.25 - 170) < 1 and 5.5 ** 3 == 166.375
    sf = sx(0, 45, 38) / sx(0, 14, 22) * sx(64, 10)
    assert abs(sf - (203 + 5 / 6)) < 0.05 and round(sf + sx(64, 10)) == 268
    # al-Battani's distances
    part = sx(1, 50) / sx(5, 50)
    near = sx(64, 10) - part * sx(10, 20)
    sun = 18.8 * (60 + 29 / 30)
    print(f"ch. 30: 1;50 / 5;50 = {part:.4f} (1/3 - 1/50 = {1 / 3 - 1 / 50:.4f}); x 10;20 = {part * sx(10, 20):.3f};"
          f" moon {near:.3f} (60 29/30 = {60 + 29 / 30:.3f}); sun {sun:.1f}; shadow {sun / 4.5:.1f};"
          f" sun to moon {sun - 60 - 29 / 30:.1f}; variation {2 * sx(2, 4, 45) / 60 * 1108:.1f}")
    assert abs(part - (1 / 3 - 1 / 50)) < 0.002 and abs(near - (60 + 29 / 30)) < 0.05
    assert round(sun) == 1146 and abs(sun / 4.5 - (254 + 2 / 3)) < 0.1 and round(sun - 60 - 29 / 30) == 1085
    assert 76 <= 2 * sx(2, 4, 45) / 60 * 1108 < 77
    # the parallax of the sun from the eclipse relation: the parallaxes of the sun and the moon together equal the
    # apparent radii of the shadow and the sun together (minutes of arc)
    p_moon = D(math.asin(1 / sx(64, 10))) * 60
    p_ptolemy = 40 + 40 / 60 + 15 + 40 / 60 - p_moon
    p_battani = 38.5 + 15 + 40 / 60 - p_moon
    print(f"ch. 30: parallax of the moon {p_moon:.2f}'; of the sun with 40;40 {p_ptolemy:.2f}', with 38;30"
          f" {p_battani:.2f}' (ratio {p_ptolemy / p_battani:.2f})")
    assert 53.4 < p_moon < 53.7 and abs(p_ptolemy - 2.75) < 0.05 and abs(p_battani - 0.6) < 0.05
    assert 4.5 < p_ptolemy / p_battani < 5
    # the modern mean distance of the sun in radii of the earth, against al-Battani's mean 1108
    au = 149597870.7 / 6378.137
    print(f"ch. 30: astronomical unit {au:.0f} radii of the earth, {au / 1108:.1f} times al-Battani's mean distance")
    assert 23400 < au < 23500 and 20 < au / 1108 < 22
    # Antioch and al-Raqqa (36;9 and 39;4 east of Greenwich); the sun of 23 January 901 from its nearest distance
    assert abs(sx(39, 4) - sx(36, 9) - sx(2, 55)) < 1e-9 and abs(4 * sx(2, 55) - (11 + 2 / 3)) < 1e-9
    assert sexa((300 + sx(8, 35)) - (sx(82, 17) + 180), 2) == [46, 18]
    # the sun of 3 August 901: mean Leo 16;10 with the apogee at Gemini 22;17 gives the subtractive equation 1;34
    # and the true position 14;36 of the text
    a = R(120 + sx(16, 10) - (60 + sx(22, 17)))
    q = D(math.atan2(sx(2, 4, 45) * math.sin(a), 60 + sx(2, 4, 45) * math.cos(a)))
    print(f"ch. 30: the sun of 3 August 901: anomaly {D(a):.2f}, equation {sexa(q)}, true {sexa(sx(16, 10) - q)}")
    assert sexa(q, 2) == [1, 34] and sexa(sx(16, 10) - q, 2) == [14, 36]


def julian_day(y, m, d):
    """the day number of a date of the Julian calendar (astronomical years: 312 BC is -311)"""
    a = (14 - m) // 12
    y2, m2 = y + 4800 - a, m + 12 * a - 3
    return d + (153 * m2 + 2) // 5 + 365 * y2 + y2 // 4 - 32083


def chapter_32():
    """the eras: their first days and the days between them, the weekday rules for 1 Muharram, 1 Aylul and the
    Nayruz, and the two faulty rules (the year after a Roman leap year; Persian years to Roman ones)"""
    def weekday(j):                      # 0 Sunday ... 6 Saturday
        return (j + 1) % 7

    def cast(s):                         # «cast from Sunday»: 1 Sunday ... 7 Saturday, as a weekday 0 ... 6
        return (s % 7 or 7) - 1
    hijra, yazd = julian_day(622, 7, 15), julian_day(632, 6, 16)
    dq, copt = julian_day(-311, 9, 1), julian_day(-24, 8, 29)
    days = "Sunday Monday Tuesday Wednesday Thursday Friday Saturday".split()
    print(f"ch. 32: first days: Hijra {days[weekday(hijra)]}, Yazdajird {days[weekday(yazd)]}, Dhu l-Qarnayn"
          f" {days[weekday(dq)]}, Copts {days[weekday(copt)]}")
    assert [weekday(j) for j in (hijra, yazd, dq, copt)] == [4, 2, 6, 5]
    assert hijra - julian_day(621, 9, 1) == 317 and yazd - hijra == 3624
    assert julian_day(632, 9, 1) - yazd == 77 and abs((copt - dq) / 365.25 - 287) < 0.01
    assert cast(0 + 5) == weekday(hijra) and cast(3 * 365) == weekday(yazd)
    # 1 Aylul: the rule (fraction of the quarter dropped) against the true day, and with three quarters counted
    wrong = [n for n in range(2000) if cast((n + n // 4) * 365) != weekday(julian_day(-311 + n, 9, 1))]
    right = [n for n in range(2000) if cast((n + (n + 1) // 4) * 365) != weekday(julian_day(-311 + n, 9, 1))]
    leap = [n for n in range(2000) if (n % 4 == 2) != ((-310 + n) % 4 == 0)]
    print(f"ch. 32: 1 Aylul: the rule fails in {len(wrong)} of 2000 years, all with n % 4 = 3:"
          f" {all(n % 4 == 3 for n in wrong)}; with three quarters counted: {len(right)}; 1 September 880 is a"
          f" {days[weekday(julian_day(880, 9, 1))]}, the rule gives {days[cast((1191 + 1191 // 4) * 365)]}")
    assert len(wrong) == 500 and all(n % 4 == 3 for n in wrong) and not right and not leap
    assert weekday(julian_day(880, 9, 1)) == 4 and cast((1191 + 1191 // 4) * 365) == 3
    # the Nayruz and the Persian years (365 days)
    assert all(cast((p + 3) * 365) == weekday(yazd + 365 * p) for p in range(1500))
    # Persian years to Roman ones: the rule counts the days from 1 Aylul; the era began 77 days before it
    off = set()
    for p in range(0, 1200, 7):
        for d in (0, 40, 100, 200, 300):
            t = 365 * p + d
            true = yazd + t                                           # the date
            years, rest = divmod(t, 365.25)                           # the rule
            ruled = julian_day(-311 + 943 + int(years), 9, 1) + int(rest)
            off.add(ruled - true)
    print(f"ch. 32: Persian to Roman: the rule's date minus the true date: {sorted(off)} days")
    assert off <= {76, 77, 78}


def chapter_33():
    """the motion of the farthest distance of the sun: one degree in 66 Roman years, about 68 lunar years"""
    yearly = 3600 / 66                                   # seconds of arc a year
    lunar = 66 * 365.25 / (354 + 11 / 30)
    print(f"ch. 33: 1 degree in 66 years = {int(yearly)} seconds {round((yearly % 1) * 60)} thirds a year;"
          f" 66 Roman years = {lunar:.2f} lunar years")
    assert int(yearly) == 54 and round((yearly % 1) * 60) == 33 and round(lunar) == 68


def chapter_36_38():
    """ch. 36: the true motion equals the mean motion at the anomaly where the equation is greatest, 90 degrees and
    the greatest equation (95 for the moon at the syzygies, 92 for the sun); ch. 38: the sine of 5 degrees"""
    def equation(a, r):
        return D(math.atan2(r * math.sin(R(a)), 60 + r * math.cos(R(a))))
    for name, r, expect in (("moon", 5.25, 95), ("sun", 2 + 4 / 60 + 45 / 3600, 92)):
        best = max((equation(a / 100, r), a / 100) for a in range(0, 18001))
        print(f"ch. 36: {name}: the greatest equation {best[0]:.3f} at the anomaly {best[1]:.2f}")
        assert round(best[1]) == expect and abs(best[1] - 90 - best[0]) < 0.01
    print(f"ch. 38: 60 sin 5 = {sexa(60 * math.sin(R(5)))}")
    assert sexa(60 * math.sin(R(5))) == [5, 13, 46]


if __name__ == "__main__":
    chapter_12()
    chapter_18()
    chapter_24()
    chapter_25()
    chapter_28()
    chapter_30()
    chapter_32()
    chapter_33()
    chapter_36_38()
    print("all checks passed")

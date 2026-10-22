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


def chapter_39():
    """the parallax: the four limits and the distances; the parallax of the sun; the rules for the altitude of a degree
    of the ecliptic, the angle of latitude, the angle at the horizon (and the false rule for a northern declination
    greater than the latitude) and the angle in the middle of the sky, against direct spherical geometry"""
    sx = lambda *v: sum(x / 60 ** i for i, x in enumerate(v))  # noqa: E731
    r59 = sx(5, 15) * 59 / 60
    limits = [59 + sx(5, 10), 59 - sx(5, 10), sx(38, 43) + sx(5, 10), sx(38, 43) - sx(5, 10)]
    print(f"ch. 39: 5;15 x 59/60 = {sexa(r59)}; 39;22 x 59/60 = {sexa(sx(39, 22) * 59 / 60)}; limits"
          f" {[sexa(x, 2) for x in limits]}")
    assert sexa(r59, 2) == [5, 10] and sexa(sx(39, 22) * 59 / 60, 2) == [38, 43]
    assert [sexa(x, 2) for x in limits] == [[64, 10], [53, 50], [43, 53], [33, 33]]
    sun = [D(math.asin(1 / d)) * 60 for d in (1210, 1146, 1070)]
    print(f"ch. 39: parallax of the sun at 1210, 1146, 1070 radii: {[sexa(p / 60) for p in sun]};"
          f" 1210/1146 - 1 = 1/{1146 / 64:.1f}; 49;41 squared {sexa(sx(49, 41) ** 2)}; 1108/60 = {sexa(1108 / 60)},"
          f" 1127/60 = {sexa(1127 / 60)}")
    assert abs(sun[0] - (2 + 50.5 / 60)) < 0.1 / 60 and sexa(sun[1] / 60)[1:] == [3, 0] and sexa(sun[2] / 60)[1:] == [3, 13]
    assert round(1146 / 64) == 18 and sexa(sx(49, 41) ** 2, 2) == [2468, 26]
    assert sexa(1108 / 60, 2) == [18, 28] and sexa(1127 / 60, 2) == [18, 47]
    # the sky of a place: latitude phi, sidereal time t; vectors in the equatorial frame
    def unit(v):
        n = math.sqrt(sum(c * c for c in v))
        return [c / n for c in v]

    def dot(a, b):
        return sum(x * y for x, y in zip(a, b))

    def ecl(lon):
        return [math.cos(lon), math.sin(lon) * math.cos(EPS), math.sin(lon) * math.sin(EPS)]

    def ecl_tangent(lon):
        return [-math.sin(lon), math.cos(lon) * math.cos(EPS), math.cos(lon) * math.sin(EPS)]
    worst = {"altitude": 0.0, "angle": 0.0, "horizon": 0.0, "meridian": 0.0}
    false_rule = []
    for phi_d in (20, 36, 45):
        phi = R(phi_d)
        for t_d in range(0, 360, 15):
            t = R(t_d)
            zen = [math.cos(phi) * math.cos(t), math.cos(phi) * math.sin(t), math.sin(phi)]
            east = [-math.sin(t), math.cos(t), 0.0]
            # the ascendant: the point of the ecliptic on the horizon, on the eastern side
            a = math.atan2(-zen[0], zen[1] * math.cos(EPS) + zen[2] * math.sin(EPS))
            asc = a if dot(ecl(a), east) > 0 else a + math.pi
            mc = math.atan2(math.sin(t), math.cos(t) * math.cos(EPS))
            if dot(ecl(mc), zen) < 0:
                mc += math.pi
            d_m = math.acos(max(-1.0, min(1.0, dot(ecl(asc), ecl(mc)))))
            h_m = math.asin(dot(ecl(mc), zen))
            # the altitude of points between the ascendant and the middle of the sky
            for f in (0.2, 0.5, 0.8):
                lon = asc + (mc - asc + math.pi) % (2 * math.pi) * 0 + ((mc - asc + math.pi) % (2 * math.pi) - math.pi) * f
                d = math.acos(dot(ecl(asc), ecl(lon)))
                h = math.asin(dot(ecl(lon), zen))
                worst["altitude"] = max(worst["altitude"], abs(math.sin(h) - math.sin(d) * math.sin(h_m) / math.sin(d_m)))
                # the angle of latitude: between the ecliptic and the circle of altitude through the point
                p = ecl(lon)
                vert = unit([zz - dot(zen, p) * pp for zz, pp in zip(zen, p)])
                ang = math.acos(abs(dot(ecl_tangent(lon), vert)))
                worst["angle"] = max(worst["angle"], abs(math.cos(ang) - math.tan(h) / abs(math.tan(d))))
            # the angle of the ecliptic with the horizon at the ascendant (the angle of longitude there)
            pole = [0.0, -math.sin(EPS), math.cos(EPS)]
            alpha = math.acos(abs(dot(pole, zen)))
            dec_m = math.asin(ecl(mc)[2])
            worst["horizon"] = max(worst["horizon"], abs(math.sin(alpha) - math.cos(phi - dec_m) / math.sin(d_m)))
            # the angle in the middle of the sky
            lam = mc % math.pi
            lam = min(lam, math.pi - lam)
            p = ecl(mc)
            vert = unit([zz - dot(zen, p) * pp for zz, pp in zip(zen, p)])
            ang = math.acos(abs(dot(ecl_tangent(mc), vert)))
            if lam > R(1):
                worst["meridian"] = max(worst["meridian"],
                                        abs(math.cos(ang) - abs(math.tan(dec_m)) / math.tan(lam)))
    # the rule for a northern declination of the middle of the sky greater than the latitude, at the horizon:
    # sin(angle of latitude) = sin(declination - latitude) / sin(arc from the ascendant to the middle of the sky)
    for phi10 in range(0, 236, 5):
        phi = R(phi10 / 10)
        for t10 in range(0, 3600, 5):
            t = R(t10 / 10)
            zen = [math.cos(phi) * math.cos(t), math.cos(phi) * math.sin(t), math.sin(phi)]
            east = [-math.sin(t), math.cos(t), 0.0]
            a = math.atan2(-zen[0], zen[1] * math.cos(EPS) + zen[2] * math.sin(EPS))
            asc = a if dot(ecl(a), east) > 0 else a + math.pi
            mc = math.atan2(math.sin(t), math.cos(t) * math.cos(EPS))
            if dot(ecl(mc), zen) < 0:
                mc += math.pi
            dec_m = math.asin(ecl(mc)[2])
            if dec_m <= phi:
                continue
            d_m = math.acos(max(-1.0, min(1.0, dot(ecl(asc), ecl(mc)))))
            alpha = math.acos(abs(dot([0.0, -math.sin(EPS), math.cos(EPS)], zen)))
            rule = D(math.asin(min(1.0, math.sin(dec_m - phi) / math.sin(d_m))))
            false_rule.append(abs(90 - D(alpha) - rule))
    print(f"ch. 39: largest errors of the rules: {', '.join(f'{k} {v:.1e}' for k, v in worst.items())};"
          f" the rule for a northern declination greater than the latitude errs by up to {max(false_rule):.2f}"
          f" degrees")
    assert all(v < 1e-9 for v in worst.values()) and 0.5 < max(false_rule) < 1
    # sin p against tan p for the parallax: at the horizon and the moon at 60 radii
    p_sin, p_tan = D(math.asin(1 / 60)), D(math.atan(1 / 60))
    assert abs(p_sin - p_tan) * 3600 < 1


def chapter_40():
    """the distance of the moon from its parallax: sin(visible zenith distance) / sin(parallax) exactly; with the
    true zenith distance, sin z / sin p (the distance from the observer) and cos z added"""
    worst = 0.0
    for dist in (33.5, 45.0, 64.2):
        for z_d in range(5, 90, 5):
            z = R(z_d)
            obs = math.sqrt(dist ** 2 - 2 * dist * math.cos(z) + 1)          # from the observer to the moon
            zeta = math.pi - math.asin(dist * math.sin(z) / obs) if dist * math.cos(z) < 1 else \
                math.asin(min(1.0, dist * math.sin(z) / obs))
            p = zeta - z
            assert abs(math.sin(zeta) / math.sin(p) - dist) < 1e-9
            worst = max(worst, abs(math.sin(z) / math.sin(p) + math.cos(z) - dist) / dist)
    print(f"ch. 40: sin(zeta)/sin(p) gives the distance exactly; sin z/sin p + cos z errs by at most {worst:.1e} of it")
    assert worst < 1e-3


def chapter_41():
    """the arcs of seeing: 12 times are 4/5 hour, in which the moon gains 2/5 part; the light; the diameters of the moon
    (half a sixth, a fifth); the inverse ratio to first order; 11;21; the daily gains from the hourly motions of
    chapter 30; the moon's motion in an eighth of an hour"""
    sx = lambda *v: sum(x / 60 ** i for i, x in enumerate(v))  # noqa: E731
    gain, hours = sx(12, 11), 12 / 15
    print(f"ch. 41: 12 times = {hours} hour; gain in it {gain * hours / 24:.3f}; 12;11 - that = {sexa(gain - 0.4, 2)};"
          f" light {gain / 15:.3f} of 12")
    assert hours == 0.8 and abs(gain * hours / 24 - 0.4) < 0.01 and sexa(gain - 0.4, 2) == [11, 47]
    assert abs(gain / 15 - 0.8) < 0.02
    far, near = sx(0, 29, 30), sx(0, 35, 20)
    mean = (far + near) / 2
    print(f"ch. 41: diameters {sexa(far)}, {sexa(near)}: about the mean {(near - mean) / mean:.4f} (1/12 = {1 / 12:.4f});"
          f" greatest over least {(near - far) / far:.4f}")
    assert abs((near - mean) / mean - 1 / 12) < 0.01 and abs((near - far) / far - 1 / 5) < 0.005
    worst = 0.0
    for i in range(-40, 41):
        d = i / 20                                    # the elongation 12;11 + d, d from -2 to 2 parts
        x = d / gain
        exact, linear = sx(11, 45) * gain / (gain + d), sx(11, 45) - sx(11, 45) * x
        assert abs(exact - linear) <= sx(11, 45) * x * x / (1 - abs(x)) + 1e-12
        worst = max(worst, abs(exact - linear))
    print(f"ch. 41: 11;45 x 12;11 / (12;11 + d) against 11;45 - (d / 12;11) 11;45, |d| <= 2: differ by at most"
          f" {sexa(worst)}")
    arc = sx(11, 45) * 13 / 12 * gain / sx(13, 40)
    least, greatest = 24 * (sx(0, 30, 12) - sx(0, 2, 33)), 24 * (sx(0, 36, 10) - sx(0, 2, 23))
    print(f"ch. 41: 11;45 x 13/12 x 12;11/13;40 = {sexa(arc)}; daily gains {sexa(least)}, {sexa(greatest)};"
          f" 0;32,56 / 8 = {sexa(sx(0, 32, 56) / 8)}")
    assert sexa(arc, 2) == [11, 21] and sexa(least) == [11, 3, 36] and sexa(greatest) == [13, 30, 48]
    assert sexa(sx(0, 32, 56) / 8) == [0, 4, 7]


def chapter_42():
    """the conjunctions: 2 1/2 minutes of a day to the hour; the sun's twelfth; Schiaparelli's 20;38/70;19 against 7/24;
    the eighth of a part as a quarter of an hour; Ptolemy's 7;23 doubled; the seconds of the hourly motion; where the
    neglected correction of the anomaly matters most; the method of minutes"""
    sx = lambda *v: sum(x / 60 ** i for i, x in enumerate(v))  # noqa: E731
    assert 60 / 24 == 2.5
    sun, moon = sx(0, 59, 8, 20), sx(13, 10, 35)                       # mean daily motions
    print(f"ch. 42: moon / sun {moon / sun:.2f}; sun's motion while the moon gains 1: {sun / (moon - sun):.4f}"
          f" = 1/{(moon - sun) / sun:.1f}")
    assert 13 < moon / sun < 13.5 and abs(sun / (moon - sun) - 1 / 12) < 0.004
    k = 2 * sx(10, 19) / (60 + sx(10, 19))
    print(f"ch. 42: 20;38/70;19 = {k:.4f}; 1/6 + 1/8 = {1 / 6 + 1 / 8:.4f}; for 5 parts {sexa(5 * k, 2)};"
          f" 1;30 / 5 = {1.5 / 5}")
    assert sexa(2 * sx(10, 19), 2) == [20, 38] and round(k, 4) == 0.2934 and abs(1 / 6 + 1 / 8 - 7 / 24) < 1e-12
    assert sexa(5 * k, 2) == [1, 28] and abs(1.5 / 5 - 7 / 24) < 0.01
    gain = sx(12, 11) / 24
    print(f"ch. 42: hourly gain {sexa(gain)}; an eighth of a part in {0.125 / gain:.3f} hour; 2 x 7;23 = {sexa(2 * sx(7, 23), 2)}")
    assert sexa(gain) == [0, 30, 28] and abs(0.125 / gain - 0.25) < 0.01 and sexa(2 * sx(7, 23), 2) == [14, 46]
    per_degree = 165 * (sx(2, 39) / sx(5, 1)) * 2 / 180                  # seconds an hour for each degree of elongation
    print(f"ch. 42: correction of the hourly motion {per_degree:.3f} seconds an hour for each degree")
    assert abs(per_degree - 1) < 0.05
    r = 60 * math.sin(R(sx(5, 1)))                                    # epicycle with the greatest equation 5;1

    def eq(a):
        return D(math.atan2(r * math.sin(R(a)), 60 + r * math.cos(R(a))))
    worst = (0.0, 0.0, 0.0)
    for i in range(3600):
        a = i / 10
        shift = 7 / 24 * (2 + abs(eq(a)))              # the correction for an elongation of 2 parts plus the equation
        worst = max(worst, (abs(eq(a + shift) - eq(a)), abs(eq(a)), a))
    print(f"ch. 42: neglected correction: at most {sexa(worst[0])} of the equation, where the equation is"
          f" {sexa(worst[1], 2)} (anomaly {worst[2]})")
    assert sexa(worst[0], 2) == [0, 7] and 2.8 < worst[1] < 3.3
    for d in (8, 10.5, 12, 14.5, 16):                                  # length of the daytime in equal hours
        assert abs(d / 2 * 2.5 - 15 * d / 12) < 1e-12
    print("ch. 42: minutes from noon to sunset = times of a seasonal hour of the daytime = 1 1/4 x the daytime")


def chapter_43():
    """the eclipses of the moon: the limit of 12 parts; the diameters and their variation; 5 7/8 over 6 and 2 3/5;
    0;14,50 and 31 1/5 digits; 60/15 3/5; the motion in latitude against the gain; the eclipsed area by the text's
    rule against the exact lens, and where the rule fails"""
    sx = lambda *v: sum(x / 60 ** i for i, x in enumerate(v))  # noqa: E731
    lat12 = D(math.asin(math.sin(R(5)) * math.sin(R(12))))
    print(f"ch. 43: latitude at 12 parts from the node {sexa(lat12)}; 0;17,40 + 0;46 = {sexa(sx(0, 17, 40) + sx(0, 46))}")
    assert sexa(lat12, 2) == [1, 2] and sexa(sx(0, 17, 40) + sx(0, 46)) == [1, 3, 40]
    assert sexa(sx(0, 35, 20) - sx(0, 29, 30)) == [0, 5, 50] and sexa(sx(0, 46) - sx(0, 38, 30)) == [0, 7, 30]
    k = (6 - 1 / 8) / 6
    r_far, r_near = sx(29, 30) / sx(30, 12), sx(35, 20) / sx(36, 10)
    print(f"ch. 43: (6 - 1/8)/6 = {k:.3f}; diameter / hourly motion {r_far:.3f}, {r_near:.3f}; 92 / 35 1/3 ="
          f" {92 / sx(35, 20):.3f}, 77 / 29 1/2 = {77 / 29.5:.3f}")
    assert round(k, 3) == 0.979 and abs(r_far - k) < 0.005 and abs(r_near - k) < 0.005
    assert abs(92 / sx(35, 20) - 2.6) < 0.01 and abs(77 / 29.5 - 2.6) < 0.015 and 92 == 2 * 46 and 77 == 2 * 38.5
    d40, d30 = 12 * 77 / sx(29, 40), 12 * 77 / 29.5
    print(f"ch. 43: 2 x 0;14,50 = {sexa(2 * sx(0, 14, 50))}; 77 minutes in digits: {d40:.2f} (0;29,40), {d30:.2f}"
          f" (0;29,30); 60 / 15 3/5 = {sexa(60 / 15.6)}")
    assert sexa(2 * sx(0, 14, 50)) == [0, 29, 40] and round(d40, 2) == 31.15 and round(d30, 2) == 31.32
    assert sexa(60 / 15.6) == [3, 50, 46]
    lat_motion, gain = sx(13, 13, 46), sx(13, 10, 35) - sx(0, 59, 8, 20)
    print(f"ch. 43: motion in latitude / gain = {lat_motion / gain:.4f} (13/12 = {13 / 12:.4f})")
    assert abs(lat_motion / gain - 13 / 12) < 0.005

    def rule(a, c, b):                                 # the text's area of the eclipsed segment
        e = a + c - b
        lk = e * (2 * c - e) / (2 * b)                  # sagitta of the shadow
        ln = e - lk                                     # sagitta of the moon
        h = math.sqrt((2 * c - ln) * ln)                # half the common chord
        lv = (c - e) + lk if e < c else abs((e - c) - lk)
        arcs = c * c * R(D(math.asin(h / c))) + a * a * R(D(math.asin(h / a)))
        if (e - c) > lk:                                # chord beyond the moon's centre: larger arc, triangle added
            fixed = c * c * (math.pi - math.asin(h / c)) + h * lv + a * a * math.asin(h / a) - h * (a - lk)
            assert abs(fixed - lens(a, c, b)) < 1e-9
        return arcs - h * lv - h * (a - lk), (e - c) > lk

    def lens(a, c, b):
        return (c * c * math.acos((b * b + c * c - a * a) / (2 * b * c))
                + a * a * math.acos((b * b + a * a - c * c) / (2 * b * a))
                - 0.5 * math.sqrt((-b + c + a) * (b + c - a) * (b - c + a) * (b + c + a)))
    worst_ok, fails = 0.0, []
    for a, c in ((sx(38, 30), sx(14, 45)), (sx(46), sx(17, 40)), (40.0, 15.5)):
        for i in range(1, 60):
            e = 2 * c * i / 60                          # eclipsed part of the diameter, below the whole
            b = a + c - e
            area, deep = rule(a, c, b)
            if deep:
                fails.append(abs(area - lens(a, c, b)) / lens(a, c, b))
                assert area < lens(a, c, b)             # too little
                assert b * b < a * a - c * c + 1e-9    # the deep case is the chord beyond the moon's centre
            else:
                worst_ok = max(worst_ok, abs(area - lens(a, c, b)))
    print(f"ch. 43: the area rule is exact (error {worst_ok:.1e}) until the chord passes the centre of the moon;"
          f" beyond, it errs by {min(fails):.0%} to {max(fails):.0%} of the area")
    assert worst_ok < 1e-9 and min(fails) > 0


def chapter_44():
    """the eclipses of the sun: the parallax rules against the exact visible conjunction (and Schiaparelli's objection);
    the limits 0;34,30 and 0;30,25; 2 1/3; the circle of the sun in digits; the area rule with the sun eclipsed"""
    sx = lambda *v: sum(x / 60 ** i for i, x in enumerate(v))  # noqa: E731
    gain, moon = sx(12, 11) / 24, sx(13, 10, 35) / 24              # in parts an hour
    for amp, start, rate in ((0.95, 60, 12), (0.95, 40, 14), (0.7, 75, 10)):
        def par(t):                                     # parallax in longitude, increasing the longitude, east
            return amp * math.sin(R(start - rate * t))
        p1 = par(0.0)                                   # the true conjunction at t = 0
        t1 = -p1 / moon                                 # hours of the first parallax
        p2 = par(t1)
        t2 = -p2 / gain                                 # hours of the second parallax
        p3 = par(t2)

        def visible(t):                                 # visible moon less sun
            return gain * t + par(t)
        assert abs(visible(t2) - (p3 - p2)) < 1e-12     # the sentences Schiaparelli calls false
        motion = gain - (par(t2 - 1 / 6) - p3) * 6      # the corrected motion
        t_rule = t2 - (p3 - p2) / motion
        lo, hi = t2 - 1, t2 + 1
        for _ in range(100):
            mid = (lo + hi) / 2
            lo, hi = (lo, mid) if visible(lo) * visible(mid) <= 0 else (mid, hi)
        err_rule, err_t2 = abs(t_rule - lo) * 3600, abs(t2 - lo) * 60
        print(f"ch. 44: visible minus true at the second time = p3 - p2; rule off by {err_rule:.2f} s,"
              f" second parallax alone by {err_t2:.2f} min")
        assert err_rule < 2 and err_t2 > 0.05
    hi_lim, lo_lim = (sx(0, 33, 40) + sx(0, 35, 20)) / 2, (sx(0, 31, 20) + sx(0, 29, 30)) / 2
    print(f"ch. 44: limits {sexa(hi_lim)}, {sexa(lo_lim)}; 0;33,40 - 0;31,20 = {sexa(sx(0, 33, 40) - sx(0, 31, 20))}")
    assert sexa(hi_lim) == [0, 34, 30] and sexa(lo_lim) == [0, 30, 25] and sexa(sx(0, 33, 40) - sx(0, 31, 20)) == [0, 2, 20]
    circ = 12 * sx(3, 8, 30)
    print(f"ch. 44: 12 x 3;8,30 = {sexa(circ, 2)}, half {sexa(circ / 2, 2)}, area {sexa(circ / 2 * 6, 2)},"
          f" quarter {sexa(circ / 4)}")
    assert sexa(circ, 2) == [37, 42] and sexa(circ / 2, 2) == [18, 51] and sexa(circ / 2 * 6, 2) == [113, 6]
    assert sexa(circ / 4) == [9, 25, 30]

    def lens(a, c, b):
        return (c * c * math.acos((b * b + c * c - a * a) / (2 * b * c))
                + a * a * math.acos((b * b + a * a - c * c) / (2 * b * a))
                - 0.5 * math.sqrt((-b + c + a) * (b + c - a) * (b - c + a) * (b + c + a)))
    for r in (5.5, 6.0, 6.5):                           # radius of the moon in digits; the sun's is 6
        for i in range(1, 120):
            e = 12 * i / 120                            # digits of the eclipse
            d = r + 6 - e                               # distance of the centres
            if d <= abs(r - 6) + 1e-9:                  # the eclipse is no longer partial
                continue
            s_moon = (12 - e) * e / (2 * d)
            s_sun = e - s_moon
            h = math.sqrt((12 - s_sun) * s_sun)
            x_sun = s_moon + (6 - e)                    # from the centre of the sun to the chord
            x_moon = d - x_sun                          # from the centre of the moon to the chord
            area = (36 * math.asin(h / 6) + r * r * math.asin(h / r) - h * abs(x_sun) - h * abs(x_moon))
            if x_sun >= 0 and x_moon >= 0:
                assert abs(area - lens(6, r, d)) < 1e-9
            else:
                assert area < lens(6, r, d)
    print("ch. 44: the area rule for the sun is exact while the chord lies between the centres, too small beyond")


def chapter_46():
    """the daily motions in anomaly: Ptolemy's (Almagest IX 3) rounded to the minute"""
    sx = lambda *v: sum(x / 60 ** i for i, x in enumerate(v))  # noqa: E731
    ptolemy = {"Saturn": sx(0, 57, 7, 43, 41), "Jupiter": sx(0, 54, 9, 2, 46), "Mars": sx(0, 27, 41, 40, 19),
               "Venus": sx(0, 36, 59, 25, 53), "Mercury": sx(3, 6, 24, 6, 59)}
    text = {"Saturn": [0, 57], "Jupiter": [0, 54], "Mars": [0, 28], "Venus": [0, 37], "Mercury": [3, 6]}
    print("ch. 46: " + ", ".join(f"{k} {sexa(v, 2)}" for k, v in ptolemy.items()))
    assert all(sexa(ptolemy[k], 2) == text[k] for k in text)


def chapter_47_48():
    """the third latitudes of Venus and Mercury; the anomalies of the greatest elongations of Venus and Mercury"""
    sx = lambda *v: sum(x / 60 ** i for i, x in enumerate(v))  # noqa: E731
    assert 60 / 6 == 10 and 60 * 3 / 4 == 45
    venus, mercury = 180 - D(math.acos(sx(43, 10) / 60)), 180 - D(math.acos(sx(22, 30) / 60))
    print(f"ch. 47: a sixth and three quarters of 60 minutes: 10 and 45; ch. 48: greatest elongations at anomalies"
          f" {venus:.2f} (Venus) and {mercury:.2f} (Mercury)")
    assert round(venus) == 136 and round(mercury) == 112


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
    chapter_39()
    chapter_40()
    chapter_41()
    chapter_42()
    chapter_43()
    chapter_44()
    chapter_46()
    chapter_47_48()
    print("all checks passed")

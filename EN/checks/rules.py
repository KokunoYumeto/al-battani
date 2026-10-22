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


if __name__ == "__main__":
    chapter_12()
    chapter_18()
    chapter_24()
    chapter_25()
    print("all checks passed")

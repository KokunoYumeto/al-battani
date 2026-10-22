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


if __name__ == "__main__":
    chapter_12()
    chapter_18()
    print("all checks passed")

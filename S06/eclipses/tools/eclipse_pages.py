"""Read Part II pp. 88-91: the tables for computing eclipses.
  p. 88  the true hourly motions of the Sun and the Moon at the syzygies, for the anomaly n = 0, 6 ... 180 (and
         360 - n); a small table of increments (1-7 degrees of mean elongation: 1-7 seconds)
  p. 89  the table of correction (n = 6 ... 180): portions of the distance of the Moon (minutes, seconds), and the
         corrections for the epicycle and the eccentre (minutes); the digits of the diameters eclipsed (1-12) with the
         eclipsed area of the solar and the lunar disc (digits, minutes); the digits 0-21 with the inclinations at the
         beginning and end of a solar eclipse and of the immersion and emersion of a lunar one (degrees)
  p. 90  lunar eclipses at the greatest and the least distance: true latitude of the Moon, the arc of incidence,
         the half duration of totality, the digits eclipsed (0-21)
  p. 91  solar eclipses at the greatest and the least distance of the Moon: apparent latitude, digits, incidence
Models:
  hourly motions   Sun: v (1 - q'(n)) with tan q = e sin n / (1 + e cos n), e = 2;4,45 / 60, v = 0.98565176 / 24;
                   Moon: v_moon - q'(n) v_anom with r = 5;15 / 60 (q' = e (e + cos n) / (1 + 2 e cos n + e^2))
  portions         60 (d(0) - d(n)) / (d(0) - d(180)), d(n) = sqrt(60^2 + r^2 + 2 60 r cos n), r = 5;15
  epicycle         12 times the same fraction; eccentre: 32 (60 - rho(n)) / (60 - 39;22), rho the distance of the
                   centre of the epicycle at the double elongation n (eccentricity 10;19)
  areas            the area of the disc covered (12 digits = the whole disc), the occulting disc of the same radius
                   (Sun) or of 2;36 radii (the shadow, Moon)
  inclinations     sin = 1 - d / D (D = 12.4 for the Sun; 21.6 for the Moon); end of immersion (d >= 12):
                   sin = (3.6 - d / 6) / 1.6
  p. 90            latitude = S - d (2 r_m / 12), S = r_u + r_m (53′; 63′ 36″), r_m = 14′ 45″ (17′ 40″);
                   incidence = sqrt(S^2 - b^2) (- sqrt((r_u - r_m)^2 - b^2) when total), half duration
                   sqrt((r_u - r_m)^2 - b^2)
  p. 91            latitude = S - d (2 r_s / 12), S = 31′ (34′), r_s = 16′ 15″; incidence sqrt(S^2 - b^2)
Output: MP{pdf}{tag}.json via motion_page.run."""
import math
import motion_page as mp

E_SUN = (2 + 4 / 60 + 45 / 3600) / 60
R_EPI = 5.25 / 60
E_ECC = (10 + 19 / 60) / 60
V_SUN = 0.98565176 / 24 * 3600                       # seconds of arc per hour
V_MOON = 13.17639871 / 24 * 3600
V_ANOM = 13.06498287 / 24 * 3600


def dq(n, e):
    c = math.cos(math.radians(n))
    return e * (e + c) / (1 + 2 * e * c + e * e)


def hourly_sun(n):
    return V_SUN * (1 - dq(n, E_SUN))


def hourly_moon(n):
    return V_MOON - dq(n, R_EPI) * V_ANOM


def dist(n):
    return math.sqrt(60 ** 2 + 5.25 ** 2 + 2 * 60 * 5.25 * math.cos(math.radians(n)))


def fraction(n):
    return (dist(0) - dist(n)) / (dist(0) - dist(180))


def rho(n):
    m = math.radians(n)
    e = E_ECC
    return e * math.cos(m) + math.sqrt((1 - e) ** 2 - (e * math.sin(m)) ** 2)


def eccentre(n):
    return 32 * (1 - rho(n)) / (2 * E_ECC)


def overlap(R, r, s):
    """area of the intersection of circles of radii R, r at distance s"""
    if s >= R + r:
        return 0.0
    if s <= abs(R - r):
        return math.pi * min(R, r) ** 2
    a = R * R * math.acos((s * s + R * R - r * r) / (2 * s * R))
    b = r * r * math.acos((s * s + r * r - R * R) / (2 * s * r))
    c = 0.5 * math.sqrt((-s + R + r) * (s + R - r) * (s - R + r) * (s + R + r))
    return a + b - c


def area_digits(d, ratio):
    """digits of the disc area covered when d digits of its diameter are covered; ratio = occulting radius / radius"""
    s = 1 + ratio - d / 6
    return 12 * overlap(1, ratio, s) / math.pi


def incl(x):
    return math.degrees(math.asin(max(0.0, min(1.0, x))))


def agreed(name, tv):
    """the expected values, replaced by the reading wherever both readers give the same numbers (MP{name}.json of an
    earlier pass); used for the columns that depart from their computation by more than the reading tolerance"""
    import os, wide_kit as wk
    if not os.path.exists(wk.OUT + f"MP{name}.json"):
        return tv
    out = [list(col) for col in tv]
    for (i, gi), units in mp.agreed_units(name).items():
        if gi < len(out) and i < len(out[gi]):
            out[gi][i] = units
    return out


def lunar(d, S, rm):
    """p. 90: latitude, incidence, half duration (minutes of arc) for d digits; S = r_u + r_m"""
    ru = S - rm
    b = S - d * 2 * rm / 12
    tot = math.sqrt(max(0.0, (ru - rm) ** 2 - b * b)) if b < ru - rm else 0.0
    inc = math.sqrt(max(0.0, S * S - b * b)) - tot
    return b, inc, tot


def solar(d, S, rs=16.25):
    b = S - d * 2 * rs / 12
    return b, math.sqrt(max(0.0, S * S - b * b))


def sec(x):
    return round(x * 60)                              # minutes -> seconds


NS = list(range(0, 181, 6))
keep2 = lambda k: (lambda r: sum(c is not None for g in r["groups"] for c in g) >= k)

JOBS = {
    # p. 88: n | 360 - n | Sun ′ ″ | Moon ′ ″
    "537": lambda: mp.run(537, 284, 740, [114.3, 148.0, 181.3, 249.1, 316.4],
                          [[360 - n for n in NS], [round(hourly_sun(n)) for n in NS], [round(hourly_moon(n)) for n in NS]],
                          args=NS, nsub=[1, 2, 2], mods=[1000, 60, 60], fixed=[(0, 1)] * 3, keep=keep2(4)),
    "537s": lambda: mp.run(537, 280, 386, [367.6, 451.0, 534.8], [[n for n in range(1, 8)]], args=None,
                           nsub=[2], mods=[60], fixed=[(0, 1)], tag="s", keep=keep2(2)),
    # p. 89: n | 360 - n | portions ′ ″ | epicycle | eccentre
    "538": lambda: mp.run(538, 282, 735, [63.9, 94.0, 123.8, 168.6, 196.2, 225.1],
                          agreed("538", [[360 - n for n in NS[1:]], [round(3600 * fraction(n)) for n in NS[1:]],
                                         [round(12 * fraction(n)) for n in NS[1:]], [round(eccentre(n)) for n in NS[1:]]]),
                          args=NS[1:], nsub=[1, 2, 1, 1], mods=[1000, 61, 100, 100], fixed=[(0, 1)] * 4, keep=keep2(4)),
    # p. 89: digits 1-12 | solar area (digits, minutes) | lunar area
    "538a": lambda: mp.run(538, 380, 732, [225.1, 254.7, 302.0, 350.5],
                           agreed("538a", [[round(60 * area_digits(d, 1.035)) for d in range(1, 13)],
                                           [round(60 * area_digits(d, 2.44)) for d in range(1, 13)]]),
                           args=list(range(1, 13)), nsub=[2, 2], mods=[13, 13], fixed=[(0, 1)] * 2, tag="a",
                           keep=keep2(3)),
    # p. 89: digits 0-21 (and «compl.») | inclinations
    "538i": lambda: mp.run(538, 380, 732, [350.5, 385.9, 419.1, 452.6, 486.3],
                           agreed("538i", [[round(incl(1 - d / 12.4)) for d in DIG],
                                           [round(incl(1 - d / 21.6)) for d in DIG],
                                           [round(incl((3.6 - d / 6) / 1.6)) if 12 <= d < 21.6 else 0 for d in DIG]]),
                           args=None, nsub=[1, 1, 1], mods=[100, 100, 100], fixed=[(0, 1)] * 3, tag="i",
                           keep=keep2(3)),
}
DIG = list(range(22)) + [21.6]


def p90(pdf, rules, S, rm, tag):
    rows = [lunar(d, S, rm) for d in range(22)] + [lunar(12 * S / (2 * rm), S, rm)]
    return mp.run(pdf, 280, 716, rules, [[sec(b) for b, i, t in rows], [sec(i) for b, i, t in rows],
                                         [sec(t) for b, i, t in rows], list(range(22)) + [21]],
                  args=None, nsub=[2, 2, 2, 1], mods=[70, 70, 70, 100], fixed=[(0, 1)] * 4, tag=tag, keep=keep2(5))


def p91(pdf, rules, S, n, tag):
    rows = [solar(d, S) for d in range(n)] + [solar(12 * S / 32.5, S)]
    return mp.run(pdf, 300, 562, rules, [[sec(b) for b, i in rows], list(range(n)) + [n - 1],
                                         [sec(i) for b, i in rows]],
                  args=None, nsub=[2, 1, 2], mods=[40, 100, 40], fixed=[(0, 1)] * 3, tag=tag, keep=keep2(3))


JOBS.update({
    "539L": lambda: p90(539, [112.0, 117.0, 167.7, 218.6, 268.9, 319.7], 53.0, 14.75, "L"),
    "539R": lambda: p90(539, [329.0, 334.0, 384.8, 435.3, 486.6, 538.7], 63.6, 17 + 2 / 3, "R"),
    "540L": lambda: p91(540, [88.0, 92.8, 144.2, 195.8, 247.3], 31.0, 12, "L"),
    "540R": lambda: p91(540, [303.0, 307.6, 359.9, 410.9, 461.6], 34.0, 13, "R"),
})

if __name__ == "__main__":
    import sys
    for name in sys.argv[1:] or JOBS:
        out = JOBS[name]()
        bad = [(i + 1, r["arg"], r.get("arg_exp")) for i, r in enumerate(out["rows"]) if r.get("arg_ok") is False]
        print(name, len(out["rows"]), out["classes"], "flags", len(out["flags"]), "args off", bad[:6])
        for f in out["flags"][:40]:
            print("    ", f)

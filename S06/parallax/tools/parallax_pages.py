"""Read Part II pp. 93-94: the parallaxes of the Sun and the Moon in altitude, for the true zenith distance z = 2, 4
... 90 degrees (Nallino, Part II pp. 235-237). Columns: z; the Sun's parallax (′ ″); the Moon's parallax in the first
term (′ ″), the difference of the second and the first (′ ″), the parallax in the third term (° ′ ″), the difference of
the fourth and the third (′ ″); the sixtieths for the epicycle with its centre at the apogee and at the perigee of the
eccentre (argument: half the true anomaly) and for the eccentre (argument: the mean elongation) (′ ″).
Models:  tan p = sin pi sin z / (1 - sin pi cos z), sin pi = 1 / distance in Earth radii: the Sun 1210; the Moon
64;10, 53;50, 43;53, 33;33 (Ptolemy's four terms; the table's horizontal parallaxes are 53′ 34″, 63′ 51″, 79′ and 104′);
sixtieths 60 (d_max - d) / (d_max - d_min) for the distance of the Moon on the epicycle (radius 5;15) about a centre at
60 or at 39;22, and for the distance of the centre of the epicycle on the eccentre (eccentricity 10;19).
Output: MP{pdf}.json via motion_page.run."""
import math
import motion_page as mp
from eclipse_pages import agreed

R_EPI = 5.25
E_ECC = 10 + 19 / 60


def par(z, pi_min):
    """parallax in seconds for the horizontal parallax pi (minutes) at true zenith distance z"""
    s = math.sin(math.radians(pi_min / 60))
    zz = math.radians(z)
    return math.degrees(math.atan2(s * math.sin(zz), 1 - s * math.cos(zz))) * 3600


def pi_of(dist):
    return math.degrees(math.asin(1 / dist)) * 60


PI = {"sun": pi_of(1210), "I": pi_of(64 + 10 / 60), "II": pi_of(53 + 50 / 60), "III": 79.0, "IV": 104.0}


def epi(alpha, centre):
    d = lambda a: math.sqrt(centre ** 2 + R_EPI ** 2 + 2 * centre * R_EPI * math.cos(math.radians(a)))
    return 60 * (d(0) - d(alpha)) / (d(0) - d(180))


def ecc(eta2):
    m, e, R = math.radians(eta2), E_ECC, 60 - E_ECC
    rho = e * math.cos(m) + math.sqrt(R * R - (e * math.sin(m)) ** 2)
    return 60 * (60 - rho) / (2 * E_ECC)


def tv(zs):
    s = lambda x: round(x)
    return [[s(par(z, PI["sun"])) for z in zs],
            [s(par(z, PI["I"])) for z in zs],
            [s(par(z, PI["II"]) - par(z, PI["I"])) for z in zs],
            [s(par(z, PI["III"])) for z in zs],
            [s(par(z, PI["IV"]) - par(z, PI["III"])) for z in zs],
            [s(60 * epi(2 * z, 60)) for z in zs],
            [s(60 * epi(2 * z, 60 - 2 * E_ECC)) for z in zs],
            [s(60 * ecc(2 * z)) for z in zs]]


Z1 = list(range(2, 45, 2))
Z2 = list(range(46, 91, 2))
keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 10
JOBS = {
    "542": lambda: mp.run(542, 326, 732, [68.7, 117.2, 157.9, 205.4, 246.3, 300.4, 347.3, 394.4, 441.6, 489.5],
                          agreed("542", tv(Z1)), args=Z1, nsub=[2, 2, 2, 3, 2, 2, 2, 2],
                          mods=[60, 60, 60, 60, 60, 61, 61, 61], fixed=[(0, 1)] * 8, keep=keep),
    "543": lambda: mp.run(543, 318, 730, [111.6, 146.5, 186.2, 233.4, 274.3, 342.7, 389.5, 437.5, 484.5, 533.4],
                          agreed("543", tv(Z2)), args=Z2, nsub=[2, 2, 2, 3, 2, 2, 2, 2],
                          mods=[60, 60, 60, 60, 60, 61, 61, 61], fixed=[(0, 1)] * 8, keep=keep),
}

if __name__ == "__main__":
    import sys
    for name in sys.argv[1:] or JOBS:
        out = JOBS[name]()
        bad = [(i + 1, r["arg"], r.get("arg_exp")) for i, r in enumerate(out["rows"]) if r.get("arg_ok") is False]
        print(name, len(out["rows"]), out["classes"], "flags", len(out["flags"]), "args off", bad[:6])
        for f in out["flags"][:60]:
            print("    ", f)

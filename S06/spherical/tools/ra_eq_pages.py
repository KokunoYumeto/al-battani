"""Read Part II pp. 61-64: the right ascensions of the signs counted from the beginning of Capricorn, and the
equation of days with their nights, for every degree; three signs per page (Capricorn, Aquarius, Pisces on p. 61 ...).
Model (al-Battani's elements): obliquity 23 35', solar apogee 82 17', eccentricity giving the greatest equation of the
Sun 1 59' 10"; right ascension alpha(lambda) from the beginning of Capricorn; the equation of days = (mean longitude -
alpha), shifted so that its least value over the year is 0 (Nallino: always subtractive).
Output: p3_kit/MP{pdf}.json and contact sheets."""
import math
import motion_page as mp

EPS = math.radians(23 + 35 / 60)
APOGEE = 82 + 17 / 60
E = math.sin(math.radians(1 + 59 / 60 + 10 / 3600))


def ra(lam):
    """right ascension of longitude lam (degrees from Aries), degrees in [0, 360)"""
    l = math.radians(lam)
    return math.degrees(math.atan2(math.cos(EPS) * math.sin(l), math.cos(l))) % 360


def mean_longitude(lam):
    """mean longitude of the Sun whose true longitude is lam: v = M - q(M), q = atan(e sin M / (1 + e cos M))"""
    v = math.radians(lam - APOGEE)
    m = v
    for _ in range(20):
        q = math.atan2(E * math.sin(m), 1 + E * math.cos(m))
        m = v + q
    return (APOGEE + math.degrees(m)) % 360


def eq_raw(lam):
    d = mean_longitude(lam) - ra(lam)
    return (d + 180) % 360 - 180


MIN = min(eq_raw(x / 10) for x in range(3600))


def equation(lam):
    return eq_raw(lam) - MIN


def asc_from_capricorn(lam):
    return (ra(lam) - 270) % 360


# signs on each page: first longitude of each sign (Aries = 0)
PAGES = {510: (270, 300, 330), 511: (0, 30, 60), 512: (90, 120, 150), 513: (180, 210, 240)}

if __name__ == "__main__":
    import sys
    import p2cols
    for pdf in [int(a) for a in sys.argv[1:]] or PAGES:
        print(pdf, [round(x, 1) for x in p2cols.rules(pdf, 290, 750, maxw=8)])


RULES = {510: [72.4, 107.6, 171.5, 235.8, 299.8, 362.5, 427.8, 491.2],
         511: [115.6, 150.4, 213.7, 278.5, 343.1, 407.8, 472.1, 535.5],
         512: [71.8, 106.9, 170.5, 233.0, 298.3, 361.6, 427.3, 491.4],
         513: [116.0, 150.1, 213.2, 276.5, 342.4, 405.2, 471.0, 536.5]}


def run_page(pdf, y0=288, y1=745):
    tv = []
    for s in PAGES[pdf]:
        lams = [s + n for n in range(1, 31)]
        tv.append([round(asc_from_capricorn(l) * 60) for l in lams])
        tv.append([round(equation(l) * 60) for l in lams])
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 6      # drop fragments of the rules
    out = mp.run(pdf, y0, y1, RULES[pdf], tv, args=list(range(1, 31)), nsub=[2] * 6, mods=[360] * 6, fixed=[(0, 1)] * 6,
                 keep=keep)
    return out

"""Read Part II pp. 68-71: the oblique ascensions of every degree of the ecliptic (counted from Aries) at ar-Raqqah,
latitude 36 0', with the seasonal hours; three signs per page (Aries, Taurus, Gemini on p. 68 ...).
Output: p3_kit/MP{pdf}.json and contact sheets."""
import motion_page as mp
from oblique_pages import oblique, hour

PHI = 36.0
FIRST = {517: (0, 30, 60), 518: (90, 120, 150), 519: (180, 210, 240), 520: (270, 300, 330)}
RULES = {517: [116.4, 150.0, 213.4, 276.7, 342.8, 406.4, 471.6, 536.9],
         518: [71.0, 106.7, 169.6, 232.9, 298.3, 361.6, 426.8, 489.4],
         519: [114.4, 149.6, 212.6, 277.0, 341.2, 406.0, 470.0, 535.5],
         520: [65.5, 100.7, 164.0, 227.0, 292.7, 355.8, 421.1, 483.7]}


def run_page(pdf, y0=288, y1=750, phi=PHI):
    tv = []
    for s in FIRST[pdf]:
        lams = [s + n for n in range(1, 31)]
        tv.append([round(oblique(l, phi) * 60) for l in lams])
        tv.append([round(hour(l, phi) * 60) for l in lams])
    keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 6
    return mp.run(pdf, y0, y1, RULES[pdf], tv, args=list(range(1, 31)), nsub=[2] * 6, mods=[361] * 6, fixed=[(0, 1)] * 6,
                  keep=keep)


if __name__ == "__main__":
    for pdf in (517, 518, 519, 520):
        out = run_page(pdf)
        bad = [(i + 1, r["arg"], r["arg_exp"]) for i, r in enumerate(out["rows"]) if r.get("arg_ok") is False]
        print(pdf, len(out["rows"]), out["classes"], "flags", len(out["flags"]), "args off", bad[:5])
        for f in out["flags"]:
            print("    ", f)
        k, files = mp.sheet(pdf)
        print("    sheet", k, [f.split("\\")[-1] for f in files])

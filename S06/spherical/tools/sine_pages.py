"""Read Part II pp. 55-56 (sines for every half degree, radius 60): three sections per page, each with the arc,
its supplement (degrees, minutes) and the sine (parts, minutes, seconds). Each section is read as one table:
the arc is the argument, the supplement and the sine are matched against 180 - arc and 60 sin(arc) (the reader's
candidate within 2 units of that value). Output: p3_kit/MP{pdf}s{k}.json and contact sheets MS{pdf}s{k}_*.png"""
import math
import motion_page as mp

SECTIONS = {504: ([66.0, 102.0, 144.5, 200.6], [202.9, 242.0, 285.6, 340.8], [343.3, 383.0, 425.5, 480.5]),
            505: ([118.3, 157.0, 201.7, 257.3], [259.6, 298.0, 342.0, 397.9], [400.3, 439.0, 482.8, 540.5])}
FIRST = {504: 0.0, 505: 45.0}


def expected(theta):
    supp = round((180 - theta) * 60)
    sine = round(60 * math.sin(math.radians(theta)) * 3600)
    return supp, sine


if __name__ == "__main__":
    for pdf, secs in SECTIONS.items():
        for k, rules in enumerate(secs):
            thetas = [FIRST[pdf] + 15 * k + 0.5 * (i + 1) for i in range(30)]
            ex = [expected(t) for t in thetas]
            args = [f"{int(t)}{int(round((t % 1) * 60))}" for t in thetas]
            out = mp.run(pdf, 288, 752, rules, [[e[0] for e in ex], [e[1] for e in ex]], args=args, nsub=[2, 3],
                         tag=f"s{k}", mods=[360, 61], fixed=[(0, 1), (0, 1)])
            bad = [(i + 1, r["arg"], r["arg_exp"]) for i, r in enumerate(out["rows"]) if r.get("arg_ok") is False]
            print(pdf, k, len(out["rows"]), out["classes"], "flags", len(out["flags"]), "args off", len(bad))
            for f in out["flags"]:
                print("    ", f)
            n, files = mp.sheet(pdf, f"s{k}")
            print("    sheet", n, [f.split("\\")[-1] for f in files])

"""Read Part II p. 59 (half the increase of the longest day for each latitude, 0 30' ... 60 0') and p. 60 (the
shadow of a gnomon of 12 digits for each altitude 1 ... 90): three sections per page; the argument column is the
latitude or altitude, the value column (degrees or digits, minutes) is matched against its computed value:
  p. 59  arcsin(tan phi tan eps), eps = 23 35'      p. 60  12 cot h
Output: p3_kit/MP{pdf}s{k}.json and contact sheets."""
import math
import motion_page as mp

EPS = math.radians(23 + 35 / 60)
SECTIONS = {508: ([74.8, 145.0, 214.2], [216.0, 285.0, 354.5], [356.4, 425.8, 494.5]),
            509: ([111.2, 167.6, 249.4], [251.8, 307.8, 389.8], [392.0, 447.8, 533.6])}
BAND = {508: (268, 760), 509: (278, 745)}


def half_increment(phi):
    return math.degrees(math.asin(math.tan(math.radians(phi)) * math.tan(EPS)))


def shadow(h):
    return 0.0 if h == 90 else 12 / math.tan(math.radians(h))


if __name__ == "__main__":
    for pdf, secs in SECTIONS.items():
        for k, rules in enumerate(secs):
            if pdf == 508:
                args = [20 * k + 0.5 * (i + 1) for i in range(40)]
                exp = [round(half_increment(a) * 60) for a in args]
                argtxt = [f"{int(a)}{int(round(a % 1 * 60))}" for a in args]
                mod = 360
            else:
                args = [30 * k + i + 1 for i in range(30)]
                exp = [round(shadow(a) * 60) for a in args]
                argtxt = [str(a) for a in args]
                mod = 1000
            out = mp.run(pdf, *BAND[pdf], rules, [exp], args=argtxt, nsub=[2], tag=f"s{k}", mods=[mod], fixed=[(0, 1)])
            bad = [(i + 1, r["arg"], r["arg_exp"]) for i, r in enumerate(out["rows"]) if r.get("arg_ok") is False]
            print(pdf, k, len(out["rows"]), out["classes"], "flags", len(out["flags"]), "args off", bad[:6])
            for f in out["flags"]:
                print("    ", f)
            n, files = mp.sheet(pdf, f"s{k}")
            print("    sheet", n, [f.split("\\")[-1] for f in files])

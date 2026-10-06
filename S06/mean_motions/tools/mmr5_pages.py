"""Read Part II pp. 102-106: the mean motions of Saturn, Jupiter and Mars (longitude) and the anomalies of Venus and
Mercury in the Roman (Julian) calendar, in degrees and minutes: collected years 931, 951 ... (p. 102), single years 1-20
and the sums of 40 ... 600 years (p. 103), the months from adhar (March) to subat (February, common and leap; p. 104),
hours 1-24 (p. 105), days 1-30 (p. 106). Each column is a + b t with t in days; the daily motions are those fitted to
pp. 24-28. Output: p3_kit/MP{pdf}{tag}.json."""
import motion_page as mp

# degrees per day: the motions in 20 Roman years (7305 days) printed under the single years on p. 103, whole
# revolutions included (Saturn 244 42 44 20, Jupiter 1 rev. + 247 17 34 26, Mars 10 rev. + 228 22 10 49, Venus
# 12 rev. + 183 43 2, Mercury 63 rev. + 14 27 43 20)
def _sx(d, m, s, t=0):
    return d + m / 60 + s / 3600 + t / 216000


RATE = [_sx(244, 42, 44, 20) / 7305, (360 + _sx(247, 17, 34, 26)) / 7305, (3600 + _sx(228, 22, 10, 49)) / 7305,
        (4320 + _sx(183, 43, 2)) / 7305, (22680 + _sx(14, 27, 43, 20)) / 7305]
MONTHS = [31, 61, 92, 122, 153, 184, 214, 245, 275, 306, 337, 365, 366]
SUMS = [40, 60, 80, 100, 200, 400, 600]
keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 7


def fixed_run(pdf, rules, y0, y1, t, args, tag=""):
    tv = [[x * r * 60 for x in t] for r in RATE]                         # minutes of arc
    return mp.run(pdf, y0, y1, rules, tv, args=args, nsub=2, fixed=[(0, 1)] * 5, keep=keep, tag=tag,
                  mods=[360] * 5)


JOBS = {
    "551": lambda: mp.run(551, 290, 742, [109.6, 147.3, 223.2, 299.2, 375.5, 452.2, 529.9], list(range(34)),
                          args=[931 + 20 * k for k in range(34)], nsub=2, rates=[7305 * r * 60 for r in RATE], keep=keep),
    "552": lambda: fixed_run(552, [62.6, 102.6, 179.2, 255.6, 331.4, 408.2, 484.8], 292, 566,
                             [365 * n + n // 4 for n in range(1, 21)], list(range(1, 21))),
    "552s": lambda: fixed_run(552, [62.6, 102.6, 179.2, 255.6, 331.4, 408.2, 484.8], 645, 742,
                              [365.25 * n for n in SUMS], SUMS, tag="s"),
    "553": lambda: fixed_run(553, [113.5, 212.8, 277.1, 341.4, 405.8, 469.9, 535.0], 305, 676, MONTHS, None),
    "554": lambda: fixed_run(554, [65.8, 104.2, 180.2, 257.1, 332.8, 409.0, 485.0], 298, 740,
                             [h / 24 for h in range(1, 25)], list(range(1, 25))),
    "555": lambda: fixed_run(555, [113.0, 150.9, 227.1, 302.9, 379.4, 455.4, 535.0], 290, 742,
                             list(range(1, 31)), list(range(1, 31))),
}

if __name__ == "__main__":
    import sys
    for name in sys.argv[1:] or JOBS:
        out = JOBS[name]()
        bad = [(i + 1, r["arg"], r.get("arg_exp")) for i, r in enumerate(out["rows"]) if r.get("arg_ok") is False]
        print(name, len(out["rows"]), out["classes"], "flags", len(out["flags"]), "args off", bad[:6])
        for f in out["flags"][:30]:
            print("    ", f)

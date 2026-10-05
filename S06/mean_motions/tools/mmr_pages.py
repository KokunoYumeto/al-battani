"""Read Part II pp. 72-77: mean motions of the Sun, the Moon, the lunar anomaly and the node in the Roman (Julian)
calendar: collected years 931, 951 ... 1631 (p. 72), single years 1-20 (p. 73), the months from adhar (March) to
subat (February, common and leap; p. 74), days 1-30 (p. 75), hours 1-24 (p. 76), intervals of 20 ... 600 years (p. 77).
Each column is a + b t with t in days; the fit takes the daily motions as rates. Output: p3_kit/MP{pdf}.json."""
import motion_page as mp

# al-Battani's daily motions, as fitted to his collected Arab years (pp. 19-23), in seconds per day
RATE = [0.98565176 * 3600, 13.17639871 * 3600, 13.06498287 * 3600, 0.05295093 * 3600]
MONTHS = [31, 61, 92, 122, 153, 184, 214, 245, 275, 306, 337, 365, 366]
YEARS77 = [20, 40, 60, 80, 100, 200, 300, 400, 500, 600]
PAGES = {
    521: ([118.6, 167.4, 260.4, 353.9, 447.2, 540.7], 284, 742, list(range(36)), [931 + 20 * k for k in range(36)], 7305),
    522: ([69.4, 119.8, 212.8, 305.6, 398.9, 490.7], 312, 765, [365 * n + n // 4 for n in range(1, 21)], list(range(1, 21)), 1),
    523: ([111.5, 210.8, 291.6, 371.8, 452.3, 532.7], 308, 676, MONTHS, None, 1),
    524: ([69.2, 119.4, 212.5, 305.5, 398.0, 492.1], 284, 742, list(range(1, 31)), list(range(1, 31)), 1),
    525: ([113.0, 161.2, 254.6, 348.1, 441.2, 535.6], 290, 733, [h / 24 for h in range(1, 25)], list(range(1, 25)), 1),
    526: ([67.0, 115.9, 209.3, 301.9, 394.3, 485.3], 320, 560, [365.25 * n for n in YEARS77], YEARS77, 1),
}

if __name__ == "__main__":
    import sys
    for pdf in [int(a) for a in sys.argv[1:]] or PAGES:
        rules, y0, y1, tv, args, scale = PAGES[pdf]
        keep = lambda r: sum(c is not None for g in r["groups"] for c in g) >= 9    # drop stray fragments
        rates = None if pdf == 521 else [r * scale for r in RATE]                       # p. 72: the median step
        out = mp.run(pdf, y0, y1, rules, tv, args=args, nsub=3, rates=rates, keep=keep)
        bad = [(i + 1, r["arg"], r["arg_exp"]) for i, r in enumerate(out["rows"]) if r.get("arg_ok") is False]
        print(pdf, len(out["rows"]), out["classes"], "flags", len(out["flags"]), "args off", bad[:5])
        for f in out["flags"][:20]:
            print("    ", f)
        k, files = mp.sheet(pdf)
        print("    sheet", k, [f.split("\\")[-1] for f in files])

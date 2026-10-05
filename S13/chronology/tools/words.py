"""Word boxes of one text line (gaps in the vertical ink projection), right to left, master copy.
Usage: python words.py PDF x0 x1 baseline [gap_pt]   prints  index: x0-x1  for each word (ink from baseline-14 to +5 pt)."""
import sys
import numpy as np
import fitz
import wide_kit as wk

n = int(sys.argv[1]); x0, x1, b = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
gap = float(sys.argv[5]) if len(sys.argv) > 5 else 2.2
dpi = 600; s = 72 / dpi
a = np.array(wk.gray(wk.doc[n - 1], dpi, fitz.Rect(x0, b - 6, x1, b + 2))) < 128    # the letter bodies only
on = a.sum(0) > 0
words, i = [], 0
while i < len(on):
    if on[i]:
        j = i; last = i
        while j < len(on) and (on[j] or (j - last) * s < gap):
            if on[j]:
                last = j
            j += 1
        words.append((x0 + i * s, x0 + (last + 1) * s)); i = j
    else:
        i += 1
words.reverse()
print("  ".join(f"{k}:{a_:.1f}-{b_:.1f}" for k, (a_, b_) in enumerate(words, 1)))

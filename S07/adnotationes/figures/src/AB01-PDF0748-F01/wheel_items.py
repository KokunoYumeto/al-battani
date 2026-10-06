"""Measure the printed labels of the astrological wheel (Nallino Part II p. 299, master PDF page 748). For each sector
and ring the ink is turned upright (see wheel_sector.py), the circles, the dashed circle and the sector lines are
masked out, specks are dropped, and the glyphs are clustered into words (boxes less than GAP pt apart along the line
and overlapping across it). Each word is reported with its box and the median lower edge of its glyphs (the
baseline) in pt, in polar terms: for every word the angle (deg, counterclockwise from the sector's middle line) and
the distance from the centre of the point where the word begins on its baseline, and the angle and distance of the
word's centre. Output: wheel_items.json beside this script and a printed summary. Needs the master PDF of the
edition through the working kit wide_kit (not in the repository)."""
import json, math, sys
from pathlib import Path
import numpy as np
import fitz
from PIL import Image
from scipy import ndimage
sys.path.insert(0, r"F:/user/Documents/Papors/Chatnotes/CHat translates and clean/al-battani/_intake/tables")
import wide_kit as wk

CX, CY = 266.5, 457.15
DPI = 600
S = DPI / 72
GAP = 2.0
RINGS = {  # name: (mode, rin, rout, extra circles to mask)
    "sign": ("t", 193.5, 214.0, []),
    "terms": ("r", 146.95, 193.5, []),
    "trip": ("t", 109.25, 146.95, [127.7]),
    "faces": ("r", 71.5, 109.25, []),
    "domic": ("t", 55.85, 71.5, []),
    "exalt": ("t", 40.3, 55.85, []),
}

page = wk.doc[747]
X0, Y0 = CX - 222, CY - 222
base_im = wk.gray(page, DPI, fitz.Rect(X0, Y0, CX + 222, CY + 222))
C = ((CX - X0) * S, (CY - Y0) * S)


def merge_words(boxes, mode):
    """boxes: [x0, x1, y0, y1, bottom] in the upright frame (px); merge into words"""
    words = [[b] for b in boxes]
    changed = True
    while changed:
        changed = False
        for i in range(len(words)):
            for j in range(i + 1, len(words)):
                a, b = words[i], words[j]
                ax0, ax1 = min(q[0] for q in a), max(q[1] for q in a)
                ay0, ay1 = min(q[2] for q in a), max(q[3] for q in a)
                bx0, bx1 = min(q[0] for q in b), max(q[1] for q in b)
                by0, by1 = min(q[2] for q in b), max(q[3] for q in b)
                gx = max(bx0 - ax1, ax0 - bx1) / S
                ov = min(ay1, by1) - max(ay0, by0)
                if gx < GAP and ov > -0.5 * S:
                    words[i] = a + b
                    del words[j]
                    changed = True
                    break
            if changed:
                break
    return words


items = []
for sec in range(12):
    th = 105 + 30 * sec
    for ring, (mode, rin, rout, extra) in RINGS.items():
        rot = base_im.rotate(-(th + 180) if mode == "r" else -(th - 90), resample=Image.BICUBIC, center=C,
                             fillcolor=255)
        a = np.array(rot) < 128
        H, W = a.shape
        yy, xx = np.mgrid[0:H, 0:W]
        dx = (xx - C[0]) / S
        dy = (yy - C[1]) / S
        r = np.hypot(dx, dy)
        ang = np.degrees(np.arctan2(dy, -dx)) if mode == "r" else np.degrees(np.arctan2(dx, -dy))
        keep = (r > rin + 1.9) & (r < rout - 1.9)
        for e in extra:
            keep &= np.abs(r - e) > 1.8
        lim = 15 - np.degrees(np.arcsin(np.clip(2.2 / np.maximum(r, 1), 0, 1)))
        keep &= np.abs(ang) < (lim if ring != "sign" else 15)
        lab, n = ndimage.label(a & keep)
        boxes = []
        for k, sl in enumerate(ndimage.find_objects(lab), 1):
            if sl is None:
                continue
            if (lab[sl] == k).sum() < 40:  # specks
                continue
            boxes.append([sl[1].start, sl[1].stop, sl[0].start, sl[0].stop, sl[0].stop])
        for wd in merge_words(boxes, mode):
            x0 = min(q[0] for q in wd); x1 = max(q[1] for q in wd)
            y0 = min(q[2] for q in wd); y1 = max(q[3] for q in wd)
            base = float(np.median([q[4] for q in wd]))
            # upright frame -> the frame of the sector: u along the middle line outwards, v across it (ccw positive)
            if mode == "r":  # x to the left is outwards; y down is counterclockwise
                def uv(px, py):
                    return (C[0] - px) / S, (py - C[1]) / S
            else:  # y up is outwards; x to the right is clockwise
                def uv(px, py):
                    return (C[1] - py) / S, -(px - C[0]) / S
            if mode == "r":
                su, sv = uv(x0, base)  # the word begins at its outer end
            else:
                su, sv = uv(x0, base)  # the word begins at its left end
            cu, cv = uv((x0 + x1) / 2, (y0 + y1) / 2)
            items.append({"sector": sec, "ring": ring,
                          "start_ang": round(math.degrees(math.atan2(sv, su)), 2), "start_r": round(math.hypot(su, sv), 2),
                          "cen_ang": round(math.degrees(math.atan2(cv, cu)), 2), "cen_r": round(math.hypot(cu, cv), 2),
                          "w": round((x1 - x0) / S, 2), "h": round((y1 - y0) / S, 2)})
json.dump(items, open(Path(__file__).with_name("wheel_items.json"), "w", encoding="utf-8"), indent=0)
for sec in range(12):
    for ring in RINGS:
        its = [i for i in items if i["sector"] == sec and i["ring"] == ring]
        its.sort(key=lambda i: (i["cen_ang"], -i["cen_r"]) if RINGS[ring][0] == "r" else (-i["cen_r"], -i["cen_ang"]))
        print(f"{sec:2d} {ring:5s} " + " | ".join(
            f"s({i['start_ang']},{i['start_r']}) c({i['cen_ang']},{i['cen_r']}) {i['w']}x{i['h']}" for i in its))

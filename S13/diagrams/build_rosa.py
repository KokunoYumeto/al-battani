"""Write the TSV data of the astrological figure («rosa astrologica») from the reading files in rows/:
  rosa_p3.tsv  Part III p. 244 (the codex figure, Arabic)
  rosa_p2.tsv  Part II p. 299 (Nallino's emended Latin figure)
Columns: kind (header, title, closing, footnote, sign, term, trip, face, ring1, house, exalt), sign, idx (term 1-5,
face 1-3; for trip 1 = by day / outer, 2 = by night / inner), t (angle in degrees counterclockwise from the right-hand
horizontal of the page), planet (the planet as printed: an Arabic name, a Latin name or a symbol), value (degrees as
printed: abjad letters, the zero sign {0}, or Latin «6°»), text (the printed text of the item), doubt."""
import csv, importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLS = ["kind", "sign", "idx", "t", "planet", "value", "text", "doubt"]


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / "rows" / f"{name}.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def rows(m, arabic):
    out = []
    for side, text in m.HEADER.items():
        out.append({"kind": "header", "idx": side, "text": text, "doubt": getattr(m, "HEADER_DOUBT", "") if side == "page" else ""})
    out.append({"kind": "title", "text": m.TITLE, "doubt": getattr(m, "TITLE_DOUBT", "")})
    out.append({"kind": "closing", "text": m.CLOSING, "doubt": getattr(m, "CLOSING_DOUBT", "")})
    for n, text in m.FOOTNOTES:
        out.append({"kind": "footnote", "idx": n, "text": text})
    for t, text in m.SIGN_LABELS:
        out.append({"kind": "sign", "t": f"{t:g}", "text": text, "doubt": getattr(m, "SIGN_DOUBT", {}).get(text, "")})
    for s in m.SIGNS:
        for i, (t, planet, value) in enumerate(m.TERMS[s], 1):
            out.append({"kind": "term", "sign": s, "idx": i, "t": f"{t:g}", "planet": planet, "value": value,
                        "doubt": m.TERM_DOUBT.get((s, i), "")})
        for i, text in enumerate(m.TRIPLICITIES[s], 1):
            out.append({"kind": "trip", "sign": s, "idx": i, "text": text})
        for i, (t, planet) in enumerate(m.FACES[s], 1):
            out.append({"kind": "face", "sign": s, "idx": i, "t": f"{t:g}", "planet": planet,
                        "doubt": m.FACE_DOUBT.get((s, i), "")})
        if arabic:
            text, house, planet, value = m.RING1[s]
            out.append({"kind": "ring1", "sign": s, "text": text, "doubt": m.RING1_DOUBT.get(s, "")})
            out.append({"kind": "house", "sign": s, "planet": house})
            out.append({"kind": "exalt", "sign": s, "planet": planet, "value": value})
        else:
            out.append({"kind": "house", "sign": s, "planet": m.HOUSES[s]})
            planet, value = m.EXALTATIONS[s]
            out.append({"kind": "exalt", "sign": s, "planet": planet, "value": value, "doubt": m.EXALT_DOUBT.get(s, "")})
    return out


def write(name, data):
    with open(HERE / name, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in data:
            w.writerow({c: r.get(c, "") for c in COLS})
    print(name, len(data))


if __name__ == "__main__":
    write("rosa_p3.tsv", rows(load("rosa_p3"), True))
    write("rosa_p2.tsv", rows(load("rosa_p2"), False))

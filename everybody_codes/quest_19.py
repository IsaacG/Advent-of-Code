"""Everyone Codes Day N."""

import functools
import logging
import itertools

log = logging.info

OFFSETS = [
    complex(-1, -1), complex(0, -1), complex(1, -1), complex(1,  0),
    complex( 1,  1), complex(0,  1), complex(-1,  1), complex(-1,  0),
]
ROTATE = {
    "R": OFFSETS[1:] + OFFSETS[:1],
    "L": OFFSETS[-1:] + OFFSETS[:-1],
}

def solve(part: int, data: str, testing) -> int:
    """Solve the parts."""
    key, text = data.split("\n\n")
    lines = text.splitlines()
    max_x, max_y = len(lines[0]) - 1, len(lines) - 1

    # Populate a map with coordinates. Rotate everything once. Reverse the map to get a from-to translation.
    # This tells us where a rune (starting position) moves to after one round.
    log("Start")
    translation = {
        complex(x, y): complex(x, y)
        for y, line in enumerate(lines)
        for x, char in enumerate(line)
    }
    directions = itertools.cycle(key)
    for y in range(1, max_y):
        for x in range(1, max_x):
            pos = complex(x, y)
            rot_dir = next(directions)
            chars = [translation[pos + i] for i in OFFSETS]
            for i, char in zip(ROTATE[rot_dir], chars):
                translation[pos + i] = char
    translation = {v: k for k, v in translation.items()}
    log("Translated")

    vals = {
        complex(x, y): char
        for y, line in enumerate(lines)
        for x, char in enumerate(line)
    }
    if testing:
        vals = {k: v for k, v in vals.items() if v.isalnum() or v in "><"}
    else:
        vals = {k: v for k, v in vals.items() if v.isdigit() or v in "><"}
    steps = {1: 1, 2: 100, 3: 1048576000}[part]
    dest = {}
    for pos, char in vals.items():
        step = 0
        seen = {pos}
        while step < steps:
            step += 1
            pos = translation[pos]
            if pos in seen:
                cycle = len(seen)
                log(f"Found {cycle=}")
                mult = (steps - step) // cycle
                step += cycle * mult
                break
            seen.add(pos)
        while step < steps:
            step += 1
            pos = translation[pos]
        dest[pos] = char
        log(f"Done {len(dest)}/{len(vals)}")
            
    for py in range(max_y + 1):
        line = []
        for px in range(max_x + 1):
            line.append(dest.get(complex(px, py), " "))
        print("".join(line))
    log("Done")



TEST_DATA = [
    """\
LR

>-IN-
-----
W---<""",
    """\
RRLL

A.VI..>...T
.CC...<...O
.....EIB.R.
.DHB...YF..
.....F..G..
D.H........""",
]
TESTS = [
    (1, TEST_DATA[0], "WIN"),
    (2, TEST_DATA[1], "VICTORY"),
    # (3, TEST_DATA[2], None),
]

"""Everyone Codes Day N."""

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

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    key, text = data.split("\n\n")
    lines = text.splitlines()
    max_x, max_y = len(lines[0]) - 1, len(lines) - 1
    vals = {
        complex(x, y): char
        for y, line in enumerate(lines)
        for x, char in enumerate(line)
    }
    matters = "><0123456789"

    for _ in itertools.count():
        directions = itertools.cycle(key)
        for y in range(1, max_y):
            for x in range(1, max_x):
                pos = complex(x, y)
                rot_dir = next(directions)
                chars = [vals[pos + i] for i in OFFSETS]
                for i, char in zip(ROTATE[rot_dir], chars):
                    vals[pos + i] = char

        for py in range(max_y + 1):
            line = []
            for px in range(max_x + 1):
                line.append(vals[complex(px, py)])
            if ">" in line and "<" in line:
                part = line[line.index(">") + 1:line.index("<")]
                print("".join(part))
                if part and "." not in part:
                    return "".join(part)



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

"""Everyone Codes Day N."""

import itertools
import logging
import string

log = logging.info

OFFSETS = [
    complex(-1, -1), complex(0, -1), complex( 1, -1), complex( 1, 0),
    complex( 1,  1), complex(0,  1), complex(-1,  1), complex(-1, 0),
]
ROTATE = {
    "R": OFFSETS[1:] + OFFSETS[:1],
    "L": OFFSETS[-1:] + OFFSETS[:-1],
}


def parse_lines(lines: list[str], testing: bool) -> dict[complex, str]:
    """Parse the input lines."""
    want = "><" + string.digits + (string.ascii_letters if testing else "")
    return {
        complex(x, y): char
        for y, line in enumerate(lines)
        for x, char in enumerate(line)
        if char in want
    }


def make_translation(max_x: int, max_y: int, key: str) -> dict[complex, complex]:
    """Compute the position translation after one pass."""
    translation = {
        complex(x, y): complex(x, y)
        for y in range(max_y + 1)
        for x in range(max_x + 1)
    }
    directions = itertools.cycle(key)
    for y in range(1, max_y):
        for x in range(1, max_x):
            pos = complex(x, y)
            rot_dir = next(directions)
            chars = [translation[pos + i] for i in OFFSETS]
            for i, char in zip(ROTATE[rot_dir], chars):
                translation[pos + i] = char
    return {v: k for k, v in translation.items()}


def translate(position: complex, translation: dict[complex, complex], steps: int) -> complex:
    """Translate a position n steps with cycle detection."""
    step = 0
    seen = {position}
    positions = [position]
    while step < steps:
        step += 1
        position = translation[position]
        if position in seen:
            logging.debug("Found cycle %d", len(seen))
            offset = (steps - step) % len(seen)
            return positions[offset]
        seen.add(position)
        positions.append(position)
    # No cycle, explored all the steps. Use the last position.
    return position


def extract_string(max_x: int, max_y: int, final_position: dict[complex, str]) -> str:
    """Extract the string from the final data."""
    for y in range(max_y + 1):
        line = []
        for x in range(max_x + 1):
            line.append(final_position.get(complex(x, y), " "))
        if ">" in line and "<" in line:
            log("Done")
            return "".join(line[line.index(">") + 1:line.index("<")])
    raise RuntimeError("No solution found.")


def solve(part: int, data: str, testing: bool) -> str:
    """Solve the parts."""
    key, text = data.split("\n\n")
    lines = text.splitlines()
    max_x, max_y = len(lines[0]) - 1, len(lines) - 1
    steps = {1: 1, 2: 100, 3: 1048576000}[part]

    # Populate a map with coordinates. Rotate everything once. Reverse the map to get a from-to translation.
    # This tells us where a rune (starting position) moves to after one round.
    log("Start")
    translation = make_translation(max_x, max_y, key)
    log("Translated")

    # Data we care about.
    # Make part 3 faster by dropping parts of the data.
    vals = parse_lines(lines, testing)

    # For each character, do cycle detection to efficiently compute where it eventually lands.
    # Track both seen and positions. Sets are much faster for membership checks. The list is used to get prior steps.
    final_position = {
        translate(position, translation, steps): char
        for position, char in vals.items()
    }
    log("Deciphered")
    # Read each line and look for ">..data..<".
    return extract_string(max_x, max_y, final_position)


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

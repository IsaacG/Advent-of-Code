"""Everyone Codes Day Three."""

from lib import helpers, parsers


def solve(part: int, helpers.Map: str) -> int:
    """Solve puzzle."""
    pos = data.coords["#"]
    remove = 0
    offsets = [1j ** i for i in range(4)]
    if part == 3:
        offsets.extend(complex(1, 1) * 1j ** i for i in range(4))
    while pos:
        remove += len(pos)
        pos = {i for i in pos if all(i + offset in pos for offset in offsets)}
    return remove


PARSER = parsers.CoordinatesParser(chars="#")
TEST_DATA = """\
..........
..###.##..
...####...
..######..
..######..
...####...
.........."""
TESTS = [
    (1, TEST_DATA, 35),
    # (2, TEST_DATA, None),
    (3, TEST_DATA, 29),
]

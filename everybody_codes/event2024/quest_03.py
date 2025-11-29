"""Everyone Codes Day Three."""

from lib import helpers, parsers


def solve(part: int, data: helpers.Map) -> int:
    """Solve puzzle."""
    positions = data.coords["#"]
    remove = 0
    offsets = helpers.STRAIGHT_NEIGHBORS_T if part < 3 else helpers.ALL_NEIGHBORS_T
    while positions:
        remove += len(positions)
        positions = {
            position
            for position in positions
            if all(neighbor in positions for neighbor in helpers.neighbors_t(*position, offsets))
        }
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

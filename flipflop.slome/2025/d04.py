"""FlipFlop Codes: Puzzle 4: Beach cleanup."""
from lib import parsers


def solve(part: int, data: list[list[int]]) -> int:
    """Solve the parts."""
    x, y = 0, 0
    total = 0
    if part == 3:
        data.sort(key=sum)
    for a, b in data:
        dx, dy = abs(x - a), abs(y - b)
        if part == 1:
            total += dx + dy
        else:
            total += max(dx, dy)
        x, y = a, b
    return total


PARSER = parsers.parse_ints
TEST_DATA = """\
3,3
9,9
6,6"""

TESTS = [
    (1, TEST_DATA, 24),
    (2, TEST_DATA, 12),
    (3, TEST_DATA, 9),
]

"""Everyone Codes Day Four."""
from lib import parsers


def solve(part: int, data: list[int]) -> int:
    """Solve puzzle."""
    heights = data
    if part in [1, 2]:
        target = min(heights)
        return sum(i - target for i in heights)
    return min(
        sum(abs(i - target) for i in heights)
        for target in heights
    )


PARSER = parsers.parse_one_int_per_line
TEST_DATA = [
    """\
3
4
7
8""",
    """\
2
4
5
6
8""",
]
TESTS = [
    (1, TEST_DATA[0], 10),
    # (2, TEST_DATA[1], None),
    (3, TEST_DATA[1], 8),
]

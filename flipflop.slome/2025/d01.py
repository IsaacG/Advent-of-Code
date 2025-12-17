"""FlipFlop Codes: Puzzle 1: Banana Contest."""
from lib import parsers


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    lines = data.splitlines()
    if part == 2:
        lines = [line for line in lines if len(line) % 4 == 0]
    if part == 3:
        lines = [line for line in lines if "ne" not in line]

    return sum(len(line) // 2 for line in lines)


PARSER = parsers.parse_one_str
TEST_DATA = """\
banana
banenanana
bananana
bananananana
bananananana"""
TESTS = [
    (1, TEST_DATA, 24),
    (2, TEST_DATA, 16),
    (3, TEST_DATA, 19),
]

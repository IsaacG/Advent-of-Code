"""FlipFlop Codes: Puzzle 7: Hyper grids."""
import itertools
from lib import parsers


def solve(part: int, data: list[list[int]]) -> int:
    """Solve the parts."""
    total = 0
    if part == 1:
        shapes = [tuple([x, y]) for x, y in data]
    elif part == 2:
        shapes = [tuple([x, y, x]) for x, y in data]
    else:
        shapes = [tuple([size] * dims) for dims, size in data]

    for dimensions in shapes:
        ways = {}
        dims = len(dimensions)
        for position in itertools.product(*[range(i) for i in dimensions]):
            if sum(position) == 0:
                ways[position] = 1
            else:
                val = 0
                for idx in range(dims):
                    neighbor = list(position)
                    neighbor[idx] -= 1
                    val += ways.get(tuple(neighbor), 0)
                ways[position] = val

        total += ways[tuple(i - 1 for i in dimensions)]
    return total


PARSER = parsers.parse_ints
TEST_DATA = """\
2 2
3 3
2 3"""
TESTS = [
    (1, TEST_DATA, 11),
    (2, TEST_DATA, 108),
    (3, TEST_DATA, 98),
    (3, "4 3", 2520),
]

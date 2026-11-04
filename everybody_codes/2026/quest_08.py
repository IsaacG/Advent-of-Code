"""Everyone Codes Event 2026 Day 8."""

import collections
import itertools
from lib import helpers


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    DIRS = [(1, 1), (-1, 1), (-2, 0), (-1, -1), (1, -1), (2, 0)]
    energy = 0
    need = 100000

    field = {pos: int(char) for pos, char in data.chars.items() if char != "."}
    for rnd, (dx, dy) in enumerate(itertools.cycle(DIRS), 1):
        shadows = collections.defaultdict(int)
        for (x, y), char in field.items():
            for i, h in enumerate(range(char - 1, 0, -1), 1):
                shadows[(x + i * dx, y + i * dy)] = max(shadows[(x + i * dx, y + i * dy)], h)

        new = {}
        for pos, char in field.items():
            if char < 1:
                new[pos] = char + 1
            elif char <= shadows[pos]:
                new[pos] = char
            else:
                energy += 1
                new[pos] = char + 1
                if new[pos] == 10:
                    new[pos] = -2
                    need -= 1

        if part == 1 or part == 2 and rnd == 6:
            return energy
        if part == 3:
            field = new

        if need <= 0:
            return energy


TEST_DATA = """\
....1.9.6.1.7....
...9.2.3.3.8.1...
..7.8.3.5.1.4.3..
.4.6.7.4.1.1.8.9.
4.5.3.6.5.8.9.4.9
.9.5.1.5.6.2.8.9.
..7.7.6.4.6.2.4..
...9.3.8.3.8.4...
....1.6.6.2.8...."""
TESTS = [
    (1, TEST_DATA, 32),
    (2, TEST_DATA, 187),
    (3, TEST_DATA, 899889),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

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


if __name__ == "__main__":
    helpers.run_solution(globals())

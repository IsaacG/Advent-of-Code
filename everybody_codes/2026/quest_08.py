"""Everyone Codes Event 2026 Day N."""

import collections
import itertools
import logging
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    DIRS = [(1, 1), (-1, 1), (-2, 0), (-1, -1), (1, -1), (2, 0)]
    if part == 1:
        DIRS = [(1, 1)]
    t = 0

    if part != 3:
        for dx, dy in DIRS:
            shadows = collections.defaultdict(int)
            for pos, char in data.chars.items():
                if char == ".":
                    continue
                x, y = pos
                for i, h in enumerate(range(int(char) - 1, 0, -1), 1):
                    shadows[(x + i * dx, y + i * dy)] = max(shadows[(x + i * dx, y + i * dy)], h)

            energy = sum(
                int(char) > shadows[pos]
                for pos, char in data.chars.items()
                if char != "."
            )
            t += energy
        return t

    need = 100000

    field = {pos: int(char) for pos, char in data.chars.items() if char != "."}
    for rnd, (dx, dy) in enumerate(itertools.cycle(DIRS), 1):
        shadows = collections.defaultdict(int)
        for pos, char in field.items():
            x, y = pos
            for i, h in enumerate(range(char - 1, 0, -1), 1):
                shadows[(x + i * dx, y + i * dy)] = max(shadows[(x + i * dx, y + i * dy)], h)

        new = {}
        for pos, char in field.items():
            if char < 1:
                new[pos] = char + 1
            elif char <= shadows[pos]:
                new[pos] = char
            else:
                t += 1
                new[pos] = char + 1
                if new[pos] == 10:
                    new[pos] = -2
                    need -= 1
        field = new

        if need <= 0:
            return t
    return t
                

                




# PARSER = parsers.parse_one_str
TEST_DATA = [
    """\
""",
    """\
""",
    """\
""",
    """\
""",
    """\
""",
]
TESTS = [
    # (1, TEST_DATA[0], None),
    # (2, TEST_DATA[1], None),
    # (3, TEST_DATA[2], None),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

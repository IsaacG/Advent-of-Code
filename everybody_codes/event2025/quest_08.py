"""Everyone Codes Day N."""

import collections
import logging
from lib import helpers
from lib import parsers

log = logging.info


def solve(part: int, data: list[list[int]], testing: bool) -> int:
    """Solve the parts."""
    numbers = data[0]
    size = 8 if testing else 32 if part == 1 else 256

    # Create lines between nails.
    lines = []
    for a, b in zip(numbers, numbers[1:]):
        if a > b:
            a, b = b, a
        # Shift 1..256 to 0..255 to make the modulo math simple.
        lines.append((a - 1, b - 1))

    if part == 1:
        return sum(b - a == size // 2 for a, b in lines)
    if part == 2:
        return sum(
            (i < a < j) != (i < b < j) and a != i and b != j
            for idx, (a, b) in enumerate(lines)
            for i, j in lines[:idx]
        )

    # Count the occurance of lines between nails, in both directions.
    frequency: dict[int, dict[int, int]] = collections.defaultdict(lambda: collections.defaultdict(int))
    for a, b in lines:
        frequency[a][b] += 1
        frequency[b][a] += 1

    # Count the cumulative lines from nail a to nails [a + 1..b].
    # We can count the lines that i-j cuts anchored by nail a
    # by looking at the difference between difference between lines from a-(j-1) and a-(i).
    # This gives the total lines from a to `[(i+1)..(j-1)]`.
    cumulative: dict[int, dict[int, int]] = collections.defaultdict(lambda: collections.defaultdict(int))
    for a in range(1, size):
        for b in range(a + 1, a + size):
            cumulative[a][b % size] = cumulative[a][(b - 1) % size] + frequency[a][b % size]

    most = 0
    for a in range(size - 1):
        for b in range(a + 2, size):
            knots = frequency[a][b]
            for i in range(a + 1, b):
                knots += cumulative[i][(a - 1) % size] - cumulative[i][b]
            most = max(most, knots)
    return most


PARSER = parsers.parse_ints
TESTS = [
    (1, "1,5,2,6,8,4,1,7,3", 4),
    (2, "1,5,2,6,8,4,1,7,3,5,7,8,2", 21),
    (3, "1,5,2,6,8,4,1,7,3,6", 7),
]


if __name__ == "__main__":
    helpers.run_solution(globals())

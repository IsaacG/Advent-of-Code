"""Everyone Codes Day N."""

import functools
import math
import sys

AVAILABLE_DOTS = [
    [1, 3, 5, 10],
    [1, 3, 5, 10, 15, 16, 20, 24, 25, 30],
    [1, 3, 5, 10, 15, 16, 20, 24, 25, 30, 37, 38, 49, 50, 74, 75, 100, 101],
]


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    sys.setrecursionlimit(5000)
    targets = [int(line) for line in data.splitlines()]
    available_dots = AVAILABLE_DOTS[part - 1]

    @functools.cache
    def get_candidates(limit: int) -> set[int]:
        """Return candidate dots.

        1. Filter out all dots which are too large/above the target.
        2. Filter out dots for which there is a larger multiple, eg always use 20 over 10.
        """
        candidates = {i for i in available_dots if i <= limit}
        return {i for i in candidates if all(j % i or j == i for j in candidates)}

    @functools.cache
    def min_dots(target: int) -> int:
        """Return the minimum number of dots to get the target."""
        if target == 0:
            return 0
        max_candidate = max(i for i in available_dots if i <= target)
        candidates = get_candidates(max_candidate)
        lcm = math.lcm(*candidates)
        if target > lcm + max_candidate:
            steps = (target - lcm) // max_candidate
            return steps + min_dots(target - steps * max_candidate)
        return 1 + min(min_dots(target - i) for i in candidates if i <= target)

    if part in [1, 2]:
        return sum(min_dots(target) for target in targets)

    return sum(
        min(
            min_dots(upper) + min_dots(target - upper)
            for upper in range(target // 2, target // 2 + 51, 1)
        )
        for target in targets
    )


TEST_DATA = [
    "2\n4\n7\n16",
    "33\n41\n55\n99",
    "156488\n352486\n546212",
]
TESTS = [
    (1, TEST_DATA[0], 10),
    (2, TEST_DATA[1], 10),
    (3, TEST_DATA[2], 10449),
]

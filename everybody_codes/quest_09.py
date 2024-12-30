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
    targets = [int(line) for line in data.splitlines()]
    available_dots = AVAILABLE_DOTS[part - 1]
    sys.setrecursionlimit(sys.getrecursionlimit()*20)

    @functools.cache
    def get_candidates(limit: int) -> set[int]:
        candidates = {i for i in available_dots if i <= limit}
        candidates = {i for i in candidates if all(j % i or j == i for j in candidates)}
        # print(f"Candidates for {limit} -> {candidates}")
        return candidates

    @functools.cache
    def min_dots(target: int) -> int:
        # print(f"min_dots({target})")
        if target == 0:
            return 0
        if target in available_dots:
            return 1
        max_candidate = max(i for i in available_dots if i < target)
        candidates = get_candidates(max_candidate)
        # print(f"min_dots({target}) -> get_candidates({max_candidate}) = {candidates}")
        dm_d, dm_m = divmod(target, max_candidate)
        if dm_m == 0:
            return dm_d
        lcm = math.lcm(*candidates)
        # steps = lcm // max(available_dots)
        if target > lcm:
            # print(target, lcm, candidates)
            # return steps * (target // lcm) + min_dots(target % lcm)
            # return 1 + min_dots(target - max(available_dots))
            s = 0
            while target > lcm:
                target -= max_candidate
                s += 1
            # print(s, target)
            return s + min_dots(target)
        # print(candidates, target)
        return 1 + min(min_dots(target - i) for i in candidates if i < target)

    if part in [1, 2]:
        return sum(min_dots(target) for target in targets)

    for i in available_dots:
        min_dots(i)
        for j in available_dots:
            min_dots(i * j)

    total = 0
    for target in targets:
        t_min = target
        for ball_a in range(target // 2 - 1, target // 2 + 53, 1):
            ball_b = target - ball_a
            if abs(ball_a - ball_b) > 100:
                continue
            t_min = min(t_min, min_dots(ball_a) + min_dots(ball_b))
        total += t_min
    return total


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

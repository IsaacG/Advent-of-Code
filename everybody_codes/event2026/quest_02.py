"""Everyone Codes Event 2026 Day 2."""

import functools
import itertools

from lib import helpers


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    total = 0
    for group in data:
        cmp = {}
        nums = set()
        for pair in group:
            if ">" in pair:
                a, b = pair.split(">")
            else:
                b, a = pair.split("<")
            cmp[int(a), int(b)] = -1
            cmp[int(b), int(a)] = 1
            nums.add(int(a))
            nums.add(int(b))
        for a, b in itertools.combinations(nums, 2):
            if (a, b) not in cmp:
                c = next(i for i in (nums - {a, b}) if (a, i) in cmp and (i, b) in cmp and cmp[a, i] == cmp[i, b])
                cmp[a, b] = cmp[a, c]
                cmp[b, a] = cmp[c, a]
        total += int("".join(str(i) for i in sorted(nums, key=functools.cmp_to_key(lambda a, b: cmp[a, b]))))
    return total


TEST_DATA = [
    """\
4<3 2<5 3>1 1>2 1<5 4<1 3>2 4<2 3>5 4<5
4>1 2>1 3>2 1<5 4>5 2<5 3>1 4>3 2<4 5<3
5>1 5>2 4>1 2<4 3>2 3<4 1>2 3>5 1<3 4>5""",
    """\
2<5 3>1 1>2 1<5 4<1 3>2 4<2 3>5 4<5
2>1 3>2 1<5 4>5 2<5 3>1 4>3 2<4 5<3
5>1 5>2 4>1 3>2 3<4 1>2 3>5 1<3 4>5""",
    """\
3>1 1>2 1<5 4<2 3>5
2>1 2<5 3>1 4>3 2<4 5<3
5>1 3<4 1>2 3>5""",
]
TESTS = [
    (1, TEST_DATA[0], 122157),
    (2, TEST_DATA[1], 122157),
    (3, TEST_DATA[2], 122157),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

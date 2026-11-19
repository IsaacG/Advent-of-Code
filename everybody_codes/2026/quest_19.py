"""Everyone Codes Event 2026 Day N."""

import collections
import itertools
import math
import logging
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""

    def getcount(mapping):
        count = collections.defaultdict(int)

        for pos in data[0].chars:
            a, b = data[0].chars[pos], data[1].chars[pos]
            b = mapping[b]
            if "K" in (a, b):
                count["K"] += 1
            elif {a, b} == {"C", "M"}:
                count["B"] += 1
            elif {a, b} == {"C", "Y"}:
                count["G"] += 1
            elif {a, b} == {"M", "Y"}:
                count["R"] += 1
            elif len({a, b}) == 1:
                count[a] += 1
            else:
                raise ValueError(f"{a} {b}")
        return math.prod(sorted(count.values(), reverse=True)[:3])

    if part == 1:
        return getcount({i:i for i in "CMYK"})

    if part == 2:
        return max(
            getcount({a: b for a, b in enumerate(i, 1)})
            for i in itertools.permutations("CMYK")
        )

    s = collections.Counter(data[0].chars.values())
    t = s['M'] + s['Y'] + s['C']
    print(t)
    a = [(s['M'] + s['Y'] + s['C'] + i) // 3 for i in range(3)]
    print(s, a)
    return math.prod(a)
    t1 = (s['M'] + s['Y'] + s['C'] + 1) // 3
    t2 = (s['M'] + s['Y'] + s['C'] + 2) // 3
    assert t0 + t1 + t2 == s['M'] + s['Y'] + s['C']
    print(t0 * t1 * t2)


    for pos, char in data[0].chars.items():
        count[char] += 1
    print(count)

    """
{'M': 12624, 'Y': 9853, 'C': 15655, 'K': 3852})
GR
Y=9853 => 4927, 4926 =>       24270402 * K
BR => M=12624 => 6312*6312 => 39841344
BG
C => 15655 => 7827*7828    => 61269756 * 3852
M = 12624 - 7827 => 4797      61269756 * 4797

6817.33
M = 2 * 6312
C = 15655 - 6312 = 9343


293911019532 wrong len, right 2
251478563328
2053548611910


1400249595312 wrong length

"""
    best = 0
    for a, b in itertools.combinations("BGR", r=2):
        best = max(best, math.prod(new))
    return best








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

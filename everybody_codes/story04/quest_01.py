"""Everyone Codes Day N."""

import logging
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if part == 3:
        return s3(data)

    total = 0
    for jumps in data:
        pos = 0
        seen = {0}
        for jump in jumps:
            if pos >= jump and pos - jump not in seen:
                jump = -jump
            pos += jump
            while part == 2 and pos in seen:
                pos += 1
            seen.add(pos)
        total += pos
    return total

def s3(data: str) -> int:
    """Solve the parts."""
    total = 0
    for jumps in data:
        log(jumps)
        pos = 0
        seen = {0}
        pairs = {True: [], False: []}

        top = False

        def crosses(t):
            a, b = pos, t
            if a > b:
                a, b = b, a
            for i, j in pairs[top]:
                if (i < a < j) != (i < b < j):
                    return True
            return False

        for jump in jumps:
            if pos >= jump and pos - jump not in seen and not crosses(pos - jump):
                t = pos - jump
            else:
                a, b = pos, pos + jump
                for i, j in pairs[top]:
                    while b in seen:
                        b += 1
                    if a < i and i < b < j:
                        b = j + 1
                    while b in seen:
                        b += 1
                if crosses(b):
                    continue
                t = b

            pairs[top].append(tuple(sorted([pos, t])))
            pairs[top].sort(key=lambda x: x[1])
            pos = t
            seen.add(pos)
            top = not top
        log(pos)
        total += pos
    return total


# PARSER = parsers.parse_one_str
TEST_DATA = [
    """\
1,2,3,4,5,6,7,8,9
1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30""",
    """\
1,1,1,1,1
5,1,2,3,4,5,1,2,3,4
2,1,1,2,1,1,2,1,1,2,1,1
5,1,2,1,2,7,1,2,1,2,7,1,2,1,2""",
    """\
1,1,1,1,1
5,1,2,3,4,5,1,2,3,4
2,1,1,2,1,1,2,1,1,2,1,1
5,1,2,1,2,7,1,2,1,2,7,1,2,1,2""",
    """\
1,1,1,1,1
5,1,2,3,4,5,1,2,3,4
2,1,1,2,1,1,2,1,1,2,1,1
5,1,2,1,2,7,1,2,1,2,7,1,2,1,2""",
    """\
5,3,1,1
5,3,1,1,5,1,1,3,4,8,1,1
5,3,1,1,5,1,1,3,4,8,2,1
10,9,9,8,8,7,7,6,6,5,5,4,4,3,3,2,2,1"""
]
TESTS = [
    (1, TEST_DATA[0], 66),
    (1, TEST_DATA[1], 34),
    (2, TEST_DATA[2], 43),
    (3, TEST_DATA[3], 27),
    (3, TEST_DATA[4], 35),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

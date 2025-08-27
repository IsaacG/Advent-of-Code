"""Everyone Codes Day 1."""

import functools
import logging

log = logging.info


@functools.cache
def get_points(rows, token, start):
    pos = start * 2
    bounces = iter(token)
    for row in rows:
        if row[pos] == ".":
            continue
        bounce = next(bounces)
        if pos == 0:
            pos += 1
        elif pos == len(row) - 1:
            pos -= 1
        elif bounce == "R":
            pos += 1
        else:
            pos -= 1
    assert pos % 2 == 0
    end = (pos // 2) + 1
    points = end * 2 - start - 1
    points = max(0, points)
    return points


def min_max_points(rows, tokens, slots):

    @functools.cache
    def cached(tokens, slots):
        assert len(tokens) < len(slots)
        if len(tokens) == 1:
            points = sorted(get_points(rows, tokens[0], i) for i in slots)
            return points[0], points[-1]

        token, *tokens = tokens
        return min(
            get_points(rows, token, slot) + cached(tuple(tokens), frozenset(slots - {slot}))[0]
            for slot in slots
        ), max(
            get_points(rows, token, slot) + cached(tuple(tokens), frozenset(slots - {slot}))[1]
            for slot in slots
        )

    return cached(tokens, slots)


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    nails, tokens = data.split("\n\n")
    rows = nails.splitlines()
    assert len(rows[0]) % 2 == 1
    positions = (len(rows[0]) + 1) // 2

    if part in [1, 2]:
        score = 0
        for start, token in enumerate(tokens.splitlines()):
            if part == 1:
                score += get_points(rows, token, start)
            if part == 2:
                score += max(get_points(rows, token, i) for i in range(positions))
        return score

    slots = frozenset(range(positions))
    return min_max_points(tuple(rows), tuple(tokens.splitlines()), slots)


TEST_DATA = [
    """\
*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.
*.*.*...*.*...*..
.*.*.*.*.*...*.*.
*.*.....*...*.*.*
.*.*.*.*.*.*.*.*.
*...*...*.*.*.*.*
.*.*.*.*.*.*.*.*.
*.*.*...*.*.*.*.*
.*...*...*.*.*.*.
*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.

RRRLRLRRRRRL
LLLLRLRRRRRR
RLLLLLRLRLRL
LRLLLRRRLRLR
LLRLLRLLLRRL
LRLRLLLRRRRL
LRLLLLLLRLLL
RRLLLRLLRLRR
RLLLLLRLLLRL""",
    """\
*.*.*.*.*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.*.*.*.*.
..*.*.*.*...*.*...*.*.*..
.*...*.*.*.*.*.*.....*.*.
*.*...*.*.*.*.*.*...*.*.*
.*.*.*.*.*.*.*.*.......*.
*.*.*.*.*.*.*.*.*.*...*..
.*.*.*.*.*.*.*.*.....*.*.
*.*...*.*.*.*.*.*.*.*....
.*.*.*.*.*.*.*.*.*.*.*.*.
*.*.*.*.*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.*...*.*.
*.*.*.*.*.*.*.*.*...*.*.*
.*.*.*.*.*.*.*.*.....*.*.
*.*.*.*.*.*.*.*...*...*.*
.*.*.*.*.*.*.*.*.*.*.*.*.
*.*.*...*.*.*.*.*.*.*.*.*
.*...*.*.*.*...*.*.*...*.
*.*.*.*.*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.*.*.*.*.

RRRLLRRRLLRLRRLLLRLR
RRRRRRRRRRLRRRRRLLRR
LLLLLLLLRLRRLLRRLRLL
RRRLLRRRLLRLLRLLLRRL
RLRLLLRRLRRRLRRLRRRL
LLLLLLLLRLLRRLLRLLLL
LRLLRRLRLLLLLLLRLRRL
LRLLRRLLLRRRRRLRRLRR
LRLLRRLRLLRLRRLLLRLL
RLLRRRRLRLRLRLRLLRRL
""",
    """\
*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.
*.*.*...*.*...*..
.*.*.*.*.*...*.*.
*.*.....*...*.*.*
.*.*.*.*.*.*.*.*.
*...*...*.*.*.*.*
.*.*.*.*.*.*.*.*.
*.*.*...*.*.*.*.*
.*...*...*.*.*.*.
*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.

RRRLRLRRRRRL
LLLLRLRRRRRR
RLLLLLRLRLRL
LRLLLRRRLRLR
LLRLLRLLLRRL
LRLRLLLRRRRL""",
]
TESTS = [
    (1, TEST_DATA[0], 26),
    (2, TEST_DATA[1], 115),
    (3, TEST_DATA[2], (13, 43)),
]

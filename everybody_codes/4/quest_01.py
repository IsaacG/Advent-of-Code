"""Everyone Codes Story 4 Quest 1."""

from lib import helpers


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    total = 0
    for jumps in data:
        pos = 0
        seen = {0}
        pairs = {True: [], False: []}
        top = False

        for jump in jumps:
            if (
                # Jump backwards if it won't be a repeat.
                pos >= jump
                and pos - jump not in seen
                and (
                    part < 3 or all(  # Part 3: avoid crossings
                        (i < pos - jump < j) == (i < pos < j)
                        for i, j in pairs[top]
                    )
                )
            ):
                next_pos = pos - jump
            else:
                # Jump forward, avoid repeats
                next_pos = pos + jump
                while part > 1 and next_pos in seen:
                    next_pos += 1
                # Part 3: avoid crossing
                if part == 3:
                    discard = False
                    for i, j in pairs[top]:
                        # Discard if we can't avoid crossing by incrementing.
                        if i < pos < j < next_pos:
                            discard = True
                            break
                        if pos < i < next_pos < j:
                            next_pos = j + 1
                        while next_pos in seen:
                            next_pos += 1
                    if discard:
                        continue

            pairs[top].append(tuple(sorted([pos, next_pos])))
            pairs[top].sort(key=lambda x: x[1])
            pos = next_pos
            seen.add(pos)
            top = not top
        total += pos
    return total


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

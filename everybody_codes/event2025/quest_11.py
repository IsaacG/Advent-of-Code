"""Everyone Codes Day N."""

import logging
import math
import time
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    columns = [i[0] for i in data]
    num = len(columns) - 1
    steps = 0
    ducks = sum(columns)

    while any(a > b for a, b in zip(columns, columns[1:])):
        log(" ".join(str(i) for i in columns))
        ptr = 0
        changes = []
        min_delta = ducks
        while ptr < num:
            if columns[ptr] <= columns[ptr + 1]:
                ptr += 1
                continue
            start = ptr
            while ptr < num and columns[ptr] > columns[ptr + 1]:
                ptr += 1
            mid = ptr
            while ptr < num and columns[ptr] == columns[ptr + 1]:
                ptr += 1

            end = ptr
            spread = 1 + end - mid
            move = columns[start] - columns[mid]

            move = min(move, columns[start] - columns[start + 1])
            move = min(move, spread * (columns[mid - 1] - columns[mid]))
            if end < num:
                move = min(move, spread * (columns[end + 1] - columns[end]))
            if mid == start + 1:
                move = min(move, int(math.ceil(spread * (columns[start] - columns[start + 1]) / 2)))
            if spread > move:
                move = 1
                mid = end
                print("=================")
            else:
                move -= move % spread

            changes.append((start, mid, end, move))


        move = min(move for start, mid, end, move in changes)
        print(f"{columns=}, {move=}, {changes=}")

        for start, mid, end, _ in changes:
            columns[start] -= move
            amnt = move // (end + 1 - mid)
            for b in range(mid, end + 1):
                columns[b] += amnt
        steps += move
    print(" ".join(str(i) for i in columns))

    if part == 1: return 10 # debug

    while any(a > b for b, a in zip(columns, columns[1:])):
        # print("Before", ' '.join(str(i) for i in columns))
        ptr = 0
        changes = []
        min_delta = ducks
        while ptr < num:
            if columns[ptr + 1] <= columns[ptr]:
                ptr += 1
                continue
            start = ptr
            while ptr < num and columns[ptr + 1] >= columns[ptr]:
                ptr += 1
            changes.append((start, ptr))

        min_delta = min(
            min(columns[i + 1] - columns[i] + (i != a) for i in range(a, b))
            for a, b in changes
        )
        limit = min((columns[i] - columns[i + 1] for _, i in changes if i < num), default=ducks)
        min_delta = min(min_delta, limit)
        for b, a in changes:
            columns[a] -= min_delta
            columns[b] += min_delta
        steps += min_delta

    return steps


PARSER = parsers.parse_ints
TEST_DATA = [
    """\
9
1
1
4
9
6""",
    """\
9
1
1
4
9
6""",
    """\
805
706
179
48
158
150
232
885
598
524
423""",
]
TESTS = [
    (1, TEST_DATA[0], 109),
    (2, TEST_DATA[1], 11),
    (2, TEST_DATA[2], 1579),
    # (3, TEST_DATA[2], None),
]

if __name__ == "__main__":
    for _part, _data, expected in TESTS:
        assert solve(_part, PARSER.parse(_data)) == expected
    print("Tests pass.")
    day = int(__file__.split("_", maxsplit=-1)[-1].split(".")[0])
    for _part in range(1, 4):
        with open(f"inputs/{day:02}.{_part}.txt", encoding="utf-8") as f:
            _input = PARSER.parse(f.read())  # type: list[list[int]]
            start = time.perf_counter_ns()
            got = solve(_part, _input)
            end = time.perf_counter_ns()
            print(f"{day:02}.{_part} {got:15} {helpers.format_ns(end - start):8}")

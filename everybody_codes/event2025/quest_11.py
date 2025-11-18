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
            if columns[ptr] < columns[ptr + 1]:
                ptr += 1
                continue
            src_start = ptr
            while ptr < num and columns[ptr] == columns[ptr + 1]:
                ptr += 1
            src_end = ptr
            if ptr == num or columns[ptr] < columns[ptr + 1]:
                ptr += 1
                continue
            while ptr < num and columns[ptr] > columns[ptr + 1]:
                ptr += 1
            dst_start = ptr
            while ptr < num and columns[ptr] == columns[ptr + 1]:
                ptr += 1
            dst_end = ptr
            src_num = src_end - src_start + 1
            dst_num = dst_end - dst_start + 1
            move = (columns[src_start] - columns[dst_start]) * src_num
            if move < dst_num:
                move = 1
                src_start = src_end
                dst_end = dst_start
                src_num = dst_num = 1

            DEBUG = [703, 703, 179, 153, 154, 154, 232, 636, 598, 598, 598]
            print(columns)
            if columns == DEBUG: print(1, move)
            move = min(move, src_num * (columns[src_end] - columns[src_end + 1]))
            if columns == DEBUG: print(2, move)
            move = min(move, dst_num * (columns[dst_start - 1] - columns[dst_start]))
            if columns == DEBUG: print(3, move)
            if dst_end < num:
                move = min(move, dst_num * (columns[dst_end + 1] - columns[dst_end]))
            if columns == DEBUG: print(4, move)
            if src_end == dst_start - 1:
                move = min(move, int(math.ceil((columns[src_start] - columns[dst_start]) / src_num * dst_num / 2)))
            if columns == DEBUG: print(5, move)

            if move < math.lcm(dst_num, src_num):
                move = 1
                src_start = src_end
                dst_end = dst_start
                src_num = dst_num = 1
                print("clamp", f"{columns=}, {src_start, src_end, dst_start, dst_end, move}")

            if columns == DEBUG: print(6, move)
            move -= move % math.lcm(dst_num, src_num)
            if columns == DEBUG: print(7, move)
            assert move > 0, f"{columns=}, {src_start, src_end, dst_start, dst_end, move}"

            changes.append((src_start, src_end, dst_start, dst_end, move))


        min_move = min(move for src_start, src_end, dst_start, dst_end, move in changes)
        print(f"{columns=}, {move=}, {changes=}")

        for src_start, src_end, dst_start, dst_end, move in changes:
            for i in range(src_start, src_end + 1):
                columns[i] -= min_move // (src_end - src_start + 1)
            for i in range(dst_start, dst_end + 1):
                columns[i] += min_move // (dst_end - dst_start + 1)
        steps += min_move
        assert ducks == sum(columns)
    print(" ".join(str(i) for i in columns))

    if part == 1: return 10 # debug

    print(columns)
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
    print(columns)
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

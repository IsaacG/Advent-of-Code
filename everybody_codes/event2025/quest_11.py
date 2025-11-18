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

    counter = 0

    while any(a > b for a, b in zip(columns, columns[1:])):
        counter += 1
        if counter > 4:
            return
        print("Before", ' '.join(str(i) for i in columns))
        ptr = 0
        changes = []
        min_delta = ducks
        while ptr < num:
            if columns[ptr] <= columns[ptr + 1]:
                ptr += 1
                continue
            start = ptr
            delta = int(math.ceil((columns[ptr] - columns[ptr + 1]) / 2))
            print(f"{ptr=} {delta=}")
            while ptr < num and columns[ptr] >= columns[ptr + 1]:
                delta = min(delta, int(math.floor((columns[ptr] + delta - columns[ptr + 1]) / 2)))
                ptr += 1
            changes.append((start, ptr))
            print(f"Move {start} to {ptr}: {delta}")
            min_delta = min(min_delta, delta)
        for a, b in changes:
            columns[a] -= min_delta
            columns[b] += min_delta
        steps += min_delta
        print(f"After {steps} {min_delta=} | {' '.join(str(i) for i in columns)}")
        print()


    while any(a < b for a, b in zip(columns, columns[1:])):
        steps += 1
        for i in range(num):
            if columns[i] < columns[i + 1]:
                columns[i] += 1
                columns[i + 1] -= 1
        if part == 1 and steps == 10:
            return sum(idx * count for idx, count in enumerate(columns, start=1))
    if part == 2:
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

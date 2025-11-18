"""Everyone Codes Day N."""

import time
from lib import helpers
from lib import parsers


def solve(part: int, data: list[int]) -> int:
    """Solve the parts."""
    ducks = data
    num = len(ducks) - 1

    steps = 0
    while any(a > b for a, b in zip(ducks, ducks[1:])):
        steps += 1
        for i in range(num):
            if ducks[i] > ducks[i + 1]:
                ducks[i] -= 1
                ducks[i + 1] += 1

    if part > 1:
        assert ducks == sorted(ducks)
        average = sum(ducks) // len(ducks)
        return steps + sum(abs(i - average) for i in ducks) // 2

    for _ in range(steps, 10):
        for i in range(num):
            if ducks[i] < ducks[i + 1]:
                ducks[i] += 1
                ducks[i + 1] -= 1
    return sum(idx * count for idx, count in enumerate(ducks, start=1))


PARSER = parsers.parse_one_int_per_line
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
]

if __name__ == "__main__":
    for _part, _data, expected in TESTS:
        assert solve(_part, PARSER.parse(_data)) == expected
    print("Tests pass.")
    day = int(__file__.split("_", maxsplit=-1)[-1].split(".")[0])
    for _part in range(1, 4):
        with open(f"inputs/{day:02}.{_part}.txt", encoding="utf-8") as f:
            _input = PARSER.parse(f.read())  # type: list[int]
            start = time.perf_counter_ns()
            got = solve(_part, _input)
            end = time.perf_counter_ns()
            print(f"{day:02}.{_part} {got:15} {helpers.format_ns(end - start):8}")

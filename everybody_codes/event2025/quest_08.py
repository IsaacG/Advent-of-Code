"""Everyone Codes Day N."""

import logging
import time
from lib import helpers
from lib import parsers

log = logging.info


def solve(part: int, data: list[list[int]], testing: bool) -> int:
    """Solve the parts."""
    numbers = data[0]
    size = 8 if testing else 32 if part == 1 else 256

    # Create lines between nails.
    lines = []
    for a, b in zip(numbers, numbers[1:]):
        if a > b:
            a, b = b, a
        lines.append((a, b))

    if part == 1:
        return sum(b - a == size // 2 for a, b in lines)
    if part == 2:
        return sum(
            (i < a < j) != (i < b < j) and a != i and b != j
            for idx, (a, b) in enumerate(lines)
            for i, j in lines[:idx]
        )

    most = 0
    for a in range(1, size):
        for b in range(a + 1, size + 1):
            knots = 0
            for i, j in lines:
                if (
                    a == i and b == j
                    or
                    (i < a < j) != (i < b < j) and a != i and b != j
                ):
                    knots += 1
            most = max(most, knots)
    return most


PARSER = parsers.parse_ints
TESTS = [
    (1, "1,5,2,6,8,4,1,7,3", 4),
    (2, "1,5,2,6,8,4,1,7,3,5,7,8,2", 21),
    (3, "1,5,2,6,8,4,1,7,3,6", 7),
]


if __name__ == "__main__":
    for _part, _data, expected in TESTS:
        assert solve(_part, PARSER.parse(_data), True) == expected
    print("Tests pass.")
    day = int(__file__.split("_", maxsplit=-1)[-1].split(".")[0])
    for _part in range(1, 4):
        with open(f"inputs/{day:02}.{_part}.txt", encoding="utf-8") as f:
            _input = PARSER.parse(f.read())  # type: list[list[int]]
            start = time.perf_counter_ns()
            got = solve(_part, _input, False)
            end = time.perf_counter_ns()
            print(f"{_part} {helpers.format_ns(end - start):8}  {got}")

"""Everyone Codes Day N."""

import logging
import time
from lib import parsers

log = logging.info

def solve(part: int, data: str, testing: bool) -> int:
    """Solve the parts."""
    numbers = data[0]
    if part == 1:
        size = 8 if testing else 32
        return sum(abs((b + size) % size - a) == size // 2 for a, b in zip(numbers, numbers[1:]))
    if part == 2:
        size = 8 if testing else 256
        lines = []
        knots = 0
        for idx, (a, b) in enumerate(zip(numbers, numbers[1:])):
            if a > b:
                a, b = b, a
            # print(a, b, "=>")
            for i, j in lines:
                if a == i or b == j:
                    continue
                if (i < a < j) != (i < b < j):
                    knots += 1
            lines.append((a, b))
        if not testing:
            assert len(str(knots)) == len(str(1513591)) and knots != 1513591
        return knots
    if part == 3:
        size = 8 if testing else 256
        lines = []
        for a, b in zip(numbers, numbers[1:]):
            if a > b:
                a, b = b, a
            lines.append((a, b))
        most = 0
        for a in range(1, size):
            for b in range(a + 1, size + 1):
                knots = 0
                for i, j in lines:
                    if a == i and b == j:
                        knots += 1
                    elif a in [i, j] or b in [i, j]:
                        continue
                    elif ((i < a < j) != (i < b < j)):
                        knots += 1
                most = max(most, knots)
        if not testing:
            assert most not in [2789, 2791, 2802] and 2000 <= most < 3000, str(most)
        return most


PARSER = parsers.parse_ints
TEST_DATA = [
]
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
            data = PARSER.parse(f.read())
            start = time.perf_counter_ns()
            got = solve(_part, data, False)
            end = time.perf_counter_ns()
            print(f"{_part} {(end - start) / 1000:8}μs  {got}")

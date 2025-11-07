"""Everyone Codes Day N."""

import logging
import math
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if part == 1 or part == 2:
        gears = [i[0] for i in data]
        ratio = 1
        for a, b in zip(gears, gears[1:]):
            ratio *= a / b
        if part == 1:
            return int(ratio * 2025)
        if part == 2:
            return math.ceil(10000000000000 / ratio)
    first, *rest, last = data
    gears = [[1, first[0]], *rest, [last[0], 1]]
    ratio = 1
    for a, b in zip(gears, gears[1:]):
        ratio *= a[1] / b[0]
    print(ratio)
    return int(ratio * 100)


PARSER = parsers.parse_ints
TEST_DATA = [
]
TESTS = [
    (1, "128\n64\n32\n16\n8", 32400),
    (1, """102\n75\n50\n35\n13""", 15888),
    (2, "128\n64\n32\n16\n8", 625000000000),
    (2, """102\n75\n50\n35\n13""", 1274509803922),
    (3, "5\n5|10\n10|20\n5", 400),
    (3, "5\n7|21\n18|36\n27|27\n10|50\n10|50\n11", 6818),
]

if __name__ == "__main__":
    for _part, _data, expected in TESTS:
        assert solve(_part, PARSER.parse(_data)) == expected
    print("Tests pass.")
    day = __file__.split("_", maxsplit=1)[-1].split(".")[0]
    for _part in range(1, 4):
        with open(f"inputs/{day}.{_part}.txt", encoding="utf-8") as f:
            print(_part, solve(_part, PARSER.parse(f.read())))

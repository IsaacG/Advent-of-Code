"""Everyone Codes Event 2026 Day 3."""

import itertools
import logging
from lib import helpers
from lib import parsers

log = logging.info

def compute(iso, number):
    iso = str(abs(iso))[::-1]
    number = str(number)[::-1]
    return sum(
        int(b) * int(a) ** idx
        for idx, (a, b) in enumerate(zip(itertools.cycle(iso), number))
    )


def solve(part: int, data: str, testing) -> int:
    """Solve the parts."""
    if part < 3:
        return sum(compute(iso, number) for iso, number in data)

    total = 0
    for _, iso, number in data:
        iso = abs(iso)
        print(iso, number)
        t = compute(iso, number)
        if not any(
            compute(iso, i) == t
            for i in range(number)
        ):
            print(iso, number)
            total += t
                
    if part == 3:
        assert testing or len(str(total)) == len(str(728387)) and total // 100000 not in {6, 7}
    return total


# PARSER = parsers.parse_one_str
TEST_DATA = [
    """\
ISO-3210 7654
ISO-8742 2468
ISO-1111 1111""",
    """\
ISO-3210 7654
ISO-8742 2468
ISO-1 1111
ISO-13 777
ISO-34 140856
ISO-789 2465112
ISO-2341 945""",
    """\
ISO2-3 23
ISO2-61 149
ISO2-978 99
ISO2-5887 5923
ISO2-76988 123749
ISO2-435657 929977
ISO2-3949 870737""",
]
TESTS = [
    (1, TEST_DATA[0], 1478),
    (2, TEST_DATA[1], 1161463),
    (3, TEST_DATA[2], 50987),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

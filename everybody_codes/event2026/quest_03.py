"""Everyone Codes Event 2026 Day 3."""

import itertools
import logging
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str, testing) -> int:
    """Solve the parts."""
    total = 0
    if part < 3:
        for iso, num in data:
            iso = str(abs(iso))[::-1]
            num = str(num)[::-1]
            s = 0
            for idx, (a, b) in enumerate(zip(itertools.cycle(iso), num)):
                s += int(b) * int(a) ** idx
            total += s
    else:
        for _, iso, num in data:
            iso = str(abs(iso))[::-1]
            num = str(num)[::-1]
            s = 0
            for idx, (a, b) in enumerate(zip(itertools.cycle(iso), num)):
                s += int(b) * int(a) ** idx

            def smaller(number, size):
                positions = [int(a) ** idx for idx, (a, _) in enumerate(zip(itertools.cycle(iso), range(size)))][::-1]
                if sum(9 * p for p in positions) < number:
                    return False
                n = number
                for p in positions:
                    times = min(9, n // p)
                    n -= p * times
                return n == 0 or smaller(number, size - 1)

            def same_base(number, og):
                size = len(og)
                positions = [int(a) ** idx for idx, (a, _) in enumerate(zip(itertools.cycle(iso), range(size)))][::-1]
                top_pos = positions[0]
                top_num = int(og[-1])
                for i in range(1, top_num):
                    n = number - top_pos * i
                    if smaller(n, size - 1):
                        return True
                return False

            print(iso[::-1], num[::-1], smaller(s, len(num) - 1), same_base(s, num))
            if not same_base(s, num) and not smaller(s, len(num) - 1):
                total += s
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

"""Everyone Codes Day N."""

import logging
import time
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    pass


PARSER = parsers.parse_one_str
TEST_DATA = [
]
TESTS = [
    # (1, TEST_DATA[0], None),
    # (2, TEST_DATA[1], None),
    # (3, TEST_DATA[2], None),
]

if __name__ == "__main__":
    for _part, _data, expected in TESTS:
        assert solve(_part, PARSER.parse(_data)) == expected
    print("Tests pass.")
    day = int(__file__.split("_", maxsplit=-1)[-1].split(".")[0])
    for _part in range(1, 4):
        with open(f"inputs/{day:02}.{_part}.txt", encoding="utf-8") as f:
            data = PARSER.parse(f.read())
            start = time.perf_counter_ns()
            got = solve(_part, data)
            end = time.perf_counter_ns()
            print(f"{_part} {(end - start) / 1000:8}μs  {got}")

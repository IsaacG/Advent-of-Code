"""Everyone Codes Day N."""

import logging

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    pass


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
    day = __file__.split("_", maxsplit=1)[-1].split(".")[0]
    for _part in range(1, 4):
        with open(f"inputs/{day}.{_part}.txt", encoding="utf-8") as f:
            print(_part, solve(_part, PARSER.parse(f.read())))

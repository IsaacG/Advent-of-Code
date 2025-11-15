"""Everyone Codes Day N."""

import logging

from lib import parsers


def solve(part: int, data: tuple[list[str], list[str]], testing: bool) -> str:
    """Solve the parts."""
    names, instructions = data
    count = len(names)
    cur = 0
    for instruction in instructions:
        direction, amount = instruction[0], int(instruction[1:])
        if direction == "L":
            amount = -amount
        if part == 1:
            cur = max(0, min(count - 1, cur + amount))
        elif part == 2:
            cur += amount
        else:
            names[0], names[amount % count] = names[amount % count], names[0]
    got = names[cur % count]
    if part == 3 and not testing:
        assert len(got) == len("Norakthar")
        assert got != "Norakthar"
    return got


PARSER = parsers.ParseBlocks([parsers.Transform(lambda x: x.split(","))])
TEST_DATA = [
    "Vyrdax,Drakzyph,Fyrryn,Elarzris\n\nR3,L2,R3,L1",
    "Vyrdax,Drakzyph,Fyrryn,Elarzris\n\nR3,L2,R3,L3",
]
TESTS = [
    (1, TEST_DATA[0], "Fyrryn"),
    (2, TEST_DATA[0], "Elarzris"),
    (3, TEST_DATA[1], "Drakzyph"),
]

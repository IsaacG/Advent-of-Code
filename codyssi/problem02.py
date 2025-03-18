"""Codyssi Day 2."""

def solve(part: int, data: str) -> int:
    """Solve the puzzle."""
    lines = [i == "TRUE" for i in data.splitlines()]
    if part == 1:
        return sum(i for i, line in enumerate(lines, 1) if line)
    if part == 2:
        return sum(
            (idx % 2 == 0 and a and b) or (idx % 2 == 1 and (a or b))
            for idx, (a, b) in enumerate(zip(lines[::2], lines[1::2]))
        )
    total = 0
    while lines:
        total += sum(lines)
        lines = [
            (idx % 2 == 0 and a and b) or (idx % 2 == 1 and (a or b))
            for idx, (a, b) in enumerate(zip(lines[::2], lines[1::2]))
        ]
    return total


TEST_DATA = """\
TRUE
FALSE
TRUE
FALSE
FALSE
FALSE
TRUE
TRUE"""
TESTS = [
    (1, TEST_DATA, 19),
    (2, TEST_DATA, 2),
    (3, TEST_DATA, 7),
]

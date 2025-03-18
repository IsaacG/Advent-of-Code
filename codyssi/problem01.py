"""Codyssi Day 1."""

def solve(part: int, data: str, testing: bool) -> int:
    """Solve the puzzle."""
    numbers = (int(i) for i in data.splitlines())
    if part == 1:
        return sum(numbers)
    if part == 2:
        return sum(sorted(numbers)[:-2 if testing else -20])
    numlist = list(numbers)
    return sum(numlist[::2]) - sum(numlist[1::2])


TEST_DATA = """\
912372
283723
294281
592382
721395
91238"""
TESTS = [
    (1, TEST_DATA, 2895391),
    (2, TEST_DATA, 1261624),
    (3, TEST_DATA, 960705),
]

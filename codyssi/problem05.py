"""Codyssi Day N."""

def solve(part: int, data: str) -> int:
    """Solve the puzzle."""
    *nums, syms = data.splitlines()
    symbols = list(syms)
    if part >= 2:
        symbols.reverse()
    numbers = [int(i) for i in nums]
    if part == 3:
        numbers = [
            a * 10 + b
            for a, b in zip(numbers[::2], numbers[1::2])
        ]
    heading, *rest = numbers
    for n, s in zip(rest, symbols):
        heading += n if s == "+" else -n
    return heading


TEST_DATA = """\
8
1
5
5
7
6
5
4
3
1
-++-++-++
"""
TESTS = [
    (1, TEST_DATA, 21),
    (2, TEST_DATA, 23),
    (3, TEST_DATA, 189),
]

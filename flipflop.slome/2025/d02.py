"""FlipFlop Codes: Puzzle 2: Rollercoaster Heights."""
import more_itertools

from lib import parsers


def fib(n: int) -> int:
    """Return the n'th value of the Fibonacci sequence."""
    a, b, c = 0, 1, 1
    for _ in range(n):
        a, b, c = b, c, b + c
    return a


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    highest = 0
    cur = 0
    if part == 1:
        for i in data:
            cur += 1 if i == "^" else -1
            highest = max(highest, cur)
    else:
        for direction, amount in more_itertools.run_length.encode(data):
            if part == 2:
                cur += (1 if direction == "^" else -1) * amount * (amount + 1) // 2
            else:
                cur += (1 if direction == "^" else -1) * fib(amount)
            highest = max(highest, cur)
    return highest


PARSER = parsers.parse_one_str
TESTS = [
    (1, "^^^v^^^^vvvvvvv", 6),
    (2, "^^^v^^^^vvvvvvv", 15),
    (3, "^^^v^^^^vvvvvvv", 4),
    (3, "^^^^^^^^^^^^vvvvvvvvv^", 144),
]

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
    transform = [lambda x: x, lambda x: (x * (x + 1) // 2), fib][part - 1]
    for direction, amount in more_itertools.run_length.encode(data):
        cur += (1 if direction == "^" else -1) * transform(amount)
        highest = max(highest, cur)
    return highest


PARSER = parsers.parse_one_str
TESTS = [
    (1, "^^^v^^^^vvvvvvv", 6),
    (2, "^^^v^^^^vvvvvvv", 15),
    (3, "^^^v^^^^vvvvvvv", 4),
    (3, "^^^^^^^^^^^^vvvvvvvvv^", 144),
]

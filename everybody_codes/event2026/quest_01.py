"""Everyone Codes Event 2026 Day 1."""

import itertools
from lib import helpers


class GetNext:

    def __init__(self, gen):
        self.gen = gen
        self.seen = []
        self.max = 0

    def __next__(self, limit):
        if limit <= self.max:
            return next(i for i in self.seen if limit <= i)
        while (i := next(self.gen)) < limit:
            self.seen.append(i)
        self.seen.append(i)
        self.max = i
        return i

def solve(part: int, data: list[int]) -> int:
    """Solve the parts."""
    need = 0
    for have in data:
        gen = [
            (i * i for i in itertools.count(1) if i * i >= have),
            (4 * i for i in itertools.count(2) if 4 * i >= have),
            (i * i - 1 for i in itertools.count(3, 2) if i * i - 1 >= have),
        ][part - 1]
        need += next(gen) - have
    return need


TEST_DATA = "3,11,12,16,24,25"
TESTS = [
    (1, TEST_DATA, 11),
    (2, TEST_DATA, 9),
    (3, TEST_DATA, 61),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

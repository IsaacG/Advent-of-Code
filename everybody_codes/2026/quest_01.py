"""Everyone Codes Event 2026 Day 1."""

import itertools

from lib import helpers


class CachedGetNextOverLimit:

    def __init__(self, gen):
        self.gen = gen
        self.seen = []
        self.max = 0

    def needed(self, limit):
        if limit <= self.max:
            return next(i for i in self.seen if limit <= i)
        while (i := next(self.gen)) < limit:
            self.seen.append(i)
        self.seen.append(i)
        self.max = i
        return i


def solve(part: int, data: list[int]) -> int:
    """Solve the parts."""
    gen = CachedGetNextOverLimit([
        (i * i for i in itertools.count(1)),
        (4 * i for i in itertools.count(2)),
        (i * i - 1 for i in itertools.count(3, 2)),
    ][part - 1])
    return sum(gen.needed(have) - have for have in data)


if __name__ == "__main__":
    helpers.run_solution(globals())

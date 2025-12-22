#!/usr/bin/env python
"""AoC Day 6: Custom Customs."""


def solve(data, part: int) -> int:
    """Count responses."""
    if part == 1:
        # Part 1: count the unique chars, joining all lines.
        return sum(len(set(line.replace('\n', ''))) for line in data)

    # Part 2: count num of chars found on all lines.
    total = 0
    for r in data:
        records = r.split()
        s = set(records.pop())
        while records:
            s &= set(records.pop())
        total += len(s)
    return total


PARSER = lambda x: x.split("\n\n")
TESTS = [
    (1, 'abc\n\na\nb\nc\n\nab\nac\n\na\na\na\na\n\nb', 11),
    (2, "abc\n\na\nb\nc\n\nab\nac\n\na\na\na\na\n\nb", 6),
]

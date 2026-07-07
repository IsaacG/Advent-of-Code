"""Eldarverse Day N."""

import collections
import functools
import itertools
import logging

log = logging.info

@functools.cache
def compute(n):
    counts = [0] * (n * 2)
    for table in itertools.product(itertools.product((0, 1), repeat=n - 1), repeat=n):
        mn = n * n
        mx = 0
        for i in range(n):
            wins = sum(table[i]) + sum(1 - row[i - 1] for row in table[:i]) + sum(1 - row[i] for row in table[i + 1:])
            if wins < mn:
                mn = wins
            if wins > mx:
                mx = wins
        distance = mx - mn
        for k in range(n + 1):
            if distance > k:
                counts[k] += 1
    return tuple(counts)

def _solve(data: str) -> str:
    n, k = [int(i) for i in data.split()]
    print(n, k)
    return compute(n)[k]

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    lines = data.splitlines()
    return "\n".join(
        f"Case #{idx}: {_solve(line)}"
        for idx, line in enumerate(lines[1:], 1)
    )


TESTS = [
    # (1, "2\n2 0", "Case #1: 2"),
    (1, "2\n2 0\n3 2", "Case #1: 2\nCase #2: 18"),
]

#!/bin/python
"""Advent of Code, Day 6: Memory Reallocation.

This solution is `O(blocks)` as we redistribute the blocks.
If the number of blocks is large, we can reduce `O(blocks)` to `O(banks)`.
However, the block count is low enough that the `O(blocks)` solution appears faster.

```
div, mod = divmod(num, count)
extras = {i % count for i in range(idx + 1, idx + 1 + mod)}
banks[idx] = 0
banks = [bank + div + (idx in extras) for idx, bank in enumerate(banks)]
```
"""
import itertools


def solve(data: list[int], part: int) -> int:
    """Reallocate blocks across banks until a loop is detected."""
    banks = data
    seen: dict[int, int] = {}
    count = len(banks)
    for step in itertools.count():
        hash_ = hash(tuple(banks))
        if hash_ in seen:
            return step if part == 1 else step - seen[hash_]
        seen[hash_] = step
        num, idx = max((num, -idx) for idx, num in enumerate(banks))
        idx = -idx

        banks[idx] = 0
        for bank in range(idx + 1, idx + 1 + num):
            banks[bank % count] += 1

    raise RuntimeError("No solution.")


TESTS = [(1, "0 2 7 0", 5), (2, "0 2 7 0", 4)]
# vim:expandtab:sw=4:ts=4

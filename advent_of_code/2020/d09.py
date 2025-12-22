#!/usr/bin/env python
"""AoC Day 9: Encoding Error."""

import itertools


def is_valid(pool: list[int], num: int):
    """Return if `num` is the sum of two values from the pool."""
    for a, b in itertools.combinations(pool, 2):
        if a + b == num:
            return True
    return False


def solve(data, part: int, testing: bool) -> int:
    "Analyze numbers."""
    return (part1 if part == 1 else part2)(data, testing)


def part1(nums: list[int], testing: bool) -> int:
    """Return the first number not composed of two values in the last `preamble` values."""
    preamble = 5 if testing else 25
    pool = nums[0:preamble]
    nums = nums[preamble:]
    for num in nums:
        if not is_valid(pool, num):
            return num
        pool.pop(0)
        pool.append(num)
    raise ValueError


def part2(nums: list[int], testing: bool) -> int:
    """Find a contiguous set of nums that sum to `part1()`. Return min(pool) + max(pool)."""
    want = part1(nums, testing)
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            s = sum(nums[i:j])
            if s == want:
                return min(nums[i:j]) + max(nums[i:j])
            if s > want:
                break
    raise ValueError


SAMPLE = """\
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""
TESTS = [
    (1, SAMPLE, 127),
    (2, SAMPLE, 62),
]

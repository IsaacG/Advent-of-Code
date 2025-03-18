"""Codyssi Day N."""

import logging

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    *nums, syms = data.splitlines()
    if part >= 2:
        syms = reversed(syms)
    nums = [int(i) for i in nums]
    if part == 3:
        nums = [
            a * 10 + b
            for a, b in zip(nums[::2], nums[1::2])
        ]
    heading, *rest = nums
    for n, s in zip(rest, syms):
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

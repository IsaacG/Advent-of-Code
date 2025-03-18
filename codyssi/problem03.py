"""Codyssi Day 3."""

import logging

log = logging.info

def solve(part: int, data: str) -> int:
    lines = data.splitlines()
    if part == 1:
        return sum(int(line.split()[1]) for line in lines)
    total = sum(int(line.split()[0], int(line.split()[1])) for line in lines)
    if part == 2:
        return total
    out = ""
    while total:
        total, rem = divmod(total, 65)
        digit = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#"[rem]
        out = digit + out
    return out


TEST_DATA = """\
100011101111110010101101110011 2
83546306 10
1106744474 8
170209FD 16
2557172641 8
2B290C15 16
279222446 10
6541027340 8
"""
TESTS = [
    (1, TEST_DATA, 78),
    (2, TEST_DATA, 3487996082),
    (3, TEST_DATA, "30PzDC"),
]

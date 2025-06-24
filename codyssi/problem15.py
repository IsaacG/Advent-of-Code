"""Codyssi Day N."""

import logging
import string

CHARS = string.digits + string.ascii_uppercase + string.ascii_lowercase
CHARS68 = CHARS + "!@#$%^"

log = logging.info


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    lines = data.splitlines()
    numbers = []
    for line in lines:
        num, base_str = line.split()
        base = int(base_str)
        val = 0
        for char in num:
            val = val * base + CHARS.index(char)
        numbers.append(val)
    if part == 1:
        return max(numbers)

    total = sum(numbers)
    if part == 2:
        out = []
        while total:
            total, val = divmod(total, 68)
            out.append(CHARS68[val])
        return "".join(reversed(out))
    else:  # part == 3:
        base = 1
        while base ** 4 < total:
            base *= 2
        high, low = base, base // 2
        while high > low:
            mid = (high + low) // 2
            if mid ** 4 <= total:
                low = mid + 1
            else:
                high = mid
        return high


TEST_DATA = """\
32IED4E6L4 22
1111300022221031003013 4
1C1117A3BA88 13
1100010000010010010001111000000010001100101 2
7AJ5G2AB4F 22
k6IHxTD 61"""
TESTS = [
    (1, TEST_DATA, 9047685997827),
    (2, TEST_DATA, "4iWAbo%6"),
    (3, TEST_DATA, 2366),
]

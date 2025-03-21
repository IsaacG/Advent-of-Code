"""Codyssi Day N."""

import logging
import string

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    lines = data.splitlines()
    sizes = {letter: idx for idx, letter in enumerate(string.ascii_uppercase, 1)}
    sizes |= {digit: idx for idx, digit in enumerate(string.digits)}
    if part == 2:
        compressed = []
        for line in lines:
            kept = len(line) // 10
            compressed.append(line[:kept] + str(len(line) - 2 * kept) + line[-kept:])
        lines = compressed
    if part == 3:
        compressed = []
        for line in lines:
            prev = line[0]
            count = 1
            out = ""
            for char in line[1:]:
                if char == prev:
                    count += 1
                else:
                    out += f"{count}{prev}"
                    prev = char
                    count = 1
            out += f"{count}{prev}"
            compressed.append(out)
        lines = compressed

    return sum(sizes[i] for line in lines for i in line)


TEST_DATA = """\
NNBUSSSSSDSSZZZZMMMMMMMM
PWAAASYBRRREEEEEEE
FBBOFFFKDDDDDDDDD
VJAANCPKKLZSSSSSSSSS
NNNNNNBBVVVVVVVVV"""
TESTS = [
    (1, TEST_DATA, 1247),
    (2, TEST_DATA, 219),
    (3, TEST_DATA, 539),
]

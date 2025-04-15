"""Codyssi Day N."""

import logging
import re

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    lines = data.splitlines()
    if part == 1:
        return sum(i.isalpha() for i in data)

    if part == 2:
        patterns = [re.compile(r"[0-9][-a-z]"), re.compile(r"[-a-z][0-9]")] 
    else:
        patterns = [re.compile(r"[0-9][a-z]"), re.compile(r"[a-z][0-9]")] 

    total = 0
    for line in lines:
        while True:
            original = line
            for pattern in patterns:
                line = pattern.sub("", line)
            if original == line:
                total += len(line)
                break
    return total


TEST_DATA = """\
tv8cmj0i2951190z5w44fe205k542l5818ds05ib425h9lj260ud38-l6a06
a586m0eeuqqvt5-k-8434hb27ytha3i75-lw23-0cj856l7zn8234a05eron
"""
TESTS = [
    (1, TEST_DATA, 52),
    (2, TEST_DATA, 18),
    (3, TEST_DATA, 26),
]

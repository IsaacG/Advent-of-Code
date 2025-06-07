"""i18n puzzle day N."""

import logging
import string
import unicodedata

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    return sum(
            (
                4 <= len(line) <= 12
                and {unicodedata.category(i) for i in line} >= {"Lu", "Ll", "Nd"}
                and any(i not in string.printable for i in line)
            )
        for line in data.splitlines()
    )


TEST_DATA = """\
d9Ō
uwI.E9GvrnWļbzO
ž-2á
Ģ952W*F4
?O6JQf
xi~Rťfsa
r_j4XcHŔB
71äĜ3
"""
TESTS = [
    (1, TEST_DATA, 2),
]

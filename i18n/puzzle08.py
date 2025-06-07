"""i18n puzzle day N."""

import logging
import string
import unicodedata

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    count = 0
    vowels = "aeiou"
    consonants = [i for i in string.ascii_lowercase if i not in vowels]
    for line in data.splitlines():
        if not 4 <= len(line) <= 12:
            continue
        letters = [chr(unicodedata.normalize("NFKD", i).encode()[0]).lower() for i in line]
        if len(letters) != len(set(letters)):
            continue
        if not any(i in letters for i in string.digits):
            continue
        if not any(i in letters for i in vowels):
            continue
        if not any(i in letters for i in consonants):
            continue
        count += 1
    return count


TEST_DATA = """\
iS0
V8AeC1S7KhP4Ļu
pD9Ĉ*jXh
E1-0
ĕnz2cymE
tqd~üō
IgwQúPtd9
k2lp79ąqV
"""
TESTS = [
    (1, TEST_DATA, 2),
]

"""Codyssi Day N."""

import logging
import string

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if part == 1:
        return sum(i.isalpha() for i in data)

    values = {c: v for v, c in enumerate(string.ascii_lowercase, 1)}
    values |= {c: v for v, c in enumerate(string.ascii_uppercase, 27)}
    if part == 2:
        return sum(values[i] for i in data if i in values)
    if part == 3:
        total = 0
        char_val = 0
        for char in data:
            if char.isalpha():
                char_val = values[char]
            else:
                char_val = ((2 * char_val - 5 + 51) % 52) + 1
            total += char_val
        return total


TEST_DATA = """\
t#UD$%%DVd*L?^p?S$^@#@@$pF$?xYJ$LLv$@%EXO&$*iSFZuT!^VMHy#zKISHaBj?e*#&yRVdemc#?&#Q%j&ev*#YWRi@?mNQ@eK"""
TESTS = [
    (1, TEST_DATA, 59),
    (2, TEST_DATA, 1742),
    (3, TEST_DATA, 2708),
]

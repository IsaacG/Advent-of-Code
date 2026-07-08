"""FlipFlop Codes, Puzzle 3: Password Competition."""

import itertools
import string

from lib import helpers, parsers

COLORS = {"red", "green", "blue"}
CHAR_SETS = [set(string.ascii_lowercase), set(string.ascii_uppercase), set(string.digits)]


def score(password: str, extended_rules: bool) -> int:
    """Return the score of a password."""
    chars = set(password)
    score = sum(not chars.isdisjoint(char_set) for char_set in CHAR_SETS)
    if extended_rules:
        if set(string.digits) & chars == {"7"}:
            score += 7
        run = max(len(list(group)) for char, group in itertools.groupby(password))
        if run >= 3:
            score += run * run
        if any(color in password for color in COLORS):
            score *= 3
    return len(password) * score


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if part < 3:
        return max((score(line, part == 2), line) for line in data)[1]
    return max(
        sum(score(line + char, True) for line in data)
        for char in string.ascii_lowercase + string.ascii_uppercase + string.digits
    )


TEST_DATA = """\
aaaaa111
Ks3SDblu
eowcdredkcasdblu
de333333
7dedlblu
o3klll
8ebluered
DkoGreenD7
green037"""
TESTS = [
    (1, TEST_DATA, "DkoGreenD7"),
    (2, TEST_DATA, "de333333"),
    (3, TEST_DATA, 1453),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

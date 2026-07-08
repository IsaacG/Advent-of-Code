"""FlipFlop Codes: N."""

import itertools
import string

from lib import helpers, parsers


def score(password: str, extended_rules: bool) -> int:
    """Return the score of a password."""
    score = sum(
        not set(char_set).isdisjoint(password)
        for char_set in {string.ascii_lowercase, string.ascii_uppercase, string.digits}
    )
    if extended_rules:
        if set(string.digits) & set(password) == {"7"}:
            score += 7
        run = max(len(list(b)) for a, b in itertools.groupby(password))
        if run >= 3:
            score += run * run
        if any(i in password for i in {"red", "green", "blue"}):
            score *= 3
    return len(password) * score


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if part < 3:
        return max((score(line, part == 2), line) for line in data)[1]
    return max(
        sum(score(line + c, True) for line in data)
        for c in string.ascii_lowercase + string.ascii_uppercase + string.digits
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

"""Everyone Codes Day N."""

import collections
import functools
import time
import typing
from lib import helpers
from lib import parsers


def solve(part: int, data: list[list[str | list[str]]]) -> int | str:
    """Solve the parts."""
    names, rules = typing.cast(tuple[list[str], list[list[str]]], data)

    # Parse the rules into maps.
    rule_prior = collections.defaultdict(set)
    rule_next = collections.defaultdict(set)
    for a, b in rules:
        for c in b.split(","):
            rule_next[a].add(c)
            rule_prior[c].add(a)

    @functools.cache
    def possibilities(size: int, letter: str) -> int:
        """Count the number of possible names that can be formed."""
        if size == 11:
            return 1
        count = 0 if size < 7 else 1
        size += 1
        return count + sum(possibilities(size, i) for i in rule_next[letter])

    # Dedupe names which have a prefix also included.
    if part == 3:
        filtered = set(names)
        filtered = {n for n in names if not any(n != m and n.startswith(m) for m in names)}
        names = list(filtered)

    total = 0
    for idx, name in enumerate(names, start=1):
        for a, b in zip(name, name[1:]):
            if a not in rule_prior[b]:
                break
        else:
            if part == 1:
                return name
            if part == 2:
                total += idx
            else:
                total += possibilities(len(name), name[-1])
    return total


PARSER = parsers.ParseBlocks([
    parsers.ParseMultiWords(str, separator=","),
    parsers.BaseParseMultiPerLine(word_separator=" > "),
])
TEST_DATA = [
    """\
Oronris,Urakris,Oroneth,Uraketh

r > a,i,o
i > p,w
n > e,r
o > n,m
k > f,r
a > k
U > r
e > t
O > r
t > h""",
    """\
Xanverax,Khargyth,Nexzeth,Helther,Braerex,Tirgryph,Kharverax

r > v,e,a,g,y
a > e,v,x,r
e > r,x,v,t
h > a,e,v
g > r,y
y > p,t
i > v,r
K > h
v > e
B > r
t > h
N > e
p > h
H > e
l > t
z > e
X > a
n > v
x > z
T > i""",
    """\
Xaryt

X > a,o
a > r,t
r > y,e,a
h > a,e,v
t > h
v > e
y > p,t""",
    """\
Khara,Xaryt,Noxer,Kharax

r > v,e,a,g,y
a > e,v,x,r,g
e > r,x,v,t
h > a,e,v
g > r,y
y > p,t
i > v,r
K > h
v > e
B > r
t > h
N > e
p > h
H > e
l > t
z > e
X > a
n > v
x > z
T > i""",
]
TESTS = [
    (1, TEST_DATA[0], "Oroneth"),
    (2, TEST_DATA[1], 23),
    (3, TEST_DATA[2], 25),
    (3, TEST_DATA[3], 1154),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

"""Everyone Codes Day N."""

import collections
import logging
import itertools
import math
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    total = 0
    if part in [1, 2]:
        counts = collections.defaultdict(int)
        for i in data:
            if i.isupper():
                counts[i.lower()] += 1
            else:
                if (i == "a" and part == 1) or part == 2:
                    total += counts[i]
        return total

    once  = math.ceil(1000 / len(data))
    twice = once * 2
    three = once * 3

    mentors = collections.defaultdict(set)
    for idx, m in enumerate(j for i in range(twice) for j in data):
        if m.isupper():
            mentors[m.lower()].add(idx)
    print("Done counting mentors")
    
    edges = 0
    for idx, m in enumerate(j for i in range(twice) for j in data):
        if m.islower():
            for i in mentors[m.lower()]:
                if abs(idx - i) <= 1000:
                    edges += 1
    print("edges", edges)

    mentors = collections.defaultdict(set)
    for idx, m in enumerate(j for i in range(three) for j in data):
        if m.isupper():
            mentors[m.lower()].add(idx)
    print("Done counting mentors")
    
    middle = 0
    count = 1000 - twice
    for idx, m in enumerate(data):
        if m.islower():
            for i in mentors[m.lower()]:
                if abs(idx + once * len(data) - i) <= 1000:
                    middle += 1
    print(f"{len(data)=}, {edges=}, {middle=}, {once=}, {twice=}, {three=}, {count=}, {count + twice=}")

    return edges + middle * count



TESTS = [
    (1, "ABabACacBCbca", 5),
    (2, "ABabACacBCbca", 11),
    (3, "AABCBABCABCabcabcABCCBAACBCa", 3442321),
]

if __name__ == "__main__":
    for _part, _data, expected in TESTS:
        assert solve(_part, (_data)) == expected
    print("Tests pass.")
    day = __file__.split("_", maxsplit=-1)[-1].split(".")[0]
    for _part in range(1, 4):
        with open(f"inputs/{day}.{_part}.txt", encoding="utf-8") as f:
            print(_part, solve(_part, (f.read())))

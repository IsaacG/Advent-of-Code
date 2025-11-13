"""Everyone Codes Day N."""

import itertools
import logging
import time
from lib import helpers
from lib import parsers

log = logging.info

def dist(a, b, c):
    x, y = 0, 0
    for i, j, k in zip(a, b, c):
        if i == j:
            x += 1
        if i == k:
            y += 1
        if i != j and i != k:
            return 0
    return x * y

def related(triplets):
    return any(
        dist(*((triplets * 2)[n: n + 3]))
        for n in range(3)
    )

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    dnas = [line.split(":")[-1] for line in data.splitlines()]
    if part == 1:
        for n in range(3):
            a, b, c = (dnas * 2)[n: n + 3]
            d = dist(a, b, c)
            if d: return d
    if part == 2:
        total = 0
        for triplets in itertools.combinations(dnas, 3):
            for n in range(3):
                a, b, c = (triplets * 2)[n: n + 3]
                d = dist(a, b, c)
                if d:
                    total += d
                    break
        return total

    scales = {}
    for line in data.splitlines():
        scales[line.split(":")[-1]] = int(line.split(":")[0])

    children = set()
    for triplets in itertools.combinations(dnas, 3):
        if related(triplets):
            children.add(frozenset(triplets))
    groups = []
    while children:
        this_group = {children.pop()}
        to_test = this_group.copy()
        while to_test:
            testing = to_test.pop()
            for other in list(children):
                if any(
                    related(triplets)
                    for triplets in itertools.product(testing, other, dnas)
                    if len(set(triplets)) == 3
                ):
                    children.remove(other)
                    to_test.add(other)
                    this_group.add(other)
        print(f"Found family group of size {len(this_group)}.")
        groups.append(this_group)
    most = max(len(g) for g in groups)
    for g in groups:
        if len(g) == most:
            ids = {scales[d] for f in g for d in f}
            return sum(ids)












PARSER = parsers.parse_one_str
TEST_DATA = [
    """\
1:CAAGCGCTAAGTTCGCTGGATGTGTGCCCGCG
2:CTTGAATTGGGCCGTTTACCTGGTTTAACCAT
3:CTAGCGCTGAGCTGGCTGCCTGGTTGACCGCG""",
    """\
1:GCAGGCGAGTATGATACCCGGCTAGCCACCCC
2:TCTCGCGAGGATATTACTGGGCCAGACCCCCC
3:GGTGGAACATTCGAAAGTTGCATAGGGTGGTG
4:GCTCGCGAGTATATTACCGAACCAGCCCCTCA
5:GCAGCTTAGTATGACCGCCAAATCGCGACTCA
6:AGTGGAACCTTGGATAGTCTCATATAGCGGCA
7:GGCGTAATAATCGGATGCTGCAGAGGCTGCTG""",
    """\
1:GCAGGCGAGTATGATACCCGGCTAGCCACCCC
2:TCTCGCGAGGATATTACTGGGCCAGACCCCCC
3:GGTGGAACATTCGAAAGTTGCATAGGGTGGTG
4:GCTCGCGAGTATATTACCGAACCAGCCCCTCA
5:GCAGCTTAGTATGACCGCCAAATCGCGACTCA
6:AGTGGAACCTTGGATAGTCTCATATAGCGGCA
7:GGCGTAATAATCGGATGCTGCAGAGGCTGCTG""",
    """\
1:GCAGGCGAGTATGATACCCGGCTAGCCACCCC
2:TCTCGCGAGGATATTACTGGGCCAGACCCCCC
3:GGTGGAACATTCGAAAGTTGCATAGGGTGGTG
4:GCTCGCGAGTATATTACCGAACCAGCCCCTCA
5:GCAGCTTAGTATGACCGCCAAATCGCGACTCA
6:AGTGGAACCTTGGATAGTCTCATATAGCGGCA
7:GGCGTAATAATCGGATGCTGCAGAGGCTGCTG
8:GGCGTAAAGTATGGATGCTGGCTAGGCACCCG""",
]
TESTS = [
    (1, TEST_DATA[0], 414),
    (2, TEST_DATA[1], 1245),
    (3, TEST_DATA[2], 12),
    (3, TEST_DATA[3], 36),
]

if __name__ == "__main__":
    for _part, _data, expected in TESTS:
        assert solve(_part, PARSER.parse(_data)) == expected
    print("Tests pass.")
    day = int(__file__.split("_", maxsplit=-1)[-1].split(".")[0])
    for _part in range(1, 4):
        with open(f"inputs/{day:02}.{_part}.txt", encoding="utf-8") as f:
            _input = PARSER.parse(f.read())  # type: list[list[int]]
            start = time.perf_counter_ns()
            got = solve(_part, _input)
            end = time.perf_counter_ns()
            print(f"{_part} {helpers.format_ns(end - start):8}  {got}")

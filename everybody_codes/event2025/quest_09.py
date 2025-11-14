"""Everyone Codes Day N."""

import collections.abc
import itertools
import logging
import time
from lib import helpers
from lib import parsers

log = logging.info


def degree_of_similarity(triplets: collections.abc.Iterable[str]) -> int:
    """Compute the degree of similarity for three DNA strands."""
    for child, parent_one, parent_two in itertools.permutations(triplets):
        if parent_one > parent_two:
            continue
        matches_p1, matches_p2 = 0, 0
        for base_child, base_p1, base_p2 in zip(child, parent_one, parent_two):
            if base_child == base_p1:
                matches_p1 += 1
            if base_child == base_p2:
                matches_p2 += 1
            if base_child not in [base_p1, base_p2]:
                break
        else:
            return matches_p1 * matches_p2
    return 0


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    # Parse the input. scale => dna.
    dnas = {}
    for line in data.splitlines():
        scale, dna = line.split(":")
        dnas[int(scale)] = dna

    if part in [1, 2]:
        return sum(
            degree_of_similarity(triplets)
            for triplets in itertools.combinations(dnas.values(), 3)
        )

    # Create all parent-parent-child groups.
    groups = []
    for triplets in itertools.combinations(dnas.items(), 3):
        if degree_of_similarity(dna for _, dna in triplets):
            groups.append({scale for scale, _ in triplets})

    # Combine family groups that have any overlap. Repeat until there is no change.
    prior_size = 0
    while len(groups) != prior_size:
        prior_size = len(groups)
        new_groups = []
        while groups:
            group = groups.pop()
            # Combine groups that have any overlap.
            for other in groups.copy():
                if group & other:
                    group |= other
                    groups.remove(other)
            new_groups.append(group)
        groups = new_groups
    return sum(sorted(groups, key=len)[-1])


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
            _input = PARSER.parse(f.read())  # type: str
            start = time.perf_counter_ns()
            got = solve(_part, _input)
            end = time.perf_counter_ns()
            print(f"{day:02}.{_part} {got:15} {helpers.format_ns(end - start):8}")

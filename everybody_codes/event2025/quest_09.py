"""Everyone Codes Day N."""

import logging
import math
from lib import helpers
from lib import parsers

log = logging.info


def compute_parents(dnas: dict[int, str]) -> list[tuple[int, ...]]:
    """Return a list of child-parent-parent values."""
    # Transform DNA into bitfields.
    # Bucket DNAs by one nucleotide for quickly identifying one parent.
    nucleotides = {n: 1 << idx for idx, n in enumerate("ACGT")}
    scales = {}
    bucket: dict[int, set[int]] = {i: set() for i in nucleotides.values()}
    for scale, dna in dnas.items():
        val = 0
        for char in dna:
            val = (val << 4) + nucleotides[char]
        scales[val] = scale
        bucket[val & 0b1111].add(val)

    # Create all parent-parent-child groups.
    # Optimized for speed.
    parents: list[tuple[int, ...]] = []
    for child in scales:
        parents_found = False
        bucket_key = child & 0b1111
        for p1 in scales:
            if child == p1:
                continue
            # Pick the second parent based on knowing one nucleotide matches.
            for p2 in bucket[bucket_key]:
                if p2 == child or p2 == p1:  # pylint: disable=R1714
                    continue
                if child & (p1 | p2) == child:
                    parents.append(tuple(scales[i] for i in [child, p1, p2]))
                    parents_found = True
                    break
            if parents_found:
                break
    return parents


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    # Parse the input. scale => dna.
    dnas = {}
    for line in data.splitlines():
        _scale, dna = line.split(":")
        dnas[int(_scale)] = dna

    parents = compute_parents(dnas)

    if part in [1, 2]:
        # Return the sum-of-products of the matches.
        return sum(
            math.prod(
                # Count pair-wise matches between the child and a parent.
                sum(base_child == base_parent for base_child, base_parent in zip(dnas[child], parent))
                for parent in [dnas[p] for p in parents]
            )
            for child, *parents in parents
        )

    # Combine family groups that have any overlap. Repeat until there is no change.
    families: list[set[int]] = [set(i) for i in parents]
    prior_size = 0
    while len(families) != prior_size:
        prior_size = len(families)
        new_groups = []
        while families:
            group = families.pop()
            # Combine families that have any overlap.
            for other in families.copy():
                if group & other:
                    group |= other
                    families.remove(other)
            new_groups.append(group)
        families = new_groups
    return sum(sorted(families, key=len)[-1])


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
    helpers.run_solution(globals())

"""Everyone Codes Day N."""

import collections
import logging
from lib import helpers
from lib import parsers

TR = str.maketrans({c: "0" for c in "srgb"} | {c: "1" for c in "SRGB"})


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    scales = []
    for line in data:
        if ":" not in line:
            print(line)
        scale_id, raw_colors = line.split(":")
        colors = [int(color.translate(TR), 2) for color in raw_colors.split()]
        scales.append([int(scale_id)] + colors)

    if part == 1:
        return sum(
            scale_id
            for scale_id, red, green, blue in scales
            if green > red and green > blue
        )

    if part == 2:
        want_shine = max(shine for *_, shine in scales)
        color = min(
            sum(colors)
            for _, *colors, shine in scales
            if shine == want_shine
        )
        return sum(
            scale_id
            for scale_id, *colors, shine in scales
            if sum(colors) == color
            and shine == want_shine
        )

    groups = collections.defaultdict(set)
    for scale_id, *colors, shine in scales:
        highest = max(colors)
        if colors.count(highest) == 1 and (shine <= 30 or shine >= 33):
            groups[shine < 33, colors.index(highest)].add(scale_id)
    largest_group = max(groups, key=lambda x: len(groups[x]))
    return sum(groups[largest_group])


PARSER = parsers.parse_one_str_per_line
TEST_DATA = [
    """\
2456:rrrrrr ggGgGG bbbbBB
7689:rrRrrr ggGggg bbbBBB
3145:rrRrRr gggGgg bbbbBB
6710:rrrRRr ggGGGg bbBBbB""",
    """\
2456:rrrrrr ggGgGG bbbbBB sSsSsS
7689:rrRrrr ggGggg bbbBBB ssSSss
3145:rrRrRr gggGgg bbbbBB sSsSsS
6710:rrrRRr ggGGGg bbBBbB ssSSss""",
    """\
15437:rRrrRR gGGGGG BBBBBB sSSSSS
94682:RrRrrR gGGggG bBBBBB ssSSSs
56513:RRRrrr ggGGgG bbbBbb ssSsSS
76346:rRRrrR GGgggg bbbBBB ssssSs
87569:rrRRrR gGGGGg BbbbbB SssSss
44191:rrrrrr gGgGGG bBBbbB sSssSS
49176:rRRrRr GggggG BbBbbb sSSssS
85071:RRrrrr GgGGgg BBbbbb SSsSss
44303:rRRrrR gGggGg bBbBBB SsSSSs
94978:rrRrRR ggGggG BBbBBb SSSSSS
26325:rrRRrr gGGGgg BBbBbb SssssS
43463:rrrrRR gGgGgg bBBbBB sSssSs
15059:RRrrrR GGgggG bbBBbb sSSsSS
85004:RRRrrR GgGgGG bbbBBB sSssss
56121:RRrRrr gGgGgg BbbbBB sSsSSs
80219:rRRrRR GGGggg BBbbbb SssSSs""",
]
TESTS = [
    (1, TEST_DATA[0], 9166),
    (2, TEST_DATA[1], 2456),
    (3, TEST_DATA[2], 292320),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

"""Everyone Codes Day N."""

import collections
import logging
from lib import helpers
from lib import parsers

log = logging.info
TR = str.maketrans({c: "0" for c in "srgb"} | {c: "1" for c in "SRGB"})


def to_val(color):
    return int(color.translate(TR), 2)
    
def solve(part: int, data: str) -> int:
    """Solve the parts."""
    out = 0
    numbers = []
    for line in data.splitlines():
        if ":" not in line:
            print(line)
        lid, rest = line.split(":")
        colors = [to_val(i) for i in rest.split()]
        numbers.append([int(lid)] + colors)
    if part == 1:
        return sum(
            lid
            for lid, *colors in numbers
            if colors[1] > colors[0] and colors[1] > colors[2]
        )
    if part == 2:
        want_shine = max(n[4] for n in numbers)
        color = min(sum(n[1:4]) for n in numbers if n[4] == want_shine)
        return sum(n[0] for n in numbers if sum(n[1:4]) == color and n[4] == want_shine)

    groups = collections.defaultdict(set)
    for lid, *colors, shine in numbers:
        highest = max(colors)
        if 30 < shine < 33 or colors.count(highest) != 1:
            continue
        groups[shine < 33, colors.index(highest)].add(lid)
    largest_group = max(groups, key=lambda x: len(groups[x]))
    return sum(groups[largest_group])

        


PARSER = parsers.parse_one_str
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

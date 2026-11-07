"""Everyone Codes Event 2026 Day N."""

import collections
import itertools
import logging
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str, testing) -> int:
    """Solve the parts."""
    hits = 10 if testing else 10000
    hits = 10000 if part == 2 else 1000000000000
    spaces = data.coords.get(">", set()) | data.coords.get("<", set()) | data.coords.get("v", set()) | data.coords.get("^", set()) | data.coords["."]
    ghosts = [(pos, direction, 0) for char, direction in helpers.ARROW_DIRECTIONS_T.items() for pos in data.coords.get(char, [])]
    ghosts = [(idx, *d) for idx, d in enumerate(ghosts)]
    # for pos, _ in ghosts:
    #     assert pos in spaces
    # print(ghosts)
    # print(spaces)
    collisions = 0
    seen = {}
    skips = 0

    for rnd in itertools.count(1):
        s = ghosts.copy()
        next_ghosts = []
        wall_coll = 0
        for gid, pos, direction, count in ghosts:
            npos = pos[0] + direction[0], pos[1] + direction[1]
            if npos not in spaces:
                direction = helpers.rotate_counterclockwise(*direction)
                npos = pos
                wall_coll += 1
                count += 1
            if part == 1 or count < hits:
                next_ghosts.append((gid, npos, direction, count))
        ghosts = next_ghosts
        collisions += wall_coll

        shared = collections.Counter(pos for gid, pos, _, _ in ghosts)
        next_ghosts = []
        ghost_coll = 0
        for gid, pos, direction, count in ghosts:
            if shared[pos] > 1:
                ghost_coll += 1
                direction = (-direction[0], -direction[1])
                count += 1
            if part == 1 or count < hits:
                next_ghosts.append((gid, pos, direction, count))
        ghosts = next_ghosts
        collisions += ghost_coll

        if part == 1:
            print(f"{rnd=}, {wall_coll=}, {ghost_coll=}")
        if part == 1 and rnd == 10:
            return collisions

        if False:
            print(rnd)
            print(f"Round: {rnd}")
            print(f"Collisions this round: {ghost_coll + wall_coll}")
            print(f"Disappeared: {len(s) - len(ghosts)}")
            print()

            gs = [p for p, _, _ in ghosts]
            for y in range(data.height):
                l = ""
                for x in range(data.width):
                    if (x, y) not in spaces:
                        l += "#"
                    elif (x, y) in shared and shared[x, y] > 1:
                        l += str(shared[x, y])
                    elif (x, y) in gs:
                        d = next(d for p, d, c in ghosts if p == (x, y))
                        l += next(c for c, direction in helpers.ARROW_DIRECTIONS_T.items() if d == direction)
                    else:
                        l += "."
                print(l)
            print()

            for idx, pos, direction, count in ghosts:
                print(f"position={pos}, direction={next(c for c, d in helpers.ARROW_DIRECTIONS_T.items() if d == direction)}, remaining collisions={10 - count}")
            print()
        if part > 1 and not ghosts:
            return rnd + skips

        ghosts.sort()
        fp = tuple(i for idx, pos, direction, count in ghosts for i in (*pos, *direction))
        counts = [count for idx, pos, direction, count in ghosts]
        if fp in seen:
            print(rnd, seen[fp][0])
            print(counts, seen[fp][1])
            rnd_stride = rnd - seen[fp][0]
            steps = min((hits - 1 - a) // (a - b) for a, b in zip(counts, seen[fp][1]) if a != b)
            skips += rnd_stride * steps
            ghosts = [
                (idx, pos, direction, count + (count - b) * steps)
                for (idx, pos, direction, count), b in zip(ghosts, seen[fp][1])
            ]

        seen[fp] = (rnd, [count for idx, pos, direction, count in ghosts])







# PARSER = parsers.parse_one_str
TEST_DATA = [
    """\
###########
#####.#####
###.....###
##.......##
##.>>.<<.##
#v...>...v#
##...v...##
##.......##
###.....###
#####.#####
###########""",
    """\
###########
#####.#####
###.....###
##.......##
##.>>.<<.##
#v...>...v#
##...v...##
##.......##
###.....###
#####.#####
###########""",
    """\
#######################
###########.###########
#######.^>.^.<^.#######
#####..<.>.v^>>^^<#####
####..v<^v.>.>v..^.####
###.................###
###.................###
##.......<...<.<....>##
##...v....>....v.v<.^##
##........###........##
##v......#####.......##
#.<......#####......>.#
##.......#####.......##
##........###........##
##...................##
##...................##
###.................###
###.................###
####...............####
#####.............#####
#######....v....#######
###########.###########
#######################""",
    """\
""",
    """\
""",
]
TESTS = [
    (1, TEST_DATA[0], 29),
    (2, TEST_DATA[1], 50000),
    (3, TEST_DATA[2], 13314695352588),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

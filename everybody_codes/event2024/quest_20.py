"""Everyone Codes Day N."""

import collections
import functools
import itertools
import logging
import queue

DIRECTIONS = {(0, 1), (0, -1), (1, 0), (-1, 0)}
log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    chars = {i for i in data} | {"."} - {"\n"}
    lines = data.splitlines()
    maps = {
        char: {
            (x, y)
            for y, line in enumerate(lines)
            for x, ch in enumerate(line)
            if ch == char
        }
        for char in chars
    }
    for k, v in maps.items():
        if k.isalpha():
            maps["."] |= v

    if part == 1:
        return p1(maps)
    if part == 2:
        return p2(maps)


def p2(maps):
    points = ["S"] + sorted(i for i in maps if i.isalpha() and i != "S") + ["S"]
    deltas = {p: -1 for p in maps["."]} | {p: -2 for p in maps["-"]} | {p: 1 for p in maps["+"]}

    def is_cluster(start):
        x, y = start

        clumps = [
            [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)],
            [(x, y), (x - 1, y), (x, y + 1), (x - 1, y + 1)],
            [(x, y), (x + 1, y), (x, y - 1), (x + 1, y - 1)],
            [(x, y), (x - 1, y), (x, y - 1), (x - 1, y - 1)],
        ]
        return any(all(i in maps["+"] for i in clump) for clump in clumps)

    logging.debug("Build clusters")
    clusters = {i for i in maps["+"] if is_cluster(i)}
    logging.debug("Done building clusters. Found %d positions.", len(clusters))

    legs = {}

    for start, end in zip(points, points[1:]):
        logging.debug(f"Compute routes {start}-{end}")
        dest = maps[end].copy().pop()
        pos = maps[start].copy().pop()
        best = {pos: (0, False, frozenset())}
        todo = {(pos, False)}
        for steps in range(1, 500):
            next_todo = set()
            for position, hit_cluster in todo:
                seen = best[position][2]
                next_seen = frozenset(seen | {position})
                for d in DIRECTIONS:
                    next_pos = (position[0] + d[0], position[1] + d[1])
                    if next_pos not in deltas or next_pos in seen:
                        continue
                    next_altitude = best[position][0] + deltas[next_pos]
                    next_hit = hit_cluster or next_pos in clusters
                    if next_pos not in best or (position not in best[next_pos][2] and (next_altitude > best[next_pos][0] or (next_altitude == best[next_pos][0] and next_hit))):
                        best[next_pos] = (next_altitude, next_hit, next_seen)
                        next_todo.add((next_pos, next_hit))
            todo = next_todo
            if not todo:
                break
        legs[end] = (steps,) + best[dest][:2]

    log(f"{legs=}")
    steps = sum(i[0] for i in legs.values())
    delta = -min(sum(i[1] for i in legs.values()), 0)
    log(f"{steps=}, {delta=}")
    # assert any(i[2] for i in legs.values()) or delta == 0
    if delta % 2:
        delta += 1
    return steps + delta
    

def p1(maps):
    def is_cluster(start):
        todo = {
            ((start[0] + x, start[1] + y), (x, y))
            for x, y in DIRECTIONS
            if (start[0] + x, start[1] + y) in maps["+"]
        }
        seen = todo.copy()
        while todo:
            pos, direction = todo.pop()
            for x, y in DIRECTIONS - {(-direction[0], -direction[1])}:
                next_pos = (pos[0] + x, pos[1] + y)
                if next_pos == start:
                    return True
                if (next_pos, (x, y)) in seen or next_pos not in maps["+"]:
                    continue
                seen.add((next_pos, (x, y)))
                todo.add((next_pos, (x, y)))
        return False

    logging.debug("Build clusters")
    clusters = {i for i in maps["+"] if is_cluster(i)}
    logging.debug("Done building clusters. Found %d positions.", len(clusters))

    deltas = {p: -1 for p in maps["."]} | {p: -2 for p in maps["-"]} | {p: 1 for p in maps["+"]}
    altitude = 1000
    position = maps["S"].pop()

    best = {position: 0}
    seen = set()
    todo = {position}
    for steps in range(100):
        next_todo = set()
        for position in todo:
            for d in DIRECTIONS:
                next_pos = (position[0] + d[0], position[1] + d[1])
                if next_pos in seen or next_pos not in deltas:
                    continue
                next_altitude = best[position] + deltas[next_pos]
                next_todo.add(next_pos)
                if next_pos not in best or next_altitude > best[next_pos]:
                    best[next_pos] = next_altitude
        seen |= next_todo
        todo = next_todo
        found = todo & clusters
        if found:
            return max(best[i] for i in found) + 100 - steps + 1000


TEST_DATA = [
    """\
#....S....#
#.........#
#---------#
#.........#
#..+.+.+..#
#.+-.+.++.#
#.........#""",
    """\
####S####
#-.+++.-#
#.+.+.+.#
#-.+.+.-#
#A+.-.+C#
#.+-.-+.#
#.+.B.+.#
#########""",
    """\
###############S###############
#+#..-.+.-++.-.+.--+.#+.#++..+#
#-+-.+-..--..-+++.+-+.#+.-+.+.#
#---.--+.--..++++++..+.-.#.-..#
#+-+.#+-.#-..+#.--.--.....-..##
#..+..-+-.-+.++..-+..+#-.--..-#
#.--.A.-#-+-.-++++....+..C-...#
#++...-..+-.+-..+#--..-.-+..-.#
#..-#-#---..+....#+#-.-.-.-+.-#
#.-+.#+++.-...+.+-.-..+-++..-.#
##-+.+--.#.++--...-+.+-#-+---.#
#.-.#+...#----...+-.++-+-.+#..#
#.---#--++#.++.+-+.#.--..-.+#+#
#+.+.+.+.#.---#+..+-..#-...---#
#-#.-+##+-#.--#-.-......-#..-##
#...+.-+..##+..+B.+.#-+-++..--#
###############################""",
    """\
###############S###############
#-----------------------------#
#-------------+++-------------#
#-------------+++-------------#
#-------------+++-------------#
#-----------------------------#
#-----------------------------#
#-----------------------------#
#--A-----------------------C--#
#-----------------------------#
#-----------------------------#
#-----------------------------#
#-----------------------------#
#-----------------------------#
#-----------------------------#
#--------------B--------------#
#-----------------------------#
#-----------------------------#
###############################"""
]
TESTS = [
    # (1, TEST_DATA[0], 1045),
    (2, TEST_DATA[1],  24),
    (2, TEST_DATA[2],  78),
    (2, TEST_DATA[3], 206),
    # (3, TEST_DATA[2], None),
]

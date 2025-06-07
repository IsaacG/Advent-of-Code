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

    log("Build clusters")
    clusters = {i for i in maps["+"] if is_cluster(i)}
    log("Done building clusters. Found %d positions.", len(clusters))


    if part == 1:
        return p1(maps, clusters)
    if part == 2:
        return p2(maps, clusters)


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def p2(maps, clusters):
    points = ["S"] + sorted(i for i in maps if i.isalpha() and i != "S") + ["S"]
    deltas = {p: -1 for p in maps["."]} | {p: -2 for p in maps["-"]} | {p: 1 for p in maps["+"]}

    legs = {}
    improvements = collections.defaultdict(dict)

    for start, end in zip(points, points[1:]):
        log(f"Compute routes {start}-{end}")
        dest = maps[end].copy().pop()
        pos = maps[start].copy().pop()
        q = queue.PriorityQueue()
        seen = {(pos, direction) for direction in DIRECTIONS}
        min_step_count = None
        max_altitude = None
        for direction in DIRECTIONS:
            # score (manhattan + steps), steps, altitude, pos, direction
            q.put((manhattan(pos, dest), 0, 0, pos, direction))
        while not q.empty():
            _, altitude, steps, position, direction = q.get()
            if position == dest:
                if min_step_count is None:
                    min_step_count = steps
                    max_altitude = altitude
                else:
                    if steps == min_step_count:
                        max_altitude = max(max_altitude, altitude)
                    else:
                        improvements[end][steps - min_step_count] = max(improvements.get(steps - min_step_count, 0), altitude - max_altitude)
                continue

            if q.qsize() > 10_000_000:
                break

            steps += 1
            if min_step_count and steps > min_step_count + 10:
                break
            for d in DIRECTIONS - {(-direction[0], -direction[1])}:
                next_pos = (position[0] + d[0], position[1] + d[1])
                if (next_pos, d) in seen or next_pos not in deltas:
                    continue
                next_altitude = altitude + deltas[next_pos]
                q.put((manhattan(next_pos, dest) + steps, next_altitude, steps, next_pos, d))
        legs[end] = (min_step_count, max_altitude)
        improvements[end][0] = 0

    steps = sum(i[0] for i in legs.values())
    delta = sum(i[1] for i in legs.values())
    log(f"{steps=}, {delta=}, {improvements=}")

    if delta >= 0:
        return steps
    delta = -delta
    can_do = set()
    for modifications in itertools.product(*[((k, v) for k, v in a.items() if k == 0 or v != 0) for a in improvements.values()]):
        extra_steps = sum(i[0] for i in modifications)
        extra_elevation = sum(i[1] for i in modifications)
        if extra_elevation >= delta:
            can_do.add(extra_steps)
    return min(can_do) + steps
    

def p1(maps, clusters):
    deltas = {p: -1 for p in maps["."]} | {p: -2 for p in maps["-"]} | {p: 1 for p in maps["+"]}
    
    altitude = 1000
    direction = (0, 1) # arbitrary but ought to work in p1
    position = maps["S"].pop()

    # score = -1 * (steps_remaining + altitude)
    q = queue.PriorityQueue()
    q.put((-(altitude + 100), altitude, position, direction, 100))
    seen = {position}

    while not q.empty():
        score, altitude, position, direction, steps_left = q.get()
        if position in clusters:
            return altitude + steps_left
        if steps_left == 0:
            return altitude
        next_steps_left = steps_left - 1
        for d in DIRECTIONS - {(-direction[0], -direction[1])}:
            next_pos = (position[0] + d[0], position[1] + d[1])
            if next_pos in seen or next_pos not in deltas:
                continue
            if clusters:
                seen.add(next_pos)
            next_altitude = altitude + deltas[next_pos]
            if next_altitude < 0:
                continue
            q.put((-(next_altitude + next_steps_left), next_altitude, next_pos, d, next_steps_left))


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
    # (2, TEST_DATA[1],  24),
    (2, TEST_DATA[2],  78),
    (2, TEST_DATA[3], 206),
    # (3, TEST_DATA[2], None),
]

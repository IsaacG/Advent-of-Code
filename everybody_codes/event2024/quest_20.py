"""Everyone Codes Day N."""

import collections
import functools
import itertools
import logging
import queue
import time

DIRECTIONS = {(0, 1), (0, -1), (1, 0), (-1, 0)}
NEXT_DIR = {
    (0, +1): [(0, +1), (+1, 0), (-1, 0)],
    (0, -1): [(0, -1), (+1, 0), (-1, 0)],
    (+1, 0): [(0, +1), (0, -1), (+1, 0)],
    (-1, 0): [(0, +1), (0, -1), (-1, 0)],
}

log = logging.info

def solve(part: int, data: str, testing: bool) -> int:
    """Solve the parts."""
    chars = set(".+-SABC")
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
        if k in "SABC":
            maps["."] |= v

    if part == 1:
        return p1(maps)
    if part == 2:
        return p2(maps, testing)
    if part == 3:
        return p3(data)


def compute_loop(best):
    choice = {}
    for start, nexts in best.items():
        gliders = {start: 0}
        opts = {}
        for n in range(1, len(best) * 8):
            next_pos = {}
            for src, drop in gliders.items():
                for dst, moredrop in nexts.items():
                    combined = drop + moredrop
                    if dst not in next_pos or next_pos[dst] < combined:
                        next_pos[dst] = combined
            opts[n] = next_pos[start]
        choice[start] = max(((steps, elevation) for steps, elevation in opts.items()), key=lambda x: x[1] / x[0])
    return choice


def compute_drops(width, height, delta):
    starts = {(x, 0) for x in range(width) if (x, 0) in delta and (x, height - 1) in delta}
    ends = {(x, height - 1) for x, _ in starts}
    routes = {}
    next_dir = {
        (0, +1): [(0, +1), (+1, 0), (-1, 0)],
        (0, -1): [(0, -1), (+1, 0), (-1, 0)],
        (+1, 0): [(0, +1), (0, -1), (+1, 0)],
        (-1, 0): [(0, +1), (0, -1), (-1, 0)],
    }

    def candidates(pos, direction):
        x, y = pos
        for dx, dy in next_dir[direction]:
            n = x + dx, y + dy
            if n in delta:
                yield n, (dx, dy)

    for start in starts:
        q = collections.deque([(start, (0, 1), 0)])
        best = {(start, (0, 1)): 0}
        while q:
            pos, direction, elevation = q.popleft()
            for n_pos, d_dir in candidates(pos, direction):
                n_elev = elevation + delta[n_pos]
                if (n_pos, d_dir) in best and best[n_pos, d_dir] >= n_elev:
                    continue
                best[n_pos, d_dir] = n_elev
                q.append((n_pos, d_dir, n_elev))
        frame = {}
        for end in ends:
            pick = max(best[end, direction] for direction in [(0, +1), (+1, 0), (-1, 0)] if (end, direction) in best)
            next_pos = end[0], 0
            frame[end[0]] = pick + delta[end[0], 0]
        routes[start[0]] = frame
    return routes


def p3(data: str):
    delta = {}
    start = (0, 0)
    for y, line in enumerate(data.splitlines()):
        height = y
        for x, char in enumerate(line):
            if char == "+":
                delta[x, y] = +1
            elif char == "-":
                delta[x, y] = -2
            elif char == ".":
                delta[x, y] = -1
            elif char == "S":
                delta[x, y] = -1
                start = (x, y)
    width = len(data.splitlines()[0])
    height = len(data.splitlines())

    cycle_drops = compute_drops(width, height, delta)
    loop = compute_loop(cycle_drops)
    print(cycle_drops)
    print(loop)

def p2(maps, testing):
    deltas = {p: -1 for p in maps["."]}
    deltas |= {p: -2 for p in maps["-"]} | {p: 1 for p in maps["+"]}

    checkpoints = {maps[char].copy().pop(): char for char in "ABCS"}
    start = maps["S"].copy().pop()
    goals = {"A": "B", "B": "C", "C": "S"}
    board = set(deltas)

    def candidates(pos, direction):
        x, y = pos
        for dx, dy in NEXT_DIR[direction]:
            n = x + dx, y + dy
            if n in board:
                yield n, (dx, dy)

    bound = 125
    lower, upper = 10000 - bound, 10000 + bound
    possibilities = {(start, (0, 1), "A"): 10000}
    for step in range(1, 800):
        next_possibilities = {}
        # log(f"{step=}, {len(possibilities)=}")
        for (position, direction, goal), elevation in possibilities.items():
            for next_pos, next_dir in candidates(position, direction):
                next_elev = elevation + deltas[next_pos]
                if not lower <= next_elev <= upper:
                    continue
                next_goal = goal
                if checkpoints.get(next_pos) == next_goal:
                    if next_goal == "S":
                        if next_elev >= 10000:
                            return step
                        continue
                    else:
                        next_goal = goals[next_goal]
                fp = (next_pos, next_dir, next_goal)
                next_possibilities[fp] = max(next_possibilities.get(fp, 0), next_elev)
        possibilities = next_possibilities


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


PARSER = str
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
###############################""",
    """\
#......S......#
#-...+...-...+#
#.............#
#..+...-...+..#
#.............#
#-...-...+...-#
#.............#
#..#...+...+..#""",
]
TESTS = [
    # (1, TEST_DATA[0], 1045),
    (2, TEST_DATA[1],  24),
    (2, TEST_DATA[2],  78),
    (2, TEST_DATA[3], 206),
    (3, TEST_DATA[4], 768790),
]

if __name__ == "__main__":
    day = int(__file__.split("_", maxsplit=-1)[-1].split(".")[0])
    test_data = TESTS
    _part = 2
    parser = str

    for i, (p, _data, expected) in enumerate(test_data):
        if p == _part:
            log("Test", i)
            assert solve(_part, _data, testing=True) == expected
    log("Tests pass.")
    with open(f"inputs/{day:02}.{_part}.txt", encoding="utf-8") as f:
        _input = parser(f.read())  # type: str
        start = time.perf_counter_ns()
        got = solve(_part, _input, testing=False)
        end = time.perf_counter_ns()
        print(f"{day:02}.{_part} {got:15} {(end - start)//1000000:8}")

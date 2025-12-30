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


def p2(maps, testing):
    deltas = {p: -1 for p in maps["."]}
    deltas |= {p: -2 for p in maps["-"]} | {p: 1 for p in maps["+"]}

    def distance(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    board = set().union(*[m for m in maps.values()])
    checkpoint_pos = {char: maps[char].copy().pop() for char in "ABCS"}
    start = checkpoint_pos["S"]
    deltas[start] = -1
    checkpoint_numbers = {pos: "ABCS".index(char) for char, pos in checkpoint_pos.items()}
    seen_pos = {v: k for k, v in checkpoint_numbers.items()} | {4: start}
    next_checkpoint = ["A", "B", "C", "S"]
    additional_steps = {}
    additional_steps[4] = 0
    additional_steps[3] = 0
    additional_steps[2] = distance(checkpoint_pos["C"], checkpoint_pos["S"]) + additional_steps[3]
    additional_steps[1] = distance(checkpoint_pos["B"], checkpoint_pos["C"]) + additional_steps[2]
    additional_steps[0] = distance(checkpoint_pos["A"], checkpoint_pos["B"]) + additional_steps[1]

    def h(pos, seen):
        return distance(pos, seen_pos[seen]) + additional_steps[seen]

    def candidates(pos, direction):
        x, y = pos
        for dx, dy in NEXT_DIR[direction]:
            n = x + dx, y + dy
            if n in board:
                yield n, (dx, dy)

    max_rank = 210 if testing else 750

    for bound in range(100, 101):
        lower, upper = 10000 - bound, 10000 + bound
        # A*: score, elapsed time, elevation, 
        q = queue.PriorityQueue()
        q.put((0, 0, 10000, start, (0, 1), 0))
        # Map position/direction/checkpoints to (time, elevation) to help prune
        seen = collections.defaultdict(set)
        while not q.empty():
            rank, elapsed, elevation, pos, direction, checkpoints_checked = q.get()

            if q.qsize() > 9_000_000:
                log(f"too much q w/ {bound=}")
                break

            if checkpoints_checked == 4:
                if elevation >= 10000:
                    return elapsed
                continue
            elapsed += 1

            if rank > max_rank:
                continue

            for next_pos, next_dir in candidates(pos, direction):
                next_elevation = elevation + deltas[next_pos]
                next_checkpoints_collected = checkpoints_checked
                if next_pos in checkpoint_numbers and checkpoint_numbers[next_pos] == checkpoints_checked:
                    next_checkpoints_collected += 1

                fp = (next_pos, next_dir, next_checkpoints_collected)
                if fp in seen:
                    if any(elapsed > i[0] and next_elevation < i[1] for i in seen[fp]):
                        continue

                if not lower < next_elevation < upper: continue

                seen[fp].add((elapsed, next_elevation))
                q.put((elapsed + h(next_pos, next_checkpoints_collected), elapsed, next_elevation, next_pos, next_dir, next_checkpoints_collected))


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
###############################"""
]
TESTS = [
    # (1, TEST_DATA[0], 1045),
    (2, TEST_DATA[1],  24),
    (2, TEST_DATA[2],  78),
    (2, TEST_DATA[3], 206),
    # (3, TEST_DATA[2], None),
]

if __name__ == "__main__":
    day = int(__file__.split("_", maxsplit=-1)[-1].split(".")[0])
    test_data = TESTS
    _part = 2
    parser = str

    for i, (p, _data, expected) in enumerate(test_data):
        if p == _part:
            print("Test", i)
            assert solve(_part, _data, testing=True) == expected
    print("Tests pass.")
    with open(f"inputs/{day:02}.{_part}.txt", encoding="utf-8") as f:
        _input = parser(f.read())  # type: str
        start = time.perf_counter_ns()
        got = solver(_part, _input, testing=False)
        end = time.perf_counter_ns()
        print(f"{day:02}.{_part} {got:15} {helpers.format_ns(end - start):8}")

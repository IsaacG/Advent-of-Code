"""FlipFlop Codes: N."""

import collections
import curses
import queue
import logging
from lib import helpers, parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    spaces = data.coords["S"] | data.coords["E"] | data.coords["."]
    walls = data.coords["#"]
    start = data.coords["S"].copy().pop()
    end = data.coords["E"].copy().pop()
    
    seen = {end}
    distance = {}
    todo = collections.deque()
    todo.append((0, end))
    while todo:
        steps, pos = todo.popleft()
        distance[pos] = steps
        steps += 1

        for n in helpers.neighbors_t(*pos):
            if n not in seen and n in spaces:
                seen.add(n)
                todo.append((steps, n))

    seen = {start}

    if part == 1:
        return distance[start]

    if part == 2:
        todo = queue.PriorityQueue()
        todo.put((0, start))
        while not todo.empty():
            steps, pos = todo.get()
            if pos == end:
                return steps
            steps += 1

            for n in helpers.neighbors_t(*pos):
                if n not in seen and n in spaces:
                    seen.add(n)
                    todo.put((steps, n))
            x, y = pos
            for dx, dy in helpers.FOUR_DIRECTIONS_T:
                n = pos
                n2 = (n[0] + dx, n[1] + dy)
                while n2 in spaces:
                    n = n2
                    n2 = (n[0] + dx, n[1] + dy)
                if n not in seen and n in spaces:
                    seen.add(n)
                    todo.put((steps, n))

    if part == 3:
        # stdscr = curses.initscr()

        counter = 0
        default = 10000
        todo = queue.PriorityQueue()

        seen = {}
        todo.put((0, start, False, tuple()))

        while todo:
            counter += 1
            steps, pos, on_portal, path = todo.get()
            if not counter % 50000:
                log("Count %d: Q %d, steps %d, dist %d", counter, todo.qsize(), steps, distance[pos])
            if pos == end:
                # print(path)
                return steps

            # Option one: no portals.
            for n in helpers.neighbors_t(*pos):
                state = (n, False)
                if n in spaces and seen.get(state, default) > steps + 1:
                    seen[state] = steps + 1
                    todo.put((steps + 1, *state, path + tuple(("W", n))))

            # No adjacent wall to open a portal
            if all(n in spaces for n in helpers.neighbors_t(*pos)):
                continue

            # Option two: use a portal.
            # Consider where to open the other end.
            for dx, dy in helpers.FOUR_DIRECTIONS_T:
                n = pos
                while (n2 := (n[0] + dx, n[1] + dy)) not in walls:
                    n = n2
                if n == pos:
                    continue
                moves = 2 if on_portal else 3
                state = (n, True)
                if seen.get(state, default) > steps + moves:
                    seen[state] = steps + moves
                    todo.put((steps + moves, *state, path + tuple(("T", n))))


# PARSER = parsers.parse_one_str
TEST_DATA = ["""\
###########
#S#.#...#.#
#.#.#.###.#
#.#.......#
#.#.#.#####
#...#.#..E#
###.#.#.###
#...#.#...#
#.###.#.#.#
#.#.....#.#
###########""",
    """\
#######
#S....#
#####.#
#E#.#.#
#.###.#
#.....#
#######"""
]
TESTS = [
    (1, TEST_DATA[0], 24),
    (2, TEST_DATA[0], 10),
    (3, TEST_DATA[1], 9),
]


if __name__ == "__main__":
    helpers.run_solution(globals())

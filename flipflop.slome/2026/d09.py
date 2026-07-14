"""FlipFlop Codes: N."""

import collections
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
        counter = 0
        todo = queue.PriorityQueue()
        # Start with portals outside the map
        blue, orange = ((-100000, -1000000), (-100000, -100000)), ((-200000, -200000), (-200000, -200000))
        seen = {(start, blue, orange)}
        for portal in blue, orange:
            distance[portal[0]] = 1000000

        def add(steps, pos, p1, p2):
            if pos not in spaces:
                return
            if p1[0] == p2[0]:
                return
            if p1 > p2:
                p1, p2 = p2, p1
            if (pos, p1, p2) in seen:
                return
            seen.add((pos, p1, p2))
            todo.put((0, steps, pos, p1, p2))

        add(0, start, blue, orange)

        while todo:
            counter += 1
            _, steps, pos, blue, orange = todo.get()
            if steps >= 1380:  # >500 <1380
                continue
            if not counter % 50000:
                log("Count %d: Q %d, steps %d, dist %d", counter, todo.qsize(), steps, distance[pos])
            if pos == end:
                return steps
            steps += 1

            for n in helpers.neighbors_t(*pos):
                for portal_a, portal_b in [(blue, orange), (orange, blue)]:
                    if (pos, n) == portal_a:
                        n2 = portal_b[0]
                        if distance[n2] < distance[pos]:
                            add(steps, n2, blue, orange)
                add(steps, n, blue, orange)

            x, y = pos
            for dx, dy in helpers.FOUR_DIRECTIONS_T:
                n = pos
                n2 = (n[0] + dx, n[1] + dy)
                while n2 in spaces:
                    n = n2
                    n2 = (n[0] + dx, n[1] + dy)
                m = (n, n2)
                if distance[n] <= distance[pos]:
                    add(steps, pos, m, orange)
                if distance[n] <= distance[pos]:
                    add(steps, pos, m, blue)


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

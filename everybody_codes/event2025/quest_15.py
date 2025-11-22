"""Everyone Codes Day N."""

import collections
import logging
import queue
from lib import helpers
from lib import parsers

log = logging.info
HEADINGS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    x, y = 0, 0
    heading = 0
    walls = set()

    for instruction in data.split(","):
        direction, distance_raw = instruction[0], instruction[1:]
        if direction == "L":
            heading = (heading + 3) % 4
        else:
            heading = (heading + 1) % 4
        sx, sy = x + HEADINGS[heading][0], y + HEADINGS[heading][1]
        nx, ny = x + int(distance_raw) * HEADINGS[heading][0], y + int(distance_raw) * HEADINGS[heading][1]
        ax, bx = min(sx, nx), max(sx, nx)
        ay, by = min(sy, ny), max(sy, ny)
        walls.add((ax, ay, bx, by))
        x, y = nx, ny
    end = (x, y)

    def dist(pos):
        return abs(end[0] - pos[0]) + abs(end[1] - pos[1])

    def is_wall(pos):
        if pos == end:
            return False
        x, y = pos
        for ax, ay, bx, by in walls:
            if ax <= x <= bx and ay <= y <= by:
                return True
        return False

    seen = set([(0, 0)])
    q = queue.PriorityQueue()
    q.put((0, 0, (0, 0)))
    while q:
        _, steps, pos = q.get()
        if pos == end:
            if part == 3:
                assert steps != 952381124
            return steps
        steps += 1
        for dx, dy in HEADINGS:
            new = (pos[0] + dx, pos[1] + dy)
            if (new in seen) or is_wall(new):
                continue
            seen.add(new)
            q.put((steps + dist(new), steps, new))



PARSER = parsers.parse_one_str
TEST_DATA = [
]
TESTS = [
    (1, "R3,R4,L3,L4,R3,R6,R9", 6),
    (1, "L6,L3,L6,R3,L6,L3,L3,R6,L6,R6,L6,L6,R3,L3,L3,R3,R3,L6,L6,L3", 16),
    # (2, TEST_DATA[1], None),
    # (3, TEST_DATA[2], None),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

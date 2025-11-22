"""Everyone Codes Day N."""

import collections
import logging
import operator
import queue
from lib import helpers
from lib import parsers

log = logging.info
HEADINGS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    instructions = data.split(",")
    x, y = 0, 0
    heading = 0
    walls = [set(), set()]
    vertical = True

    for idx, instruction in enumerate(data.split(",")):
        direction, distance = instruction[0], int(instruction[1:])
        # Rotate right/left
        vertical = not vertical
        heading = (heading + (3 if direction == "L" else 1)) % 4
        if idx == 0:
            # The initial wall starts one over from the starting point.
            x, y = x + HEADINGS[heading][0], y + HEADINGS[heading][1]
            distance -= 1
            initial_heading = heading
        nx, ny = x + distance * HEADINGS[heading][0], y + distance * HEADINGS[heading][1]
        if idx + 1 == len(instructions):
            # The final wall ends one short of the target exit.
            end = (nx, ny)
            distance -= 1
            nx, ny = x + distance * HEADINGS[heading][0], y + distance * HEADINGS[heading][1]

        # Sort segements.
        ax, bx = sorted([x, nx])
        ay, by = sorted([y, ny])
        # Walls are either horizontal or vertical.
        # print(f"{idx=}, {instruction=}, {vertical=}, {(x,y)=}, {(nx,ny)=}, {heading=}")
        if vertical:
            walls[heading % 2].add((ay, by, ax))
            # assert ax == bx, f"{idx=}, {vertical=}, {(x,y)=}, {(nx,ny)=}, {heading=}"
        else:
            walls[heading % 2].add((ax, bx, ay))
            # assert ay == by, f"{idx=}, {vertical=}, {(x,y)=}, {(nx,ny)=}, {heading=}"
        x, y = nx, ny

    # Note the x/y of the vertical/horizontal walls. These indicate points of interest.
    edges = [{i for wall in half for i in wall[:2]} for half in walls]

    log(f"{end=}")
    log(f"{walls=}")
    log(f"{edges=}")

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

    seen = {(0, 0): 0}
    q = queue.PriorityQueue()
    q.put((0, 0, (0, 0), initial_heading))

    while q:
        _, steps, pos, heading = q.get()
        x, y = pos
        if pos == end:
            return steps

        # Initial heading is a wall; do not try that direction.
        # Otherwise, heading is how we got here. Try right and left.
        if steps == 0:
            headings = [i for i in range(4) if i != heading]
        else:
            headings = [(heading + i) % 4 for i in [1, 3]]
        log(f"Popped {steps=}, {pos=}; {heading=} = {HEADINGS[heading]}; try {headings=}")

        for heading in headings:
            dx, dy = HEADINGS[heading]
            if pos == (0,1) and heading == 1:
                log("===")
            log(f"{pos=} try {heading=} ={HEADINGS[heading]}, {dx+dy=}, {heading % 2=}")
            f = max if dx + dy == -1 else min
            g = operator.ge if dx + dy == 1 else operator.le
            h = operator.gt if dx + dy == 1 else operator.lt
            a, b = (x, y) if heading % 2 else (y, x)
            end_a = end[0 if heading % 2 else 1]

            blocker = f(
                (
                    cross
                    for start, end, cross in walls[(heading + 1) % 2]
                    if g(cross, a) and start <= b <= end
                ), default=None
            )
            distances = {
                abs(cross - a) + 1
                for start, end, cross in walls[(heading + 1) % 2]
                if g(cross, a) and (blocker is None or h(blocker, cross))
            }
            if g(end_a, a) and (blocker is None or h(blocker, end_a)):
                log(f"Add end {abs(end_a-a)} to distances")
                distances.add(abs(end_a - a))
            log(f"{blocker=}, {distances=}")

            candidates = []
            for distance in distances:
                new = x + distance * dx, y + distance * dy
                n_steps = steps + distance
                if new in seen and n_steps >= seen[new]:
                    continue
                seen[new] = n_steps
                candidates.append((n_steps + dist(new), n_steps, new, heading))
            log(f"{candidates=}")
            for i in candidates:
                q.put(i)


PARSER = parsers.parse_one_str
TESTS = [
    (1, "R3,R4,L3,L4,R3,R6,R9", 6),
    (1, "L6,L3,L6,R3,L6,L3,L3,R6,L6,R6,L6,L6,R3,L3,L3,R3,R3,L6,L6,L3", 16),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

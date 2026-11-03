"""Everyone Codes Day N."""

import operator
import queue
from lib import helpers
from lib import parsers

HEADINGS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def parse_walls(data: str) -> tuple[list[set[tuple[int, int, int]]], int, tuple[int, int]]:
    """Parse the data into a set of vertical and horizontal walls.

    Since walls are straight vertical or horizontal,
    either the start-x, end-x or the start-y, end-y will match.
    We only need to start start-x, end-x, y for walls with a constant y.

    The start, end values can be sorted for easy of checking start <= i <= end.

    Since every wall segment is 90 degrees from the prior,
    the walls alternate between horizontal and vertical.
    """
    instructions = data.split(",")
    x, y = 0, 0
    heading = 0
    initial_heading, end = 0, (0, 0)
    walls: list[set[tuple[int, int, int]]] = [set(), set()]
    vertical = True

    for idx, instruction in enumerate(data.split(",")):
        direction, distance = instruction[0], int(instruction[1:])
        # Rotate right/left
        heading = (heading + (3 if direction == "L" else 1)) % 4
        vertical = not vertical
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
        # Walls are either horizontal or vertical. Store those separately.
        if vertical:
            walls[heading % 2].add((ay, by, ax))
        else:
            walls[heading % 2].add((ax, bx, ay))
        x, y = nx, ny
    return walls, initial_heading, end


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    _ = part
    walls, initial_heading, end = parse_walls(data)

    seen = {(0, 0), }
    q: queue.PriorityQueue[tuple[int, tuple[int, int], int]] = queue.PriorityQueue()
    q.put((0, (0, 0), initial_heading))

    # Start at the begining. Use Djiksta to explore moves.
    # At any point, we can rotate right or left then move forward to either
    # (1) go just past a wall or (2) line up with the end.
    while q:
        steps, pos, heading = q.get()
        x, y = pos
        if pos == end:
            return steps

        # Initial heading is a wall; do not try that direction.
        # Otherwise, heading is how we got here. Try right and left.
        if steps == 0:
            headings = [i for i in range(4) if i != heading]
        else:
            headings = [(heading + i) % 4 for i in [1, 3]]

        for heading in headings:
            dx, dy = HEADINGS[heading]
            # Helper functions depending on the direction/orientation.
            minmax = max if dx + dy == -1 else min
            ge_le = operator.ge if dx + dy == 1 else operator.le
            gt_lt = operator.gt if dx + dy == 1 else operator.lt
            # cur_pos is the current position on the "number line" used to
            # check which walls and "forward" of this position.
            # cur_line is the position orthoganol of the movement.
            # This is used to determine if we would be blocked by a wall or go around it.
            cur_pos, cur_line = (x, y) if heading % 2 else (y, x)
            # end_pos is the x- or y-part of the end that is used to determine if we should
            # stop moving forward at this position, ie when the cur_pos matches it.
            end_pos = end[0 if heading % 2 else 1]

            # Find the first wall we would hit when moving forward.
            # This limits which walls we can "move past" as candidate positions.
            blocker = minmax(
                (
                    cross
                    for start, end, cross in walls[(heading + 1) % 2]
                    if ge_le(cross, cur_pos) and start <= cur_line <= end
                ), default=None
            )
            # distances is how far forward we can move to "move past" a wall (prior to hitting the blocker).
            distances = {
                abs(cross - cur_pos) + 1
                for start, end, cross in walls[(heading + 1) % 2]
                if ge_le(cross, cur_pos) and (blocker is None or gt_lt(blocker, cross))
            }
            # Also consider stopping when we line up with the end position.
            if ge_le(end_pos, cur_pos) and (blocker is None or gt_lt(blocker, end_pos)):
                distances.add(abs(end_pos - cur_pos))

            for distance in distances:
                new = x + distance * dx, y + distance * dy
                if new in seen:
                    continue
                seen.add(new)
                q.put((steps + distance, new, heading))
    raise RuntimeError("Not solved.")


PARSER = parsers.parse_one_str
TESTS = [
    (1, "R3,R4,L3,L4,R3,R6,R9", 6),
    (1, "L6,L3,L6,R3,L6,L3,L3,R6,L6,R6,L6,L6,R3,L3,L3,R3,R3,L6,L6,L3", 16),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

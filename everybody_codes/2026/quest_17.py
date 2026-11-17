"""Everyone Codes Event 2026 Day N."""

import collections
import logging
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    spots = data.coords["#"]

    if part == 1:
        todo = collections.deque()
        todo.append((0, min(spots)))
        end = max(spots)
        print(min(spots), max(spots))
        seen = {min(spots)}
        while todo:
            step, pos = todo.popleft()
            if pos == end:
                return step
            step += 1
            for n in helpers.neighbors_t(*pos):
                if n not in seen and n in spots:
                    todo.append((step, n))
                    seen.add(n)

    if part == 2:
        pos = min(spots)
        direction = (1, 0)
        assert helpers.rotate_counterclockwise(*direction) == (0, 1)
        walked = set()
        start = min(spots)
        end = max(spots)
        got_herb = False
        while True:
            if pos == start and got_herb:
                break
            walked.add(pos)
            direction = helpers.rotate_clockwise(*direction)
            while (n := (pos[0] + direction[0], pos[1] + direction[1])) not in spots:
                direction = helpers.rotate_counterclockwise(*direction)
            pos = n
            if pos == end:
                got_herb = True

        print(walked)
        
        return sum(
            n not in spots for p in walked for n in helpers.neighbors_t(*p)
        )


    pos = min(spots)
    direction = (1, 0)
    walked = set()
    start = min(spots)
    end = max(spots)
    got_herb = False
    walls = 0
    while True:
        direction = helpers.rotate_clockwise(*direction)
        while (n := (pos[0] + direction[0], pos[1] + direction[1])) not in spots:
            direction = helpers.rotate_counterclockwise(*direction)
            walls += 1
        pos = n
        if pos == end:
            break
    a = walls + 1

    pos = min(spots)
    direction = (0, 1)
    walked = set()
    start = min(spots)
    end = max(spots)
    got_herb = False
    walls = 0
    while True:
        direction = helpers.rotate_counterclockwise(*direction)
        while (n := (pos[0] + direction[0], pos[1] + direction[1])) not in spots:
            direction = helpers.rotate_clockwise(*direction)
            walls += 1
        pos = n
        if pos == end:
            break
    b = walls + 2
    return min(a,b)











# PARSER = parsers.parse_one_str
TEST_DATA = [
    """\
""",
    """\
""",
    """\
""",
    """\
""",
    """\
""",
]
TESTS = [
    # (1, TEST_DATA[0], None),
    # (2, TEST_DATA[1], None),
    # (3, TEST_DATA[2], None),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

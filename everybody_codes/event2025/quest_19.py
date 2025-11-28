"""Everyone Codes Day N."""

import collections
import math
import logging
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: list[list[int]]) -> int:
    """Solve the parts."""
    cur_x, cur_y = 0, 0
    total = 0
    walls = collections.defaultdict(list)
    for wall_x, wall_y, wall_size in data:
        walls[wall_x].append((wall_y, wall_size))

    for wall_x, openings in sorted(walls.items()):
        wall_y = min(wall_y for wall_y, _ in openings)
        delta_y = wall_y - cur_y
        delta_x = wall_x - cur_x
        # drop = distance - 2 * flaps
        # climb = 2 * flaps - distance
        # flaps = (climb + distance) / 2
        flaps_needed = math.ceil((delta_y + delta_x) / 2)
        flaps_needed = max(0, flaps_needed)
        total += flaps_needed
        cur_x = wall_x
        cur_y += 2 * flaps_needed - delta_x
        # print(f"{cur_x, cur_y}, {flaps_needed=}")
    return total

    


PARSER = parsers.parse_ints
TEST_DATA = [
    """\
7,7,2
12,0,4
15,5,3
24,1,6
28,5,5
40,8,2""",
    """\
7,7,2
7,1,3
12,0,4
15,5,3
24,1,6
28,5,5
40,3,3
40,8,2""",
]
TESTS = [
    (1, TEST_DATA[0], 24),
    (2, TEST_DATA[1], 22),
    # (3, TEST_DATA[2], None),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

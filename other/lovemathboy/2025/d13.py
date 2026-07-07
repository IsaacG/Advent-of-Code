"""Love May Boy Day N."""

import collections
import logging
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    heights = collections.defaultdict(int)
    prior_arg = ""
    for op, arg in data:
        if op == "plant":
            heights[arg] += 1
        else:
            if arg != "all" and arg == prior_arg:
                continue
            if arg == "all":
                plants = [h for h, j in heights.items() if j]
            elif arg == "odd":
                plants = [h for h, j in heights.items() if j and h % 2 == 1]
            else:
                plants = [h for h, j in heights.items() if j and h % 2 == 0]
            if part == 1:
                plants.sort(reverse=True)
                for p in plants:
                    heights[p + 1] += heights[p]
                    del heights[p]
            elif part == 2:
                plants.sort()
                for p in plants:
                    heights[p // 2] += heights[p]
                    del heights[p]
        # print(op, arg, heights)
        prior_arg = arg
    return sum(i * j for i, j in heights.items())


PARSER = parsers.parse_multi_mixed_per_line
TEST_DATA = [
    """\
plant 5
spray even
spray odd
plant 9
spray all
plant 4
spray even""",
]
TESTS = [
    (1, TEST_DATA[0], 23),
    (2, TEST_DATA[0], 5),
    # (3, TEST_DATA[2], None),
]

if __name__ == "__main__":
    helpers.run_solution(globals(), parts=[2])

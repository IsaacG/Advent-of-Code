"""Everyone Codes Day N."""

import collections
from lib import helpers
from lib import parsers


def solve(part: int, data: list[list[int]]) -> int:
    """Solve the parts."""
    boxes = data[0]
    if part == 1:
        return sum(set(boxes))
    if part == 2:
        return sum(sorted(set(boxes))[:20])
    return collections.Counter(boxes).most_common(1)[0][1]


PARSER = parsers.parse_ints
TESTS = [
    (1, "10,5,1,10,3,8,5,2,2", 29),
    (2, "4,51,13,64,57,51,82,57,16,88,89,48,32,49,49,2,84,65,49,43,9,13,2,3,75,72,63,48,61,14,40,77", 781),
    (3, "4,51,13,64,57,51,82,57,16,88,89,48,32,49,49,2,84,65,49,43,9,13,2,3,75,72,63,48,61,14,40,77", 3),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

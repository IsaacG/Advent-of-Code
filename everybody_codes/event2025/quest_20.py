"""Everyone Codes Day N."""

import collections
import logging
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    start, end = (0, 0), (0, 0)
    lines = [line.strip(".") for line in data.splitlines()]
    trampolines = set()
    positions = set()

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            x, m = divmod(x, 2)
            r = bool(m)
            if c == "S":
                start = x, y, r
            if c == "E":
                end = x, y, r
            if c in "SET":
                trampolines.add((x, y, r))
            positions.add((x, y, r))
    # print(sorted(trampolines))
    # print(len(lines))

    neigbors = collections.defaultdict(set)
    for position in positions:
        x, y, r = position
        nr = not r
        if r:
            adjacents = {(x, y, nr), (x + 1, y, nr), (x, y + 1, nr), (x, y, r)}
        else:
            adjacents = {(x - 1, y, nr), (x, y, nr), (x, y - 1, nr), (x, y, r)}
        for adjacent in adjacents:
            if adjacent in trampolines:
                neigbors[position].add(adjacent)

    if part == 1:
        return sum(len(j) for i, j in neigbors.items() if i in trampolines) // 2

    center = (len(lines) - 1) // 2
    max_y = len(lines) - 1

    def transform(x, y, r):
        if y < center:
            # top
            nx = y
            ny = (len(lines[y]) // 2) - (1 if r else 0) - x
        elif x < center:
            # left
            ny = max_y - x - (1 if r else 0) - y
            nx = (max_y - ny) - (1 if r else 0) - x
        else:
            nx = y
            ny = max_y - y - x
        return nx, ny, r


    q = collections.deque()
    seen = set()
    q.append((0, start))
    seen.add(start)
    while q:
        steps, pos = q.popleft()
        if pos == end:
            return steps
        steps += 1
        if part == 3:
            i = transform(*pos)
            # print(f"{pos} ==> {i}: neighbors: {neigbors[i]}")
            pos = i
        for neighbor in neigbors[pos]:
            if neighbor not in seen:
                seen.add(neighbor)
                q.append((steps, neighbor))


    log(f"{start, end}")




PARSER = parsers.parse_one_str
TEST_DATA = [
    """\
T#TTT###T##
.##TT#TT##.
..T###T#T..
...##TT#...
....T##....
.....#..... """,
    """\
T#T#T#T#T#T
.T#T#T#T#T.
..T#T#T#T..
...T#T#T...
....T#T....
.....T..... """,
    """\
T#T#T#T#T#T
.#T#T#T#T#.
..#T###T#..
...##T##...
....#T#....
.....#..... """,
    """\
TTTTTTTTTTTTTTTTT
.TTTT#T#T#TTTTTT.
..TT#TTTETT#TTT..
...TT#T#TTT#TT...
....TTT#T#TTT....
.....TTTTTT#.....
......TT#TT......
.......#TT.......
........S........""",
    """\
T####T#TTT##T##T#T#
.T#####TTTT##TTT##.
..TTTT#T###TTTT#T..
...T#TTT#ETTTT##...
....#TT##T#T##T....
.....#TT####T#.....
......T#TT#T#......
.......T#TTT.......
........TT#........
.........S.........""",
]
TESTS = [
    (1, TEST_DATA[0], 7),
    (1, TEST_DATA[1], 0),
    (1, TEST_DATA[2], 0),
    (2, TEST_DATA[3], 32),
    (3, TEST_DATA[4], 23),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

"""Everyone Codes Day N."""

import collections
from lib import helpers
from lib import parsers

Coord = tuple[int, int, bool]


def parse(lines: list[str]) -> tuple[Coord, Coord, dict[Coord, set[Coord]], set[Coord]]:
    """Parse the input."""
    start = end = (0, 0, False)
    # trampolines contains the coordinates of all trampolines.
    trampolines = set()
    # positions contains all coordinates in the triangle board.
    positions = set()

    # Find coordinates for: start, end, trampolines and all positions.
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            # Combine pairs of cells into a right and left.
            x, m = divmod(x, 2)
            r = bool(m)
            if c == "S":
                start = x, y, r
            if c == "E":
                end = x, y, r
            if c in "SET":
                trampolines.add((x, y, r))
            positions.add((x, y, r))

    # Compute the neighbors (potential next hops) for all positions -- even if they aren't trampolines!
    neighbors = collections.defaultdict(set)
    for position in positions:
        x, y, r = position
        nr = not r
        # adjacents: left, right, up-or-down, self.
        if r:
            adjacents = {(x, y, nr), (x + 1, y, nr), (x, y + 1, nr), (x, y, r)}
        else:
            adjacents = {(x - 1, y, nr), (x, y, nr), (x, y - 1, nr), (x, y, r)}
        neighbors[position] = {adjacent for adjacent in adjacents if adjacent in trampolines}

    return start, end, neighbors, trampolines


def solve(part: int, data: str) -> int:
    """Solve the parts.

    https://www.redblobgames.com/grids/parts/#triangle-grids
    The board is handled like a square grid with each cell split into two.
    Each (x, y) can contain two triangles: a left and right half.
    Triangle coordinates are (x, y, r) where r means "right".
    Each `r` triangle is adjacent to three `not r` triangles and vice verse.
    """
    lines = [line.strip(".") for line in data.splitlines()]
    start, end, neighbors, trampolines = parse(lines)

    if part == 1:
        total = sum(
            len(adjacent)
            for position, adjacent in neighbors.items()
            if position in trampolines
        )
        # Remove self-hops.
        total -= len(trampolines)
        # Correct for counting a-to-b and b-to-a.
        total //= 2
        return total

    # The center is used for rotation.
    # Anything above this y can be rotated top-to-left.
    # Anything left of this x can be rotated left-to-right.
    center = (len(lines) - 1) // 2
    max_y = len(lines) - 1

    def rotate(x: int, y: int, r: bool) -> Coord:
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
        # The r does not change.
        return nx, ny, r

    # Dijkstra
    q: collections.deque[tuple[int, Coord]] = collections.deque()
    seen = set()
    q.append((0, start))
    seen.add(start)
    while q:
        steps, pos = q.popleft()
        if pos == end:
            return steps
        steps += 1
        if part == 3:
            pos = rotate(*pos)
        for neighbor in neighbors[pos]:
            if neighbor not in seen:
                seen.add(neighbor)
                q.append((steps, neighbor))
    raise RuntimeError("No solution found.")


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

"""Everyone Codes Event 2026 Day 12."""

from lib import helpers


def sides(points: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    return min(x for x, y in points), max(x for x, y in points), min(y for x, y in points), max(y for x, y in points)


def spells(points: set[tuple[int, int]]) -> int:
    if not points:
        return 0
    x1, x2, y1, y2 = sides(points)
    return min(x2 - x1, y2 - y1) + 1


def solve(part: int, data: str | helpers.Map) -> int:
    """Solve the parts."""
    if isinstance(data, str):
         coords = {(x, y) for y, row in enumerate(data.splitlines()) for x, char in enumerate(row) if char == "#"}
    else:
        coords = data.coords["#"]

    shapes = helpers.build_dsu(
        {i} | {n for n in helpers.neighbors_t(*i) if n in coords}
        for i in coords
    )

    total = 0
    for shape in shapes:
        out_left, out_right, out_top, out_bottom = sides(shape)
        inner_left = min((x for x, y in shape if x != out_left and (x - 1, y) not in shape), default=None)
        inner_right = max((x for x, y in shape if x != out_right and (x + 1, y) not in shape), default=None)
        inner_top = min((y for x, y in shape if y != out_top and (x, y - 1) not in shape), default=None)
        inner_bottom = max((y for x, y in shape if y != out_bottom and (x, y + 1) not in shape), default=None)

        top = bottom = right = left = set()
        if inner_left:
            right = {(x, y) for x, y in shape if x >= inner_left}
        if inner_right:
            left = {(x, y) for x, y in shape if x <= inner_right}
        if inner_top:
            bottom = {(x, y) for x, y in shape if y >= inner_top}
        if inner_bottom:
            top = {(x, y) for x, y in shape if y <= inner_bottom}

        total+= min(
            spells(t) + spells(b) + spells(right - t - b) + spells(left - t - b)
            for t in [top, top - left, top - right, top - left - right]
            for b in [bottom, bottom - left, bottom - right, bottom - left - right]
        ) or spells(shape)

    return total


TEST_DATA = [
    """\
........#.
.##.......
.##..####.
.##..####.
.....####.
.###......""",
    """\
........#.
.##.......
.##..####.
.#...#....
.....#....
.####.....""",
    """\
.................
..#######........
..#######........
..#######........
.......##........
.......##........
.......##........
.................""",
    """\
...............................
.####....#####..#######........
.####....#####..#######........
.####....#####..#######........
.........#####.......##........
.........########....##........
.........########....##........
...............................
.######....#.....#.....###.....
...........#...........###.....
...........#......########.....
...........#......########.....
...........#......########.....
..................########.....
...............................""",
    """\
........#.
.##.......
.##..####.
.#...#..#.
.....####.
.###......""",
    """\
..............................
.##########....##.....#######.
.##########.##.##..#..#######.
.####..####.##.##.....#.#####.
.##########.##.#####..#.#####.
.##########.##........#######.
..............................
.##########..################.
.##########..#..............#.
.#######..#..#..............#.
.#######..#..################.
.##########..################.
..............................""",
    """\
..............................
.############################.
.##...................###.###.
.##..################.###.###.
.##..######.........#.###.###.
.##..################.###.###.
.##...................###.###.
.##..####################.###.
.##..####################.###.
.##.......................###.
.############################.
..............................""",
]
TESTS = [
    (1, TEST_DATA[0], 7),
    (2, TEST_DATA[1], 6),
    (2, TEST_DATA[2], 5),
    (2, TEST_DATA[3], 23),
    (3, TEST_DATA[4], 8),
    (3, TEST_DATA[5], 29),
    (3, TEST_DATA[6], 16),
]


if __name__ == "__main__":
    helpers.run_solution(globals())

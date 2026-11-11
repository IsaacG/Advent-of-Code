"""Everyone Codes Event 2026 Day N."""

import functools
import itertools
import logging
import platform

try:
    from lib import helpers
    from lib import parsers
except ModuleNotFoundError as e:
    if platform.python_implementation() != "PyPy":
        raise

log = logging.info

def for_block(s):
    if not s:
        return 0
    x1, x2, y1, y2 = (min(x for x, y in s), max(x for x, y in s), min(y for x, y in s), max(y for x, y in s))
    return min(x2 - x1, y2 - y1) + 1


def lines(block):
    if not block:
        return 0
    x, y = min(block)

    if False:  # brute force
        row = list(itertools.takewhile((lambda i: (i, y) in block), itertools.count(x)))
        col = list(itertools.takewhile((lambda i: (x, i) in block), itertools.count(y)))
        return 1 + min(
            lines(block - {(i, y) for i in row}),
            lines(block - {(x, i) for i in col}),
        )



    # print(f"{len(block)} @ ({x}, {y}) = {sorted(block)}")
    longest_row, lry = [], 0
    longest_col, lcx = [], 0
    for x, y in sorted(block):
        if (x - 1, y) not in block:
            row = list(itertools.takewhile((lambda i: (i, y) in block), itertools.count(x)))
            if len(row) >= len(longest_row):
                longest_row = row
                lry = y
        if (x, y - 1) not in block:
            col = list(itertools.takewhile((lambda i: (x, i) in block), itertools.count(y)))
            if len(col) >= len(longest_col):
                longest_col = col
                lcx = x

    row, col = longest_row, longest_col

    y = lry
    x = lcx
    if len(row) > len(col):
        # # print(f"Take out row {len(row)=}, x={row} y={y}")
        return 1 + lines(block - {(i, y) for i in row})
    if len(row) < len(col):
        # print(f"Take out col {len(col)=}, {col=}")
        return 1 + lines(block - {(x, i) for i in col})
    return 1 + min(
        lines(block - {(i, y) for i in row}),
        lines(block - {(x, i) for i in col}),
    )
    


def render(s):
    x1, x2, y1, y2 = (min(x for x, y in s), max(x for x, y in s), min(y for x, y in s), max(y for x, y in s))
    print()
    for y in range(y1, y2 + 1):
        print("".join("#" if (x, y) in s else " " for x in range(x1, x2 + 1)))
    print()

def solve(part: int, data: str, testing) -> int:
    """Solve the parts."""
    if platform.python_implementation() == "PyPy":
         coords = {(x, y) for y, row in enumerate(data.splitlines()) for x, char in enumerate(row) if char == "#"}
    else:
        coords = data.coords["#"]

    # print(data)
    sets = []
    for i in coords:
        n = {n for n in helpers.neighbors_t(*i) if n in coords}
        n.add(i)
        helpers.add_to_disjoint_sets(sets, n)
    n = []
    for s in sets:
        out_left, out_right, out_top, out_bottom = (min(x for x, y in s), max(x for x, y in s), min(y for x, y in s), max(y for x, y in s))
        blocks = []

        in_left = min((x for x, y in s if x != out_left and (x - 1, y) not in s), default=None)
        in_right = max((x for x, y in s if x != out_right and (x + 1, y) not in s), default=None)
        in_top = min((y for x, y in s if y != out_top and (x, y - 1) not in s), default=None)
        in_bottom = max((y for x, y in s if y != out_bottom and (x, y + 1) not in s), default=None)
        tl = min(s)

        if tl == (22, 1):
            print()
            render(s)
            print()
        top = bottom = right = left = set()
        blocks = []
        if in_left is not None:
            blocks.append({(x, y) for x, y in s if x >= in_left})
            right = blocks[-1]
            if tl == (22, 1):
                print("R", sorted(blocks[-1]))
                render(right)
        if in_right is not None:
            blocks.append({(x, y) for x, y in s if x <= in_right})
            left = blocks[-1]
            if tl == (22, 1):
                print("L", sorted(blocks[-1]))
                render(left)
        if in_top is not None:
            blocks.append({(x, y) for x, y in s if y >= in_top})
            bottom = blocks[-1]
            if tl == (22, 1):
                print("B", sorted(blocks[-1]))
                render(bottom)
        if in_bottom is not None:
            blocks.append({(x, y) for x, y in s if y <= in_bottom})
            top = blocks[-1]
            if tl == (22, 1):
                print("T", sorted(blocks[-1]))
                render(top)

        if blocks:
            need = len(s)
            for t in [top, top - left, top - right, top - left - right]:
                for b in [bottom, bottom - left, bottom - right, bottom - left - right]:
                    i = for_block(t) + for_block(b) + for_block(right - t - b) + for_block(left - t - b)
                    if i < need:
                        need = i
                        if tl == (22, 1):
                            print(f"Solve in {i}: {t=}, {b=}")
        else:
            need = for_block(s)

        print(f"{need} for {min(s)}, {len(blocks)=}")
        # print([len(i) for i in blocks])
        n.append(need)
    print("Needed:", n)
    t = sum(n)
    if not testing and part == 3:
        assert t != 2939
        assert t != 2884
    return t



# PARSER = parsers.parse_one_str
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

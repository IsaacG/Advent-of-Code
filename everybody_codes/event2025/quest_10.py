"""Everyone Codes Day N."""

import collections
import logging
import functools
import time
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str, testing) -> int:
    """Solve the parts."""
    dragon = {
        (x, y)
        for y, line in enumerate(data.splitlines())
        for x, char in enumerate(line)
        if char == "D"
    }
    sheep = {
        (x, y)
        for y, line in enumerate(data.splitlines())
        for x, char in enumerate(line)
        if char == "S"
    }
    hide = {
        (x, y)
        for y, line in enumerate(data.splitlines())
        for x, char in enumerate(line)
        if char == "#"
    }
    board = {
        (x, y)
        for y, line in enumerate(data.splitlines())
        for x, char in enumerate(line)
    }
    start = dragon.copy().pop()
    seen = set()
    q = collections.deque([(start, 0)])

    OFFSETS = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    def moves(dragon):
        x, y = dragon
        for dx, dy in OFFSETS:
            pos = (x + dx, y + dy)
            if pos in board:
                yield pos

    if part == 1:
        max_moves = 3 if testing else 4
    if part == 2:
        max_moves = 3 if testing else 20

    if part == 1:
        count = 0
        while q:
            dragon, steps = q.popleft()
            if dragon in sheep:
                count += 1
            steps += 1
            if steps > max_moves:
                continue
            for pos in moves(dragon):
                if pos in seen:
                    continue
                seen.add(pos)
                q.append((pos, steps))
        return count

    if part == 2:
        count = 0
        while q:
            dragon, steps = q.popleft()
            if dragon not in hide and steps:
                x, y = dragon
                y -= (steps - 1)
                if (x, y) in sheep:
                    count += 1
                    sheep.remove((x, y))
                y -= 1
                if (x, y) in sheep:
                    count += 1
                    sheep.remove((x, y))
            steps += 1
            if steps > max_moves:
                continue
            for pos in moves(dragon):
                if (pos, steps) in seen:
                    continue
                seen.add((pos, steps))
                q.append((pos, steps))
        return count


    bottom = len(data.splitlines()) - 1

    @functools.cache
    def possibilities(dragon, sheep):
        if all(y == bottom for _, y in sheep):
            return 0
        sheep_down = []
        for ship in sheep:
            x, y = ship
            if y == bottom:
                continue
            n = x, y + 1
            if (n != dragon) or (n in hide):
                sheep_down.append((sheep - {ship}) | {n})
        if not sheep_down and any(y == bottom for _, y in sheep):
            return 0

        options = 0
        for next_sheep in set(sheep_down or [sheep]):
            assert len(next_sheep) == len(sheep)
            if dragon not in hide:
                assert dragon not in next_sheep
            for pos in moves(dragon):
                ns = next_sheep.copy()
                if pos in next_sheep and pos not in hide:
                    ns -= {pos}
                if not ns:
                    options += 1
                else:
                    options += possibilities(pos, frozenset(ns))
        return options

    return possibilities(start, frozenset(sheep))

    



PARSER = parsers.parse_one_str
TEST_DATA = [
    """\
...SSS.......
.S......S.SS.
..S....S...S.
..........SS.
..SSSS...S...
.....SS..S..S
SS....D.S....
S.S..S..S....
....S.......S
.SSS..SS.....
.........S...
.......S....S
SS.....S..S..""",
    """\
...SSS##.....
.S#.##..S#SS.
..S.##.S#..S.
.#..#S##..SS.
..SSSS.#.S.#.
.##..SS.#S.#S
SS##.#D.S.#..
S.S..S..S###.
.##.S#.#....S
.SSS.#SS..##.
..#.##...S##.
.#...#.S#...S
SS...#.S.#S..""",
    """\
SSS
..#
#.#
#D.""",
    """\
SSS
..#
..#
.##
.D#""",
    """\
..S..
.....
..#..
.....
..D..""",
    """\
.SS.S
#...#
...#.
##..#
.####
##D.#""",
]
TESTS = [
    (1, TEST_DATA[0], 27),
    (2, TEST_DATA[1], 27),
    (3, TEST_DATA[2], 15),
    (3, TEST_DATA[3], 8),
    (3, TEST_DATA[4], 44),
    (3, TEST_DATA[5], 4406),
]

if __name__ == "__main__":
    for _part, _data, expected in TESTS:
        assert solve(_part, PARSER.parse(_data), True) == expected
    print("Tests pass.")
    day = int(__file__.split("_", maxsplit=-1)[-1].split(".")[0])
    for _part in range(1, 4):
        with open(f"inputs/{day:02}.{_part}.txt", encoding="utf-8") as f:
            _input = PARSER.parse(f.read())  # type: list[list[int]]
            start = time.perf_counter_ns()
            got = solve(_part, _input, False)
            end = time.perf_counter_ns()
            print(f"{day:02}.{_part} {got:15} {helpers.format_ns(end - start):8}")

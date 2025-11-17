"""Everyone Codes Day N. Note, `ship` == one sheep."""

import functools
import time
from lib import helpers
from lib import parsers

OFFSETS = [complex(*i) for i in [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]]


def p12(part: int, data: helpers.Map, testing: bool) -> int:
    """Solve the first half."""
    dragons, sheep, hideouts = (data.coords.get(i, set()) for i in "DS#")
    board = data.all_coords
    start = dragons.pop()

    def moves(dragon: complex) -> list[complex]:
        return [
            dragon + offset
            for offset in OFFSETS
            if dragon + offset in board
        ]

    max_moves = 3 if testing else 4 if part == 1 else 20
    seen = set()
    count = 0
    q = [(start, 0)]
    while q:
        dragon, steps = q.pop()
        sheep_offset = [complex()] if part == 1 else [complex(0, steps - 1), complex(0, steps)]
        if dragon not in hideouts and steps:
            for offset in sheep_offset:
                sheep_pos = dragon - offset
                if sheep_pos in sheep:
                    count += 1
                    sheep.remove(sheep_pos)
        steps += 1
        if steps > max_moves:
            continue
        for pos in moves(dragon):
            if (pos, steps) in seen:
                continue
            seen.add((pos, steps))
            q.append((pos, steps))
    return count


def solve(part: int, data: helpers.Map, testing) -> int:
    """Solve the parts."""
    if part in [1, 2]:
        return p12(part, data, testing)

    dragons, initial_sheep, hideouts = (data.coords.get(i, set()) for i in "DS#")
    board = data.all_coords
    start = dragons.pop()
    bottom = data.max_y
    # If the sheep reaches this location, the game ends.
    game_over = {complex(x, data.max_y + 1) for x in range(data.max_x + 1)}
    for _ in range(data.max_y):
        for i in hideouts:
            if i + 1j in game_over:
                game_over.add(i)
    # This is the lowest position the sheep can enter and the dragon still wins.
    last_spot = {
        complex(x, min(i.imag for i in game_over if i.real == x) - 1)
        for x in range(data.max_x + 1)
    }

    def moves(dragon):
        for offset in OFFSETS:
            pos = dragon + offset
            if pos in board:
                yield pos

    @functools.cache
    def possibilities(dragon: complex, sheep: frozenset[complex]) -> int:
        next_sheeps = []
        for ship in sheep:
            # Do not count sheep moving off the board; this is not a possible win.
            if ship in last_spot:
                continue
            # See if this sheep can move down. If yes, this is a possible next move for the sheep.
            n = ship + 1j
            if (n != dragon) or (n in hideouts):
                next_sheeps.append((sheep - {ship}) | {n})
        # If no sheep moved, either
        # (1) they are all at the bottom and the dragon loses or
        # (2) they stay still this turn.
        if not next_sheeps:
            if any(ship in last_spot for ship in sheep):
                return 0
            next_sheeps = [sheep]

        # Count possible ways to move for each sheep move, for each dragon move.
        options = 0
        for next_sheep in next_sheeps:
            for pos in moves(dragon):
                sheep = next_sheep.copy()
                # Dragon eats sheep; take it off the board.
                if pos in next_sheep and pos not in hideouts:
                    sheep -= {pos}
                # Either the dragon finished all the sheep; we are done.
                # Otherwise, count child possibilities.
                if not sheep:
                    options += 1
                else:
                    options += possibilities(pos, frozenset(sheep))
        return options

    return possibilities(start, frozenset(initial_sheep))


PARSER = parsers.CoordinatesParser()
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
            _input = PARSER.parse(f.read())
            _start = time.perf_counter_ns()
            got = solve(_part, _input, False)
            end = time.perf_counter_ns()
            print(f"{day:02}.{_part} {got:15} {helpers.format_ns(end - _start):8}")

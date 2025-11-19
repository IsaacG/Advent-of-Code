"""Everyone Codes Day N."""

import functools
import logging
import time
from lib import helpers
from lib import parsers

log = logging.info
OFFSETS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    board = {
        (x, y): int(char)
        for y, line in enumerate(data.splitlines())
        for x, char in enumerate(line)
    }
    top_left, bottom_right = min(board), max(board)

    @functools.cache
    def explode(starting_points: tuple[tuple[int, int], ...]) -> set[tuple[int, int]]:
        """Return all the barrels that explode from a given set of starting explosions."""
        boom = set(starting_points)
        todo = set(starting_points)
        while todo:
            cur = todo.pop()
            for dx, dy in OFFSETS:
                n = (cur[0] + dx, cur[1] + dy)
                if n in boom or n not in board or board[n] > board[cur]:
                    continue
                if board[n] == board[cur]:
                    # Expand the search when the barrel size is the same.
                    boom.add(n)
                    todo.add(n)
                else:
                    # Use dynamic programming to reuse sub-explosions with smaller barrels.
                    boom |= explode((n, ))
        return boom

    if part == 1:
        return len(explode((top_left,)))
    if part == 2:
        return len(explode((top_left, bottom_right)))

    starting_barrels = []
    available = set(board.keys())
    log("Start")

    for choice in range(3):
        best_choice, max_damage = (0, 0), 0
        for barrel in available:
            # Cheat to speed up code.
            if choice == 0 and board[barrel] < 4:
                continue
            damage = explode((barrel, )) & available
            if len(damage) > max_damage:
                max_damage = len(damage)
                best_choice = barrel
        starting_barrels.append(best_choice)
        log(f"Picked {best_choice} for {max_damage} damage")
        # Reduce what barrels are considered unbroken.
        available -= explode((best_choice, ))

    available = set(board.keys())
    return len(explode(tuple(starting_barrels)))


PARSER = parsers.parse_one_str
TEST_DATA = [
    """\
989611
857782
746543
766789""",
    """\
9589233445
9679121695
8469121876
8352919876
7342914327
7234193437
6789193538
6781219648
5691219769
5443329859""",
    """\
5411
3362
5235
3112""",
    """\
41951111131882511179
32112222211508122215
31223333322105122219
31234444432147511128
91223333322176021892
60112222211166431583
04661111166111111746
01111119042122222177
41222108881233333219
71222127839122222196
56111026279711111507""",
]
TESTS = [
    (1, TEST_DATA[0], 16),
    (2, TEST_DATA[1], 58),
    (3, TEST_DATA[2], 14),
    (3, TEST_DATA[3], 133),
]

if __name__ == "__main__":
    for _part, _data, expected in TESTS:
        assert solve(_part, PARSER.parse(_data)) == expected
    print("Tests pass.")
    day = int(__file__.split("_", maxsplit=-1)[-1].split(".")[0])
    for _part in range(1, 4):
        with open(f"inputs/{day:02}.{_part}.txt", encoding="utf-8") as f:
            _input = PARSER.parse(f.read())  # type: str
            start = time.perf_counter_ns()
            got = solve(_part, _input)
            end = time.perf_counter_ns()
            print(f"{day:02}.{_part} {got:15} {helpers.format_ns(end - start):8}")

"""Everyone Codes Day N."""

from lib import helpers
from lib import parsers

DIAGONALS = [(x, y) for x in [-1, 1] for y in [-1, 1]]


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    lines = data.splitlines()
    input_width = len(lines[0])
    input_height = len(lines)
    assert input_width == input_height
    board_size = input_width if part in [1, 2] else 34

    offset = 0 if part in [1, 2] else (board_size - input_width) // 2
    input_active = {
        (x + offset, y + offset)
        for y, line in enumerate(lines)
        for x, char in enumerate(line)
        if char == "#"
    }
    # Used for part 3.
    input_inactive = {
        (x + offset, y + offset)
        for y, line in enumerate(lines)
        for x, char in enumerate(line)
        if char != "#"
    }

    active = frozenset() if part == 3 else frozenset(input_active)

    def neighbors(x, y):
        return [(x + dx, y + dy) for dx, dy in DIAGONALS if 0 <= x + dx < board_size and 0 <= y + dy < board_size]

    want_steps = [10, 2025, 1000000000][part - 1]

    total = 0
    seen_at = {}
    seen: dict[frozenset[tuple[int, int]], int] = {}

    for step in range(5000):
        active = frozenset({
            (x, y) for x in range(board_size) for y in range(board_size)
            if (
                ((x, y) in active and sum(n in active for n in neighbors(x, y)) % 2 == 1)
                or ((x, y) not in active and sum(n in active for n in neighbors(x, y)) % 2 == 0)
            )
        })

        if part != 3:
            total += len(active)
            if step + 1 == want_steps:
                return total
        elif input_active.issubset(active) and input_inactive.isdisjoint(active):
            seen_at[step] = len(active)
            if active in seen:
                cycle_start = seen[active]
                cycle = step - cycle_start
                spots: set[int] = set()
                for prior in seen_at:
                    if prior >= cycle_start:
                        spots.update(range(cycle_start + (prior - cycle_start), want_steps, cycle))
                return sum(
                    seen_at[((spot - cycle_start) % cycle) + cycle_start]
                    for spot in spots
                )

            seen[active] = step
    raise RuntimeError("No solution found.")


PARSER = parsers.parse_one_str
TEST_DATA = [
    """\
.#.##.
##..#.
..##.#
.#.##.
.###..
###.##""",
    """\
#......#
..#..#..
.##..##.
...##...
...##...
.##..##.
..#..#..
#......#""",
]
TESTS = [
    (1, TEST_DATA[0], 200),
    (3, TEST_DATA[1], 278388552),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

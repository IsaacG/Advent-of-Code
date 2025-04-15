"""Codyssi Day N."""

from typing import cast

def get_distances(
    islands: set[tuple[int, int]], current_x: int, current_y: int
) -> list[tuple[int, int, int]]:
    """Return the distances to a set of islands."""
    return [
        (abs(current_x - x) + abs(current_y - y), x, y)
        for x, y in islands
    ]


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    islands = {
        cast(tuple[int, int], tuple(int(i) for i in line.removeprefix("(").removesuffix(")").split(", ")))
        for line in data.splitlines()
    }

    if part == 1:
        distances = get_distances(islands, 0, 0)
        return max(distances)[0] - min(distances)[0]
    if part == 2:
        _, start_x, start_y = min(get_distances(islands, 0, 0))
        return min(get_distances(islands - {(start_x, start_y)}, start_x, start_y))[0]
    if part == 3:
        current = [0, 0]
        total = 0

        while islands:
            distance, *current = min(get_distances(islands, *current))
            islands.remove(tuple(current))
            total += distance

        return total
    raise RuntimeError("This is not reachable code")


TEST_DATA = """\
(-16, -191)
(92, 186)
(157, -75)
(39, -132)
(-42, 139)
(-74, -150)
(200, 197)
(-106, 105)
"""
TESTS = [
    (1, TEST_DATA, 226),
    (2, TEST_DATA, 114),
    (3, TEST_DATA, 1384),
]

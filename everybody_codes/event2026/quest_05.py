"""Everyone Codes Event 2026 Day 5."""

from lib import helpers
from lib import parsers


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    # Seed the initial land mass.
    center = (data.width // 2, data.height // 2)
    land = {center}

    # Grow the land.
    todo = {center}
    dark = data.coords[1] | {center}
    while todo:
        cur = todo.pop()
        for n in helpers.neighbors_t(*cur, helpers.EIGHT_DIRECTIONS_T):
            if n in land:
                continue
            count = sum(i in dark for i in helpers.neighbors_t(*n, helpers.EIGHT_DIRECTIONS_T))
            if count >= 5:
                land.add(n)
                todo.add(n)
                dark.add(n)

    if part == 1:
        return len(land)

    # Seed the sand: any land adjacent to water.
    sand = {i for i in land if any(j not in land for j in helpers.neighbors_t(*i, helpers.EIGHT_DIRECTIONS_T))}
    land -= sand

    # Grow the sand.
    todo = sand.copy()
    while todo:
        cur = todo.pop()
        for n in helpers.neighbors_t(*cur, helpers.EIGHT_DIRECTIONS_T):
            if n in sand:
                continue
            count = sum(i in sand for i in helpers.neighbors_t(*n, helpers.EIGHT_DIRECTIONS_T))
            if count >= 5:
                sand.add(n)
                todo.add(n)

    if part == 2:
        return len(sand)

    stamp = helpers.EIGHT_DIRECTIONS_T + [
        (x, y) for x in [-2, 2] for y in [-1, 0, 1]
    ] + [(x, y) for y in [-2, 2] for x in [-1, 0, 1]]
    assert len(stamp) == 8 + 12

    # Seed the trees.
    trees = {i for i in land if all(n in land for n in helpers.neighbors_t(*i, stamp))}
    # Expand the trees.
    for _ in range(2):
        new_trees = set()
        for i in land - trees:
            count = sum(n in trees for n in helpers.neighbors_t(*i, helpers.EIGHT_DIRECTIONS_T))
            if count < 4:
                continue
            if all(n not in sand for n in helpers.neighbors_t(*i, helpers.EIGHT_DIRECTIONS_T)):
                new_trees.add(i)
        trees |= new_trees
    return len(trees)


TEST_DATA = """\
010100100100001101000
111101001000001110000
101111011000101010011
001000101010000100000
000110100110011001100
000001110111111000000
101100010101011110000
001101100000001010011
001001001111010001001
100011011110011010101
001100101110010010000"""
TESTS = [
    (1, TEST_DATA, 137),
    (2, TEST_DATA, 69),
    (3, TEST_DATA, 14),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

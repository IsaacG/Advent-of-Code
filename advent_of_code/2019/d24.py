#!/bin/python
"""Advent of Code, ${title}."""
from lib import helpers

# Position of outer/inner cell(s) as we move between depths.
OUTER = {
    (-1, 0): (1, 2),
    (+1, 0): (3, 2),
    (0, -1): (2, 1),
    (0, +1): (2, 3),
}
INNER = {
    (-1, 0): [(4, y) for y in range(5)],
    (+1, 0): [(0, y) for y in range(5)],
    (0, -1): [(x, 4) for x in range(5)],
    (0, +1): [(x, 0) for x in range(5)],
}


def simple_neighbors(p: tuple[int, int]) -> list[tuple[int, int]]:
    """Return adjacent cells using simple board logic. Part 1."""
    x, y = p
    out = []
    for dx, dy in helpers.STRAIGHT_NEIGHBORS_T:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 5 and 0 <= ny < 5:
            out.append((nx, ny))
    return out


def nested_neighbors(p: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    """Return adjacent cells using nested boards. Part 2."""
    x, y, z = p
    out: list[tuple[int, int, int]] = []
    for dx, dy in helpers.STRAIGHT_NEIGHBORS_T:
        nx, ny = x + dx, y + dy
        if nx == 2 and ny == 2:
            for nx, ny in INNER[dx, dy]:
                out.append((nx, ny, z + 1))
        elif 0 <= nx < 5 and 0 <= ny < 5:
            out.append((nx, ny, z))
        else:
            # go out a level
            nx, ny = OUTER[dx, dy]
            out.append((nx, ny, z - 1))
    return out


def solve(data: helpers.Map, part: int, testing: bool) -> int:
    """Count how many bugs there are after some time."""
    assert (2, 2) not in data.coords["#"]
    steps = 10 if testing else 200

    active: frozenset[set[tuple[int, int] | tuple[int, int, int]]]
    if part == 1:
        active = frozenset(data.coords["#"])
    else:
        active = frozenset({(x, y, 0) for x, y in data.coords["#"]})

    get_neighbors = simple_neighbors if part == 1 else nested_neighbors

    seen = set()
    step = 0
    while True:
        # Part 1: run until a pattern is repeated.
        if part == 1:
            if active in seen:
                break
            seen.add(active)

        # Part 2: run N steps.
        if part == 2 and step == steps:
            break
        step += 1

        new_active = set()
        # Check if bugs remain alive. Collect all adjacencies at the same time.
        all_adjacencies = set()
        for p in active:
            neighbors = get_neighbors(p)
            if sum(n in active for n in neighbors) == 1:
                new_active.add(p)
            all_adjacencies.update(neighbors)
        # Check for new bug-adjacent infestations.
        for p in all_adjacencies - active:
            count = sum(n in active for n in get_neighbors(p))
            if count in {1, 2}:
                new_active.add(p)
        active = frozenset(new_active)

    if part == 1:
        return sum(1 << (x + y * data.width) for x, y in active)
    return len(active)


SAMPLE = """\
....#
#..#.
#..##
..#..
#...."""
TESTS = [(1, SAMPLE, 2129920), (2, SAMPLE, 99)]
# vim:expandtab:sw=4:ts=4

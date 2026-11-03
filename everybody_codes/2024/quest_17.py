"""Everyone Codes Day N."""

import itertools
import math


def manhatten(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Return the Manhatten distance between two points."""
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def constellation_size(stars: set[tuple[int, int]]) -> int:
    """Return the "size" of a constellation."""
    ungrouped = stars.copy()
    grouped = {ungrouped.pop()}
    result = 1
    while ungrouped:
        distance, star = min(
            (manhatten(a, b), a)
            for a, b in itertools.product(ungrouped, grouped)
            if a != b
        )
        result += 1 + distance
        grouped.add(star)
        ungrouped.remove(star)
    return result


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    stars = {
        (x, y)
        for y, line in enumerate(data.splitlines())
        for x, char in enumerate(line)
        if char == "*"
    }

    if part in (1, 2):
        return constellation_size(stars)

    # Group stars into constellation where each start is within 5 of a neighbor.
    neighbors = {
        a: {
            b
            for b in stars
            if a != b and manhatten(a, b) < 6
        }
        for a in stars
    }

    sizes = []
    while stars:
        # Select a star then expand the group to include all nearby neighbors.
        todo = {stars.copy().pop()}
        constellation = set()
        while todo:
            cur = todo.pop()
            stars.remove(cur)
            constellation.add(cur)
            todo.update(n for n in neighbors[cur] if n not in constellation)
        # Get the constellation size.
        sizes.append(constellation_size(constellation))
    return math.prod(sorted(sizes, reverse=True)[:3])


TEST_DATA = [
    """\
*...*
..*..
.....
.....
*.*..""",
    """\
.......................................
..*.......*...*.....*...*......**.**...
....*.................*.......*..*..*..
..*.........*.......*...*.....*.....*..
......................*........*...*...
..*.*.....*...*.....*...*........*.....
.......................................""",
]
TESTS = [
    (1, TEST_DATA[0], 16),
    (3, TEST_DATA[1], 15624),
]

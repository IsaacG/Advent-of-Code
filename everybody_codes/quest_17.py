"""Everyone Codes Day N."""

import itertools
import logging
import math

log = logging.info

def manhatten(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)

def constellation_size(stars):
    ungrouped = stars.copy()
    grouped = {ungrouped.pop()}
    result = 1
    while ungrouped:
        # log(f"{ungrouped=}, {grouped=}")
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

    log("Start")
    neighbors = {
        a: {
            b
            for b in stars
            if a != b and manhatten(a, b) < 6
        }
        for a in stars
    }
    log("Got neighbors")

    sizes = []
    while stars:
        log(f"Unprocessed: {len(stars)}")
        todo = {stars.copy().pop()}
        constellation = set()
        while todo:
            cur = todo.pop()
            stars.remove(cur)
            constellation.add(cur)
            todo.update(n for n in neighbors[cur] if n not in constellation)
        size = constellation_size(constellation)
        log(f"Grouped {len(constellation)} stars into a constellation, {size=}")
        sizes.append(size)
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

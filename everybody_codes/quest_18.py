"""Everyone Codes Day N."""

import itertools
import logging

log = logging.info

def neighbors(i):
    x, y = i
    return [(x + 1, y + 0), (x - 1, y + 0), (x + 0, y + 1), (x + 0, y - 1)]


def flood_fill(canal, trees, start):
    assert start
    todo = start
    filled = set()
    times = []
    for step in itertools.count(0):
        filled.update(todo)
        times.extend([step] * len(trees & todo))
        if trees < filled:
            return times
        todo = {
            n
            for i in todo
            for n in neighbors(i)
            if n in canal and n not in filled
        }

def tree_neighbors(canal, empty, trees, start):
    todo = {start}
    filled = set()
    times = []
    trees = trees.copy()
    trees.remove(start)
    for step in itertools.count(0):
        for t in todo & trees:
            times.append((step, t))
        filled.update(todo)

        todo -= trees
        if not todo:
            return times
        todo = {
            n
            for i in todo
            for n in neighbors(i)
            if n in canal and n not in filled
        }

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    lines = data.splitlines()
    trees = {
        (x, y)
        for y, line in enumerate(lines)
        for x, char in enumerate(line)
        if char == "P"
    }
    empty = {
        (x, y)
        for y, line in enumerate(lines)
        for x, char in enumerate(line)
        if char == "."
    }

    canal = empty | trees
    max_x = len(lines[0]) - 1
    max_y = len(lines) - 1
    todo = {i for i in canal if 0 in i or i[0] == max_x or i[1] == max_y}

    if part < 3:
        times = flood_fill(canal, trees, todo)
        return times[-1]

    log("start tree_graph")
    tree_graph = {
        t: tree_neighbors(canal, empty, trees, t)
        for t in trees
    }
    log("end tree_graph. {tree_graph=}")
    tns = {t: {n[1] for n in ns} for t, ns in tree_graph.items()}
    assert (209, 69) in tns[203, 81]
    assert (203, 81) in tns[209, 69]


    def tree_flood_fill(start, ignores):
        todo = {(0, start)}
        seen = {start}
        total = 0
        while todo:
            dist, t = todo.pop()
            # log(f"Popped {t}. Neighbors: {tree_graph[t]}.")
            total += dist
            assert tree_graph[t]
            for ndist, neighbor in tree_graph[t]:
                if neighbor in seen:
                    continue
                seen.add(neighbor)
                # log(f"Push {neighbor}")
                todo.add((dist + ndist, neighbor))
        assert seen == trees, f"{len(seen)=} != {len(trees)}"
        return total

    log("tree starts")
    empty_set = set()
    tree_starts = sorted(
        (tree_flood_fill(t, empty_set), t) for t in trees
    )
    log(f"tree starts: {tree_starts[:5]}")

    todo = {t[1] for t in tree_starts[:3]}
    log(f"{len(todo)=}")
    seen = set()
    while todo:
        todo = {
            n
            for i in todo
            for n in neighbors(i)
            if n in empty and n not in seen
        }
        seen.update(todo)
    log(f"{len(seen)=} vs {len(empty)=}")

    return min(
        sum(flood_fill(canal, trees, {start}))
        for start in seen
    )

    


TEST_DATA = [
    """\
##########
..#......#
#.P.####P#
#.#...P#.#
##########""",
    """\
#######################
...P..P...#P....#.....#
#.#######.#.#.#.#####.#
#.....#...#P#.#..P....#
#.#####.#####.#########
#...P....P.P.P.....P#.#
#.#######.#####.#.#.#.#
#...#.....#P...P#.#....
#######################""",
    """\
##########
#.#......#
#.P.####P#
#.#...P#.#
##########"""
]
TESTS = [
    (1, TEST_DATA[0], 11),
    (2, TEST_DATA[1], 21),
    (3, TEST_DATA[2], 12),
]

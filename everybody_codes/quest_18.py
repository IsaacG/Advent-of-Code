"""Everyone Codes Day N."""

import itertools
import logging

log = logging.info

def neighbors(i):
    x, y = i
    return [(x + 1, y + 0), (x - 1, y + 0), (x + 0, y + 1), (x + 0, y - 1)]


def flood_fill(canal, trees, start):
    todo = start
    filled = set()
    times = []
    for step in itertools.count(0):
        filled.update(todo)
        times.extend([step] * len(trees & todo))
        if trees < filled or not todo:
            return times
        todo = {
            n
            for i in todo
            for n in neighbors(i)
            if n in canal and n not in filled
        }

def tree_neighbors(canal, trees, start):
    todo = {start}
    filled = set()
    times = []
    trees = trees.copy()
    trees.discard(start)
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

def solve(part: int, data: str, testing) -> int:
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

    tree_graph = {
        t: tree_neighbors(canal, trees, t)
        for t in trees
    }

    def tree_flood_fill(start, ignore, start_dist):
        todo = {(start_dist, start)}
        seen = {start} | ignore
        total = 0
        while todo:
            dist, t = todo.pop()
            total += dist
            for ndist, neighbor in tree_graph[t]:
                if neighbor in seen:
                    continue
                seen.add(neighbor)
                todo.add((dist + ndist, neighbor))
        return total

    empty_set = set()
    tree_starts = sorted(
        (tree_flood_fill(t, empty_set, 0), t) for t in trees
    )

    todo = {t[1] for t in tree_starts[:3]}
    seen = set()
    while todo:
        todo = {
            n
            for i in todo
            for n in neighbors(i)
            if n in empty and n not in seen
        }
        seen.update(todo)

    # got = min(
    #     (sum(flood_fill(canal, trees, {start})), start)
    #     for start in seen
    # )
    # log(f"{got=}")
    # return got[0]
    # got=(12, (3, 2))
    # got=(271050, (151, 27))

    if not testing:
        point = (151, 27)
        ff = sum(flood_fill(canal, trees, {point}))
        log(f"flood fill from {point} => {ff}")

        starting_location = point
        neighboring_trees = tree_neighbors(canal, trees, starting_location)
        log(f"{point} neighboring trees: {neighboring_trees}")
        totals = sum(d for d, t in neighboring_trees)
        nt = {t for d, t in neighboring_trees}
        log(f"{point} {nt=}")
        totals = 0
        totals += sum(tree_flood_fill(t, nt - {t}, 0) for t in nt)
        log(f"Total from {point}: {totals}")
    # return


    results = []
    candidate_well_locations = seen
    # log(f"{candidate_well_locations=}")
    for starting_location in candidate_well_locations:
        neighboring_trees = tree_neighbors(canal, trees, starting_location)
        nt = {t for d, t in neighboring_trees}
        totals = sum(tree_flood_fill(t, nt - {t}, d) for d, t in neighboring_trees)
        results.append(totals)



    # log(results)
    return min(results)

    


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

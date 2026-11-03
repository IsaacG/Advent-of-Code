"""Everyone Codes Day N."""

import itertools
import logging

log = logging.info

Point = tuple[int, int]


def neighbors(position: Point) -> list[Point]:
    """Return the neighbors adjacent to a position."""
    x, y = position
    return [(x + 1, y + 0), (x - 1, y + 0), (x + 0, y + 1), (x + 0, y - 1)]


def simple_flood_fill(canal: set[Point], trees: set[Point], todo: set[Point]) -> int:
    """Simple flood fill from given starting points until all the trees are watered.

    Return the number of steps until all trees are reached.
    """
    seen: set[Point] = set()
    steps = 0
    while trees - seen:
        seen.update(todo)
        todo = {
            neighbor
            for position in todo
            for neighbor in neighbors(position)
            if neighbor in canal and neighbor not in seen
        }
        steps += 1
    return steps - 1


def distance_to_next_trees(canal: set[Point], trees: set[Point], start: Point) -> list[tuple[int, Point]]:
    """Return trees neighboring a point, along with the distance to those trees.

    Flood fill from a start until trees; do not pass through trees.
    """
    todo = {start}
    seen = set()
    times = []
    trees = trees - {start}
    for step in itertools.count(0):
        for tree in todo & trees:
            times.append((step, tree))
        seen.update(todo)

        # Do not pass through trees.
        todo -= trees
        if not todo:
            return times
        todo = {
            neighbor
            for position in todo
            for neighbor in neighbors(position)
            if neighbor in canal and neighbor not in seen
        }
    raise RuntimeError("Not reachable")


def part3(trees: set[Point], empty: set[Point], canal: set[Point]) -> int:
    """Solve part 3."""
    # Distance from trees to their neighboring trees.
    tree_graph = {
        tree: distance_to_next_trees(canal, trees, tree)
        for tree in trees
    }

    def tree_flood_fill(start: Point, ignore: set[Point], start_dist: int) -> int:
        """Using the tree graph, return the total (part 3) tree-distance sum from one tree to all trees.

        Ignored trees are not traversed.
        """
        todo = {(start_dist, start)}
        seen = {start} | ignore
        total = 0
        while todo:
            dist, tree = todo.pop()
            total += dist
            for ndist, neighbor in tree_graph[tree]:
                if neighbor in seen:
                    continue
                seen.add(neighbor)
                todo.add((dist + ndist, neighbor))
        return total

    # Compute the total cost using the tree graph starting from every tree.
    # This is much cheaper than exploring the entire farm as the trees are pretty sparse.
    # Assume the optimal starting point is in the vicinity of an optimal starting tree.
    empty_set: set[Point] = set()
    tree_starts = sorted(
        (tree_flood_fill(tree, empty_set, 0), tree) for tree in trees
    )

    # Expand from the best three trees into the neighboring canal spots for an optimal starting point.
    todo = {tree[1] for tree in tree_starts[:3]}
    seen: set[Point] = set()
    while todo:
        todo = {
            neighbor
            for position in todo
            for neighbor in neighbors(position)
            if neighbor in empty and neighbor not in seen
        }
        seen.update(todo)
    candidate_well_locations = seen

    # For each candidate well location, compute the cost to the nearest trees
    # plus the flood fill from those trees to all over trees (ignoring other trees near the well.
    results = []
    for starting_location in candidate_well_locations:
        nearby_trees_and_distance = distance_to_next_trees(canal, trees, starting_location)
        neighboring_trees = {tree for distance, tree in nearby_trees_and_distance}
        totals = sum(
            tree_flood_fill(tree, neighboring_trees - {tree}, distance)
            for distance, tree in nearby_trees_and_distance
        )
        results.append(totals)

    return min(results)


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    log("Start")
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

    if part < 3:
        max_x = len(lines[0]) - 1
        max_y = len(lines) - 1
        todo = {position for position in canal if 0 in position or position[0] == max_x or position[1] == max_y}
        log("End")
        return simple_flood_fill(canal, trees, todo)

    log("End")
    return part3(trees, empty, canal)


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

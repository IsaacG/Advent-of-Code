"""Everyone Codes Day 15."""
import collections
import queue

Point = tuple[int, int]


def get_distances(points_of_interest: set[Point], spaces: set[Point]) -> dict[Point, dict[Point, int]]:
    """Return distances between points of interest."""

    def neighbors(pos: Point) -> list[Point]:
        """Return all the neighboring accessible map positions."""
        x, y = pos
        n = [(x + 1, y + 0), (x - 1, y + 0), (x + 0, y + 1), (x + 0, y - 1)]
        return [i for i in n if i in spaces]

    def get_dist(starting: Point) -> dict[Point, int]:
        """Return the distance from a starting position to all other points of interest. Dijkstra."""
        bfs = collections.deque([(0, starting)])
        found = 0
        want = len(points_of_interest)
        seen = {starting}
        distances = {}
        while found < want:
            steps, pos = bfs.popleft()
            if pos in points_of_interest:
                distances[pos] = steps
                found += 1
            steps += 1
            for neighbor in neighbors(pos):
                if neighbor not in seen:
                    bfs.append((steps, neighbor))
                    seen.add(neighbor)
        return distances

    # Build a map of the distance from every point of interest to every other point of interest (POI).
    return {pos: get_dist(pos) for pos in points_of_interest}


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    del part
    # Parse the input, building various structures.
    starts = set()
    spaces = set()
    plants = collections.defaultdict(set)
    lines = data.splitlines()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char in "#~":
                continue
            pos = (x, y)
            if char.isalpha():
                plants[char].add(pos)
            spaces.add(pos)
            if y == 0:
                starts.add(pos)

    start = starts.copy().pop()
    # All the plant types to collect.
    all_plant_types = frozenset(plants)
    # All the nodes in the path -- one of each plant type plus return to the start.
    all_want = frozenset(all_plant_types | {"start"})
    points_of_interest = starts.union(*plants.values())

    distances = get_distances(points_of_interest, spaces)
    # For every point of interest, get the nearest plant of every type. Distance, position, plant type.
    nearest = {
        pos: sorted((*min((distances[pos][p], p) for p in plants[t]), t) for t in all_plant_types)
        for pos in points_of_interest
    }

    # Approach, tailored to the specifics of the puzzle input.
    # Plants are grouped in rooms; all plants of a given type are only found in one room.
    # Two optimizations.
    # 1. Rather than considering all uncollected plants as candidates for the next step,
    #    only consider the closest three types.
    # 2. Rather than considering the path through every plant in a room, only track the path through a few plants.
    # The first optimization can be done using the `nearest` which maps the nearest plant of each type to any given POI.
    # The second optimization builds on the first.
    # * Given a position, figure out the nearest three plant types we want to consider.
    # * For each candidate plant type, find the closest position with that plant (candidate position).
    # * For each candidate position, find the next-next three closest plant types and positions.
    # * For each next plant type and its associated three next-next plant positions,
    #   pick positions for the next plant type which minimizes the distance to the next-next plant positions.
    #
    # Assume we're currently at S and considering plants A, B, C.
    # From A we can next visit A1, A2, A3.
    # Select the three plants of type A which minimizes the distance from S through A to A1, A2, A3.
    # Repeat for B, C.
    q: queue.PriorityQueue[tuple[int, frozenset[str], Point]] = queue.PriorityQueue()
    # Steps, items collected, position.
    q.put((0, frozenset(), start))
    seen = set()
    while not q.empty():
        steps, found, pos = q.get()
        # If we collected everything, this is the solition.
        if found == all_want:
            return steps
        # Nearly done! Return to start.
        if found == all_plant_types:
            q.put((steps + distances[pos][start], all_want, start))
        else:
            # Pick the next three closest plant types as candidates.
            next_candidates = [(d, p, t) for d, p, t in nearest[pos] if t not in found][:3]
            # Ugly hack to prune candidates based on distance. Be a bit greedy.
            if len(next_candidates) > 2 and next_candidates[-1][0] > next_candidates[0][0] * 2:
                next_candidates.pop()
            # For each candidate plant type, pick three positions which minimize distance
            # through that plant type to the next-next plant type.
            for _, c_pos, next_type in next_candidates:
                next_have = frozenset(found | {next_type})
                # Once we have all the plant types, the next-next type is the start.
                if next_have == all_plant_types:
                    next_next_candidates = list(starts)
                else:
                    next_next_candidates = [p for d, p, t in nearest[c_pos] if t not in next_have][:3]
                for next_next_pos in next_next_candidates:
                    # Compute the min distance for all next_type plants.
                    next_pos = min(
                        (distances[pos][next_pos] + distances[next_pos][next_next_pos], next_pos)
                        for next_pos in plants[next_type]
                    )[1]
                    d = (steps + distances[pos][next_pos], next_have, next_pos)
                    if d not in seen:
                        q.put(d)
                        seen.add(d)
    raise RuntimeError("No solution found.")


TEST_DATA = [
    """\
#####.#####
#.........#
#.######.##
#.........#
###.#.#####
#H.......H#
###########""",
    """\
##########.##########
#...................#
#.###.##.###.##.#.#.#
#..A#.#..~~~....#A#.#
#.#...#.~~~~~...#.#.#
#.#.#.#.~~~~~.#.#.#.#
#...#.#.B~~~B.#.#...#
#...#....BBB..#....##
#C............#....C#
#####################""",
]
TESTS = [
    (1, TEST_DATA[0], 26),
    (2, TEST_DATA[1], 38),
]

"""Everyone Codes Day 15."""
import collections
import itertools
import logging
import queue

DIRECTIONS = [complex(0, 1), complex(0, -1), complex(1, 0), complex(-1, 0)]


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    # Parse
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
    assert len(starts) == 1
    plantmap = {pos: plant for plant, positions in plants.items() for pos in positions}
    start = starts.copy().pop()
    all_plant_types = frozenset(plants)
    all_want = frozenset(all_plant_types | {"start"})
    all_plant_pos = set().union(*plants.values())
    points_of_interest = starts | all_plant_pos
    logging.info(f"Points: {len(points_of_interest)}. Plant types: {len(plants)}")

    def neighbors(pos):
        x, y = pos
        n = [(x + 1, y + 0), (x - 1, y + 0), (x + 0, y + 1), (x + 0, y - 1)]
        return [i for i in n if i in spaces]

    def get_dist(starting):
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
            for nd in neighbors(pos):
                if nd not in seen:
                    bfs.append((steps, nd))
                    seen.add(nd)
        return distances

    # 3. Part two, second attempt.
    # logging.info({t: len(u) for t, u in plants.items()})
    dist = {pos: get_dist(pos) for pos in points_of_interest}

    if part < 3:
        shortest = None
        for ordering in itertools.permutations(plants):
            s = min(
                sum(dist[a][b] for a, b in zip(path, list(path)[1:]))
                for path in itertools.product(starts, *[plants[i] for i in ordering], starts)
            )
            if shortest is None or s < shortest:
                logging.info(f"{ordering} is shorter than {shortest} at {s}")
                shortest = s
            else:
                logging.info(f"{ordering} is longer than {shortest} at {s}")
        return shortest

    # logging.info("Part three")
    logging.info("Distance graph built.")

    nearest = {
        pos: sorted((*min((dist[pos][p], p) for p in plants[t]), t) for t in all_plant_types)
        for pos in points_of_interest
    }
    logging.info("Nearest graph built.")

    def get_them_all():
        most_found = 0
        q = queue.PriorityQueue()
        q.put((0, set(), start))
        counts = collections.defaultdict(int)
        seen = set()
        while not q.empty():
            steps, found, pos = q.get()
            counts[frozenset(found)] += 1
            if len(found) > most_found:
                logging.info(f"Found {len(found)} in {steps=} at qlen {q.qsize()}")
                most_found = len(found)
                # logging.info(dict(counts))
            if found == all_want:
                return steps
            elif found == all_plant_types:
                logging.info(f"Found a solution: {steps + dist[pos][start]}")
                q.put((steps + dist[pos][start], all_want, start))
            else:
                next_candidates = [(d, p, t) for d, p, t in nearest[pos] if t not in found][:3]
                assert next_candidates
                candidates = []
                for c_dist, c_pos, c_type in next_candidates:
                    c_found = found | {c_type}
                    if c_found == all_plant_types:
                        next_next_candidates = starts
                    else:
                        next_next_candidates = [p for d, p, t in nearest[c_pos] if t not in c_found][:3]
                    assert next_next_candidates
                    for next_next_pos in next_next_candidates:
                        consider = min((dist[pos][next_pos] + dist[next_pos][next_next_pos], next_pos) for next_pos in plants[c_type])[1]
                        candidates.append((consider, c_type))

                assert candidates
                for next_pos, next_type in candidates:
                    next_have = frozenset(found | {next_type})
                    assert len(next_have) > len(found), f"{found=}, {next_type=}, {next_have=}"
                    d = (steps + dist[pos][next_pos], next_have, next_pos)
                    if d not in seen:
                        q.put(d)
                        seen.add(d)

    return get_them_all()


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
    # (3, TEST_DATA[2], None),
]

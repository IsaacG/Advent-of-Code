"""Everyone Codes Day 15."""
import collections
import itertools
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
            pos = complex(x, y)
            if char.isalpha():
                plants[char].add(pos)
            spaces.add(pos)
            if y == 0:
                starts.add(pos)
    assert len(starts) == 1
    plantmap = {pos: plant for plant, positions in plants.items() for pos in positions}
    start = starts.copy().pop()
    all_plant_types = set(plants)
    all_plant_pos = set().union(*plants.values())
    points_of_interest = starts | all_plant_pos
    print(f"Points: {len(points_of_interest)}. Plant types: {len(plants)}")

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
            for d in DIRECTIONS:
                nd = pos + d
                if nd in spaces and nd not in seen:
                    bfs.append((steps, nd))
                    seen.add(nd)
        return distances

    # 3. Part two, second attempt.
    dist = {pos: get_dist(pos) for pos in points_of_interest}

    if part < 3:
        shortest = None
        for ordering in itertools.permutations(plants):
            s = min(
                sum(dist[a][b] for a, b in zip(path, list(path)[1:]))
                for path in itertools.product(starts, *[plants[i] for i in ordering], starts)
            )
            if shortest is None or s < shortest:
                print(f"{ordering} is shorter than {shortest} at {s}")
                shortest = s
            else:
                print(f"{ordering} is longer than {shortest} at {s}")
        return shortest
    print("Part three")
    print("Distance graph built.")
    want_count = len(all_plant_types) + 1
    all_want = all_plant_types | {"start"}
    max_dist = max(max(j.values()) for j in dist.values())
    print(f"{max_dist=}, {len(all_plant_types) + 2}, {max_dist * (len(all_plant_types) + 2)}")

    # 4. Part three, second attempt.
    def get_them_all(starting):
        print(f"get_them_all({starting})")
        q = queue.PriorityQueue()
        q.put((dist[start][starting], {plantmap[starting]}, starting.real, starting.imag))
        while not q.empty():
            steps, found, posx, posy = q.get()
            # print(q.qsize(), len(found))
            pos = complex(posx, posy)
            if found == all_want:
                return steps
            elif found == all_plant_types:
                q.put((steps + dist[pos][start], all_want, start.real, start.imag))
            else:
                for next_type in all_plant_types - found:
                    next_have = found | {next_type}
                    for next_pos in plants[next_type]:
                        q.put((steps + dist[pos][next_pos], next_have, next_pos.real, next_pos.imag))

    if True:
        # 4. Part three, second attempt.
        shortest = None
        for pos in all_plant_pos:
            got = get_them_all(pos)
            print(f"{got} from {pos} vs {shortest}")
            if not shortest or got < shortest:
                shortest = got
        return shortest
    else:
        # 2. Part two, first attempt.
        # Floyd–Warshall algorithm
        largest = len(lines) * len(lines[0]) * 2
        dist = {a: {b: largest for b in spaces} for a in spaces}
        for pos in spaces:
            dist[pos][pos] = 0
            for d in DIRECTIONS:
                nd = pos + d
                if nd in spaces:
                    dist[pos][nd] = 1
        for k, i, j in itertools.product(spaces, repeat=3):
            if dist[i][j] > dist[i][k] + dist[k][j]:
                dist[i][j] = dist[i][k] + dist[k][j]
    print("Done FW")

    for ordering in itertools.permutations(plants):
        s = min(
            sum(dist[a][b] for a, b in zip(path, list(path)[1:]))
            for path in itertools.product(starts, *[plants[i] for i in ordering], starts)
        )
        if shortest is None or s < shortest:
            print(f"{ordering} is shorter than {shortest} at {s}")
            shortest = s
        else:
            print(f"{ordering} is longer than {shortest} at {s}")
    return shortest

    # 1. Part one, first attempt
    bfs = collections.deque([(0, pos) for pos in starts])
    seen = set()
    while bfs:
        steps, pos = bfs.popleft()
        if pos in plants["H"]:
            return 2 * steps
        steps += 1
        for d in DIRECTIONS:
            nd = pos + d
            if nd in spaces and nd not in seen:
                bfs.append((steps, nd))
                seen.add(nd)


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

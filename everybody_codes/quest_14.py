"""Everyone Codes Day N."""
import queue
import typing

OFFSET = {
    "U": ( 0, +1,  0),
    "D": ( 0, -1,  0),
    "R": (+1,  0,  0),
    "L": (-1,  0,  0),
    "F": ( 0,  0, +1),
    "B": ( 0,  0, -1),
}


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    # Track various pieces of growth info.
    all_pos = set()
    leaves = set()
    height = 0
    for line in data.splitlines():
        position = (0, 0, 0)
        for step in line.split(","):
            direction, amount = step[0], step[1:]
            for _ in range(int(amount)):
                position = tuple(pos + offset for pos, offset in zip(position, OFFSET[direction]))  # type: ignore
                all_pos.add(position)
            height = max(height, position[1])
        leaves.add(position)

    if part == 1:
        return height
    if part == 2:
        return len(all_pos)

    # All possible trunk heights and the count.
    trunks = {pos[1] for pos in all_pos if pos[0] == pos[2] == 0}
    num_trunks = len(trunks)

    def trunk_distance(leaf: tuple[int, int, int]) -> dict[int, int]:
        """Return the distance of a leaf to all parts of the main trunk."""
        todo: queue.PriorityQueue[tuple[int, int, tuple[int, int, int]]] = queue.PriorityQueue()
        todo.put((sum(abs(i) for i in leaf), 0, leaf))
        seen = set()
        distances: dict[int, int] = {}
        while len(distances) < num_trunks:
            _, steps, pos = todo.get()
            if pos[0] == pos[2] == 0:
                distances[pos[1]] = steps

            steps = steps + 1
            for offset in OFFSET.values():
                n = typing.cast(tuple[int, int, int], tuple(i + j for i, j in zip(pos, offset)))
                if n not in all_pos or n in seen:
                    continue
                seen.add(n)
                todo.put((sum(abs(i) for i in n) + steps, steps, n))
        return distances

    # Collect the distance from all leaves to all parts of the trunk.
    distances = {leaf: trunk_distance(leaf) for leaf in leaves}
    return min(
        sum(distances[leaf][trunk_height] for leaf in leaves)
        for trunk_height in trunks
    )


TEST_DATA = """\
U20,L1,B1,L2,B1,R2,L1,F1,U1
U10,F1,B1,R1,L1,B1,L1,F1,R2,U1
U30,L2,F1,R1,B1,R1,F2,U1,F1
U25,R1,L2,B1,U1,R2,F1,L2
U16,L1,B1,L1,B3,L1,B1,F1"""

TESTS = [
    (1, "U5,R3,D2,L5,U4,R5,D2", 7),
    (2, "U5,R3,D2,L5,U4,R5,D2\nU6,L1,D2,R3,U2,L1", 32),
    (3, "U5,R3,D2,L5,U4,R5,D2\nU6,L1,D2,R3,U2,L1", 5),
    (3, TEST_DATA, 46),
]

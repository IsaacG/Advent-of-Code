"""Everyone Codes Day N."""
import queue


OFFSET = {
    "U": ( 0, +1,  0),
    "D": ( 0, -1,  0),
    "R": (+1,  0,  0),
    "L": (-1,  0,  0),
    "F": ( 0,  0, +1),
    "B": ( 0,  0, -1),
}


def solve(part: int, data: str, testing) -> int:
    """Solve the parts."""
    all_pos = set()
    leaves = set()
    height = 0
    for line in data.splitlines():
        position = (0, 0, 0)
        for step in line.split(","):
            direction, amount = step[0], step[1:]
            for step in range(int(amount)):
                position = tuple(pos + offset for pos, offset in zip(position, OFFSET[direction]))
                all_pos.add(position)
            height = max(height, position[1])
        leaves.add(position)
        
    if part == 1:
        return height
    if part == 2:
        return len(all_pos)

    def distance(a, b):
        return sum(abs(i - j) for i, j in zip(a, b))

    def trunk_distance(leaf, target) -> int:
        todo = queue.PriorityQueue()
        todo.put((distance(leaf, target), 0, leaf))
        seen = set()
        while not todo.empty():
            _, steps, pos = todo.get()
            if pos == target:
                return steps
            for offset in OFFSET.values():
                n = tuple(i + j for i, j in zip(pos, offset))
                if n not in all_pos or n in seen:
                    continue
                seen.add(n)
                todo.put((distance(n, target) + steps + 1, steps + 1, n))
        raise ValueError()

    def murkiness(pos: tuple[int, int, int]) -> int:
        return sum(trunk_distance(leaf, pos) for leaf in leaves)

    return min(murkiness((0, y, 0)) for y in range(height + 1) if (0, y, 0) in all_pos)


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

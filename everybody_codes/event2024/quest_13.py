"""Everyone Codes Day 13."""
import queue


def solve(data: str) -> int:
    """Solve the parts."""
    heights = {}
    starts = set()
    end = (0, 0)

    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            if char == "S":
                starts.add((x, y))
            if char == "E":
                end = (x, y)
            if char in "SE":
                char = "0"
            if char.isdigit():
                heights[x, y] = int(char)

    def neighbors(position: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = position
        options = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [i for i in options if i in heights]

    min_costs = {end: 0}
    todo: queue.PriorityQueue[tuple[int, tuple[int, int]]] = queue.PriorityQueue()
    todo.put((0, end))
    while not todo.empty():
        cost, position = todo.get()
        if position in starts:
            return cost
        min_costs[position] = cost
        for neighbor in neighbors(position):
            distance = abs(heights[position] - heights[neighbor])
            # Allow wrapping up/down.
            if distance > 5:
                distance = 10 - distance
            if neighbor not in min_costs:
                todo.put((cost + distance + 1, neighbor))
    raise RuntimeError("Did not find a path.")


TEST_DATA = [
    """\
#######
#6769##
S50505E
#97434#
#######""",
    """\
SSSSSSSSSSS
S674345621S
S###6#4#18S
S53#6#4532S
S5450E0485S
S##7154532S
S2##314#18S
S971595#34S
SSSSSSSSSSS""",
]
TESTS = [
    (1, TEST_DATA[0], 28),
    (3, TEST_DATA[1], 14),
]

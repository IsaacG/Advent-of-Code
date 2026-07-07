"""FlipFlop Codes, Puzzle 2: Lasering Walls."""

from lib import helpers
from lib import parsers


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    shift = {">": +1, "<": -1}

    robot = 0
    temps = [0] * 100
    for direction, revDirection in zip(data, reversed(data)):
        robot += shift[direction]
        if part > 1:
            # Parts 2, 3: the wall(s) move. Or, the robot moves in reverse. It's all relative.
            robot -= shift[revDirection]
        robot %= 100
        temps[robot] += 1
    # Part 2: check a specific wall segment.
    if part == 2:
        return temps[0]
    # Parts 1, 3: return max temp * (min) position of the wall with that temp.
    hottest = max(temps)
    return hottest * (temps.index(hottest) + 1)


TEST_DATA = "><>><<>><<<>>>>><><><><><>>>>>"
TESTS = [
    (1, TEST_DATA, 12),
    (2, TEST_DATA, 3),
    (3, TEST_DATA, 1358),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

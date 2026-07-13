"""FlipFlop Codes, Puzzle 1: Coffee Brewing."""

import logging
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if part < 3:
        temps_targets = zip(data, [60] * len(data))
    else:
        temps_targets = zip(data[:len(data) // 2], data[len(data) // 2:])

    return sum(
        (target - temp) * (1 if target > temp else 0 if part == 1 else -5)
        for temp, target in temps_targets
    )


TEST_DATA = "41 87 93 104 46 102 65 105 81 36 66 46 60 65 64 64 61 73 55 69".replace(" ", "\n")
WANT = [76, 1371, 1141]
TESTS = [(i, TEST_DATA, want) for i, want in enumerate(WANT, start=1)]

if __name__ == "__main__":
    helpers.run_solution(globals())

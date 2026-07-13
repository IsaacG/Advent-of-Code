"""FlipFlop Codes, Puzzle 7: Ross's Pet Snake."""

import collections
from lib import helpers, parsers

DIRECTIONS = {">": (1, 0), "<": (-1, 0), "^": (0, 1), "v": (0, -1)}


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    # Set up input data
    moves, sushi_data = data
    if part == 1:
        moves = moves[:len(moves) // 2]
    sushis = iter(sushi_data)

    # Set up board state and counters
    sushi = tuple(next(sushis))
    x, y = 0, 0
    autophagy = 0
    sushi_ate = 0

    # Track the body
    body = collections.deque()
    body.append((x, y))

    for move in moves:
        dx, dy = DIRECTIONS[move]
        x += dx
        y += dy
        if (x, y) == sushi:
            # Eat sushi, do not shrink the tail
            sushi = tuple(next(sushis, (-1, -1)))
            sushi_ate += 1
        else:
            # No sushi, tail shrinks, check for collision.
            body.popleft()
            if (x, y) in body:
                if part == 2:
                    return len(body) + 1
                autophagy += 1
                for _ in range(body.index((x, y)) + 2):
                    body.popleft()
        body.append((x, y))

    if part == 1:
        return sushi_ate
    return len(body) * autophagy


TEST_DATA = """\
>>>^>>v<^<^>>>>v<^^>vv>^<^^^^^<^<vv>^^^>

3,0
5,1
5,0
3,2
7,1
6,1
7,3
7,1
7,6
5,8
5,7
6,6
7,9"""
WANT = [7, 7, 18]
TESTS = [(i, TEST_DATA, want) for i, want in enumerate(WANT, start=1)]

if __name__ == "__main__":
    helpers.run_solution(globals())

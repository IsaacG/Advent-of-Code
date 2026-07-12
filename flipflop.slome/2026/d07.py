"""FlipFlop Codes, Puzzle 7: Ross's Pet Snake."""

import collections
import logging
from lib import helpers, parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    moves, sushis = data
    sushis = iter(sushis)
    sushi = tuple(next(sushis))
    ate = 0
    x, y = 0, 0

    if part == 1:
        for move in moves[:len(moves) // 2]:
            dx, dy = {">": (1, 0), "<": (-1, 0), "^": (0, 1), "v": (0, -1)}[move]
            x += dx
            y += dy
            while (x, y) == sushi:
                ate += 1
                sushi = tuple(next(sushis))
        return ate

    size = 1
    body = collections.deque()
    body.append((x, y))

    if part == 2:
        for move in moves:
            dx, dy = {">": (1, 0), "<": (-1, 0), "^": (0, 1), "v": (0, -1)}[move]
            x += dx
            y += dy
            dropped = body.popleft()
            if (x, y) in body:
                return size
            body.append((x, y))
            if (x, y) == sushi:
                size += 1
                sushi = tuple(next(sushis))
                body.appendleft(dropped)
        raise ValueError("Not found")

    eat_self = 0
    if part == 3:
        for move in moves:
            dx, dy = {">": (1, 0), "<": (-1, 0), "^": (0, 1), "v": (0, -1)}[move]
            x += dx
            y += dy
            dropped = body.popleft()
            if (x, y) in body:
                eat_self += 1
                for _ in range(body.index((x, y)) + 2):
                    body.popleft()
            body.append((x, y))
            if (x, y) == sushi:
                size += 1
                sushi = tuple(next(sushis, (-1, -1)))
                body.appendleft(dropped)
        return len(body) * eat_self



# PARSER = parsers.parse_one_str
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
TESTS = [
    (1, TEST_DATA, 7),
    (2, TEST_DATA, 7),
    (3, TEST_DATA, 18),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

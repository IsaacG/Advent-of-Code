"""FlipFlop Codes: N."""

import logging
from lib import helpers, parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    board = {
        (x, y): helpers.ARROW_DIRECTIONS_T[char]
        for y, line in enumerate(data)
        for x, char in enumerate(line)
    }

    directions = set(helpers.FOUR_DIRECTIONS_T)
    rotate = helpers.rotate_counterclockwise
    # rotate = helpers.rotate_clockwise
    max_y = len(data) - 1
    max_x = len(data[0]) - 1
    edges = {i for i in board if i[0] in {0, max_x} or i[1] in {0, max_y}}
    non_edge = set(board) - edges

    # Drive the city.
    pos = (0, 0)
    seen = set()
    while pos not in seen:
        seen.add(pos)
        pos = (pos[0] + board[pos][0], pos[1] + board[pos][1])

    # Part one: return steps until looping.
    if part == 1:
        return len(seen)

    # Part two: try changing all the streets we previously visited.
    # Part three: try changing all non-edges.
    if part == 2:
        non_edge &= seen

    best = 0
    for street in non_edge:
        modified_streets = board.copy()
        for d in directions - {board[street]}:
            modified_streets[street] = d
            turns = 3 if part == 3 else 0

            pos = (0, 0)
            seen = set()

            while pos not in seen or turns > 0:
                if pos in seen:
                    if pos in edges:
                        break
                    turns -= 1
                    direction = rotate(*modified_streets[pos])
                else:
                    seen.add(pos)
                    direction = modified_streets[pos]
                pos = (pos[0] + direction[0], pos[1] + direction[1])


            best = max(best, len(seen))
    return best


PARSER = parsers.parse_one_str_per_line
TEST_DATA = """\
>>>>vvv>vv
>^>>>>>>>v
>>^<>vvv>v
^^^>>vv>^v
^<<<v>vv>v
^<>^<>v>v<
>^^<<<<<vv
^^^<^v<<>v
^v<^<<vvvv
^<^<<<<<<<"""
TESTS = [
    (1, TEST_DATA, 45),
    (2, TEST_DATA, 49),
    (3, TEST_DATA, 61),
    # (2, TEST_DATA[1], None),
    # (3, TEST_DATA[2], None),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

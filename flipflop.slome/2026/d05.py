"""FlipFlop Codes, Puzzle 5: One Way City."""

import logging
from lib import helpers, parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    board = {pos: helpers.ARROW_DIRECTIONS_T[char] for pos, char in data.chars.items()}

    directions = set(helpers.FOUR_DIRECTIONS_T)
    rotate = helpers.rotate_counterclockwise
    edges = {i for i in board if i[0] in {0, data.max_x} or i[1] in {0, data.max_y}}
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
    # Try to modify every non-edge street.
    for street in non_edge:
        modified_streets = board.copy()
        # Try every direction excluding the current one.
        for direction in directions - {board[street]}:
            modified_streets[street] = direction

            # Drive the map.
            pos = (0, 0)
            seen = set()
            turns = 3 if part == 3 else 0

            while pos not in seen or turns:
                direction = modified_streets[pos]
                if pos in seen:
                    if pos in edges:
                        break
                    turns -= 1
                    direction = rotate(*direction)
                else:
                    seen.add(pos)
                pos = (pos[0] + direction[0], pos[1] + direction[1])

            best = max(best, len(seen))

    return best


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
    (3, TEST_DATA, 66),
]

if __name__ == "__main__":
    helpers.run_solution(globals())

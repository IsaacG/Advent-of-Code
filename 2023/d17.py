#!/bin/python
"""Advent of Code, Day 17: Clumsy Crucible."""

import queue
from lib import aoc

SAMPLE = [
    """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""",
    """\
111111111111
999999999991
999999999991
999999999991
999999999991""",
]

InputType = tuple[dict[tuple[int, int], int], tuple[int, int]]


class Day17(aoc.Challenge):
    """Day 17: Clumsy Crucible."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=102),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=94),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=71),
    ]
    INPUT_PARSER = aoc.int_map

    def solver(self, parsed_input: InputType, part_one: bool) -> int:
        """Return the minimum heat loss from start to end."""
        board, end = parsed_input
        max_distance = 3 if part_one else 10
        seen = {}

        loss, location, direction, count = 0, (0, 0), (0, 0), 0
        todo = queue.PriorityQueue()
        todo.put((loss, location, direction, count))

        while not todo.empty():
            loss, location, direction, count = todo.get()
            if location == end and (part_one or count >= 4):
                return loss
            
            # Try moving in all four directions.
            for next_direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                if next_direction[0] == -direction[0] and next_direction[1] == -direction[1]:
                    # No reversing.
                    continue
                if not part_one and direction != (0, 0) and next_direction != direction and count < 4:
                    # Part two: no turning prior to 4 moves.
                    continue
                if next_direction == direction and count == max_distance:
                    # No moving in one direction for too long.
                    continue

                next_location = (location[0] + next_direction[0], location[1] + next_direction[1])
                if next_location not in board:
                    continue

                next_loss = loss + board[next_location]
                next_count = count + 1 if next_direction == direction else 1

                # Avoid looping when a path was already explored at equal/lower cost.
                fp = (next_location, next_direction, next_count)
                if fp in seen and seen[fp] <= next_loss:
                    continue
                seen[fp] = next_loss

                todo.put((next_loss, next_location, next_direction, next_count))

        raise RuntimeError("Failed to solve")

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        board = {
            (idx_x, idx_y): int(val)
            for idx_y, line in enumerate(puzzle_input.splitlines())
            for idx_x, val in enumerate(line)
        }
        end = list(board.keys())[-1]
        return board, end

# vim:expandtab:sw=4:ts=4

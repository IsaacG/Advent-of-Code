#!/bin/python
"""Advent of Code, Day 9: Movie Theater."""
import collections
import itertools

from lib import aoc

SAMPLE = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""


class Day09(aoc.Challenge):
    """Day 9: Movie Theater."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=50),
        aoc.TestCase(part=2, inputs=SAMPLE, want=24),
    ]

    def solver(self, puzzle_input: list[list[int]], part_one: bool) -> int:
        if puzzle_input[0][0] == puzzle_input[1][0]:
            points = puzzle_input[-1:] + puzzle_input
        else:
            points = puzzle_input + puzzle_input[:1]
        lines = len(puzzle_input)

        # y, x1, x2
        horizontal_walls = [
            [points[i][1], *sorted([points[i][0], points[i+1][0]])]
            for i in range(0, lines, 2)
        ]
        # x, y1, y2
        vertical_walls = [
            [points[i][0], *sorted([points[i][1], points[i+1][1]])]
            for i in range(1, lines + 1, 2)
        ]

        # Used for the accurate_valid() test:
        white_tiles = self.white_tiles(points, vertical_walls, horizontal_walls)

        def accurate_valid(rect_x1: int, rect_y1: int, rect_x2: int, rect_y2: int) -> bool:
            """Check if a rectangle is fully enclosed by the border.

            This utilizes a list of all the white rectangles to check for any overlap.
            This correctly handles any input.
            """
            top, bottom = sorted([rect_y1, rect_y2])
            left, right = sorted([rect_x1, rect_x2])

            return not any(
                y1 <= bottom and y2 >= top and x1 <= right and x2 >= left
                for x1, y1, x2, y2 in white_tiles
            )

        def valid_with_assumptions(rect_x1: int, rect_y1: int, rect_x2: int, rect_y2: int) -> bool:
            """Check if a rectangle is fully enclosed by the border.

            This checks if any borders cross through the rectangle.
            This approach is faster but relies on the input being "nice";
            if two adjacent borders run through the rectangle, this method will incorrectly
            flag the rectangle as not valid.
            """
            top, bottom = sorted([rect_y1, rect_y2])
            left, right = sorted([rect_x1, rect_x2])

            for (y, x1, x2) in horizontal_walls:
                if top < y < bottom and x1 < right and x2 > left:
                    return False
            for (x, y1, y2) in vertical_walls:
                if left < x < right and y1 < bottom and y2 > top:
                    return False
            return True

        best = 0
        for (x1, y1), (x2, y2) in itertools.combinations(puzzle_input, 2):
            size = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            # if size > best and (part_one or accurate_valid(x1, y1, x2, y2)):
            if size > best and (part_one or valid_with_assumptions(x1, y1, x2, y2)):
                best = size
        return best

    def condensed_slower_code(self, puzzle_input: list[list[int]], part_one: bool) -> int:
        """A more compact version of the solution."""
        points = puzzle_input[-1:] + puzzle_input
        walls = [
            (*sorted([x1, x2]), *sorted([y1, y2]))
            for (x1, y1), (x2, y2) in zip(points, points[1:])
        ]

        def valid(x1, y1, x2, y2):
            top, bottom = sorted([y1, y2])
            left, right = sorted([x1, x2])
            return not any(
                y1 < bottom and y2 > top and x1 < right and x2 > left
                for (x1, x2, y1, y2) in walls
            )

        return max(
            (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            for (x1, y1), (x2, y2) in itertools.combinations(puzzle_input, 2)
            if part_one or valid(x1, y1, x2, y2)
        )

    def white_tiles(
        self,
        points: list[list[int]],
        vertical_walls: list[list[int]],
        horizontal_walls: list[list[int]],
    ) -> list[tuple[int, int, int, int]]:
        """Return a list of rectangles that composes all the white tiles.

        Use line scanning to walk the board, splitting it into horizontal segments separated
        by any line which contains a horizontal wall.

        Between horizontal walls, the white tiles are the regions outside pairs of vertical walls.
        Crossing a wall changes the tile color from white to not-white and back.

        Along lines with horizontal walls, a bit more care needs to be taken to track inside vs outside.
        """
        # Add an imaginary boundary (left and right walls) so white tiles have a place to start.
        min_x = min(x for x, y in points)
        max_x = max(x for x, y in points)
        min_y = min(y for x, y in points)
        max_y = max(y for x, y in points)
        walls = vertical_walls.copy() + [
            (min_x - 5, min_y - 5, max_y + 5), (max_x + 5, min_y - 5, max_y + 5)
        ]
        # Sort walls into two groups. One by the walls' top, the other by the bottom.
        # These are used to add/remove a wall when we get to any given y value.
        wall_starts = collections.deque(sorted(walls, key=lambda x: x[1]))
        wall_ends = collections.deque(sorted(walls, key=lambda x: x[2]))
        # horizontal is used to check if a horizontal wall exists between
        # any two walls that start/end on the same line.
        horizontal = collections.defaultdict(set)
        for y, x1, x2 in horizontal_walls:
            horizontal[y].add((x1, x2))

        # active: The walls in play for the current range.
        # This is kept sorted by x so we can identify wall pairs which bound inside/outside.
        active = list[list[int]]()

        # x1, y1, x2, y2
        white_tiles = []

        # Arbitrary start location.
        prior_y = min_y - 10
        while wall_ends:
            # Increment the y-scanner to the next horizontal line.
            cur_y = wall_ends[0][2]
            if wall_starts:
                cur_y = min(wall_starts[0][1], cur_y)

            # Add ranges from prior_y to cur_y (excluding the fold line).
            if cur_y >= prior_y:
                cur_y -= 1
                for (x1, *_), (x2, *_) in itertools.batched(active, 2):
                    if x1 + 1 < x2:  # ignore adjacent touching lines
                        white_tiles.append((x1 + 1, prior_y, x2 - 1, cur_y))
                cur_y += 1

            # Treat the fold line as its own range.
            # Add new walls that start here. Compute white tiles for this row. Remove walls that ended.
            while wall_starts and wall_starts[0][1] == cur_y:
                active.append(wall_starts.popleft())
            active.sort(key=lambda x: x[0])
            # Walk the line.
            white = False
            for (x1, top1, bottom1), (x2, top2, bottom2) in itertools.pairwise(active):
                white = not white
                # If these walls are connected, there are no white tiles between them.
                if (x1, x2) in horizontal[cur_y]:
                    # If the walls make an L-7 or F-J shape, there is only one wall crossing across both of them.
                    if top1 == bottom2 or bottom1 == top2:
                        white = not white
                elif white:  # Otherwise there are tiles between them.
                    white_tiles.append((x1 + 1, cur_y, x2 - 1, cur_y))

            # Remove walls that ended.
            while wall_ends and wall_ends[0][2] == cur_y:
                active.remove(wall_ends.popleft())

            # The next block starts after the fold line.
            prior_y = cur_y + 1
        # Sort the ranges for easier reading.
        white_tiles.sort(key=lambda x: (x[1], x[0]))
        return white_tiles

# vim:expandtab:sw=4:ts=4

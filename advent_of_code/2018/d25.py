#!/bin/python
"""Advent of Code, Day 25: Four-Dimensional Adventure."""

from lib import aoc

SAMPLE = [
    """\
0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0""",
    """\
-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0""",
    """\
1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2""",
    """\
1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2""",
]


class Day25(aoc.Challenge):
    """Day 25: Four-Dimensional Adventure."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=2),
        aoc.TestCase(part=1, inputs=SAMPLE[1], want=4),
        aoc.TestCase(part=1, inputs=SAMPLE[2], want=3),
        aoc.TestCase(part=1, inputs=SAMPLE[3], want=8),
    ]

    def solver(self, puzzle_input: list[list[int]], part_one: bool) -> int:
        """Return how many constellations exist by grouping stars based on distances."""
        groups = 0
        todo = set(tuple(i) for i in puzzle_input)
        while todo:
            groups += 1
            group = {todo.pop()}

            prior_size = 0
            while len(group) != prior_size:
                prior_size = len(group)
                candidates = iter(list(todo))
                while True:
                    to_add = next(
                        (
                            i for i in candidates
                            if any(
                                abs(i[0] - j[0]) + abs(i[1] - j[1]) + abs(i[2] - j[2]) + abs(i[3] - j[3]) <= 3
                                for j in group
                            )
                        ), None
                    )
                    if to_add is None:
                        break
                    group.add(to_add)
                    todo.remove(to_add)

        return groups

# vim:expandtab:sw=4:ts=4

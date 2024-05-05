#!/bin/python
"""Advent of Code, Day 11: Chronal Charge. Find the subgrid with the max sum value."""

from lib import aoc

SAMPLE = ["18", "42"]


class Day11(aoc.Challenge):
    """Day 11: Chronal Charge."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want="33,45"),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want="21,61"),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want="90,269,16"),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want="232,251,12"),
    ]
    INPUT_PARSER = aoc.parse_one_int
    PARAMETERIZED_INPUTS = [(2, 3, False), (2, 100, True)]

    def solver(self, parsed_input: int, *args, **kwargs) -> str:
        serial = parsed_input
        range_start, range_end, include_size = args[0]

        def power_level(x: int, y: int) -> int:
            rack_id = x + 10
            power = rack_id * (rack_id * y + serial)
            return ((power // 100) % 10) - 5

        grid = []
        for y in range(300):
            row = []
            for x in range(300):
                row.append(power_level(x + 1, y + 1))
            grid.append(row)

        def max_grid(size: int) -> tuple[int, int, int]:
            xgroups = []
            for row in grid:
                xrow = []
                window = sum(row[:size])
                for x in range(300 - size):
                    window += row[x + size]
                    xrow.append(window)
                    window -= row[x]
                xgroups.append(xrow)

            ygroups = []
            for col in zip(*xgroups):
                ycol = []
                window = sum(col[:size])
                for y in range(300 - size):
                    window += col[y + size]
                    ycol.append(window)
                    window -= col[y]
                ygroups.append(ycol)

            groups = list(zip(*ygroups))
            return max(
                (val, x, y)
                for y, row in enumerate(groups)
                for x, val in enumerate(row)
            )

        (val, x, y), size = max(
            (max_grid(size), size)
            for size in range(range_start, range_end)
        )

        out = [x + 1, y + 1]
        if include_size:
            out.append(size + 1)
        return ",".join(str(i) for i in out)

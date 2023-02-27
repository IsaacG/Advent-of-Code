#!/bin/python
"""Advent of Code, Day 11: Chronal Charge. Find the subgrid with the max sum value."""

import typer
from lib import aoc

SAMPLE = ["18", "42"]
LineType = int
InputType = list[LineType]


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

    def solver(self, parsed_input: InputType, *args, **kwargs) -> int:
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
        grid_t = list(zip(*grid))

        sumgrid = [[0] * 297 for _ in range(297)]
        for x in range(297):
            for y in range(297):
                sumgrid[y][x] = sum(
                    grid[y + dy][x + dx]
                    for dx in range(3)
                    for dy in range(3)
                )

        size = 3
        val, xmax, ymax = max(
            (val, x, y)
            for y, row in enumerate(sumgrid)
            for x, val in enumerate(row)
        )
        for i in range(3, range_end):
            sumgrid.pop()
            for row in sumgrid:
                row.pop()
            for x in range(299 - i):
                for y in range(299 - i):
                    sumgrid[y][x] += sum(grid[y + i][x:x + i + 1])
                    sumgrid[y][x] += sum(grid_t[x + i][y: y + i])
            cand_val, cand_x, cand_y = max(
                (val, x, y)
                for y, row in enumerate(sumgrid)
                for x, val in enumerate(row)
            )
            if cand_val > val:
                val, xmax, ymax, size = cand_val, cand_x, cand_y, i

        out = [xmax + 1, ymax + 1]
        if include_size:
            out.append(size + 1)
        return ",".join(str(i) for i in out)


if __name__ == "__main__":
    typer.run(Day11().run)

# vim:expandtab:sw=4:ts=4

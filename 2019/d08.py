#!/usr/bin/env python
"""Day 8: Space Image Format.

Read and flatten layered images.
"""

import collections
import math
import more_itertools

from lib import aoc


WIDTH = 25
HEIGHT = 6
chunked = more_itertools.chunked


class Day08(aoc.Challenge):
    """Day 8."""

    INPUT_PARSER = aoc.parse_one_str

    def part1(self, puzzle_input: str) -> int:
        """Find the min layer."""
        layers = chunked(puzzle_input, WIDTH * HEIGHT)
        count = sorted((collections.Counter(layer) for layer in layers), key=lambda x: x['0'])[0]
        return count['1'] * count['2']

    def part2(self, puzzle_input: str) -> int:
        """Flatten layers, handling transparent pixels."""
        image = [
            [row for row in chunked(layer, WIDTH)]
            for layer in chunked(puzzle_input, WIDTH * HEIGHT)
        ]
        out = []
        for rw in range(HEIGHT):
            row = []
            for col in range(WIDTH):
                for layer in range(len(image)):
                    if image[layer][rw][col] != '2':
                        row.append('█' if image[layer][rw][col] == '1' else ' ')
                        break
            out.append(''.join(row))
        # Displays the actual solution.
        # print('\n'.join(out))
        # Meaningless number to use in the solutions file.
        return math.prod(sum(True for i in row if i != ' ') for row in out)

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

def solve(data: str, part: int) -> int:
    """Flatten layers, handling transparent pixels."""
    layers = more_itertools.chunked(data, WIDTH * HEIGHT)
    if part == 1:
        count = sorted((collections.Counter(layer) for layer in layers), key=lambda x: x['0'])[0]
        return count['1'] * count['2']

    image = [
        [row for row in more_itertools.chunked(layer, WIDTH)]
        for layer in layers
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
    return math.prod(sum(i != ' ' for i in row) for row in out)


TESTS = list[tuple[int, int, int]]()

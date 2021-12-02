#!/usr/bin/env python
"""Day 8: Space Image Format.

Read and flatten layered images.
"""

import collections
import more_itertools
import typer

from lib import aoc


WIDTH = 25
HEIGHT = 6
chunked = more_itertools.chunked


class Day08(aoc.Challenge):

  def part1(self, line: str) -> int:
    """Find the min layer."""
    layers = chunked(line, WIDTH * HEIGHT)
    count = sorted((collections.Counter(layer) for layer in layers), key=lambda x: x['0'])[0]
    return count['1'] * count['2']

  def part2(self, line: str) -> int:
    """Flatten layers, handling transparent pixels."""
    image = [
      [row for row in chunked(layer, WIDTH)]
      for layer in chunked(line, WIDTH * HEIGHT)
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
    return self.mult(sum(True for i in row if i != ' ') for row in out)

  def parse_input(self, puzzle_input: str):
    return puzzle_input


if __name__ == '__main__':
  typer.run(Day08().run)

# vim:ts=2:sw=2:expandtab

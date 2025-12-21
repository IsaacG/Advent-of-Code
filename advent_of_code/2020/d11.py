#!/usr/bin/env python
"""Day 11. Ferry Seating Area a.k.a. Conway's Game of Life."""

from lib import aoc
import data
S1 = data.D11S1
S2 = data.D11S2


class Day11(aoc.Challenge):
  """Solve Day 11."""

  TESTS = [
    aoc.TestCase(inputs=S1[0], part=1, want=37),
    aoc.TestCase(inputs=S2[0], part=2, want=26),
  ]

  def solver(self, puzzle_input: aoc.Map, part_one: bool) -> int:
    seats = puzzle_input.coords.get("#", set()) | puzzle_input.coords["L"]
    occupied = puzzle_input.coords.get("#", set())
    board = set(puzzle_input.chars.keys())
    limit = 4 if part_one else 5
    prior = set((1,1))
    while prior != occupied:

        def look(pos, direction):
            x, y = pos
            dx, dy = direction
            x += dx
            y += dy
            if part_one:
                return (x, y) in occupied
            while (x, y) in board:
                if (x, y) in occupied:
                    return True
                elif (x, y) in seats:
                    return False
                x += dx
                y += dy
            return False

        new = set()
        for seat in seats:
            adjacent_occupied = sum(look(seat, d) for d in aoc.EIGHT_DIRECTIONS_T)
            if seat not in occupied:
                if adjacent_occupied == 0:
                    new.add(seat)
            else:
                if adjacent_occupied < limit:
                    new.add(seat)
        prior, occupied = occupied, new

    return len(occupied)

#!/usr/bin/env pypy
"""Day 23.

Crab Cups.
The small crab challenges you to a game! The crab is going to mix up some cups,
and you have to predict where they'll end up.
https://adventofcode.com/2020/day/23
"""

import typer
from lib import aoc
from typing import List, Optional


class Cup:
  """Linked list node."""

  TIMER_ITERATIONS = (50, 3)
  next = None  # type: Cup

  def __init__(self, val: int, prev: Optional["Cup"]):
    """Create a Cup."""
    self.val = val
    if prev:
      prev.next = self

  def nodes(self):
    """Generate all nodes starting at `self`."""
    yield self
    c = self.next
    while c != self:
      yield c
      c = c.next


class Day23(aoc.Challenge):
  """Track the cups."""

  TESTS = (
    aoc.TestCase(inputs='389125467', part=1, want=67384529),
    aoc.TestCase(inputs='389125467', part=2, want=149245887792),
  )

  def solve(self, cups: List[int], rounds: int) -> Cup:
    """Solve the cups game.

    Use a list of labels as a starting point.
    Run for `rounds` iteration.
    Return the cup labeled "1".
    """
    # Build a linked list of Cups with a map from label to Cup.
    mapping = {}
    cur = None  # type: Cup
    for i in cups:
      cur = Cup(i, cur)
      mapping[i] = cur

    # Link the last and first cups, making the list circular.
    cur.next = mapping[cups[0]]

    # Start the game with the "first" Cup.
    cur = mapping[cups[0]]
    highest = max(cups)
    for rounds in range(rounds):
      # Destination label cannot be current or next three labels.
      not_valid_dest = (cur.val, cur.next.val, cur.next.next.val, cur.next.next.next.val)
      dest = cur.val
      while dest in not_valid_dest:
        # Try one lower value - with circular counting.
        dest = (dest - 1) or highest

      # Move 3 Cups from cur to dest.
      other = mapping[dest]

      # Update the cups with the next three cups shifted.
      # C => (j k l) => x y z D => e
      # C: current cup. D: destination cup. j k l are the three to move.
      # Update C.next = x; l.next = e; D.next = j
      if False:
        # Does not work. No idea why.
        cur.next, cur.next.next.next.next, other.next = cur.next.next.next.next, other.next, cur.next
      else:
        # Longer form.
        taken = cur.next
        taken_end = cur.next.next.next
        taken_next = cur.next.next.next.next
        dest_plus_one = other.next

        cur.next = taken_next
        other.next = taken
        taken_end.next = dest_plus_one

      # Move to the next Cup.
      cur = cur.next

    return mapping[1]

  def part2(self, cups: List[int]) -> int:
    """Extend the cups through 1M. Play for 10M rounds."""
    cups = list(cups)
    cups.extend(range(10, int(1e6) + 1))
    one = self.solve(cups, int(1e7))
    return one.next.val * one.next.next.val

  def part1(self, cups: List[int]) -> int:
    """Play for 100 rounds, return the list of Cups."""
    cups = list(cups)
    one = self.solve(cups, 100)
    vals = [i.val for i in one.nodes()]
    return int("".join(str(i) for i in vals[1:]))

  def parse_input(self, puzzle_input: str):
    return [int(i) for i in puzzle_input]


if __name__ == '__main__':
  typer.run(Day23().run)

# vim:ts=2:sw=2:expandtab

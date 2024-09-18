#!/usr/bin/env python
"""Day 13. Bus terminal departure schedules."""

from lib import aoc
from typing import List


SAMPLE = ["""\
939
7,13,x,x,59,x,31,19
"""]


class Day13(aoc.Challenge):
  """Figure out when busses depart."""

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=295),
    aoc.TestCase(inputs=SAMPLE[0], part=2, want=1068781),
  )
  INPUT_PARSER = aoc.parse_one_str_per_line

  def part1(self, puzzle_input: List[str]) -> int:
    """Find which bus will first arrive once we are at the bus terminal."""
    earliest = int(puzzle_input[0])
    busses = [int(i) for i in puzzle_input[1].split(',') if i != 'x']
    departs_at = {}
    for bus in busses:
      depart_time = (int(earliest / bus) + 1) * bus
      departs_at[depart_time] = bus
    pick = min(departs_at)
    return (pick - earliest) * departs_at[pick]

  def part2(self, puzzle_input: List[str]) -> int:
    """Find out a time at which the busses will all arrive one minute apart.

    The bus numbers are all prime which is handy.
    Start with start_time=1 and step=1.
    Loop with start_time+=step until we find a time as which a bus will depart
    at that time (plus bus offset). Call that bus number, N.
    Now we want times that are start_time + multiples of N so update step *= N.
    The step accumulates all the busses we "found" so we can drop the bus from
    the pending list once it is found.
    Continue stepping through time, updating step *= N with each bus we find,
    until we found all busses.
    """
    # Build a list of offset, bus for all busses we care about.
    buslist = [int(i) if i != 'x' else 0 for i in puzzle_input[1].split(',')]
    busses = [(a, b) for a, b in enumerate(buslist) if b]

    start_time = 0
    step = 1
    while busses:
      start_time += step

      # See if any new busses align with this timestamp.
      newfounds = [b for (k, b) in busses if not (start_time + k) % b]
      if newfounds:
        newfound = newfounds[0]
        # Remove the bus from the unfound bus list and update the step
        # so future iterations would include this bus, too.
        busses = [(a, b) for a, b in busses if b != newfound]
        step *= newfound
    else:
      return start_time

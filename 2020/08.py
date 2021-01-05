#!/usr/bin/env pypy

import typer
from typing import List, Tuple

from lib import aoc


SAMPLE = ["""\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
""", """\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""]


class Day08(aoc.Challenge):

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=5),
    aoc.TestCase(inputs=SAMPLE[1], part=2, want=8),
  )

  def compute(self, lines: List[str]) -> Tuple[int, bool]:
    """Run the code, returning the accumulator and if the end was hit."""
    # Accumulator
    acc = 0
    # Instruction pointer. The next instruction to execute.
    ptr = 0
    # Track which instructions were previously executed for loop detection.
    seen = set()
    # max value for the ptr, ie the end of the instructions.
    max_ptr = len(lines) - 1

    while True:
      seen.add(ptr)
      op, sval = lines[ptr].split()
      val = int(sval)
      if op == 'nop':
        ptr += 1
      elif op == 'jmp':
        ptr += val
      elif op == 'acc':
        ptr += 1
        acc += val
      else:
        raise ValueError(f'Invalid op {op}')

      # Got to the end.
      if ptr > max_ptr:
        return acc, True
      # Loop detection.
      if ptr in seen:
        return acc, False

  def part1(self, lines: List[str]) -> int:
    """Run the code until a loop is detected."""
    acc, end = self.compute(lines)
    assert not end
    return acc

  def part2(self, lines: List[str]) -> int:
    """Swap jmp<>nop until the code can run to the end."""
    for i in range(len(lines)):
      op, val = lines[i].split()
      line = lines[i]
      if op == 'acc':
        continue
      if op == 'nop':
        lines[i] = f'jmp {val}'
      elif op == 'jmp':
        lines[i] = f'nop {val}'
      acc, end = self.compute(lines)
      if end:
        return acc
      lines[i] = line
    raise RuntimeError


if __name__ == '__main__':
  typer.run(Day08().run)

# vim:ts=2:sw=2:expandtab

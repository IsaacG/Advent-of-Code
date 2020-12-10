#!/bin/python

import collections
import util
import re
import sys
import time
from typing import List, Dict


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

TESTS = (
  util.TestCase(inputs=SAMPLE[0], part=1, want=5),
  util.TestCase(inputs=SAMPLE[1], part=2, want=8),
)


def compute(lines: List[str]) -> int:
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
    op, val = lines[ptr].split()
    val = int(val)
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


def part1(lines: List[str]) -> int:
  """Run the code until a loop is detected."""
  acc, end = compute(lines)
  assert end == False
  return acc


def part2(lines: List[str]) -> int:
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
    acc, end = compute(lines)
    if end:
      return acc
    lines[i] = line


CONFIG = {
  'debug': False,
  'funcs': {1: part1, 2: part2},
  'tranform': str,
  'tests': TESTS,
  'sep': '\n',
}


# ######################################### #
# Fixed code. Probably do not need to edit. #

debug = lambda x: util.debug(CONFIG, x)

def main():
  """Run the tests then the problems."""
  util.run_tests(CONFIG)

  data = util.load_data(sys.argv[1], config=CONFIG)
  for i, func in enumerate((part1, part2)):
    debug(f"Running part {i + 1}:")
    print(func(data))


if __name__ == '__main__':
  main()

# vim:ts=2:sw=2:expandtab

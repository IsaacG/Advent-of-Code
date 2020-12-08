#!/bin/python

import collections
from util import load_data
import re
import time
from typing import List, Dict


SAMPLE1 = """\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""

SAMPLE2 = """\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""

TEST_DATA = {
  'input1': SAMPLE1,
  'input2': SAMPLE2,
  'want1': 5,
  'want2': 8,
}


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


def get_func(i):
  if i == 1:
    return part1
  elif i == 2:
    return part2
  else:
    raise ValueError(f'Bad part {i}')


def test():
  """Assert solution works."""
  for i in (1, 2):
    if TEST_DATA[f'input{i}'].strip() and TEST_DATA[f'want{i}']:
      sample_text = TEST_DATA[f'input{i}']
      sample_data = load_data(text=sample_text)
      func = get_func(i)
      want = TEST_DATA[f'want{i}']
      got = func(sample_data)
      assert want == got, f'part{i}: want({want}) != got({got})'


def main():
  test()
  data = load_data()
  for i in (1, 2):
    if TEST_DATA[f'input{i}'].strip():
      func = get_func(i)
      print(func(data))


if __name__ == '__main__':
  main()

# vim:ts=2:sw=2:expandtab

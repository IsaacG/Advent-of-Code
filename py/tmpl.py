#!/bin/python

import collections
from util import load_data
import re
import time
from typing import List, Dict


SAMPLE1 = """\
"""

SAMPLE2 = """\
"""

TEST_DATA = {
  'input1': SAMPLE1,
  'input2': SAMPLE2,
  'want1': None,
  'want2': None,
}


def work(lines: List[str]) -> int:
  return 0


def part1(lines: List[str]) -> int:
  return work(lines)


def part2(lines: List[str]) -> int:
  return work(lines)


# ######################################### #
# Fixed code. Probably do not need to edit. #

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

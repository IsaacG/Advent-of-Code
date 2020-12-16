#!/bin/python
"""Advent of Code framework."""

import dataclasses
import os
import pathlib
import sys
import time

from typing import Callable, Iterable, List


def mult(nums: Iterable[int]) -> int:
  """Product of all values. Like sum() but with multiplication."""
  p = 1
  for n in nums:
    p *= n
  return p


@dataclasses.dataclass
class TestCase:
  """Test out a solution with a known input/want."""
  inputs: str
  want: int
  part: int


class Challenge:
  """Daily Challenge."""

  SEP = '\n'
  TRANSFORM = str
  TESTS = ()
  DEBUG = False
  TEST_ARGS = []
  RUN_ARGS = []
  SLOW = False, False

  def __init__(self):
    self.funcs = {1: self.part1, 2: self.part2}
    super().__init__()

  @property
  def day(self):
    """Return the day of this class."""
    name = type(self).__name__
    assert name.startswith('Day')
    return int(name[3:])

  def part1(self, lines: List[str]) -> int:
    """Solve part 1."""
    raise NotImplementedError

  def part2(self, lines: List[str]) -> int:
    """Solve part 2."""
    raise NotImplementedError

  def load_data(self, src: str) -> List[str]:
    """Load exercise data."""
    if os.path.exists(src):
      text = pathlib.Path(src).read_text()
    else:
      text = src
    data = text.strip().split(self.SEP)
    return [self.TRANSFORM(i) for i in data]

  def run_tests(self):
    """Run the tests."""
    for i, case in enumerate(self.TESTS):
      self.debug(f'Running test {i + 1} (part{case.part})')
      data = self.load_data(case.inputs)
      got = self.funcs[case.part](data, *self.TEST_ARGS)
      if case.want != got:
        print(f'FAILED! {case.part}: want({case.want}) != got({got})')
        break
      self.debug('PASSED!')
    self.debug('=====')

  def debug(self, msg):
    """Maybe print a message."""
    if self.DEBUG:
      print(msg)

  def pre_run(self):
    """Hook to run things prior to tests and actual."""

  def run(self):
    """Run the tests then the problems."""
    run_solution = True
    run_timer = False

    if sys.argv[1].startswith('-'):
      mode = sys.argv.pop(1)
      if mode == '-r':
        run_solution, run_timer = True, False
      elif mode == '-v':
        run_solution, run_timer = False, False
      elif mode == '-t':
        run_solution, run_timer = False, True
      elif mode == '-b':
        run_solution, run_timer = True, True
      else:
        raise ValueError(f'Bad arg {mode}')

    self.pre_run()
    self.run_tests()

    if run_solution:
      data = self.load_data(sys.argv[1])
      for i, func in self.funcs.items():
        self.debug(f'Running part {i}:')
        print(func(data, *self.RUN_ARGS))
    if run_timer:
      self.time()

  def time_func(self, count: int, func: Callable) -> float:
    start = time.clock_gettime(time.CLOCK_MONOTONIC)
    for _ in range(count):
      func()
    end = time.clock_gettime(time.CLOCK_MONOTONIC)
    return end - start

  def time(self, count: int = None):
    """Benchmark the solution."""
    data = self.load_data(sys.argv[1])
    times = []

    for part, func in self.funcs.items():
      r = lambda: func(data, *self.RUN_ARGS)

      if count:
        _count = count
      elif self.SLOW[part - 1]:
        _count = 1
      else:
        t = self.time_func(1, r)
        _count = min(5000, max(1, int(10 / t)))

      t = self.time_func(_count, r)
      avg = 1000 * t / _count
      times.append(f'{avg:.4f}')

    print(f'{self.day}: ' + '/'.join(times) + ' ms')


# vim:ts=2:sw=2:expandtab

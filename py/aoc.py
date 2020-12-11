#!/bin/python

import dataclasses
import os
import pathlib
import sys
import time

from typing import Any, Callable, Dict, List, Optional


@dataclasses.dataclass
class TestCase:
  inputs: str
  want: int
  part: int


class Challenge:

  SEP = '\n'
  TRANSFORM = str
  TESTS = ()
  DEBUG = True
  TEST_ARGS = []
  RUN_ARGS = []

  def __init__(self):
    self.FUNCS = {1: self.part1, 2: self.part2}
    super().__init__()

  def part1(self, lines: List[str]) -> int:
    raise NotImplemented

  def part2(self, lines: List[str]) -> int:
    raise NotImplemented

  def load_data(self, src: str) -> List[str]:
    if os.path.exists(src):
      text = pathlib.Path(src).read_text()
    else:
      text = src
    data = text.strip().split(self.SEP)
    return [self.TRANSFORM(i) for i in data]

  def run_tests(self):
    """Run the tests."""
    for i, case in enumerate(self.TESTS):
      self.debug(f"Running test {i + 1} (part{case.part})")
      data = self.load_data(case.inputs)
      got = self.FUNCS[case.part](data, *self.TEST_ARGS)
      assert case.want == got, f'FAILED! want({case.want}) != got({got})'
      self.debug(f"PASSED!")
    self.debug('=====')

  def debug(self, s):
    """Maybe print a message."""
    if self.DEBUG:
      print(s)

  def pre_run(self):
    """Hook to run things prior to tests and actual."""
    pass

  def run(self):
    """Run the tests then the problems."""
    self.pre_run()
    self.run_tests()

    data = self.load_data(sys.argv[1])
    for i, func in self.FUNCS.items():
      self.debug(f"Running part {i}:")
      print(func(data, *self.RUN_ARGS))

  def time(self, count=None):
    data = self.load_data(sys.argv[1])
    for part, func in self.FUNCS.items():
      if count is None:
        # if self.DAY in (11,):
        # Really slow days. Do not run in a loop.
        #  _count = 1
        # else:
          # Time once to get count, aiming for 10s runtime.
        start = time.clock_gettime(time.CLOCK_MONOTONIC)
        func(data, *self.RUN_ARGS)
        end = time.clock_gettime(time.CLOCK_MONOTONIC)
        _count = max(1, int(10 / (end - start)))
      else:
        _count = count

      start = time.clock_gettime(time.CLOCK_MONOTONIC)
      for i in range(_count):
        func(data, *self.RUN_ARGS)
      end = time.clock_gettime(time.CLOCK_MONOTONIC)
      avg = (end - start) / _count
      if avg < 5:
        avg *= 1000
        print(f"Part {part}: {avg:.4f} ms")
      else:
        print(f"Part {part}: {avg:.4f} s")


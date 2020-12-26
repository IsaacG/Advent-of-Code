#!/bin/python
"""Advent of Code framework."""

import dataclasses
import os
import pathlib
import time

try:
  from . import site
  _SITE = True
except ImportError:
  _SITE = False

from typing import Callable, Iterable, List, Optional


def mult(nums: Iterable[int]) -> int:
  """Product of all values. Like sum() but with multiplication."""
  p = 1
  for n in nums:
    p *= n
  return p


def sum_map(lines: List[str], func: Callable[[str], int]) -> int:
  """sum_map(lines, func)"""
  return sum(func(line) for line in lines)


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
  TIMER_ITERATIONS = (None, None)

  def __init__(self):
    self.funcs = {1: self.part1, 2: self.part2}
    self.testing = False
    self._site = None
    super().__init__()

  def site(self):
    if self._site is None:
      self._site = site.Website(self.year, self.day)
    return self._site

  @property
  def data_file(self) -> pathlib.Path:
    return (self.data_dir / f'{self.day:02d}').with_suffix('.txt')

  @property
  def data_dir(self) -> pathlib.Path:
    for p in pathlib.Path(__file__).parents:
      d = p / 'data'
      if d.exists():
        return d
    return RuntimeError('No data dir found')

  @property
  def day(self) -> int:
    """Return the day of this class."""
    name = type(self).__name__
    assert name.startswith('Day')
    return int(name[3:])

  @property
  def year(self) -> int:
    """Return the year of this class."""
    p = pathlib.Path(__file__).parent.parent.name
    assert len(p) == 4 and p.isnumeric(), p
    return p

  def part1(self, lines: List[str]) -> int:
    """Solve part 1."""
    raise NotImplementedError

  def part2(self, lines: List[str]) -> int:
    """Solve part 2."""
    raise NotImplementedError

  def preparse_input(self, x):
    """Optional parser to parse data to send to the parts."""
    return x

  def load_data(self, src: Optional[str]) -> List[str]:
    """Load exercise data."""
    if src is None:
      src = self.data_file
    elif isinstance(src, str) and os.path.exists(src):
      src = pathlib.Path(src)

    if isinstance(src, pathlib.Path):
      if not src.exists():
        src.write_text(self.site().get_input())
      text = src.read_text()
    elif isinstance(src, str):
      text = src
    else:
      raise RuntimeError('Bad data source {src!r}')

    data = text.strip().split(self.SEP)
    return [self.TRANSFORM(i) for i in data]

  def run_tests(self):
    """Run the tests."""
    self.testing = True
    for i, case in enumerate(self.TESTS):
      self.debug(f'Running test {i + 1} (part{case.part})')
      assert isinstance(case.inputs, str), 'TestCase.inputs must be a string!'
      data = self.load_data(case.inputs)
      data = self.preparse_input(data)
      got = self.funcs[case.part](data, *self.TEST_ARGS)
      if case.want != got:
        print(f'FAILED! {case.part}: want({case.want}) != got({got})')
        break
      self.debug('PASSED!')
    self.debug('=====')
    self.testing = False

  def debug(self, msg):
    """Maybe print a message."""
    if self.DEBUG:
      print(msg)

  def pre_run(self):
    """Hook to run things prior to tests and actual."""

  def run(
    self,
    data: str = None,
    test: bool = False,
    solve: bool = False,
    submit: bool = False,
    check: bool = False,
    time: bool = False,
  ):
    assert any((test, solve, check, time))
    raw_data = self.load_data(data)

    self.pre_run()
    if test:
      self.run_tests()
      print(f'Day {self.day:02d}: TEST PASS')

    if solve:
      for i, func in self.funcs.items():
        parsed_data = self.preparse_input(raw_data)
        self.debug(f'Running part {i}:')
        try:
          print(func(parsed_data, *self.RUN_ARGS))
        except NotImplementedError:
          print(f'Part {i}: Not implemented')

    if submit:
      answer = None
      for i, func in self.funcs.items():
        parsed_data = self.preparse_input(raw_data)
        try:
          answer = func(parsed_data, *self.RUN_ARGS)
        except NotImplementedError:
          pass
      if answer is not None:
        self.site().submit(answer)

    if check:
      lines = (self.data_dir.parent / 'solutions').with_suffix('.txt').read_text().strip().split('\n')
      for line in lines:
        parts = line.split()
        assert len(parts) == 3, f'Line does not have 3 parts: {line!r}.'
        if int(parts[0]) == self.day:
          break
      for i, func in self.funcs.items():
        parsed_data = self.preparse_input(raw_data)
        got = func(parsed_data, *self.RUN_ARGS)
        want = parts[i]
        if isinstance(got, int):
          want = int(want)
        assert want == got, f'Day {self.day:02d} Part {i}: want({want}) != got({got})'
      print(f'Day {self.day:02d}: CHECK PASS')
    if time:
      self.time(raw_data)

  def time_func(self, count: int, func: Callable) -> float:
    start = time.clock_gettime(time.CLOCK_MONOTONIC)
    for _ in range(count):
      func()
    end = time.clock_gettime(time.CLOCK_MONOTONIC)
    return 1000 * (end - start) / count

  def time(self, raw_data):
    """Benchmark the solution."""
    times = []
    times.append(self.time_func(10000, lambda: self.preparse_input(raw_data)))
    parsed_data = self.preparse_input(raw_data)

    for part, func in self.funcs.items():
      r = lambda: func(parsed_data, *self.RUN_ARGS)

      if self.TIMER_ITERATIONS[part - 1]:
        _count = self.TIMER_ITERATIONS[part - 1]
      else:
        t = self.time_func(5, r) / 1000
        _count = min(10000, max(1, int(25 / t)))

      t = self.time_func(_count, r)
      times.append(t)

    print(f'{self.day}: ' + '/'.join(f'{t:.3f}' for t in times) + ' ms')


# vim:ts=2:sw=2:expandtab

#!/bin/python
"""Advent of Code framework."""

import dataclasses
import os
import pathlib
import time

from . import site
from typing import Any, Callable, Generator, Iterable, List, Optional


@dataclasses.dataclass
class TestCase:
  """Test out a solution with a known input/want."""
  inputs: str
  want: int
  part: int


class Helpers:

  _primes = [2, 3, 5]
  _gcd = {}

  def mult(self, nums: Iterable[int]) -> int:
    """Product of all values. Like sum() but with multiplication."""
    p = 1
    for n in nums:
      p *= n
    return p

  def sum_map(self, lines: List[str], func: Callable[[str], int]) -> int:
    """sum_map(lines, func)"""
    return sum(func(line) for line in lines)

  def primes(self) -> Generator[int, None, None]:
    s = 0
    for s in self._primes:
      yield s
    while True:
      s += 2
      if all(s % f for f in self._primes):
        self._primes.append(s)
        yield s

  def angle(self, c: complex) -> complex:
    return c / self.gcd(int(c.real), int(c.imag))

  def gcd(self, a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    if a > b:
      a, b = b, a
    if a == 0:
      return b if b else 1
    tple = (a, b)
    if tple not in self._gcd:
      gcd = 1
      p = 1
      pgen = self.primes()
      while p < a:
        p = next(pgen)
        while (a % p == 0 and b % p == 0):
          a //= p
          b //= p
          gcd *= p
      self._gcd[tple] = gcd
    return self._gcd[tple]


class Challenge(Helpers):
  """Daily Challenge."""

  SEP = '\n'
  TRANSFORM = str
  TESTS = ()
  DEBUG = False
  TIMER_ITERATIONS = (None, None)

  def __init__(self):
    self.funcs = {1: self.part1, 2: self.part2}
    self.testing = False
    self._site = None
    self._filecache = {}
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

  def raw_data(self, filename: Optional[str]) -> str:
    """Read puzzle data from file."""
    if filename not in self._filecache:
      if filename is None:
        path = self.data_file
      else:
        path = pathlib.Path(filename)

      if not path.exists():
        if filename:
          raise RuntimeError(f'Input file {filename} does not exist.')
        else:
          print(f'Input does not exist. Downloading.')
          path.write_text(self.site().get_input())

      self._filecache[filename] = path.read_text().strip()
    return self._filecache[filename]

  def parse_input(self, data: str) -> List[Any]:
    """Parse input data. Block of text -> lines -> TRANSFORM -> preparse_input."""
    data = data.strip().split(self.SEP)
    data = [self.TRANSFORM(i) for i in data]
    data = self.preparse_input(data)
    return data

  def run_tests(self):
    """Run the tests."""
    self.testing = True
    for i, case in enumerate(self.TESTS):
      self.debug(f'Running test {i + 1} (part{case.part})')
      assert isinstance(case.inputs, str), 'TestCase.inputs must be a string!'
      data = self.parse_input(case.inputs)
      got = self.funcs[case.part](data)
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
    assert any((test, solve, check, time, submit))

    self.pre_run()
    if test:
      self.run_tests()

    if solve:
      for i in (1, 2):
        puzzle_input = self.parse_input(self.raw_data(data))
        self.debug(f'Running part {i}:')
        try:
          print(self.funcs[i](puzzle_input))
        except NotImplementedError:
          print(f'Part {i}: Not implemented')

    if submit:
      answer = None
      for i in (1, 2):
        puzzle_input = self.parse_input(self.raw_data(data))
        try:
          a = self.funcs[i](puzzle_input)
          if a:
            answer = a
        except NotImplementedError:
          pass
      if not answer:
        print('Did not get an answer.')
      else:
        print('Submitting answer:', answer)
        print('Response:')
        print(self.site().submit(answer))

    if check:
      lines = (self.data_dir.parent / 'solutions').with_suffix('.txt').read_text().strip().split('\n')
      for line in lines:
        parts = line.split()
        assert len(parts) == 3, f'Line does not have 3 parts: {line!r}.'
        if int(parts[0]) == self.day:
          break
      for i in (1, 2):
        puzzle_input = self.parse_input(self.raw_data(data))
        got = self.funcs[i](puzzle_input)
        want = parts[i]
        if isinstance(got, int):
          want = int(want)
        if want == got:
          print(f'Day {self.day:02d} Part {i}: PASS!')
        else:
          print(f'Day {self.day:02d} Part {i}: want({want}) != got({got})')
    if time:
      puzzle_input = self.parse_input(self.raw_data(data))
      self.time(puzzle_input)

  def time_func(self, count: int, func: Callable) -> float:
    start = time.clock_gettime(time.CLOCK_MONOTONIC)
    for _ in range(count):
      func()
    end = time.clock_gettime(time.CLOCK_MONOTONIC)
    return 1000 * (end - start) / count

  def time(self, puzzle_input):
    """Benchmark the solution."""
    times = []
    times.append(self.time_func(10000, lambda: self.preparse_input(list(raw_data))))

    for part, func in self.funcs.items():
      r = lambda: func(puzzle_input)

      if self.TIMER_ITERATIONS[part - 1]:
        _count = self.TIMER_ITERATIONS[part - 1]
      else:
        t = self.time_func(5, r) / 1000
        _count = min(10000, max(1, int(25 / t)))

      t = self.time_func(_count, r)
      times.append(t)

    print(f'{self.day}: ' + '/'.join(f'{t:.3f}' for t in times) + ' ms')


# vim:ts=2:sw=2:expandtab

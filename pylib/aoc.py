#!/bin/python
"""Advent of Code framework.

TODO:
* prepare file needs to insert SAMPLES in the right place
* prepare file should run the day
* running the day:
  - watch the file and run tests, ignore NotImplemented
  - when a test transitions from failing to passing, submit one time (and only one time)
  - exit after both submits
"""

from __future__ import annotations

import dataclasses
import functools
import inspect
import pathlib
import time
from typing import Any, Callable, Generator, Iterable, List, Optional

from . import site


COLOR_SOLID = '█'
COLOR_EMPTY = ' '

TEST_SKIP = "__DO_NOT_RUN__"
# 4 cardinal directions
DIRECTIONS = [-1j ** i for i in range(4)]


def print_point_set(board: set[complex]) -> None:
    """Print out a set of points as a map."""
    min_x, max_x = int(min(p.real for p in board)), int(max(p.real for p in board))
    min_y, max_y = int(min(p.imag for p in board)), int(max(p.imag for p in board))
    for y in range(min_y, max_y+1):
        line = ""
        for x in range(min_x, max_x + 1):
            line += "#" if complex(x, y) in board else "."
        print(line)
    print()


class Board(dict):
    """A Board, represented as a set of complex points."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert all(isinstance(point, complex) for point in self.keys())

    @property
    def width(self):
        """Return the width of the board."""
        return int(max(point.real for point in self)) + 1

    @property
    def height(self):
        """Return the height of the board."""
        return int(max(point.imag for point in self)) + 1

    @property
    def max_point(self) -> complex:
        """Return the max point in the board."""
        return complex(self.width - 1, self.height - 1)

    def neighbors(self, point: complex, diagonal: bool) -> list[complex]:
        """Return the 4/8 neighbors of a point."""
        neighbors = []
        for i in range(4):
            if (candidate := point + -1j ** i) in self:
                neighbors.append(candidate)
        if diagonal:
            for i in range(4):
                if (candidate := point + (1 + 1j) * -1j ** i) in self:
                    neighbors.append(candidate)
        return neighbors

    @classmethod
    def from_block_map(cls, block: str, transform: Callable[[str], Any]) -> Board:
        """Return a Board from a block mapped with transform()."""
        raw_dict = {
            x + y * 1j: transform(val)
            for y, line in enumerate(block.splitlines())
            for x, val in enumerate(line)
        }
        return cls(raw_dict)

    @classmethod
    def from_int_block(cls, block: str) -> Board:
        """Return a Board from a block of ints."""
        return cls.from_block_map(block, int)


@dataclasses.dataclass(frozen=True)
class Point:
    """A cartesian point."""
    x: int
    y: int


@dataclasses.dataclass(frozen=True)
class Rect:
    """A rectangle formed between two cartesian points."""

    start: Point
    end: Point

    @classmethod
    def from_input(line: str) -> Rect:
        x1, y1, x2, y2 = (int(i) for i in re.findall(r"\d+", line))
        start = Point(min(x1, x2), min(y1, y2))
        end = Point(max(x1, x2), max(y1, y2))
        return Rect(start, end)

    def area(self) -> int:
        return abs(self.end.x - self.start.x + 1) * abs(self.end.y - self.start.y + 1)

    def overlap(self, other: Rect) -> Optional[Rect]:
        if other.end.x < self.start.x or other.end.y < self.start.y:
            return None
        if other.start.x > self.end.x or other.start.x > self.end.y:
            return None
        start = Point(max(self.start.x, other.start.x), max(self.start.y, other.start.y))
        end = Point(min(self.end.x, other.end.x), min(self.end.y, other.end.y))
        return Rect(start, end)


@dataclasses.dataclass(frozen=True)
class Line:
    """A line formed between two cartesian points."""
    start: Point
    end: Point

    def points(self) -> list[Point]:
        """Return the points on the line."""
        if (
            abs(self.start.x - self.end.x) != abs(self.start.y - self.end.y)  # 45 degrees
            and abs(self.start.x - self.end.x) != 0  # vertical
            and abs(self.start.y - self.end.y) != 0  # horizontal
        ):
            raise RuntimeError(f"{self} not 90 nor 45 degrees")

        if self.start == self.end:
            steps = 1
        elif abs(self.start.x - self.end.x) != 0:
            steps = abs(self.start.x - self.end.x)
        else:
            steps = abs(self.start.y - self.end.y)

        dir_x = (self.end.x - self.start.x) / steps
        dir_y = (self.end.y - self.start.y) / steps
        return [
            Point(self.start.x + dir_x * i, self.start.y + dir_y * i)
            for i in range(steps + 1)
        ]


def render(points: set[complex]) -> str:
    """Render a set of points to a string."""
    xs = int(max(p.real for p in points))
    ys = int(max(p.imag for p in points))

    rows = []
    for y in range(ys + 1):
        row = ''
        for x in range(xs + 1):
            if x + y * 1j in points:
                row += COLOR_SOLID
            else:
                row += COLOR_EMPTY
        rows.append(row)
    return "\n".join(rows)


@dataclasses.dataclass
class TestCase:
    """Test out a solution with a known input/want."""
    inputs: str
    want: str | int
    part: int


class Helpers:
    """A collection of helper functions."""

    _primes = [2, 3, 5]
    _gcd = {}

    @staticmethod
    def mult(nums: Iterable[int]) -> int:
        """Product of all values. Like sum() but with multiplication."""
        p = 1
        for n in nums:
            p *= n
        return p

    @staticmethod
    def sum_map(lines: List[str], func: Callable[[str], int]) -> int:
        """sum_map(lines, func)"""
        return sum(func(line) for line in lines)

    def primes(self) -> Generator[int, None, None]:
        """Yield primes without end."""
        s = 0
        for s in self._primes:
            yield s
        while True:
            s += 2
            for p in self._primes:
                if s % p == 0:
                    break
                if p * p > s:
                    self._primes.append(s)
                    yield s
                    break

    def angle(self, c: complex) -> complex:
        """Return the angle given by a complex number."""
        return c / self.gcd(int(c.real), int(c.imag))

    @staticmethod
    def sum_series(n: int) -> int:
        """Return the sum of the series [1..n]."""
        return n * (n + 1) // 2

    def gcd(self, a: int, b: int) -> int:
        """Return the GCD of two numbers."""
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

    INPUT_TYPES = str
    TRANSFORM = None
    TESTS: list[TestCase] = []
    DEBUG = False
    TIMER_ITERATIONS = (None, None)
    SUBMIT = {1: True, 2: True}

    def __init__(self):
        self.funcs = {1: self.part1, 2: self.part2}
        self.testing = False
        self._site = None
        self._filecache = {}
        super().__init__()

    @functools.cached_property
    def site(self) -> site.Website:
        """Return a cached Website object."""
        return site.Website(self.year, self.day)

    @property
    def data_file(self) -> pathlib.Path:
        """Return the path to today's data file."""
        return (self.data_dir / f'{self.day:02d}').with_suffix('.txt')

    @property
    def data_dir(self) -> pathlib.Path:
        """Return the directory named "data" with the inputs."""
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

    def part1(self, parsed_input: Any) -> int:
        """Solve part 1."""
        raise NotImplementedError

    def part2(self, parsed_input: Any) -> int:
        """Solve part 2."""
        raise NotImplementedError

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
                print('Input does not exist. Downloading.')
                path.write_text(self.site.get_input())

            self._filecache[filename] = path.read_text().rstrip()
        return self._filecache[filename]

    def input_parser(self, puzzle_input: str) -> Any:
        """Parse input data. Block of text -> output."""
        if self.TRANSFORM is not None:
            transform = self.TRANSFORM
        elif inspect.ismethod(getattr(self, "line_parser", None)):
            transform = self.line_parser
        elif not isinstance(self.INPUT_TYPES, list):
            transform = self.INPUT_TYPES
        else:

            def transform(line: str) -> list:
                parts = line.split(maxsplit=len(self.INPUT_TYPES) - 1)
                return [func(piece) for func, piece in zip(self.INPUT_TYPES, parts)]

        return [transform(i) for i in puzzle_input.splitlines()]

    def test(self, data=None):
        """Run the tests."""
        self.testing = True

        for i, case in enumerate(self.TESTS):
            if case.want == TEST_SKIP:
                continue
            self.debug(f'Running test {i + 1} (part{case.part})')
            assert isinstance(case.inputs, str), 'TestCase.inputs must be a string!'
            data = self.input_parser(case.inputs.rstrip())
            start = time.clock_gettime(time.CLOCK_MONOTONIC)
            got = self.funcs[case.part](data)
            end = time.clock_gettime(time.CLOCK_MONOTONIC)
            delta = int(1000 * (end - start))
            if case.want != got:
                print(f'FAILED! {case.part}: want({case.want}) != got({got})')
                break
            print(f'PASSED! Test #{i + 1} in {delta}ms')
        self.debug('=====')
        self.testing = False

    def debug(self, msg):
        """Maybe print a message."""
        if self.DEBUG:
            print(msg)

    def pre_run(self):
        """Hook to run things prior to tests and actual."""

    def solve(self, data=None) -> None:
        for i in (1, 2):
            puzzle_input = self.input_parser(self.raw_data(data))
            self.debug(f'Running part {i}:')
            try:
                print(self.funcs[i](puzzle_input))
            except NotImplementedError:
                print(f'Part {i}: Not implemented')

    def check(self, data=None) -> None:
        """Check the generated solutions match the contents of solutions.txt."""
        lines = (self.data_dir.parent / 'solutions').with_suffix('.txt').read_text().strip().split('\n')
        for line in lines:
            parts = line.split()
            assert len(parts) == 3, f'Line does not have 3 parts: {line!r}.'
            if int(parts[0]) == self.day:
                break
        for i in (1, 2):
            start = time.clock_gettime(time.CLOCK_MONOTONIC)
            puzzle_input = self.input_parser(self.raw_data(data))
            got = self.funcs[i](puzzle_input)
            end = time.clock_gettime(time.CLOCK_MONOTONIC)
            delta = int(1000 * (end - start))
            want = parts[i]
            if isinstance(got, int):
                want = int(want)
            if want == got:
                print(f'Day {self.day:02d} Part {i}: PASS in {delta}ms!')
            else:
                print(f'Day {self.day:02d} Part {i}: want({want}) != got({got})')

    def submit(self, data=None) -> None:
        """Generate a solution for the next unsolved part and submit it."""
        answers = []
        for i in (1, 2):
            puzzle_input = self.input_parser(self.raw_data(data))
            try:
                a = self.funcs[i](puzzle_input)
                if a:
                    answers.append(a)
            except NotImplementedError:
                pass
        if not answers:
            print('Did not get an answer.')
            return

        print(f'Generated answers {answers}; submitting part {len(answers)}.')
        response = self.site.submit(answers[-1])
        if response:
            print(f'Response: {response}')

    def get_run_method(self, **kwargs: bool) -> Callable[[Challenge, Optional[str]], None]:
        if sum(kwargs.values()) != 1:
            raise ValueError("Must specify exactly one action.")
        action = [k for k, v in kwargs.items() if v][0]
        return getattr(self, action)

    def run(
        self,
        data: str = None,
        test: bool = False,
        solve: bool = False,
        submit: bool = False,
        check: bool = False,
        benchmark: bool = False,
    ):
        """Run the challenges."""
        self.pre_run()
        f = self.get_run_method(test=test, solve=solve, submit=submit, check=check, benchmark=benchmark)
        f(data)

    def time_func(self, count: int, func: Callable) -> float:
        """Time a callable, averaged over count runs."""
        start = time.clock_gettime(time.CLOCK_MONOTONIC)
        for _ in range(count):
            func()
        end = time.clock_gettime(time.CLOCK_MONOTONIC)
        return 1000 * (end - start) / count

    def benchmark(self, data=None):
        """Benchmark the solution."""
        times = []
        times.append(self.time_func(10000, lambda: self.input_parser(self.raw_data(data))))

        for part, func in self.funcs.items():

            r = lambda: func(self.input_parser(self.raw_data(data)))

            if self.TIMER_ITERATIONS[part - 1]:
                _count = self.TIMER_ITERATIONS[part - 1]
            else:
                t = self.time_func(5, r) / 1000
                _count = min(10000, max(1, int(25 / t)))

            t = self.time_func(_count, r)
            times.append(t)

        print(f'{self.day}: ' + '/'.join(f'{t:.3f}' for t in times) + ' ms')


# vim:ts=4:sw=4:expandtab

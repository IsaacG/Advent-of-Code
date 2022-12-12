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
import re
import time
from typing import Any, Callable, Generator, Iterable, List, Optional

from .parsers import *
from . import site


COLOR_SOLID = '█'
COLOR_EMPTY = ' '

TEST_SKIP = "__DO_NOT_RUN__"
# 4 cardinal directions
FOUR_DIRECTIONS = [1j ** i for i in range(4)]
STRAIGHT_NEIGHBORS = FOUR_DIRECTIONS
DIAGONALS = [((1 + 1j) * -1j ** i) for i in range(4)]
EIGHT_DIRECTIONS = FOUR_DIRECTIONS + DIAGONALS
ALL_NEIGHBORS = EIGHT_DIRECTIONS

OCR_MAP = {
    # 2022/10: 6x5
    # From https://github.com/SizableShrimp/AdventOfCode2022/blob/main/src/util/java/me/sizableshrimp/adventofcode2022/helper/LetterParser.java
    # V, W, X not included
    0b01100_10010_10010_11110_10010_10010: "A",
    0b11100_10010_11100_10010_10010_11100: "B",
    0b01100_10010_10000_10000_10010_01100: "C",
    0b11100_10010_10010_10000_10010_11100: "D",
    0b11110_10000_11100_10000_10000_11110: "E",
    0b11110_10000_11100_10000_10000_10000: "F",
    0b01100_10010_10000_10110_10010_01110: "G",
    0b10010_10010_11110_10010_10010_10010: "H",
    0b11100_01000_01000_01000_01000_11100: "I",
    0b00110_00010_00010_00010_10010_01100: "J",
    0b10010_10100_11000_10100_10100_10010: "K",
    0b10000_10000_10000_10000_10000_11110: "L",
    0b10010_11110_11110_10010_10010_10010: "M",
    0b10010_11010_10110_10010_10010_10010: "N",
    0b01100_10010_10010_10010_10010_01100: "O",
    0b11100_10010_10010_11100_10000_10000: "P",
    0b01100_10010_10010_10010_10100_01010: "Q",
    0b11100_10010_10010_11100_10100_10010: "R",
    0b01110_10000_01100_00010_00010_11100: "S",
    0b11100_01000_01000_01000_01000_01000: "T",
    0b11111_00100_00100_00100_00100_00100: "T",
    0b10010_10010_10010_10010_10010_01100: "U",
    0b10001_10001_01010_00100_00100_00100: "Y",
    0b11110_00010_00100_01000_10000_11110: "Z",
    # 2018: 7x10 from https://github.com/mstksg/advent-of-code-ocr/blob/main/src/Advent/OCR/LetterMap.hs#L210
    0b0011000_0100100_1000010_1000010_1000010_1111110_1000010_1000010_1000010_1000010: "A",
    0b1111100_1000010_1000010_1000010_1111100_1000010_1000010_1000010_1000010_1111100: "B",
    0b0111100_1000010_1000000_1000000_1000000_1000000_1000000_1000000_1000010_0111100: "C",
    0b1111110_1000000_1000000_1000000_1111100_1000000_1000000_1000000_1000000_1111110: "E",
    0b1111110_1000000_1000000_1000000_1111100_1000000_1000000_1000000_1000000_1000000: "F",
    0b0111100_1000010_1000000_1000000_1000000_1001110_1000010_1000010_1000110_0111010: "G",
    0b1000010_1000010_1000010_1000010_1111110_1000010_1000010_1000010_1000010_1000010: "H",
    0b0001110_0000100_0000100_0000100_0000100_0000100_0000100_1000100_1000100_0111000: "J",
    0b1000010_1000100_1001000_1010000_1100000_1100000_1010000_1001000_1000100_1000010: "K",
    0b1000000_1000000_1000000_1000000_1000000_1000000_1000000_1000000_1000000_1111110: "L",
    0b1000010_1100010_1100010_1010010_1010010_1001010_1001010_1000110_1000110_1000010: "N",
    0b1111100_1000010_1000010_1000010_1111100_1000000_1000000_1000000_1000000_1000000: "P",
    0b1111100_1000010_1000010_1000010_1111100_1001000_1000100_1000100_1000010_1000010: "R",
    0b1000010_1000010_0100100_0100100_0011000_0011000_0100100_0100100_1000010_1000010: "X",
    0b1111110_0000010_0000010_0000100_0001000_0010000_0100000_1000000_1000000_1111110: "Z",
}


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


class OCR:
    """OCR helper for pixel displays."""

    def __init__(self, output: list[list[bool]]):
        self.output = output
        self.height = len(output)
        if self.height not in (6, 10):
            raise ValueError(f"Must have 6 or 10 rows; found {len(output)}")
        # 6x5 or 10x7
        self.width = {6: 5, 10: 7}[self.height]
        if any(len(l) != len(output[0]) for l in output):
            raise ValueError("Lines are not uniform size.")
        # Zero-pad rows if needed with a space.
        if len(output[0]) % self.width == self.width - 1:
            self.output = [row + [] for row in self.output]
        if len(output[0]) % self.width != 0:
            raise ValueError(f"Lines must be a multiple of {self.width} in length, got {len(output[0])}.")

    def as_string(self) -> str:
        """Return the OCR text."""
        chars = []
        for x in range(0, len(self.output[0]), self.width):
            num = 0
            alternative = 0
            for row in self.output:
                for byte in row[x:x + self.width]:
                    num = num << 1 | byte
                    alternative = alternative << 1 | (not byte)
            if num not in OCR_MAP:
                if alternative in OCR_MAP:
                    num = alternative
                else:
                    print(f"Unknown char: {bin(num)}")
            chars.append(OCR_MAP.get(num, "?"))
        if "?" in chars:
            self.render()
        return "".join(chars)

    def render(self) -> None:
        """Print the pixels to STDOUT."""
        pixel = {True: COLOR_SOLID, False: COLOR_EMPTY}
        for row in self.output:
            print("".join(pixel[i] for i in row))

    @classmethod
    def from_point_set(cls, points: set[complex]):
        """OCR from a set of points."""
        rows = point_set_to_lists(points)
        return cls(rows)


def point_set_to_lists(points: set[complex]) -> list[list[bool]]:
    """Convert a set of complex points to a 2D list of bools."""
    xs = int(max(p.real for p in points))
    ys = int(max(p.imag for p in points))

    rows = []
    for y in range(ys + 1):
        row = [x + y * 1j in points for x in range(xs + 1)]
        rows.append(row)
    return rows


class Board(dict):
    """A Board, represented as a set of complex points."""

    def __init__(self, *args, diagonal=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.diagonal = diagonal
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

    @property
    def corners(self) -> tuple[complex, complex, complex, complex]:
        return (
            0,
            complex(0, self.height - 1),
            complex(self.width - 1, 0),
            complex(self.width - 1, self.height - 1)
        )

    def neighbors(self, point: complex) -> dict[complex, Any]:
        """Return the 4/8 neighbors of a point."""
        neighbors = {}
        for i in range(4):
            if (candidate := point + -1j ** i) in self:
                neighbors[candidate] = self[candidate]
        if self.diagonal:
            for i in range(4):
                if (candidate := point + (1 + 1j) * -1j ** i) in self:
                    neighbors[candidate] = self[candidate]
        return neighbors

    def edges(self) -> set[complex]:
        """Return the edges of a fully populated board."""
        edges: set[complex] = set()
        cur = 0
        for direction in DIRECTIONS:
            while cur + direction in self:
                cur += direction
                edges.add(cur)
        return edges

    @classmethod
    def from_block_map(
        cls,
        block: str,
        transform: Callable[[str], Any],
        diagonal: bool = False,
    ) -> Board:
        """Return a Board from a block mapped with transform()."""
        raw_dict = {
            x + y * 1j: transform(val)
            for y, line in enumerate(block.splitlines())
            for x, val in enumerate(line)
        }
        return cls(raw_dict, diagonal=diagonal)

    @classmethod
    def from_int_block(cls, block: str, diagonal: bool = False) -> Board:
        """Return a Board from a block of ints."""
        return cls.from_block_map(block, int, diagonal)


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
    def from_input(cls, line: str) -> Rect:
        x1, y1, x2, y2 = (int(i) for i in re.findall(r"\d+", line))
        start = Point(min(x1, x2), min(y1, y2))
        end = Point(max(x1, x2), max(y1, y2))
        return cls(start, end)

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
    lines = point_set_to_lists(points)

    rows = []
    for line in lines:
        row = [COLOR_SOLID if i else COLOR_EMPTY for i in line]
        rows.append("".join(row))
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
    def cmp(a: float, b: float) -> int:
        """Compare two numbers like Perl <=>.

        Binary "<=>" returns -1, 0, or 1 depending on whether the left argument
        is numerically less than, equal to, or greater than the right argument.
        """
        if a < b:
            return -1
        if a > b:
            return +1
        return 0

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
    INPUT_PARSER: Optional[BaseParser] = None
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

    def part1(self, parsed_input: Any) -> int | str:
        """Solve part 1."""
        raise NotImplementedError

    def part2(self, parsed_input: Any) -> int | str:
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
        if self.INPUT_PARSER is not None:
            if inspect.isclass(self.INPUT_PARSER):
                raise ValueError(f"{self.INPUT_PARSER!r} is a class and not an instance!")
            return self.INPUT_PARSER.parse(puzzle_input)
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
                print(f'{self.year}/{self.day:02d} Part {i}: PASS in {delta}ms!')
            else:
                print(f'{self.year}/{self.day:02d} Part {i}: want({want}) != got({got})')

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

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

import contextlib
import dataclasses
import functools
import itertools
import pathlib
import re
import time
from typing import Any, Callable, Generator, Iterable, List, Optional

from .parsers import *
from . import parsers
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
RE_INT = re.compile(r"[+-]?\d+")

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


def format_ns(ns: float) -> str:
    units = [("ns", 1000), ("µs", 1000), ("ms", 1000), ("s", 60), ("mn", 60)]
    for unit, shift in units:
        if ns < shift:
            break
        ns /= shift
    else:
        unit = "hr"
    return f"{ns:>7.3f} {unit:>2}"


class OCR:
    """OCR helper for pixel displays."""

    def __init__(self, output: list[list[bool]]):
        self.output = output
        self.height = len(output)
        if self.height not in (6, 10):
            raise ValueError(f"Must have 6 or 10 rows; found {len(output)}")
        # 6x5 or 10x7
        self.width = {6: 5, 10: 7}[self.height]
        if any(len(line) != len(output[0]) for line in output):
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
        if len(rows) == 6 and len(rows[0]) % 5 == 4:
            rows = [row + [False] for row in rows]
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
        cur = complex(0, 0)
        for direction in FOUR_DIRECTIONS:
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
            x + y * 1j: transform(char)
            for y, line in enumerate(block.splitlines())
            for x, char in enumerate(line)
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

    def __complex__(self) -> complex:
        return complex(self.x, self.y)

    @classmethod
    def from_complex(cls, point: complex) -> Point:
        return cls(int(point.real), int(point.imag))


def n_dim_directions(dims: int, diagonal=False):
    """Return all the directions of a point for an n-dimensional point."""
    if diagonal:
        return [i for i in itertools.product([-1, 0, 1], repeat=dims) if sum(val == 0 for val in i) != dims]
    return [i for i in itertools.product([-1, 0, 1], repeat=dims) if sum(val == 0 for val in i) == dims - 1]


def n_dim_add(p1: tuple[int, ...], p2: tuple[int, ...]) -> tuple[int, ...]:
    """Add two n-dimensional points."""
    return tuple(a + b for a, b in zip(p1, p2, strict=True))


def n_dim_neighbors(point: tuple[int, ...], diagonal=False) -> set[tuple[int, ...]]:
    """Return all the neighbors of a point for an n-dimensional point."""
    return {n_dim_add(point, direction) for direction in n_dim_directions(len(point), diagonal)}


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
            Point(int(self.start.x + dir_x * i), int(self.start.y + dir_y * i))
            for i in range(steps + 1)
        ]

    @classmethod
    def from_complex(cls, start: complex, end: complex) -> Line:
        return cls(Point.from_complex(start), Point.from_complex(end))


def render(points: set[complex], off: str = COLOR_EMPTY, on: str = COLOR_SOLID) -> str:
    """Render a set of points to a string."""
    lines = point_set_to_lists(points)

    rows = []
    for line in lines:
        row = [on if i else off for i in line]
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
    _gcd: dict[tuple[int, int], int] = {}

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

    INPUT_PARSER: Optional[parsers.BaseParser] = None
    TESTS: list[TestCase] = []
    DEBUG = False
    TIMER_ITERATIONS = (None, None)
    SUBMIT = {1: True, 2: True}
    TIMEOUT: Optional[int] = None
    PARAMETERIZED_INPUTS: Any = None

    def __init__(self, parts_to_run: tuple[int, ...] = (1, 2)):
        if self.day == 25:
            parts_to_run = tuple(set(parts_to_run) - {2, })
        self.funcs = {1: self.part1, 2: self.part2}
        self.parts_to_run = parts_to_run
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
        raise RuntimeError('No data dir found')

    @property
    def day(self) -> int:
        """Return the day of this class."""
        name = type(self).__name__
        assert name.startswith('Day')
        return int(name[3:])

    @property
    def year(self) -> str:
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

    def solver(self, parsed_input: Any, *args, **kwargs) -> Any:
        raise NotImplementedError

    def input_parser(self, puzzle_input: str) -> Any:
        """Parse input data. Block of text -> output."""
        assert self.INPUT_PARSER is not None
        if not isinstance(self.INPUT_PARSER, BaseParser):
            raise ValueError(f"{self.INPUT_PARSER!r} is a class and not an instance!")

        return self.INPUT_PARSER.parse(puzzle_input)

    def run_solver(self, part: int, puzzle_input: str) -> Any:
        """Run a solver for one part."""
        func = {1: self.part1, 2: self.part2}
        parsed_input = self.input_parser(puzzle_input.rstrip())
        self.pre_run(parsed_input)
        if self.solver.__func__ is not Challenge.solver and self.PARAMETERIZED_INPUTS is not None:
            return self.solver(parsed_input, self.PARAMETERIZED_INPUTS[part - 1])
        if func[part].__func__ is getattr(Challenge, f"part{part}"):
            return None
        result = func[part](parsed_input)
        if isinstance(result, float):
            print("=== WARNING!! Casting float to int. ===")
            result = int(result)
        return result

    def test(self, input_file: Optional[str] = None) -> None:
        """Run the tests."""
        self.testing = True

        for i, case in enumerate(self.TESTS):
            if case.want == TEST_SKIP:
                continue
            if case.part not in self.parts_to_run:
                continue
            self.debug(f'Running test {i + 1} (part{case.part})')
            assert isinstance(case.inputs, str), 'TestCase.inputs must be a string!'
            start = time.perf_counter_ns()
            got = self.run_solver(case.part, case.inputs.rstrip())
            end = time.perf_counter_ns()
            if case.want != got:
                print(f'{self.year}/{self.day:02d} Test {i + 1}: FAILED! {case.part}: want({case.want}) != got({got})')
                break
            else:
                print(f'{self.year}/{self.day:02d} Test {i + 1}: PASS in {format_ns(end - start)}! (part {case.part})')
        self.debug('=====')
        self.testing = False

    def debug(self, msg):
        """Maybe print a message."""
        if self.DEBUG:
            print(msg)

    def pre_run(self, puzzle_input: Any) -> None:
        """Hook to run things prior to tests and actual."""

    def solve(self, input_file: Optional[str]) -> None:
        for part in self.parts_to_run:
            self.debug(f'Running part {part}:')
            try:
                got = self.run_solver(part, self.raw_data(input_file))
                print(got)
            except NotImplementedError:
                print(f'Part {part}: Not implemented')

    def check(self, input_file: Optional[str] = None) -> None:
        """Check the generated solutions match the contents of solutions.txt."""
        lines = (self.data_dir.parent / 'solutions').with_suffix('.txt').read_text().strip().split('\n')
        solution = None
        for line in lines:
            parts = line.split()
            assert len(parts) in {2, 3}, f'Line does not have 2-3 parts: {line!r}.'
            if int(parts[0]) == self.day:
                solution = parts[1:]
                break
        if not solution:
            print(f'{self.year}/{self.day:02d} No solution found!')
            return
        for part in self.parts_to_run:
            start = time.perf_counter_ns()
            got = self.run_solver(part, self.raw_data(input_file))
            end = time.perf_counter_ns()
            if part == 2 and len(solution) == 1:
                print("No part2 solution in solutions.txt; skipping.")
                return
            want = solution[part - 1]
            if isinstance(got, int):
                want = int(want)
            if want == got:
                print(f'{self.year}/{self.day:02d} Part {part}: PASS in {format_ns(end - start)}!')
            else:
                print(f'{self.year}/{self.day:02d} Part {part}: want({want}) != got({got})')

    def submit(self, input_file: Optional[str] = None) -> None:
        """Generate a solution for the next unsolved part and submit it."""
        answers = []
        for part in self.parts_to_run:
            try:
                got = self.run_solver(part, self.raw_data(input_file))
                if got:
                    answers.append(got)
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
        input_file: Optional[str] = None,
        test: bool = False,
        solve: bool = False,
        submit: bool = False,
        check: bool = False,
        benchmark: bool = False,
    ):
        """Run the challenges."""
        f = self.get_run_method(
            test=test,
            solve=solve,
            submit=submit,
            check=check,
            benchmark=benchmark,
        )
        f(input_file)

    def time_func(self, count: int, func: Callable) -> float:
        """Time a callable, averaged over count runs."""
        start = time.clock_gettime(time.CLOCK_MONOTONIC)
        for _ in range(count):
            func()
        end = time.clock_gettime(time.CLOCK_MONOTONIC)
        return 1000 * (end - start) / count

    def benchmark(self, puzzle_input: Any):
        """Benchmark the solution."""
        times = []
        times.append(self.time_func(10000, lambda: self.input_parser(self.raw_data(data))))

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

    @contextlib.contextmanager
    def context_timer(self, description: str) -> Generator[None, None, None]:
        start = time.perf_counter_ns()
        try:
            yield
        finally:
            end = time.perf_counter_ns()
            self.debug(f"{description}: {format_ns(end - start)}")


# vim:ts=4:sw=4:expandtab

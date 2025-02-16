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
import operator
import pathlib
import re
import time
from typing import Any, Callable, Generator, Iterable, Iterator, Optional, Sequence, TypeVar

from .helpers import *
from .parsers import *
from . import parsers
from . import site


TEST_SKIP = "__DO_NOT_RUN__"

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
    0b01110_10000_10000_01100_00010_11100: "S",
    0b01110_10000_01100_00010_00010_11100: "S",
    0b11100_01000_01000_01000_01000_01000: "T",
    0b11111_00100_00100_00100_00100_00100: "T",
    0b10010_10010_10010_10010_10010_01100: "U",
    0b10001_10001_01010_00100_00100_00100: "Y",
    0b11110_00010_00100_01000_10000_11110: "Z",
    # 2018: 6x8
    0b100010_100010_100010_111110_100010_100010_100010_100010: "H",
    0b111000_010000_010000_010000_010000_010000_010000_111000: "I",
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


def print_io(func):
    """Decorate a function to show the inputs and output."""

    def inner(*args):
        got = func(*args)
        if isinstance(args[0], aoc.Challenge):
            print(f"{type(args[0]).__name__}.{func.__name__}{args[1:]} => {got}")
        else:
            print(f"{func.__name__}{args} => {got}")
        return got

    return inner


def print_point_set(board: set[complex]) -> None:
    """Print out a set of points as a map."""
    min_x, min_y, max_x, max_y = bounding_coords(board)
    for y in range(min_y, max_y+1):
        line = ""
        for x in range(min_x, max_x + 1):
            line += "#" if complex(x, y) in board else "."
        print(line)
    print()


class CachedIterable(Iterable[T]):
    """Cached Iterable by phy1729."""

    def __init__(self, iterable: Iterable[T]) -> None:
        self._iter = iter(iterable)
        self._cache: list[T] = []

    def __iter__(self) -> Iterator[T]:
        yield from self._cache
        while True:
            val = next(self._iter)
            self._cache.append(val)
            yield val


class CachedIterator(Iterator[T]):
    """Cached Iterator by phy1729."""

    def __init__(self, parent: CachedIterable[T]) -> None:
        self._pos = 0
        self._parent = parent

    def __next__(self) -> T:
        if len(self._parent._cache) == self._pos:
            self._parent._cache.append(next(self._parent._iter))

        result = self._parent._cache[self._pos]
        self._pos += 1
        return result


class OCR:
    """OCR helper for pixel displays."""

    DIMS = {6: 5, 8: 6, 10: 7}

    def __init__(self, output: list[list[bool]], validate: bool = True):
        self.output = output
        self.height = len(output)
        if not validate:
            return
        if self.height not in (6, 8, 10):
            raise ValueError(f"Must have 6, 8, 10 rows; found {len(output)}")
        # 6x5 or 10x7
        self.width = self.DIMS[self.height]
        if any(len(line) != len(output[0]) for line in output):
            raise ValueError("Lines are not uniform size.")
        # Zero-pad rows if needed with a space.
        if len(output[0]) % self.width == self.width - 1:
            self.output = [row + [] for row in self.output]

    def blocks(self):
        transposed = zip(*self.output)
        while True:
            bits = []
            col = next(transposed, None)
            while col and not any(col):
                col = next(transposed, None)
            if col is None:
                return
            bits.append(col)
            try:
                while any(col):
                    col = next(transposed)
                    bits.append(col)
            except StopIteration:
                pass
            while len(bits) < self.width:
                bits.append([False] * self.height)
            combined = []
            for row in zip(*bits):
                combined.extend(row)
            yield combined

    def as_string(self) -> str:
        """Return the OCR text."""
        chars = []
        for block in self.blocks():
            num = 0
            alternative = 0
            for byte in block:
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

    def is_valid(self) -> bool:
        for block in self.blocks():
            num = 0
            alternative = 0
            for byte in block:
                num = num << 1 | byte
                alternative = alternative << 1 | (not byte)
            if num not in OCR_MAP and alternative not in OCR_MAP:
                return False
        return True

    def render(self) -> None:
        """Print the pixels to STDOUT."""
        pixel = {True: COLOR_SOLID, False: COLOR_EMPTY}
        for row in self.output:
            print("".join(pixel[i] for i in row))

    @classmethod
    def from_point_set(cls, points: set[complex]):
        """OCR from a set of points."""
        rows = point_set_to_lists(points)
        width = cls.DIMS[len(rows)]
        while len(rows[0]) % width:
            rows = [row + [False] for row in rows]
        return cls(rows)


def bounding_coords(points: Iterable[complex]) -> tuple[int, int, int, int]:
    """Return bounding min (x, y), max (x, y) for coordinates."""
    min_x = int(min(p.real for p in points))
    max_x = int(max(p.real for p in points))
    min_y = int(min(p.imag for p in points))
    max_y = int(max(p.imag for p in points))
    return min_x, min_y, max_x, max_y

def point_set_to_lists(points: set[complex]) -> list[list[bool]]:
    """Convert a set of complex points to a 2D list of bools."""
    min_x, min_y, max_x, max_y = bounding_coords(points)
    rows = []
    for y in range(min_y, max_y + 1):
        row = [x + y * 1j in points for x in range(min_x, max_x + 1)]
        rows.append(row)
    return rows


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


def sign(number: float) -> int:
    """Return the "sign" of a number, i.e. 1 or -1."""
    if number > 0:
        return 1
    if number < 0:
        return -1
    return 0


def cmp(a: float, b: float) -> int:
    """Compare two numbers like Perl <=>.

    Binary "<=>" returns -1, 0, or 1 depending on whether the left argument
    is numerically less than, equal to, or greater than the right argument.
    """
    return sign(a - b)



def reading_order(data: Sequence[complex]) -> list[complex]:
    return sorted(data, key=lambda x: (x.imag, x.real))


def floodfill(
    data: set[complex],
    start: complex,
    predicate: Callable[[complex, complex], bool],
    directions: list[complex] = FOUR_DIRECTIONS
) -> set[complex]:
    """Expand a point to its region by flood filling so long as the char matches."""
    todo = {start}
    region = set()
    while todo:
        cur = todo.pop()
        region.add(cur)
        todo.update(
            p for p in neighbors(cur, directions)
            if p in data and p not in region and predicate(cur, p)
        )
    return region


def partition_regions(
    data: set[complex],
    predicate: Callable[[complex, complex], bool],
    directions: list[complex] = FOUR_DIRECTIONS,
) -> list[set[complex]]:
    """Partition a map into regions."""
    regions = []
    todo = set(data)
    while todo:
        cur = todo.pop()
        region = floodfill(data, cur, predicate, directions)
        todo -= region
        regions.append(region)
    return regions


def interval_overlap(one: Interval, two: Interval) -> tuple[Interval | None, Interval | None, Interval | None]:
    one_start, one_end = one
    two_start, two_end = two
    if one_end < two_start or two_end < one_start:
        return None, None, None
    overlap_start, overlap_end = max(one_start, two_start), min(one_end, two_end)

    pre = (one_start, overlap_start - 1) if one_start < two_start else None
    post = (overlap_end + 1, one_end)  if one_end > two_end else None
    return pre, (overlap_start, overlap_end), post


@dataclasses.dataclass
class TestCase:
    """Test out a solution with a known input/want."""
    inputs: str
    want: str | int | None
    part: int


@dataclasses.dataclass(slots=True)
class Node:
    """Node in a double linked list."""
    val: Optional[int]
    prev: Optional[Node] = None
    next: Optional[Node] = None

    def __post_init__(self):
        """Update any neighboring nodes."""
        if self.next:
            self.next.prev = self
        if self.prev:
            self.prev.next = self


class LinkedList:
    """Double linked list."""

    first: Node
    last: Node
    len: int

    def __init__(self):
        """Create a double linked list."""
        self.head = Node(None)
        self.tail = Node(None, prev=self.head)
        self.nodes = []
        self.sealed = False

    def seal(self) -> None:
        """Convert the list to a circular list."""
        self.first = self.head.next
        self.last = self.tail.prev
        self.first.prev = self.last
        self.last.next = self.first
        self.len = len(self.nodes)
        self.sealed = True

    @classmethod
    def circular_list(cls, values: Iterable[int]) -> LinkedList:
        """Return a circular list from inputs."""
        nodelist = cls()
        for value in values:
            nodelist.add(value)
        nodelist.seal()
        return nodelist

    def add(self, val: int) -> None:
        """Insert a new value at the end of the list."""
        assert not self.sealed
        self.nodes.append(Node(val, prev=self.tail.prev, next=self.tail))

    def move_after(self, node: Node, insert_after: Node) -> None:
        """Move a node from its current location to the postion after insert_after."""
        if node == insert_after:
            return
        if node == insert_after.next:
            raise ValueError("node == insert_after")
        # Remove the node from the old location and close the gap.
        assert node.prev is not None
        assert node.next is not None
        node.prev.next, node.next.prev = node.next, node.prev
        # Insert between insert_after and insert_after.next
        node.prev, node.next = insert_after, insert_after.next
        assert node.prev is not None
        assert node.next is not None
        node.prev.next, node.next.prev = node, node


class Challenge:
    """Daily Challenge."""

    INPUT_PARSER: Optional[parsers.BaseParser] = None
    TESTS: list[TestCase] = []
    DEBUG = False
    TIMER_ITERATIONS = (None, None)
    SUBMIT = {1: True, 2: True}
    TIMEOUT: Optional[int] = None

    def __init__(self, parts_to_run: tuple[int, ...] = (1, 2)):
        if self.day == 25:
            parts_to_run = tuple(set(parts_to_run) - {2, })
        self.funcs = {1: self.part1, 2: self.part2}
        self.parts_to_run = parts_to_run
        self.testing = False
        self._site = None
        self._filecache: dict[pathlib.Path, str] = {}
        super().__init__()
        self.print_input_stats()

    @functools.cached_property
    def site(self) -> site.Website:
        """Return a cached Website object."""
        return site.Website(self.year, self.day)

    @property
    def data_file(self) -> pathlib.Path:
        """Return the path to today's data file."""
        return (self.data_dir / f'{self.year}.{self.day:02d}.txt')

    @property
    def data_dir(self) -> pathlib.Path:
        """Return the directory named "inputs" with the inputs."""
        for p in pathlib.Path(__file__).parents:
            d = p / 'inputs'
            if d.exists():
                return d
        raise RuntimeError('No data dir found')

    @property
    def solutions_file(self) -> pathlib.Path:
        """Return the path to today's data file."""
        return (self.solutions_dir / f'{self.year}.txt')

    @property
    def solutions_dir(self) -> pathlib.Path:
        """Return the directory named "solutions" with the solutions."""
        for p in pathlib.Path(__file__).parents:
            d = p / 'solutions'
            if d.exists():
                return d
        raise RuntimeError('No solution dir found')

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

    def print_input_stats(self):
        """Print some stats about the input."""

        def count(name: str, collection: list) -> None:
            self.debug(f"{name}: {len(collection)} ({len(set(collection))} unique)")

        # Line count, char count, uniq lines/chars. Min/max/count/unique ints.
        raw_data = self.raw_data(None)
        count("Lines", raw_data.splitlines())
        count("Words", raw_data.split())
        ints = [int(i) for i in RE_INT.findall(raw_data)]
        if ints:
            int_msg = f"Integers [({min(ints)})-({max(ints)})]"
            if len(int_msg) > 60:
                int_msg = int_msg[:50] + "...]"
            count(int_msg, ints)
        else:
            self.debug("No numbers.")

    def part1(self, puzzle_input: Any) -> int | str:
        """Solve part 1."""
        raise NotImplementedError

    def part2(self, puzzle_input: Any) -> int | str:
        """Solve part 2."""
        raise NotImplementedError

    def solver(self, puzzle_input: Any, part_one: bool) -> int | str:
        raise NotImplementedError

    def raw_data(self, filename: Optional[str]) -> str:
        """Read puzzle data from file."""
        path = pathlib.Path(filename) if filename else self.data_file
        if path not in self._filecache:
            if not path.exists():
                if filename:
                    raise RuntimeError(f'Input file {filename} does not exist.')
                print('Input does not exist. Downloading.')
                path.write_text(self.site.get_input())

            self._filecache[path] = path.read_text().rstrip()
        return self._filecache[path]

    @functools.cache
    def _parser(self) -> parsers.BaseParser:
        # print("Code defined" if self.INPUT_PARSER is not None else "Heuristic determined")
        if self.INPUT_PARSER is not None:
            if not isinstance(self.INPUT_PARSER, BaseParser):
                raise ValueError(f"{self.INPUT_PARSER!r} is a class and not an instance!")
            return self.INPUT_PARSER
        # Use heuristics to guess at an input parser.
        data = self.raw_data(None)
        lines = data.splitlines()
        multi_line = len(lines) > 1
        one_line = lines[0]

        if len(lines) > 5 and len(lines[0]) > 5 and len(lines) == len(lines[0]):
            return CoordinatesParser()
        pi = ParseIntergers(multi_line=multi_line)
        if pi.matches(data):
            return pi

        if len(RE_INT.findall(one_line)) > 1 and multi_line:
            lines = lines[:4]
            for char in "?()+*":
                lines = [l.replace(char, "\\" + char) for l in lines]
            lines = [re.sub("  +", " ", line) for line in lines]
            one_line = lines[0]
            template = re.compile(RE_INT.sub(lambda x: RE_INT.pattern, one_line))
            # print(template)
            if all(template.fullmatch(line) for line in lines):
                return parse_ints_per_line
        elif not multi_line and all(RE_INT.fullmatch(i) for i in one_line.split()):
            return parse_ints_one_line

        word_count = max(len(line.split()) for line in data.splitlines())
        if word_count == 1:
            return parse_one_str_per_line if multi_line else parse_one_str
        return parse_multi_str_per_line if multi_line else parse_one_str

    def input_parser(self, puzzle_input: str) -> Any:
        """Parse input data. Block of text -> output."""
        return self._parser().parse(puzzle_input)

    def run_solver(self, part: int, puzzle_input: str) -> Any:
        """Run a solver for one part."""
        func = {1: self.part1, 2: self.part2}
        parsed_input = self.input_parser(puzzle_input.rstrip())
        self.pre_run(parsed_input)
        try:
            return self.solver(parsed_input, part == 1)
        except NotImplementedError:
            pass
        try:
            result = func[part](parsed_input)
        except NotImplementedError:
            return None
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
            if len(case.inputs) <= 1:
                print('WARNING TestCase.inputs is less than two chars.')
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

    def tprint(self, *args):
        """Print a message but only for testing."""
        if self.testing and self.DEBUG:
            print(*args)

    def debug(self, *args):
        """Print a message if debug is enabled."""
        if self.DEBUG:
            print(*args)

    def pre_run(self, puzzle_input: Any) -> None:
        """Hook to run things prior to tests and actual."""

    def solve(self, input_file: Optional[str]) -> None:
        for part in self.parts_to_run:
            self.debug(f'Running part {part}:')
            try:
                start = time.perf_counter_ns()
                got = self.run_solver(part, self.raw_data(input_file))
                end = time.perf_counter_ns()
                print(f'{self.year}/{self.day:02d} Part {part}: GOT {got!r:20} {format_ns(end - start)}!')
            except NotImplementedError:
                print(f'Part {part}: Not implemented')

    def check(self, input_file: Optional[str] = None) -> None:
        """Check the generated solutions match the contents of solutions.txt."""
        lines = self.solutions_file.read_text().strip().split('\n')
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
            want: int | str = solution[part - 1]
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

    def get_run_method(self, **kwargs: bool) -> Callable[[Optional[str]], None]:
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
        times.append(self.time_func(10000, lambda: self.input_parser(self.raw_data(puzzle_input))))

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

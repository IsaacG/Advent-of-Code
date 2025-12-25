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
import logging
import operator
import pathlib
import re
import time
from typing import Any, Callable, Generator, Iterable, Iterator, Optional, Sequence, TypeVar

from .helpers import *
from .ocr import *
from .parsers import *
from . import parsers
from . import site


TEST_SKIP = "__DO_NOT_RUN__"

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

    def populate_cache(self, values: Iterable[T]) -> None:
        self._cache.extend(values)


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


def points_along_line(start_x: int, start_y: int, end_x: int, end_y: int) -> list[tuple[int, int]]:
    """Return the points on the line."""
    if (
        abs(start_x - end_x) != abs(start_y - end_y)  # 45 degrees
        and abs(start_x - end_x) != 0  # vertical
        and abs(start_y - end_y) != 0  # horizontal
    ):
        raise RuntimeError(f"Line not 90 nor 45 degrees")

    if start_x == end_x and start_y == end_y:
        steps = 1
    elif abs(start_x - end_x) != 0:
        steps = abs(start_x - end_x)
    else:
        steps = abs(start_y - end_y)

    dir_x = (end_x - start_x) / steps
    dir_y = (end_y - start_y) / steps
    return [
        (int(start_x + dir_x * i), int(start_y + dir_y * i))
        for i in range(steps + 1)
    ]


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
    data: set[T],
    start: T,
    predicate: Callable[[T, T], bool],
) -> set[T]:
    """Expand a point to its region by flood filling so long as the char matches."""
    adjacent = neighbors if isinstance(list(data)[0], complex) else t_neighbors4
    todo = {start}
    region = set()
    while todo:
        cur = todo.pop()
        region.add(cur)
        todo.update(
            p for p in adjacent(cur)  # type: ignore
            if p in data and p not in region and predicate(cur, p)  # type: ignore
        )
    return region


def partition_regions(
    data: set[T],
    predicate: Callable[[T, T], bool],
) -> list[set[T]]:
    """Partition a map into regions."""
    regions = []
    todo = set(data)
    while todo:
        cur = todo.pop()
        region = floodfill(data, cur, predicate)
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


class Challenge:
    """Daily Challenge."""

    INPUT_PARSER: Optional[parsers.BaseParser] = None
    TESTS: list[TestCase] = []
    SUBMIT = {1: True, 2: True}
    TIMEOUT: Optional[int] = None

    def __init__(self, year: int, day: int, parts_to_run: tuple[int, ...] = (1, 2)):
        self.year = year
        self.day = day
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

    def print_input_stats(self):
        """Print some stats about the input."""

        def count(name: str, collection: list) -> None:
            logging.info(f"{name}: {len(collection)} ({len(set(collection))} unique)")

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
            logging.info("No numbers.")

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

            self._filecache[path] = path.read_text().removesuffix("\n")
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
        got = self._guess_parser(data)
        # print("Guessing at parser", got)
        return got

    def _guess_parser(self, data: str) -> parsers.BaseParser:
        for i in range(5, 1, -1):
            sep = "\n" * i
            if sep in data:
                parsers = [self._guess_parser(chunk) for chunk in data.split(sep)]
                if len(parsers) > 5 and all(type(parser) == type(parsers[0]) for parser in parsers):
                    parsers = parsers[:1]
                return ParseBlocks(separator=sep, parsers=parsers)

        lines = data.splitlines()
        multi_line = len(lines) > 1
        one_line = lines[0]
        line_lengths = [len(line) for line in lines]

        check_lines = lines if len(lines) < 10 else lines[:-1]
        if len(lines) >= 5 and line_lengths[0] >= 5 and len(set(line_lengths)) == 1:
            return CoordinatesParser()
        pi = ParseIntergers(multi_line=multi_line)
        if pi.matches(data):
            return pi

        if all(i < 100 for i in line_lengths):
            pat = re.compile(r'\w+: \w+')
            if all(pat.fullmatch(line) for line in lines[:30]):
                return ParseDict(scalar=True, separator=": ")
            pat = re.compile(r'\w+:( \S+)+')
            if all(pat.fullmatch(line) for line in lines[:30]):
                return ParseDict(scalar=False, separator=": ")

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
        return parse_multi_mixed_per_line if multi_line else parse_one_str

    def input_parser(self, puzzle_input: str) -> Any:
        """Parse input data. Block of text -> output."""
        return get_parser(self.raw_data(None), self.INPUT_PARSER)(puzzle_input.rstrip("\n"))

    def run_solver(self, part: int, puzzle_input: str) -> Any:
        """Run a solver for one part."""
        func = {1: self.part1, 2: self.part2}
        parsed_input = self.input_parser(puzzle_input)
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
            if case.want == None:
                print(f'{self.year}/{self.day:02d} Test {i + 1}: wanted value not set!')
                continue
            if case.want == TEST_SKIP:
                continue
            if case.part not in self.parts_to_run:
                continue
            logging.info(f'Running test {i + 1} (part{case.part})')
            assert isinstance(case.inputs, str), 'TestCase.inputs must be a string!'
            if len(case.inputs) <= 1:
                print('WARNING TestCase.inputs is less than two chars.')
            start = time.perf_counter_ns()
            got = self.run_solver(case.part, case.inputs)
            end = time.perf_counter_ns()
            if case.want != got:
                print(f'{self.year}/{self.day:02d} Test {i + 1}: FAILED! {case.part}: want({case.want}) != got({got})')
                break
            else:
                print(f'{self.year}/{self.day:02d} Test {i + 1}: PASS in {format_ns(end - start)}! (part {case.part})')
        logging.info('=====')
        self.testing = False

    def solve(self, input_file: Optional[str]) -> None:
        for part in self.parts_to_run:
            logging.info(f'Running part {part}:')
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
    ):
        """Run the challenges."""
        f = self.get_run_method(
            test=test,
            solve=solve,
            submit=submit,
            check=check,
        )
        f(input_file)

# vim:ts=4:sw=4:expandtab

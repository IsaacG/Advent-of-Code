"""Helper code."""

import collections
import collections.abc
import dataclasses
import datetime
import inspect
import logging
import operator
import os
import re
import resource
import time
import typing

COLOR_SOLID = '█'
COLOR_EMPTY = ' '
T = typing.TypeVar("T")

# 4 cardinal directions
UP, DOWN, RIGHT, LEFT = complex(0, -1), complex(0, 1), complex(1), complex(-1)
FOUR_DIRECTIONS = [UP, DOWN, RIGHT, LEFT]
# UP, DOWN, RIGHT, LEFT = aoc.FOUR_DIRECTIONS
ARROW_DIRECTIONS = {"^": UP, "v": DOWN, ">": RIGHT, "<": LEFT}
LETTER_DIRECTIONS = {"U": UP, "D": DOWN, "R": RIGHT, "L": LEFT}
COMPASS_DIRECTIONS = {"S": -1j, "N": 1j, "E": 1, "W": -1}
STRAIGHT_NEIGHBORS = FOUR_DIRECTIONS
DIAGONALS = [((1 + 1j) * -1j ** i) for i in range(4)]
EIGHT_DIRECTIONS = FOUR_DIRECTIONS + DIAGONALS
ALL_NEIGHBORS = EIGHT_DIRECTIONS

HEX_AXIAL_DIRS_POINTY_TOP = {
  'e':  +1 +0j,
  'w':  -1 +0j,
  'ne': +1 +1j,
  'nw': +0 +1j,
  'se': +0 -1j,
  'sw': -1 -1j,
}

HEX_AXIAL_DIRS_FLAT_TOP = {
  'n':  +0 +1j,
  's':  +0 -1j,
  'ne': +1 +0j,
  'nw': -1 +1j,
  'se': +1 -1j,
  'sw': -1 +0j,
}

RE_INT = re.compile(r"[+-]?\d{1,1000}")
RE_BOUNDED_INT = re.compile(r"[+-]?\b\d+\b")
OPERATORS = {
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
    "=": operator.eq,
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
}
Interval = tuple[int, int]


class LogFormatter(logging.Formatter):
    """Custom log formatter to insert time deltas and part numbers."""
    def __init__(self, day: int = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_call = time.perf_counter_ns()
        self.day = day
        self.part = 0

    def set_part(self, part: int) -> None:
        """Set the part number."""
        self.part = part

    def format(self, record) -> str:
        """Format a log record, replacing DAYPART with the day.part."""
        msg = super().format(record)
        if "DAYPART" in msg and self.day and self.part:
            msg = msg.replace("DAYPART", f"{self.day}.{self.part}")
        return msg

    def formatTime(self, record, datefmt=None) -> str:
        """Format the time, including milliseconds since the last log call."""
        if datefmt:
            return super().formatTime(record, datefmt)
        call_time = time.perf_counter_ns()
        delta = call_time - self.last_call
        self.last_call = call_time
        return datetime.datetime.now().strftime(f"%H:%M:%S ({format_ns(delta)})")


def setup_logging(day: int, verbose: int) -> logging.Formatter:
    """Configure logging."""
    log_level = [logging.WARN, logging.INFO, logging.DEBUG][min(2, verbose)]
    handler = logging.StreamHandler()
    formatter = LogFormatter(day, fmt="%(asctime)s [DAYPART|%(funcName)s():L%(lineno)s] %(message)s")
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(log_level)
    return formatter

def setup_resources() -> None:
    """Configure resources to make runner play nicely."""
    os.nice(19)
    try:
        resource.setrlimit(resource.RLIMIT_RSS, (int(10e9), int(100e9)))
    except ValueError:
        pass


def format_ns(ns: float) -> str:
    """Convert nanosecond duration into human time."""
    units = [("ns", 1000), ("µs", 1000), ("ms", 1000), ("s", 60), ("mn", 60)]
    for unit, shift in units:
        if ns < shift:
            break
        ns /= shift
    else:
        unit = "hr"
    return f"{ns:>7.3f} {unit:>2}"


def timed(func: collections.abc.Callable[..., T], *args, **kwargs) -> tuple[str, T]:
    """Run a function. Return how long it took along with the result."""
    params = inspect.signature(func).parameters
    kwargs = {k: v for k, v in kwargs.items() if k in params}
    start = time.perf_counter_ns()
    got = func(*args, **kwargs)
    end = time.perf_counter_ns()
    return format_ns(end - start), got


def neighbors(point: complex, directions: collections.abc.Sequence[complex] = STRAIGHT_NEIGHBORS) -> collections.abc.Iterable[complex]:
    """Return the 4/8 neighbors of a point."""
    return (point + offset for offset in directions)


def t_neighbors4(point: collections.abc.Sequence[int]) -> collections.abc.Iterable[tuple[int, int]]:
    """Return the 4 neighbors of a point."""
    x, y = point
    yield x + 1, y
    yield x - 1, y
    yield x, y + 1
    yield x, y - 1


@dataclasses.dataclass
class Map:
    max_x: int
    max_y: int
    chars: dict[complex, str | int]
    coords: dict[str | int, set[complex]]
    all_coords: set[complex]
    blank_char: str
    non_blank_chars: set[str]

    def __post_init__(self) -> None:
        self.width = self.max_x + 1
        self.height = self.max_y + 1
        self.t_coords = {
            char: {(int(p.real), int(p.imag)) for p in points}
            for char, points in self.coords.items()
        }

    def __sub__(self, key: str) -> set[complex]:
        return self.all_coords - self[key]

    def __contains__(self, item) -> bool:
        if not isinstance(item, complex):
            raise TypeError(f"contains not defined for {type(item)}")
        return item in self.all_coords

    def __getitem__(self, key: str | complex) -> str | int | set[complex] | list[set[complex]]:
        if isinstance(key, complex):
            return self.chars[key]
        if isinstance(key, int):
            return self.coords[key]
        if isinstance(key, str) and len(key) == 1:
            return self.coords[key]
        if isinstance(key, collections.abc.Sequence):
            return [self.coords[k] for k in key]
        raise ValueError(f"Could not index on {key}")

    @property
    def size(self) -> int:
        if self.max_x != self.max_y:
            raise ValueError(f"The input is {self.width, self.height} and not square!")
        return self.width

    def get_coords(self, chars: collections.abc.Iterable[str]) -> list[set[complex]]:
        return [self.coords[char] for char in chars]

    @property
    def corners(self) -> tuple[complex, complex, complex, complex]:
        return (
            0,
            complex(0, self.max_y),
            complex(self.max_x, 0),
            complex(self.max_x, self.max_y)
        )

    def neighbors(self, point: complex, directions: collections.abc.Sequence[complex] = STRAIGHT_NEIGHBORS) -> dict[complex, T]:
        """Return neighboring points and values which are in the map."""
        return {n: self.chars[n] for n in neighbors(point, directions) if n in self.all_coords}


def render_char_map(chars: dict[complex, str], height: int, width: int) -> str:
    """Render the map as a string."""
    lines = []
    for y in range(height):
        line = []
        for x in range(width):
            line.append(chars.get(complex(x, y), " "))
        lines.append("".join(line))
    return "\n".join(lines)


def binary_search(low: int, high: int, predicate: collections.abc.Callable[[int], bool]) -> int:
    """Perform a binary search and return when the function matches.

    The predicate should return -1 for "lower", 0 for "match" and +1 for higher.
    """
    while low < high:
        cur = (high + low) // 2
        if predicate(cur):
            high = cur
        else:
            low = cur + 1
    return high

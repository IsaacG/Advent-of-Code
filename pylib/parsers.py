"""AoC Parser collection.

aoc.Challenge classes can define an INPUT_PARSER.
That value should be a BaseParser instance.
The Parser class shall have a `parse()` method which takes the puzzle input
and returns the parsed value.
"""

import collections
import collections.abc
import dataclasses
import inspect
import itertools
import re
from typing import Any, Callable, Iterable

from .helpers import *

RE_INT = re.compile(r"[+-]?\d{1,1000}")
RE_BOUNDED_INT = re.compile(r"[+-]?\b\d+\b")
RE_BOUNDED_INT_UNSIGNED = re.compile(r"\b\d+\b")
RE_INT_RANGES = re.compile(r"\d+(-\d+)+")
RE_POINT = re.compile(r"[+-]?\d+,[+-]?\d+")


def input_to_ints(inputs: Iterable[str]) -> list[int]:
    """Return a list of int values from an iterable."""
    return [int(i) for i in inputs]


def input_to_complex(inputs: Iterable[str]) -> list[complex]:
    """Return a list of complex values from an iterable."""
    out = []
    for pair in inputs:
        x, y = pair.split(",")
        out.append(complex(int(x), int(y)))
    return out


def input_to_strs(inputs: Iterable[str]) -> list[str]:
    """Return a list of str values from an iterable."""
    return [str(i) for i in inputs]


def input_to_auto(inputs: Iterable[str]) -> list[int] | list[str]:
    """Return a list of int or str values from an iterable."""
    if all(RE_INT.fullmatch(i) for i in inputs):
        return input_to_ints(inputs)
    return input_to_strs(inputs)


def value_to_mixed(input: str) -> int | str:
    return int(input) if RE_INT.fullmatch(input) else str(input)


def input_to_mixed(inputs: Iterable[str]) -> list[int | str]:
    """Return a list of int | str values from an iterable."""
    return [int(i) if RE_INT.fullmatch(i) else str(i) for i in inputs]


class BaseParser:
    """Base class for input parsing."""

    def parse(self, puzzle_input: str) -> Any:
        """Parse a puzzle input."""
        raise NotImplementedError

    def __call__(self, puzzle_input: str) -> Any:
        return self.parse(puzzle_input)


@dataclasses.dataclass
class ParseIntergers(BaseParser):
    """Get integers from input."""

    multi_line: bool | None = None

    def matches(self, puzzle_input) -> bool:
        """Check if the input is all numbers."""
        lines = puzzle_input.splitlines()
        trans = str.maketrans({i: "" for i in "-,;|"})
        if all(line.translate(trans).isdigit() for line in lines):
            return True
        if any(len(line) > 1000 for line in lines):
            return False
        patterns = [
            re.compile(r"[+-]?\d{1,1000}( +[+-]?\d{1,1000})*"),
        ]
        return any(
            all(pattern.fullmatch(line) for line in lines)
            for pattern in patterns
        )

    def parse(self, puzzle_input: str) -> int | list[int] | list[list[int]]:
        """Parse a puzzle input."""
        lines = puzzle_input.splitlines()
        regex = RE_BOUNDED_INT
        if all(RE_INT_RANGES.fullmatch(line) for line in lines):
            regex = RE_BOUNDED_INT_UNSIGNED
        numbers = [[int(num) for num in regex.findall(line)] for line in lines]
        numbers = [n for n in numbers if n]
        multi_line = len(numbers) > 1 if self.multi_line is None else self.multi_line
        multi_word = any(len(line) > 1 for line in numbers)
        if multi_line:
            if multi_word:
                return numbers
            return [words[0] for words in numbers]
        else:
            if multi_word:
                return numbers[0]
            else:
                return numbers[0][0]


@dataclasses.dataclass
class ParseOneWord(BaseParser):
    """Parse an input which is a single line with a single word."""

    input_type: Callable[[str], Any]

    def parse(self, puzzle_input: str) -> Any:
        """Parse puzzle input as a single object and convert to a type."""
        return self.input_type(puzzle_input)

@dataclasses.dataclass
class ParseMultiWords(BaseParser):
    """Parse an input which is a single line with multiple words."""

    input_type: Callable[[str], Any]
    separator: str | None = None

    def parse(self, puzzle_input: str) -> Any:
        """Parse puzzle input as a single object and convert to a type."""
        return [self.input_type(i) for i in puzzle_input.split(self.separator)]


@dataclasses.dataclass
class ParseOneWordPerLine(BaseParser):
    """Parse an input which is multiple lines with a single word per line."""

    input_type: Callable[[str], Any]

    def parse(self, puzzle_input: str) -> list[Any]:
        """Parse puzzle lines, converting each line to a type."""
        return [
            self.input_type(line)
            for line in puzzle_input.splitlines()
        ]


@dataclasses.dataclass
class BaseParseMultiPerLine(BaseParser):
    """Parse an input which is multiple lines with multiple words per line."""

    convert: Callable[[Iterable[str]], Any] = lambda x: x
    word_separator: str | None = None

    def parse(self, puzzle_input: str) -> list[list[Any]]:
        """Parse puzzle lines, converting each line to a list of types."""
        return [
            self.convert(line.split(self.word_separator))
            for line in puzzle_input.splitlines()
        ]


@dataclasses.dataclass
class BaseParseRe(BaseParser):
    """Parse multi-line input by applying a regex to find words on each line."""

    regex: str | re.Pattern
    convert: Callable[[Iterable[str]], list[Any]]
    one_line: bool = False

    def __post_init__(self) -> None:
        self.compiled = re.compile(self.regex) if isinstance(self.regex, str) else self.regex

    def parse(self, puzzle_input: str) -> list[list[Any]] | list[Any]:
        """Parse puzzle lines, applying a regex to each line."""
        data = [
            self.convert(self.line_to_iterable(line))
            for line in puzzle_input.splitlines()
        ]
        if self.one_line:
            if "\n" in puzzle_input:
                raise ValueError("Parser set to one line but input has multiple lines!")
            return data[0]
        return data

    def line_to_iterable(self, line: str) -> Iterable[str]:
        """Return an iterable of str for each line."""
        raise NotImplementedError


class BaseParseReFindall(BaseParseRe):
    """Parse an input by applying re.Pattern.findall to each line."""

    def line_to_iterable(self, line: str) -> Iterable[str]:
        """Return matches on a line via re.Pattern.findall."""
        return self.compiled.findall(line)


class BaseParseReGroups(BaseParseRe):
    """Parse an input by applying re.Pattern.groups to each line."""

    def line_to_iterable(self, line: str) -> Iterable[str]:
        """Return matches on a line via re.Pattern.match().groups."""
        if (match := self.compiled.match(line)):
            return match.groups()
        raise ValueError(f"Pattern did not match! {self.compiled.pattern=} {line=}")


@dataclasses.dataclass
class BaseMultiParser(BaseParser):
    """Base for using multiple parsers."""

    parsers: Iterable[BaseParser]

    def __post_init__(self) -> None:
        for parser in self.parsers:
            if inspect.isclass(parser):
                raise ValueError(f"{parser!r} is a class and not an instance!")


@dataclasses.dataclass
class ParseBlocks(BaseMultiParser):
    """Parse an input by splitting into blocks and applying a parser to each block."""

    parsers: Iterable[BaseParser]
    separator: str = "\n\n"

    def parse(self, puzzle_input: str) -> list[Any]:
        """Convert input into "blocks" and parse each block."""
        blocks = puzzle_input.split(self.separator)
        outputs = []
        for block, parser in zip(blocks, itertools.cycle(self.parsers)):
            outputs.append(parser.parse(block))
        return outputs


class ParseMultiple(BaseMultiParser):
    """Parse an input multiple ways."""

    def parse(self, puzzle_input: str) -> list[Any]:
        """Parse the input with each parser."""
        return [parser.parse(puzzle_input) for parser in self.parsers]


class ParseChain(BaseMultiParser):
    """Parse an input via a chain of serial parser steps."""

    def parse(self, puzzle_input: str) -> Any:
        """Convert input into "blocks" and parse each block."""
        parsed = puzzle_input
        for parser in self.parsers:
            parsed = parser.parse(parsed)
        return parsed


@dataclasses.dataclass
class Transform(BaseParser):
    """Apply an arbitrary transform to the data."""

    func: collections.abc.Callable

    def parse(self, puzzle_input: Any) -> Any:
        """Apply a transformation."""
        return self.func(puzzle_input)


@dataclasses.dataclass
class CoordinatesParserC(BaseParser):
    """Generate coordinate sets for multiple characters."""

    chars: collections.abc.Iterable[str] | None = None
    origin_top_left: bool = True
    ignore: str | None = None

    def parse(self, puzzle_input: str) -> MapC:
        """Parse a map and return the coordinates of different chars."""
        lines = puzzle_input.splitlines()

        if not self.origin_top_left:
            lines.reverse()

        x, y = (len(lines[0]), len(lines))

        all_chars = set(i for line in lines for i in line)
        want_chars = set(self.chars) if self.chars else all_chars
        if self.ignore:
            want_chars -= set(self.ignore)
        transform: Callable[[str], str | int]
        if all(i.isdigit() for i in all_chars):
            transform = int
        else:
            transform = str

        coords_by_char = collections.defaultdict(set)
        char_by_coord = {}
        all_coords = set()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char not in want_chars:
                    continue
                pos = complex(x, y)
                all_coords.add(pos)
                coords_by_char[transform(char)].add(pos)
                char_by_coord[pos] = transform(char)

        blank_char = max(coords_by_char, key=lambda x: len(coords_by_char[x]))
        non_blank_chars = set(coords_by_char) - {blank_char}

        return MapC(
            max_x=x,
            max_y=y,
            chars=char_by_coord,
            coords=dict(coords_by_char),
            all_coords=all_coords,
            blank_char=str(blank_char),
            non_blank_chars={str(i) for i in non_blank_chars},
        )


@dataclasses.dataclass
class CoordinatesParser(BaseParser):
    """Generate coordinate sets for multiple characters."""

    chars: collections.abc.Iterable[str] | None = None
    origin_top_left: bool = True
    ignore: str | None = None

    def parse(self, puzzle_input: str) -> Map:
        """Parse a map and return the coordinates of different chars."""
        lines = puzzle_input.splitlines()

        if not self.origin_top_left:
            lines.reverse()

        x, y = (len(lines[0]), len(lines))

        all_chars = set(i for line in lines for i in line)
        want_chars = set(self.chars) if self.chars else all_chars
        if self.ignore:
            want_chars -= set(self.ignore)
        transform: Callable[[str], str | int]
        if all(i.isdigit() for i in all_chars):
            transform = int
        else:
            transform = str

        coords_by_char = collections.defaultdict(set)
        char_by_coord = {}
        all_coords = set()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char not in want_chars:
                    continue
                pos = (x, y)
                all_coords.add(pos)
                coords_by_char[transform(char)].add(pos)
                char_by_coord[pos] = transform(char)

        blank_char = max(coords_by_char, key=lambda x: len(coords_by_char[x]))
        non_blank_chars = set(coords_by_char) - {blank_char}

        return Map(
            max_x=x,
            max_y=y,
            chars=char_by_coord,
            coords=dict(coords_by_char),
            all_coords=all_coords,
            blank_char=str(blank_char),
            non_blank_chars={str(i) for i in non_blank_chars},
        )


@dataclasses.dataclass
class ParseDict(BaseParser):
    """Parse an input into a dict by splitting on ': '."""

    scalar: bool
    separator: str = ": "

    def parse(self, puzzle_input: str) -> list[Any]:
        """Convert input into a dict or values."""
        blocks = puzzle_input.split(self.separator)
        outputs = {}
        for line in puzzle_input.splitlines():
            key_, val = line.split(self.separator, maxsplit=1)
            key = value_to_mixed(key_)
            if self.scalar:
                outputs[key] = value_to_mixed(val)
            else:
                outputs[key] = input_to_mixed(val.split())
        return outputs


# Convert the entire input into one str.
parse_one_str = ParseOneWord(str)
# Convert the entire input into one int.
parse_one_int = ParseOneWord(int)

# Convert the input into list[type], one per line.
parse_one_str_per_line = ParseOneWordPerLine(str)
parse_one_int_per_line = ParseOneWordPerLine(int)
parse_multi_str_one_line = ParseMultiWords(str)

# Convert the input into list[list[str]], splitting each line into multiple words.
parse_multi_str_per_line = BaseParseMultiPerLine(input_to_strs)
parse_re_group_str = lambda x: BaseParseReGroups(x, input_to_strs)
parse_re_findall_str = lambda x: BaseParseReFindall(x, input_to_strs)

# Convert the input into list[list[int]], splitting each line into multiple words.
parse_re_group_int = lambda x: BaseParseReGroups(x, input_to_ints)
parse_re_findall_int = lambda x: BaseParseReFindall(x, input_to_ints)
parse_ints_one_line = BaseParseReFindall(RE_INT, input_to_ints, one_line=True)
parse_ints_per_line = BaseParseReFindall(RE_INT, input_to_ints, one_line=False)
parse_ints = parse_ints_per_line

# Convert the input into list[list[int | str]], splitting each line into multiple words.
parse_multi_mixed_per_line = BaseParseMultiPerLine(input_to_mixed)
parse_re_group_mixed = lambda x: BaseParseReGroups(x, input_to_mixed)
parse_re_findall_mixed = lambda x: BaseParseReFindall(x, input_to_mixed)
parse_re_findall_points = BaseParseReFindall(RE_POINT, input_to_complex)

parse_multiple_words_per_line = BaseParseMultiPerLine(input_to_auto)

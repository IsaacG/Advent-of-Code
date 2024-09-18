"""AoC Parser collection.

aoc.Challenge classes can define an INPUT_PARSER.
That value should be a BaseParser instance.
The Parser class shall have a `parse()` method which takes the puzzle input
and returns the parsed value.
"""

import collections.abc
import dataclasses
import inspect
import itertools
import re
from typing import Any, Callable, Iterable

RE_INT = re.compile(r"[+-]?\d+")
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


def input_to_mixed(inputs: Iterable[str]) -> list[int | str]:
    """Return a list of int | str values from an iterable."""
    return [int(i) if RE_INT.fullmatch(i) else str(i) for i in inputs]


class BaseParser:
    """Base class for input parsing."""

    def parse(self, puzzle_input: str) -> Any:
        """Parse a puzzle input."""
        raise NotImplementedError


@dataclasses.dataclass
class ParseOneWord(BaseParser):
    """Parse an input which is a single line with a single word."""

    input_type: Callable[[str], Any]

    def parse(self, puzzle_input: str) -> Any:
        """Parse puzzle input as a single object and convert to a type."""
        return self.input_type(puzzle_input)


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

    convert: Callable[[Iterable[str]], Any]

    def parse(self, puzzle_input: str) -> list[list[Any]]:
        """Parse puzzle lines, converting each line to a list of types."""
        return [
            self.convert(line.split())
            for line in puzzle_input.splitlines()
        ]


@dataclasses.dataclass
class BaseParseRe(BaseParser):
    """Parse multi-line input by applying a regex to find words on each line."""

    regex: str
    convert: Callable[[Iterable[str]], list[Any]]
    one_line: bool = False

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

    def parse(self, puzzle_input: str) -> list[Any]:
        """Convert input into "blocks" and parse each block."""
        parsed = puzzle_input
        for parser in self.parsers:
            parsed = parser.parse(parsed)
        return parsed


@dataclasses.dataclass
class ParseCharMap(BaseParser):
    """Parse a map of values, generating a set[complex]."""

    transform: Callable[[str], Any]

    def parse(self, puzzle_input: str) -> dict[complex, Any]:
        """Parse a map."""
        out: dict[complex, Any] = {}
        for y, line in enumerate(puzzle_input.splitlines()):
            for x, char in enumerate(line):
                if (val := self.transform(char)) is not None:
                    out[complex(x, y)] = val
        return out


@dataclasses.dataclass
class Transform(BaseParser):
    """Apply an arbitrary transform to the data."""

    func: collections.abc.Callable

    def parse(self, puzzle_input: Any) -> Any:
        """Apply a transformation."""
        return self.func(puzzle_input)


@dataclasses.dataclass
class AsciiBoolMapParser(BaseParser):
    """Parse a map of on/off values to build a set of "on" points."""

    on_chars: str
    origin_top_left: bool = True

    def parse(self, puzzle_input: str) -> set[complex]:
        """Parse ASCII to find points in a map which are "on"."""
        lines = puzzle_input.splitlines()
        if not self.origin_top_left:
            lines.reverse()
        return {
            complex(x, y)
            for y, line in enumerate(lines)
            for x, char in enumerate(line)
            if char in self.on_chars
        }


@dataclasses.dataclass
class CharCoordinatesParser(BaseParser):
    """Generate coordinate sets for multiple characters."""

    chars: collections.abc.Iterable[str]

    def parse(self, puzzle_input: str) -> tuple[tuple[int, int], set[complex], ...]:
        """Parse a map and return the coordinates of different chars."""
        lines = puzzle_input.splitlines()
        size = (len(lines[0]), len(lines))
        maps = (
            {
                complex(x, y)
                for y, line in enumerate(lines)
                for x, got in enumerate(line)
                if got == want
            }
            for want in self.chars
        )
        return (size, *maps)


# Convert the entire input into one str.
parse_one_str = ParseOneWord(str)
# Convert the entire input into one int.
parse_one_int = ParseOneWord(int)

# Convert the input into list[type], one per line.
parse_one_str_per_line = ParseOneWordPerLine(str)
parse_one_int_per_line = ParseOneWordPerLine(int)

# Convert the input into list[list[str]], splitting each line into multiple words.
parse_multi_str_per_line = BaseParseMultiPerLine(input_to_strs)
parse_re_group_str = lambda x: BaseParseReGroups(x, input_to_strs)
parse_re_findall_str = lambda x: BaseParseReFindall(x, input_to_strs)

# Convert the input into list[list[int]], splitting each line into multiple words.
parse_multi_int_per_line = BaseParseMultiPerLine(input_to_ints)
parse_re_group_int = lambda x: BaseParseReGroups(x, input_to_ints)
parse_re_findall_int = lambda x: BaseParseReFindall(x, input_to_ints)
parse_ints = BaseParseReFindall(RE_INT, input_to_ints)
parse_ints_one_line = BaseParseReFindall(RE_INT, input_to_ints, one_line=True)
parse_ints_per_line = BaseParseReFindall(RE_INT, input_to_ints, one_line=False)

# Convert the input into list[list[int | str]], splitting each line into multiple words.
parse_multi_mixed_per_line = BaseParseMultiPerLine(input_to_mixed)
parse_re_group_mixed = lambda x: BaseParseReGroups(x, input_to_mixed)
parse_re_findall_mixed = lambda x: BaseParseReFindall(x, input_to_mixed)
parse_re_findall_points = BaseParseReFindall(RE_POINT, input_to_complex)

char_map = ParseCharMap(str)
int_map = ParseCharMap(int)

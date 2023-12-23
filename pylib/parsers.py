"""AoC Parser collection.

aoc.Challenge classes can define an INPUT_PARSER.
That value should be a BaseParser instance.
The Parser class shall have a `parse()` method which takes the puzzle input
and returns the parsed value.
"""

import collections.abc
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
    return [int(i) if i.isdigit() else str(i) for i in inputs]


class BaseParser:
    """Base class for input parsing."""

    def parse(self, puzzle_input: str) -> Any:
        """Parse a puzzle input."""
        raise NotImplementedError


class ParseOneWord(BaseParser):
    """Parse an input which is a single line with a single word."""

    def __init__(self, input_type: Callable[[str], Any]):
        self.input_type = input_type

    def parse(self, puzzle_input: str) -> Any:
        """Parse puzzle input as a single object and convert to a type."""
        return self.input_type(puzzle_input)


class ParseOneWordPerLine(BaseParser):
    """Parse an input which is multiple lines with a single word per line."""

    def __init__(self, input_type: Callable[[str], Any]):
        self.input_type = input_type

    def parse(self, puzzle_input: str) -> list[Any]:
        """Parse puzzle lines, converting each line to a type."""
        return [
            self.input_type(line)
            for line in puzzle_input.splitlines()
        ]


class BaseParseMultiPerLine(BaseParser):
    """Parse an input which is multiple lines with multiple words per line."""

    def __init__(self, convert: Callable[[Iterable[str]], Any]):
        self.convert = convert

    def parse(self, puzzle_input: str) -> list[list[Any]]:
        """Parse puzzle lines, converting each line to a list of types."""
        return [
            self.convert(line.split())
            for line in puzzle_input.splitlines()
        ]


class BaseParseRe(BaseParser):
    """Parse multi-line input by applying a regex to find words on each line."""

    def __init__(self, regex: str, convert: Callable[[Iterable[str]], list[Any]]):
        self.compiled = re.compile(regex)
        self.convert = convert

    def parse(self, puzzle_input: str) -> list[list[Any]]:
        """Parse puzzle lines, applying a regex to each line."""
        return [
            self.convert(self.line_to_iterable(line))
            for line in puzzle_input.splitlines()
        ]

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


class BaseMultiParser(BaseParser):
    """Base for using multiple parsers."""

    def __init__(self, parsers: Iterable[BaseParser]):
        for parser in parsers:
            if inspect.isclass(parser):
                raise ValueError(f"{parser!r} is a class and not an instance!")
        self.parsers = parsers


class ParseBlocks(BaseMultiParser):
    """Parse an input by splitting into blocks and applying a parser to each block."""

    def __init__(self, parsers: Iterable[BaseParser], separator: str = "\n\n"):
        super().__init__(parsers)
        self.separator = separator

    def parse(self, puzzle_input: str) -> list[Any]:
        """Convert input into "blocks" and parse each block."""
        blocks = puzzle_input.split(self.separator)
        outputs = []
        for block, parser in zip(blocks, itertools.cycle(self.parsers)):
            outputs.append(parser.parse(block))
        return outputs


class ParseChain(BaseMultiParser):
    """Parse an input via a chain of serial parser steps."""

    def parse(self, puzzle_input: str) -> list[Any]:
        """Convert input into "blocks" and parse each block."""
        parsed = puzzle_input
        for parser in self.parsers:
            parsed = parser.parse(parsed)
        return parsed


class ParseCharMap(BaseParser):
    """Parse a map of values, generating a set[complex]."""

    def __init__(self, transform: Callable[[str], Any]):
        self.transform = transform

    def parse(self, puzzle_input: str) -> dict[complex, Any]:
        """Parse a map."""
        out: dict[complex, Any] = {}
        for y, line in enumerate(puzzle_input.splitlines()):
            for x, char in enumerate(line):
                if (val := self.transform(char)) is not None:
                    out[complex(x, y)] = val
        return out


class Transform(BaseParser):
    """Apply an arbitrary transform to the data."""

    def __init__(self, func: collections.abc.Callable):
        self.func = func

    def parse(self, puzzle_input: Any) -> Any:
        """Apply a transformation."""
        return self.func(puzzle_input)


class AsciiBoolMapParser(BaseParser):
    """Parse a map of on/off values to build a set of "on" points."""

    def __init__(self, on_chars: str):
        self.on_chars = on_chars

    def parse(self, puzzle_input: str) -> set[complex]:
        """Parse ASCII to find points in a map which are "on"."""
        return {
            complex(x, y)
            for y, line in enumerate(puzzle_input.splitlines())
            for x, char in enumerate(line)
            if char in self.on_chars
        }


class CharCoordinatesParser(BaseParser):
    """Generate coordinate sets for multiple characters."""

    def __init__(self, chars: collections.abc.Iterable[str]):
        self.chars = chars

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

# Convert the input into list[list[int | str]], splitting each line into multiple words.
parse_multi_mixed_per_line = BaseParseMultiPerLine(input_to_mixed)
parse_re_group_mixed = lambda x: BaseParseReGroups(x, input_to_mixed)
parse_re_findall_mixed = lambda x: BaseParseReFindall(x, input_to_mixed)
parse_re_findall_points = BaseParseReFindall(RE_POINT, input_to_complex)

parse_ascii_bool_map = AsciiBoolMapParser
parse_ascii_char_map = ParseCharMap
char_map = ParseCharMap(str)

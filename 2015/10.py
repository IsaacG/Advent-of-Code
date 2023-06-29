#!/bin/python
"""Advent of Code: Day 10."""

import functools

from lib import aoc

SAMPLE = "1"

InputType = str


@functools.cache
def look_say(string: str) -> str:
    """Return a look-say version of a string."""
    str_len = len(string)
    # Reduce large inputs to take advantage of caching.
    # Find a split point between differing chars.
    if str_len > 15:
        split = str_len // 2
        while split > 3:
            if string[split - 1] == string[split]:
                split -= 1
            else:
                return look_say(string[:split]) + look_say(string[split:])

    out = []
    count = 0
    prior = string[0]
    for char in string:
        if char == prior:
            count += 1
        else:
            out.extend((str(count), prior))
            prior = char
            count = 1
    out.extend((str(count), prior))
    return "".join(out)


class Day10(aoc.Challenge):
    """Day 10: Elves Look, Elves Say. Run a look-say algorithm."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=6),
        aoc.TestCase(inputs=SAMPLE, part=2, want=6),
    ]
    INPUT_PARSER = aoc.parse_one_str
    TIMEOUT = 70

    def look_say_loop(self, string: str, steps: int) -> str:
        """Return look-say length after looping."""
        for _ in range(5 if self.testing else steps):
            string = look_say(string)
        return len(string)

    def part1(self, parsed_input: InputType) -> int:
        """Look-say, 40 iterations."""
        return self.look_say_loop(parsed_input, 40)

    def part2(self, parsed_input: InputType) -> int:
        """Look-say, 50 iterations."""
        return self.look_say_loop(parsed_input, 50)

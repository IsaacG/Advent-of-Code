#!/bin/python
"""Advent of Code: Day 08."""

import collections

from lib import aoc

# A list of lines.
# Each line is split into a tuple (data, output).
# Each data, output is a list of wires, each a set[str].
InputType = list[tuple[list[frozenset[str]], list[frozenset[str]]]]

SAMPLE = """\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


class Day08(aoc.Challenge):
    """Debug a seven segment display, based on which wires are on."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=26),
        aoc.TestCase(inputs=SAMPLE, part=2, want=61229),
    )

    def part1(self, parsed_input: InputType) -> int:
        """Count the number of 1, 4, 7, 8's in the output."""
        want_lengths = {2, 3, 4, 7}
        return sum(
            # Count occurances...
            1
            # ...for all wires in the digits...
            for _, digits in parsed_input for wires in digits
            # ...where the right number of wires are on.
            if len(wires) in want_lengths
        )

    @staticmethod
    def decipher(values: list[set[str]]) -> dict[frozenset, int]:
        """Build a map of wires -> value from inputs."""
        known = {}
        # Sort wires by length.
        inputs_by_size = collections.defaultdict(list)
        for wires in values:
            inputs_by_size[len(wires)].append(wires)

        # First map wires based on the number of wires.
        by_size = {2: 1, 3: 7, 4: 4, 7: 8}
        for size, val in by_size.items():
            known[val] = inputs_by_size[size][0]

        # Next handles length 6 wires.
        for wires in inputs_by_size[6]:
            if wires.issuperset(known[4]):
                known[9] = wires
            elif wires.issuperset(known[1]):
                known[0] = wires
            else:
                known[6] = wires

        # Next handles length 5 wires (this should be all of them).
        for wires in inputs_by_size[5]:
            if wires.issuperset(known[1]):
                known[3] = wires
            elif wires.issubset(known[6]):
                known[5] = wires
            else:
                known[2] = wires

        # If only 9 are found, we could infer the 10th by omission.
        # Not needed here, though.
        assert len(known) == 10, f"{len(known)} {sorted(known)}"

        return known

    def part2(self, parsed_input: InputType) -> int:
        """Decipher each output digits based on the sample digits."""
        sum_result = 0
        for samples, digits in parsed_input:
            wires_to_str = {
                wires: str(value)
                for value, wires in self.decipher(samples).items()
            }
            display = "".join(wires_to_str[wires] for wires in digits)
            sum_result += int(display)

        return sum_result

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return [
            tuple(
                [frozenset(wires) for wires in section.split()]
                for section in line.split(" | ")
            )
            for line in puzzle_input.splitlines()
        ]

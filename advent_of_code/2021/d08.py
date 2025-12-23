#!/bin/python
"""Advent of Code: Day 08. Debug a seven segment display, based on which wires are on."""

import collections

# A list of lines.
# Each line is split into a tuple (data, output).
# Each data, output is a list of wires, each a set[str].
InputType = list[tuple[list[frozenset[str]], ...]]


def decipher(values: list[frozenset[str]]) -> dict[int, frozenset[str]]:
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


def solve(data: InputType, part: int) -> int:
    """Analyze wires."""
    return (part1 if part == 1 else part2)(data)


def part1(data: InputType) -> int:
    """Count the number of 1, 4, 7, 8's in the output."""
    want_lengths = {2, 3, 4, 7}
    # Count occurances of wires where the correct number of wires is on.
    return sum(
        len(wires) in want_lengths
        for _, digits in data for wires in digits
    )


def part2(data: InputType) -> int:
    """Decipher each output digits based on the sample digits."""
    sum_result = 0
    for samples, digits in data:
        wires_to_str = {
            wires: str(value)
            for value, wires in decipher(samples).items()
        }
        display = "".join(wires_to_str[wires] for wires in digits)
        sum_result += int(display)

    return sum_result


def input_parser(data: str) -> InputType:
    """Parse the input data."""
    return [
        tuple(
            [frozenset(wires) for wires in section.split()]
            for section in line.split(" | ")
        )
        for line in data.splitlines()
    ]


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
TESTS = [(1, SAMPLE, 26), (2, SAMPLE, 61229)]

#!/bin/python
"""Advent of Code, Day 16: Flawed Frequency Transmission."""
from lib import aoc


class Day16(aoc.Challenge):
    """Day 16: Flawed Frequency Transmission."""

    TESTS = [
        aoc.TestCase(inputs="80871224585914546619083218645595", part=1, want=24176176),
        aoc.TestCase(inputs="19617804207202209144916044189917", part=1, want=73745418),
        aoc.TestCase(inputs="69317163492948606335995924319873", part=1, want=52432133),
        aoc.TestCase(inputs="03036732577212944063491565474664", part=2, want=84462026),
        aoc.TestCase(inputs="02935109699940807407585447034323", part=2, want=78725270),
        aoc.TestCase(inputs="03081770884921959731165446850517", part=2, want=53553731),
    ]
    INPUT_PARSER = str
    TIMEOUT = 90

    def fft(self, signal: list[int], offset: int) -> list[int]:
        """Compute the FFT.

        This technique leverages two tricks.
        1. When repeatedly summing up sub-ranges, we can be more efficient by computing
           a cumulative/running sum of the numbers. Taking the difference between the
           start and end of the range gives the sum of the range.
        2. The pattern [0, 1, 0, -1] with a shift of 1 means the n'th element is unaffected
           by elements prior to n (they get zeroed out). We can rewrite the pattern as
           [1, 0, -1, 0] starting at element n, no skipping needed.
           If we only care about elements after index n with a large n, we can truncate
           the pattern to start at n. This is the `offset`.
        """
        # Add a -1 element so we can access the pre-range value for the first element.
        cumulative_sums = [0]
        accumulator = 0
        for i in signal:
            accumulator += i
            cumulative_sums.append(accumulator)

        fft_signal = []
        signal_len = len(signal)
        for idx in range(signal_len):
            # Toggle between 1 and -1 on every other range.
            multiplier = 1
            element = 0
            range_len = idx + 1 + offset
            for current_range in range(idx, signal_len, 2 * range_len):
                element += multiplier * (
                    cumulative_sums[min(current_range + range_len, signal_len)] - cumulative_sums[current_range]
                )
                multiplier *= -1
            fft_signal.append(abs(element) % 10)
        return fft_signal

    def solver(self, puzzle_input: str, part_one: bool) -> int:
        """Return a sub-signal after applying FFT to a signal."""
        if part_one:
            offset = 0
        else:
            offset = int(puzzle_input[:7])
            puzzle_input = (puzzle_input * 10000)[offset:]
        signal = [int(i) for i in puzzle_input]
        for i in range(100):
            signal = self.fft(signal, offset)
        return int(str("".join(str(i) for i in signal[:8])))

# vim:expandtab:sw=4:ts=4

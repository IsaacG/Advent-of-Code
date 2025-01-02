#!/bin/python
"""Advent of Code, Day 22: Monkey Market."""

import collections
from lib import aoc

SAMPLE = [
    "1 10 100 2024".replace(" ", "\n"),
    "1 2 3 2024".replace(" ", "\n"),
]
MOD = 16777216


class Day22(aoc.Challenge):
    """Day 22: Monkey Market."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=37327623),
        aoc.TestCase(part=2, inputs=SAMPLE[1], want=23),
    ]
    TIMEOUT = 300

    @staticmethod
    def pseudo_randon(number: int) -> int:
        """Generate the next pseudo random number."""
        number = (number ^ (number << 6)) % MOD   # i <<  6 == i  *   64
        number = (number ^ (number >> 5)) % MOD   # i >>  5 == i //   32
        number = (number ^ (number << 11)) % MOD  # i << 11 == i  * 2048
        return number

    def part1(self, puzzle_input: list[int]) -> int:
        """Compute the 2000th pseudo random number."""
        total = 0
        for number in puzzle_input:
            for _ in range(2000):
                number = self.pseudo_randon(number)
            total += number
        return total

    def part2(self, puzzle_input: list[int]) -> int:
        """Find the delta-pattern which maximizes returns."""

        def delta_values():
            """Generate the deltas between the last digit of 2000 prices."""
            patterns_seen = set()
            delta_collections = []
            for number in puzzle_input:
                deltas = collections.deque(maxlen=4)
                # Compute the first three deltas.
                for _ in range(3):
                    next_num = self.pseudo_randon(number)
                    deltas.append((next_num % 10) - (number % 10))
                    number = next_num
                prices_per_pattern = {}
                # Load the next number, compute the delta. Store the price for the run of the last 5 prices.
                for _ in range(1997):
                    next_num = self.pseudo_randon(number)
                    deltas.append((next_num % 10) - (number % 10))
                    number = next_num

                    # Create a pattern based on four deltas.
                    pattern = 0
                    for delta in deltas:
                        pattern = pattern * 100 + delta

                    patterns_seen.add(pattern)
                    if pattern not in prices_per_pattern:
                        prices_per_pattern[pattern] = number % 10
                delta_collections.append(prices_per_pattern)
            return delta_collections, patterns_seen

        sequence_prices, patterns_seen = delta_values()

        if self.testing:
            deltas = [-2, 1, -1, 3]
            pattern = deltas[0] * 1000000 + deltas[1] * 10000 + deltas[2] * 100 + deltas[3] * 1
            return sum(prices.get(pattern, 0) for prices in sequence_prices)

        return max(
            sum(prices.get(pattern, 0) for prices in sequence_prices)
            for pattern in patterns_seen
        )

# vim:expandtab:sw=4:ts=4

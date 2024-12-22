#!/bin/python
"""Advent of Code, Day 22: Monkey Market."""

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

    def pseudo_randon(self, number: int) -> int:
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
            sequences = set()
            delta_collections = []
            for number in puzzle_input:
                sequence = [number % 10]
                for _ in range(2000):
                    number = self.pseudo_randon(number)
                    sequence.append(number % 10)
                coll = {}
                for i in range(len(sequence) - 4):
                    nums = sequence[i:i + 5]
                    deltas = [b - a + 9 for a, b in zip(nums, nums[1:])]
                    fp = deltas[0] + deltas[1] * 100 + deltas[2] * 10000 + deltas[3] * 1000000
                    sequences.add(fp)
                    if fp not in coll:
                        coll[fp] = nums[-1]
                delta_collections.append(coll)
            return delta_collections, sequences

        sequence_prices, sequences = delta_values()

        if self.testing:
            deltas = [-2, 1, -1, 3]
            fp = deltas[0] + deltas[1] * 100 + deltas[2] * 10000 + deltas[3] * 1000000
            return sum(prices.get(fp, 0) for prices in sequence_prices)

        return max(
            sum(prices.get(fp, 0) for prices in sequence_prices)
            for fp in sequences
        )

# vim:expandtab:sw=4:ts=4

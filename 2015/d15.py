#!/bin/python
"""Advent of Code, Day 15: Science for Hungry People."""

import itertools

from lib import aoc

SAMPLE = """\
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"""

LineType = int
InputType = list[LineType]
PROPERTIES = "capacity durability flavor texture".split()


class Day15(aoc.Challenge):
    """Day 15: Science for Hungry People."""

    ATTEMPTED = """
    Attempt to write a product() with better limiting:
        names = list(puzzle_input)
        n = len(names)

        combos = [[]]
        for name in names:
            combos = [
                x + [y]
                for x in combos
                for y in range(min(101 - sum(x), limits[name] + 1))
            ]
    """

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=62842880),
        aoc.TestCase(inputs=SAMPLE, part=2, want=57600000),
    ]

    def sorted_limits(self, ingredients: InputType, check_calories: bool) -> int:
        """Generate the acceptable ranges for each ingredient.

        The upper limit of ingredients can be computed based on their
        negative properties.  If one item has -5 capacity, the other
        ingredients must counter that capacity to yield a capacity > 0.

        We can find the ingredient with the largest capacity to offset it and
        use the to limit the first ingredient.
        That limits can then be fed into itertools.product() to reduce generated options.

        ```
        Tbsp_a * abs_score_a < Tbsp_b * score_b
        Tbsp_a * abs_score_a < (100 - Tbsp_a) * score_b
        Tbsp_a * abs_score_a < 100 * score_b - Tbsp_a * score_b
        Tbsp_a * abs_score_a + Tbsp_a * score_b < 100 * score_b
        Tbsp_a * (abs_score_a + score_b) < 100 * score_b
        Tbsp_a < (100 * score_score_b) / (abs_score_a + score_b)
        Tbsp_a < (100 * mx) / (-val + mx)
        ```
        """
        limits = {name: 100 for name in ingredients}
        for name, props in ingredients.items():
            if check_calories:
                limits[name] = min(100, 500 // props["calories"])
            for prop, val in props.items():
                if val >= 0:
                    continue
                lim, num = max((p[prop], num) for num, p in ingredients.items())
                limit = (100 * lim) // (lim - val)
                limits[name] = min(limit, limits[name])
        return sorted((limit, name) for name, limit in limits.items())

    def combo_generator_b(self, ingredients: InputType, check_calories: bool):
        """Generate amount combinations to try."""
        ranges, _ = list(zip(*self.sorted_limits(ingredients, check_calories)))
        for amounts in itertools.product(*[range(i + 1) for i in ranges[:-1]]):
            yield amounts + (100 - sum(amounts),)

    def combo_generator(self, ingredients: InputType, check_calories: bool):
        """Generate amount combinations to try."""
        ranges, _ = list(zip(*self.sorted_limits(ingredients, check_calories)))
        num = len(ranges)
        amounts = [0] * (num - 1)
        while amounts[-1] <= ranges[-2]:
            yield amounts + [100 - sum(amounts)]
            while True:
                amounts[0] += 1
                for i in range(num - 2):
                    if amounts[i] > ranges[i]:
                        amounts[i] = 0
                        amounts[i + 1] += 1
                if sum(amounts) <= 100:
                    break

    def solver(self, puzzle_input: InputType, check_calories: bool) -> int:
        """Solve for the optimal recipe."""
        most = 0
        _, names = list(zip(*self.sorted_limits(puzzle_input, check_calories)))
        for amounts in self.combo_generator(puzzle_input, check_calories):
            name_amounts = list(zip(names, amounts))
            if check_calories and sum(
                amount * puzzle_input[name]["calories"]
                for name, amount in name_amounts
            ) != 500:
                continue
            total = 1
            for prop in PROPERTIES:
                total *= max(0, sum(
                    amount * puzzle_input[name][prop]
                    for name, amount in name_amounts
                ))
                if total == 0:
                    continue
            if total > most:
                most = total
        return most

    def part1(self, puzzle_input: InputType) -> int:
        return self.solver(puzzle_input, check_calories=False)

    def part2(self, puzzle_input: InputType) -> int:
        return self.solver(puzzle_input, check_calories=True)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        data = {}
        for line in puzzle_input.splitlines():
            name, properties = line.split(": ", 1)
            data[name] = {
                prop.split()[0]: int(prop.split()[-1])
                for prop in properties.split(", ")
            }
        return data

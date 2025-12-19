#!/bin/python
"""Advent of Code, Day 15: Science for Hungry People."""

import itertools

from lib import parsers


PROPERTIES = "capacity durability flavor texture".split()


ATTEMPTED = """
Attempt to write a product() with better limiting:
    names = list(data)
    n = len(names)

    combos = [[]]
    for name in names:
        combos = [
            x + [y]
            for x in combos
            for y in range(min(101 - sum(x), limits[name] + 1))
        ]
"""


def sorted_limits(ingredients: dict[str, dict[str, int]], check_calories: bool) -> list[tuple[int, str]]:
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


def combo_generator_b(ingredients: dict[str, dict[str, int]], check_calories: bool):
    """Generate amount combinations to try."""
    ranges, _ = list(zip(*sorted_limits(ingredients, check_calories)))
    for amounts in itertools.product(*[range(i + 1) for i in ranges[:-1]]):
        yield amounts + (100 - sum(amounts),)


def combo_generator(ingredients: dict[str, dict[str, int]], check_calories: bool):
    """Generate amount combinations to try."""
    ranges, _ = list(zip(*sorted_limits(ingredients, check_calories)))
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


def solve(data: dict[str, dict[str, int]], part: int) -> int:
    """Solve for the optimal recipe."""
    check_calories = part == 2
    most = 0
    _, names = list(zip(*sorted_limits(data, check_calories)))
    for amounts in combo_generator(data, check_calories):
        name_amounts = list(zip(names, amounts))
        if check_calories and sum(
            amount * data[name]["calories"]
            for name, amount in name_amounts
        ) != 500:
            continue
        total = 1
        for prop in PROPERTIES:
            total *= max(0, sum(
                amount * data[name][prop]
                for name, amount in name_amounts
            ))
            if total == 0:
                continue
        most = max(total, most)
    return most


def input_parser(data: str) -> dict[str, dict[str, int]]:
    """Parse the input data."""
    recipe = {}
    for line in data.splitlines():
        name, properties = line.split(": ", 1)
        recipe[name] = {
            prop.split()[0]: int(prop.split()[-1])
            for prop in properties.split(", ")
        }
    return recipe


PARSER = parsers.ParseCustom(input_parser)
SAMPLE = """\
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"""
TESTS = [
    (1, SAMPLE, 62842880),
    (2, SAMPLE, 57600000),
]


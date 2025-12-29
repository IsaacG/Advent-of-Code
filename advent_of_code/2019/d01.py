#!/usr/bin/env python
"""2019 Day 01: The Tyranny of the Rocket Equation. Compute fuel costs."""


def fuel(mass):
    """Sum fuel needed for some mass and all its fuel."""
    total = 0
    unfueled = simple_fuel(mass)
    while unfueled:
        total += unfueled
        unfueled = simple_fuel(unfueled)
    return total


def simple_fuel(mass):
    """Direct fuel needed for some mass."""
    return max(0, int(mass / 3) - 2)


def solve(data: list[int], part: int) -> int:
    func = simple_fuel if part == 1 else fuel
    return sum(func(i) for i in data)


TESTS = [
    (1, "12", 2),
    (1, "14", 2),
    (1, "1969", 654),
    (1, "100756", 33583),
    (2, "14", 2),
    (2, "1969", 966),
    (2, "100756", 50346),
]

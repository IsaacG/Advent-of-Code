#!/bin/python
"""Advent of Code, Day 14: Chocolate Charts. Mix recipes until a pattern is found."""


def solve(data: str, part: int) -> int | str:
    """Solve for the target recipes."""
    # Compute target data.
    p1_target = int(data)
    p1_stop = p1_target + 10
    # Note: switching to dequeue made things slower.
    p2_want = [int(i) for i in data]
    p2_want_last = p2_want[-1]
    p2_want_len = len(data)

    # Initialize loop variables.
    recipes = [3, 7]
    elf1, elf2 = 0, 1
    count = 2

    while count < 100000000:
        # Compute the new values to add.
        recipe1, recipe2 = recipes[elf1], recipes[elf2]
        new_recipe = recipe1 + recipe2
        if new_recipe >= 10:
            to_add = [1, new_recipe - 10]
        else:
            to_add = [new_recipe]

        # Add new recipes and check for end conditions.
        for recipe in to_add:
            recipes.append(recipe)
            count += 1
            if part == 2 and recipe == p2_want_last and recipes[-p2_want_len:] == p2_want:
                return count - p2_want_len

        if part == 1 and count >= p1_stop:
            return "".join(str(i) for i in recipes[p1_target:p1_stop])

        # Update the elves' recipes.
        elf1, elf2 = (elf1 + 1 + recipe1) % count, (elf2 + 1 + recipe2) % count
    raise RuntimeError("Unreachable")


PARSER = str
TESTS = [
    (1, "9", "5158916779"),
    (1, "5", "0124515891"),
    (1, "18", "9251071085"),
    (1, "2018", "5941429882"),
    (2, "51589", 9),
    (2, "01245", 5),
    (2, "92510", 18),
    (2, "59414", 2018),
]

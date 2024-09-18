#!/bin/python
"""Advent of Code, Day 14: Chocolate Charts."""

from lib import aoc


class Day14(aoc.Challenge):
    """Day 14: Chocolate Charts. Mix recipes until a pattern is found."""

    INPUT_PARSER = aoc.parse_one_str
    TESTS = [
        aoc.TestCase(inputs="9", part=1, want="5158916779"),
        aoc.TestCase(inputs="5", part=1, want="0124515891"),
        aoc.TestCase(inputs="18", part=1, want="9251071085"),
        aoc.TestCase(inputs="2018", part=1, want="5941429882"),
        aoc.TestCase(inputs="51589", part=2, want=9),
        aoc.TestCase(inputs="01245", part=2, want=5),
        aoc.TestCase(inputs="92510", part=2, want=18),
        aoc.TestCase(inputs="59414", part=2, want=2018),
    ]

    def solver(self, parsed_input: str, part_one: bool) -> int | str:
        """Solve for the target recipes."""
        # Compute target data.
        p1_target = int(parsed_input)
        p1_stop = p1_target + 10
        # Note: switching to dequeue made things slower.
        p2_want = [int(i) for i in parsed_input]
        p2_want_last = p2_want[-1]
        p2_want_len = len(parsed_input)

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
                if not part_one and recipe == p2_want_last and recipes[-p2_want_len:] == p2_want:
                    return count - p2_want_len

            if part_one and count >= p1_stop:
                return "".join(str(i) for i in recipes[p1_target:p1_stop])

            # Update the elves' recipes.
            elf1, elf2 = (elf1 + 1 + recipe1) % count, (elf2 + 1 + recipe2) % count
        raise RuntimeError("Unreachable")

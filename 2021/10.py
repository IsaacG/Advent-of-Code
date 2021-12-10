#!/bin/python
"""Advent of Code: Day 10."""

from typing import Optional
import typer

from lib import aoc

InputType = list[str]

SAMPLE = """\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""
BRACKETS = "()[]{}<>"

class Day10(aoc.Challenge):
    """Solve bracket matching."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=26397),
        aoc.TestCase(inputs=SAMPLE, part=2, want=288957),
    )

    INPUT_TYPES = str

    @staticmethod
    def bracket_match(line: str) -> tuple[Optional[str], list[str]]:
        """Bracket match a line, returning first invalid char and stack."""
        stack = []
        # Map closing bracket to its opening pair.
        pairs = {BRACKETS[i + 1]: BRACKETS[i] for i in range(0, len(BRACKETS), 2)}
        open_chars = pairs.values()  # ([{<
        close_chars = pairs.keys()   # )]}>
        for char in line:
            # Open bracket. Add to the stack.
            if char in open_chars:
                stack.append(char)
            # Close bracket. Pop from the stack or error.
            if char in close_chars:
                if not stack:
                    return char, stack
                if stack[-1] == pairs[char]:
                    stack.pop()
                else:
                    return char, stack
        return None, stack

    def part1(self, lines: InputType) -> int:
        """Find lines with a close bracket without a corresponding open bracket."""
        bracket_values = {")": 3, "]": 57, "}": 1197, ">": 25137}
        # Find the bad closing bracket for each line (or None).
        bad_closing = [self.bracket_match(line)[0] for line in lines]
        # Sum up the value of the bad chars.
        return sum(bracket_values[char] for char in bad_closing if char)

    def part2(self, lines: InputType) -> int:
        """Score the required closing brackets for each line to make it valid."""
        bracket_values = {"(": 1, "[": 2, "{": 3, "<": 4}

        def evaluate_stack(stack: list[str]):
            """Assign a score to remaining brackets."""
            value = 0
            for char in reversed(stack):
                value *= 5
                value += bracket_values[char]
            return value

        # Map each line to the bad closing bracket and remaining stack.
        char_and_stacks = [self.bracket_match(line) for line in lines]
        # Score lines without a bad closing bracket.
        scores = [evaluate_stack(stack) for char, stack in char_and_stacks if not char]
        # Return the middle score.
        return sorted(scores)[len(scores)//2]


if __name__ == "__main__":
    typer.run(Day10().run)

# vim:expandtab:sw=4:ts=4

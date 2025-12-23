#!/bin/python
"""Advent of Code: Day 05."""

from lib import aoc

SAMPLE = ["""\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""]


class Day05(aoc.Challenge):
    """Day 5: Supply Stacks. Move crates from stack to stack."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want="CMZ"),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want="MCD"),
    ]
    INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line, aoc.parse_re_findall_int(r"\d+")])

    def build_stacks(self, setup: list[str]) -> list[list[str]]:
        """Build the initial stacks from input."""
        stack_count = len(setup[-1].split())
        width = stack_count * 4
        stack: list[list[str]] = [[] for _ in range(stack_count)]
        for line in setup[-2::-1]:
            line = line.ljust(width)
            for i in range(stack_count):
                crate = line[1 + i * 4]
                if crate != " ":
                    stack[i].append(crate)
        return stack

    def part1(self, puzzle_input: tuple[list[str], list[tuple[int, int, int]]]) -> str:
        """Return crates after moving them with a CrateMover 9000."""
        setup_block, moves = puzzle_input
        stack = self.build_stacks(setup_block)

        for move_count, src, dst in moves:
            for _ in range(move_count):
                stack[dst - 1].append(stack[src - 1].pop())
        return "".join(s.pop() for s in stack)

    def part2(self, puzzle_input: tuple[list[str], list[tuple[int, int, int]]]) -> str:
        """Return crates after moving them with a CrateMover 9001."""
        setup_block, moves = puzzle_input
        stack = self.build_stacks(setup_block)

        for move_count, src, dst in moves:
            stack[dst - 1].extend(stack[src - 1][-move_count:])
            del stack[src - 1][-move_count:]

        return "".join(s.pop() for s in stack)

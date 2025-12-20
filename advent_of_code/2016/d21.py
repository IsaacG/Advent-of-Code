#!/bin/python
"""Advent of Code, Day 21: Scrambled Letters and Hash. Scramble a password following instructions."""

from lib import aoc


def solve(data: list[list[str]], part: int, testing: bool) -> str:
    """Scramble a password following instructions."""
    if testing:
        input_word = "abcde"
    elif part == 1:
        input_word = "abcdefgh"
    else:
        input_word = "fbgdceah"

    registers = list(input_word)
    size = len(registers)
    # Rotate right, rotate left. Reversed for part 2.
    rotate_direction = {1: {"right": -1, "left": 1}, 2: {"right": 1, "left": -1}}[part]
    if part == 2:
        data.reverse()

    for instruction in data:
        match instruction:
            case ["swap", "position", reg_x, "with", "position", reg_y]:
                registers[int(reg_x)], registers[int(reg_y)] = registers[int(reg_y)], registers[int(reg_x)]
            case ["swap", "letter", reg_x, "with", "letter", reg_y]:
                swap = {reg_x: reg_y, reg_y: reg_x}
                registers = [swap.get(i, i) for i in registers]
            case ["rotate", direction, reg_x, _]:
                dist = int(reg_x)
                dist *= rotate_direction[direction]
                registers = registers[dist:] + registers[:dist]
            case ["reverse", "positions", reg_x, "through", reg_y]:
                start, end = int(reg_x), int(reg_y) + 1
                registers[start:end] = reversed(registers[start:end])
            case ["move", "position", reg_x, "to", "position", reg_y]:
                if part == 2:
                    reg_x, reg_y = reg_y, reg_x
                registers.insert(int(reg_y), registers.pop(int(reg_x)))
            case ["rotate", "based", "on", "position", "of", "letter", reg_x]:
                if part == 1:
                    dist = registers.index(reg_x)
                    dist = -1 * (dist + (2 if dist >= 4 else 1)) % size
                else:
                    new_pos = registers.index(reg_x)
                    options = []
                    # Try every possible original position and see if the distance lines up.
                    for orig_pos in range(size):
                        moved = new_pos - orig_pos
                        if moved <= 0:
                            moved += size
                        dist = (orig_pos + (2 if orig_pos >= 4 else 1)) % size
                        if dist == moved % size:
                            options.append(moved)
                    # The sample input cannot be reversed deterministically. There are multiple valid rotations.
                    assert len(options) == 1, options
                    dist = options[0]

                registers = registers[dist:] + registers[:dist]
    return "".join(registers)


PARSER = aoc.parse_multi_str_per_line
SAMPLE = """\
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d"""
TESTS = [(1, SAMPLE, "decab")]

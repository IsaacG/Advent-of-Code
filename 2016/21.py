#!/bin/python
"""Advent of Code, Day 21: Scrambled Letters and Hash. Scramble a password following instructions."""

from lib import aoc

SAMPLE = """\
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d"""


class Day21(aoc.Challenge):
    """Day 21: Scrambled Letters and Hash."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want="decab"),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_multi_str_per_line

    def solver(self, parsed_input: list[list[str]], part2: bool) -> str:
        """Scramble a password following instructions."""
        if self.testing:
            start = "abcde"
        elif not part2:
            start = "abcdefgh"
        else:
            start = "fbgdceah"

        data = list(start)
        size = len(data)
        # Rotate right, rotate left. Reversed for part 2.
        rotate_direction = {False: {"right": -1, "left": 1}, True: {"right": 1, "left": -1}}[part2]
        if part2:
            parsed_input.reverse()

        for instruction in parsed_input:
            match instruction:
                case ["swap", "position", reg_x, "with", "position", reg_y]:
                    data[int(reg_x)], data[int(reg_y)] =  data[int(reg_y)], data[int(reg_x)]
                case ["swap", "letter", reg_x, "with", "letter", reg_y]:
                    swap = {reg_x: reg_y, reg_y: reg_x}
                    data = [swap.get(i, i) for i in data]
                case ["rotate", direction, reg_x, _]:
                    dist = int(reg_x)
                    dist *= rotate_direction[direction]
                    data = data[dist:] + data[:dist]
                case ["reverse", "positions", reg_x, "through", reg_y]:
                    start, end = int(reg_x), int(reg_y) + 1
                    data[start:end] = reversed(data[start:end])
                case ["move", "position", reg_x, "to", "position", reg_y]:
                    if part2:
                        reg_x, reg_y = reg_y, reg_x
                    data.insert(int(reg_y), data.pop(int(reg_x)))
                case ["rotate", "based", "on", "position", "of", "letter", reg_x]:
                    if not part2:
                        dist = data.index(reg_x)
                        dist = -1 * (dist + (2 if dist >= 4 else 1)) % size
                    else:
                        new_pos = data.index(reg_x)
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

                    data = data[dist:] + data[:dist]
        return "".join(data)

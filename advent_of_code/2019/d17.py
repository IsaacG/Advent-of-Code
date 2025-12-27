#!/bin/python
"""Advent of Code, Day 17: Set and Forget."""
import typing
import intcode
from lib import aoc


def trace_path(coords: dict[str, set[complex]]) -> list[str]:
    """Walk the scaffolding, translating the path to a series of L|R turns and forward steps."""
    scaffolding = coords["#"]
    for char, delta in aoc.ARROW_DIRECTIONS.items():
        if char in coords:
            direction = delta
            pos = coords[char].pop()
            break
    steps = []
    while pos + direction * 1j in scaffolding or pos + direction * -1j in scaffolding:
        if pos + direction * 1j in scaffolding:
            steps.append("R")
            direction *= 1j
        else:
            steps.append("L")
            direction *= -1j
        count = 0
        while pos + direction in scaffolding:
            pos += direction
            count += 1
        steps.append(str(count))
    return steps


def compute_subroutines(steps: list[str]) -> dict[str, list[str]]:
    """Return three subroutines that can be used to compose the steps."""
    segments = [steps]
    subroutines = {}
    for routine in "ABC":
        for size in range(len(segments[0]), 0, -2):
            # Find the largest block of steps that repeats at least three times.
            block = segments[0][:size]
            count = sum(
                block == segment[i:i + size]
                for segment in segments
                for i in range(len(segment) - size + 1)
            )
            if count > 2:
                # Remove the subroutine and compute the remaining segments.
                subroutines[routine] = block
                new_segments = []
                for segment in segments:
                    idx = 0
                    while idx < len(segment):
                        start = idx
                        while idx < len(segment) and segment[idx:idx + size] != block:
                            idx += 2
                        if start != idx:
                            new_segments.append(segment[start:idx])
                        idx += size
                segments = new_segments
                break

    assert not segments, "There should be no remaining segments."
    return subroutines


def compute_program(steps: list[str], subroutines: dict[str, list[str]]) -> list[str]:
    """Translate a series of steps into subroutines."""
    idx = 0
    program = []
    while idx < len(steps):
        for name, sub in subroutines.items():
            if steps[idx:idx + len(sub)] == sub:
                program.append(name)
                idx += len(sub)
                break
    return program


class Day17(aoc.Challenge):
    """Day 17: Set and Forget."""

    TESTS = [
        aoc.TestCase(inputs="", part=1, want=aoc.TEST_SKIP),
        aoc.TestCase(inputs="", part=2, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_one_str

    def solver(self, puzzle_input: str, part_one: bool) -> int:
        computer = intcode.Computer(puzzle_input)
        # Run the computer, read the output map, parse it.
        computer.run()
        data = [chr(i) for i in computer.output]
        display = aoc.CoordinatesParserC(chars="#<>^v").parse("".join(data))
        scaffolding = display.coords["#"]
        if part_one:
            return sum(
                int(pos.real * pos.imag)
                for pos in scaffolding
                if all(pos + direction in scaffolding for direction in aoc.FOUR_DIRECTIONS)
            )
        # Convert the path to a series of L|R turns and steps forward.
        steps = trace_path(typing.cast(dict[str, set[complex]], display.coords))
        # Find repeating patterns/subroutines in the data.
        subroutines = compute_subroutines(steps)
        # Translate the steps into a series of subroutines.
        program = compute_program(steps, subroutines)

        # Write the ASCII program and subroutines into the computer and run it.
        computer.reset()
        computer.memory[0] = 2
        computer.input_line(",".join(program))
        for name in "ABC":
            computer.input_line(",".join(subroutines[name]))
        computer.input_line("n")
        computer.run()
        # Read the result.
        return computer.output.pop()

# vim:expandtab:sw=4:ts=4

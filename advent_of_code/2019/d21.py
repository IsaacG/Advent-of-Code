#!/bin/python
"""Advent of Code, Springdroid Adventure."""
import intcode


def solve(data: str, part: int) -> int:
    """Run a springscript ASCII program to navigate a droid across holes."""
    computer = intcode.Computer(data)
    computer.run()
    if part == 1:
        # Jump if (there is a hole in 1,2, or 3) and (there is ground at 4).
        # (!A || !B || !C) && (D)
        program = """\
            NOT A J
            NOT B T
            OR  T J
            NOT C T
            OR  T J
            AND D J
            WALK
        """
    else:
        # Jump if there is an upcoming hole
        # and there is a place to land
        # and we have a place to go from there.
        # (!1 || !2 || !3) && 4 && (8 || (5 && (6 || 9)))
        # (!A || !B || !C) && D && (H || (E && (F || I)))
        # (!A || !B || !C) && D && (((F || I) && E) || H)
        program = """
            NOT A J
            NOT B T
            OR  T J
            NOT C T
            OR  T J
            AND D J
            NOT F T
            NOT T T
            OR  I T
            AND E T
            OR  H T
            AND T J
            RUN
        """
    for line in program.strip().splitlines():
        computer.input_line(line.strip())
    computer.run()
    got = computer.output.pop()
    if got < 255:
        # Did not make it across. Print output.
        computer.output.append(got)
        print(computer.get_output())
    return got


PARSER = str
TESTS = list[tuple[int, int, int]]()

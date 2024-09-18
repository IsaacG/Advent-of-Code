#!/bin/python
"""Advent of Code, Day 22: Sporifica Virus."""

from lib import aoc


SAMPLE = """\
..#
#..
..."""
CLEAN, WEAKENED, INFECTED, FLAGGED = range(4)
STATES_P1 = [CLEAN, INFECTED, CLEAN]
STATES_P2 = [CLEAN, WEAKENED, INFECTED, FLAGGED, CLEAN]
ROTATIONS = {CLEAN: 1j, WEAKENED: 1, INFECTED: -1j, FLAGGED: -1}


class Day22(aoc.Challenge):
    """Day 22: Sporifica Virus."""

    INPUT_PARSER = aoc.ParseMultiple(
        [
            aoc.Transform(lambda x: len(x.splitlines())),
            aoc.AsciiBoolMapParser("#", origin_top_left=False),
        ]
    )

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=5587),
        aoc.TestCase(part=2, inputs=SAMPLE, want=2511944),
    ]

    def solver(self, parsed_input: tuple[int, set[complex]], part_one: bool) -> int:
        """Simulate a virus and count the infections."""
        dimension, initial_infected = parsed_input
        board = {i: INFECTED for i in initial_infected}
        states = STATES_P1 if part_one else STATES_P2
        next_state = {a: b for a, b in zip(states[:-1], states[1:])}
        direction = complex(0, 1)
        location = complex(1, 1) * ((dimension - 1) // 2)
        infected = 0
        for step in range(10000 if part_one else 10000000):
            state = board.get(location, CLEAN)
            direction *= ROTATIONS[state]
            board[location] = next_state[state]
            if board[location] == INFECTED:
                infected += 1
            location += direction

        return infected

# vim:expandtab:sw=4:ts=4

#!/bin/python
"""Advent of Code, Day 12: Subterranean Sustainability. Compute what plants will be alive in future generations."""

from lib import aoc

SAMPLE = [
    """\
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #""",  # 23
]

InputType = tuple[list[list[bool]], list[list[bool]]]


class Day12(aoc.Challenge):
    """Day 12: Subterranean Sustainability."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=325),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.ParseBlocks(
        [aoc.BaseParseReFindall(r"[.#]", lambda line: [i == "#" for i in line])] * 2
    )

    def solver(self, parsed_input: InputType, part_one: bool) -> int:
        """Simulate N generations of plant growth."""
        # How many generations to simulate.
        target_gen = 20 if part_one else 50000000000
        state = {i for i, j in enumerate(parsed_input[0][0]) if j}
        # Rules for new generations.
        rules = {tuple(rule[:5]) for rule in parsed_input[1] if rule[5]}
        # Cycle detection.
        seen: dict[frozenset[int], tuple[int, int]] = {}

        for gen in range(target_gen):
            new_state = set()
            for pot in range(min(state) - 2, max(state) + 3):
                window = tuple(i in state for i in range(pot - 2, pot + 3))
                if window in rules:
                    new_state.add(pot)

            state = new_state
            # For cycle detection, shift pots so the pattern is relative to "0".
            offset = min(state)
            shift_state = frozenset(pot - offset for pot in state)
            # Cycle detected.
            if shift_state in seen:
                prior_gen, prior_offset = seen[shift_state]
                gen_delta, offset_delta = (gen - prior_gen, offset - prior_offset)
                assert gen_delta == 1  # Less math if the cycle is 1 gen each.
                steps = target_gen - gen - 1
                total_shift = steps * offset_delta
                state = {pot + total_shift for pot in state}
                break
            else:
                # Record generation.
                seen[shift_state] = gen, offset

        return sum(state)

#!/bin/python
"""Advent of Code, Day 15: Beverage Bandits."""
from __future__ import annotations

import collections
import copy
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######""", 27730, 4988,
    """\
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######""", 36334, None,
    """\
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######""", 39514, 31284,
    """\
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######""", 27755, 3478,
    """\
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######""", 28944, 6474,
    """\
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########""", 18740, 1140,
]

LineType = int
InputType = list[LineType]
OTHER = {"E": "G", "G": "E"}


def reading_order(position: complex) -> tuple[float, float]:
    return position.imag, position.real


class Day15(aoc.Challenge):
    """Day 15: Beverage Bandits."""

    DEBUG = False
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[i], part=1, want=SAMPLE[i + 1])
        for i in range(0, 18, 3)
    ] + [
        aoc.TestCase(inputs=SAMPLE[i], part=2, want=SAMPLE[i + 2])
        for i in range(0, 18, 3)
        if SAMPLE[i + 2]
    ]

    def part1(self, parsed_input: InputType) -> int:
        return self.simulate(*parsed_input, 3)

    def part2(self, parsed_input: InputType) -> int:
        spaces, og_units = parsed_input
        elf_count = len(og_units["E"])
        for elf_damage in range(3, 100):
            units = copy.deepcopy(og_units)
            score = self.simulate(spaces, units, elf_damage)
            if len(units["E"]) == elf_count:
                assert score < 59339
                return score

    def simulate(self, spaces, units_by_type, elf_damage) -> int:
        """Simulate a battle."""
        damage = {"G": 3, "E": elf_damage}
        occupied = {
            location: unit_type
            for unit_type in "EG"
            for location in units_by_type[unit_type]
        }

        # Similate up to 200 rounds of combat.
        for count in range(200):
            # Each unit acts in reading order.
            for location in sorted(occupied, key=reading_order):
                # A unit may have been killed. If so, skip.
                if location not in occupied:
                    continue

                unit_type = occupied[location]
                friends = units_by_type[unit_type]
                other_type = OTHER[unit_type]
                enemies = units_by_type[other_type]

                # Check if the battle is ended. Check on a per-unit basis to accurately capture
                # which round was fully completed.
                if not enemies:
                    self.debug(f"Battle ended. Round {count}, winner={unit_type}, {elf_damage=}")
                    return count * sum(hp for hp in friends.values())

                # Move if there is no adjacent enemy.
                if not any(neighbor in enemies for neighbor in aoc.neighbors(location)):
                    open_spaces = set(spaces) - set(occupied)
                    # Compute all potential locations we can move to attack an enemy.
                    enemies_reachable = {
                        neighbor
                        for target_location, unit in enemies.items()
                        for neighbor in aoc.neighbors(target_location)
                        if neighbor in open_spaces
                    }
                    # BFS to compute the closest move_to target, along with the best path.
                    candidates = {location}
                    seen = {location}
                    prior_location = collections.defaultdict(set)
                    steps = 0
                    # Keep expanding until we have reached a valid move_to location.
                    while enemies_reachable and candidates and candidates.isdisjoint(enemies_reachable):
                        new_candidates = set()
                        for candidate in candidates:
                            for neighbor in aoc.neighbors(candidate):
                                if neighbor in open_spaces and neighbor not in seen:
                                    new_candidates.add(neighbor)
                                    # Used to backtrack and compute a path.
                                    prior_location[neighbor].add(candidate)
                        seen.update(new_candidates)
                        candidates = new_candidates
                        steps += 1
                    options = candidates & enemies_reachable
                    if options:
                        # All options are equal distance. Pick based on reading order.
                        move_to = min(options, key=reading_order)
                        # Follow the path backwards to find the next step which brings us to the enemy.
                        next_step = {move_to}
                        for _ in range(steps - 1):
                            next_step = {p for n in next_step for p in prior_location[n]}
                        new_loc = min(next_step, key=reading_order)
                        assert abs(new_loc - location) == 1, "Moving more than one space!"
                        # self.debug(f"{units[location]['type']} ({location}) {move_to=} {steps=} via {new_loc}")
                        # Update this unit's location.
                        friends[new_loc] = friends[location]
                        occupied[new_loc] = unit_type
                        del friends[location]
                        del occupied[location]
                        location = new_loc
                    else:
                        # self.debug(f"{units[location]['type']} at {location} unable to attack or move")
                        pass
                else:
                    # self.debug(f"{units[location]['type']} at {location} can attack without moving")
                    pass

                # Attack if possible.
                neighboring_enemies = {neighbor for neighbor in aoc.neighbors(location) if neighbor in enemies}
                if neighboring_enemies:
                    # Pick a target based on lowest health then reading order.
                    target = min(neighboring_enemies, key=lambda x: (enemies[x], x.imag, x.real))
                    enemies[target] -= damage[unit_type]
                    # self.debug(f"{units[location]['type']} at {location} attacks {target}, hp={units[target]['hp']}")
                    if enemies[target] <= 0:
                        self.debug(f"Round {count}: {unit_type}@{location} kills {other_type}@{target}")
                        del enemies[target]
                        del occupied[target]
                else:
                    # self.debug(f"Round: {count}. {location=} cannot find anyone to attack")
                    pass


        return 0

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        spaces = aoc.parse_ascii_bool_map(".EG").parse(puzzle_input)

        units = {
            unit_type: {
                i: 200
                for i in aoc.parse_ascii_bool_map(unit_type).parse(puzzle_input)
            }
            for unit_type in "EG"
        }
        return spaces, units

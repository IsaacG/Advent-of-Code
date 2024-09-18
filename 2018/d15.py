#!/bin/python
"""Advent of Code, Day 15: Beverage Bandits."""

import collections
import copy
import itertools

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

InputType = tuple[set[complex], dict[str, dict[complex, int]]]
OTHER = {"E": "G", "G": "E"}


def reading_order(position: complex) -> tuple[float, float]:
    """Helper function to sort by reading order."""
    return position.imag, position.real


class Day15(aoc.Challenge):
    """Day 15: Beverage Bandits. Simulate a D&D style battle between Elves and Goblins."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[i], part=part, want=SAMPLE[i + part])
        for i in range(0, len(SAMPLE), 3)
        for part in [1, 2]
    ]

    def part1(self, puzzle_input: InputType) -> int:
        """Compute the number of rounds in an even battle."""
        return self.simulate(*puzzle_input, 3)

    def part2(self, puzzle_input: InputType) -> int:
        """Compute how much damage boost the Elves need to win without a fatality."""
        spaces, og_units = puzzle_input
        elf_count = len(og_units["E"])
        for elf_damage in itertools.count(start=3):
            units = copy.deepcopy(og_units)
            score = self.simulate(spaces, units, elf_damage)
            # Check if there are no fatalities.
            if len(units["E"]) == elf_count:
                return score
        raise RuntimeError("Unreachable")

    def simulate(self, spaces: set[complex], units_by_type: dict[str, dict[complex, int]], elf_damage: int) -> int:
        """Simulate a battle."""
        damage = {"G": 3, "E": elf_damage}
        occupied = {
            location: unit_type
            for unit_type in units_by_type
            for location in units_by_type[unit_type]
        }

        # Similate combat
        for count in itertools.count():
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

                    if options := candidates & enemies_reachable:
                        # All options are equal distance. Pick based on reading order.
                        move_to = min(options, key=reading_order)
                        # Follow the path backwards to find the next step which brings us to the enemy.
                        next_step = {move_to}
                        for _ in range(steps - 1):
                            next_step = {p for n in next_step for p in prior_location[n]}
                        new_loc = min(next_step, key=reading_order)
                        # Update this unit's location.
                        friends[new_loc] = friends[location]
                        occupied[new_loc] = unit_type
                        del friends[location]
                        del occupied[location]
                        location = new_loc

                # Attack if possible.
                neighboring_enemies = {neighbor for neighbor in aoc.neighbors(location) if neighbor in enemies}
                if neighboring_enemies:
                    # Pick a target based on lowest health then reading order.
                    target = min(neighboring_enemies, key=lambda x: (enemies[x], x.imag, x.real))
                    enemies[target] -= damage[unit_type]
                    # Remove dead units.
                    if enemies[target] <= 0:
                        del enemies[target]
                        del occupied[target]
        raise RuntimeError("Unreachable")

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        spaces = aoc.AsciiBoolMapParser(".EG").parse(puzzle_input)
        units = {
            unit_type: {
                i: 200
                for i in aoc.AsciiBoolMapParser(unit_type).parse(puzzle_input)
            }
            for unit_type in "EG"
        }
        return spaces, units

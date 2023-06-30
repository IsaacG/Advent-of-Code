#!/bin/python
"""Advent of Code, Day 11: Radioisotope Thermoelectric Generators. Solve moving devices around the warehouse."""

import functools
import itertools
import queue
import re
from collections.abc import Generator, Iterable

from lib import aoc

SAMPLE = """\
The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant."""
LineType = int
InputType = list[LineType]
Device = tuple[int, bool]


class Day11(aoc.Challenge):
    """Day 11: Radioisotope Thermoelectric Generators."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=11),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_re_group_str(r"The (.*) floor contains (.*)\.$")

    @functools.cache
    def valid_floor(self, floor: Iterable[Device]) -> bool:
        """Return if all chips on the floor have a generator."""
        generators = {material for material, device in floor if device}
        chips = {material for material, device in floor if not device}
        unpowered_chips = chips - generators
        return not (unpowered_chips and generators)

    @functools.cache
    def valid(self, state: tuple[Iterable[Device], ...]) -> bool:
        """Return if all floors are valid."""
        return all(self.valid_floor(floor) for floor in state)

    def moves(self, floor: Iterable[Device]) -> Generator[tuple[set[Device], set[Device]], None, None]:
        """Generator what devices can be moved off a floor while leaving the floor valid."""
        candidates = [{device} for device in floor]
        candidates.extend(set(i) for i in itertools.combinations(floor, 2))
        for candidate in candidates:
            new_floor = floor - candidate
            if self.valid_floor(new_floor):
                yield (candidate, new_floor)

    @staticmethod
    def cost(floors: Iterable[Device]) -> int:
        """A* cost function: minimum moves needed to solve the puzzle."""
        return sum(len(floor) * i for i, floor in zip((3, 2, 1), floors[:3]))

    def part1(self, parsed_input: InputType) -> int:
        """Solve for minimum moves using A*."""
        state, materials = parsed_input

        # Initial setup
        elevator, steps = 0, 0
        todo = queue.PriorityQueue()
        todo.put((self.cost(state), steps, elevator, state))
        seen = {(elevator, state): 0}

        while not todo.empty():
            # Pop the lowest cost state to explore.
            _, steps, elevator, state = todo.get()
            # Check if we are done.
            if all(not floor for floor in state[:3]):
                self.debug(f"Seen states: {len(seen)}")
                return steps
            next_steps = steps + 1
            next_floors = {elevator + n for n in (1, -1) if 0 <= elevator + n <= 3}

            # Consider all possible valid moves (devices which can move into the elevator).
            for moving, new_floor in self.moves(state[elevator]):
                # Consider which direction the elevator moves in.
                for next_floor in next_floors:
                    # Check if the floor we move onto is valid.
                    new_next = frozenset(state[next_floor] | moving)
                    if not self.valid_floor(new_next):
                        continue

                    # Compute what the new state looks like with the moving devices on the new floor.
                    new_floors = list(state)
                    new_floors[elevator] = new_floor
                    new_floors[next_floor] = new_next
                    new_floors = tuple(new_floors)

                    # Have we encountered this state before at a lower cost?
                    if (next_floor, new_floors) in seen and seen[(next_floor, new_floors)] <= next_steps:
                        continue
                    # Add this option to the queue.
                    seen[(next_floor, new_floors)] = next_steps
                    todo.put((self.cost(new_floors), next_steps, next_floor, new_floors))

    def part2(self, parsed_input: InputType) -> int:
        """Add extra devices then solve the puzzle."""
        state, materials = parsed_input
        floors = list(state)
        ground = list(floors[0])
        for material in ("dilithium", "elerium"):
            materials.append(material)
            material_idx = materials.index(material)
            for device_type in (True, False):
                ground.append((material_idx, device_type))
        floors[0] = frozenset(ground)
        return self.part1((tuple(floors), materials))

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        state = [[] for _ in range(4)]
        floor_names = ["first", "second", "third", "fourth"]
        line_re = re.compile(r"The (.*) floor contains (.*)\.")
        content_re = re.compile(r"a (\w+)( generator|-compatible microchip)")

        materials = []
        for line in puzzle_input.splitlines():
            if not (m := line_re.fullmatch(line).groups()):
                print(f"{line!r} did not match regex.")
                continue
            floor, contents = line_re.fullmatch(line).groups()
            if contents == "nothing relevant":
                self.debug(f"{floor} is empty")
                continue

            floor_idx = floor_names.index(floor)
            for material, device in content_re.findall(contents):
                if material not in materials:
                    materials.append(material)
                material_idx = materials.index(material)
                state[floor_idx].append((material_idx, device.strip() == "generator"))

        return tuple(frozenset(floor) for floor in state), materials


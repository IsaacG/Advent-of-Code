#!/bin/python
"""Advent of Code, Day 11: Radioisotope Thermoelectric Generators."""
from __future__ import annotations

import collections
import functools
import itertools
import queue
import math
import re

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

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

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
        candidates = [{device} for device in floor]
        candidates.extend(set(i) for i in itertools.combinations(floor, 2))
        for candidate in candidates:
            new_floor = floor - candidate
            if self.valid_floor(new_floor):
                yield (candidate, new_floor)

    def part1(self, parsed_input: InputType) -> int:
        state, materials = parsed_input
        # print(f"{state=}, {materials=}, {self.valid(state)=}")

        def cost(floors: Iterable[floors]) -> int:
            return sum(len(floor) * i for i, floor in zip((3, 2, 1), floors[:3]))

        todo = queue.PriorityQueue()
        todo.put((cost(state), 0, 0, state))
        seen = {}
        count = 1

        while not todo.empty():
            if count % 100000 == 0:
                print(count)
            count += 1
            _, steps, elevator, state = todo.get()
            next_steps = steps + 1
            if (elevator, state) in seen and seen[(elevator, state)] <= steps:
                continue
            seen[(elevator, state)] = steps

            next_floors = {elevator + n for n in (1, -1) if 0 <= elevator + n <= 3}
            for moving, new_floor in self.moves(state[elevator]):
                # print(f"Move {moving}, leaving {new_floor}")
                for next_floor in next_floors:
                    new_next = frozenset(state[next_floor] | moving)
                    if not self.valid_floor(new_next):
                        continue
                    # self.debug(f"Move {moving} from {elevator} to {next_floor}")
                    new_floors = list(state)
                    new_floors[elevator] = new_floor
                    new_floors[next_floor] = new_next
                    new_floors = tuple(new_floors)
                    # self.debug(f"{new_floors=}")
                    todo.put((cost(new_floors), next_steps, next_floor, new_floors))

                    if next_floor == 3 and not new_floor and not new_floors[0] and not new_floors[1]:
                        print("Seen states:", len(seen))
                        return next_steps

    def part2(self, parsed_input: InputType) -> int:
        state, materials = parsed_input
        floors = list(state)
        ground = list(floors[0])
        for material in ("elerium", "dilithium"):
            materials.append(material)
            material_idx = materials.index(material)
            for device_type in (True, False):
                ground.append((material_idx, device_type))
        floors[0] = frozenset(ground)
        return self.part1((tuple(floors), materials))

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

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


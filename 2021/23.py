#!/bin/python
"""Advent of Code: Day 23.

Optimizations needed:
* Use A* and h(): x-distance

The A* should help when you have:

#############
#...........#
###.#A#.#.###
  #.#.#.#.#
  #########

when moving to the hallway first, Dijkstra generates:
############# Cost: 2
#...A.......#
###.#.#.#.###
  #.#.#.#.#
  #########

############# Cost: 2
#.....A.....#
###.#.#.#.###
  #.#.#.#.#
  #########

Since both have the same cost, either might be considered first.
This generates A in home-room with costs 5 or 9, depending which
is considered first.
"""

import collections
import functools
import itertools
import re

import typer
from lib import aoc

SAMPLE = """\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""
InputType = tuple[tuple[str, int, int], ...]

STEP_COST = {"A": 1, "B": 10, "C": 100, "D": 1000}
ROOM_X = dict(zip("ABCD", (2, 4, 6, 8)))
VALID_HALLWAY = {(x, 0) for x in range(11) if x not in ROOM_X.values()}
ALL_HALLWAY = {(x, 0) for x in range(11)}


class AmphipodGame:

    def __init__(self, room_size, iter_limit):
        self.room_size = room_size
        self.iter_limit = iter_limit

        self.room = {
            name: {(x, y) for y in range(1, room_size+1)}
            for name, x in ROOM_X.items()
        }
        all_rooms = set(itertools.chain.from_iterable(self.room.values()))
        self.all_spots = ALL_HALLWAY | all_rooms
        self.valid_spots = VALID_HALLWAY | all_rooms

    def solve(self, pieces):
        for assumption in ["ABCD"[i:] for i in range(1, 5)]:
            if solution := self.solve_with_assumption(pieces, assumption):
                return solution

    def solve_with_assumption(self, pieces, assumption):
        self.no_extra_move = assumption
        to_explore = set([pieces])
        cost = {pieces: 0}
        f_cost = {pieces: 0}

        count = 0
        while to_explore and count < self.iter_limit:
            count += 1
            current = sorted(to_explore, key=lambda x: f_cost[x])[0]
            to_explore.remove(current)

            for board, move_cost in self.next_board(current).items():
                combined_cost = cost[current] + move_cost
                if board in cost and cost[board] <= combined_cost:
                    continue
                cost[board] = combined_cost
                f_cost[board] = combined_cost + self.heuristic(board)
                to_explore.add(board)

        final_pos = tuple(sorted((amphi, x, y) for amphi, room in self.room.items() for x, y in room))
        return cost.get(final_pos)

    @functools.cache
    def heuristic(self, pieces):
        cost = 0
        for piece in pieces:
            amphi, x, y = piece
            want_x = ROOM_X[amphi]
            cost += STEP_COST[amphi] * abs(x - want_x)
        return cost

    @functools.cache
    def can_reach(self, start, occupied):
        to_explore = set([start])
        explored = set()
        steps = {start: 0}
        while to_explore:
            cur = sorted(to_explore, key=lambda x: steps[x])[0]
            to_explore.remove(cur)
            explored.add(cur)
            for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                maybe = (cur[0] + x, cur[1] + y)
                if maybe in explored or maybe in occupied:
                    continue
                if maybe in self.all_spots:
                    to_explore.add(maybe)
                    steps[maybe] = steps[cur] + 1
        del steps[start]
        return {pos: cost for pos, cost in steps.items() if pos in self.valid_spots}

    def next_board(self, positions):
        next_positions = {}
        for piece in positions:
            for n, cost in self.valid_moves(piece, positions).items():
                next_positions[n] = cost
        return next_positions

    def valid_moves(self, start, positions):
        amphi, loc = start[0], start[1:]
        locations = tuple(sorted(i[1:] for i in positions))
        room = self.room[amphi]
        only_right = not any(
            (x, y) in room and piece != amphi
            for piece, x, y in positions
        )
        step_cost = STEP_COST[amphi]

        # If the amphipod is in its room and there are no other types of amphipods in that
        # room, it will not move.
        if loc in room and only_right:
            return {}
        # If the amphipod is in the hallway, it will only move to the home room.
        # If the home room has other amphipods, it will not move.
        if loc in VALID_HALLWAY and not only_right:
            return {}

        reachable = self.can_reach(loc, locations)
        valid = reachable.keys()
        valid_to_home = valid & room

        # If the amphipod can move to the home room, always do that.
        if only_right and valid_to_home:
            valid = set([max(valid_to_home)])
        # If the amphipod is in the hallway, it will only move to the home room.
        # That is checked in the prior clause. If that is not an option,
        # the amphipod will stay in the hallway without moving.
        elif loc in VALID_HALLWAY:
            return {}
        # Otherwise, the amphipod will only move to the hallway..
        else:
            valid &= VALID_HALLWAY
            # Attempt to solve assuming no_extra_move pieces never move in the direction away from their home room.
            if amphi in self.no_extra_move and loc not in room:
                want_x = ROOM_X[amphi]
                if loc[0] > want_x:
                    valid_x = range(want_x, loc[0] + 1)
                else:
                    valid_x = range(loc[0], want_x + 1)
                valid = {(x, y) for x, y in valid if x in valid_x}

        next_steps = {}
        other_pieces = list(positions)
        other_pieces.remove(start)
        for p in valid:
            energy = reachable[p] * step_cost
            new_positions = tuple(sorted(other_pieces + [(amphi,) + p]))
            next_steps[new_positions] = energy
        return next_steps

    def show(self, pieces):
        locations = {}
        for piece in pieces:
            if len(piece) == 2:
                n = "X"
                x, y = piece
            elif len(piece) == 3:
                n, x, y = piece
            else:
                raise ValueError(repr(piece))
            locations[(x, y)] = n
        print("#" * 13)
        for y in range(3):
            if y == 0:
                line = "#"
                for x in range(11):
                    line += locations.get((x, y), " ")
                line += "#"
                print(line)
            else:
                line = "#"
                for x in range(11):
                    if x in (2, 4, 6, 8):
                        line += locations.get((x, y), " ")
                    else:
                        line += "#"
                line += "#"
                print(line)
        print("#" * 13)
        print()


class Day23(aoc.Challenge):

    DEBUG = True
    SUBMIT = {1: False, 2: False}

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=12521),
        aoc.TestCase(inputs=SAMPLE, part=2, want=44169),
    )

    def part2(self, parsed_input: InputType) -> int:
        pieces = parsed_input
        updated = []
        # Shift the bottom row down by two.
        for amphipod, x, y in pieces:
            if y == 2:
                y = 4
            updated.append((amphipod, x, y))
        # Add the extra two rows.
        updated.extend([
            ("D", 2, 2), ("C", 4, 2), ("B", 6, 2), ("A", 8, 2),
            ("D", 2, 3), ("B", 4, 3), ("A", 6, 3), ("C", 8, 3),
        ])
        pieces = tuple(sorted(updated))
        game = AmphipodGame(4, 10000000)
        return game.solve(pieces)

    def part1(self, parsed_input: InputType) -> int:
        pieces = parsed_input
        game = AmphipodGame(2, 100000)
        return game.solve(parsed_input)

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data.

                   1
           01234567890
          #############
        0 #...........#
        1 ###C#C#B#D###
        2   #D#A#B#A#
            #########
             2 4 6 8 
        """
        locations = []
        room_lines = puzzle_input.splitlines()[2:4]
        for y, line in enumerate(room_lines):
            for x, piece in enumerate(re.findall(r"[ABCD]", line)):
                locations.append((piece, (x + 1) * 2, y + 1))
        return tuple(sorted(locations))


if __name__ == "__main__":
    typer.run(Day23().run)

# vim:expandtab:sw=4:ts=4

#!/bin/python
"""Advent of Code: Day 23.

Optimizations needed:
* Never move C/D pieces in an x-direction away from final room.
* When possible, move piece direct to home-room and skip hallways.
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

SAMPLE = ["""\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""]
"""
           01234567890
          #############
        0 #...........#
        1 ###C#C#B#D###
        2   #D#A#B#A#
            #########
             2 4 6 8 
"""
InputType = list[int]

STEP_COST = {"A": 1, "B": 10, "C": 100, "D": 1000}
ROOM_X = (2,4,6,8)
VALID_HALLWAY = {(x, 0) for x in range(11) if x not in ROOM_X}
ALL_HALLWAY = {(x, 0) for x in range(11)}
ROOM_DEPTH = 2
ROOM = {
    name: {(ROOM_X[i], y) for y in range(1, ROOM_DEPTH+1)}
    for i, name in enumerate("ABCD")
}
ALL_ROOMS = set(itertools.chain.from_iterable(ROOM.values()))
ALL_SPOTS = ALL_HALLWAY | ALL_ROOMS
VALID_SPOTS = VALID_HALLWAY | ALL_ROOMS
VALID_FOR_TYPE = {n: VALID_HALLWAY | ROOM[n] for n in "ABCD"}


@functools.cache
def can_reach(start, occupied):
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
            if maybe in ALL_SPOTS:
                to_explore.add(maybe)
                steps[maybe] = steps[cur] + 1
    del steps[start]
    return {pos: cost for pos, cost in steps.items() if pos in VALID_SPOTS}


@functools.cache
def next_board(positions):
    next_positions = {}
    for piece in positions:
        for n, cost in valid_moves(piece, positions).items():
            assert n not in next_positions
            next_positions[n] = cost
    return next_positions


@functools.cache
def valid_moves(start, positions):
    amphi, loc = start[0], start[1:]
    locations = just_positions(positions)
    reachable = can_reach(loc, locations)
    room = ROOM[amphi]
    only_right = not any(
        (x, y) in room and piece != amphi
        for piece, x, y in positions
    )
    step_cost = STEP_COST[amphi]

    valid = reachable.keys()
    
    # If the amphipod is in the hallway, it will only move to its room, and only
    # if no other amphipod types are in that room.
    if loc in VALID_HALLWAY:
        if only_right and (vr := valid & room):
            valid = set([max(vr)])
        else:
            return {}
    # If the amphipod is in its room and there are no other types of amphipods in that
    # room, it will not move.
    elif loc in room and only_right:
        return {}
    # Otherwise, the amphipod will only move to the hallway..
    else:
        valid &= VALID_HALLWAY

    next_steps = {}
    other_pieces = list(positions)
    other_pieces.remove(start)
    for p, c in reachable.items():
        if p not in valid:
            continue
        energy = c * step_cost
        new_positions = tuple(sorted(other_pieces + [(amphi,) + p]))
        next_steps[new_positions] = energy
    return next_steps


def just_positions(pieces):
    return tuple(sorted(i[1:] for i in pieces))


def show(pieces):
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
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=12521),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=0),
    )

    def part1(self, parsed_input: InputType) -> int:
        pieces = parsed_input
        show(pieces)
        print(1)
        a = ("A", 2, 2)
        b = ("B", 9, 0)
        c = ("C", 2, 1)
        print(valid_moves(a, (a, b, c)))
        print(2)
        show((a, b, c))
        for board, cost in next_board((a,b,c)).items():
            print(cost)
            show(board)
        # return 0

        to_explore = set([pieces])
        cost = {pieces: 0}

        count = 0
        while to_explore and count < 100000:
            count += 1

            current = sorted(to_explore, key=lambda x: cost[x])[0]
            if count % 100 == 0:
                print(len(cost))
                print(cost[current])
                show(current)
            to_explore.remove(current)

            for board, move_cost in next_board(current).items():
                combined_cost = cost[current] + move_cost
                if board in cost and cost[board] <= combined_cost:
                    continue
                cost[board] = combined_cost
                to_explore.add(board)

        final_pos = tuple(sorted((amphi, x, y) for amphi, room in ROOM.items() for x, y in room))
        show(final_pos)
        return cost[final_pos]

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

          #############
        0 #...........#
        1 ###B#C#B#D###
        2   #A#D#C#A#
            #########
           0 2 4 6 8 10
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

#!/bin/python
"""Advent of Code: Day 23."""

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
        other_pieces = [p for p in positions if p != piece]
        costs = valid_moves(piece, positions)
        for move, cost in costs.items():
            piece_move = tuple([piece[0]] + list(move))
            next_positions[tuple(sorted(other_pieces + [piece_move]))] = cost
    return next_positions

@functools.cache
def valid_moves(start, positions):
    # When moving into a room, if the room does not have other types,
    # the only valid move is to move to the lowest position.
    # If the room does have other types, only move to the top position.
    # If starting in the hall, do not move to the hall.
    amphi, loc = start[0], start[1:]
    locations = just_positions(positions)
    reachable = can_reach(loc, locations)
    valid = reachable.keys() & VALID_FOR_TYPE[amphi]
    # If the piece is in its final room, it may not move into this room.
    maybe_room = valid & ROOM[amphi]
    if maybe_room:
        # If the piece can move to a final position, this is the only valid move.
        # TODO: ADD THIS
        if loc in ROOM[amphi]:
            valid -= ROOM[amphi]
        else:
            valid_for_room = max(valid & ROOM[amphi])
            valid -= ROOM[amphi]
            valid.add(valid_for_room)
    step_cost = STEP_COST[amphi]
    return {p: c * step_cost for p, c in reachable.items() if p in valid}


@functools.cache
def all_possible_next(current):
    possibilities = []
    positions = list(itertools.chain.from_iterable(current))
    for i, current in enumerate(positions):
        steps = can_reach(current, as_tuple(positions))
        for position, cost in steps.items():
            new_positions = positions.copy()
            new_positions[i] = position
            possibilities.append((cost, as_tuple(new_positions)))
            check_type(possibilities[-1][1])
    return possibilities


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
        # show(valid_moves(("B", 0, 0), (("C", 4,2),)).keys())
        # return 0
        for board, cost in next_board((("A", 0, 0),)).items():
            print(cost)
            show(board)
        return 0
        # for board, cost in next_board(pieces).items():
        #     print(cost)
        #     show(board)
        # return 0
        to_explore = set([pieces])
        cost = {pieces: 0}
        seen = set()

        count = 0
        while to_explore and count < 1000:
            count += 1
            current = sorted(to_explore, key=lambda x: cost[x])[0]
            to_explore.remove(current)
            seen.add(current)

            for board, move_cost in next_board(current).items():
                if board in seen:
                    continue
                cost[board] = cost[current] + move_cost
                to_explore.add(board)

        for b, c in cost.items():
            print(c)
            show(b)
        print(len(cost))
        return cost[final_pos]

    # Implement A*

    @staticmethod
    @functools.cache
    def heuristic(positions):
        cost = 0
        for i, pos in enumerate(positions):
            want_x = ((i//2)+1)*2
            want_y = max(1, pos[1])
            distance = abs(pos[0] - want_x) + abs(pos[1] - want_y)
            c = 10**(i//2)
            cost += c * distance
        return cost

    def move_to_room(positions):
        # check if a room is open for occupancy
        open_room = []
        for room in range(4):
            # back of room is open 
            if room*2+8 not in positions:
                open_room.append(room)
            # back of room is properly occupied and front of room is open
            elif (positions.index(room*2+8) // 2) == room and room*2+7 not in positions:
                open_room.append(room)
        if not open_room:
            return False

        for room in open_room:
            dest = room*2+8 if room*2+8 not in positions else room*2+7
            for i, loc in enumerate(positions):
                if (m := self.moves(positions, loc, dest)):
                    new_pos = list(positions)
                    new_pos[i] = dest
                    return 10 ** (i // 2) * m + self.cost(tuple(new_pos))





    @functools.cache
    def cost(self, positions):
        pass


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

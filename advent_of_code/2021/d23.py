#!/bin/python
"""Advent of Code: Day 23. Amphipod puzzle.

Solve for the minimum amount of energy needed to sort all the amphipods
into their proper rooms.

This solution uses A* to explore all possible moves.

For any board configuration, consider all possible moves for all pieces.

For any piece, evaluate all positions it can reach. Remove invalid hall positions.
Apply rules to reduce possible moves:
* A home-room is only valid if the home-room does not have any
  other types of amphipods.
* If a home-room is a valid and possible, that is the only valid move.
* If a piece is in the hallway and the home-room is not valid, the piece cannot move.
* If the piece is in the home-room and there are no other types, the piece cannot move.
* Otherwise, the piece must move from a room into the hallway.

The A* heuristic is the cost to move all pieces to their home room, assuming they can
move "through" each other. That's the x-distance for each piece plus the y-cost to
fit all the pieces into the room. To compute the y-cost, count how many pieces still
need to move into the room. The number of steps for N pieces from the hallway into the
room is TRIANGLE[N].

Pruning optimizations. Attempt to solve assuming more expensive pieces never more
further away from their room (x-distance). Solve with that assumption held for
"BCD" then "CD" then "D" then "".
"""

import functools
import itertools
import re

from lib import aoc

SAMPLE = """\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""
# Amphipod type ("ABCD") and (x, y) location.
Piece = tuple[str, int, int]
# Cartesian point.
Location = tuple[int, int]
# A board configuration - where all the Amphipods are located.
Board = tuple[Piece, ...]

# Cost of one step for each Amphipod.
STEP_COST = {"A": 1, "B": 10, "C": 100, "D": 1000}
# The "x" location of each Amphipod's room.
ROOM_X = dict(zip("ABCD", (2, 4, 6, 8)))
# Valid locations to stop in the hallway.
VALID_HALLWAY = {(x, 0) for x in range(11) if x not in ROOM_X.values()}
# Valid locations to move through the hallway.
ALL_HALLWAY = {(x, 0) for x in range(11)}
# Total y-steps required to move N pieces into a room.
TRIANGLE = {0: 0, 1: 1, 2: 3, 3: 6, 4: 10}


class AmphipodGame:
    """Amphipod Game."""

    def __init__(self, room_size: int):
        """Set up a game for a given room size."""
        self.room_size = room_size

        # The set of points for each "ABCD" room.
        self.room = {
            name: {(x, y) for y in range(1, room_size + 1)}
            for name, x in ROOM_X.items()
        }
        # The set of points of all four rooms.
        all_rooms = set(itertools.chain.from_iterable(self.room.values()))
        self.all_spots = ALL_HALLWAY | all_rooms
        self.valid_spots = VALID_HALLWAY | all_rooms
        self.final_pieces = tuple(sorted(
            (amphi, x, y) for amphi, room in self.room.items()
            for x, y in room
        ))

    def heuristic(self, pieces: Board) -> int:
        """Return the bounded min cost to complete this board.

        Compute the cost to solve this board, assuming pieces could move
        through each other.
        Total cost is the x-distance plus the y-steps needed to move N pieces into
        a room, for N pieces not in the room yet.
        """
        cost = 0
        out_of_room = {amphi: 0 for amphi in "ABCD"}
        for piece in pieces:
            amphi, x, y = piece
            want_x = ROOM_X[amphi]
            steps = abs(x - want_x)
            if x != want_x:
                steps += y
                out_of_room[amphi] += 1
            cost += STEP_COST[amphi] * steps
        for amphi, count in out_of_room.items():
            cost += STEP_COST[amphi] * TRIANGLE[count]
        return cost

    def neighbors(self, location: Location) -> list[Location]:
        """Return all neighboring locations which are on the board."""
        x0, y0 = location
        return [
            (x0 + dx, y0 + dy)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]
            if (x0 + dx, y0 + dy) in self.all_spots
        ]

    @functools.cache
    def possible_moves(self, piece: Piece, occupied: Board) -> dict[Location, int]:
        """Return Locations a Piece can reach and step count, considering other pieces.

        Given a Board configuration, find all the Locations a specific Piece
        can possibly move, including how many steps it would take.
        """
        # Use Dijksta's to explore the available moves.
        to_explore = set([piece])
        explored = set()
        cost = {piece: 0}

        while to_explore:
            location = sorted(to_explore, key=lambda x: cost[x])[0]
            to_explore.remove(location)
            explored.add(location)
            for next_location in self.neighbors(location):
                if next_location in explored or next_location in occupied:
                    continue
                to_explore.add(next_location)
                cost[next_location] = cost[location] + 1
        # Do not consider the starting location.
        del cost[piece]
        return {
            location: cost for location, cost in cost.items()
            if location in self.valid_spots
        }

    def valid_moves(self, piece: Piece, pieces: Board) -> dict[Board, int]:
        """Find all valid next-board configuration (and cost) for a given piece.

        Given a Board and a Piece to move, find all places that piece can move
        and return what the Board will look like with that move.

        This method takes into account all the various rules of the game,
        and applies some optimizations.
        """
        amphi, location = piece[0], piece[1:]
        locations = tuple(sorted(i[1:] for i in pieces))
        # Home room for this piece.
        room = self.room[amphi]
        # Check if the home room has any other Amphipod types.
        home_has_other = any(
            (x, y) in room and piece != amphi
            for piece, x, y in pieces
        )

        # If the amphipod is in its home room and there are
        # no other types of amphipods in that room, it will not move.
        if location in room and not home_has_other:
            return {}

        # If the amphipod is in the hallway, it will only move to the home room.
        # If the home room has other amphipods, it will not move.
        if location in VALID_HALLWAY and home_has_other:
            return {}

        move_costs = self.possible_moves(location, locations)
        valid = move_costs.keys()
        valid_to_home = valid & room

        # If the amphipod can move to the home room, always do that.
        if not home_has_other and valid_to_home:
            valid = set([max(valid_to_home)])
        # If the amphipod is in the hallway, it will only move to the home room.
        # That is checked in the prior clause. If that is not an option,
        # the amphipod will stay in the hallway without moving.
        elif location in VALID_HALLWAY:
            return {}
        # Otherwise, the amphipod will only move to the hallway..
        else:
            valid &= VALID_HALLWAY

            # Attempt to solve assuming no_extra_move pieces never move in
            # the direction away from their home room.
            if amphi in self.no_extra_move and location not in room:
                want_x = ROOM_X[amphi]
                if location[0] > want_x:
                    valid_x = range(want_x, location[0] + 1)
                else:
                    valid_x = range(location[0], want_x + 1)
                valid = {(x, y) for x, y in valid if x in valid_x}

        # Combine the valid movements of this Piece with the rest of
        # the Board to construct next board options.
        other_pieces = list(pieces)
        other_pieces.remove(piece)
        step_cost = STEP_COST[amphi]

        next_steps = {}
        for location in valid:
            energy = move_costs[location] * step_cost
            new_positions = tuple(sorted(other_pieces + [(amphi,) + location]))
            next_steps[new_positions] = energy
        return next_steps

    def next_board(self, pieces: Board) -> dict[Board, int]:
        """Return all possible moves (and cost) for a given Board."""
        next_positions = {}
        for piece in pieces:
            next_positions |= self.valid_moves(piece, pieces)
        return next_positions

    def solve_with_assumption(self, pieces: Board, assumption: str) -> int:
        """Solve the game with assumptions about some pieces."""
        self.no_extra_move = assumption

        # A* Search Algorithm.
        to_explore = set([pieces])
        cost = {pieces: 0}
        f_cost = {pieces: 0}

        while to_explore:
            # Find the board configuration with the lowest cost.
            current = sorted(to_explore, key=lambda x: f_cost[x])[0]
            to_explore.remove(current)

            if current == self.final_pieces:
                return cost[current]

            # Update the cost for every reachable adjacent configuration.
            for board, move_cost in self.next_board(current).items():
                combined_cost = cost[current] + move_cost
                # Not valid for Dijksta. Maybe or maybe not valid for A*. Unsure.
                # Works for the example and my input. Runs faster.
                # Makes the check outside the for loop unnecessary.
                # if board == self.final_pieces:
                #    return combined_cost
                # For Dijksta and possibly other inputs:
                # if board in cost and cost[board] <= combined_cost:
                #     continue
                # Not valid for Dijksta. Maybe valid for A*?
                # Works for the example and my input.
                if board in cost:
                    continue
                cost[board] = combined_cost
                # Dijksta: heuristic(x) = 0. A*: use Manhattan distance.
                f_cost[board] = combined_cost + self.heuristic(board)
                to_explore.add(board)

        return cost.get(self.final_pieces)

    def solve(self, pieces: Board) -> int:
        """Solve the game, attemping with decreasing assumptions.

        Start by assuming some pieces never need to move "away" from home-rooms
        and decrease assumptions until a solution is found.
        """
        for assumption in ("BCD", "CD", "D", ""):
            if solution := self.solve_with_assumption(pieces, assumption):
                return solution
        raise RuntimeError("unable to solve this board")

    def show(self, pieces: Board | list[Location]) -> None:
        """Print out a Board configuration."""
        locations = {}
        for piece in pieces:
            if len(piece) == 2:
                amphi = "X"
                x, y = piece
            elif len(piece) == 3:
                amphi, x, y = piece
            else:
                raise ValueError(repr(piece))
            locations[(x, y)] = amphi
        print("#" * 13)
        for y in range(self.room_size + 1):
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
    """Solve the cost of an Amphipod Game."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=12521),
        aoc.TestCase(inputs=SAMPLE, part=2, want=44169),
    )

    def part1(self, puzzle_input: Board) -> int:
        """Solve for room_size = 2."""
        return AmphipodGame(2).solve(puzzle_input)

    def part2(self, puzzle_input: Board) -> int:
        """Solve for room_size = 4."""
        pieces = puzzle_input

        # Add two rows of pieces.
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
        if self.testing:
            return AmphipodGame(4).solve_with_assumption(pieces, [])
        else:
            return AmphipodGame(4).solve(pieces)

    def input_parser(self, puzzle_input: str) -> Board:
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

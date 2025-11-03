#!/bin/python
"""Advent of Code, Day 20: Donut Maze."""
from __future__ import annotations

import collections
import functools
import itertools
import logging
import math
import re
import string

from lib import aoc

SAMPLE = [
    """\
         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z""",
    """\
                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P""",
    """\
             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     """,
]

LineType = int
InputType = list[LineType]
log = logging.info


class Day20(aoc.Challenge):
    """Day 20: Donut Maze."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=23),
        aoc.TestCase(part=1, inputs=SAMPLE[1], want=58),
        aoc.TestCase(part=2, inputs=SAMPLE[2], want=396),
    ]

    INPUT_PARSER = aoc.CoordinatesParser(origin_top_left=True)

    def part1(self, puzzle_input: InputType) -> int:
        # Outer portals
        o_left = min(c.real for c in puzzle_input.coords["."])
        o_right = max(c.real for c in puzzle_input.coords["."])
        o_top = min(c.imag for c in puzzle_input.coords["."])
        o_bottom = max(c.imag for c in puzzle_input.coords["."])
        # Inner portals
        centers = {
            coord: char for coord, char in puzzle_input.chars.items()
            if (
                char in string.ascii_uppercase + " "
                and o_left < coord.real < o_right
                and o_top < coord.imag < o_bottom
            )
        }
        i_left = max(c.real for c in centers) + 1
        i_right = min(c.real for c in centers) - 1
        i_top = max(c.imag for c in centers) + 1
        i_bottom = min(c.imag for c in centers) - 1
        # print("inner", i_left, i_right, i_top, i_bottom)
        # print(centers)

        portals_pos = collections.defaultdict(list)
        for chars, left, right, top, bottom in [
            (puzzle_input.chars, o_left, o_right, o_top, o_bottom),
            (centers, i_left, i_right, i_top, i_bottom),
        ]:
            for coord, char in chars.items():
                # print(coord, char)
                if char not in string.ascii_uppercase:
                    continue
                # if char in "BC":
                #     print("pre", coord, char, left, right, top, bottom)
                if coord.real == left - 1:
                    adjacent = coord - 1
                elif coord.real == right + 1:
                    adjacent = coord + 1
                elif coord.imag == top - 1:
                    adjacent = coord - 1j
                elif coord.imag == bottom + 1:
                    adjacent = coord + 1j
                else:
                    continue
                # if char in "BC":
                #     print("post", coord, char)
                if coord.real == left - 1 or coord.imag == top - 1:
                    key = chars[adjacent] + char
                else:
                    key = char + chars[adjacent]
                portals_pos[key].append(coord)
        # print(portals_pos)
        assert "AA" in portals_pos
        assert "ZZ" in portals_pos
        assert all(len(c) == 2 for k, c in portals_pos.items() if k not in ["AA", "ZZ"])

        portal_adjacent = lambda pos: next(
            p for p in puzzle_input.neighbors(pos) if p in puzzle_input.coords["."]
        )

        portal = {}
        start, end = None, None
        for key, pair in portals_pos.items():
            if key == "AA":
                start = pair[0]
            elif key == "ZZ":
                end = pair[0]
            else:
                a, b = pair
                portal[a] = portal_adjacent(b)
                portal[b] = portal_adjacent(a)
        # print(portal)

        todo = collections.deque([(0, start)])
        seen = {start}
        valid = set(puzzle_input.coords["."]) | set(portal) | {start, end}
        while todo:
            steps, pos = todo.popleft()
            if pos == end:
                return steps - 2
            steps += 1
            to_add = []
            for neighbor in puzzle_input.neighbors(pos):
                if neighbor in portal:
                    neighbor = portal[neighbor]
                if neighbor in valid and neighbor not in seen:
                    seen.add(neighbor)
                    to_add.append((steps, neighbor))
            todo.extend(to_add)
            # print(pos, steps, "add", to_add)


        # print("\n".join(["==="] + [f"{k}={v!r}" for k, v in locals().items()] + ["==="]))
        return None

    def part2(self, puzzle_input: InputType) -> int:
        # Outer portals
        o_left = min(c.real for c in puzzle_input.coords["."])
        o_right = max(c.real for c in puzzle_input.coords["."])
        o_top = min(c.imag for c in puzzle_input.coords["."])
        o_bottom = max(c.imag for c in puzzle_input.coords["."])
        # Inner portals
        centers = {
            coord: char for coord, char in puzzle_input.chars.items()
            if (
                char in string.ascii_uppercase + " "
                and o_left < coord.real < o_right
                and o_top < coord.imag < o_bottom
            )
        }
        i_left = max(c.real for c in centers) + 1
        i_right = min(c.real for c in centers) - 1
        i_top = max(c.imag for c in centers) + 1
        i_bottom = min(c.imag for c in centers) - 1
        # print("inner", i_left, i_right, i_top, i_bottom)
        # print(centers)

        portals_pos = collections.defaultdict(list)
        for chars, depth, left, right, top, bottom in [
            (puzzle_input.chars, -1, o_left, o_right, o_top, o_bottom),
            (centers, +1, i_left, i_right, i_top, i_bottom),
        ]:
            for coord, char in chars.items():
                # print(coord, char)
                if char not in string.ascii_uppercase:
                    continue
                # if char in "BC":
                #     print("pre", coord, char, left, right, top, bottom)
                if coord.real == left - 1:
                    adjacent = coord - 1
                elif coord.real == right + 1:
                    adjacent = coord + 1
                elif coord.imag == top - 1:
                    adjacent = coord - 1j
                elif coord.imag == bottom + 1:
                    adjacent = coord + 1j
                else:
                    continue
                # if char in "BC":
                #     print("post", coord, char)
                if coord.real == left - 1 or coord.imag == top - 1:
                    key = chars[adjacent] + char
                else:
                    key = char + chars[adjacent]
                portals_pos[key].append((coord, depth))

        portal_adjacent = lambda pos: next(
            p for p in puzzle_input.neighbors(pos) if p in puzzle_input.coords["."]
        )

        portal = {}
        start, end = None, None
        for key, pair in portals_pos.items():
            if key == "AA":
                start = portal_adjacent(pair[0][0])
            elif key == "ZZ":
                end = portal_adjacent(pair[0][0])
            else:
                (a, depth_a), (b, depth_b) = pair
                portal[a] = (portal_adjacent(b), depth_a)
                portal[b] = (portal_adjacent(a), depth_b)
        print(portal)

        todo = collections.deque([(0, 0, start)])
        seen = {(start, 0)}
        valid = set(puzzle_input.coords["."]) | set(portal)
        while todo:
            steps, depth, pos = todo.popleft()
            if pos == end and depth == 0:
                return steps
            steps += 1
            for neighbor in puzzle_input.neighbors(pos):
                n_depth = depth
                if neighbor in portal:
                    neighbor, depth_offset = portal[neighbor]
                    n_depth += depth_offset
                    if n_depth < 0:
                        continue
                if neighbor in valid and (neighbor, n_depth) not in seen:
                    seen.add((neighbor, n_depth))
                    todo.append((steps, n_depth, neighbor))
            # print(pos, steps, "add", to_add)


        # print("\n".join(["==="] + [f"{k}={v!r}" for k, v in locals().items()] + ["==="]))
        return None



# vim:expandtab:sw=4:ts=4

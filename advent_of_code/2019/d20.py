#!/bin/python
"""Advent of Code, Day 20: Donut Maze."""
import collections
import string
from typing import cast

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


class Day20(aoc.Challenge):
    """Day 20: Donut Maze."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=23),
        aoc.TestCase(part=1, inputs=SAMPLE[1], want=58),
        aoc.TestCase(part=2, inputs=SAMPLE[2], want=396),
    ]
    INPUT_PARSER = aoc.CoordinatesParserC()

    def get_portals(self, puzzle_input: aoc.Map, part_one: bool) -> dict[str, list[tuple[complex, int]]]:
        """Return a map of all the portals (their positions and in/out direction)."""
        real, imag = (lambda x: x.real), (lambda x: x.imag)
        # Outer edges
        edge_fns = [(min, real), (max, real), (min, imag), (max, imag)]
        # min|max(c.real|imag for c in puzzle_input.coords["."])
        outer = [f(g(c) for c in puzzle_input.coords["."]) for f, g in edge_fns]
        o_left, o_right, o_top, o_bottom = outer

        # Inner edges
        centers = {
            coord: char for coord, char in puzzle_input.chars.items()
            if (
                char in string.ascii_uppercase + " "
                and o_left < coord.real < o_right
                and o_top < coord.imag < o_bottom
            )
        }
        edge_fns = [
            (lambda x: max(x) + 1, real), (lambda x: min(x) - 1, real),
            (lambda x: max(x) + 1, imag), (lambda x: min(x) - 1, imag),
        ]
        inner = [f(g(c) for c in centers) for f, g in edge_fns]
        i_left, i_right, i_top, i_bottom = inner

        # Find all portals that lie along the edge.
        # Connect with the adjacent label to form the name.
        # Connect with the adjacent "." for the coordinate.
        portals_pos: dict[str, list[tuple[complex, int]]] = collections.defaultdict(list)
        for chars, depth, left, right, top, bottom in [
            (puzzle_input.chars, -1, o_left, o_right, o_top, o_bottom),
            (centers, +1, i_left, i_right, i_top, i_bottom),
        ]:
            # Part one doesn't use a depth.
            if part_one:
                depth = 0
            for coord, char in chars.items():
                if char not in string.ascii_uppercase:
                    continue
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
                if coord.real == left - 1 or coord.imag == top - 1:
                    key = chars[adjacent] + char
                else:
                    key = char + chars[adjacent]
                portals_pos[key].append((coord, depth))
        return portals_pos

    def build_map(
            self, puzzle_input: aoc.Map, part_one: bool
        ) -> tuple[complex, complex, dict[complex, tuple[complex, int]]]:
        """Return the start, end, portal map: coordinate to coordinate with depth change."""
        portal_adjacent = lambda pos: next(
            p for p in puzzle_input.neighbors(pos) if p in puzzle_input.coords["."]
        )

        portals_pos = self.get_portals(puzzle_input, part_one)
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

        return start, end, portal

    def solver(self, puzzle_input: aoc.Map, part_one: bool) -> int:
        """Return the number of steps required to solve the maze."""
        start, end, portal = self.build_map(puzzle_input, part_one)

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
                    # We can go "inside" indefinitely but cannot go outside beyond "0".
                    if n_depth < 0:
                        continue
                if neighbor in valid and (neighbor, n_depth) not in seen:
                    seen.add((neighbor, n_depth))
                    todo.append((steps, n_depth, neighbor))

        raise RuntimeError("No solution found.")


# vim:expandtab:sw=4:ts=4

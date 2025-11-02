#!/bin/python
"""Advent of Code, Day 18: Many-Worlds Interpretation."""
import collections
import string
import typing

from lib import aoc

SAMPLE = [
    """\
#########
#b.A.@.a#
#########""",
    """\
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################""",
    """\
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################""",
    """\
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################""",
    """\
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################""",
    """\
#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######""",
    """\
###############
#d.ABC.#.....a#
######...######
######.@.######
######...######
#b.....#.....c#
###############""",
    """\
#############
#DcBa.#.GhKl#
#.###...#I###
#e#d#.@.#j#k#
###C#...###J#
#fEbA.#.FgHi#
#############""",
    """\
#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba...BcIJ#
#####.@.#####
#nK.L...G...#
#M###N#H###.#
#o#m..#i#jk.#
#############""",
]


class Day18(aoc.Challenge):
    """Day 18: Many-Worlds Interpretation. Collect all keys in a maze, unlocking doors to explore farther."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=8),
        aoc.TestCase(part=1, inputs=SAMPLE[1], want=86),
        aoc.TestCase(part=1, inputs=SAMPLE[2], want=132),
        aoc.TestCase(part=1, inputs=SAMPLE[3], want=136),
        aoc.TestCase(part=1, inputs=SAMPLE[4], want=81),
        aoc.TestCase(part=2, inputs=SAMPLE[5], want=8),
        aoc.TestCase(part=2, inputs=SAMPLE[6], want=24),
        aoc.TestCase(part=2, inputs=SAMPLE[7], want=32),
        aoc.TestCase(part=2, inputs=SAMPLE[8], want=72),
    ]
    INPUT_PARSER = aoc.parse_one_str

    def build_edges(self, data: aoc.Map, nodes: dict[str, complex]) -> dict[str, dict[str, tuple[int, int]]]:
        """Return a map of all {start|key}-key pairs with the min distance and blocking doors."""
        edges: dict[str, dict[str, tuple[int, int]]] = {node: {} for node in nodes}
        # For each starting point, explore depth first to discover paths to keys.
        for start, pos in nodes.items():
            todo = collections.deque([(0, pos, 0)])
            seen = {pos}
            while todo:
                steps, pos, doors = todo.popleft()
                char = typing.cast(str, data.chars[pos])
                if char.islower() and char != start:
                    edges[start][char] = (steps, doors)
                steps += 1
                for n in data.neighbors(pos):
                    if n in seen:
                        continue
                    seen.add(n)
                    char = typing.cast(str, data.chars[n])
                    new_doors = doors
                    if char.isupper():
                        new_doors |= 1 << string.ascii_uppercase.index(char)
                    todo.append((steps, n, new_doors))
        return edges

    def solve_for(self, starts: list[str], edges: dict[str, dict[str, tuple[int, int]]]) -> int:
        """Return the minimum steps needed to collect all the keys."""
        # pylint: disable=too-many-locals
        num_keys = len(set(edges) - set(starts))
        todo: collections.deque[tuple] = collections.deque()
        todo.append((0, *starts, 0))
        smallest = int(1e9)
        seen: dict[tuple, int] = {}

        while todo:
            steps, *positions, got = todo.pop()
            if steps > smallest:
                continue
            if got.bit_count() == num_keys:
                smallest = min(steps, smallest)
                continue
            for bot, pos in enumerate(positions):
                for key, (distance, doors) in edges[pos].items():
                    n_key = 1 << string.ascii_lowercase.index(key)
                    new_steps = steps + distance
                    if n_key & got or doors & ~got or new_steps > smallest:
                        continue
                    new_got = got | n_key
                    new_positions = positions.copy()
                    new_positions[bot] = key
                    if (*new_positions, new_got) in seen and seen[*new_positions, new_got] <= new_steps:
                        continue
                    seen[*new_positions, new_got] = new_steps
                    todo.append((new_steps, *new_positions, new_got))

        return smallest

    def solver(self, puzzle_input: str, part_one: bool) -> int:
        if not part_one:
            data = aoc.CoordinatesParser(ignore=None, origin_top_left=True).parse(puzzle_input)

            center = data.coords["@"].copy().pop()
            data.update(center, "#")
            for i, n in enumerate([complex(-1, -1), complex(1, -1), complex(1, 1), complex(-1, 1)]):
                data.update(center + n, str(i))
            for n in data.neighbors(center):
                data.update(n, "#")

            puzzle_input = aoc.render_char_map(
                typing.cast(dict[complex, str], data.chars), data.max_y + 1, data.max_x + 1
            )

        data = aoc.CoordinatesParser(ignore="#", origin_top_left=True).parse(puzzle_input)
        starts = list("@" if part_one else "0123")
        nodes: dict[str, complex] = {
            char: pos
            for pos, char in typing.cast(dict[complex, str], data.chars).items()
            if char.islower() or char in "@0123"
        }
        return self.solve_for(starts, self.build_edges(data, nodes))

# vim:expandtab:sw=4:ts=4

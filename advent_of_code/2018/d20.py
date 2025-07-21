#!/bin/python
"""Advent of Code, Day 20: A Regular Map."""

import collections
import functools

from lib import aoc


class Day20(aoc.Challenge):
    """Day 20: A Regular Map."""

    TESTS = [
        aoc.TestCase(part=1, inputs="^WNE$", want=3),
        aoc.TestCase(part=1, inputs="^ENWWW(NEEE|SSE(EE|N))$", want=10),
        aoc.TestCase(part=1, inputs="^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$", want=18),
        aoc.TestCase(part=1, inputs="^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$", want=23),
        aoc.TestCase(part=1, inputs="^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$", want=31),
        aoc.TestCase(part=2, inputs="", want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_one_str

    def solver(self, puzzle_input: str, part_one: bool) -> int:
        """Walk a regex to explore a map."""
        position = complex(0, 0)
        graph = collections.defaultdict(set)
        puzzle_input = puzzle_input.removeprefix("^").removesuffix("$")

        @functools.cache
        def explore(pos: complex, instructions: str) -> None:
            """Explore a segment of the map, with support for branching."""
            for idx, char in enumerate(instructions):
                if char in aoc.COMPASS_DIRECTIONS:
                    next_pos = pos + aoc.COMPASS_DIRECTIONS[char]
                    graph[pos].add(next_pos)
                    graph[next_pos].add(pos)
                    pos = next_pos
                else:
                    assert char == "("
                    depth = 1
                    splits = []
                    i = 0
                    for i, x in enumerate(instructions[idx + 1:], idx + 1):
                        if x == "(":
                            depth += 1
                        elif x == ")":
                            depth -= 1
                            if depth == 0:
                                break
                        elif x == "|" and depth == 1:
                            splits.append(i)
                    chunks = [instructions[a + 1:b] for a, b in zip([idx] + splits, splits + [i])]
                    for chunk in chunks:
                        explore(pos, chunk + instructions[i + 1:])
                    return

        # Explore the map, building a graph.
        explore(position, puzzle_input)

        # Walk the graph, breadth first, and track doors.
        todo: collections.deque[tuple[int, complex]] = collections.deque()
        todo.append((0, complex(0, 0)))
        added = {complex(0, 0), }
        far = set()
        while todo:
            steps, pos = todo.popleft()
            if steps >= 1000:
                far.add(pos)
            for adjacent in graph[pos]:
                if adjacent in added:
                    continue
                added.add(adjacent)
                todo.append((steps + 1, adjacent))
        if part_one:
            return steps
        return len(far)

# vim:expandtab:sw=4:ts=4

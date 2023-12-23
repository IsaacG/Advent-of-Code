#!/bin/python
"""Advent of Code, Day 23: A Long Walk."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""

LineType = int
InputType = list[LineType]


class Day23(aoc.Challenge):
    """Day 23: A Long Walk."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=94),
        aoc.TestCase(inputs=SAMPLE, part=2, want=154),
    ]

    INPUT_PARSER = aoc.parse_ascii_char_map(lambda x: x)

    def part1(self, parsed_input: InputType) -> int:
        board = parsed_input
        min_x, min_y, max_x, max_y = aoc.bounding_coords(board)
        start = next(i for i, char in board.items() if i.imag == min_y and char == ".")
        end = next(i for i, char in board.items() if i.imag == max_y and char == ".")

        paths = []
        paths.append((start, {start}))
        max_path = 0
        while paths:
            current, seen = paths.pop()
            if current == end:
                new_len = len(seen)
                if new_len > max_path:
                    max_path = new_len


            char = board[current]
            if char in aoc.ARROW_DIRECTIONS:
                next_pos = current + aoc.ARROW_DIRECTIONS[char]
                assert board[next_pos] != "#"
                if next_pos not in seen:
                    paths.append((next_pos, seen | {next_pos}))
            else:
                for next_pos in aoc.neighbors(current):
                    if board.get(next_pos, "#") != "#" and next_pos not in seen:
                        paths.append((next_pos, seen | {next_pos}))

        return max_path - 1

        assert len(completed) == len(set(completed))
        print([len(i) for i in completed])
        if False:
            for y in range(max_y + 1):
                line = []
                for x in range(max_x + 1):
                    pos = complex(x, y)
                    if pos in seen:
                        line.append("O")
                    else:
                        line.append(board[pos])
                print("".join(line))
            print()

        # Do not count start
        return 0


        print(f"{parsed_input!r}")
        return 0

    def part2(self, parsed_input: InputType) -> int:
        board = {pos for pos, char in parsed_input.items() if char != "#"}
        min_x, min_y, max_x, max_y = aoc.bounding_coords(board)
        start = next(i for i in board if i.imag == min_y)
        end = next(i for i in board if i.imag == max_y)

        forks = {coord for coord in board if len(set(aoc.neighbors(coord)) & board) > 2}
        forks.add(start)
        destinations = forks | {end}

        longest_dist = collections.defaultdict(lambda: collections.defaultdict(int))

        for coord in forks:
            neighbors = set(aoc.neighbors(coord)) & board

            for current in neighbors:
                steps = 1
                prior = coord

                while current not in destinations:
                    steps += 1
                    options = set(aoc.neighbors(current)) & board 
                    assert len(options) == 2
                    current, prior = next(i for i in options if i != prior), current

                dist = max(steps, longest_dist[coord][current])
                longest_dist[coord][current] = dist
                longest_dist[current][coord] = dist

        labels = {coord: idx for idx, coord in enumerate(destinations)}
        longest_dist = {
            labels[start]: {
                labels[end]: distance
                for end, distance in data.items()
            }
            for start, data in longest_dist.items()
        }
        start, end = labels[start], labels[end]

        # Prune off side branches which do not lead to the end.
        if False:
            for coord in longest_dist:
                for neighbor in list(longest_dist[coord]):
                    if coord == end or neighbor == end:
                        continue
                    seen = {neighbor}
                    todo = {neighbor}
                    while todo:
                        cur = todo.pop()
                        for next_coord in longest_dist[cur]:
                            if next_coord not in seen and next_coord != coord:
                                todo.add(next_coord)
                                seen.add(next_coord)
                    if end not in seen:
                        del longest_dist[coord][neighbor]

        max_path = 0
        paths = []
        paths.append((0, start, {start}))
        max_seen = collections.defaultdict(int)

        penultimate_pos, penultimate_distance = list(longest_dist[end].items())[0]
        end = penultimate_pos

        for src, data in longest_dist.items():
            # print(f"{src} -> {list(data)}")
            pass

        while paths:
            steps, current, seen = paths.pop()
            if current == end:
                if steps > max_path:
                    max_path = steps
                continue

            for next_pos, distance in longest_dist[current].items():
                if next_pos not in seen:
                    next_steps = steps + distance
                    next_seen = seen | {next_pos}

                    # Stop exploring a path if we explored it and found a longer version.
                    # This balloons memory usage in a bad way.
                    # if len(next_seen) < 20:
                    #     if max_seen[next_pos, next_seen] > next_steps:
                    #         continue
                    #     max_seen[next_pos, next_seen] = next_steps

                    paths.append((next_steps, next_pos, next_seen))

        return max_path + penultimate_distance

# vim:expandtab:sw=4:ts=4

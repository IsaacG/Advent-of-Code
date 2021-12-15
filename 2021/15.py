#!/bin/python
"""Advent of Code: Day 15."""

import collections
import functools
import math
import re
import time
import sys

import typer

from lib import aoc

InputType = list[int]
SAMPLE = ["""\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""]


class Day15(aoc.Challenge):

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=40),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=315),
    )

    def part1(self, lines: InputType) -> int:
        graph = lines
        costs = {0: 0}
        visited = set()
        todo = set([0])
        while todo:
            current = sorted(todo, key=lambda x: costs[x])[0]
            todo.remove(current)
            visited.add(current)
            neighbors = [current + d for d in (1, -1, 1j, -1j) if current + d in graph and current + d not in visited]
            todo.update(neighbors)
            for neighbor in neighbors:
                cost = costs[current] + graph[neighbor]
                if neighbor not in costs or costs[neighbor] > cost:
                    costs[neighbor] = cost
        return costs[self.end]

    def part2(self, lines: InputType) -> int:
        graph = lines
        full_graph = {}
        for x in range(5):
            for y in range(5):
                for point, val in graph.items():
                    point = (x * (self.width+1) + point.real) + (y * (self.height+1) + point.imag) * 1j
                    val = ((val + x + y - 1) % 9) + 1
                    full_graph[point] = val
        graph = full_graph
        end = max(p.real for p in graph) + max(p.imag for p in graph) * 1j

        costs = {0: 0}
        visited = set()
        todo = set([0])
        while todo:
            current = sorted(todo, key=lambda x: costs[x])[0]
            todo.remove(current)
            visited.add(current)
            neighbors = [current + d for d in (1, -1, 1j, -1j) if current + d in graph and current + d not in visited]
            todo.update(neighbors)
            for neighbor in neighbors:
                cost = costs[current] + graph[neighbor]
                if neighbor not in costs or costs[neighbor] > cost:
                    costs[neighbor] = cost
        return costs[end]

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        lines = puzzle_input.splitlines()
        self.width = len(lines[0]) - 1
        self.height = len(lines) - 1
        self.end = self.width + self.height * 1j
        return {
            x + y * 1j: int(val)
            for y, line in enumerate(lines)
            for x, val in enumerate(line)
        }

if __name__ == "__main__":
    typer.run(Day15().run)

# vim:expandtab:sw=4:ts=4

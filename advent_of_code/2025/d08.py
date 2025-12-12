#!/bin/python
"""Advent of Code, Day 8: Playground."""
import collections
import heapq
import itertools
import math
from lib import aoc

SAMPLE = """\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""


class Day08(aoc.Challenge):
    """Day 8: Playground."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=40),
        aoc.TestCase(part=2, inputs=SAMPLE, want=25272),
    ]

    def solver(self, puzzle_input: list[list[int]], part_one: bool) -> int:
        """Return stats from connecting junction boxes into circuits using minimum distances."""
        boxes = [tuple(i) for i in puzzle_input]
        distances = [(math.dist(a, b), a, b) for a, b in itertools.combinations(boxes, 2)]
        heapq.heapify(distances)
        circuits = []

        def add_connection(new: set[int]) -> set[int]:
            """Add a new connection to the collection of circuits. Simplified Disjoint Set Union."""
            for a in list(circuits):
                if a & new:
                    circuits.remove(a)
                    a |= new
                    return add_connection(a)
            circuits.append(new)
            return new

        if part_one:
            for _ in range(10):
                _, a, b = heapq.heappop(distances)
                print((a, b, math.dist(a, b)))
            return
            for _ in range(10 if self.testing else 1000):
                _, a, b = heapq.heappop(distances)
                add_connection({a, b})
            sizes = sorted(len(i) for i in circuits)[-3:]
            return math.prod(sizes)

        total_boxes = len(boxes)
        while distances:
            _, a, b = heapq.heappop(distances)
            circuit = add_connection({a, b})
            if len(circuit) == total_boxes:
                return a[0] * b[0]
        raise RuntimeError("Not solved")

# vim:expandtab:sw=4:ts=4

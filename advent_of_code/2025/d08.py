#!/bin/python
"""Advent of Code, Day 8: Playground."""
import collections
import heapq
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
        distances = [
            (math.dist(a, b), idx_a, idx_b)
            for idx_a, a in enumerate(boxes)
            for idx_b, b in enumerate(boxes)
            if idx_a < idx_b
        ]
        heapq.heapify(distances)
        dsu = aoc.DisjointSet()

        if part_one:
            for _ in range(10 if self.testing else 1000):
                _, a, b = heapq.heappop(distances)
                aoc.dsu_add_pair(dsu, a, b)
            sizes = [
                count for i, count in collections.Counter(
                    aoc.dsu_find(dsu, i) for i in dsu
                ).most_common(3)
            ]
            return math.prod(sizes)

        total_boxes = len(boxes)
        while distances:
            _, a, b = heapq.heappop(distances)
            root = aoc.dsu_add_pair(dsu, a, b)
            if dsu[root][1] == total_boxes:
                return boxes[a][0] * boxes[b][0]
        raise RuntimeError("Not solved")

# vim:expandtab:sw=4:ts=4

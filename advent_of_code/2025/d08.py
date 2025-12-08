#!/bin/python
"""Advent of Code, Day 8: Playground."""
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
        boxes = set(tuple(i) for i in puzzle_input)
        distances = sorted(
            (math.dist(a, b), a, b)
            for a in boxes
            for b in boxes
            if a < b
        )

        if part_one:
            circuits = [{a, b} for _, a, b in distances[:10 if self.testing else 1000]]
            circuits = aoc.merge_disjoint_sets(circuits)
            return math.prod(sorted((len(i) for i in circuits), reverse=True)[:3])

        total_boxes = len(boxes)
        circuits = list[set[tuple[int, ...]]]()

        for _, box_a, box_b in distances:
            changed = aoc.add_to_disjoint_sets(circuits, {box_a, box_b})
            if len(changed) == total_boxes:
                return box_a[0] * box_b[0]
        raise RuntimeError("Not solved")

# vim:expandtab:sw=4:ts=4

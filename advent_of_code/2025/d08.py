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

        circuits = list[set[tuple[int, ...]]]()
        total_boxes = len(boxes)
        p1_stop = 10 if self.testing else 1000

        for idx, (_, box_a, box_b) in enumerate(distances):
            if part_one and idx == p1_stop:
                return math.prod(sorted((len(i) for i in circuits), reverse=True)[:3])
            circuit_a = next((i for i in circuits if box_a in i), {box_a, })
            circuit_b = next((i for i in circuits if box_b in i), {box_b, })
            if circuit_a == circuit_b:
                continue
            if len(circuit_a) > 1:
                circuits.remove(circuit_a)
            if len(circuit_b) > 1:
                circuits.remove(circuit_b)
            combined = circuit_a | circuit_b
            circuits.append(combined)
            if len(combined) == total_boxes:
                return box_a[0] * box_b[0]
        raise RuntimeError("Not solved")

# vim:expandtab:sw=4:ts=4

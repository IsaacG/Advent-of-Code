#!/usr/bin/env python
"""2019 Day 3: Crossed Wires. Compute where wires cross and find the min cost of a crossing."""

from lib import aoc

DIRS = aoc.LETTER_DIRECTIONS

def solve(data: list[str], part: int) -> int:
    """Walk the two wires.

    For wire one, save locations visited and steps.
    For wire two, on intersection, save `cost`.
    Return min cost.

    Wire cross cost p1: combined step count.
    Wire cross cost p2: Manhatten distance.
    """
    spots = {}
    intersections = set()

    def save_steps(cur, steps):
        if cur not in spots:
            spots[cur] = steps

    def save_cost(cur, steps):
        if cur in spots:
            if part == 1:
                # Manhatten distance.
                cost = abs(int(cur.real)) + abs(int(cur.imag))
            else:
                # Combined steps.
                cost = spots[cur] + steps
            intersections.add(cost)

    def walk_wire(wire, func):
        steps = 0
        cur = 0
        for piece in wire:
            direction = DIRS[piece[0]]
            count = int(piece[1:])
            for _ in range(count):
                steps += 1
                cur += direction
                func(cur, steps)

    walk_wire(data[0], save_steps)
    walk_wire(data[1], save_cost)
    return min(intersections)

def input_parser(data: str):
    return [line.split(',') for line in data.split('\n')]

SAMPLES = [
    'R8,U5,L5,D3\nU7,R6,D4,L4',
    'R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83',
    'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7',
]
TESTS = (
    (1, SAMPLES[0], 6),
    (1, SAMPLES[1], 159),
    (1, SAMPLES[2], 135),
    (2, SAMPLES[0], 30),
    (2, SAMPLES[1], 610),
    (2, SAMPLES[2], 410),
)

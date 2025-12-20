#!/bin/python
"""Advent of Code, Day 20: Particle Swarm."""

import collections


def distance(vals: tuple[int, ...]) -> int:
    """Return the Manhatten distance of a coordinate."""
    return sum(abs(i) for i in vals)


def solve(data: list[list[int]], part: int) -> int:
    """Return particle metadata.

    Part one: return which particle will be farthest from the origin.
    Part two: return the number of particles after collisions.
    """
    pos, vel, acc = [
        {idx: tuple(vals[i * 3:(i + 1) * 3]) for idx, vals in enumerate(data)}
        for i in range(3)
    ]
    # Simulate some ticks for collision removal. 40 is the min that works for my input.
    for _ in range(0 if part == 1 else 100):
        # Count positions. Any position with multiple particles is a collision.
        counts = collections.Counter(pos.values())
        collisions = {p for p, count in counts.items() if count > 1}
        # Remove particles which collided.
        pos = {idx: p for idx, p in pos.items() if p not in collisions}
        vel = {idx: v for idx, v in vel.items() if idx in pos}
        # Update velocity then position.
        vel = {idx: tuple(vel[idx][dim] + acc[idx][dim] for dim in range(3)) for idx in pos}
        pos = {idx: tuple(pos[idx][dim] + vel[idx][dim] for dim in range(3)) for idx in pos}

    if part == 2:
        return len(pos)
    # Sort remaining particles by acceleration then velocity (Manhatten distance).
    slowest = sorted((distance(acc[idx]), distance(vel[idx]), idx) for idx in pos)
    return slowest[0][2]


SAMPLE = [
    """\
p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>""",  # 29
    """\
p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>""",
]
TESTS = [(1, SAMPLE[0], 0), (2, SAMPLE[1], 1)]
# vim:expandtab:sw=4:ts=4

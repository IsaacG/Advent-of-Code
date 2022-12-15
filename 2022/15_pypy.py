#!/usr/bin/pypy3
"""Advent of Code, Day 15: Beacon Exclusion Zone. mypy benchmark version."""

import re
import time


def part2():
    t1 = time.perf_counter()
    dims = 4000000
    sensor_tuples = []
    RE = re.compile(r"-?\d+")

    with open("data/15.txt") as f:
        for line in f:
            sx, sy, bx, by = [int(i) for i in RE.findall(line)]
            sensor_tuples.append([sx, sy, abs(sx - bx) + abs(sy - by)])
    sensor_tuples.sort()
    t2 = time.perf_counter()
    print("Setup:", (t2 - t1) * 1000)

    t1 = time.perf_counter()
    for cury in range(dims + 1):
        curx = 0
        for sensor_x, sensor_y, sensor_dist in sensor_tuples:
            y_dist = abs(sensor_y - cury)
            point_dist = abs(sensor_x - curx) + y_dist
            if point_dist <= sensor_dist:
                curx = sensor_x + sensor_dist - y_dist + 1
        if curx <= dims:
            t2 = time.perf_counter()
            print("Solve:", (t2 - t1) * 1000)
            print(f"Solved!!! {curx, cury}")
            print(curx * 4000000 + cury)
            print(curx * 4000000 + cury == 13134039205729)

if __name__ == "__main__":
    part2()

# vim:expandtab:sw=4:ts=4

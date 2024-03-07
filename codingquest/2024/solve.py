#!/bin/python
"""CodingQuest.io solver."""
from __future__ import annotations

import collections
import dataclasses
import functools
import itertools
import hashlib
import math
import pathlib
import queue
import re
import statistics
import string
import textwrap
import time
from typing import Optional

import click
import more_itertools
import png  # type: ignore
import requests  # type: ignore

# Regex used to detect an interger (positive or negative).
NUM_RE = re.compile("-?[0-9]+")
INPUT_ENDPOINT = "https://codingquest.io/api/puzzledata"
COLOR_SOLID = '█'
COLOR_EMPTY = ' '


def purchase_tickets(data: str) -> int:
    """Day 28: Return the cheapest airline cost."""
    pattern = re.compile(r"(\S+): (\S+) (\d+)")
    negative = ("Rebate", "Discount")
    costs = collections.defaultdict(int)
    for line in data.splitlines():
        airline, item_type, cost = pattern.fullmatch(line).groups()
        costs[airline] += int(cost) * (-1 if item_type in negative else 1)
    return min(costs.values())


def broken_firewall(data: str) -> str:
    """Day 29."""
    ship, customer = 0, 0
    for line in data.splitlines():
        datum = [int(a + b, 16) for a, b in more_itertools.chunked(line, 2)]
        length = datum[2] * 256 + datum[3]
        addrs = (datum[12:16], datum[16:20])
        if any(addr[:2] == [192, 168] and all(i <= 254 for i in addr[:2]) for addr in addrs):
            ship += length
        elif any(addr[:2] == [10, 0] and all(i <= 254 for i in addr[:2]) for addr in addrs):
            customer += length
    return f"{ship}/{customer}"


def hotel_door_code(data: str) -> str:
    """Day 30."""
    pixels = [
        pixel
        for pixel, chunk in zip(itertools.cycle([COLOR_EMPTY, COLOR_SOLID]), data.split())
        for _ in range(int(chunk))
    ]
    return "\n".join("".join(i) for i in more_itertools.chunked(pixels[0:8000], 100))


def closest_star_systems(data: str) -> float:
    """Day 31."""
    coords = {
        tuple(float(i) for i in line.split()[-3:])
        for line in data.splitlines()[1:]
    }
    return round(
        min(
            math.sqrt((x2 - x1)**2 + (y2 - y1)**2 +  (z2 - z1)**2)
            for (x1, y1, z1), (x2, y2, z2) in itertools.combinations(coords, 2)
        ), 3
    )



FUNCS = {
    28: purchase_tickets,
    29: broken_firewall,
    30: hotel_door_code,
    31: closest_star_systems,
}


@click.command()
@click.option("--day", type=int, required=False)
@click.option("--data", type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path))
def main(day: int | None, data: Optional[pathlib.Path]):
    """Run the solver for a specific day."""
    if not day:
        day = max(FUNCS)
    if day not in FUNCS:
        print(f"Day {day:02} not solved.")
        return
    if not data:
        data = pathlib.Path(f"input/{day:02}.txt")
        if not data.exists():
            response = requests.get(INPUT_ENDPOINT, params={"puzzle": f"{day:02}"})
            response.raise_for_status()
            data.write_text(response.text)
    start = time.perf_counter_ns()
    got = FUNCS[day](data.read_text().rstrip())
    if isinstance(got, str) and "\n" in got:
        got = "\n" + got
    end = time.perf_counter_ns()
    delta = end - start
    units = ["ns", "us", "ms", "s"]
    unit = ""
    for i in units:
        unit = i
        if delta < 1000:
            break
        delta //= 1000

    print(f"Day {day:02} ({delta:4}{unit:<2}): {got}")


if __name__ == "__main__":
    main()

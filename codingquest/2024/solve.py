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
    costs = collections.defaultdict(int)
    for line in data.splitlines():
        airline, item = line.split(": ")
        item_type, cost = item.split()
        cost = int(cost)
        if item_type in ("Rebate", "Discount"):
            cost *= -1
        costs[airline] += cost
    return min(costs.values())


FUNCS = {
    28: purchase_tickets,
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

#!/bin/python
"""CodingQuest.io solver."""
from __future__ import annotations

import collections
import dataclasses
import functools
import ipaddress
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
    ranges = (
        (ipaddress.IPv4Address("192.168.0.0"), ipaddress.IPv4Address("192.168.254.254")),
        (ipaddress.IPv4Address("10.0.0.0"), ipaddress.IPv4Address("10.0.254.254")),
    )
    counts = [0] * len(ranges)
    for line in data.splitlines():
        datum = [int(a + b, 16) for a, b in more_itertools.chunked(line, 2)]
        length = datum[2] * 256 + datum[3]
        addrs = [
            ipaddress.IPv4Address(bytes(int(p) for p in parts))
            for parts in (datum[12:16], datum[16:20])
        ]
        for idx, (low, high) in enumerate(ranges):
            if any(low <= addr <= high for addr in addrs):
                counts[idx] += length
    return "/".join(str(i) for i in counts)


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


def busy_moon_rovers(data: str) -> int:
    chart, log = (i.splitlines() for i in data.split("\n\n"))
    dsts = chart[0].split()
    graph = {}
    for line in chart[1:]:
        src, *distances = line.split()
        graph[src] = {
            dst: int(distance)
            for dst, distance in zip(dsts, distances, strict=True)
        }
    result = 0
    for line in log:
        locations = line.split(": ")[1].split(" -> ")
        result += sum(graph[src][dst] for src, dst in zip(locations, locations[1:]))
    return result
        

def playfair(data: str) -> str:
    """Day 33: Playfair Cipher."""
    chunks = data.split("\n\n")
    key, message = (chunk.split(": ")[1] for chunk in data.split("\n\n"))
    key += string.ascii_lowercase
    # Set up the cipher block
    letter_coord = {}
    coord_letter = {}
    count = 0
    for letter in key.replace("j", ""):
        if letter in letter_coord:
            continue
        coord = (count % 5, count // 5)
        letter_coord[letter] = coord
        coord_letter[coord] = letter
        count += 1

    # Decrypt the message
    full_result = []
    for word in message.split():
        result = []
        for chars in  more_itertools.chunked(word, 2):
            (x_a, y_a), (x_b, y_b) = (letter_coord[char] for char in chars)
            # Look left/up when letters are on the same column/row.
            dx, dy = (4 * (y_a == y_b)), (4 * (x_a == x_b))
            letters = [
                coord_letter[(x_b + dx) % 5, (y_a + dy) % 5],
                coord_letter[(x_a + dx) % 5, (y_b + dy) % 5],
            ]
            # For some reason, letters need swapping when on the same row.
            if y_a == y_b:
                letters.reverse()
            result.extend(letters)
        full_result.append("".join(result))

    return " ".join(full_result)


def the_purge(data: str) -> int:
    """Day 34: count space freed upon file deletion."""
    # Initialize variables.
    folder_size = collections.defaultdict(int)
    file_deletion = collections.defaultdict(int)
    folder_deletion = set()
    folder_children = collections.defaultdict(set)
    delete_re = re.compile(r"delete|temporary")
    dir_entry_re = re.compile(r" - ([^ ]+) \[FOLDER (\d+)\]")
    file_entry_re = re.compile(r" - ([^ ]+) (\d+)")

    # Parse the input and populate the data structures.
    cur_folder = 0
    for line in data.splitlines():
        if line.startswith("Folder: "):
            cur_folder = int(line.removeprefix("Folder: "))
        elif m := dir_entry_re.fullmatch(line):
            folder_num = int(m.group(2))
            folder_children[cur_folder].add(folder_num)
            if delete_re.search(m.group(1)):
                folder_deletion.add(folder_num)
        elif m := file_entry_re.fullmatch(line):
            file_size = int(m.group(2))
            folder_size[cur_folder] += file_size
            if delete_re.search(m.group(1)):
                file_deletion[cur_folder] += file_size

    # Expand folders to be deleted.
    exploded_folder_deletion = set()
    exploded = set()
    while folder_deletion:
        folder = folder_deletion.pop()
        exploded_folder_deletion.add(folder)
        children = folder_children[folder]
        exploded_folder_deletion.update(children)
        for child in children:
            if child not in exploded:
                folder_deletion.add(child)
        exploded.add(folder)

    # Add up all the deletions.
    not_deleted = set(file_deletion) - exploded_folder_deletion
    result = sum(folder_size[folder] for folder in exploded_folder_deletion)
    result += sum(file_deletion[folder] for folder in not_deleted)
    return result


def connecting_cities(data: str) -> int:
    """Day 35 (2024/8): compute the number of permutations which sums to a target."""
    sample = "sample" in data
    options = {3, 2, 1} if sample else {40, 12, 2, 1}
    target = 5 if sample else 856

    @functools.cache
    def solve(target: int) -> int:
        if target == 0:
            return 1
        return sum(solve(target - option) for option in options if option <= target)

    return solve(target)


def mining_tunnels(data: str) -> int:
    """Day 36 (2024/9): return the shortest distance through a maze."""
    # Extract spaces and elevator 3D coordinates.
    spaces, elevators = (
        {
            (x, y, level)
            for level, floormap in enumerate(data.split("\n\n"))
            for y, line in enumerate(floormap.splitlines())
            for x, char in enumerate(line)
            if char in chars
        }
        for chars in (".$", "$")
    )
    assert all((x, y, 1 - level) in elevators for x, y, level in elevators)
    # Find the left-most and right-most spaces, i.e. the entrance and exist.
    start, end = (f(spaces, key=lambda x: x[0]) for f in (min, max))

    offsets = [(0, -1), (0, +1), (-1, 0), (+1, 0)]
    # Deptch first search.
    dq = collections.deque([(0, *start)])
    seen = set()
    while dq:
        step, x, y, level = dq.popleft()
        if (x, y, level) == end:
            return step
        # Consider left, right, up, down. And maybe elevators.
        options = [(x + dx, y + dy, level) for dx, dy in offsets]
        if (x, y, level) in elevators:
            options.append((x, y, 1 - level))
        for pos in options:
            if pos in spaces and pos not in seen:
                seen.add(pos)
                # Add one when not riding the elevator.
                next_step = step + (level == pos[2])
                dq.append((next_step, *pos))


FUNCS = {
    28: purchase_tickets,
    29: broken_firewall,
    30: hotel_door_code,
    31: closest_star_systems,
    32: busy_moon_rovers,
    33: playfair,
    34: the_purge,
    35: connecting_cities,
    36: mining_tunnels,
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
    if data:
        files = [data]
    else:
        input_file = pathlib.Path(f"input/{day:02}.txt")
        if not input_file.exists():
            response = requests.get(INPUT_ENDPOINT, params={"puzzle": f"{day:02}"})
            response.raise_for_status()
            input_file.write_text(response.text)
        files = [pathlib.Path(f"input/{day:02}.sample"), input_file]
    for file in files:
        if not file.exists():
            print(f"{file} does not exist.")
            continue
        start = time.perf_counter_ns()
        got = FUNCS[day](file.read_text().rstrip())
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

        print(f"Day {day:02} ({delta:4}{unit:<2}, {str(file):15}): {got}")


if __name__ == "__main__":
    main()

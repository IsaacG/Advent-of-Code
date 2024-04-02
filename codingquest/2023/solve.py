#!/bin/python
"""CodingQuest.io solver."""
from __future__ import annotations

import collections
import dataclasses
import functools
import math
import queue
import pathlib
import re
import statistics
import time
from typing import Optional

import click
import requests  # type: ignore

DAY_OFFSET = 17
# Regex used to detect an interger (positive or negative).
NUM_RE = re.compile("-?[0-9]+")
INPUT_ENDPOINT = "https://codingquest.io/api/puzzledata"
COLOR_SOLID = '█'
COLOR_EMPTY = ' '


def inventory_check(data: str) -> int:
    """1: Sum up inventory values. """
    counts: dict[str, int] = collections.defaultdict(int)
    for line in data.splitlines():
        _, count, category = line.split()
        counts[category] += int(count)
    return math.prod(count % 100 for count in counts.values())


def navigation_sensor(data: str) -> int:
    """2: Apply parity checks."""
    parity_mask = 1 << 15  # 0x8000
    value_mask = parity_mask - 1  # 0x7FFF

    values = []
    for line in data.splitlines():
        number = int(line)
        parity, value = bool(parity_mask & number), (value_mask & number)
        if value.bit_count() % 2 == parity:
            values.append(value)
    return round(statistics.mean(values))


def tic_tac_toe(data: str) -> int:
    """3: Score tic tac toe. 20938290."""
    # Game configuration.
    player_count, size = 2, 3
    # All possible ways to win.
    lines = [  # Horizontal
        set(range(i, i + size * size, size)) for i in range(size)
    ]
    lines.extend(  # Vertical
        set(range(i, i + size)) for i in range(0, size * size, size)
    )
    lines.append(set(range(0, size * size, size + 1)))  # Diagonal
    lines.append(set(range(size - 1, size * size - 1, size - 1)))  # Diagonal
    # Outcome counters.
    wins = {player: 0 for player in range(player_count)}
    draws = 0
    # Game logic.
    for line in data.splitlines():
        positions: dict[int, set[int]] = {player: set() for player in range(player_count)}
        for turn, move in enumerate(line.split()):
            positions[turn % player_count].add(int(move) - 1)
            if any(positions[turn % player_count].issuperset(line) for line in lines):
                wins[turn % player_count] += 1
                break
        else:
            draws += 1
    return math.prod(wins.values()) * draws


def packet_parsing(data: str) -> str:
    """4: Parsing a byte stream."""
    packets = collections.defaultdict(list)
    for line in data.splitlines():
        stream = iter(line)

        def read_n(n: int) -> int:
            return int("".join(next(stream) for _ in range(2 * n)), 16)

        header = read_n(2)
        if header != 0x5555:
            continue
        sender = read_n(4)
        sequence_number = read_n(1)
        checksum = read_n(1)
        message = [read_n(1) for _ in range(24)]
        if checksum != sum(message) % 256:
            continue
        packets[sender].append((sequence_number, message))

    message = [c for _, segment in sorted(list(packets.values())[0]) for c in segment]
    return "".join(chr(i) for i in message)


def overlapping_rectangles(data: str) -> str:
    """5: Toggle rectangles on and off, brute force."""
    grid = [[True] * 50 for _ in range(10)]
    for line in data.splitlines():
        xstart, ystart, width, height = (int(i) for i in line.split())
        for ypos in range(ystart, ystart + height):
            for xpos in range(xstart, xstart + width):
                grid[ypos][xpos] = not grid[ypos][xpos]
    return "\n".join(
        "".join(COLOR_EMPTY if col else COLOR_SOLID for col in row)
        for row in grid
    )


def astroid_field(data: str) -> str:
    """6: Find the gap in the astroid field."""
    filled = set()
    size, offset, duration = 100, 60 * 60, 60
    for line in data.splitlines():
        xstart, ystart, xspeed, yspeed = (float(i) for i in line.split())
        for steps in range(duration):
            seconds = offset + steps
            xpos = int(xstart + xspeed * seconds)
            ypos = int(ystart + yspeed * seconds)
            if 0 <= xpos < size and 0 <= ypos < size:
                filled.add((xpos, ypos))
    for xpos in range(size):
        for ypos in range(size):
            if (xpos, ypos) not in filled:
                return f"{xpos}:{ypos}"
    raise RuntimeError("Not solved.")


def snake(data: str) -> int:
    """7: Play the snake game."""
    # Parse the inputs, set up data.
    lines = data.splitlines()
    fruit_line, move_line = lines[1], lines[3]
    directions = {"U": complex(0, -1), "D": complex(0, 1), "L": complex(-1, 0), "R": complex(1, 0)}
    moves = (directions[i] for i in move_line)

    def to_complex(pair: str) -> complex:
        x, y = pair.split(",")
        return complex(int(x), int(y))

    fruits = (to_complex(pair) for pair in fruit_line.split())
    # Initialize game state.
    head = complex(0, 0)
    cur_fruit = next(fruits)
    body: collections.deque[complex] = collections.deque()
    body.append(head)
    score = 0
    # Play the game.
    for move in moves:
        head = head + move
        if head in body or any(not 0 <= i < 20 for i in (head.real, head.imag)):
            return score
        score += 1
        body.append(head)
        if head == cur_fruit:
            score += 100
            cur_fruit = next(fruits)
        else:
            body.popleft()
    raise RuntimeError("No move moves left.")


def traveling_salesman(data: str) -> int:
    """8: Brute force the traveling salesman."""
    # Create the cost matrix.
    distances = {
        start: {
            end: int(value)
            for end, value in enumerate(line.split())
        }
        for start, line in enumerate(data.splitlines())
    }

    @functools.cache
    def solve(current, to_visit):
        """Return the minimum cost of visiting all nodes starting at a given node."""
        # Add the cost to return to the start after all nodes are visited.
        if len(to_visit) == 0:
            return distances[current][0]
        # Return the minimum cost of visiting all nodes with each option as a candidate.
        return min(
            distances[current][candidate] + solve(candidate, frozenset(to_visit - {candidate}))
            for candidate in to_visit
        )

    return solve(0, frozenset(set(distances) - {0}))


def binary_tree_shape(data: str) -> int:
    """9: Compute the shape of a binary tree."""

    @dataclasses.dataclass
    class BTSNode:
        """Binary Tree Shape node."""

        value: int
        children: list[Optional[BTSNode]] = dataclasses.field(default_factory=lambda: [None] * 2)

        def insert(self, value: int) -> None:
            """Insert a value into the tree."""
            side = 0 if value < self.value else 1
            node = self[side]
            if node is None:
                self[side] = value
            else:
                node.insert(value)

        def depth(self) -> int:
            """Return the depth of the tree."""
            return 1 + max(
                0 if child is None else child.depth()
                for child in self.children
            )

        def __getitem__(self, key: int) -> Optional[BTSNode]:
            return self.children[key]

        def __setitem__(self, key: int, value: int) -> None:
            self.children[key] = BTSNode(value)

        def __hash__(self) -> int:
            return hash(self.value)

    # Initialize the tree with a 0 value root then fill it.
    tree = BTSNode(0)
    for line in data.splitlines():
        tree.insert(int(line, 16))

    # BFS to get the width at each level.
    nodes = {tree}
    max_width = 0
    while nodes:
        max_width = max(max_width, len(nodes))
        nodes = {i for n in nodes for i in n.children if i}

    return (tree.depth() - 1) * max_width


def shortest_path(data: str) -> int:
    """10: Find the shortest path through a graph."""
    wait_time = 600
    distances = {}
    for line in data.splitlines():
        src, _, *dests = line.split()
        distances[src] = {
            dest_dist[:3]: int(dest_dist[4:])
            for dest_dist in dests
        }

    todo: queue.PriorityQueue[tuple[int, str]] = queue.PriorityQueue()
    min_at = {"TYC": 0}
    todo.put((0, "TYC"))
    while not todo.empty():
        duration, position = todo.get()
        if position == "EAR":
            break
        for dest, dist in distances[position].items():
            cost = duration + wait_time + dist
            if dest not in min_at or cost < min_at[dest]:
                todo.put((cost, dest))
                min_at[dest] = cost

    # No need to wait at EAR
    return duration - wait_time


FUNCS = [
    inventory_check,
    navigation_sensor,
    tic_tac_toe,
    packet_parsing,
    overlapping_rectangles,
    astroid_field,
    snake,
    traveling_salesman,
    binary_tree_shape,
    shortest_path,
]


@click.command()
@click.option("--day", type=int, required=False)
@click.option("--data", type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path))
def main(day: int | None, data: Optional[pathlib.Path]):
    """Run the solver for a specific day."""
    if not day:
        day = len(FUNCS)
    if day > len(FUNCS):
        print(f"Day {day:02} not solved.")
        return
    if data:
        files = [data]
    else:
        input_file = pathlib.Path(f"input/{day:02}.txt")
        if not input_file.exists():
            response = requests.get(INPUT_ENDPOINT, params={"puzzle": f"{day + DAY_OFFSET:02}"})
            response.raise_for_status()
            input_file.write_text(response.text)
        files = [input_file]
    for file in files:
        if not file.exists():
            print(f"{file} does not exist.")
            continue
        start = time.perf_counter_ns()
        got = FUNCS[day - 1](file.read_text().rstrip())
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

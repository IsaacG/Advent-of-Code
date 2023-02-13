#!/bin/python

import collections
import functools
import itertools
import hashlib
import math
import pathlib
import queue
import re
import string
import time

import click
import humanize
import more_itertools
import png

NUM_RE = re.compile("-?[0-9]+")

def print_points(points, flip: bool) -> None:
    xmin = min(x for x, y in points.keys())
    xmax = max(x for x, y in points.keys())
    ymin = min(y for x, y in points.keys())
    ymax = max(y for x, y in points.keys())

    for y in range(ymin, ymax + 1):
        if flip:
            y = ymax - y
        line = [f"Row {y}: "]
        for x in range(xmin, xmax + 1):
            line.append(str(points.get((x, y), "_")))
        print("".join(line))
            



def rolling_average(data: str) -> int:
    lines = [int(i) for i in data.splitlines()]
    low = 1500 * 60
    high = 1600 * 60
    count = 0
    linecount = 0
    total = sum(lines[:59])
    for add, rem in zip(lines[59:], [0] + lines):
        total = total + add - rem
        if not low <= total <= high:
            count += 1
    return count


def lotto_winnings(data: str) -> int:
    winning_numbers = {12, 48, 30, 95, 15, 55, 97}
    values = {0: 0, 1: 0, 2: 0, 3: 1, 4: 10, 5: 100, 6: 1000}
    tickets = [[int(i) for i in line.split()] for line in data.splitlines()]
    total = 0
    for ticket in tickets:
        total += values[len([i for i in ticket if i in winning_numbers])]
    return total


def tour_length(data: str) -> int:
    total = 0
    lines = [[int(i) for i in line.split()] for line in data.splitlines()]
    for src, dest in zip(lines, lines[1:]):
        total += math.isqrt(sum((a - b) ** 2 for a, b in zip(src, dest)))
    return total


def connect_four(data: str) -> int:
    players = 3
    row_size = 4
    moves = {}
    wins = {i: 0 for i in range(players)}

    def rows(point: tuple[int, int]) -> list[list[tuple[int, int]]]:
        x, y = point
        return [
            [(x, y + i) for i in range(row_size)],
            [(x + i, y) for i in range(row_size)],
            [(x + i, y + i) for i in range(row_size)],
            [(x + i, y - i) for i in range(row_size)],
        ]

    def has_won(player: int) -> bool:
        for p in moves[player]:
            for row in rows(p):
                if all(q in moves[player] for q in row):
                    return True
        return False

    for line in data.splitlines():
        for i in range(players):
            moves[i] = set()
        height = [0] * 7
        for move, col in enumerate(line):
            column = int(col) - 1
            moves[move % players].add((column, height[column]))
            height[column] += 1
            if has_won(move % players):
                wins[move % players] += 1
                break
    return math.prod(wins.values())


def blockchain(data: str) -> str:
    prior_hash = data.splitlines()[0].split("|")[2]
    numbers = [
        821649, 1280359, 4675746, 7034044, 7103037, 8447017, 10479258,
        13953955, 17511092, 18147393, 20596537, 23807772, 35728140,
    ]
    for count, line in enumerate(data.splitlines()):
        desc, num, _, hash_out = line.split("|")
        hash_in = "|".join([desc, num, prior_hash]).encode("utf-8")
        if hashlib.sha256(hash_in).hexdigest() == hash_out:
            prior_hash = hash_out
        else:
            start = hashlib.sha256(f"{desc}|".encode("utf-8"))
            # for num in itertools.count():
            for num in itertools.count():
                c = start.copy()
                c.update(f"{num}|{prior_hash}".encode("utf-8"))
                hash_out = c.hexdigest()
                if hash_out.startswith("000000"):
                    prior_hash = hash_out
                    # print(f"Computed hash {hash_out} for {count} using {num}")
                    break
    return prior_hash


def cpu(data: str) -> str:
    variables = collections.defaultdict(int)
    max_instructions = 1000

    def lookup(name: str) -> int:
        if NUM_RE.match(name):
            return int(name)
        return variables[name]

    ptr = 0
    test = False
    out = []
    instructions = [line.split() for line in data.splitlines()]
    for step in range(max_instructions):
        match instructions[ptr]:
            case ["ADD", target, source]:
                variables[target] += lookup(source)
            case ["MOD", target, source]:
                variables[target] %= lookup(source)
            case ["DIV", target, source]:
                variables[target] //= lookup(source)
            case ["MOV", target, source]:
                variables[target] = lookup(source)
            case ["JMP", source]:
                ptr += lookup(source) - 1
            case ["JIF", source] if test:
                ptr += lookup(source) - 1
            case ["CEQ", this, that]:
                test = lookup(this) == lookup(that)
            case ["CGE", this, that]:
                test = lookup(this) >= lookup(that)
            case ["OUT", source]:
                out.append(str(lookup(source)))
            case ["END"]:
                break
        ptr += 1
    return "\n".join(out)


def heatshield(data: str) -> int:
    squares = [tuple(int(i) for i in line.split()) for line in data.splitlines()]
    xmax = 20000
    ymax = 100000
    if len(squares) == 3:
        xmax, ymax = 10, 10
    if len(squares) == 20:
        xmax, ymax = 100, 100

    if False:
        covered = set()
        for xstart, ystart, width, height in squares:
            for x in range(xstart, xstart + width):
                for y in range(ystart, ystart + height):
                    covered.add((x, y))

    to_add = queue.PriorityQueue()
    to_remove = queue.PriorityQueue()
    in_use = set()
    for square in squares:
        to_add.put((square[1], square))
    next_add = to_add.get()
    next_rem = None

    total = 0
    exposed = xmax
    for y in range(ymax):
        changed = False
        while next_rem is not None and next_rem[0] == y:
            # print(f"Row {y}: Drop {next_rem}")
            changed = True
            square = next_rem[1]
            in_use.remove(square)
            next_rem = None if to_remove.empty() else to_remove.get()

        while next_add is not None and next_add[0] == y:
            # print(f"Row {y}: Add {next_add}")
            changed = True
            square = next_add[1]
            in_use.add(square)
            remove = (square[1] + square[3], square)
            to_remove.put(remove)
            if next_rem is None:
                next_rem = to_remove.get()
            next_add = None if to_add.empty() else to_add.get()

        if changed:
            exposed = 0
            cur = 0
            for square in sorted(in_use, key=lambda square: square[0]):
                if cur < square[0]:
                    exposed += square[0] - cur
                cur = square[0] + square[2]
            if cur < xmax:
                exposed += xmax - cur
            # brute = sum((x, y) not in covered for x in range(xmax))
            # assert brute == exposed, f"Row {y}: {exposed=} {brute=}"

        total += exposed
    return total


def shift_cipher(data: str) -> str:
    key = "Roads? Where We're Going, We Don't Need Roads."
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,;:?! '()"
    message = data
    distances = itertools.cycle(chars.index(i) + 1 for i in key)
    charpad = list(reversed(chars)) * 2

    out = []
    for char, distance in zip(message, distances):
        if char in chars:
            char = charpad[charpad.index(char) + distance]
        out.append(char)
    return re.search(r" '([^']+)' ", "".join(out)).group(1)


def maze(data: str) -> str:
    walls = set()
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            if char == "#":
                walls.add((x, y))
    xmax = len(data.splitlines()[0]) - 1
    ymax = len(data.splitlines()) - 1

    xstart = next(x for x in range(xmax + 1) if (x, 0) not in walls)

    def neighbors(x: int, y: int) -> list[tuple[int, int]]:
        return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    seen = set()
    todo = collections.deque()
    todo.append((1, xstart, 0))

    while todo:
        steps, xcur, ycur = todo.popleft()
        if ycur == ymax:
            return steps
        for xnext, ynext in neighbors(xcur, ycur):
            if (xnext, ynext) in seen:
                continue
            if (xnext, ynext) in walls:
                continue
            if ynext < 0:
                continue
            seen.add((xnext, ynext))
            todo.append((steps + 1, xnext, ynext))


def png_message(data: str) -> str:
    imgfile = "input/10.png"
    rows = png.Reader(filename=imgfile).read()[2]
    last = ""
    for row in rows:
        out = []
        for bits in more_itertools.chunked((rgb[0] & 1 for rgb in more_itertools.chunked(row, 3)), 8):
            char = chr(sum(bit << pos for pos, bit in enumerate(reversed(bits))))
            if char in string.printable:
                out.append(char)
        if not out:
            return last
        last = "".join(out).split()[-1].strip(string.punctuation)


FUNCS = {
    1: rolling_average,
    2: lotto_winnings,
    3: tour_length,
    4: connect_four,
    5: blockchain,
    6: cpu,
    7: heatshield,
    8: shift_cipher,
    9: maze,
    10: png_message,
}


@click.command()
@click.option("--day", type=int, required=True)
def main(day: int):
    data = pathlib.Path(f"input/{day:02}.txt")
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

    print(f"Day {day} ({delta}{unit}): {got}")

if __name__ == "__main__":
    main()

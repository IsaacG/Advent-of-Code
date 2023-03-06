#!/bin/python

import collections
import functools
import itertools
import hashlib
import math
import pathlib
import re
import string
import time
from typing import Optional

import click
import humanize
import more_itertools
import png
import requests

# Regex used to detect an interger (positive or negative).
NUM_RE = re.compile("-?[0-9]+")
INPUT_ENDPOINT = "https://codingquest.io/api/puzzledata"


def rolling_average(data: str) -> int:
    """Return the number of 60s rolling average values outside the thresholds.

    Day 1.
    Rather than summing up 60 numbers over and over and over, a rolling sum can
    be maintained by adding a new number to the window and substracting the oldest
    value.
    """
    lines = [int(i) for i in data.splitlines()]
    # Rather than looking at averages, we can use the sums.
    # This means the thresholds need to be multiplied by the count, 60.
    low = 1500 * 60
    high = 1600 * 60
    total = 0
    # Start with the first 59 seconds loaded.
    window_sum = sum(lines[:59])
    # Walk the remaining entires, removing one value and adding a new value.
    for add, rem in zip(lines[59:], [0] + lines):
        window_sum = window_sum + add - rem
        if not low <= window_sum <= high:
            total += 1
    return total


def lotto_winnings(data: str) -> int:
    """Return the winnings from a lotta for a given set of tickets.

    Day 2.
    """
    winning_numbers = {12, 48, 30, 95, 15, 55, 97}
    values = {0: 0, 1: 0, 2: 0, 3: 1, 4: 10, 5: 100, 6: 1000}
    tickets = [[int(i) for i in line.split()] for line in data.splitlines()]
    return sum(
        values[len([i for i in ticket if i in winning_numbers])]
        for ticket in tickets
    )


def tour_length(data: str) -> int:
    """Return the total distance for a 3D tour route.

    Day 3.
    """
    lines = [[int(i) for i in line.split()] for line in data.splitlines()]
    return sum(
        math.isqrt(sum((a - b) ** 2 for a, b in zip(src, dest)))
        for src, dest in zip(lines, lines[1:])
    )


def connect_four(data: str) -> int:
    """Return the winners in connect four games.

    Day 4.
    """
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
    """Return the final SHA256 hash from a blockchain.

    Day 5.
    """
    prior_hash = data.splitlines()[0].split("|")[2]
    # The computation is expensive and slow (several minutes).
    # So I'm caching the computed mining numbers to speed things up on reruns.
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
                    break
    return prior_hash


def cpu(data: str) -> str:
    """Simulate a CPU and run instructions.

    Day 6.
    """
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
    """Return the number of points not covered by rectangles.

    Day 7.

    This uses a linesweep approach. By considering the sorted y-values of tiles,
    we can compute at which row another tile comes into play or is removed from play.
    Tiles can be "added" or "removed" in a presorted order.

    If no new tile applies to any given row, the row has the same exposure as
    the previous row.

    If we know which tiles are in play for a row, we can sort tiles by x-value and
    walk the row by jumping from row-start to tile-start to tile-end.
    """
    squares = set()
    for line in data.splitlines():
        xstart, ystart, width, height = [int(i) for i in line.split()]
        # Covert width/height to end column/row.
        squares.add((xstart, ystart, xstart + width, ystart + height))

    # Different grids for different inputs.
    if len(squares) == 3:
        xmax, ymax = 10, 10
    elif len(squares) == 20:
        xmax, ymax = 100, 100
    else:
        xmax, ymax = 20000, 100000

    # Sort tile starts by the start row.
    to_add = sorted(squares, key=lambda s: s[1], reverse=True)
    # Sort tile ends by the end row.
    to_remove = sorted(squares, key=lambda s: s[3], reverse=True)
    # Track which tiles are currently in play.
    in_use = set()

    total = 0
    exposed = 0
    changed = True
    for y in range(ymax):
        # Remove tiles which have gone out of play at this row.
        while to_remove and to_remove[-1][3] == y:
            changed = True
            in_use.remove(to_remove.pop())

        # Add tiles which go into play at this row.
        while to_add and to_add[-1][1] == y:
            changed = True
            in_use.add(to_add.pop())

        # If the tiles changed, update the exposure.
        if changed:
            changed = False
            exposed = 0
            cur = 0
            for square in sorted(in_use, key=lambda square: square[0]):
                xstart, _, xend, _ = square
                if cur < xstart:
                    exposed += xstart - cur
                if cur < xend:
                    cur = xend
            if cur < xmax:
                exposed += xmax - cur

        total += exposed

    return total


def shift_cipher(data: str) -> str:
    """Return a decoded message using a shift cipher.

    Day 8.
    """
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
    """Return the length of the shortest way through a maze.

    Day 9.
    Use breadth first search.
    """
    walls = set()
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            if char == "#":
                walls.add((x, y))
    xmax = len(data.splitlines()[0]) - 1
    ymax = len(data.splitlines()) - 1
    xstart = next(x for x in range(xmax + 1) if (x, 0) not in walls)

    seen = set()
    todo = collections.deque()
    todo.append((1, xstart, 0))

    while todo:
        steps, x, y = todo.popleft()
        if y == ymax:
            return steps
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for xnext, ynext in neighbors:
            if (xnext, ynext) in seen or (xnext, ynext) in walls or ynext < 0:
                continue
            seen.add((xnext, ynext))
            todo.append((steps + 1, xnext, ynext))


def png_message(data: str) -> str:
    """Return a message encoded inside a PNG file.

    Day 10.
    """
    imgfile = "input/10.png"
    rows = png.Reader(filename=imgfile).read()[2]
    last = ""
    for row in rows:
        out = []
        pixels = more_itertools.chunked(row, 3)
        byte_stream = more_itertools.chunked((rgb[0] & 1 for rgb in pixels), 8)
        for bits in byte_stream:
            char = chr(sum(bit << pos for pos, bit in enumerate(reversed(bits))))
            if char in string.printable:
                out.append(char)
        if not out:
            return last
        last = "".join(out).split()[-1].strip(string.punctuation)


def snakes_and_ladders(data: str) -> int:
    """Return the number of moves for a player to win the game.

    Day 13.
    """
    split_data = {True: [], False: []}
    for line in data.splitlines():
        split_data[len(line) == 3].append(line)
    board = []
    for i, line in enumerate(reversed(split_data[False])):
        squares = [int(i) for i in line.split()]
        if i % 2:
            squares.reverse()
        board.extend(squares)
    rolls = [int(i) for line in split_data[True] for i in line.split()]
    end = len(board) - 1

    positions = {1: 0, 2: 0}
    for steps, (roll, player) in enumerate(zip(rolls, itertools.cycle([1, 2])), start=2):
        positions[player] += roll
        if positions[player] > end:
            return player * (steps // 2)
        while board[positions[player]]:
            positions[player] += board[positions[player]]
            if positions[player] > end:
                return player * (steps // 2)


def wordle(data: str) -> str:
    """Return a Wordle solution based on prior guesses.

    Day 14.
    """
    setup = [("keyless", "YYBBYYG"), ("society", "YGYYYBB"), ("phobias", "BBGBGBG")]

    black = set()
    yellow = set()
    known_positions: dict[int, str] = {}
    known_not: dict[int, set[str]] = collections.defaultdict(set)
    char_set_by_color = {"B": black, "Y": yellow, "G": yellow}

    for word, score in setup:
        for position, (char, char_score) in enumerate(zip(word, score)):
            char_set_by_color[char_score].add(char)
            if char_score == "Y":
                known_not[position].add(char)
            if char_score == "G":
                known_positions[position] = char

    for word in data.splitlines():
        chars = set(word)
        if (
            chars & black
            or not chars >= yellow
            or any(c != known_positions[p] for p, c in enumerate(word) if p in known_positions)
            or any(c in known_not[p] for p, c in enumerate(word))
        ):
            continue
        return word


def astroid_sizes(data: str) -> int:
    """Return the average size of astroids.

    Day 15.
    """
    sizes = {
        (x, y): int(s)
        for y, line in enumerate(data.splitlines())
        for x, s in enumerate(line.split())
    }
    # Track all the unsorted sizes. Iterate until all pieces are grouped.
    todo = {p for p, s in sizes.items() if s}
    astroids = []
    while todo:
        parts = []
        # Pop one piece and add all adjacent pieces, grouping by adjacency.
        sub_todo = {todo.pop(),}
        while sub_todo:
            xy = sub_todo.pop()
            x, y = xy
            todo.discard(xy)
            parts.append(sizes[xy])
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            sub_todo.update(
                neighbor
                for neighbor in neighbors
                if neighbor in todo
            )
        astroids.append(sum(parts))
    return sum(astroids) // len(astroids)


def checksums(data: str) -> int:
    """Detect and repair a checksum error.

    Day 16.
    """
    rows = [[int(i, base=16) for i in line.split()] for line in data.splitlines()]
    y, x = [
        next(
            i
            for i, numbers in enumerate(dataset[:-1])
            if sum(numbers[:-1]) % 256 != numbers[-1]
        )
        for dataset in (rows, list(zip(*rows)))
    ]
    byte = rows[y][x]
    difference = (sum(rows[y][:-1]) - rows[y][-1]) % 256
    return byte * (byte - difference)


def huffman_decode(data: str) -> str:
    """Return a decoded message using Huffman encoding.

    Day 17.
    """
    table = {
        0b0010: "A", 0b0000: "E", 0b0001: "T", 0b0011: "I", 0b0100: "N",
        0b0101: "O", 0b0110: "S", 0b0111: "H", 0b10000: "R", 0b10001: "D",
        0b10010: "L", 0b10011: "U", 0b10100: "C", 0b10101: "M", 0b10110: "F",
        0b10111: "B", 0b1100000: "F", 0b1100001: "Y", 0b1100010: "W", 0b1100011: "G",
        0b1100100: "P", 0b1100101: "B", 0b1100110: "V", 0b1100111: "K", 0b1101000: "Q",
        0b1101001: "J", 0b1101010: "X", 0b1101011: "Z", 0b1110000: "0", 0b1110001: "1",
        0b1110010: "2", 0b1110011: "3", 0b1110100: "4", 0b1110101: "5", 0b1110110: "6",
        0b1110111: "7", 0b1111000: "8", 0b1111001: "9", 0b1111010: "_", 0b1111011: ".",
        0b1111100: "'", 0b1111111: "*",
    }

    # Convert a hex string to a stream of 0 and 1s.
    char_stream = iter(int(i) for i in bin(int(data, base=16)).removeprefix("0b"))
    out = []
    while True:
        # Read four bits to start.
        v = 0
        for _ in range(4):
            v = (v << 1) + next(char_stream)
        # Read additioonal bits until we have a table match.
        while v not in table:
            v = (v << 1) + next(char_stream)
        char = table[v]
        if char == "*":
            break
        out.append(char)
    return "".join(out)


def inventory_check(data: str) -> int:
    """Sum up inventory values.

    Day 18.
    """
    counts = collections.defaultdict(int)
    for line in data.splitlines():
        _, count, category = line.split()
        counts[category] += int(count)
    return math.prod(count % 100 for count in counts.values())



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
    13: snakes_and_ladders,
    14: wordle,
    15: astroid_sizes,
    16: checksums,
    17: huffman_decode,
    18: inventory_check,
}


@click.command()
@click.option("--day", type=int, required=True)
@click.option("--data", type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path))
def main(day: int, data: Optional[pathlib.Path]):
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

    print(f"Day {day} ({delta}{unit}): {got}")

if __name__ == "__main__":
    main()

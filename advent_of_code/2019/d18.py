#!/bin/python
"""Advent of Code, Day 18: Many-Worlds Interpretation. Collect all keys in a maze, unlocking doors to explore farther."""
import collections
import string
import typing

from lib import aoc


def build_edges(data: aoc.Map, nodes: dict[str, complex]) -> dict[str, dict[str, tuple[int, int]]]:
    """Return a map of all {start|key}-key pairs with the min distance and blocking doors."""
    edges: dict[str, dict[str, tuple[int, int]]] = {node: {} for node in nodes}
    # For each starting point, explore depth first to discover paths to keys.
    for start, pos in nodes.items():
        todo = collections.deque([(0, pos, 0)])
        seen = {pos}
        while todo:
            steps, pos, doors = todo.popleft()
            char = typing.cast(str, data.chars[pos])
            if char.islower() and char != start:
                edges[start][char] = (steps, doors)
            steps += 1
            for n in data.neighbors(pos):
                if n in seen:
                    continue
                seen.add(n)
                char = typing.cast(str, data.chars[n])
                new_doors = doors
                if char.isupper():
                    new_doors |= 1 << string.ascii_uppercase.index(char)
                todo.append((steps, n, new_doors))
    return edges


def solve_for(starts: list[str], edges: dict[str, dict[str, tuple[int, int]]]) -> int:
    """Return the minimum steps needed to collect all the keys."""
    # pylint: disable=too-many-locals
    num_keys = len(set(edges) - set(starts))
    todo: collections.deque[tuple] = collections.deque()
    num_bots = len(starts)
    for active in range(num_bots):
        todo.append((0, "".join(starts), 0, active))
    smallest = int(1e9)
    seen: dict[tuple, int] = {}

    while todo:
        steps, positions, got, active = todo.pop()
        if steps > smallest:
            continue
        if got.bit_count() == num_keys:
            smallest = min(steps, smallest)
            continue
        found = False
        # Try moving the active bot. Other move other bots if the active bot is stuck.
        for bot in range(active, active + num_bots):
            bot %= num_bots
            pos = positions[bot]
            for key, (distance, doors) in edges[pos].items():
                # Skip if we already have this key or if there is a locked door we cannot cross.
                n_key = 1 << string.ascii_lowercase.index(key)
                if n_key & got or doors & ~got:
                    continue
                # Build the new state.
                new_got = got | n_key
                t = list(positions)
                t[bot] = key
                new_positions = "".join(t)
                new_steps = steps + distance
                if (new_positions, new_got) in seen and seen[new_positions, new_got] <= new_steps:
                    continue
                seen[new_positions, new_got] = new_steps
                todo.append((new_steps, new_positions, new_got, bot))
                found = True
            # If the active bot is able to move, do not try other bots.
            if found and bot == active:
                break

    return smallest


def solve(data: str, part: int) -> int:
    if part == 2:
        board = aoc.CoordinatesParserC(ignore=None, origin_top_left=True).parse(data)

        center = board.coords["@"].copy().pop()
        board.update(center, "#")
        for i, n in enumerate([complex(-1, -1), complex(1, -1), complex(1, 1), complex(-1, 1)]):
            board.update(center + n, str(i))
        for n in board.neighbors(center):
            board.update(n, "#")

        data = aoc.render_char_map(
            typing.cast(dict[complex, str], board.chars), board.max_y + 1, board.max_x + 1
        )

    board = aoc.CoordinatesParserC(ignore="#", origin_top_left=True).parse(data)
    starts = list("@" if part == 1 else "0123")
    nodes: dict[str, complex] = {
        char: pos
        for pos, char in typing.cast(dict[complex, str], board.chars).items()
        if char.islower() or char in "@0123"
    }
    return solve_for(starts, build_edges(board, nodes))


PARSER = aoc.parse_one_str
SAMPLE = [
    """\
#########
#b.A.@.a#
#########""",
    """\
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################""",
    """\
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################""",
    """\
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################""",
    """\
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################""",
    """\
#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######""",
    """\
###############
#d.ABC.#.....a#
######...######
######.@.######
######...######
#b.....#.....c#
###############""",
    """\
#############
#DcBa.#.GhKl#
#.###...#I###
#e#d#.@.#j#k#
###C#...###J#
#fEbA.#.FgHi#
#############""",
    """\
#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba...BcIJ#
#####.@.#####
#nK.L...G...#
#M###N#H###.#
#o#m..#i#jk.#
#############""",
]
TESTS = [
    (1, SAMPLE[0], 8),
    (1, SAMPLE[1], 86),
    (1, SAMPLE[2], 132),
    (1, SAMPLE[3], 136),
    (1, SAMPLE[4], 81),
    (2, SAMPLE[5], 8),
    (2, SAMPLE[6], 24),
    (2, SAMPLE[7], 32),
    (2, SAMPLE[8], 72),
]

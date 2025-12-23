#!/bin/python
"""Advent of Code, Day 14: Parabolic Reflector Dish."""
from lib import aoc
InputType = tuple[set[tuple[int, int]], set[tuple[int, int]]]
STEPS_P2 = 1000000000


def cycle(edges, moving, stationary):
    """Tilt the board in four directions."""
    min_x, min_y, max_x, max_y = edges
    # This logic can be deduped by rotating the grid by 1j and looping 4x.
    # However, that seems to run 50% slower.
    north = (0, -1)
    west = (-1, 0)
    south = (0, 1)
    east = (1, 0)

    # North
    post_move = set(stationary)
    for rock in sorted(moving, key=lambda x: x[1], reverse=False):
        while (new_pos := (rock[0] + north[0], rock[1] + north[1])) not in post_move and rock[1] > min_y:
            rock = new_pos
        post_move.add(rock)
    moving = post_move - stationary

    # West
    post_move = set(stationary)
    for rock in sorted(moving, key=lambda x: x[0], reverse=False):
        while (new_pos := (rock[0] + west[0], rock[1] + west[1])) not in post_move and rock[0] > min_x:
            rock = new_pos
        post_move.add(rock)
    moving = post_move - stationary

    # South
    post_move = set(stationary)
    for rock in sorted(moving, key=lambda x: x[1], reverse=True):
        while (new_pos := (rock[0] + south[0], rock[1] + south[1])) not in post_move and rock[1] < max_y:
            rock = new_pos
        post_move.add(rock)
    moving = post_move - stationary

    # East
    post_move = set(stationary)
    for rock in sorted(moving, key=lambda x: x[0], reverse=True):
        while (new_pos := (rock[0] + east[0], rock[1] + east[1])) not in post_move and rock[0] < max_x:
            rock = new_pos
        post_move.add(rock)
    moving = post_move - stationary

    return moving


def solve(data: aoc.Map, part: int) -> int:
    """Tilt the board and see where things land."""
    height, stationary, moving = data.height, data.coords["#"], data.coords["O"]

    if part == 1:
        north = (0, -1)
        post_move = set(stationary)
        for rock in sorted(moving, key=lambda x: x[1]):
            while (new_pos := (rock[0] + north[0], rock[1] + north[1])) not in post_move and rock[1] > 0:
                rock = new_pos
            post_move.add(rock)
        moving = post_move - stationary
        return int(sum(height - rock[1] for rock in moving))

    # Find a cycle in the rotation.
    step_to_map = list[frozenset[tuple[int, int]]]()
    map_to_step = dict[frozenset[tuple[int, int]], int]()
    for step in range(STEPS_P2):
        moving = cycle(data.edges, moving, stationary)

        frozen = frozenset(moving)
        if frozen in map_to_step:
            cycle_size = step - map_to_step[frozen]
            remaining_steps = STEPS_P2 - step - 1
            remaining_steps %= cycle_size
            moving = set(step_to_map[map_to_step[frozen] + remaining_steps])
            break
        map_to_step[frozen] = step
        step_to_map.append(frozen)

    return int(sum(height - rock[1] for rock in moving))


SAMPLE = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
TESTS = [(1, SAMPLE, 136), (2, SAMPLE, 64)]
# vim:expandtab:sw=4:ts=4

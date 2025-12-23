#!/bin/python
"""Advent of Code, Day 15: Warehouse Woes."""
from lib import aoc
PARSER = str


def solve(data: str, part: int) -> int:
    """Solve the parts."""
    return (part1 if part == 1 else part2)(data)


def part1(data: str) -> int:
    board, instructions = aoc.ParseBlocks(
        [aoc.CoordinatesParserC(), aoc.parse_one_str]).parse(data)
    robot = board["@"].pop()
    walls, boxes = board["#O"]
    directions = (aoc.ARROW_DIRECTIONS[i] for i in instructions.replace("\n", ""))
    for direction in directions:
        distance = 1
        while robot + distance * direction in boxes:
            distance += 1
        if robot + distance * direction in walls:
            # Hit a wall. Cannot move in this direction.
            continue
        new_robot = robot + direction
        if distance > 1:
            boxes.remove(new_robot)
            boxes.add(robot + distance * direction)
        robot = new_robot

    return int(sum(b.imag * 100 + b.real for b in boxes))


def part2(data: str) -> int:
    for find, replace in [("#", "##"), ("O", "[]"), (".", ".."), ("@", "@.")]:
        data = data.replace(find, replace)
    board, instructions = aoc.ParseBlocks(
        [aoc.CoordinatesParserC(), aoc.parse_one_str]).parse(data)
    robot = board["@"].pop()
    walls, boxes = board["#["]

    directions = (aoc.ARROW_DIRECTIONS[i] for i in instructions.replace("\n", ""))
    for direction in directions:
        if direction in [1, -1]:
            # Sideways pushing, box size is one.
            distance = 1
            box_offset = 0 if direction == 1 else 1
            while robot + (distance + box_offset) * direction in boxes:
                distance += 2
            if robot + distance * direction not in walls:
                box = robot + direction * (1 if direction == 1 else 2)
                # Shift boxes over by 1.
                while box in boxes:
                    boxes.remove(box)
                    boxes.add(box + direction)
                    box += 2 * direction
                robot += direction
        else:
            # Vertical movement. Track which coordinates on each row are affected.
            pushing = {robot + direction}
            boxes_moved = set()
            while all(i not in walls for i in pushing):
                new_pushing = set()
                for i in pushing:
                    for j in [0, 1]:
                        if i - j in boxes:
                            boxes_moved.add(i - j)
                            new_pushing.add(i - j + direction)
                            new_pushing.add(i - j + direction + 1)
                if not new_pushing:
                    break
                pushing = new_pushing
            # Shuffle all the boxes.
            # Remove then add to avoid adding a box on top of an existing box
            # then removing both.
            if all(i not in walls for i in pushing):
                robot += direction
                boxes -= boxes_moved
                boxes |= {b + direction for b in boxes_moved}

    return int(sum(b.imag * 100 + b.real for b in boxes))


SAMPLE = [
    """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^""",  # 0
    """\
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<""",  # 8
    """\
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^""",
]
TESTS = [(1, SAMPLE[0], 10092), (1, SAMPLE[1], 2028), (2, SAMPLE[0], 9021)]
# vim:expandtab:sw=4:ts=4

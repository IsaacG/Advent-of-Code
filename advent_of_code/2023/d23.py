#!/bin/python
"""Advent of Code, Day 23: A Long Walk."""

import collections
import typing
from lib import aoc


def solve(data: aoc.Map, part: int) -> int:
    """Solve the parts."""
    return (part1 if part == 1 else part2)(data)


def part1(data: aoc.Map) -> int:
    """Return the max steps to the end, taking slopes into account."""
    board = typing.cast(dict[tuple[int, int], str], data.chars)
    min_y, max_y = data.min_y, data.max_y
    start = next(i for i, char in board.items() if i[1] == min_y and char == ".")
    end = next(i for i, char in board.items() if i[1] == max_y and char == ".")

    # Explore nodes, tracking the current location and all visited locations to get here.
    to_explore = [(start, {start})]
    max_steps = 0
    while to_explore:
        current_node, seen = to_explore.pop()
        # Track the max steps we saw when getting to the end.
        if current_node == end:
            max_steps = max(max_steps, len(seen))

        # Determine what nodes are viable as next steps.
        char = board[current_node]
        if char in aoc.ARROW_DIRECTIONS:
            options = [(
                current_node[0] + aoc.ARROW_DIRECTIONS_T[char][0],
                current_node[1] + aoc.ARROW_DIRECTIONS_T[char][1]
            )]
        else:
            options = [
                next_pos
                for next_pos in aoc.t_neighbors4(current_node)
                if board.get(next_pos, "#") != "#"
            ]
        # Add nodes for future exploration.
        for next_pos in options:
            if next_pos not in seen:
                to_explore.append((next_pos, seen | {next_pos}))

    # The path length includes the start node.
    # The correct step count should not include the start.
    return max_steps - 1


def compressed_graph(board: set[tuple[int, int]]) -> tuple[dict[int, dict[int, int]], int, int]:
    """Return a "hallway compressed" graph, i.e. a weighted graph between points of interest."""
    min_y, max_y = min(p[1] for p in board), max(p[1] for p in board)
    start_coord = next(i for i in board if i[1] == min_y)
    end_coord = next(i for i in board if i[1] == max_y)

    # Find all the interesting locations on the board, ignoring the hallways in between.
    forks = {coord for coord in board if len(set(aoc.t_neighbors4(coord)) & board) > 2}
    forks.add(start_coord)
    forks.add(end_coord)

    # Compute the longest distances between all interesting locations.
    longest_dist = collections.defaultdict[tuple[int, int], dict[tuple[int, int], int]](
        lambda: collections.defaultdict(int)
    )
    # For each start location, pick one direction and
    # walk down that hallway until hitting another fork.
    for coord in forks:
        neighbors = set(aoc.t_neighbors4(coord)) & board
        for current_node in neighbors:
            steps = 1
            prior = coord
            while current_node not in forks:
                steps += 1
                options = set(aoc.t_neighbors4(current_node)) & board
                current_node, prior = next(i for i in options if i != prior), current_node

            # Record the longest hallways between these two locations.
            dist = max(steps, longest_dist[coord][current_node])
            longest_dist[coord][current_node] = dist
            longest_dist[current_node][coord] = dist

    # Replace coordinates with `int` labels to reduce the storage needed to store paths.
    # Replace defaultdicts with dicts at the same time.
    labels = {coord: idx for idx, coord in enumerate(forks)}
    start, end = labels[start_coord], labels[end_coord]
    graph = {
        labels[start]: {
            labels[end]: distance
            for end, distance in data.items()
        }
        for start, data in longest_dist.items()
    }
    return graph, start, end


def part2(data: aoc.Map) -> int:
    """Return the max steps to the end, ignoring slopes."""
    board = {pos for pos, char in data.chars.items() if char != "#"}
    longest_dist, start, end = compressed_graph(board)

    # The end node is connected to exactly one fork.
    # If we solve to that fork, we can prune the graph once reaching it.
    penultimate_pos, penultimate_distance = list(longest_dist[end].items())[0]

    # Explore all paths, looking for the max steps to the end.
    max_steps = 0
    to_explore = [(0, start, {start})]

    while to_explore:
        steps, current_node, seen = to_explore.pop()
        # Stop when we get to the penultimate node.
        if current_node == penultimate_pos:
            max_steps = max(max_steps, steps)
        else:
            for next_pos, distance in longest_dist[current_node].items():
                if next_pos in seen:
                    continue

                # Optimization: prune when we can no longer out perform a prior max_steps.
                # Given the set of seen values, explore all reachable, unused nodes and assume
                # max distance to each node. See if that could do better.
                reachable = set()
                todo = {next_pos}
                while todo:
                    cur = todo.pop()
                    for neighbor in longest_dist[cur]:
                        if neighbor not in seen and neighbor not in reachable:
                            todo.add(neighbor)
                            reachable.add(neighbor)
                # Bail if we cannot reach the end.
                if penultimate_pos not in reachable:
                    continue
                # Bail if we cannot beat the prior record.
                possible_points = sum(max(longest_dist[node].values()) for node in reachable)
                if steps + possible_points < max_steps:
                    continue

                to_explore.append((steps + distance, next_pos, seen | {next_pos}))

    return max_steps + penultimate_distance


SAMPLE = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""
TESTS = [(1, SAMPLE, 94), (2, SAMPLE, 154)]
# vim:expandtab:sw=4:ts=4

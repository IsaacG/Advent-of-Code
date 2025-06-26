#!/bin/python
"""Advent of Code, Day 23: A Long Walk."""

import collections
from lib import aoc

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

InputType = dict[complex, str]


class Day23(aoc.Challenge):
    """Day 23: A Long Walk."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=94),
        aoc.TestCase(inputs=SAMPLE, part=2, want=154),
    ]
    TIMEOUT = 45

    def part1(self, puzzle_input: InputType) -> int:
        """Return the max steps to the end, taking slopes into account."""
        board = puzzle_input.chars
        _, min_y, _, max_y = aoc.bounding_coords(board)
        start = next(i for i, char in board.items() if i.imag == min_y and char == ".")
        end = next(i for i, char in board.items() if i.imag == max_y and char == ".")

        # Explore nodes, tracking the current location and all visited locations to get here.
        to_explore = [(start, {start})]
        max_steps = 0
        while to_explore:
            current_node, seen = to_explore.pop()
            # Track the max steps we saw when getting to the end.
            if current_node == end:
                new_len = len(seen)
                if new_len > max_steps:
                    max_steps = new_len

            # Determine what nodes are viable as next steps.
            char = board[current_node]
            if char in aoc.ARROW_DIRECTIONS:
                options = [current_node + aoc.ARROW_DIRECTIONS[char]]
            else:
                options = [
                    next_pos
                    for next_pos in aoc.neighbors(current_node)
                    if board.get(next_pos, "#") != "#"
                ]
            # Add nodes for future exploration.
            for next_pos in options:
                if next_pos not in seen:
                    to_explore.append((next_pos, seen | {next_pos}))

        # The path length includes the start node.
        # The correct step count should not include the start.
        return max_steps - 1

    def compressed_graph(self, board: set[complex]) -> tuple[dict[int, dict[int, int]], int, int]:
        """Return a "hallway compressed" graph, i.e. a weighted graph between points of interest."""
        _, min_y, _, max_y = aoc.bounding_coords(board)
        start_coord = next(i for i in board if i.imag == min_y)
        end_coord = next(i for i in board if i.imag == max_y)

        # Find all the interesting locations on the board, ignoring the hallways in between.
        forks = {coord for coord in board if len(set(aoc.neighbors(coord)) & board) > 2}
        forks.add(start_coord)
        forks.add(end_coord)

        # Compute the longest distances between all interesting locations.
        longest_dist: dict[complex, dict[complex, int]] = collections.defaultdict(lambda: collections.defaultdict(int))
        # For each start location, pick one direction and
        # walk down that hallway until hitting another fork.
        for coord in forks:
            neighbors = set(aoc.neighbors(coord)) & board
            for current_node in neighbors:
                steps = 1
                prior = coord
                while current_node not in forks:
                    steps += 1
                    options = set(aoc.neighbors(current_node)) & board
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

    def part2(self, puzzle_input: InputType) -> int:
        """Return the max steps to the end, ignoring slopes."""
        board = {pos for pos, char in puzzle_input.chars.items() if char != "#"}
        longest_dist, start, end = self.compressed_graph(board)

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
                if steps > max_steps:
                    max_steps = steps
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

# vim:expandtab:sw=4:ts=4
